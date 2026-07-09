# Yuxi（语析）部署手册

> 多租户 Harness + 企业知识库平台。LangGraph 多智能体编排 + Milvus 知识库 + Neo4j 知识图谱 + Vue 3 + FastAPI。
> 跟德勤项目强相关（多智能体编排 / Skills / MCP / SubAgents），是 Hermes-based 德勤 MVP 的开源参考实现。

## 项目信息

| 项 | 值 |
|---|---|
| 用途 | 多租户 Agent 智能体平台（LangGraph + RAG + 知识图谱） |
| 源码 | https://github.com/xerrors/Yuxi |
| 版本 | v0.7.1.beta1（2026-07-09） |
| 镜像 | yuxi-api / yuxi-web / yuxi-sandbox-provisioner（本地 build）|
| 公网 URL | http://101.33.212.119:5173/（Web）<br/>http://101.33.212.119:5050/（API）<br/>http://101.33.212.119:8002/（Sandbox） |
| 公网 IP | 101.33.212.119（腾讯云主机，已放通 5173/5050/8002/5433/6381/7474/7687/9000/9001/19530） |

## 硬件依赖

| 资源 | 最低 | 当前服务器 |
|---|---|---|
| CPU | 4 核 | ✅ |
| 内存 | 16 GB | ✅（30 GB，已用 ~22 GB） |
| 磁盘 | 30 GB | ✅（221 GB 空闲） |
| GPU | ❌ 无（mineru-vllm / paddlex 默认不启）| n/a |
| Docker | 24+ | ✅ 29.1.3 |

## 一键部署（从 0 到 1）

```bash
# 1. 下载源码（GitHub API tarball 绕过 443 屏蔽）
curl -sL https://api.github.com/repos/xerrors/Yuxi/tarball -o /tmp/yuxi.tar.gz
mkdir -p /tmp/yuxi-extract && tar -xzf /tmp/yuxi.tar.gz -C /tmp/yuxi-extract
mv /tmp/yuxi-extract/xerrors-Yuxi-* /root/projects/Yuxi

# 2. 创建 .env（从模板复制）
cd /root/projects/Yuxi
cp .env.template .env

# 3. 自动生成 JWT_SECRET_KEY 和 YUXI_INSTANCE_ID
echo "JWT_SECRET_KEY=$(openssl rand -hex 32)" >> .env
echo "YUXI_INSTANCE_ID=instance-$(openssl rand -hex 8)" >> .env

# 4. 配 MiniMax API key
echo "MINIMAX_API_KEY=sk-cp-你的key" >> .env

# 5. 改端口冲突：postgres 5433/5432, redis 6381/6379
sed -i 's|- "5432:5432"|- "5433:5432"|' docker-compose.yml
sed -i 's|- "6379:6379"|- "6381:6379"|' docker-compose.yml

# 6. 串行 build（避免 api+worker 并发命名冲突）
docker compose build api
docker compose build worker   # 会复用 api image
docker compose build web
docker compose build sandbox-provisioner

# 7. 启动所有服务
docker compose up -d

# 8. seed 默认账户
docker compose exec -T api uv run --no-sync --no-dev python scripts/seed_initial_users.py

# 9. 配置 provider 和默认模型（用 superadmin token）
TOKEN=$(curl -s -X POST http://localhost:5050/api/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=zwj&password=zwj12138" | python3 -c "import json,sys;print(json.load(sys.stdin)['access_token'])")

curl -s -X PUT "http://localhost:5050/api/system/model-providers/minimax-cn" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"is_enabled":true,"api_key":"sk-cp-你的key","enabled_models":[{"id":"MiniMax-Text-01","type":"chat","display_name":"MiniMax-Text-01"}],"capabilities":["chat"]}'

curl -s -X POST "http://localhost:5050/api/system/config" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"key":"default_model","value":"minimax-cn:MiniMax-Text-01"}'
```

## 配置文件

### `.env` 关键项

```bash
YUXI_ENV=development
JWT_SECRET_KEY=（32 字节 hex）
YUXI_INSTANCE_ID=instance-（8 字节 hex）
MINIMAX_API_KEY=sk-cp-（MiniMax 直连 key）

# 端口冲突改 yuxi 默认（不变）
POSTGRES_PASSWORD=postgres
NEO4J_PASSWORD=neo4j-password
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
```

### `docker-compose.yml` 端口变更

```yaml
# 默认 -> 改后（避免与 RAGFlow/Langfuse/AgentSpace 冲突）
postgres: "5433:5432"  # 默认 5432
redis:    "6381:6379"  # 默认 6379
```

## 启动命令

```bash
cd /root/projects/Yuxi
docker compose up -d                                    # 启动
docker compose down                                     # 停止
docker compose logs -f api                              # 查 API 日志
docker compose restart api worker                       # 重启（改 .env 后）
docker compose exec -T api uv run --no-sync python scripts/seed_initial_users.py  # 重新 seed（清数据后）
```

