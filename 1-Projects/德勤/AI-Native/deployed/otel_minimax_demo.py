#!/usr/bin/env python3
"""
德勤 AI-Native MVP — 轻量 Mem0 等价实现（**MiniMax 全栈**）
=============================================================

何大人 2026-07-05 21:49 决策：替换 Mem0 用的 OpenAI 官方 key → 改用 MiniMax。
何大人 2026-07-05 23:14 提供 MiniMax API key。

**问题**：Mem0 0.x 的 add 流程会触发 spaCy + BM25 模型下载，hang 在网络。
**解决方案**：不依赖 Mem0，自己实现核心 add/search 逻辑（更轻、更可控）。

## 用法

```bash
export MINIMAX_API_KEY=*** <key>
python3 /root/vault/1-Projects/德勤/AI-Native/deployed/otel_minimax_demo.py
```

## 输出

- ✅ OpenTelemetry trace JSON
- ✅ MiniMax LLM 提取事实（extract facts from text）
- ✅ MiniMax embedding 入向量库（type=db for add, type=query for search）
- ✅ Qdrant 本地存储 + 向量检索
- ✅ Trace summary JSON
"""
import os
import sys
import json
import time
import uuid
import hashlib
import requests
import numpy as np
from datetime import datetime, timezone

# ============== 1. OpenTelemetry 初始化 ==============
print("\n=== 1️⃣ OpenTelemetry 初始化 ===")
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource

resource = Resource.create({
    "service.name": "deloitte-ai-native-mvp",
    "service.version": "0.3.0-minimal",
    "deployment.environment": "dev",
    "llm.provider": "MiniMax",
})
provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
print("  ✓ TracerProvider 初始化")

# ============== 2. MiniMax API 封装 ==============
print("\n=== 2️⃣ MiniMax API 客户端 ===")

MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
if not MINIMAX_API_KEY:
    print("  ⚠ MINIMAX_API_KEY 未设置")
    sys.exit(1)

BASE_URL = "https://api.minimaxi.com/v1"
CHAT_MODEL = "MiniMax-M2.7"  # 支持 json_object
EMBED_MODEL = "embo-01"
EMBED_DIM = 1536


def minimax_chat(messages, model=CHAT_MODEL, json_mode=True, timeout=60):
    """调 MiniMax chat API（OpenAI 兼容）。"""
    payload = {"model": model, "messages": messages}
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    r = requests.post(
        f"{BASE_URL}/text/chatcompletion_v2",
        headers={"Authorization": f"Bearer {MINIMAX_API_KEY}", "Content-Type": "application/json"},
        json=payload,
        timeout=timeout,
    )
    r.raise_for_status()
    data = r.json()
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    return content


def minimax_embed(texts, type_="db"):
    """调 MiniMax embedding API（自定义参数：texts + type=db|query）。

    Args:
        texts: 单个 str 或 list[str]
        type_: 'db' 写入向量库 / 'query' 搜索
    """
    if isinstance(texts, str):
        texts = [texts]
    r = requests.post(
        f"{BASE_URL}/embeddings",
        headers={"Authorization": f"Bearer {MINIMAX_API_KEY}", "Content-Type": "application/json"},
        json={"model": EMBED_MODEL, "texts": texts, "type": type_},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["vectors"]


# 验证
print("  ✓ MiniMax 客户端就绪")
test_vec = minimax_embed("test")
print(f"  ✓ Embedding API 验证 OK（{len(test_vec[0])} dim）")

# ============== 3. Qdrant 封装（不用 Mem0 的 BM25/spaCy 依赖） ==============
print("\n=== 3️⃣ Qdrant 向量存储（独立封装）===")
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

QDRANT_PATH = "/tmp/deloitte_mem0_qdrant"
COLLECTION = "deloitte_memories"

client = QdrantClient(path=QDRANT_PATH)
# 重建 collection
try:
    client.delete_collection(COLLECTION)
    print(f"  ✓ 删除旧 collection: {COLLECTION}")
except Exception:
    pass
client.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
)
print(f"  ✓ 创建 collection: {COLLECTION}（{EMBED_DIM} dim, COSINE）")

