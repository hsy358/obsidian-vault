from __future__ import annotations

"""
---
title: Claude Code adapter（德勤 M6 执行与日志）
date: 2026-07-01
type: code-reference
purpose: 封装 Claude Code CLI 或 mock runner，使其表现为统一执行器接口，并输出结构化日志
related:
  - /root/vault/1-Projects/德勤/AI-Native/executor/abstract-interface.md
  - /root/vault/1-Projects/德勤/AI-Native/executor/log-schema.json
  - /root/vault/1-Projects/德勤/AI-Native/executor/adapters/hermes-chat-adapter.py
---
"""

"""
Claude Code adapter（德勤 M6）

这个文件的定位是：
1. 为 Claude Code / ACP 类执行器提供与 Hermes chat 一致的抽象接口。
2. 优先尝试真实 `claude -p` CLI；若环境中不可用，则自动退化到 mock。
3. 让 demo 即使没有正式 Claude Code SDK，也能验证接口与日志 schema。

说明：
- 德勤本轮验收重点是“至少两类执行器”与“日志可见”，因此 mock 是明确允许的。
- 当前实现依然采用“内存态任务注册表 + 本地 JSONL 日志文件”的最小策略。
- 与 Hermes chat adapter 保持同一套字段与方法名，便于上层注册表统一调度。
"""

import json
import shutil
import subprocess
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT_DIR / "runtime"
LOG_DIR = RUNTIME_DIR / "logs"
ARTIFACT_DIR = RUNTIME_DIR / "artifacts"


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
    executor: str = "claude-code"
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
    status: str = "queued"
    started_at: str | None = None
    finished_at: str | None = None
    output_files: list[str] = field(default_factory=list)
    failure_reason: str | None = None
    token_cost: float | None = None
    raw_output: str = ""
    exit_code: int | None = None
    execution_mode: str = "mock"


class ClaudeCodeAdapter:
    """Claude Code / ACP 执行器封装。"""

    def __init__(self) -> None:
        self.tasks: dict[str, TaskRecord] = {}
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    def submit(self, task: ExecutorTask) -> str:
        self._validate_task(task)
        task_id = task.task_id or f"claude-{uuid.uuid4().hex[:8]}"
        artifacts_dir = Path(task.artifacts_dir or ARTIFACT_DIR / task_id)
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        output_path = artifacts_dir / "response.txt"

        command, execution_mode = self._build_command(task)
        record = TaskRecord(
            task_id=task_id,
            task=task,
            command=command,
            status="running",
            started_at=iso_now(),
            execution_mode=execution_mode,
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
        except subprocess.TimeoutExpired as exc:
            record.status = "failed"
            record.finished_at = iso_now()
            record.failure_reason = f"timeout after {task.timeout_seconds}s"
            timeout_stdout = exc.stdout.decode("utf-8", errors="ignore") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            record.raw_output = timeout_stdout
            self._append_log(record, input_text=task.prompt)
            raise ExecutorError(
                "E_TIMEOUT",
                "claude execution timed out",
                retryable=True,
                details={"timeout_seconds": task.timeout_seconds, "mode": execution_mode},
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
        return self._get_task(task_id).status

    def logs(self, task_id: str) -> list[dict[str, Any]]:
        self._get_task(task_id)
        path = self._log_path(task_id)
        if not path.exists():
            raise ExecutorError("E_LOG_READ_FAILED", f"log file missing for {task_id}")
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

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

    def _build_command(self, task: ExecutorTask) -> tuple[list[str], str]:
        if shutil.which("claude"):
            return ["claude", "-p", task.prompt], "cli"

        mock_text = (
            "Claude Code mock runner executed successfully. "
            f"Prompt summary: {task.prompt[:120]}"
        )
        return ["python3", "-c", f"print({mock_text!r})"], "mock"

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
            "execution_mode": record.execution_mode,
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
        if task.executor != "claude-code":
            raise ExecutorError(
                "E_EXECUTOR_NOT_FOUND",
                f"unsupported executor for ClaudeCodeAdapter: {task.executor}",
            )


def build_demo_task() -> ExecutorTask:
    """构造一个最小可跑 demo 任务。"""

    return ExecutorTask(
        title="Claude Code 最小执行 demo",
        prompt="生成一句中文说明：Claude Code adapter 已被统一执行器抽象层接入。",
        executor="claude-code",
        workspace=str(ROOT_DIR),
        artifacts_dir=str(ARTIFACT_DIR / "claude-demo"),
        timeout_seconds=300,
        context={"project": "deloitte-ai-native-mvp", "phase": "M6"},
    )


def run_demo() -> dict[str, Any]:
    """运行最小 demo，并返回摘要。"""

    adapter = ClaudeCodeAdapter()
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
        "execution_mode": latest.get("execution_mode", "unknown"),
    }


if __name__ == "__main__":
    print(json.dumps(run_demo(), ensure_ascii=False, indent=2))
