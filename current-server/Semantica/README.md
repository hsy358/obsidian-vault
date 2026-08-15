# Semantica 部署手册（当前服务器）

> 本目录专门存放 Semantica 在当前服务器（101.33.212.119）的部署信息。
> 与公众号归档文章的时间线报告分离，本 README 提供**可复现的部署 SOP**。

## 1. 项目信息

| 项 | 值 |
|---|---|
| **用途** | 开源版 Palantir —— AI 决策溯源 / Context Graph / Decision Intelligence |
| **GitHub** | <https://github.com/semantica-agi/semantica> |
| **版本** | v0.6.5 |
| **协议** | MIT |
| **部署路径** | `/root/projects/semantica/` |
| **公网 URL** | `http://semantica.101.33.212.119.nip.io/`（标准 80 端口，子域名反代） |
| **Knowledge Explorer** | <http://101.33.212.119:8100/>（FastAPI + React 前端） |
| **API 健康检查** | `GET /api/health` → `{"status":"ok"}` |
| **API endpoints** | **74 个**（决策 / 因果链 / 合规 / 先例 / 溯源 / 导出...） |
| **CLI 入口** | `semantica`（13 个子命令：ingest / extract / reason / decision / kg / embed / validate / provenance...） |

## 2. 硬件依赖

| 资源 | 最低 | 当前服务器 | 评估 |
|---|---|---|---|
| CPU | 2 核 | 8 核 | ✅ |
| 内存（空闲） | 4 GB | 12 GB 可用 | ✅ |
| 磁盘 | 5 GB | 112 GB 可用 | ✅ |
| 网络 | 出站 HTTPS | ✅ | ✅ |
| GPU | **不需要**（CPU-only 部署） | — | ✅ |

## 3. 部署架构

```
┌────────────────────────────────────────────────┐
│  Host (101.33.212.119)                         │
│  ┌──────────────────────────┐                  │
│  │ semantica-explorer       │ systemd unit     │
│  │ uvicorn :8100            │ (.venv)          │
│  │ FastAPI + React frontend │                  │
│  └────────┬─────────────────┘                  │
│           │ FALKORDB_HOST=localhost             │
│           │ FALKORDB_PORT=6382                  │
│           ▼                                    │
│  ┌──────────────────────────┐                  │
│  │ semantica-falkordb       │ Docker Compose   │
│  │ Redis protocol :6382 → 6379                 │
│  │ (图数据库, persistent data) │                │
│  └──────────────────────────┘                  │
└────────────────────────────────────────────────┘
```

## 4. 一键部署（从 0 到 1）

### 4.1 前置条件

```bash
# 系统包（应已装）
python3 --version   # ≥3.8 (本环境 3.12.3)
docker --version    # ≥20.10

# 国内 pip 镜像加速
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
```

### 4.2 创建项目目录

```bash
mkdir -p /root/projects/semantica/{logs,data,config,data/falkordb}
cd /root/projects/semantica
```

### 4.3 启动 FalkorDB 容器

`docker-compose.yml`：

```yaml
services:
  falkordb:
    image: falkordb/falkordb:latest
    container_name: semantica-falkordb
    ports:
      - "6382:6379"   # 避开 6379 冲突（已被 5 个 Redis 占用）
    volumes:
      - /root/projects/semantica/data/falkordb:/data
    networks:
      - semantica-net
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "-p", "6379", "PING"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  semantica-net:
    driver: bridge
```

```bash
docker compose up -d
docker exec semantica-falkordb redis-cli -p 6379 PING  # 应返回 PONG
```

### 4.4 创建 Python venv + 安装依赖（轻量路线）

> ⚠️ **不要直接 `pip install semantica[explorer]`** —— 默认 dependencies 会拉 `torch` 的 NVIDIA CUDA 全套包（~2GB），且服务器无 GPU。
> 用 `--no-deps` 路线：先装 semantica 本体，再按需补依赖。

```bash
cd /root/projects/semantica
python3 -m venv .venv
.venv/bin/pip install --upgrade pip

# Step 1: semantica 本体（无依赖，~2MB）
.venv/bin/pip install --no-cache-dir --no-deps "semantica==0.6.5"

# Step 2: explorer 必需库 + 核心依赖
.venv/bin/pip install --no-cache-dir \
  fastapi 'uvicorn[standard]' websockets python-multipart defusedxml \
  numpy pandas networkx rdflib pydantic click pyyaml \
  tqdm loguru

# Step 3: ContextGraph 必需库（启动时会触发 import）
.venv/bin/pip install --no-cache-dir scipy scikit-learn

# Step 4: explorer 内部 import 链需要
.venv/bin/pip install --no-cache-dir rich httpx GitPython chardet
```

