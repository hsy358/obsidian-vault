from __future__ import annotations

"""
---
title: mcp-toolbox adapter（德勤 AgentSpace 工具层 POC）
date: 2026-07-06
type: code-skeleton
purpose: 为 Hermes-based 德勤 MVP 提供数据库 -> 受限 SQL 工具 的数据层 adapter 骨架
related:
  - /root/vault/1-Projects/德勤/AI-Native/executor/abstract-interface.md
  - /root/vault/1-Projects/德勤/AI-Native/executor/langgraph-adapter.py
  - /root/vault/1-Projects/德勤/AI-Native/executor/tooling-stack-adapters.md
---
"""

"""
mcp-toolbox adapter（德勤 AgentSpace 工具层 POC）

定位：
1. 这是数据库工具服务 adapter，不是新的执行器。
2. 它负责通过 MCP 或 HTTP 调用受限 SQL / schema 工具。
3. 核心目标是把数据库访问收敛进可审计、可控边界，而不是给 Agent 直接高权限连库。

当前状态：
- 这是 POC 骨架，默认生成占位 JSON 结果。
- 后续可接真实 mcp-toolbox server、tools.yaml 和权限控制。
- 保留最小 checkpoint 与 query audit 字段，便于后续补审计链路。
"""

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = ROOT_DIR / "runtime" / "mcp_toolbox"
LOG_DIR = RUNTIME_DIR / "logs"
ARTIFACT_DIR = RUNTIME_DIR / "artifacts"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ToolboxTask:
    title: str
    datasource_id: str
    tool_name: str
    params: dict[str, Any] = field(default_factory=dict)
    artifacts_dir: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    task_id: str | None = None


@dataclass
class ToolboxRecord:
    task_id: str
    task: ToolboxTask
    status: str = "queued"
    started_at: str | None = None
    finished_at: str | None = None
    output_files: list[str] = field(default_factory=list)
    failure_reason: str | None = None
    checkpoint: dict[str, Any] = field(default_factory=dict)
    raw_output_excerpt: str = ""


class MCPToolboxAdapter:
    """数据库 -> 受限 SQL 工具 的数据层 adapter 骨架。"""

    def __init__(self) -> None:
        self.tasks: dict[str, ToolboxRecord] = {}
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    def submit(self, task: ToolboxTask) -> str:
        task_id = task.task_id or f"toolbox-{uuid.uuid4().hex[:8]}"
        record = ToolboxRecord(
            task_id=task_id,
            task=task,
            status="running",
            started_at=iso_now(),
            checkpoint={
                "phase": "dispatch",
                "query_audited": False,
                "tool_invoked": False,
            },
        )
        self.tasks[task_id] = record
        self._append_log(record)

        artifacts_dir = Path(task.artifacts_dir or ARTIFACT_DIR / task_id)
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        result_path = artifacts_dir / "result.json"
        result_path.write_text(
            json.dumps(
                {
                    "datasource_id": task.datasource_id,
                    "tool_name": task.tool_name,
                    "params": task.params,
                    "rows": [],
                    "note": "TODO: 替换为真实 mcp-toolbox 返回值",
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        record.output_files = [str(result_path)]
        record.checkpoint = {
            "phase": "completed",
            "query_audited": True,
            "tool_invoked": True,
        }
        record.status = "succeeded"
        record.finished_at = iso_now()
        record.raw_output_excerpt = "POC query result artifact generated"
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

    def _append_log(self, record: ToolboxRecord) -> None:
        payload = {
            "task_id": record.task_id,
            "executor": "mcp-toolbox-service",
            "started_at": record.started_at,
            "finished_at": record.finished_at,
            "status": record.status,
            "input": {
                "datasource_id": record.task.datasource_id,
                "tool_name": record.task.tool_name,
                "params": record.task.params,
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
