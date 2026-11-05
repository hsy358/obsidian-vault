"""执行器适配（内核基线 #7：厂商中立）

内核只认 `use` 这个**标识**，不关心背后是 Hermes、Claude Code 还是 LangGraph；
也不关心它们各自怎么启动、怎么算钱。

对齐德勤已有资产：`executor/abstract-interface.md` 的 ExecutorTask / ExecutorStatus / LogEvent，
以及 `executor/log-schema.json` 的统一日志字段。
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from .rules import AgentSpec


@dataclass
class ExecutionResult:
    """统一执行结果（字段对齐 log-schema.json）。"""

    status: str  # succeeded / failed / terminated / unknown
    output: str = ""
    failure_reason: str | None = None
    output_files: list[str] = field(default_factory=list)
    token_cost: float | None = None
    exit_code: int | None = None
    duration_ms: int | None = None

    def to_log_event(self, task_id: str, executor: str, started_at: str, finished_at: str) -> dict[str, Any]:
        """转成德勤统一的 LogEvent 结构。"""
        return {
            "task_id": task_id,
            "executor": executor,
            "started_at": started_at,
            "finished_at": finished_at,
            "status": self.status,
            "input": "",
            "output_files": list(self.output_files),
            "failure_reason": self.failure_reason,
            "token_cost": self.token_cost,
            "raw_output_excerpt": (self.output or "")[:2000],
            "exit_code": self.exit_code,
            "logged_at": finished_at,
        }


class Executor(Protocol):
    """执行器协议。"""

    def run(self, task: "DispatchTask") -> ExecutionResult:  # pragma: no cover - 协议
        ...


@dataclass
class DispatchTask:
    """内核派给执行器的东西。字段刻意保持最小且中立。"""

    task_id: str
    prompt: str
    agent: AgentSpec
    cwd: str | None
    skill: str | None
    timeout_seconds: int = 600
    context: dict[str, Any] = field(default_factory=dict)


class DryRunExecutor:
    """空执行器：不调用任何模型，只回显派活内容。

    用途：MVP 联调、回归测试、客户现场首投 observe 前的"干跑"。
    """

    def run(self, task: DispatchTask) -> ExecutionResult:
        started = time.time()
        summary = f"[dryrun] 已按规则派活：use={task.agent.use} name={task.agent.name}"
        return ExecutionResult(
            status="succeeded",
            output=summary,
            token_cost=None,
            exit_code=0,
            duration_ms=int((time.time() - started) * 1000),
        )


class CommandExecutor:
    """通用命令执行器：`command` 里的 {prompt} 会被替换。

    注意（实跑验证发现）：命令模式**拿不到 token/费用**，
    需要精确成本统计时必须写专用 adapter（见 executor/adapters/）。
    """

    def __init__(self, default_timeout: int = 600) -> None:
        self.default_timeout = default_timeout

    def run(self, task: DispatchTask) -> ExecutionResult:
        cmd = [c.replace("{prompt}", task.prompt) for c in task.agent.command]
        if not cmd:
            return ExecutionResult(status="failed", failure_reason="规则未提供 command")
        started = time.time()
        try:
            proc = subprocess.run(
                cmd,
                cwd=task.cwd or None,
                capture_output=True,
                text=True,
                timeout=task.timeout_seconds or self.default_timeout,
                env={**os.environ, "AGENT_KERNEL_TASK_ID": task.task_id},
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                status="failed",
                failure_reason=f"执行超时（>{task.timeout_seconds}s）",
                exit_code=None,
                duration_ms=int((time.time() - started) * 1000),
            )
        except FileNotFoundError as exc:
            return ExecutionResult(
                status="failed",
                failure_reason=f"命令不存在: {exc}",
                exit_code=127,
                duration_ms=int((time.time() - started) * 1000),
            )
        status = "succeeded" if proc.returncode == 0 else "failed"
        return ExecutionResult(
            status=status,
            output=(proc.stdout or "")[-8000:],
            failure_reason=None if status == "succeeded" else f"退出码 {proc.returncode}",
            output_files=[],
            token_cost=None,
            exit_code=proc.returncode,
            duration_ms=int((time.time() - started) * 1000),
        )


class ExecutorRegistry:
    """按 use 取执行器；未知 use 直接失败（厂商中立，但不放任）。"""

    def __init__(self) -> None:
        self._executors: dict[str, Executor] = {
            "dryrun": DryRunExecutor(),
            "custom": CommandExecutor(),
        }

    def register(self, use: str, executor: Executor) -> None:
        self._executors[use] = executor

    def get(self, use: str) -> Executor:
        if use not in self._executors:
            raise KeyError(f"未注册的执行器: {use}（已注册: {sorted(self._executors)}）")
        return self._executors[use]


def write_log_event(path: str | Path, event: dict[str, Any]) -> None:
    """把 LogEvent 追加成 JSONL（对齐 executor 层日志约定）。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")
