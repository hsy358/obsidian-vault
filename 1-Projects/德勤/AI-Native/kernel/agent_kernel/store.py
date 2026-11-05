"""状态存储（内核基线 #1/#5：唯一写入点 + 单事务；事件溯源）

- 全部状态变更只能经由 :meth:`Store.apply` 进入，内部**单事务**：要么全成，要么全不成。
- `facts` 表只追加不修改 —— 这是审计链的底座（`why` 命令据此还原"为什么这么跑"）。
- 只用标准库 sqlite3，**零第三方依赖**；内核不出网（基线 #6）。
"""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator

SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS events (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    ts            TEXT NOT NULL,
    source        TEXT NOT NULL,
    type          TEXT NOT NULL,
    subject       TEXT NOT NULL,
    fingerprint   TEXT NOT NULL,
    text          TEXT NOT NULL DEFAULT '',
    payload_json  TEXT NOT NULL,
    accepted      INTEGER NOT NULL,
    reject_reason TEXT,
    injection_hits TEXT
);

CREATE TABLE IF NOT EXISTS runs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at    TEXT NOT NULL,
    rule          TEXT NOT NULL,
    rule_version  INTEGER NOT NULL,
    rule_digest   TEXT NOT NULL,
    agent_use     TEXT NOT NULL,
    agent_name    TEXT NOT NULL,
    access_json   TEXT NOT NULL,
    cwd           TEXT,
    skill         TEXT,
    group_name    TEXT NOT NULL,
    lane          TEXT NOT NULL,
    chain_key     TEXT NOT NULL DEFAULT '',
    state         TEXT NOT NULL,
    hops          INTEGER NOT NULL DEFAULT 1,
    mode          TEXT NOT NULL,
    prompt        TEXT NOT NULL,
    prompt_hash   TEXT NOT NULL,
    event_id      INTEGER,
    result        TEXT,
    failure_reason TEXT,
    started_at    TEXT,
    finished_at   TEXT
);

CREATE TABLE IF NOT EXISTS facts (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    ts       TEXT NOT NULL,
    run_id   INTEGER,
    kind     TEXT NOT NULL,
    data_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chains (
    chain_key  TEXT PRIMARY KEY,
    hops       INTEGER NOT NULL DEFAULT 0,
    melted     INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rules_meta (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    version    INTEGER NOT NULL,
    digest     TEXT NOT NULL,
    installed_at TEXT NOT NULL,
    path       TEXT
);

CREATE INDEX IF NOT EXISTS idx_facts_run ON facts(run_id, id);
CREATE INDEX IF NOT EXISTS idx_runs_state ON runs(state);
CREATE INDEX IF NOT EXISTS idx_events_fp ON events(fingerprint);
"""

#: 终态（不可再流转）
TERMINAL_STATES = frozenset({"succeeded", "failed", "rejected", "skipped", "terminated"})


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Mutation:
    """一次原子变更里的一个动作。"""

    sql: str
    params: tuple[Any, ...] = ()
    # 取回新插入行的 id（可选）
    want_rowid: bool = False


class Store:
    """内核唯一的状态出口。"""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.path), isolation_level=None)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(SCHEMA)

    def close(self) -> None:
        self._conn.close()

    # ---------------------------------------------------------------- 写

    def apply(self, mutations: Iterable[Mutation]) -> list[int]:
        """唯一写入口：单事务执行全部 mutation，全成或全滚。

        返回每个 mutation 的 lastrowid（未指定 want_rowid 的为 -1）。
        """
        mutations = list(mutations)
        ids: list[int] = []
        self._conn.execute("BEGIN IMMEDIATE")
        try:
            for m in mutations:
                cur = self._conn.execute(m.sql, m.params)
                ids.append(cur.lastrowid if m.want_rowid else -1)
            self._conn.execute("COMMIT")
        except Exception:
            self._conn.execute("ROLLBACK")
            raise
        return ids

    def fact(self, kind: str, data: dict[str, Any], run_id: int | None = None) -> int:
        """追加一条审计事实。"""
        ids = self.apply([
            Mutation(
                "INSERT INTO facts(ts, run_id, kind, data_json) VALUES(?,?,?,?)",
                (iso_now(), run_id, kind, json.dumps(data, ensure_ascii=False, sort_keys=True)),
                want_rowid=True,
            )
        ])
        return ids[0]

    def facts(self, kind: str, data: dict[str, Any], run_id: int | None = None) -> int:
        return self.fact(kind, data, run_id)

    # ---------------------------------------------------------------- 读

    def query(self, sql: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
        return list(self._conn.execute(sql, params))

    def one(self, sql: str, params: tuple[Any, ...] = ()) -> sqlite3.Row | None:
        rows = self.query(sql, params)
        return rows[0] if rows else None

    def get_run(self, run_id: int) -> sqlite3.Row | None:
        return self.one("SELECT * FROM runs WHERE id = ?", (run_id,))

    def run_facts(self, run_id: int) -> list[sqlite3.Row]:
        return self.query("SELECT * FROM facts WHERE run_id = ? ORDER BY id", (run_id,))

    def active_runs_for_lane(self, group_name: str, lane: str) -> sqlite3.Row | None:
        """同 group+lane 上仍在排队/执行的轮次（用于事件合并）。"""
        return self.one(
            "SELECT * FROM runs WHERE group_name = ? AND lane = ? "
            "AND state IN ('queued','running') ORDER BY id LIMIT 1",
            (group_name, lane),
        )

    def count_active_in_group(self, group_name: str) -> int:
        row = self.one(
            "SELECT COUNT(*) AS c FROM runs WHERE group_name = ? AND state IN ('queued','running')",
            (group_name,),
        )
        return int(row["c"]) if row else 0

    def get_chain(self, chain_key: str) -> sqlite3.Row | None:
        return self.one("SELECT * FROM chains WHERE chain_key = ?", (chain_key,))

    def upsert_chain(self, chain_key: str, hops: int, melted: bool = False) -> None:
        """链级状态：记录该链已走到第几跳，以及是否已熔断。

        没有这张表，熔断会因"链断了"而被绕过 —— 链必须记住自己已经熔断。
        """
        self.apply([
            Mutation(
                "INSERT INTO chains(chain_key, hops, melted, updated_at) VALUES(?,?,?,?) "
                "ON CONFLICT(chain_key) DO UPDATE SET hops=excluded.hops, "
                "melted=excluded.melted, updated_at=excluded.updated_at",
                (chain_key, hops, 1 if melted else 0, iso_now()),
            )
        ])

    def install_ruleset(self, version: int, digest: str, path: str | None) -> None:
        self.apply([
            Mutation(
                "INSERT INTO rules_meta(version, digest, installed_at, path) VALUES(?,?,?,?)",
                (version, digest, iso_now(), path),
            )
        ])

    def latest_rules_meta(self) -> sqlite3.Row | None:
        return self.one("SELECT * FROM rules_meta ORDER BY id DESC LIMIT 1")

    @contextmanager
    def read_only(self) -> Iterator[sqlite3.Connection]:
        yield self._conn
