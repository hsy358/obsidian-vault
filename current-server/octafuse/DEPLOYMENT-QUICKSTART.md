# Octafuse Gateway 部署手册（精简版）

> 一份**可复制粘贴**的部署指南。配套详本版：`./README.md`（含全部避坑细节）。
> **目标**：在 Ubuntu 22.04 / Docker 29.x 服务器上从零部署 Octafuse Gateway v2.1.2

## TL;DR — 一句话总结

```bash
git clone https://github.com/OctaFuse/octafuse-gateway.git && \
cd octafuse-gateway && \
sed -i 's|dl-cdn.alpinelinux.org|mirrors.aliyun.com|g' Dockerfile.proxy Dockerfile.admin Dockerfile.migrate && \
npm config set registry https://registry.npmmirror.com && \
docker buildx build --load -f Dockerfile.proxy -t octafuse-proxy:local . && \
docker buildx build --load -f Dockerfile.admin -t octafuse-admin:local . && \
docker buildx build --load -f Dockerfile.migrate -t octafuse-migrate:local .
# 之后跑 docker compose 起 4 容器（见 Step 4-7）
```

**预计时长**：源码拉取 45s + 3 镜像并发 build 4min + 启动容器 2min + 改默认密码 30s = **约 8 分钟**

---

## 0. 前置要求

| 项 | 最低 | 推荐 |
|---|---|---|
| 操作系统 | Ubuntu 22.04 | Ubuntu 24.04 |
| Docker | 24.x | 29.x（`docker buildx` 内置）|
| Node.js | 不需要（容器内自带）| — |
| 内存 | 1 GB | 2 GB |
| 磁盘 | 2 GB | 5 GB |
| 公网 IP | 必备（TLS / 反代用）| — |
| 域名 / 子域名 | 1 个（推荐 2 个独立子域名）| — |

**端口分配（按本机现状，避开已用）**：
- 5436（PostgreSQL）
- 8787（Proxy，对外 API 网关）
- 8789（Admin，Next.js 后台）
- 80 / 443（nginx 反代，必备；本机已被 Dify 占用 :80，我们走子域名）

---

## 1. 克隆源码

```bash
mkdir -p /root/projects/octafuse && cd /root/projects/octafuse
git clone --depth=1 https://github.com/OctaFuse/octafuse-gateway.git
cd octafuse-gateway
```

> ⚠️ **不要 `docker pull ghcr.io/octafuse/...`**——GHCR 走 GitHub Pages CDN，单层 49MB 速度 33B/s，本环境拉 4 小时没拉完。本手册全程用本地源码 build。

---

## 2. 准备 Docker 镜像

### 2.1 改 Dockerfile 用阿里云 APK 镜像

```bash
# Alpine 默认源 dl-cdn.alpinelinux.org 在国内较慢，sed 换成阿里云
for f in Dockerfile.proxy Dockerfile.admin Dockerfile.migrate; do
  sed -i 's|dl-cdn.alpinelinux.org|mirrors.aliyun.com|g' "$f"
done
```

### 2.2 配 npm 镜像

```bash
npm config set registry https://registry.npmmirror.com
```

### 2.3 Build 3 个镜像（Docker 29.x 必须用 `buildx --load`）

```bash
# 串行 build（简单可调试；总耗时 ~5 分钟）
docker buildx build --load -f Dockerfile.proxy   -t octafuse-proxy:local   .
docker buildx build --load -f Dockerfile.admin   -t octafuse-admin:local   .
docker buildx build --load -f Dockerfile.migrate -t octafuse-migrate:local .

# 并发 build（推荐；总耗时 ~3 分钟）
nohup setsid bash -c 'docker buildx build --load -f Dockerfile.proxy   -t octafuse-proxy:local   . >/tmp/build-proxy.log   2>&1' </dev/null >/dev/null 2>&1 & disown
nohup setsid bash -c 'docker buildx build --load -f Dockerfile.admin   -t octafuse-admin:local   . >/tmp/build-admin.log   2>&1' </dev/null >/dev/null 2>&1 & disown
nohup setsid bash -c 'docker buildx build --load -f Dockerfile.migrate -t octafuse-migrate:local . >/tmp/build-migrate.log 2>&1' </dev/null >/dev/null 2>&1 & disown

# 等 3 个 build 完，验一下
sleep 240 && docker images | grep octafuse
# 期望：3 个镜像，每个 ~300MB
```

> ⚠️ **`nohup setsid` 必须双重脱离**——单纯 `&` + `disown` 在 OpenClaw exec 父进程被 SIGKILL 时会带走子进程。`setsid` 才能真正脱离父 session。

---

