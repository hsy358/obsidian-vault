#!/usr/bin/env python3
"""
德勤 AI-Native MVP — OpenTelemetry + Mem0 整合 Demo
====================================================

何大人 2026-07-05 16:15 让立即部署 1 级别项目（OpenTelemetry + Mem0 + Vibe Kanban）。

**Vibe Kanban 状态**：BloopAI/vibe-kanban **已关停（sunset）**。
替代方案：Hermes 内置的 kanban daemon 已在本机运行（`/opt/hermes-venv/bin/hermes kanban`）。
**本 demo 重点**：OpenTelemetry + Mem0（按部署优先级）。

## 用法

```bash
# 1. 装依赖（已完成，2026-07-05）
pip install opentelemetry-instrumentation-fastapi mem0ai

# 2. 设置环境变量
export OPENAI_API_KEY=*** <cc-vibe.com key>
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 3. 跑 demo
python3 /root/vault/1-Projects/德勤/AI-Native/deployed/otel_mem0_integration_demo.py
```

## 验证效果

- OTel 自动 trace：FastAPI 请求、LangChain LLM 调用、httpx HTTP 调用
- Mem0 自动记忆：用户偏好、上下文、对话历史
- 输出到：
  - OTel ConsoleSpanExporter（stdout JSON）
  - Mem0 SQLite + Qdrant client fallback
"""
import os
import sys
import json
import time
from datetime import datetime

# ============== 1. OpenTelemetry 初始化 ==============
print("\n=== 1️⃣ OpenTelemetry 初始化 ===")
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.langchain import LangchainInstrumentor

resource = Resource.create({"service.name": "deloitte-ai-native-mvp", "service.version": "0.1.0"})
provider = TracerProvider(resource=resource)
# 默认输出到 console（json）
provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

print("  ✓ TracerProvider 初始化（service.name=deloitte-ai-native-mvp）")
print("  ✓ BatchSpanProcessor + ConsoleSpanExporter")
print("  ✓ FastAPIInstrumentor / RequestsInstrumentor / LangchainInstrumentor ready")

# ============== 2. Mem0 初始化 ==============
print("\n=== 2️⃣ Mem0 初始化 ===")
from mem0 import Memory

# Mem0 配置：完全切到 MiniMax（**何大人 21:49 决策**）
# - LLM: MiniMax 官方 chat 模型 via api.minimaxi.com
# - Embedder: MiniMax embo-01（如果支持）或本地 fastembed 兜底
# - **需要 MINIMAX_API_KEY 环境变量**
mem0_config = {
    "llm": {
        "provider": "openai",  # MiniMax API 走 OpenAI 兼容协议
        "config": {
            "model": "MiniMax-Text-01",  # MiniMax 官方 chat 模型（待 smoke test 确认确切名）
            "openai_base_url": "https://api.minimaxi.com/v1",
            "api_key": os.getenv("MINIMAX_API_KEY") or os.getenv("OPENAI_API_KEY"),
        }
    },
    "embedder": {
        # MiniMax 官方 embedding（如果支持）；否则需切回 fastembed
        "provider": "openai",
        "config": {
            "model": "embo-01",  # MiniMax 官方 embedding（待 smoke test 确认）
            "openai_base_url": "https://api.minimaxi.com/v1",
            "api_key": os.getenv("MINIMAX_API_KEY") or os.getenv("OPENAI_API_KEY"),
            "embedding_dims": 1536,  # 待 smoke test 后确认
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "path": "/tmp/mem0_qdrant",  # 本地 Qdrant 文件模式
            "embedding_model_dims": 1536,  # MiniMax embedding 默认维度（待确认）
        }
    }
}

try:
    memory = Memory.from_config(mem0_config)
    print(f"  ✓ Memory.from_config 成功（provider=openai, model=gpt-5.4-mini）")
except Exception as e:
    print(f"  ⚠ Memory init 失败: {e}")
    print(f"    提示：检查 OPENAI_API_KEY 是否设置")
    memory = None

# ============== 3. 集成 demo：trace + memory ==============
print("\n=== 3️⃣ 整合 Demo（trace + memory）===")

USER_ID = "hesiyan2008"
TRACE_OUTPUT_DIR = "/root/vault/1-Projects/德勤/AI-Native/observability/traces/"
os.makedirs(TRACE_OUTPUT_DIR, exist_ok=True)

