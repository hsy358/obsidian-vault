---
title: Semantica 冲突排查 + 部署可行性评估
date: 2026-08-12 23:30 GMT+8
trigger: 何大人转发公众号「自称开源版 Palantir：一张图让每个 AI 决策都查得到来龙去脉」
source_url: https://mp.weixin.qq.com/s/Z9hkuWNY01mg5SHBnMRfZw
target: 决定 Semantica 是否部署到当前服务器（101.33.212.119）
status: 冲突排查完成 / 等何大人决策
related: ../2026-08-12 - 公众号-自称开源版Palantir-Semantica.md
---

# Semantica 部署冲突排查 + 可行性评估

> 触发：何大人 2026-08-12 23:30 转发公众号链接 → 问"能部署吗？"
> 原则：先冲突排查、再评估可行性、最后等何大人决策（不直接动手）

## 1. Semantica 是什么（要点回顾）

- **GitHub**：<https://github.com/semantica-agi/semantica>（4.5k Star、MIT、v0.6.5）
- **定位**：开源版 Palantir —— 给 AI 决策加"图谱 + 哈希链账本 + W3C PROV-O + Datalog 推理"
- **三大模块**：Context Graph / Decision Intelligence / Provenance
- **官方 Docker 镜像**：`explorer` (FastAPI + 前端, 端口 8000) + `falkordb` (端口 6379)
- **依赖**：Python ≥3.8，torch + transformers + spacy + sentence-transformers + faiss + rdflib + opencv + librosa（很重）

## 2. 冲突排查报告

| 项 | 现占用 | Semantica 拟用 | 冲突？ |
|---|---|---|---|
| HTTP API | langfuse(3000)/dify(8080)/ragflow(9385)/milvus 等 | **8000**（explorer）| ✅ 空闲 |
| FalkorDB | redis(6381)/guyu-redis(6380)/dify-redis/coze-redis/ragflow-redis 全在 6379 | **6379**（falkordb）| ❌ **直接冲突** |
| 前端 dev | （无） | 5173（仅 dev compose） | ✅ 空闲 |
| Postgres | 5433(postgres)/5432(qm-hesiyan/ontology/dify-db)/5435(agentos)/5436(octafuse) | 默认零依赖 SQLite | ✅ 不冲突 |
| Neo4j | graph (Neo4j 5.26, 7687/7474) | 可选复用 | ✅ 已存在 |
| Qdrant | guyu-qdrant (6333) | 可选复用 | ✅ 已存在 |
| Redis | 5 个实例占 6379/6380/6381 | （见 FalkorDB） | ⚠️ 见上 |
| 容器名 | dify-/langfuse-/ragflow-/milvus-/dify-... | `semantica-` 前缀 | ✅ 不冲突 |
| 路径 | /root/projects/{13 个已用名} | `/root/projects/semantica/` | ✅ 不冲突 |
| systemd | agentspace / agnos-ui / hermes-gateway / openclaw-gateway / paperclip | （不需新加，docker compose 自管） | ✅ 不冲突 |
| 资源 | 30Gi 内存 / 12Gi 可用 / 114G 磁盘空闲 / 8 核 | explorer +5GB / falkordb +0.5GB / 磁盘 +3GB | ✅ 充裕 |

### ⚠️ 唯一真冲突：FalkorDB 端口 6379

FalkorDB 用 Redis 协议，**默认绑 6379**。当前服务器 6379 已占用，但占的是普通 Redis（语义不同 —— Redis 是缓存，falkordb 是图数据库）。

**三个解法**（按推荐度排序）：

1. ✅ **改 falkordb 端口映射**（推荐）：`16379:6379` 或 `6382:6379`，零业务影响
2. ⚠️ **复用 guyu-redis-2（6380）作为 falkordb**：能跑但语义污染，不推荐
3. ❌ **直接占 6379**：会让 dify/ragflow/coze 的 Redis 连接断，不可以