**最终 venv 大小**：~455 MB（vs 官方 docker 镜像 ~3-4 GB）

### 4.5 创建 .env 配置

`/root/projects/semantica/.env`：

```bash
# FalkorDB 连接
FALKORDB_HOST=localhost
FALKORDB_PORT=6382

# Explorer 配置
SEMANTICA_API_KEY=local-dev-key-change-me
SEMANTICA_ALLOW_ANONYMOUS=true
ALLOWED_ORIGINS=http://localhost:8100,http://127.0.0.1:8100,http://101.33.212.119:8100

# matplotlib 非交互后端（避免 "no display" 报错）
MPLBACKEND=Agg

# Explorer 监听端口（避开 agentos-api 占用的 8000）
EXPLORER_HOST=0.0.0.0
EXPLORER_PORT=8100
```

### 4.6 systemd unit（守护进程）

`~/.config/systemd/user/semantica-explorer.service`：

```ini
[Unit]
Description=Semantica Knowledge Explorer (FastAPI + frontend)
Documentation=https://github.com/semantica-agi/semantica
After=network-online.target
Wants=network-online.target
# 注：falkordb 容器由 docker compose 单独管理（systemd user 不能依赖 system 服务）

[Service]
Type=simple
WorkingDirectory=/root/projects/semantica
EnvironmentFile=/root/projects/semantica/.env
ExecStart=/root/projects/semantica/.venv/bin/python -m uvicorn semantica.explorer.app:app --host 0.0.0.0 --port 8100
Restart=always
RestartSec=10
StandardOutput=append:/root/projects/semantica/logs/explorer.log
StandardError=append:/root/projects/semantica/logs/explorer.err
MemoryMax=6G
MemoryHigh=5G

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable semantica-explorer.service
systemctl --user start semantica-explorer.service
systemctl --user status semantica-explorer.service
```

## 5. 启动命令

```bash
# 启 FalkorDB
cd /root/projects/semantica && docker compose up -d

# 启 Explorer
systemctl --user start semantica-explorer.service

# 看日志
journalctl --user -u semantica-explorer.service -f
# 或
tail -f /root/projects/semantica/logs/explorer.log
```

## 6. 三维验证

### 6.1 本机

```bash
curl -sI http://127.0.0.1:8100/         # 405 (GET-only)
curl -sL http://127.0.0.1:8100/ | head  # 应返回 HTML 含 "Semantica Knowledge Explorer"
curl -s http://127.0.0.1:8100/api/health  # {"status":"ok"}
```

### 6.2 公网

```bash
curl -sI http://101.33.212.119:8100/
curl -s http://101.33.212.119:8100/api/health
```

### 6.3 后端健康

```bash
docker ps | grep semantica                # semantica-falkordb Up (healthy)
systemctl --user is-active semantica-explorer.service   # active
.venv/bin/semantica doctor                # CLI 环境检查（详见下方）
```

### 6.4 `semantica doctor` 输出

```
Check                Status     Note
─────────────────────────────────────────────────────
Python                ✓         3.12.3
semantica             ✓         0.6.5
rich                  ✓         15.0.0
Graph store           ✓         memory (always available)
Vector store          ✗         No module named 'faiss'  (影响 embed 命令，不影响决策/图谱)
OpenAI                ⚠         OPENAI_API_KEY not set   (LLM 未启用)
Anthropic             ⚠         ANTHROPIC_API_KEY not set
Groq                  ⚠         GROQ_API_KEY not set
Config file           ⚠         using defaults
Log directory         ✓         /root/projects/semantica/logs writable
```

> ✅ **CLI/Explorer 全部可用**。Vector store 缺失只影响 `embed` / 向量搜索，决策/图谱/溯源/Datalog 推理功能不受影响。

## 7. ⚠️ 避坑指南（按时间倒序）

### 坑 1：8000 端口被 agentos-api 占用

**现象**：`ERROR: [Errno 98] address already in use on 0.0.0.0:8000`
**根因**：`agentos-api` 容器（uvicorn app.main:app）已占 8000（pid 9136 是 docker-proxy）
**修法**：改用 **8100**（已改 .env 和 service 文件）
**永久规则**：启 explorer 前先 `ss -tlnp | grep -E ':8000|:8100'` 二次确认

### 坑 2：`pip install semantica[explorer]` 会拉 NVIDIA CUDA 全套

