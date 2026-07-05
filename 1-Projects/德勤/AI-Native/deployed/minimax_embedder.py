#!/usr/bin/env python3
"""
Mem0 自定义 embedder — MiniMax embo-01（**何大人 21:49 决策**）

关键差异（**vs Mem0 默认 OpenAI embedder**）：
- Mem0 默认：input=[text] + encoding_format=float + dimensions=...
- MiniMax：   texts=[text] + type=db + （无 dimensions 参数）

继承 mem0.embeddings.base.EmbeddingBase，完全替代 OpenAI embedder。
"""
import os
import requests
from typing import Literal, Optional

from mem0.configs.embeddings.base import BaseEmbedderConfig
from mem0.embeddings.base import EmbeddingBase


class MiniMaxEmbedding(EmbeddingBase):
    """Mem0 embedder adapter for MiniMax embo-01."""

    def __init__(self, config: Optional[BaseEmbedderConfig] = None):
        super().__init__(config)

        self.config.model = self.config.model or "embo-01"
        self.config.embedding_dims = self.config.embedding_dims or 1536

        api_key = self.config.api_key or os.getenv("MINIMAX_API_KEY") or os.getenv("OPENAI_API_KEY")
        base_url = self.config.openai_base_url or "https://api.minimaxi.com/v1"

        if not api_key:
            raise ValueError(
                "MiniMax API key required. Set MINIMAX_API_KEY env var "
                "or pass api_key in embedder config."
            )

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.endpoint = f"{self.base_url}/embeddings"
        self.model = self.config.model

    def embed(self, text, memory_action: Optional[Literal["add", "search", "update"]] = None):
        """Embed single text via MiniMax API.

        MiniMax requires:
          - texts=[...] (not input=)
          - type="db" or "query" (different indexes for add vs search)
        """
        text = text.replace("\n", " ")
        # type: "db" for adding to vector store, "query" for searching
        embo_type = "db" if memory_action == "add" else "query"

        payload = {
            "model": self.model,
            "texts": [text],
            "type": embo_type,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        resp = requests.post(self.endpoint, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        if "vectors" not in data or not data["vectors"]:
            raise ValueError(f"MiniMax embedding returned no vectors: {data}")

        return data["vectors"][0]

    def embed_batch(self, texts, memory_action: str = "add"):
        """Embed multiple texts (default Mem0 interface)."""
        texts = [t.replace("\n", " ") for t in texts]
        embo_type = "db" if memory_action == "add" else "query"

        # MiniMax allows batch in single request
        payload = {
            "model": self.model,
            "texts": texts,
            "type": embo_type,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        resp = requests.post(self.endpoint, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        if "vectors" not in data or len(data["vectors"]) != len(texts):
            raise ValueError(
                f"MiniMax embed_batch returned {len(data.get('vectors', []))} vectors "
                f"for {len(texts)} texts: {data}"
            )

        return data["vectors"]


if __name__ == "__main__":
    # Smoke test
    config = BaseEmbedderConfig(model="embo-01", embedding_dims=1536)
    embedder = MiniMaxEmbedding(config)

    v1 = embedder.embed("何大人偏好：先研究再批量决策", memory_action="add")
    print(f"  ✓ add mode: dim={len(v1)}, sample={v1[:3]}")

    v2 = embedder.embed("何大人的工作风格", memory_action="search")
    print(f"  ✓ search mode: dim={len(v2)}, sample={v2[:3]}")

    # Compute cosine similarity (should be high)
    import numpy as np
    sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    print(f"  ✓ similarity (related): {sim:.4f}")

    v3 = embedder.embed("量子物理黑洞理论", memory_action="search")
    sim2 = np.dot(v1, v3) / (np.linalg.norm(v1) * np.linalg.norm(v3))
    print(f"  ✓ similarity (unrelated): {sim2:.4f}")
    print(f"  → embedding 区分度 OK" if abs(sim - sim2) > 0.01 else "  → ⚠ 区分度差")