## 3. 部署方案（推荐）

### 方案 A：官方 compose 微改（最小风险）

```yaml
# /root/projects/semantica/docker-compose.yml
services:
  explorer:
    build: .
    image: semantica-knowledge-explorer:latest
    environment:
      FALKORDB_HOST: falkordb           # 容器名互通
      FALKORDB_PORT: "6379"
      SEMANTICA_API_KEY: <openssl rand -hex 32>
      ALLOWED_ORIGINS: http://101.33.212.119:8000
    ports:
      - "8000:8000"                       # 唯一新端口
    depends_on: [falkordb]
    networks: [semantica]
    restart: unless-stopped

  falkordb:
    image: falkordb/falkordb:latest
    ports:
      - "6382:6379"                       # 改端口避开 6379 冲突
    volumes:
      - semantica_falkordb:/data
    networks: [semantica]
    restart: unless-stopped

networks:
  semantica:
    driver: bridge

volumes:
  semantica_falkordb:
```

**优点**：跟官方一致、社区问题可对得上
**缺点**：explorer 镜像依赖 torch 等大型包，build 慢（首次 ~10-20 分钟）

### 方案 B：直接 pip 装 + FalkorDB 容器（最轻）

```bash
# 1. pip 装（不进 venv 隔离，避免污染系统）
python3 -m venv /root/projects/semantica/.venv
source /root/projects/semantica/.venv/bin/activate
pip install "semantica[explorer]"      # 只装 explorer 必需依赖

# 2. 只启 falkordb 容器（轻量）
docker run -d --name semantica-falkordb \
  -p 6382:6379 \
  -v semantica_falkordb:/data \
  falkordb/falkordb:latest

# 3. 启 explorer
cd /root/projects/semantica
export FALKORDB_HOST=localhost FALKORDB_PORT=6382
python -m uvicorn semantica.explorer.app:app --host 0.0.0.0 --port 8000
```

**优点**：explorer 不需要 docker build，依赖隔离干净
**缺点**：需要 systemd 单元托管 uvicorn 进程（参考现有 agentspace.service）

### 方案 C：复用现有 Neo4j（最省钱，但要走 non-default backend）

```bash
pip install "semantica[explorer,graph-neo4j]"
# 配置文件改成 NEO4J backend（需要看 semantica 配置文档确认）
```

**优点**：复用 `graph` 容器（Neo4j 5.26 已跑），零新图库
**缺点**：要研究 Neo4j backend 配置（pyproject 里只是列了依赖，不一定 explorer 直接支持），**需要先验证** —— 不作为默认推荐

## 4. 必须告诉何大人的几个坑

### ⚠️ 坑 1：Rete 引擎是骨架（作者原文 + 代码核实）

```python
# semantica/reasoning/rete_engine.py:79-104
def _matches(self, fact): return True        # 占位
def _can_join(self, left, right): return True # 占位
```

**结论**：生产合规推理只能用 Datalog，**别碰 Rete**。

### ⚠️ 坑 2：worker.py 真的空转

```python
# semantica/worker.py:39-46
while self.running:
    # Poll for tasks or process queue
    time.sleep(5)
```

**结论**：分布式 worker 还没实现 —— **单机部署不需要启 worker**，但别被它的存在误导。

### ⚠️ 坑 3：server 的 /build 接口是占位（作者说，agent 没找到 server.py 在 github 仓库里，可能被合并到 explorer）

**结论**：build 任务要走 explorer 的同步接口（要看 explorer 文档），别指望异步 worker。

### ⚠️ 坑 4："No LLM required" 有条件

- ✅ 推理 / 溯源 / 冲突检测 / 去重 —— 全程不需要 LLM
- ❌ 从原始文本建图 —— 默认还是调 LLM（`ner_method="llm"`），要改成 `pattern`（正则）或 `ml`（spaCy）

**结论**：要"全程零 LLM"，必须**手动改 ner_method 默认值**。

