---
title: Dify 部署手册 + 避坑指南
date: 2026-07-06
type: deployment-handbook
status: active
service: Dify
port: 8080（容器）→ 80（宿主机 nginx 反代）
public_url: http://101.33.212.119/install
deploy_path: /root/projects/dify
---

# 🟢 Dify 部署手册 + 避坑指南

> **一句话**：AI Workflow / Agent 编排平台。可视化拖拽 + LLM 应用生产化。Self-hosted CE 版。

---

## 1. 项目信息

| 项 | 值 |
|---|---|
| 用途 | AI Workflow / Agent 编排、LLM 应用生产化 |
| 镜像 | `langgenius/dify-api:1.15.0` + `dify-web:1.15.0` + `dify-plugin-daemon:0.6.3-local` |
| 公网 URL | `http://101.33.212.119/install`（标准 80 端口）|
| 状态 | ✅ **2026-07-06 何大人验证可登录** |
| 部署位置 | `/root/projects/dify/` |

---

## 2. 硬件依赖

| 项 | 最低 | 当前服务器 |
|---|---|---|
| CPU | 4 核 | 8 核 ✅ |
| RAM | 16 GB（Dify 多 worker）| 30 GB ✅ |
| Disk | 50 GB | 315 GB ✅ |
| 关键镜像 | postgres-15 + redis-6 + nginx | 已部署 |
| Vector store | weaviate / milvus / pgvector | **pgvector**（复用现有 PG）|

---

## 3. 一键部署（从 0 到 1）

```bash
# 1. 拉 dify 1.15.0 完整 docker 目录
mkdir -p /root/projects/dify && cd /root/projects/dify
curl -L https://github.com/langgenius/dify/archive/refs/tags/1.15.0.tar.gz | tar xz
# 拷贝 docker 目录
mv dify-1.15.0/docker/* .
rm -rf dify-1.15.0
chmod +x entrypoint.sh  # GitHub 拉下来默认无 x 权限

# 2. 准备 .env
cp .env.example .env

# 3. 宿主机 PG 装 pgvector
apt install -y postgresql-16-pgvector
sudo -u postgres psql -c "CREATE DATABASE dify;"
sudo -u postgres psql -d dify -c "CREATE EXTENSION vector;"

# 4. 改 .env（关键项）
sed -i 's|^DB_HOST=.*|DB_HOST=host.docker.internal|' .env          # 用宿主机 PG
sed -i 's|^DB_PORT=.*|DB_PORT=5432|' .env
sed -i 's|^DB_DATABASE=.*|DB_DATABASE=dify|' .env
sed -i 's|^DB_USERNAME=.*|DB_USERNAME=postgres|' .env
sed -i 's|^DB_PASSWORD=.*|DB_…ostgres|' .env
sed -i 's|^REDIS_HOST=.*|REDIS_HOST=redis|' .env                  # ← 关键：容器名！
sed -i 's|^REDIS_PASSWORD=.*|RED…456|' .env                       # ← 关键：默认密码 difyai123456
sed -i 's|^VECTOR_STORE=.*|VECTOR_STORE=pgvector|' .env
sed -i 's|^EXPOSE_NGINX_PORT=.*|EXPOSE_NGINX_PORT=8080|' .env    # 避开 80 冲突
sed -i 's|^CONSOLE_API_URL=.*|CONSO…119|' .env                    # ← 不要带 /install！
sed -i 's|^CONSOLE_WEB_URL=.*|CONSOLE_WEB_URL=http://101.33.212.119|' .env
sed -i 's|^APP_API_URL=.*|APP…119/v1|' .env
sed -i 's|^APP_WEB_URL=.*|APP_WEB_URL=http://101.33.212.119|' .env
sed -i 's|^SERVICE_API_URL=.*|SERVICE_API_URL=http://101.33.212.119/v1|' .env

# 5. docker-compose.yaml 加 extra_hosts（api/api_websocket/worker/worker_beat/plugin_daemon）
# 用 sed/python 批量加：
python3 << 'PYEOF'
import re
with open('docker-compose.yaml') as f: c = f.read()
for svc in ['api:', 'api_websocket:', 'worker:', 'worker_beat:', 'plugin_daemon:']:
    # 在 service 块内的 networks: 行前插入 extra_hosts
    pass  # 实际实现见 vault 报告
PYEOF

# 6. 启（排除内置 db_postgres/redis/pgvector）
docker compose up -d init_permissions api api_websocket worker worker_beat web nginx plugin_daemon sandbox ssrf_proxy redis
```

---

## 4. 配置文件（.env 关键项）

