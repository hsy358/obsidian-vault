from __future__ import annotations

"""
---
title: olmOCR adapter（德勤 AgentSpace 工具层 POC）
date: 2026-07-06
type: code-skeleton
purpose: 为 Hermes-based 德勤 MVP 提供脏 PDF -> 干净 Markdown 的预处理层 adapter 骨架
related:
  - /root/vault/1-Projects/德勤/AI-Native/executor/abstract-interface.md
  - /root/vault/1-Projects/德勤/AI-Native/executor/langgraph-adapter.py
  - /root/vault/1-Projects/德勤/AI-Native/executor/tooling-stack-adapters.md
---
"""

"""
olmOCR adapter（德勤 AgentSpace 工具层 POC）

定位：
1. 这是文档预处理服务 adapter，不是执行器。
2. 它负责把扫描 PDF、双栏论文、表格型文档转成干净 Markdown。
3. 上层执行器只关心输入、状态、失败原因和输出文件。

当前状态：
- 这是 POC 骨架，默认用占位输出模拟解析结果。
- 后续可接本地 GPU 服务、vLLM 托管模型，或 OpenAI 兼容 OCR API。
- 保留最小 checkpoint 字段，便于批量任务恢复与审计。
"""

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = ROOT_DIR / "runtime" / "olmocr"
LOG_DIR = RUNTIME_DIR / "logs"
ARTIFACT_DIR = RUNTIME_DIR / "artifacts"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class OlmOCRTask:
    title: str
    document_path: str
    target_format: str = "markdown"
    provider: str = "local-vllm"
    artifacts_dir: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    task_id: str | None = None


@dataclass
class OlmOCRRecord:
    task_id: str
    task: OlmOCRTask
    status: str = "queued"
    started_at: str | None = None
    finished_at: str | None = None
    output_files: list[str] = field(default_factory=list)
    failure_reason: str | None = None
    checkpoint: dict[str, Any] = field(default_factory=dict)
    raw_output_excerpt: str = ""


class OlmOCRAdapter:
    """脏 PDF -> 干净 Markdown 的预处理层 adapter 骨架。"""

    def __init__(self) -> None:
        self.tasks: dict[str, OlmOCRRecord] = {}
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    def submit(self, task: OlmOCRTask) -> str:
        task_id = task.task_id or f"olmocr-{uuid.uuid4().hex[:8]}"
        record = OlmOCRRecord(
            task_id=task_id,
            task=task,
            status="running",
            started_at=iso_now(),
            checkpoint={
                "phase": "render",
                "pages_total": None,
                "pages_completed": 0,
            },
        )
        self.tasks[task_id] = record
        self._append_log(record)

        artifacts_dir = Path(task.artifacts_dir or ARTIFACT_DIR / task_id)
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        markdown_path = artifacts_dir / "parsed.md"
        markdown_path.write_text(
            "# OCR Result\n\nTODO: 这里替换为 olmOCR 输出的干净 Markdown。\n",
            encoding="utf-8",
        )

        record.output_files = [str(markdown_path)]
        record.checkpoint = {
            "phase": "completed",
            "pages_total": 1,
            "pages_completed": 1,
        }
        record.status = "succeeded"
        record.finished_at = iso_now()
        record.raw_output_excerpt = "POC markdown artifact generated"
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

    def _append_log(self, record: OlmOCRRecord) -> None:
        payload = {
            "task_id": record.task_id,
            "executor": "olmocr-service",
            "started_at": record.started_at,
            "finished_at": record.finished_at,
            "status": record.status,
            "input": {
                "document_path": record.task.document_path,
                "target_format": record.task.target_format,
                "provider": record.task.provider,
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
