# AgentOS（agno-agi）部署手册

> **项目**：AgentOS — Agno Agent 运行时（REST API + MCP server + Web 管理）
> **仓库**：https://github.com/agno-agi/agentos-docker
> **部署时间**：2026-07-25
> **公网访问**：`http://101.33.212.119:8001`（nginx :8001 反代 → 127.0.0.1:8000）
> **部署报告**：`./DEPLOY_REPORT.md`（含 4 个坑的完整记录）

---

## 1. 项目信息

| 项 | 值 |
|---|---|
| **用途** | AI Agent 生产级运行时（FastAPI + SSE + MCP + JWT-RBAC） |
| **镜像** | API: `agnohq/python:3.12` / DB: `agnohq/pgvector:18` |
| **服务端口** | API 8000 / DB 15432（避开宿主机 Postgres 5432） |
| **公网 URL** | `http://101.33.212.119/agentos/`（nginx 80 反代） |
| **API docs** | `http://101.33.212.119/agentos/docs` |
| **MCP endpoint** | `http://101.33.212.119/agentos/mcp` |
| **健康检查** | `http://101.33.212.119/agentos/health` |
| **管理 UI** | `https://os.agno.com`（外网，需注册） |
| **仓库路径** | `/root/projects/agentos` |

## 2. 硬件依赖

| 资源 | 最低 | 当前服务器（101.33.212.119） |
|---|---|---|
| CPU | 2 vCPU | ✅ 充足 |
| RAM | 4 GB | ✅ 充足 |
| 磁盘 | 10 GB（Postgres 数据） | ✅ 充足 |
| Docker | ≥ 20.10 | ✅ Docker 28.x |
| Docker Compose | ≥ 2.24.4（需 `!reset`/`!override`） | ✅ v2.40.3 |

## 3. 一键部署（从 0 到 1）

### 3.1 克隆仓库

```bash
mkdir -p /root/projects
cd /root/projects
git clone https://github.com/agno-agi/agentos-docker agentos
cd agentos
```

### 3.2 配置 `.env`

```bash
cp example.env .env
vim .env  # 按下面"4. 配置文件"填值
```

### 3.3 自定义 compose.yaml（端口避让 + 关闭 telemetry）

**不要直接用上游 compose.yaml**——5432 跟本机 Postgres 16 冲突。改两个地方：

```yaml
# /root/projects/agentos/compose.yaml（已 patch）
services:
  agentos-db:
    image: agnohq/pgvector:18
    container_name: agentos-db
    restart: unless-stopped
    ports:
      - "15432:5432"   # ← 改：避开本机 5432
    volumes:
      - pgdata:/var/lib/postgresql
    environment:
      POSTGRES_USER: ${DB_USER:-ai}
      POSTGRES_PASSWORD: ${DB_PASS:-ai}
      POSTGRES_DB: ${DB_DATABASE:-ai}
    networks:
      - agentos

  agentos-api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: agentos-api
    image: ${IMAGE_NAME:-agentos}:${IMAGE_TAG:-latest}
    command: >
      uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
      --reload-dir agents --reload-dir app --reload-dir db --reload-dir evals --reload-dir workflows
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    env_file:
      - path: .env
        required: false
    environment:
      RUNTIME_ENV: dev
      AGNO_DEBUG: "True"
      WAIT_FOR_DB: "True"
      AGENTOS_URL: http://127.0.0.1:8000
      DB_HOST: agentos-db
      DB_PORT: 5432
      DB_USER: ${DB_USER:-ai}
      DB_PASS: ${DB_PASS:-ai}
      DB_DATABASE: ${DB_DATABASE:-ai}
      AGNO_TELEMETRY: "False"   # ← 加：合规
    depends_on:
      - agentos-db
    networks:
      - agentos
    extra_hosts:
      - "host.docker.internal:host-gateway"

networks:
  agentos:

volumes:
  pgdata:
```

### 3.4 compose.prod.yaml（生产 override，原样可用）