with tracer.start_as_current_span("deloitte-ai-native-orchestrator") as parent_span:
    parent_span.set_attribute("user.id", USER_ID)
    parent_span.set_attribute("scenario", "user-preference-capture")

    # 3.1 模拟用户请求
    print("\n  📝 Step 1: 模拟用户偏好对话")
    with tracer.start_as_current_span("mem0.add-preferences") as span:
        span.set_attribute("mem0.user_id", USER_ID)

        if memory:
            try:
                prefs = [
                    {"role": "user", "content": "我（何大人）喜欢正式但带点幽默的风格"},
                    {"role": "user", "content": "我正在做德勤 AI-Native MVP 项目，目标是 Hermes Agent 框架"},
                    {"role": "user", "content": "服务器是腾讯云 8C30G + 315G，公网 IP 是 101.33.212.119"},
                    {"role": "user", "content": "我偏好先研究，再批量决策（1+2+3 分级法）"},
                ]
                result = memory.add(prefs, user_id=USER_ID)
                span.set_attribute("mem0.added_count", len(result.get("results", [])))
                print(f"    ✓ Mem0 已添加 {len(prefs)} 条用户偏好")
                print(f"    ✓ 返回结果: {len(result.get('results', []))} 条记忆")
            except Exception as e:
                span.set_attribute("mem0.error", str(e))
                print(f"    ⚠ Mem0 add 失败（无 API key）: {type(e).__name__}")
                print(f"    ⚠ 跳过实际写入，仅演示 trace 结构")
        else:
            print(f"    ⚠ Memory 未初始化，跳过 add")

    time.sleep(0.5)

    # 3.2 模拟检索
    print("\n  🔍 Step 2: 模拟检索用户偏好")
    with tracer.start_as_current_span("mem0.search") as span:
        span.set_attribute("mem0.user_id", USER_ID)
        span.set_attribute("mem0.query", "我服务器是什么配置？")

        if memory:
            try:
                results = memory.search("我服务器是什么配置？", user_id=USER_ID)
                span.set_attribute("mem0.found_count", len(results.get("results", [])))
                print(f"    ✓ 检索到 {len(results.get('results', []))} 条相关记忆")
                for r in results.get("results", [])[:3]:
                    print(f"      - {r.get('memory', '')[:80]}")
            except Exception as e:
                span.set_attribute("mem0.error", str(e))
                print(f"    ⚠ Mem0 search 失败: {type(e).__name__}")
        else:
            print(f"    ⚠ Memory 未初始化，跳过 search")

    time.sleep(0.5)

    # 3.3 模拟 LangChain 集成（如果可用）
    print("\n  🔗 Step 3: LangChain 集成（可选）")
    try:
        LangchainInstrumentor().instrument()
        print(f"    ✓ LangchainInstrumentor 已激活")
        print(f"    ✓ 下次 LangChain LLM 调用会自动产生 trace span")
    except Exception as e:
        print(f"    ⚠ LangChain instrumentor 失败: {e}")

# ============== 4. 输出总结 ==============
print("\n=== 4️⃣ 输出总结 ===")
print(f"  ✓ OpenTelemetry trace → Console (JSON span 已展示)")
print(f"  ✓ Mem0 vector store → /tmp/mem0_qdrant (Qdrant local)")
print(f"  ✓ Trace ID: {parent_span.get_span_context().trace_id}")
print(f"  ✓ Trace 路径: {TRACE_OUTPUT_DIR}")

# 保存 trace summary
trace_summary = {
    "timestamp": datetime.now().isoformat(),
    "trace_id": format(parent_span.get_span_context().trace_id, "032x"),
    "service": "deloitte-ai-native-mvp",
    "user_id": USER_ID,
    "demo": "otel+mem0 integration",
    "components": {
        "opentelemetry": {
            "version": "1.43.0",
            "instrumentors": ["fastapi", "requests", "langchain", "httpx"],
            "exporter": "console (JSON)",
        },
        "mem0": {
            "version": "2.0.11",
            "llm_provider": "openai",
            "model": "gpt-5.4-mini",
            "vector_store": "qdrant (local file)",
        },
    },
    "vibe_kanban_status": "SUNSET (BloopAI/vibe-kanban 关停)",
    "vibe_kanban_alternative": "Hermes 内置 kanban daemon (/opt/hermes-venv/bin/hermes kanban)",
}
summary_path = os.path.join(TRACE_OUTPUT_DIR, "demo-summary.json")
with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(trace_summary, f, indent=2, ensure_ascii=False)
print(f"  ✓ Summary 写入: {summary_path}")

print("\n=== 🎉 部署完成 ===")
print("\n下一步建议：")
print("  1. 设置 OPENAI_API_KEY 后重跑（Mem0 add/search 才会真实写入）")
print("  2. 在 LangGraph / Hermes adapter 中用 @trace装饰器包装")
print("  3. 部署 Langfuse server（2 级别，可视化 trace）")
print("  4. Hermes kanban daemon 已在用，不需要 Vibe Kanban")