**现象**：pip 卡 20+ 分钟，下 torch 526MB + nvidia-cudnn 366MB + nvidia-cusparselt 170MB + ...
**根因**：semantica 默认 dependencies 含 `torch>=1.13.1`，torch setup.py 标了 NVIDIA extras，pip 自动拉
**修法**：用 `--no-deps` 装 semantica 本体，按需补依赖
**永久规则**：semantica 永远走 **轻量路线**（455MB venv vs 官方 3-4GB 镜像）；GPU 包只在显式要求时才装

### 坑 3：pytorch.org CPU 源拉的依赖极慢

**现象**：`pip install torch==2.13.0 --index-url https://download.pytorch.org/whl/cpu`，5+ 分钟还在下依赖
**根因**：PyTorch 源只提供 torch 自己的包，依赖（sympy/networkx/jinja2 等）要从标准 PyPI 下，但 PyTorch 源 index 不包含这些，速度被卡
**修法**：直接放弃这个路线，改用 `--no-deps` 路线（见坑 2）
**永久规则**：要 CPU torch 时，直接用 `--no-deps` + 标准 PyPI 源（或阿里云 mirror），不要碰 pytorch.org 源

### 坑 4：explorer 启动时 import 链报各种 ModuleNotFoundError

**现象**：`from rich.console import Console` → `ModuleNotFoundError: No module named 'rich'`
**现象 2**：`from scipy.spatial.distance import cosine` → `ModuleNotFoundError: No module named 'scipy'`
**根因**：semantica 默认 dependencies 列了 rich / scipy，但 `pip install --no-deps semantica` 不装这些
**修法**：按启动报错顺序补装：rich, scipy, scikit-learn, httpx, GitPython, chardet
**永久规则**：轻量路线下，每次 `pip install --no-deps semantica` 都要按报错补装 4-6 个核心库，**一次性装齐**：

```bash
.venv/bin/pip install --no-cache-dir \
  fastapi 'uvicorn[standard]' websockets python-multipart defusedxml \
  numpy pandas networkx rdflib pydantic click pyyaml \
  tqdm loguru scipy scikit-learn rich httpx GitPython chardet
```

### 坑 5：matplotlib 报 "no display"

**现象**：explorer 启动时报 `_tkinter.TclError: no display`
**根因**：matplotlib 默认后端 TkAgg 需要 X display
**修法**：在 .env 里加 `MPLBACKEND=Agg`
**永久规则**：所有 matplotlib 集成的服务，systemd unit / .env 必须设 `MPLBACKEND=Agg`

### 坑 6：FalkorDB 默认 6379 端口冲突

**现象**：`docker compose up -d` 失败 "port 6379 already in use"
**根因**：服务器 5 个 Redis 已占 6379
**修法**：host port 改 **6382**（container 内部仍 6379 不变）
**永久规则**：新 Redis-类服务默认走 6382+，避 6379 冲突

### 坑 7：systemd user 找不到 docker.service

**现象**：`Failed to start semantica-explorer.service: Unit docker.service not found`
**根因**：docker.service 是 system 级，user systemd 看不到
**修法**：service 文件去掉 `Requires=docker.service`，只保留 `After=network-online.target`
**永久规则**：systemd user unit 永远不依赖 system 级服务；falkordb 用 docker compose 单独管

## 8. 当前状态

```
容器：
  semantica-falkordb    Up 52 minutes (healthy)   0.0.0.0:6382->6379/tcp
                          RestartCount: 0
                          镜像: falkordb/falkordb:latest
                          内存: ~30MB
                          数据: /root/projects/semantica/data/falkordb/

systemd user 服务：
  semantica-explorer.service    Active: active (running)
                          Main PID: 3608950 (python)
                          Memory: 111.3MB (high 5.0G, max 6.0G)
                          Tasks: 21
                          日志: /root/projects/semantica/logs/explorer.{log,err}

资源占用：
  venv:  455 MB
  data:  8 KB（falkordb 刚启，暂无图数据）
  磁盘总计: < 1 GB
  内存总计: ~150 MB（falkordb 30MB + explorer 111MB）
```

## 9. 关联文档