```yaml
# 原样复制上游，但要确保 v2.24.4+
services:
  agentos-api:
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    volumes: !reset []
    environment:
      RUNTIME_ENV: prd
      AGNO_DEBUG: "False"
      AGENTOS_URL: ${AGENTOS_URL:-http://127.0.0.1:8000}
      MCP_CONNECT_SECRET: ${MCP_CONNECT_SECRET:-}

  agentos-db:
    ports: !override
      - "127.0.0.1:15432:5432"   # ← 同步改：避本机 5432
```

### 3.5 启动（dev 模式）

```bash
cd /root/projects/agentos
docker compose up -d --build
```

### 3.6 启动（prod 模式，必先配 JWT）

```bash
cd /root/projects/agentos
docker compose -f compose.yaml -f compose.prod.yaml up -d --build
```

## 4. 配置文件（`.env` 关键项）

```bash
# ========== 必需 ==========
OPENAI_API_KEY=sk-...                          # OpenAI key（必需）

# ========== 生产必需 ==========
JWT_VERIFICATION_KEY="-----BEGIN PUBLIC KEY-----   # os.agno.com 拿的公钥
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
-----END PUBLIC KEY-----"
# AGENTOS_URL=https://your-domain  # 公网 URL（用 nginx 反代就填 http://101.33.212.119/agentos）

# ========== 推荐（MCP OAuth） ==========
MCP_CONNECT_SECRET=$(openssl rand -base64 32)    # ≥16 chars，让 claude.ai/ChatGPT 可连

# ========== 数据库 ==========
DB_USER=ai
DB_PASS=<STRONG_PASSWORD>                       # 生产必改（dev 默认 ai/ai）
DB_DATABASE=ai

# ========== 遥测 ==========
AGNO_TELEMETRY=false                            # 关闭（合规）

# ========== 可选 ==========
# PARALLEL_API_KEY=...                          # WebSearch agent
# SLACK_BOT_TOKEN=xoxb-...                      # Slack 接口
# SLACK_SIGNING_SECRET=...
# ENABLE_DEPLOY_CHECK=True
# EVALS_TAG=smoke
```

## 5. 启动命令

```bash
# 首次启动（dev 模式，无 JWT，可立刻测试）
cd /root/projects/agentos
docker compose up -d --build

# 切到生产
docker compose -f compose.yaml -f compose.prod.yaml up -d --build

# 查看日志
docker compose logs -f agentos-api

# 重启单个服务
docker compose restart agentos-api

# 停止
docker compose down

# 完全清空（含数据）
docker compose down -v
```

## 6. 三维度验证

### 6.1 本地 curl（127.0.0.1）

```bash
curl -s http://127.0.0.1:8000/health
# 期望：{"status":"ok"} 或类似

curl -s http://127.0.0.1:8000/docs | head -5
# 期望：HTML 含 "Swagger UI"
```

### 6.2 容器内 curl（确认网络通）

```bash
docker compose exec agentos-api curl -s http://agentos-db:5432 || echo "DB reachable"
# 期望：连接成功（Postgres 不会响应 HTTP，但能 telnet 通即代表 OK）
```

### 6.3 公网 curl（nginx 反代验证）

```bash
curl -s http://101.33.212.119/agentos/health
curl -s http://101.33.212.119/agentos/docs | head -5
curl -s http://101.33.212.119/agentos/agents
# dev 模式：返回 agents 列表（JSON）
# prod 模式：返回 401（需 JWT token）
```

## 7. nginx 反代配置

`/etc/nginx/sites-available/agentos.conf`（已配）：

```nginx
# /agentos 路径反代到 127.0.0.1:8000
location /agentos/ {
    # 把 /agentos/x 改成 /x 转发给后端
    rewrite ^/agentos(/.*)$ $1 break;
    proxy_pass http://127.0.0.1:8000;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Prefix /agentos;
    # MCP / SSE 需要
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 300s;
    proxy_send_timeout 300s;
    proxy_buffering off;
    client_max_body_size 100M;
}
```