## 三维度验证

### 本地 curl
```bash
# API 健康
curl http://localhost:5050/api/system/health
# → {"status":"ok","message":"服务正常运行","version":"0.7.1b1"}

# Web
curl -I http://localhost:5173/
# → HTTP/1.1 200 OK

# Neo4j 浏览器
curl -I http://localhost:7474/
# → HTTP/1.1 200 OK

# 登录拿 token
curl -X POST http://localhost:5050/api/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=zwj&password=zwj12138"
```

### 公网 IP curl
```bash
curl -I http://101.33.212.119:5173/   # HTTP 200
curl http://101.33.212.119:5050/api/system/health   # {"status":"ok"...}
```

### 后端健康（容器）
```bash
docker compose ps   # 10 个容器 all healthy/Up
```

### 端到端 chat（验证 MiniMax key 真能用）
```bash
TOKEN=$(curl -s -X POST http://localhost:5050/api/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=zwj&password=zwj12138" | python3 -c "import json,sys;print(json.load(sys.stdin)['access_token'])")

curl -X POST http://localhost:5050/api/chat/call \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"你好","meta":{}}'

# 预期：1-2 秒拿到回复（如 "你好，我是一个充满好奇心..."）
```

## ⚠️ 避坑指南

### 坑 1：GitHub clone 卡死（134 秒超时）

**现象**：`git clone https://github.com/xerrors/Yuxi.git` 卡在 `Cloning into ...` 阶段，134 秒后报 `Failed to connect to github.com port 443`。

**根因**：腾讯云主机出网 443 屏蔽 github.com 直连（curl 测 TCP 443 FAIL）。

**修法**：用 GitHub API 下载 tarball（api.github.com 是通的）：
```bash
curl -sL https://api.github.com/repos/xerrors/Yuxi/tarball -o /tmp/yuxi.tar.gz
# 不要用 gh-proxy.net / ghfast.top / gh-proxy.com（要么 403 要么返回空）
```

**永久规则**：GitHub 源码下载走 `api.github.com/repos/<owner>/<repo>/tarball`，不走 `github.com` 主域。

### 坑 2：buildx 并发 build api+worker 失败

**现象**：首次 `docker compose up -d --build` 跑了 8+ 小时，buildx 日志最后报：
```
#37 ERROR: image "docker.io/library/yuxi-api:0.7.1.beta1": already exists
#36 CANCELED
failed to solve: image "yuxi-api:0.7.1.beta1": already exists
```

**根因**：docker-compose.yml 把 `api` 和 `worker` 两个 service 都指向同一 image 名 `yuxi-api:${YUXI_VERSION}`。buildx 并发 build 时两个 build 都尝试命名同一 tag，后命名者报 already exists，整个 batch CANCELED。

**修法**：**串行 build**（先 api，再 worker，worker 复用 api image）：
```bash
docker compose build api         # 第一次 build yuxi-api
docker compose build worker      # 第二次 - 因 image 已存在会 skip（0.2s 完成）
docker compose build web         # 独立 image 名
docker compose build sandbox-provisioner  # 独立 image 名
```

**永久规则**：
- ✅ 任何 docker-compose 项目多个 service 共享 image 名时，必须**串行 build**
- ✅ `docker compose build <service>` 逐个 build，不要一次性 `--build` 全跑
- ❌ 不要依赖 buildx 自动去重（不支持）

### 坑 3：端口冲突

**现象**：postgres:5432 + redis:6379 与 RAGFlow / Langfuse 已占端口冲突，docker compose 启动报 `bind: address already in use`。

**修法**：改 Yuxi 默认端口，主机端口避开冲突（容器端口保持 5432/6379 不变）：
```bash
sed -i 's|- "5432:5432"|- "5433:5432"|' docker-compose.yml
sed -i 's|- "6379:6379"|- "6381:6379"|' docker-compose.yml
```

**永久规则**：
- ✅ 新项目部署前先 `ss -tlnp | grep :<port>` 查端口占用
- ✅ 端口冲突时改新项目端口，不改已有项目
- ✅ 容器端口（如 5432）保持不变，内部用容器名连接（`postgres:5432`）

### 坑 4：默认模型 = siliconflow-cn（无 key 跑不起来）

**现象**：Yuxi 默认 `default_model = siliconflow-cn:Pro/MiniMaxAI/MiniMax-M2.5`，但 siliconflow API key 没配，前端"模型列表"空白，对话 401。

**根因**：`backend/package/yuxi/config/app.py` 硬编码 `default_model = "siliconflow-cn:Pro/MiniMaxAI/MiniMax-M2.5"`。init.sh 强制要求 SILICONFLOW_API_KEY。

