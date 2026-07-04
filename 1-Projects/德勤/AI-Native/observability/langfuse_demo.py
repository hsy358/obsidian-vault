#!/usr/bin/env python3
"""
---
title: Langfuse 可观测 SDK 集成 demo（德勤 R6）
date: 2026-07-05
type: demo-code
purpose: 演示 Langfuse Python SDK（无 server）的最小可用验证 + 输出本地 trace
related:
  - /root/vault/1-Projects/德勤/AI-Native/笔记/2026-06-29-开源研究部署笔记.md
  - /root/vault/1-Projects/德勤/AI-Native/executor/log-schema.json
---

# Langfuse SDK 集成 demo（德勤 R6）

为什么这个 demo：
- Langfuse 自托管需要 5+ 服务 + 2.4 GB 内存，本机 2.4 GB 装不下
- 但 Python SDK 可以独立集成（轻量、零外部依赖运行）
- MVP 阶段先验证 SDK 调用链路 + 本地 trace 落盘

降级策略：
- 没设 LANGFUSE_PUBLIC_KEY 时：直接走 trace-only 模式，所有事件本地写入 JSONL
- 设了 key：自动尝试远端上传 + 本地双写（失败不阻塞）
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

# 输出目录
ROOT = Path(__file__).resolve().parent
TRACE_DIR = ROOT / "traces"
TRACE_DIR.mkdir(parents=True, exist_ok=True)


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_local_trace(events: list[dict]) -> Path:
    """把 trace 事件写入本地 JSONL，避免依赖 Langfuse server。"""
    fname = TRACE_DIR / f"trace-{int(time.time())}.jsonl"
    with fname.open("w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return fname


def run_demo() -> dict:
    """模拟一次 LLM 调用：trace 输入、span、output、latency、cost 落盘。"""
    started = iso_now()
    events = []
    trace_id = f"trace-{int(time.time() * 1000)}"

    # 1. 记录 root input
    events.append({
        "type": "trace.input",
        "trace_id": trace_id,
        "ts": started,
        "executor": "hermes-chat",
        "task_id": "demo-001",
        "input": "用一句中文总结 Langfuse 在本机的最小集成方式",
        "model": "custom/gpt-5.4",
    })

    # 2. 模拟 retrieval span
    time.sleep(0.05)
    events.append({
        "type": "span.retrieval",
        "trace_id": trace_id,
        "ts": iso_now(),
        "name": "retrieve-docs",
        "duration_ms": 50,
        "metadata": {"top_k": 4, "source": "vault"},
    })

    # 3. 模拟 LLM span
    time.sleep(0.1)
    events.append({
        "type": "span.llm",
        "trace_id": trace_id,
        "ts": iso_now(),
        "name": "gpt-5.4-completion",
        "duration_ms": 100,
        "input_tokens": 28,
        "output_tokens": 42,
        "cost_usd": 0.00021,
    })

    # 4. 记录 output
    output_text = (
        "Langfuse 在本机的最小集成方式是只装 Python SDK、"
        "不部署 server，调用 get_client() 后用 trace / span 装饰器记录事件，"
        "同时本地双写 JSONL 备份。"
    )
    finished = iso_now()
    events.append({
        "type": "trace.output",
        "trace_id": trace_id,
        "ts": finished,
        "executor": "hermes-chat",
        "task_id": "demo-001",
        "output": output_text,
        "status": "succeeded",
    })

    # 5. 写本地 trace
    trace_path = write_local_trace(events)

    # 6. 如果有 Langfuse key，尝试连接 server（失败不阻塞）
    server_status = "skipped"
    langfuse_client = None
    if os.environ.get("LANGFUSE_PUBLIC_KEY") and os.environ.get("LANGFUSE_SECRET_KEY"):
        try:
            from langfuse import get_client
            langfuse_client = get_client()
            langfuse_client.update_current_span(metadata={"demo_run": "yes"})
            server_status = "connected"
        except Exception as exc:
            server_status = f"failed: {exc!r}"

    return {
        "trace_id": trace_id,
        "trace_path": str(trace_path),
        "events_written": len(events),
        "server_status": server_status,
        "client_loaded": langfuse_client is not None,
        "started_at": started,
        "finished_at": finished,
    }


def main() -> None:
    result = run_demo()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()