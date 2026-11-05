"""调度内核（只做四件事：收事件 → 按规则分活 → 派活 → 记每一步）

对应 Agent Autoloop 的 decide.ts，但用德勤口径重写：
- 规则是**人工维护 + 确定性匹配**，内核不调用模型；
- AI 自规划若要存在，只能发生在**执行层 Agent 侧**（回执 ask / 续跑），并受内核熔断约束；
- 授权不可变：每轮都记录规则 version + 内容哈希。
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from . import MAX_HOPS
from .events import EventRejected, NormalizedEvent, json_dumps, looks_like_injection, normalize
from .executors import DispatchTask, ExecutionResult, ExecutorRegistry
from .rules import Rule, RuleSet, redact, render_prompt
from .store import Mutation, Store, iso_now


@dataclass
class IngestOutcome:
    accepted: bool
    event_id: int
    reason: str | None = None
    run_ids: list[int] | None = None
    injection_hits: list[str] | None = None


class Kernel:
    """内核。"""

    def __init__(
        self,
        store: Store,
        ruleset: RuleSet,
        executors: ExecutorRegistry | None = None,
    ) -> None:
        self.store = store
        self.ruleset = ruleset
        self.executors = executors or ExecutorRegistry()

    # ------------------------------------------------------------ 收事件

    def ingest(self, raw: dict[str, Any], parent_run_id: int | None = None) -> IngestOutcome:
        """收一条外部事件。控制字段 → 整条拒收；通过则按规则分活。"""
        try:
            event = normalize(raw)
        except EventRejected as exc:
            detail = dict(exc.detail)
            detail["raw_keys"] = sorted(raw.keys()) if isinstance(raw, dict) else []
            ids = self.store.apply([
                Mutation(
                    "INSERT INTO events(ts, source, type, subject, fingerprint, text, "
                    "payload_json, accepted, reject_reason, injection_hits) "
                    "VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (
                        iso_now(),
                        str(raw.get("source", "?")) if isinstance(raw, dict) else "?",
                        str(raw.get("type", "?")) if isinstance(raw, dict) else "?",
                        str(raw.get("subject", "")) if isinstance(raw, dict) else "",
                        "",
                        "",
                        json_dumps(detail),
                        0,
                        exc.reason,
                        None,
                    ),
                    want_rowid=True,
                ),
            ])
            self.store.fact("event_rejected", {"reason": exc.reason, **detail})
            return IngestOutcome(accepted=False, event_id=ids[0], reason=exc.reason)

        hits = looks_like_injection(event.text)
        payload = event.payload()
        mutations = [
            Mutation(
                "INSERT INTO events(ts, source, type, subject, fingerprint, text, "
                "payload_json, accepted, reject_reason, injection_hits) "
                "VALUES(?,?,?,?,?,?,?,?,?,?)",
                (
                    iso_now(),
                    event.source,
                    event.type,
                    event.subject,
                    event.fingerprint,
                    event.text,
                    json_dumps(payload),
                    1,
                    None,
                    json_dumps(hits) if hits else None,
                ),
                want_rowid=True,
            ),
        ]
        ids = self.store.apply(mutations)
        event_id = ids[0]
        self.store.fact(
            "event_accepted",
            {"event_id": event_id, "source": event.source, "type": event.type,
             "subject": event.subject, "injection_hits": hits},
        )
        if hits:
            # 不删原文、不静默：标记 + 事实留痕，是否升级人工由规则决定
            self.store.fact("injection_suspected", {"event_id": event_id, "hits": hits})

        run_ids = self._plan(event, event_id, parent_run_id)
        return IngestOutcome(
            accepted=True,
            event_id=event_id,
            run_ids=run_ids,
            injection_hits=hits,
        )

    # ------------------------------------------------------------ 分活

    def _plan(self, event: NormalizedEvent, event_id: int, parent_run_id: int | None) -> list[int]:
        rules = self.ruleset.find(event.source, event.type)
        if not rules:
            self.store.fact("no_rule_matched", {"event_id": event_id, "type": event.type})
            return []

        # 跳数熔断：事件链层数超限 → 拒派
        hops = 1
        parent = self.store.get_run(parent_run_id) if parent_run_id else None
        if parent is not None:
            hops = int(parent["hops"]) + 1
            chain_key = parent["chain_key"] or f"chain:{parent['id']}"
        else:
            # 链的起点：一条新事件自己开一条链
            chain_key = f"chain:{event_id}"

        run_ids: list[int] = []
        for rule in rules:
            lane = event.subject or event.fingerprint
            chain = self.store.get_chain(chain_key)
            if chain is not None and int(chain["melted"]):
                # 链已熔断：后续同链事件一律拒派（熔断不得被"链断了"绕过）
                self.store.fact(
                    "chain_melted",
                    {"rule": rule.name, "chain": chain_key, "hops": int(chain["hops"])},
                )
                continue

            if hops > min(rule.max_hops, MAX_HOPS):
                self.store.upsert_chain(chain_key, hops=hops, melted=True)
                self.store.fact(
                    "hops_exceeded",
                    {"rule": rule.name, "hops": hops, "max_hops": min(rule.max_hops, MAX_HOPS),
                     "parent_run": parent_run_id, "chain": chain_key},
                )
                continue
            existing = self.store.active_runs_for_lane(rule.group, lane)
            if existing is not None:
                # 同一交付物上的连续事件 → 合并进现有轮次，不新开
                self.store.fact(
                    "event_merged",
                    {"rule": rule.name, "lane": lane, "into_run": existing["id"], "event_id": event_id},
                    run_id=int(existing["id"]),
                )
                run_ids.append(int(existing["id"]))
                continue

            # 组内并发上限
            active = self.store.count_active_in_group(rule.group)
            if active >= rule.parallel:
                self.store.fact(
                    "deferred_by_group_limit",
                    {"rule": rule.name, "group": rule.group, "active": active, "limit": rule.parallel},
                )

            state = "queued"
            if rule.mode == "observe":
                state = "observed"  # 首投灰度：只记录不执行
            self.store.upsert_chain(chain_key, hops=hops, melted=False)
            prompt = render_prompt(rule, event.fields)
            prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
            created = iso_now()
            ids = self.store.apply([
                Mutation(
                    "INSERT INTO runs(created_at, rule, rule_version, rule_digest, agent_use, agent_name, "
                    "access_json, cwd, skill, group_name, lane, chain_key, state, hops, mode, prompt, prompt_hash, "
                    "event_id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        created,
                        rule.name,
                        self.ruleset.version,
                        self.ruleset.digest,
                        rule.to.use,
                        rule.to.name,
                        json_dumps(list(rule.to.access)),
                        rule.cwd,
                        rule.skill,
                        rule.group,
                        lane,
                        chain_key,
                        state,
                        hops,
                        rule.mode,
                        prompt,
                        prompt_hash,
                        event_id,
                    ),
                    want_rowid=True,
                ),
            ])
            run_id = ids[0]
            run_ids.append(run_id)
            self.store.fact(
                "rule_matched",
                {
                    "rule": rule.name,
                    "rule_version": self.ruleset.version,
                    "rule_digest": self.ruleset.digest[:12],
                    "agent_use": rule.to.use,
                    "mode": rule.mode,
                    "lane": lane,
                    "hops": hops,
                },
                run_id=run_id,
            )
            self.store.fact("run_created", {"state": state, "prompt_hash": prompt_hash[:12]}, run_id=run_id)
            if state == "observed":
                self.store.fact(
                    "observe_mode_skipped_execution",
                    {"note": "首投 observe：只记录不执行，人工核对后再放开"},
                    run_id=run_id,
                )
        return run_ids

    # ------------------------------------------------------------ 派活

    def dispatch_pending(self, limit: int = 20) -> list[tuple[int, ExecutionResult]]:
        """取排队中的轮次并执行。observe/dry 的处理在此收口。"""
        rows = self.store.query(
            "SELECT * FROM runs WHERE state = 'queued' ORDER BY id LIMIT ?", (limit,)
        )
        results: list[tuple[int, ExecutionResult]] = []
        for row in rows:
            run_id = int(row["id"])
            rule = self._rule_by_name(row["rule"])
            if rule is None:
                self._finish(run_id, "failed", None, "规则已不存在（规则集变更后未重建）")
                continue
            if rule.mode == "observe":
                self._finish(run_id, "skipped", None, "observe 模式不执行")
                results.append((run_id, ExecutionResult(status="skipped", output="observe")))
                continue

            task = DispatchTask(
                task_id=f"run-{run_id}",
                prompt=row["prompt"],
                agent=rule.to,
                cwd=row["cwd"],
                skill=row["skill"],
                context={"run_id": run_id, "rule": row["rule"], "rule_version": row["rule_version"]},
            )
            self.store.apply([
                Mutation("UPDATE runs SET state='running', started_at=? WHERE id=?", (iso_now(), run_id))
            ])
            self.store.fact("run_started", {"executor": rule.to.use}, run_id=run_id)
            try:
                executor = self.executors.get(rule.to.use)
                result = executor.run(task)
            except KeyError as exc:
                result = ExecutionResult(status="failed", failure_reason=str(exc))
            except Exception as exc:  # 执行器炸了也不能让内核状态失真
                result = ExecutionResult(status="failed", failure_reason=f"执行器异常: {exc}")

            self._finish(run_id, result.status, result, None)
            results.append((run_id, result))
        return results

    def _finish(
        self,
        run_id: int,
        state: str,
        result: ExecutionResult | None,
        failure_reason: str | None,
    ) -> None:
        reason = failure_reason or (result.failure_reason if result else None)
        output = redact(result.output) if result else ""
        self.store.apply([
            Mutation(
                "UPDATE runs SET state=?, finished_at=?, result=?, failure_reason=? WHERE id=?",
                (state, iso_now(), output[:4000], reason, run_id),
            )
        ])
        self.store.fact(
            "run_finished",
            {
                "state": state,
                "failure_reason": reason,
                "exit_code": result.exit_code if result else None,
                "duration_ms": result.duration_ms if result else None,
                "token_cost": result.token_cost if result else None,
            },
            run_id=run_id,
        )

    def _rule_by_name(self, name: str) -> Rule | None:
        for r in self.ruleset.rules:
            if r.name == name:
                return r
        return None

    # ------------------------------------------------------------ 审计

    def why(self, run_id: int) -> list[dict[str, Any]]:
        """还原某一轮"为什么这么跑"（基线 #5）。"""
        run = self.store.get_run(run_id)
        if run is None:
            return []
        chain = [
            {
                "ts": run["created_at"],
                "kind": "run_created",
                "detail": {
                    "rule": run["rule"],
                    "rule_version": run["rule_version"],
                    "rule_digest": run["rule_digest"][:12],
                    "agent_use": run["agent_use"],
                    "mode": run["mode"],
                    "hops": run["hops"],
                },
            }
        ]
        for f in self.store.run_facts(run_id):
            chain.append({
                "ts": f["ts"],
                "kind": f["kind"],
                "detail": json.loads(f["data_json"]),
            })
        return chain

    def status(self) -> dict[str, Any]:
        rows = self.store.query(
            "SELECT state, COUNT(*) AS c FROM runs GROUP BY state ORDER BY state"
        )
        counts = {r["state"]: int(r["c"]) for r in rows}
        meta = self.store.latest_rules_meta()
        return {
            "rules_version": meta["version"] if meta else None,
            "rules_digest": (meta["digest"][:12] if meta else None),
            "runs": counts,
            "total_runs": sum(counts.values()),
        }