**修法**（二选一）：
- **A. 用 MiniMax 直连**：enable `minimax-cn` provider + 改默认模型
  ```bash
  TOKEN=...  # superadmin token
  curl -X PUT "http://localhost:5050/api/system/model-providers/minimax-cn" \
    -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
    -d '{"is_enabled":true,"api_key":"sk-cp-...","enabled_models":[{"id":"MiniMax-Text-01","type":"chat"}],"capabilities":["chat"]}'
  
  curl -X POST "http://localhost:5050/api/system/config" \
    -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
    -d '{"key":"default_model","value":"minimax-cn:MiniMax-Text-01"}'
  ```
- **B. 注册硅基流动免费 key**：https://cloud.siliconflow.cn/i/Eo5yTHGJ 写到 `SILICONFLOW_API_KEY`

**永久规则**：
- ✅ 部署 Yuxi 后立即 enable minimax-cn + 改默认模型（何大人都用 MiniMax 直连 key）
- ✅ `/config/update`（batch）这个 endpoint 当前不生效—— 用 `/config`（single-key）

### 坑 5：JFS .env 字段重复

**现象**：append `JWT_SECRET_KEY` 和 `YUXI_INSTANCE_ID` 到 `.env` 后出现两个 `JWT_SECRET_KEY=`（一空一有值）。

**根因**：Yuxi 的 init.sh 设计是 .env 留空，交互 prompt 写入。但我手动跳过 init.sh 直接 append，导致模板里原有空字段没清掉。

**修法**：
```bash
# 删除空值行
sed -i '/^JWT_SECRET_KEY=***' .env
sed -i '/^YUXI_INSTANCE_ID=$/d' .env
```

**永久规则**：
- ✅ Yuxi .env 手动追加字段后，必须 grep 确认唯一
- ✅ 或者跑 init.sh（要 TTY，需要 `expect` 或 `script`）

### 坑 6：mineru-vllm / paddlex 需 GPU

**现象**：docker-compose.yml 默认包含 mineru 和 paddlex 两个 service，但都标注 `profiles: ["all"]`——不显式 `--profile all` 不会启。

**根因**：这两个 service 用了 vLLM / PaddleX，需要 NVIDIA GPU（compose 里 `driver: nvidia, capabilities: [gpu]`）。当前腾讯云主机无 GPU。

**修法**：保持 `docker compose up -d`（不带 `--profile all`），这两个 service 不启即可。文档上传/PDF 解析功能不可用，但聊天和基本 Agent 工作。

**永久规则**：
- ✅ 默认部署不带 `--profile all`
- ⚠️ 文档解析需 GPU 或外部 MinerU API（配 `MINERU_API_KEY`）

## 当前状态（容器列表 + restart count）

```
NAME                  IMAGE                                      STATUS          PORTS
api-dev               yuxi-api:0.7.1.beta1                       Up (healthy)    0.0.0.0:5050->5050/tcp
worker-dev            yuxi-api:0.7.1.beta1                       Up              (内部)
web-dev               yuxi-web:0.7.1.beta1                       Up              0.0.0.0:5173->5173/tcp
sandbox-provisioner   yuxi-sandbox-provisioner:0.7.1.beta1       Up (healthy)    0.0.0.0:8002->8002/tcp
postgres              postgres:16                                Up (healthy)    0.0.0.0:5433->5432/tcp
redis                 redis:7-alpine                             Up (healthy)    0.0.0.0:6381->6379/tcp
minio                 minio/minio:RELEASE.2023-03-20T20-16-18Z   Up (healthy)    0.0.0.0:9000-9001
neo4j (graph)         neo4j:5.26                                 Up (healthy)    0.0.0.0:7474,7687
milvus                milvusdb/milvus:v2.5.6                     Up (healthy)    0.0.0.0:19530,9091
milvus-etcd-dev       quay.io/coreos/etcd:v3.5.5                 Up (healthy)    (内部)
```

**RestartCount**: 全 0（首次部署，无重启）。

## 关联文档

- **部署报告**：`/root/vault/current-server/2026-07-09_md_Yuxi部署报告.md`
- **Hermes 修复**：`/root/vault/1-Projects/德勤/AI-Native/2026-07-08_Hermes_cc-vibe_400_根因与永久修复.md`
- **vault 部署规范**：`/root/vault/6-System/standards/2026-07-06 - 二进制文档处理规范.md`
- **Yuxi 官方文档**：https://xerrors.github.io/Yuxi/

## 跟德勤项目的对应关系

| Yuxi 模块 | 对应德勤需求 |
|---|---|
| LangGraph 多智能体编排 | Hermes Agent v0.14 dispatcher（已选型） |
| Skills / MCP / SubAgents | Hermes-based 德勤 MVP 核心功能 |
| 知识库 / RAG | 德勤组织知识管理 |
| 多租户 | 德勤多业务线并行 |
| 沙盒（sandbox-provisioner） | Agent 工具执行环境 |
| 可观测（默认集成 Langfuse） | Hermes trace / Langfuse trace |
| Vue 3 + Pinia 前端 | 德勤管理控制台 UI 参考 |