## 3. 生成凭据

```bash
cat > /root/projects/octafuse/.secrets <<EOF
ADMIN_USERNAME=admin
ADMIN_PASSWORD=$(openssl rand -base64 15 | tr -d '+/')
MASTER_KEY=$(openssl rand -hex 16)
POSTGRES_DB=octafuse
POSTGRES_USER=octafuse
POSTGRES_PASSWORD=$(openssl rand -base64 18 | tr -d '+/')
EOF
chmod 600 /root/projects/octafuse/.secrets
cat /root/projects/octafuse/.secrets
```

> ⚠️ **ADMIN_PASSWORD 用 `tr -d '+/'` 去掉 + 和 / 字符**——某些 shell 解释 base64 + 号会变空格，/ 会当路径分隔。
> ⚠️ **MASTER_KEY 32 位 hex**（16 字节）——OpenAI API Key 风格。

---

## 4. 写 docker-compose.yaml

文件 `/root/projects/octafuse/docker-compose.yaml`：

```yaml
name: octafuse

services:
  octafuse-pg:
    image: postgres:16-alpine
    container_name: octafuse-pg
    restart: unless-stopped
    env_file: .env
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      TZ: ${TZ}
    volumes:
      - octafuse_pg:/var/lib/postgresql/data
    networks:
      octafuse-net:
        ipv4_address: 172.30.0.10
    ports:
      - "127.0.0.1:5436:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  octafuse-migrate:
    image: ${GATEWAY_MIGRATE_IMAGE}
    container_name: octafuse-migrate
    profiles: ["migrate"]
    env_file: .env
    environment:
      DATABASE_URL: postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@octafuse-pg:5432/${POSTGRES_DB}
      TZ: ${TZ}
    networks:
      octafuse-net:
        ipv4_address: 172.30.0.30
    depends_on:
      octafuse-pg:
        condition: service_healthy

  octafuse-proxy:
    image: ${GATEWAY_PROXY_IMAGE}
    container_name: octafuse-proxy
    restart: unless-stopped
    env_file: .env
    environment:
      DATABASE_URL: postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@octafuse-pg:5432/${POSTGRES_DB}
      TZ: ${TZ}
      PORT: "8787"
      AUTO_MIGRATE: "0"      # 迁移走独立 profile
    networks:
      octafuse-net:
        ipv4_address: 172.30.0.20
    ports:
      - "0.0.0.0:8787:8787"
    depends_on:
      octafuse-pg:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "node -e \"fetch('http://127.0.0.1:'+(process.env.PORT||8787)+'/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))\""]
      interval: 30s
      timeout: 5s
      start_period: 40s
      retries: 3

  octafuse-admin:
    image: ${GATEWAY_ADMIN_IMAGE}
    container_name: octafuse-admin
    restart: unless-stopped
    env_file: .env
    environment:
      DATABASE_URL: postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@octafuse-pg:5432/${POSTGRES_DB}
      TZ: ${TZ}
      PORT: "8789"
      AUTO_MIGRATE: "0"
      ADMIN_USERNAME: ${ADMIN_USERNAME}
      ADMIN_PASSWORD: ${ADMIN_PASSWORD}
    networks:
      octafuse-net:
        ipv4_address: 172.30.0.21
    ports:
      - "0.0.0.0:8789:8789"
    depends_on:
      octafuse-pg:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "node -e \"fetch('http://127.0.0.1:'+(process.env.PORT||8789)+'/').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))\""]
      interval: 30s
      timeout: 5s
      start_period: 40s
      retries: 3

networks:
  octafuse-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.30.0.0/16

volumes:
  octafuse_pg:
```

---

## 5. 写 .env

```bash
cat > /root/projects/octafuse/.env <<EOF
TZ=Asia/Shanghai
GATEWAY_PROXY_IMAGE=octafuse-proxy:local
GATEWAY_ADMIN_IMAGE=octafuse-admin:local
GATEWAY_MIGRATE_IMAGE=octafuse-migrate:local
ADMIN_USERNAME=$(grep ^ADMIN_USERNAME= /root/projects/octafuse/.secrets | cut -d= -f2)
ADMIN_PASSWORD=$(grep ^ADMIN_PASSWORD= /root/projects/octafuse/.secrets | cut -d= -f2)
MASTER_KEY=$(grep ^MASTER_KEY= /root/projects/octafuse/.secrets | cut -d= -f2)
POSTGRES_DB=$(grep ^POSTGRES_DB= /root/projects/octafuse/.secrets | cut -d= -f2)
POSTGRES_USER=$(grep ^POSTGRES_USER= /root/projects/octafuse/.secrets | cut -d= -f2)
POSTGRES_PASSWORD=$(grep ^POSTGRES_PASSWORD= /root/projects/octafuse/.secrets | cut -d= -f2)
EOF
chmod 600 /root/projects/octafuse/.env
```

