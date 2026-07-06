from __future__ import annotations

"""
---
title: OpenWiki adapter（德勤 AgentSpace 工具层 POC）
date: 2026-07-06
type: code-skeleton
purpose: 为 Hermes-based 德勤 MVP 提供代码仓库 -> Agent 可读 Wiki 的独立工具层 adapter 骨架
related:
  - /root/vault/1-Projects/德勤/AI-Native/executor/abstract-interface.md
  - /root/vault/1-Projects/德勤/AI-Native/executor/langgraph-adapter.py
  - /root/vault/1-Projects/德勤/AI-Native/executor/tooling-stack-adapters.md
---
"""

"""
OpenWiki adapter（德勤 AgentSpace 工具层 POC）

定位：
1. 这是工具/服务层 adapter，不是新的执行器。
2. 它负责把代码仓库、现有文档、git 证据转换为 Agent 可读 Wiki。
3. Hermes / Claude Code / Codex / LangGraph 都可以作为调用方发起请求。

当前状态：
- 这是 POC 骨架，重点是接口边界、日志结构和独立部署思路。
- 真实环境中可对接本地 runner、Docker service 或 OpenAI 兼容 API。
- 保留最小 checkpoint 风格，便于后续接持久化任务状态。
"""

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = ROOT_DIR / "runtime" / "openwiki"
LOG_DIR = RUNTIME_DIR / "logs"
ARTIFACT_DIR = RUNTIME_DIR / "artifacts"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class OpenWikiTask:
    title: str
    repo_path: str
    mode: str = "update"
    git_head: str | None = None
    existing_docs: list[str] = field(default_factory=list)
    artifacts_dir: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    task_id: str | None = None


@dataclass
class OpenWikiRecord:
    task_id: str
    task: OpenWikiTask
    status: str = "queued"
    started_at: str | None = None
    finished_at: str | None = None
    output_files: list[str] = field(default_factory=list)
    failure_reason: str | None = None
    raw_output_excerpt: str = ""
    checkpoint: dict[str, Any] = field(default_factory=dict)


class OpenWikiAdapter:
    """代码仓库 -> Agent Wiki 的工具层 adapter 骨架。"""

    def __init__(self) -> None:
        self.tasks: dict[str, OpenWikiRecord] = {}
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    def submit(self, task: OpenWikiTask) -> str:
        task_id = task.task_id or f"openwiki-{uuid.uuid4().hex[:8]}"
        record = OpenWikiRecord(
            task_id=task_id,
            task=task,
            status="running",
            started_at=iso_now(),
            checkpoint={
                "phase": "plan",
                "evidence_collected": False,
                "wiki_written": False,
            },
        )
        self.tasks[task_id] = record
        self._append_log(record)

        # POC: 这里只生成占位 artifact，后续替换为真实 wiki service 调用。
        artifacts_dir = Path(task.artifacts_dir or ARTIFACT_DIR / task_id)
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        quickstart_path = artifacts_dir / "quickstart.md"
        quickstart_path.write_text(
            "# Quickstart\n\nTODO: 从代码仓库和 git 证据生成 Agent 可读入口页。\n",
            encoding="utf-8",
        )

        record.output_files = [str(quickstart_path)]
        record.checkpoint = {
            "phase": "completed",
            "evidence_collected": True,
            "wiki_written": True,
        }
        record.status = "succeeded"
        record.finished_at = iso_now()
        record.raw_output_excerpt = "POC quickstart.md generated"
        self._append_log(record)
        return task_id

    def heartbeat(self, task_id: str) -> str:
        return self.tasks[task_id].status

    def logs(self, task_id: str) -> list[dict[str, Any]]:
        path = self._log_path(task_id)
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def terminate(self, task_id: str) -> str:
        record = self.tasks[task_id]
        record.status = "terminated"
        record.finished_at = record.finished_at or iso_now()
        record.failure_reason = record.failure_reason or "terminated by operator"
        self._append_log(record)
        return record.status

    def _append_log(self, record: OpenWikiRecord) -> None:
        payload = {
            "task_id": record.task_id,
            "executor": "openwiki-service",
            "started_at": record.started_at,
            "finished_at": record.finished_at,
            "status": record.status,
            "input": {
                "repo_path": record.task.repo_path,
                "mode": record.task.mode,
                "git_head": record.task.git_head,
            },
            "output_files": record.output_files,
            "failure_reason": record.failure_reason,
            "checkpoint": record.checkpoint,
            "raw_output_excerpt": record.raw_output_excerpt,
            "logged_at": iso_now(),
        }
        with self._log_path(record.task_id).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def _log_path(self, task_id: str) -> Path:
        return LOG_DIR / f"{task_id}.jsonl"