# ============== 4. Memory 核心逻辑 ==============
print("\n=== 4️⃣ Memory 核心逻辑（add/search）===")


def extract_facts(text: str) -> list:
    """用 MiniMax LLM 从原始文本提取事实。"""
    prompt = f"""从下面的用户输入中提取所有值得记住的事实。

用户输入："{text}"

返回 JSON：
{{"facts": ["fact 1", "fact 2", ...]}}

只提取可长期记忆的具体事实（偏好/属性/事实/意图），不要解释。"""

    response = minimax_chat(
        messages=[
            {"role": "system", "content": "你是事实提取助手。返回严格 JSON。"},
            {"role": "user", "content": prompt},
        ],
        json_mode=True,
    )
    # Strip markdown code block if present
    response = response.strip()
    if response.startswith("```"):
        response = response.split("\n", 1)[1].rsplit("```", 1)[0]
    try:
        data = json.loads(response)
        return data.get("facts", [])
    except json.JSONDecodeError:
        return [response]


def memory_add(text: str, user_id: str):
    """添加一条记忆：提取事实 → embedding → 写入 Qdrant。"""
    # Step 1: extract facts
    facts = extract_facts(text)
    if not facts:
        return []

    # Step 2: embedding (db mode for storage)
    vectors = minimax_embed(facts, type_="db")

    # Step 3: insert into Qdrant
    points = []
    for fact, vec in zip(facts, vectors):
        point_id = str(uuid.uuid4())
        payload = {
            "user_id": user_id,
            "text": fact,
            "hash": hashlib.md5(fact.encode()).hexdigest(),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        points.append(PointStruct(id=point_id, vector=vec, payload=payload))

    client.upsert(collection_name=COLLECTION, points=points)
    return [{"id": p.id, "memory": p.payload["text"]} for p in points]


def memory_search(query: str, user_id: str, top_k: int = 5):
    """搜索相关记忆。"""
    # Step 1: embed query (query mode for retrieval)
    query_vecs = minimax_embed(query, type_="query")
    query_vec = query_vecs[0]

    # Step 2: search Qdrant
    # qdrant-client 1.18+ 用 query_points 替代 search
    # Filter 要用 qdrant_client.models.Filter
    from qdrant_client.models import Filter, FieldCondition, MatchValue
    response = client.query_points(
        collection_name=COLLECTION,
        query=query_vec,
        limit=top_k,
        query_filter=Filter(must=[FieldCondition(key="user_id", match=MatchValue(value=user_id))]),
    )

    return [{"memory": r.payload["text"], "score": r.score} for r in response.points]


print("  ✓ memory_add / memory_search 已就绪")

# ============== 5. 整合 Demo：OTel + Memory ==============
print("\n=== 5️⃣ 整合 Demo（OTel trace + Memory）===")

USER_ID = "hesiyan2008"
TRACE_OUTPUT_DIR = "/root/vault/1-Projects/德勤/AI-Native/observability/traces/"
os.makedirs(TRACE_OUTPUT_DIR, exist_ok=True)

with tracer.start_as_current_span("deloitte-ai-native-orchestrator") as parent:
    parent.set_attribute("user.id", USER_ID)
    parent.set_attribute("llm.provider", "MiniMax")
    parent.set_attribute("embedding.model", EMBED_MODEL)
    parent.set_attribute("vector.store", "qdrant-local")

    # 5.1 add 偏好
    print("\n  📝 Step 1: 写入用户偏好")
    prefs = [
        "我（何大人）喜欢正式但带点幽默的风格",
        "我正在做德勤 AI-Native MVP 项目，目标是 Hermes Agent 框架",
        "服务器是腾讯云 8C30G + 315G，公网 IP 是 101.33.212.119",
        "我偏好先研究，再批量决策（1+2+3 分级法）",
        "德勤项目用 MiniMax API 替代 Codex/OpenAI，2026-07-05 决策",
    ]
    with tracer.start_as_current_span("memory.add-batch") as span:
        span.set_attribute("user.id", USER_ID)
        span.set_attribute("count", len(prefs))
        all_added = []
        for pref in prefs:
            with tracer.start_as_current_span("memory.add-one") as sub:
                sub.set_attribute("text", pref[:50])
                t0 = time.time()
                added = memory_add(pref, user_id=USER_ID)
                sub.set_attribute("facts.extracted", len(added))
                sub.set_attribute("duration.ms", int((time.time() - t0) * 1000))
                all_added.extend(added)
                print(f"    ✓ {pref[:30]}... → {len(added)} facts")
        span.set_attribute("total.added", len(all_added))
        print(f"  → 总计添加 {len(all_added)} 条记忆")

    time.sleep(0.5)

    # 5.2 search
    print("\n  🔍 Step 2: 多查询对比")
    queries = [
        ("我服务器是什么配置？", True),
        ("德勤项目用什么 API？", True),
        ("我的工作风格？", True),
        ("宇宙的终极真理是什么？", False),  # 应该不相关
    ]
    for q, expect_match in queries:
        with tracer.start_as_current_span("memory.search") as span:
            span.set_attribute("query", q)
            span.set_attribute("expect_match", expect_match)
            t0 = time.time()
            results = memory_search(q, user_id=USER_ID)
            span.set_attribute("results.count", len(results))
            span.set_attribute("duration.ms", int((time.time() - t0) * 1000))

            print(f"    Q: {q}")
            print(f"    → {len(results)} 条相关记忆")
            for r in results[:3]:
                match_indicator = "✓" if expect_match else "✗"
                print(f"      {match_indicator} [{r['score']:.3f}] {r['memory'][:60]}")
            print()

# ============== 6. Summary ==============
print("\n=== 6️⃣ 输出总结 ===")
trace_id = format(parent.get_span_context().trace_id, "032x")
print(f"  ✓ Trace ID: {trace_id}")
print(f"  ✓ LLM: MiniMax-M2.7（json_object mode）")
print(f"  ✓ Embedder: MiniMax embo-01（1536 dim）")
print(f"  ✓ Vector store: Qdrant local @ {QDRANT_PATH}")

summary = {
    "timestamp": datetime.now().isoformat(),
    "trace_id": trace_id,
    "service": "deloitte-ai-native-mvp",
    "version": "0.3.0-minimal",
    "user_id": USER_ID,
    "approach": "minimal Mem0 equivalent (no spaCy/BM25 deps)",
    "components": {
        "llm": {"provider": "MiniMax", "model": CHAT_MODEL},
        "embedder": {"provider": "MiniMax", "model": EMBED_MODEL, "dim": EMBED_DIM},
        "vector_store": "qdrant-local (file mode)",
        "memory_logic": "lightweight wrapper (no Mem0 dependency)",
    },
    "key_decisions": {
        "21:49": "何大人决策 B：替换 Mem0 OpenAI key → MiniMax",
        "23:14": "何大人提供 MiniMax API key",
        "23:50": "弃用 Mem0 0.x（spaCy/BM25 hang），改用轻量等价实现",
    },
    "advantages_vs_mem0": [
        "无 spaCy 依赖（不用 pip install mem0ai[nlp]）",
        "无 BM25 依赖（不用下载 Qdrant sparse 模型）",
        "完全可控（代码量 < 200 行）",
        "API 透明（直接调 MiniMax REST）",
    ],
    "disadvantages_vs_mem0": [
        "没有自动记忆去重（Mem0 内置）",
        "没有自动实体提取（Mem0 内置）",
        "没有 graph memory（Mem0 内置）",
    ],
}
summary_path = os.path.join(TRACE_OUTPUT_DIR, "demo-summary-minimal.json")
with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)
print(f"  ✓ Summary: {summary_path}")

print("\n=== 🎉 完成 ===")
print("\n下一步：")
print("  1. 用 @trace 装饰器包装 Hermes / Paperclip 调用")
print("  2. 部署 Langfuse server（2 级别，可视化 trace）")
print("  3. 评估是否回 Mem0 1.0+（如它移除了 spaCy/BM25 硬依赖）")