- [公众号原文归档（2026-08-12）](../../from-agent/2026-08-12/2026-08-12%20-%20公众号-自称开源版Palantir-Semantica.md)
- [冲突排查与部署可行性评估（2026-08-12）](../../from-agent/2026-08-12/2026-08-12%20-%20Semantica_冲突排查与部署可行性评估.md)
- [时间线报告（待补：首次部署 commit message + 公网 URL 实测）]（见 git log）
- [GitHub repo](https://github.com/semantica-agi/semantica)
- [官方 docs](https://docs.getsemantica.ai/)

## 10. 待办 / 后续

- [ ] 添加 spacy 模型 `en_core_web_sm`（~50MB），启用 NER 功能（要先装 spacy）
- [ ] 添加 faiss-cpu，启用 `embed` 命令（~30MB）
- [ ] 测试一次端到端 decision 记录 + trace_decision_chain
- [x] 公网 URL 反代到 80（2026-08-15 完成，详见 §11）
- [ ] 写 Langfuse ↔ Semantica 集成 demo（两者互补，可串起来）

## 11. 公网反代（2026-08-15 加）

### 11.1 为什么用子域名而不是 `/semantica/` 路径前缀

Semantica 前端是 Vite/React SPA，HTML 里所有静态资源都用**绝对路径**（`<script src="/assets/index-X.js">`、`href="/assets/..."`）。如果走 `/semantica/` 路径前缀，浏览器解析这些绝对路径时会绕开 nginx 反代（因为它们不在 `/semantica/*` 范围内），全 404。

子域名方案 → 前端零修改、零 sub_filter hack。

### 11.2 域名方案

`semantica.101.33.212.119.nip.io`（nip.io 是 wildcard DNS，自动把 `*.IP.nip.io` 解析成 `IP`）

- 公共 DNS 验证：`dig +short @8.8.8.8 semantica.101.33.212.119.nip.io` → `101.33.212.119` ✅
- 无需注册域名、无需 SSL（HTTP）、零运维

### 11.3 nginx 配置

`/etc/nginx/sites-available/semantica.conf`：

```nginx
server {
    listen 80;
    server_name semantica.101.33.212.119.nip.io;

    client_max_body_size 100M;
    access_log /var/log/nginx/semantica.access.log;
    error_log /var/log/nginx/semantica.error.log;

    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 120s;
    proxy_send_timeout 120s;

    location / {
        proxy_pass http://127.0.0.1:8100;
    }
}
```

**重要**：`proxy_set_header Host $host;` 让 backend 收到 `Host: semantica.101.33.212.119.nip.io`，backend 据此做 CORS 校验。必须在 `.env` 的 `ALLOWED_ORIGINS` 加这个 origin（否则前端 fetch 会被 CORS 拦截）。

### 11.4 `.env` 改动

```diff
-ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000,http://101.33.212.119:8000
+ALLOWED_ORIGINS=http://localhost:8100,http://127.0.0.1:8100,http://101.33.212.119:8100,http://semantica.101.33.212.119.nip.io
```

注意端口从 8000 → 8100（因为 8000 被 agentos-api 占）。

### 11.5 生效顺序

```bash
# 1. nginx -t + ln -s
ln -sf /etc/nginx/sites-available/semantica.conf /etc/nginx/sites-enabled/semantica.conf
systemctl reload nginx

# 2. .env 改了 → 必须 restart backend（不 restart 不重读 env）
systemctl --user restart semantica-explorer.service

# 3. 三维度验证
curl -s -m 5 -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8100/                        # 直连 backend
curl -s -m 10 -o /dev/null -w "%{http_code}\n" -H "Host: semantica.101.33.212.119.nip.io" http://101.33.212.119/   # 模拟子域名访问
curl -s -m 10 -o /dev/null -w "%{http_code}\n" http://semantica.101.33.212.119.nip.io/      # 真实子域名访问
```

### 11.6 验证结果（2026-08-15 10:35）

| 测试 | URL | 结果 |
|---|---|---|
| 直连 backend | `http://127.0.0.1:8100/` | HTTP 200 (561B) |
| 模拟子域名 Host | `Host: semantica.101.33.212.119.nip.io` @ 101.33.212.119 | HTTP 200 (561B) |
| 真实子域名 | `http://semantica.101.33.212.119.nip.io/` | HTTP 200 (561B) |
| 健康检查 | `/api/health` | `{"status":"ok"}` |
| OpenAPI | `/openapi.json` | Semantica Knowledge Explorer v0.6.5，74 paths / 77 endpoints |

### 11.7 ⚠️ 安全提醒

backend 启动日志会打：

> `Explorer is running with SEMANTICA_ALLOW_ANONYMOUS=true — all API routes are unauthenticated. Do not expose this process beyond localhost.`

当前我们用了 ANONYMOUS=true 是为了 demo 用（不用 API key 也能调）。**何大人先体验，认可以后再加 auth**：
- 关闭 ANONYMOUS：`SEMANTICA_ALLOW_ANONYMOUS=false`
- 强制要求 `X-API-Key` header（值=`.env` 里 `SEMANTICA_API_KEY`）
- 跟 Langfuse / Dify 那种 token-gate 思路一致