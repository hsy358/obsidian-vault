---
title: RAGFlow 部署手册 + 避坑指南
date: 2026-07-06
type: deployment-handbook
status: active
service: RAGFlow
port: 9385
public_url: http://101.33.212.119:9385
deploy_path: /root/projects/ragflow
---

# 🟦 RAGFlow 部署手册 + 避坑指南

> **一句话**：开源 RAG 引擎。基于深度文档理解，提供 GraphRAG / Agentic RAG / OCR 全套能力。比 LangChain + 自建召回强很多。

---

## 1. 项目信息

| 项 | 值 |
|---|---|
| 用途 | RAG 知识库 / GraphRAG / OCR / Agent 编排 |
| 镜像 | `infiniflow/ragflow:v0.18.0` + ES 8.11 + MySQL 8 + Redis + MinIO |
| 公网 URL | `http://101.33.212.119:9385` |
| 状态 | ✅ 200 OK（10h+ 稳定运行）|
| 部署位置 | `/root/projects/ragflow/` |

---

## 2. 硬件依赖

| 项 | 最低 | 当前服务器 |
|---|---|---|
| CPU | 4 核 | 8 核 ✅ |
| RAM | 16 GB | 30 GB ✅ |
| Disk | 100 GB | 315 GB ✅ |
| 关键镜像 | elasticsearch 8.11 | 已部署 |
| ES JVM | 建议 4 GB heap | 默认 1g，可改 |

---

## 3. 一键部署（从 0 到 1）

```bash
# 1. 拉 RAGFlow 完整 compose（注意：要 docker-compose.yml + docker-compose-base.yml + .env + service_conf.yaml.template + entrypoint.sh + init.sql 全部）
mkdir -p /root/projects/ragflow && cd /root/projects/ragflow
git clone --depth 1 https://github.com/infiniflow/ragflow.git .
# 或直接 curl 拉 docker compose
curl -L https://raw.githubusercontent.com/infiniflow/ragflow/main/docker/docker-compose.yml -o docker-compose.yml
curl -L https://raw.githubusercontent.com/infiniflow/ragflow/main/docker/docker-compose-base.yml -o docker-compose-base.yml
curl -L https://raw.githubusercontent.com/infiniflow/ragflow/main/docker/.env -o .env
curl -L https://raw.githubusercontent.com/infiniflow/ragflow/main/docker/service_conf.yaml.template -o service_conf.yaml.template
curl -L https://raw.githubusercontent.com/infiniflow/ragflow/main/docker/entrypoint.sh -o entrypoint.sh
curl -L https://raw.githubusercontent.com/infiniflow/ragflow/main/docker/init.sql -o init.sql

# 2. 权限（GitHub 拉下来默认无 x）
chmod +x entrypoint.sh

# 3. 改 .env（避端口冲突）
sed -i 's|^EXPOSE_MYSQL_PORT=.*|EXPOSE_MYSQL_PORT=3307|' .env       # 3306 被 guyu-mysql 占
sed -i 's|^EXPOSE_REDIS_PORT=.*|EXPOSE_REDIS_PORT=|' .env           # 留空随机
sed -i 's|^EXPOSE_MINIO_PORT=.*|EXPOSE_MINIO_PORT=|' .env           # 留空随机
sed -i 's|^EXPOSE_ES_PORT=.*|EXPOSE_ES_PORT=|' .env                 # 留空随机
sed -i 's|^SVR_WEB_HTTP_PORT=.*|SVR_WEB_HTTP_PORT=9385|' .env       # 对外 9385

# 4. service_conf.yaml 从 template 生成
cp service_conf.yaml.template service_conf.yaml

# 5. 启
docker compose up -d
```

---

## 4. 配置文件（.env 关键项）