---

## 6. 启动 + 迁移

```bash
cd /root/projects/octafuse

# 1. 起 PG（54 秒左右 healthy）
docker compose up -d octafuse-pg
sleep 15 && docker ps --format '{{.Names}}\t{{.Status}}' | grep octafuse-pg

# 2. 跑迁移（19 个 SQL；~30 秒）
docker compose --profile migrate run --rm octafuse-migrate

# 3. 起 Proxy + Admin
docker compose up -d octafuse-proxy octafuse-admin
sleep 30 && docker ps --format '{{.Names}}\t{{.Status}}' | grep -E "octafuse-(proxy|admin)"
```

---

## 7. 替换默认密码

```bash
cd /root/projects/octafuse
NEW_MK=$(grep ^MASTER_KEY= .secrets | cut -d= -f2)

# 1. 替换默认 MASTER_KEY（迁移 0002_seed.sql 写入 sk-dev…）
curl -s -X PUT -H "Authorization: Bearer sk-dev-***placeholder***" \
  -H "Content-Type: application/json" \
  -d "{\"key\":\"MASTER_KEY\",\"value\":\"$NEW_MK\"}" \
  http://127.0.0.1:8789/api/admin/config

# 2. 业务时区设到 Asia/Shanghai
curl -s -X PUT -H "Authorization: Bearer $NEW_MK" \
  -H "Content-Type: application/json" \
  -d '{"key":"BUSINESS_TIMEZONE","value":"Asia/Shanghai"}' \
  http://127.0.0.1:8789/api/admin/config

# 3. 验证
curl -s -H "Authorization: Bearer $NEW_MK" http://127.0.0.1:8789/api/admin/config | python3 -m json.tool
```

> ⚠️ **MASTER_KEY 默认值是 `sk-dev-…`**（迁移 0002_seed.sql 写入），不是用户在 .env 设的 hex。**必须 PUT 替换**，否则任何人都能用默认值调 `/api/admin/*`。
> ⚠️ **/api/admin/config 用 PUT 不是 POST**（POST 是 404）。

---

## 8. nginx 反代（两个独立子域名）

> ⚠️ **Next.js admin 用独立子域名**——它生成的 chunks 引用**绝对路径** `/_next/static/`，跟普通 API 网关放同一个 host 会导致 chunks 被错误路由到 proxy 容器。

文件 `/etc/nginx/sites-enabled/octafuse.conf`：

```nginx
# Octafuse Gateway（80 → 8787/8789）
# 子域名（避开 default_server）：
#   octafuse.<IP>.nip.io         → proxy  (OpenAI/Anthropic/Gemini)
#   admin-octafuse.<IP>.nip.io   → admin  (Next.js 后台)

server {
    listen 80;
    listen [::]:80;
    server_name octafuse.<你的IP>.nip.io;     # 例：octafuse.101.33.212.119.nip.io

    client_max_body_size 100M;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 600s;

    location / {
        proxy_pass http://127.0.0.1:8787;
    }
}

server {
    listen 80;
    listen [::]:80;
    server_name admin-octafuse.<你的IP>.nip.io;  # 例：admin-octafuse.101.33.212.119.nip.io

    client_max_body_size 100M;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 600s;

    location / {
        proxy_pass http://127.0.0.1:8789;
    }
}
```

```bash
# 测试 + reload
/usr/sbin/nginx -t
/usr/sbin/nginx -s reload
```

> ⚠️ **不要把 admin 反代到 `/admin/` 子路径**——HTML 引用的 `/_next/static/` 会被通用 `location /` 抢走送到 proxy 容器 → 404 卡 Loading 界面。

---

## 9. systemd 开机自启

文件 `/etc/systemd/system/octafuse-stack.service`：

```ini
[Unit]
Description=Octafuse Gateway stack (PG + proxy + admin) via docker compose
Requires=docker.service
After=docker.service network-online.target
Wants=network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/root/projects/octafuse
ExecStart=/usr/bin/docker compose --env-file /root/projects/octafuse/.env up -d
ExecStop=/usr/bin/docker compose --env-file /root/projects/octafuse/.env down
ExecReload=/usr/bin/docker compose --env-file /root/projects/octafuse/.env restart
TimeoutStartSec=300
TimeoutStopSec=60

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable octafuse-stack.service
```

---

## 10. 验证清单（部署完成必跑）

