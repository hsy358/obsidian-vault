"""
---
title: Hermes chat adapter（德勤 M6 执行与日志）
date: 2026-07-01
type: code-reference
purpose: 封装 hermes chat CLI，使其表现为统一执行器接口，并输出结构化日志
related:
  - /root/vault/1-Projects/德勤/AI-Native/executor/abstract-interface.md
  - /root/vault/1-Projects/德勤/AI-Native/executor/log-schema.json
  - /root/vault/1-Projects/德勤/AI-Native/executor/demo-report.md
---
"""

"""
Hermes chat adapter（德勤 M6）

这个文件的定位是：
1. 把 `hermes chat -q -Q -m ...` 封装成一个统一执行器。
2. 提供 submit / heartbeat / logs / pause / resume / terminate 五类接口。
3. 用最小实现满足“输入、状态、失败原因、输出文件可查看”的 MVP 验收。

说明：
- 这是面向 demo / 参考实现的 adapter，不追求完整生产级调度能力。
- 当前采用“内存态任务注册表 + 本地 JSONL 日志文件”的最小方案。
- pause / resume 在 MVP 中是逻辑状态，便于统一接口先跑通。
"""

from __future__ import annotations

import json
import shutil
import subprocess
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT_DIR / "runtime"
LOG_DIR = RUNTIME_DIR / "logs"
ARTIFACT_DIR = RUNTIME_DIR / "artifacts"
DEFAULT_MODEL = "custom/gpt-5.4"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ExecutorError(RuntimeError):
    """统一执行器错误。"""

    def __init__(
        self,
        error_code: str,
        message: str,
        retryable: bool = False,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.retryable = retryable
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        return {
            "error_code": self.error_code,
            "message": self.message,
            "retryable": self.retryable,
            "details": self.details,
        }


@dataclass
class ExecutorTask:
    title: str
    prompt: str
    executor: str = "hermes-chat"
    workspace: str | None = None
    context: dict[str, Any] = field(default_factory=dict)
    artifacts_dir: str | None = None
    timeout_seconds: int = 300
    metadata: dict[str, Any] = field(default_factory=dict)
    task_id: str | None = None


@dataclass
class TaskRecord:
    task_id: str
    task: ExecutorTask
    command: list[str]
    process: subprocess.Popen[str] | None = None
    status: str = "queued"
    started_at: str | None = None
    finished_at: str | None = None
    output_files: list[str] = field(default_factory=list)
    failure_reason: str | None = None
    token_cost: float | None = None
    raw_output: str = ""
    exit_code: int | None = None


class HermesChatAdapter:
    """Hermes CLI 执行器封装。"""

    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        self.model = model
        self.tasks: dict[str, TaskRecord] = {}
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    def submit(self, task: ExecutorTask) -> str:
        self._validate_task(task)
        task_id = task.task_id or f"hermes-{uuid.uuid4().hex[:8]}"
        artifacts_dir = Path(task.artifacts_dir or ARTIFACT_DIR / task_id)
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        output_path = artifacts_dir / "response.txt"

        command = [
            "hermes",
            "chat",
            "-q",
            task.prompt,
            "-Q",
            "-m",
            self.model,
        ]

        record = TaskRecord(
            task_id=task_id,
            task=task,
            command=command,
            status="running",
            started_at=iso_now(),
        )
        self.tasks[task_id] = record
        self._append_log(record, input_text=task.prompt)

        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=task.timeout_seconds,
                cwd=task.workspace or str(ROOT_DIR),
                check=False,
            )
        except FileNotFoundError as exc:
            record.status = "failed"
            record.finished_at = iso_now()
            record.failure_reason = "hermes CLI not found"
            self._append_log(record, input_text=task.prompt)
            raise ExecutorError(
                "E_SUBMIT_FAILED",
                "failed to start hermes chat process",
                retryable=False,
                details={"executor": task.executor, "raw_error": str(exc)},
            ) from exc
        except subprocess.TimeoutExpired as exc:
            record.status = "failed"
            record.finished_at = iso_now()
            record.failure_reason = f"timeout after {task.timeout_seconds}s"
            record.raw_output = exc.stdout or ""
            self._append_log(record, input_text=task.prompt)
            raise ExecutorError(
                "E_TIMEOUT",
                "hermes chat timed out",
                retryable=True,
                details={"timeout_seconds": task.timeout_seconds},
            ) from exc

        record.exit_code = completed.returncode
        record.raw_output = (completed.stdout or "") + (completed.stderr or "")
        output_path.write_text(completed.stdout or "", encoding="utf-8")
        record.output_files = [str(output_path)]
        record.finished_at = iso_now()

        if completed.returncode == 0:
            record.status = "succeeded"
        else:
            record.status = "failed"
            record.failure_reason = (completed.stderr or completed.stdout or "unknown error").strip()

        self._append_log(record, input_text=task.prompt)
        return task_id

    def heartbeat(self, task_id: str) -> str:
        record = self._get_task(task_id)
        return record.status

    def logs(self, task_id: str) -> list[dict[str, Any]]:
        self._get_task(task_id)
        path = self._log_path(task_id)
        if not path.exists():
            raise ExecutorError("E_LOG_READ_FAILED", f"log file missing for {task_id}")
        rows = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows

    def pause(self, task_id: str) -> str:
        record = self._get_task(task_id)
        if record.status == "running":
            record.status = "paused"
            self._append_log(record, input_text=record.task.prompt)
        return record.status

    def resume(self, task_id: str) -> str:
        record = self._get_task(task_id)
        if record.status == "paused":
            record.status = "running"
            self._append_log(record, input_text=record.task.prompt)
        return record.status

    def terminate(self, task_id: str) -> str:
        record = self._get_task(task_id)
        record.status = "terminated"
        record.finished_at = record.finished_at or iso_now()
        record.failure_reason = record.failure_reason or "terminated by operator"
        self._append_log(record, input_text=record.task.prompt)
        return record.status

    def _append_log(self, record: TaskRecord, input_text: str) -> None:
        payload = {
            "task_id": record.task_id,
            "executor": record.task.executor,
            "started_at": record.started_at,
            "finished_at": record.finished_at,
            "status": record.status,
            "input": input_text,
            "output_files": record.output_files,
            "failure_reason": record.failure_reason,
            "token_cost": record.token_cost,
            "event_type": "task_update",
            "raw_output_excerpt": record.raw_output[:500],
            "exit_code": record.exit_code,
            "logged_at": iso_now(),
        }
        with self._log_path(record.task_id).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def _log_path(self, task_id: str) -> Path:
        return LOG_DIR / f"{task_id}.jsonl"

    def _get_task(self, task_id: str) -> TaskRecord:
        record = self.tasks.get(task_id)
        if not record:
            raise ExecutorError("E_TASK_NOT_FOUND", f"unknown task_id: {task_id}")
        return record

    def _validate_task(self, task: ExecutorTask) -> None:
        if not task.title.strip() or not task.prompt.strip():
            raise ExecutorError("E_INVALID_TASK", "task title and prompt must be non-empty")
        if task.executor != "hermes-chat":
            raise ExecutorError(
                "E_EXECUTOR_NOT_FOUND",
                f"unsupported executor for HermesChatAdapter: {task.executor}",
            )
        if shutil.which("hermes") is None:
            raise ExecutorError("E_SUBMIT_FAILED", "hermes CLI not found in PATH")


def build_demo_task() -> ExecutorTask:
    """构造一个最小可跑 demo 任务。"""

    return ExecutorTask(
        title="Hermes chat 最小执行 demo",
        prompt="用一句中文总结：Hermes executor adapter 已接入，并输出结构化日志。",
        executor="hermes-chat",
        workspace=str(ROOT_DIR),
        artifacts_dir=str(ARTIFACT_DIR / "hermes-demo"),
        timeout_seconds=300,
        context={"project": "deloitte-ai-native-mvp", "phase": "M6"},
    )


def run_demo() -> dict[str, Any]:
    """运行最小 demo，并返回摘要。"""

    adapter = HermesChatAdapter()
    task = build_demo_task()
    task_id = adapter.submit(task)
    events = adapter.logs(task_id)
    latest = events[-1]

    return {
        "task_id": task_id,
        "status": adapter.heartbeat(task_id),
        "log_events": len(events),
        "output_files": latest["output_files"],
        "failure_reason": latest["failure_reason"],
    }


if __name__ == "__main__":
    print(json.dumps(run_demo(), ensure_ascii=False, indent=2))