```bash
# === 对外端口（关键，避免冲突）===
EXPOSE_MYSQL_PORT=3307
EXPOSE_REDIS_PORT=                       # ← 留空自动随机分配
EXPOSE_MINIO_PORT=                       # ← 留空自动随机分配
EXPOSE_ES_PORT=                          # ← 留空自动随机分配
EXPOSE_FLOW_HTTP_PORT=9381
SVR_WEB_HTTP_PORT=9385                   # ← 对外访问

# === Database ===
MYSQL_PASSWORD=***
MYSQL_ROOT_PASSWORD=***

# === MinIO ===
MINIO_USER=ragflow
MINIO_PASSWORD=***

# === ES ===
ES_PASSWORD=***
```

---

## 5. 启动命令

```bash
cd /root/projects/ragflow
docker compose up -d

# 检查启动进度
docker logs ragflow-ragflow-cpu-1 --tail 30
# 期望：RAGFlow server started on 9385

# 检查 ES
curl http://localhost:9200/_cluster/health?pretty
# 期望：status: green 或 yellow
```

---

## 6. 三维度验证

```bash
# 本地
curl -sI http://localhost:9385
# 公网
curl -sI http://101.33.212.119:9385
# 后端健康
curl -s http://localhost:9385/health
# 期望：{"status":"ok"}
```

---

## 7. ⚠️ 避坑指南（按时间倒序）

### 坑 1: 端口冲突（3306 被占）
- **现象**: `dify-mysql` 已经在跑，RAGFlow 内置 MySQL 启动失败
- **根因**: RAGFlow 默认 `EXPOSE_MYSQL_PORT=3306`，跟 guyu-mysql 冲突
- **修法**: `.env` 改 `EXPOSE_MYSQL_PORT=3307`（或者用宿主机的 MySQL 但 RAGFlow 强耦合内部）
- **永久规则**: ✅ **复用宿主机已占端口必改 `EXPOSE_*_PORT=新端口`**

### 坑 2: GitHub 拉文件默认无 x 权限
- **现象**: `entrypoint.sh` 报 `Permission denied`
- **根因**: GitHub archive 拉下来的 .sh 默认无 execute 权限
- **修法**: `chmod +x entrypoint.sh`
- **永久规则**: ✅ **任何从 GitHub 拉的可执行脚本必 `chmod +x`**

### 坑 3: service_conf.yaml 缺失
- **现象**: ragflow-cpu 启动报 `service_conf.yaml not found`
- **根因**: `.env` 路径错 + 没从 template 复制
- **修法**: `cp service_conf.yaml.template service_conf.yaml`
- **永久规则**: ✅ **启动前检查所有依赖文件存在**

### 坑 4: ES 9200 端口被暴露
- **现象**: 9200 暴露公网有安全风险
- **根因**: 默认 `EXPOSE_ES_PORT=9200`
- **修法**: 留空 `EXPOSE_ES_PORT=` → docker 自动随机分配（仅内网访问）
- **永久规则**: ✅ **内部组件不需对外暴露，host port 留空**

### 坑 5: RAGFlow 完整 compose 缺失（只 pull 了一个文件）
- **现象**: 启动报 `service docker-compose-base.yml not found`
- **根因**: 只 pull 了 `docker-compose.yml`，但它 include `docker-compose-base.yml`
- **修法**: 同时 pull `docker-compose-base.yml` + `service_conf.yaml.template` + `entrypoint.sh` + `init.sql`
- **永久规则**: ✅ **完整 pull 所有依赖文件**（看 docker-compose.yml include 列表）

---

## 8. 当前状态（2026-07-06 20:08）

| 容器 | 状态 | restart |
|---|---|---|
| ragflow-ragflow-cpu-1 | Up 10h | 0 |
| ragflow-es01-1 | Up 10h healthy | 0 |
| ragflow-mysql-1 | Up 10h healthy | 0 |
| ragflow-redis-1 | Up 10h healthy | 0 |
| ragflow-minio-1 | Up 10h healthy | 0 |

**对外服务**：`http://101.33.212.119:9385`

---

## 9. 关联文档

- `/root/vault/current-server/2026-07-06_md_三个URL部署修复完成报告.md`
- 报告含完整 compose 拉取命令