```bash
# 1. 容器全部运行
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep octafuse

# 2. 本地端口
curl -sI http://127.0.0.1:8787/ | head -1
curl -sI http://127.0.0.1:8789/ | head -1

# 3. 公网连通
curl -sI http://octafuse.<IP>.nip.io/         | head -1
curl -sI http://octafuse.<IP>.nip.io/v1/models | head -1
curl -sI http://admin-octafuse.<IP>.nip.io/    | head -1
curl -sI http://admin-octafuse.<IP>.nip.io/_next/static/chunks/<任意 chunk> | head -1

# 4. Admin API 鉴权
NEW_MK=$(grep ^MASTER_KEY= /root/projects/octafuse/.secrets | cut -d= -f2)
curl -s -H "Authorization: Bearer $NEW_MK" \
  http://admin-octafuse.<IP>.nip.io/api/admin/config | python3 -m json.tool
```

**期望输出**：所有 HTTP 都 200 / 401（v1/models 需 API key），admin API 返回 4 个 config 项。

---

## 11. 首次使用流程

1. 浏览器打开 `http://admin-octafuse.<IP>.nip.io/`
2. 用 `.secrets` 里的 `ADMIN_USERNAME` / `ADMIN_PASSWORD` 登录
3. **Providers** 页 → 选 OpenAI / Anthropic / Gemini → 填 API Key → 保存
4. **Models** 页 → 从内置目录导入模型（或新建）
5. **Routes** 页 → 把模型映射到 Provider
6. **Users** 页 → 创建业务用户 → **API Keys** → 创建 `sk-...` API Key
7. 用 API Key 调 `http://octafuse.<IP>.nip.io/v1/chat/completions`（OpenAI 协议）即可

---

## 12. 关键避坑（务必看）

| # | 坑 | 解决 |
|---|---|---|
| 1 | **GHCR 拉不动** | 别 `docker pull ghcr.io/octafuse/...`，直接 `git clone` 源码本地 build |
| 2 | **`docker build` 默认走 buildx** | 必须 `docker buildx build --load`，否则镜像不会写 daemon |
| 3 | **后台 build 被父进程 kill** | 用 `nohup setsid bash -c '...' </dev/null >/dev/null 2>&1 & disown` |
| 4 | **Alpine APK 源慢** | 每个 Dockerfile 加 `sed -i 's\|dl-cdn.alpinelinux.org\|mirrors.aliyun.com\|g' /etc/apk/repositories` |
| 5 | **admin login 路径** | 用 `POST /api/auth/login`，不是 `/api/admin/auth/login` |
| 6 | **默认 MASTER_KEY** | 必须用 `PUT /api/admin/config` 替换 `sk-dev-…` 为自己的 hex |
| 7 | **Next.js chunks 404** | admin 用独立子域名，不和 proxy 共享 host |
| 8 | **base64 凭据含 + / 字符** | 用 `openssl rand -base64 \| tr -d '+/'` 去掉 |
| 9 | **Dify 已占 :80** | 用子域名精确 server_name（不走 default_server） |

---

## 13. 升级 / 故障排查

### 升级到最新版
```bash
cd /root/projects/octafuse
# 备份数据库
docker exec octafuse-pg pg_dump -U octafuse octafuse > backup-$(date +%Y%m%d).sql

# 拉新版 + 重建
cd octafuse-gateway
git pull --ff-only
docker buildx build --load -f Dockerfile.proxy   -t octafuse-proxy:local   .
docker buildx build --load -f Dockerfile.admin   -t octafuse-admin:local   .
docker buildx build --load -f Dockerfile.migrate -t octafuse-migrate:local .
cd ..
docker compose --profile migrate run --rm octafuse-migrate
docker compose up -d
```

### 故障排查速查
| 症状 | 排查 |
|---|---|
| 容器起不来 | `docker logs octafuse-proxy` 看错误 |
| 数据库连不上 | `docker exec octafuse-pg pg_isready -U octafuse` |
| Admin 404 chunks | 检查 nginx `server_name` 是否独立子域名 |
| Master Key 失效 | 看 `.env` 跟 `/api/admin/config` 实际值是否一致 |
| Migration 失败 | `docker logs octafuse-pg` 看 SQL 错误，重跑 `docker compose --profile migrate run --rm octafuse-migrate` |

---

## 关联文档

- 官方文档：https://github.com/OctaFuse/octafuse-gateway/tree/main/docs
- 详本部署手册（含全部避坑分析）：`./README.md`
- 时间线报告：`./2026-08-07_部署全程.md`
- docker-compose.yaml：当前目录
- nginx 配置：`/etc/nginx/sites-enabled/octafuse.conf`
- systemd unit：`/etc/systemd/system/octafuse-stack.service`