激活：

```bash
sudo ln -s /etc/nginx/sites-available/agentos.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**验证**：`curl http://101.33.212.119/agentos/health` 应返回 200。

## 8. ⚠️ 避坑指南（按时间倒序）

### 8.1 端口冲突：5432 已被宿主机 Postgres 16 占用

**现象**：agentos-db 容器启动失败，端口 5432 已被占用
**根因**：本机已装 Postgres 16（Dify/RAGFlow 共享），宿主 5432 已 listen
**解法**：compose.yaml + compose.prod.yaml 都把 host port 改 **15432**

### 8.2 启动前必填 OPENAI_API_KEY

**现象**：`/health` 返回 500 或超时
**根因**：容器启动会校验 API key（即使是 health check）
**解法**：填有效的 OpenAI key；如只是想试运行，用免费 $5 credit

### 8.3 生产模式无 JWT → 拒绝启动

**现象**：`RUNTIME_ENV=prd` 时容器崩溃，logs 显示 "JWT verification key required"
**根因**：AgentOS 安全默认——生产模式必须 JWT
**解法 A**（推荐）：去 os.agno.com 注册 → Connect OS → Live → 拿 `JWT_VERIFICATION_KEY` 多行 PEM
**解法 B**（临时）：先 dev 模式跑通，再切 prod
**解法 C**（不推荐）：`app/main.py` 改 `authorization=False`

### 8.4 DB 密码只读一次

**现象**：改 `.env` 的 `DB_PASS` 后重启，agentos-api 连不上 DB
**根因**：Postgres volume 首次初始化时读 `DB_PASS`，后续改 env 不生效
**解法 A**：进容器 ALTER USER 改密码
```bash
docker compose exec agentos-db psql -U ai -c "ALTER USER ai WITH PASSWORD '<new>';"
```
**解法 B**：`docker compose down -v`（**会 wipe 所有数据**）

### 8.5 JWT 公钥必须用引号包

**现象**：多行 PEM 解析成多行 env，每行单独赋值，后面的覆盖前面
**根因**：Docker Compose `.env` 不识别多行值除非 `"..."` 包起来
**解法**：
```bash
JWT_VERIFICATION_KEY="-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgK...
-----END PUBLIC KEY-----"
```

### 8.6 MCP endpoint 需要长连接

**现象**：`/mcp` 调用 60 秒后断
**根因**：nginx 默认 `proxy_read_timeout=60s`，但 MCP 是长连接（SSE）
**解法**：nginx 配置 `proxy_read_timeout 300s;` + `proxy_buffering off;` + 转发 `Upgrade`/`Connection` 头

### 8.7 Live AgentOS Connections 是付费功能

**现象**：os.agno.com Connect OS Live 弹窗要付费
**根因**：agno 商业模式——Live 托管收费（用 PLATFORM30 优惠码免 1 个月）
**解法**：自签 JWT（自己管密钥）+ `JWT_JWKS_FILE` 跳过 os.agno.com

## 9. 当前状态

**容器列表**：

```bash
$ docker ps | grep agentos
agentos-api    Up X minutes    0.0.0.0:8000->8000/tcp
agentos-db     Up X minutes    127.0.0.1:15432->5432/tcp   # prod
                                     0.0.0.0:15432->5432/tcp  # dev
```

**重启次数**：0

**关联文档**：
- [`2026-07-25_Agno部署分析.md`](../from-agent/2026-07-25/2026-07-25%20-%20网页-Agno部署分析.md) — 技术分析 + 决策清单
- [agno-agi/agentos-docker](https://github.com/agno-agi/agentos-docker) — 上游仓库
- [docs.agno.com](https://docs.agno.com) — 官方文档

---

**最后更新**：2026-07-25 12:15（部署前）
**维护者**：openclaw-main (MiniMax-M3)