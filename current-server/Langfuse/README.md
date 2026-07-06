---
title: Langfuse 部署手册 + 避坑指南
date: 2026-07-06
type: deployment-handbook
status: active
service: Langfuse
port: 3000
public_url: http://101.33.212.119:3000
deploy_path: /root/projects/langfuse
---

# 🦊 Langfuse 部署手册 + 避坑指南

> **一句话**：LLM 可观测性 / Tracing 平台。OpenAI/Anthropic 兼容端点，可用于 MiniMax 链路追踪。

---

## 1. 项目信息

| 项 | 值 |
|---|---|
| 用途 | LLM Tracing / Prompt 调试 / 数据集管理 |
| 镜像 | `langfuse/langfuse:3` |
| 公网 URL | `http://101.33.212.119:3000` |
| 状态 | ✅ 200 OK（10h+ 稳定运行）|
| 部署位置 | `/root/projects/langfuse/` |

---

## 2. 硬件依赖

| 项 | 最低 | 当前服务器 |
|---|---|---|
| CPU | 4 核 | 8 核 ✅ |
| RAM | 8 GB | 30 GB ✅ |
| Disk | 50 GB | 315 GB ✅ |
| 关键镜像 | postgres + redis + clickhouse + minio | 已部署 |

---

## 3. 一键部署（从 0 到 1）

```bash
# 1. 拉 compose
mkdir -p /root/projects/langfuse && cd /root/projects/langfuse
# 用官方 docker-compose.yml
curl -L https://raw.githubusercontent.com/langfuse/langfuse/main/docker-compose.yml -o docker-compose.yml
# 同时拉 .env.example
curl -L https://raw.githubusercontent.com/langfuse/langfuse/main/.env.example -o .env

# 2. 改 .env
sed -i 's|^CLICKHOUSE_CLUSTER_ENABLED=.*|CLICKHOUSE_CLUSTER_ENABLED=false|' .env  # ← 关键！
sed -i 's|^NEXTAUTH_SECRET=.*|NEXTAUTH_SECRET=$(openssl rand -hex 32)|' .env
sed -i 's|^ENCRYPTION_KEY=.*|ENCRYPTION_KEY=$(openssl rand -hex 32)|' .env
sed -i 's|^LANGFUSE_S3_EVENT_UPLOAD_BUCKET=.*|LANGFUSE_S3_EVENT_UPLOAD_BUCKET=langfuse|' .env

# 3. 改 docker-compose.yaml 关键配置
# - ports: "0.0.0.0:3000:3000"  ← 必须 0.0.0.0
# - langfuse-web / langfuse-worker 都加 extra_hosts: host.docker.internal:host-gateway

# 4. 启
docker compose up -d
```

---

## 4. 配置文件（.env 关键项）

```bash
DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/postgres
REDIS_URL=redis://host.docker.internal:6379/0
CLICKHOUSE_URL=http://langfuse-clickhouse-1:8123
CLICKHOUSE_CLUSTER_ENABLED=false          # ← 关键（单节点必须关）
LANGFUSE_S3_EVENT_UPLOAD_BUCKET=langfuse
LANGFUSE_S3_EVENT_UPLOAD_REGION=us-east-1
NEXTAUTH_SECRET=<openssl rand -hex 32>
ENCRYPTION_KEY=<openssl rand -hex 32>
```

---

## 5. 启动命令

```bash
cd /root/projects/langfuse
docker compose up -d
# 检查状态
docker compose ps
# 看 logs
docker logs langfuse-web-1 --tail 30
```

---

## 6. 三维度验证

```bash
# 本地
curl -sI http://localhost:3000
# 公网
curl -sI http://101.33.212.119:3000
# 云端
# web_fetch http://101.33.212.119:3000
```

期望：HTTP 200 + HTML 包含 "Loading" (Langfuse Next.js SPA)

---

## 7. ⚠️ 避坑指南（按时间倒序）

### 坑 1: ClickHouse ReplicatedMergeTree 启动失败
- **现象**: langfuse-clickhouse-1 反复 restart，log 报 `ReplicatedMergeTree requires ZooKeeper`
- **根因**: Langfuse 默认 `CLICKHOUSE_CLUSTER_ENABLED=true`（分布式模式），单节点 ClickHouse 启动失败
- **修法**: `.env` 设 `CLICKHOUSE_CLUSTER_ENABLED=false`（走 unclustered 迁移，MergeTree 不需要 ZK）
- **永久规则**: ✅ **单节点 ClickHouse 必须 `CLICKHOUSE_CLUSTER_ENABLED=false`**

### 坑 2: ports 默认 127.0.0.1
- **现象**: 容器起来了，但 `curl http://101.33.212.119:3000` 失败
- **根因**: `langfuse-web` 端口默认 `127.0.0.1:3000:3000`（只监听 localhost）
- **修法**: `docker-compose.yaml` 改 `0.0.0.0:3000:3000`
- **永久规则**: ✅ **所有要公网访问的 Docker 容器，ports 必须 `0.0.0.0:端口:端口`**

### 坑 3: host.docker.internal 不解析
- **现象**: langfuse-web 启动失败，log 报 `Error connecting to host.docker.internal:5432`
- **根因**: Linux Docker 默认不解析 `host.docker.internal`
- **修法**: docker-compose.yaml 给 langfuse-web / langfuse-worker 加 `extra_hosts: ["host.docker.internal:host-gateway"]`
- **永久规则**: ✅ **任何用宿主机的容器都加 `extra_hosts: host-gateway`**

### 坑 4: ENCRYPTION_KEY 是默认值
- **现象**: 容器启动 warn log "ENCRYPTION_KEY is not set or using default value"
- **根因**: `.env` 里 ENCRYPTION_KEY 是占位符
- **修法**: `ENCRYPTION_KEY=$(openssl rand -hex 32)` 真随机
- **永久规则**: ✅ **任何 secret/encryption key 都用 `openssl rand -hex 32` 真随机**

### 坑 5: 宿主机 Redis protected-mode
- **现象**: langfuse-worker log 报 `Redis DENIED`
- **根因**: 宿主机 Redis `protected-mode yes` + `bind 0.0.0.0` 拒绝非 loopback
- **修法**: `/etc/redis/redis.conf` 加 `protected-mode no`（dev 场景）
- **永久规则**: ⚠️ dev 阶段 protected-mode 关闭；生产必须密码+ACL

### 坑 6: LANGFUSE_S3_EVENT_UPLOAD_BUCKET 没设
- **现象**: trace 数据上传到 MinIO 失败
- **根因**: bucket name 不匹配
- **修法**: `.env` 设 `LANGFUSE_S3_EVENT_UPLOAD_BUCKET=langfuse`
- **永久规则**: ✅ 启动前先看 .env.example vs .env diff

---

## 8. 当前状态（2026-07-06 20:08）

| 容器 | 状态 | restart |
|---|---|---|
| langfuse-web-1 | Up 10h | 0 |
| langfuse-worker-1 | Up 10h | 0 |
| langfuse-clickhouse-1 | Up 19h healthy | 0 |
| langfuse-minio-1 | Up 19h healthy | 0 |

**共享服务**（宿主机）：postgres:5432, redis:6379

---

## 9. 关联文档

- `/root/vault/current-server/2026-07-06_md_三个URL部署修复完成报告.md`
- MEMORY.md 顶部 lessons（"host.docker.internal 解析" 章节）