### ⚠️ 坑 5：依赖真的很重

explorer 镜像基于 `python:3.14-slim`，要装 torch + transformers + sentence-transformers + faiss + spacy + rdflib + opencv + librosa + matplotlib + plotly：

- 镜像 build 后 **~3-4GB**
- 运行时内存 **~4-5GB**
- 首次启动要下模型（spacy `en_core_web_sm` ~50MB，sentence-transformers 默认模型 ~80MB）

**结论**：12GB 可用内存里吃掉 5GB，还剩 7GB 给其他服务 —— **够，但不是很宽松**。

## 5. 跟现有栈的关系

| 现有服务 | Semantica 重叠度 | 备注 |
|---|---|---|
| **Langfuse v3**（3000） | ⚠️ 部分重叠 | Langfuse 是 LLM trace/observability；Semantica 是 KG+决策溯源。**互补**而非替代 |
| **Dify**（8080） | ✅ 不重叠 | Dify 是 LLM 应用平台 |
| **RAGFlow**（9385） | ⚠️ 轻度重叠 | 都是 RAG+知识库，但 Semantica 多了 Decision/Provenance 层 |
| **Neo4j**（graph 容器） | ✅ 可复用 | Semantica 支持 Neo4j 后端（需装额外依赖） |
| **Qdrant**（guyu） | ✅ 可复用 | Semantica 支持 8 个向量库后端 |

**建议定位**：把 Semantica 当成 **"决策溯源层"**，架在 Langfuse（trace）+ Dify/RAGFlow（应用）之上，给 AI 决策补"可审计"。

## 6. 决策点（何大人拍板）

我建议的部署方案，但**有几个点需要何大人决策**：

| 决策项 | 选项 | 我的建议 |
|---|---|---|
| 是否部署？ | ① 部署 ② 不部署 ③ 先做 POC 评估 | **③ 先 POC**（理由：依赖重 + 部分模块占位，全量上风险大） |
| 端口方案？ | ① 8000+6382（独立） ② 走 80 反代 | ① 独立端口 |
| 图库后端？ | ① falkordb（新容器） ② Neo4j（复用） ③ Qdrant 模拟 | ① falkordb（官方默认，少踩坑） |
| 安装方式？ | ① Docker Compose（方案 A） ② pip+systemd（方案 B） | ②（更轻、更可控） |
| 路径？ | /root/projects/semantica | ✅ 已确认不冲突 |
| 是否启用 LLM？ | ① 全程零 LLM（改 ner_method） ② 启用 LLM（用本地 Ollama 或远程） | 待定（看何大人用途） |

## 7. 我的建议（如果何大人让我直接干）

**推荐路径**：方案 B（pip+systemd）+ 方案 A 的容器编排

1. 建 `/root/projects/semantica/`
2. 启 falkordb 容器（端口 6382）
3. venv 装 `semantica[explorer,graph-neo4j]`（预留 Neo4j 后端）
4. 写 systemd unit（`semantica-explorer.service`）
5. 浏览器开 `http://101.33.212.119:8000` 看 Knowledge Explorer
6. 跑 `semantica doctor` 验证
7. 写部署报告到 `current-server/Semantica/README.md`

**预计时间**：30-45 分钟（含依赖下载）

**风险点**：
- pip 装 spacy 后还要 `python -m spacy download en_core_web_sm`（约 50MB）
- 首次 uvicorn 启动要 10-20 秒（模型 lazy load）
- `MPLBACKEND=Agg` 必须设（否则 matplotlib 报错）

## 8. 关联文档

- [公众号原文归档](./2026-08-12%20-%20公众号-自称开源版Palantir-Semantica.md)
- [current-server/from-agent/README.md](../README.md)（归档规则）
- [current-server/已有部署 README](../../)（参考部署报告格式）

---

> **结论一句话**：**能部署**，但依赖重 + 部分模块占位 → 建议**先做 POC 评估**，跑通了再考虑全量上。等何大人决策。