```bash
# === Core URLs（关键，不要带 /install 子路径）===
CONSOLE_API_URL=http://101.33.212.119          # ← 容器 web 容器用
SERVER_CONSOLE_API_URL=http://api:5001         # ← 容器内
CONSOLE_WEB_URL=http://101.33.212.119
SERVICE_API_URL=http://101.33.212.119/v1
APP_API_URL=http://101.33.212.119/v1
APP_WEB_URL=http://101.33.212.119
NEXT_PUBLIC_SOCKET_URL=ws://101.33.212.119

# === Database（用宿主机 PG）===
DB_HOST=host.docker.internal
DB_PORT=5432
DB_DATABASE=dify
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_PLUGIN_DATABASE=dify_plugin

# === Redis（用内置容器）===
REDIS_HOST=redis            # ← 容器名！
REDIS_PORT=6379
REDIS_PASSWORD=…ai123456    # ← dify 镜像默认密码
REDIS_DB=0
CELERY_BROKER_URL=redis://:…ai123456@redis:6379/1

# === Vector Store（用 pgvector 复用 PG）===
VECTOR_STORE=pgvector

# === Ports ===
EXPOSE_NGINX_PORT=8080      # 容器 nginx 监听 8080
EXPOSE_WORKER_PORT=5001

# === Secret ===
SECRET_KEY=…nssl rand -hex 32>

# === Eddition ===
EDITION=SELF_HOSTED
DEPLOY_ENV=PRODUCTION
```

---

## 5. 启动命令

```bash
cd /root/projects/dify
# 跑 alembic migration（必须 wait init_permissions 完成）
docker compose up -d init_permissions
sleep 30
# 启动主服务
docker compose up -d api api_websocket worker worker_beat web nginx plugin_daemon sandbox ssrf_proxy redis

# 看 migration 进度
docker logs dify-api-1 --tail 30
# 应该看到 "Running migrations" → "Database migration successful!" → "Listening at 5001"
```

---

## 6. 三维度验证

```bash
# 本地
curl -sI http://localhost:8080/install
# 公网（宿主机 nginx 80 反代 8080）
curl -sI http://101.33.212.119/install
# 后端 API
curl -s http://101.33.212.119/console/api/setup
# → 期望 200 + {"step":"not_started","setup_at":null}
# 云端
# web_fetch http://101.33.212.119/install
# → 期望 "© 2026 LangGenius" + 完整 HTML
```

---

## 7. 宿主机 nginx 反代（80 → 8080）

```bash
# /etc/nginx/sites-enabled/default
server {
    listen 80 default_server;
    server_name _;
    client_max_body_size 100M;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 300s;
    proxy_send_timeout 300s;
    location / { proxy_pass http://127.0.0.1:8080; }
}
```

---

## 8. ⚠️ 避坑指南（按时间倒序）

### 坑 1: Dify API 反复重启 → Chrome OOM（最严重）
- **现象**: `dify-api-1` RestartCount=724，Chrome 加载 /install 报 "Out of Memory"
- **根因链**:
  1. 容器没加 `extra_hosts: host-gateway` → host.docker.internal 解析失败
  2. 修好后连宿主机 Redis，但宿主机 Redis protected-mode 拒绝非 loopback
  3. Dify 内置 Redis 镜像默认密码 `difyai123456`，但 .env 写空密码
- **修法**:
  - docker-compose.yaml 给 5 个 service 加 extra_hosts
  - .env: `REDIS_HOST=redis`（容器名）+ `REDIS_PASSWORD=***`
  - 启动 redis service
- **永久规则**: ✅ **任何用宿主机的容器必加 extra_hosts: host-gateway** + **容器间互连优先用容器名**

### 坑 2: Dify 镜像 `host.docker.internal` 镜像构建已处理，但 .env `CONSOLE_API_URL` 误带路径
- **现象**: 浏览器 fetch `/install/console/api/system-features` 404（路径前多了 /install）
- **根因**: .env 里 `CONSOLE_API_URL=http://101.33.212.119/install`（带 /install），Dify entrypoint.sh `export NEXT_PUBLIC_API_PREFIX=${CONSOLE_API_URL}/console/api` → 变成 `http://101.33.212.119/install/console/api`
- **修法**: 改 `CONSOLE_API_URL=http://101.33.212.119`（裸域） + 重启 web 容器
- **永久规则**: ✅ **URL 不要带子路径**（Dify 自动追加 /console/api）

### 坑 3: Dify 内置 Redis 默认密码
- **现象**: api 容器启动报 `AUTH failed`
- **根因**: dify redis 镜像启动命令 `redis-server --requirepass difyai123456`，但 .env 写空密码
- **修法**: `REDIS_PASSWORD=***`
- **永久规则**: ✅ **容器启动时 `docker inspect <c> --format '{{json .Config.Cmd}}'` 看默认密码**

### 坑 4: 宿主机 Redis protected-mode 拒绝外部连接
- **现象**: Dify API 报 `ConnectionError: Error -2 connecting to host.docker.internal:6379`
- **根因**: 之前为 Langfuse 改的 `/etc/redis/redis.conf` `bind 0.0.0.0`，但保留 `protected-mode yes` → 拒绝非 loopback
- **修法**:
  - 方案 A: 宿主机 redis 关 protected-mode（dev only）
  - 方案 B: Dify 用内置 redis 容器（推荐）
- **永久规则**: ✅ **容器间互连优先用容器名（`REDIS_HOST=redis`），不绕道 host.docker.internal**

### 坑 5: pgvector 扩展未装
- **现象**: Dify 启动报 `type "vector" does not exist`
- **根因**: postgres 镜像默认没装 pgvector 扩展
- **修法**: `apt install postgresql-16-pgvector` + `psql -d dify -c "CREATE EXTENSION vector;"`
- **永久规则**: ✅ **Dify 用 pgvector 必装 vector 扩展**

### 坑 6: db_postgres/redis 内置容器被 depends_on 触发
- **现象**: `dify-db_postgres-1` / `dify-redis-1` 被自动拉起
- **根因**: 默认 docker-compose.yaml 包含所有 service，depends_on 会触发
- **修法**: `docker compose up -d <显式列表>` 排除内置 db / redis
- **永久规则**: ✅ **用宿主机的 DB/Redis 时，启动时显式列出 service 排除内置**

### 坑 7: nginx 80 端口冲突
- **现象**: Dify 容器 nginx 监听 80 启动失败
- **根因**: 宿主机 nginx 占用 80
- **修法**: `.env` 设 `EXPOSE_NGINX_PORT=8080` + 宿主机 nginx 80 反代
- **永久规则**: ✅ **容器 nginx 改非标端口，宿主机 nginx 80 反代**（何大人也能用标准 80 端口访问）

### 坑 8: GitHub 拉文件默认无 x 权限
- **现象**: `entrypoint.sh` 执行报 `Permission denied`
- **根因**: GitHub 拉下来的 .sh 默认无 execute 权限
- **修法**: `chmod +x entrypoint.sh`
- **永久规则**: ✅ **任何从 GitHub 拉的可执行脚本必 `chmod +x`**

### 坑 9: 100+ alembic migrations 耗时长
- **现象**: `dify-api-1` 启动 5+ 分钟才 `Listening at 5001`
- **根因**: Dify 1.15.0 数据库 schema 100+ alembic migrations
- **修法**: 耐心等（看 logs 确认 `Running migrations` 进度）
- **永久规则**: ⚠️ Dify 第一次启动需 5+ 分钟，dev 阶段不要急着 debug

### 坑 10: SPA 相对路径在 /install 下加前缀
- **现象**: 浏览器 fetch `/install/console/api/system-features`（多了 /install）
- **根因**: Dify nginx `location /console/api` 精确前缀匹配，`/install/console/api` 不匹配走 SPA fallback
- **修法**（**未做，14:10 后放弃**）: 加 `location ~* ^/install/(console/api|api|v1|...)`
- **状态**: ⚠️ **何大人 2026-07-06 20:06 手动验证可登录，证实不需要这个 nginx 修改**——Dify 1.15.0 镜像可能内置 base path 处理

---

## 9. 当前状态（2026-07-06 20:08）

| 容器 | 状态 | restart |
|---|---|---|
| dify-api-1 | Up 6h healthy | 0 |
| dify-api_websocket-1 | Up 6h | 0 |
| dify-worker-1 | Up 6h | 0 |
| dify-worker_beat-1 | Up 6h | 0 |
| dify-web-1 | Up 3h | 0（之前 restart=724，已修）|
| dify-plugin_daemon-1 | Up 6h | 0 |
| dify-nginx-1 | Up 10h | 0 |
| dify-redis-1 | Up 6h healthy | 0（内置）|
| dify-db_postgres-1 | Up 6h healthy | 0（内置，未用）|

**对外服务**：`http://101.33.212.119/install`（80 → 8080 反代）

---

## 10. 关联文档

- `/root/vault/current-server/2026-07-06_md_三个URL部署修复完成报告.md`
- MEMORY.md 顶部「2026-07-06 14:10 教训：Dify API restart 循环导致 Chrome OOM」
