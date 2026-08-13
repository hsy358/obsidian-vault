# Octafuse Gateway 部署手册

> **项目**：Octafuse Gateway（自托管 AI 网关 / Agent 工具平台）
> **版本**：v2.1.2（本地 build，源码 `git clone --depth=1 https://github.com/OctaFuse/octafuse-gateway.git`）
> **首次部署**：2026-08-07 15:58
> **关联时间线**：`/root/vault/current-server/2026-08-07_部署Octafuse全程.md`（待补）

## 一、用途 / 镜像 / 端口 / 公网 URL

| 项 | 值 |
|---|---|
| 项目类型 | AI 网关（OpenAI / Anthropic / Google Gemini 三协议 + Agent 工具） |
| 项目地址 | https://github.com/OctaFuse/octafuse-gateway |
| 公网 URL（Proxy） | `http://octafuse.101.33.212.119.nip.io/` |
| 公网 URL（Admin） | `http://admin-octafuse.101.33.212.119.nip.io/` |
| Proxy BaseURL | `http://octafuse.101.33.212.119.nip.io/v1`（OpenAI 协议） |
| Admin BaseURL | `http://admin-octafuse.101.33.212.119.nip.io/`（Next.js 控制台）|
| 镜像来源 | **本地 build**（GHCR 拉不下来：185.199.110.154 单 layer 49MB 卡 4 分钟+；改 git clone 源码本地 build，~100s/镜像） |
| 镜像 tag | `octafuse-proxy:local` / `octafuse-admin:local` / `octafuse-migrate:local` |
| 容器名 | `octafuse-pg` / `octafuse-proxy` / `octafuse-admin` |
| 网络 | `octafuse-net`（172.30.0.0/16，自定义独立段，已用段全避） |
| 端口 | 5436（PG, 127.0.0.1）/ 8787（Proxy, 0.0.0.0）/ 8789（Admin, 0.0.0.0） |

## 二、硬件依赖

| 维度 | 最低 | 当前服务器 | 占用 |
|---|---|---|---|
| 内存 | 1 GB | 30 GB | ~700 MB（3 容器总和） |
| 磁盘 | 2 GB | 315 GB | ~1.5 GB（镜像 + 库） |
| CPU | 1 核 | 8 核 | < 5% 空闲时 |

## 三、一键部署（从 0 到 1，按顺序复制可跑）

### Step 1：克隆源码（45 秒，避开 GHCR 拉镜像慢的坑）
```bash
mkdir -p /root/projects/octafuse && cd /root/projects/octafuse
git clone --depth=1 https://github.com/OctaFuse/octafuse-gateway.git
cd octafuse-gateway
```

### Step 2：改 3 个 Dockerfile 走阿里云 APK 镜像（避开 dl-cdn.alpinelinux.org 慢）
每个 `Dockerfile.{proxy,admin,migrate}` 在每个 `FROM` 后插入：
```bash
for f in Dockerfile.proxy Dockerfile.admin Dockerfile.migrate; do
  cp "$f" "$f.bak"
  python3 -c "
import re
with open('$f') as fh: content = fh.read()
new_content = re.sub(r'FROM\s+\S+\s+AS\s+\w+', lambda m: m.group(0) + '\n\nRUN sed -i \\'s|dl-cdn.alpinelinux.org|mirrors.aliyun.com|g\\' /etc/apk/repositories 2>/dev/null || true', content)
with open('$f', 'w') as fh: fh.write(new_content)
"
done
```

### Step 3：配 npm 镜像 + build 3 镜像（~3 分钟/镜像，并发后 ~4 分钟总）
```bash
npm config set registry https://registry.npmmirror.com

# proxy（必须用 buildx --load，新版 docker 默认走 buildx 不自动 load 到 daemon）
nohup setsid bash -c 'docker buildx build --load -f Dockerfile.proxy -t octafuse-proxy:local . >/tmp/build-proxy.log 2>&1' </dev/null >/dev/null 2>&1 & disown

# admin 和 migrate 并发
nohup setsid bash -c 'docker buildx build --load -f Dockerfile.admin -t octafuse-admin:local . >/tmp/build-admin.log 2>&1' </dev/null >/dev/null 2>&1 & disown
nohup setsid bash -c 'docker buildx build --load -f Dockerfile.migrate -t octafuse-migrate:local . >/tmp/build-migrate.log 2>&1' </dev/null >/dev/null 2>&1 & disown
```

### Step 4：建 `docker-compose.yaml` + `.env`
见同目录 `docker-compose.yaml` + `.env`（本仓库已含）。要点：
- 用 `octafuse-pg` 独立容器（5436↔5432）
- `octafuse-proxy` / `octafuse-admin` 用 `restart: unless-stopped` + AUTO_MIGRATE=1
- `network_mode: 172.30.0.0/16` 避开所有已用网段

### Step 5：起容器（4 步）
```bash
cd /root/projects/octafuse
docker compose up -d octafuse-pg                  # 1. 起 PG
sleep 15                                          # 等 healthy
docker compose --profile migrate run --rm octafuse-migrate  # 2. 跑迁移（19 个 SQL 全部应用）
docker compose up -d octafuse-proxy octafuse-admin  # 3. 起 Proxy + Admin
sleep 30                                          # 等 Next.js 启动
```

### Step 6：改默认 MASTER_KEY + 业务时区
默认 `MASTER_KEY=sk-dev-admin-key`（迁移 0002_seed.sql 写入），必须替换：
```bash
NEW_MK=$(openssl rand -hex 16)  # 32 位 hex
curl -s -X PUT -H "Authorization: Bearer sk-dev-admin-key" \
  -H "Content-Type: application/json" \
  -d "{\"key\":\"MASTER_KEY\",\"value\":\"$NEW_MK\"}" \
  http://127.0.0.1:8789/api/admin/config

# 同时把时区设到上海
curl -s -X PUT -H "Authorization: Bearer $NEW_MK" \
  -H "Content-Type: application/json" \
  -d '{"key":"BUSINESS_TIMEZONE","value":"Asia/Shanghai"}' \
  http://127.0.0.1:8789/api/admin/config
```

### Step 7：nginx 反代（80 + 两个独立子域名）
见 `/etc/nginx/sites-enabled/octafuse.conf`。要点：
- **不抢 default_server**（保持 Dify 默认行为）
- **Proxy**: `listen 80; server_name octafuse.101.33.212.119.nip.io;` → `/` → 127.0.0.1:8787
- **Admin**: `listen 80; server_name admin-octafuse.101.33.212.119.nip.io;` → `/` → 127.0.0.1:8789
- 两 server block 用精确 server_name 匹配，不会被 default server (`_`) 抢占

### Step 8：systemd 开机自启
见 `/etc/systemd/system/octafuse-stack.service`。已 enable，开机会自动 `docker compose up -d`。

## 四、关键配置

### `.env`（脱敏，ADMIN_PASSWORD/POSTGRES_PASSWORD/MASTER_KEY 在 `/root/projects/octafuse/.secrets`）
```env
TZ=Asia/Shanghai
OCTAFUSE_NETWORK_SUBNET=172.30.0.0/16
POSTGRES_HOST_PORT=5436
PROXY_HOST_PORT=8787
ADMIN_HOST_PORT=8789
GATEWAY_PROXY_IMAGE=octafuse-proxy:local
GATEWAY_ADMIN_IMAGE=octafuse-admin:local
GATEWAY_MIGRATE_IMAGE=octafuse-migrate:local
DB_TIMEZONE=UTC
ADMIN_USERNAME=admin
ADMIN_PASSWORD=***       # 20 位 base64；首次部署用 openssl rand 生成
MASTER_KEY=***           # 32 位 hex；Step 6 替换默认 sk-dev-admin-key
POSTGRES_DB=octafuse
POSTGRES_USER=octafuse
POSTGRES_PASSWORD=***    # 24 位 base64
```

### 登录信息（何大人访问用）
```
Admin:  http://admin-octafuse.101.33.212.119.nip.io/
        Username: admin
        Password: 20 位强密码（见 /root/projects/octafuse/.secrets）

API:    http://octafuse.101.33.212.119.nip.io/v1
        Authorization: Bearer <ADMIN_PASSWORD>  ← 首次用 ADMIN_PASSWORD 登录 Admin 后，
                                                  在 Users/Keys 页面创建 Gateway API Key 用
```

> **为什么 Admin 用独立子域名？**
> Octafuse admin Next.js 生成的 chunks 引用**绝对路径** `/_next/static/chunks/xxx`
> （next.config 没设 basePath）。如果把 admin 反代在 `/admin/` 子路径下，HTML 引用的
> `/_next/static/` 会被 nginx 的通用 `location /` 路由到 proxy 容器（8787）→ 404
> 卡 Loading 界面。官方文档也推荐独立子域名。

## 五、当前状态

```
$ docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep octafuse
octafuse-admin    Up X minutes (healthy)   0.0.0.0:8789->8789/tcp
octafuse-proxy    Up X minutes (healthy)   0.0.0.0:8787->8787/tcp
octafuse-pg       Up X minutes (healthy)   127.0.0.1:5436->5432/tcp

$ docker images | grep octafuse
octafuse-admin:local    328MB / 81.1MB
octafuse-migrate:local  327MB / 74.1MB
octafuse-proxy:local    287MB / 65.2MB
```

## 六、避坑指南（按时间倒序）

### ⚠️ 坑 1：GHCR 拉不动（最大坑，4 小时）
- **现象**：`docker pull ghcr.io/octafuse/octafuse-gateway-proxy:v2.1.2` 卡 2 小时没结果；layer "Already exists" 但 `docker images` 看不到镜像
- **根因**：GHCR 走 GitHub Pages CDN（IP 185.199.110.154），单 layer 49MB 速度 33B/s，docker pull 在 manifest 写入阶段 timeout
- **解法**：放弃 GHCR 预构建镜像，改 `git clone` 源码 + 本地 build（~100s/镜像）
- **永久规则**：
  - ✅ GHCR 拉镜像 = 优先 `git clone` 源码本地 build
  - ✅ `docker build` 改用 `docker buildx build --load`（29.x 默认走 buildx，不自动 load）
  - ❌ 不要再尝试 `docker pull` GHCR 拉 octafuse 镜像

### ⚠️ 坑 2：docker build 跟随父进程被 SIGKILL
- **现象**：后台 build 跑了 37 分钟后父 exec 被 abort，build 进程一起被 kill
- **根因**：`nohup &` + `disown` 仍受父 session 关联
- **解法**：`nohup setsid bash -c '...' </dev/null >/dev/null 2>&1 & disown`（parent PID 变 init）
- **永久规则**：
  - ✅ 后台跑长任务用 `setsid` 双重脱离
  - ✅ 不要 poll（OpenClaw exec 长跑会被 SIGKILL）
  - ✅ 用 nohup setsid 后，输出去 /tmp 文件，事后查 log

### ⚠️ 坑 3：apk 镜像慢（dl-cdn.alpinelinux.org 首次 0.5s+）
- **现象**：`apk add ca-certificates` 在 `apk upgrade` 阶段 fetch APKINDEX.tar.gz 卡 2 分钟+
- **根因**：alpine 默认源 dl-cdn 在国内较慢
- **解法**：在每个 Dockerfile 的每个 `FROM` 后插入 `RUN sed -i 's|dl-cdn.alpinelinux.org|mirrors.aliyun.com|g' /etc/apk/repositories`
- **永久规则**：
  - ✅ Alpine base 镜像的 Dockerfile 都加阿里云源 sed

### ⚠️ 坑 4：admin login 路径用错
- **现象**：`POST /api/admin/auth/login {"username":"admin","password":"..."}` → 401
- **真因**：正确路径是 `/api/auth/login`（不在 /api/admin/ 下）
- **解法**：`POST /api/auth/login {username, password}` → 200 + cookie
- **永久规则**：
  - ✅ Admin 用户登录 → `POST /api/auth/login`
  - ✅ Admin API 调用 → `Authorization: Bearer <MASTER_KEY>`
  - ❌ 不要用 `/api/admin/auth/login`（404）

### ⚠️ 坑 5：MASTER_KEY 默认值
- **现象**：迁移 0002_seed.sql 写入 `MASTER_KEY=sk-dev-admin-key`（admin API 鉴权 Bearer）
- **风险**：任何知道默认值的人都能调 `/api/admin/*`
- **解法**：Step 6 用 `curl -X PUT /api/admin/config` 换成自己的 32 位 hex
- **永久规则**：
  - ✅ 任何 dev 镜像/迁移默认值都要查 system_config 并替换
  - ✅ MASTER_KEY 用 `openssl rand -hex 16`（32 hex 字符）

## 七、升级 / 迁移路径

### 升级到 v2.2.0（最新版，Gemini 路由整合）
v2.2.0 引入破坏性变更（路由策略 canonical 化 + Gemini Pool 整合），需：
1. 备份数据库：`docker exec octafuse-pg pg_dump -U octafuse octafuse > /root/projects/octafuse/backup-v2.1.2-$(date +%Y%m%d).sql`
2. 停 Proxy：`docker stop octafuse-proxy`
3. 跑 0017-0019 迁移（已包含在 v2.1.2 升级到 v2.2.0 的迁移链里）
4. 部署 v2.2.0 proxy + admin

### 重建镜像（更新代码后）
```bash
cd /root/projects/octafuse/octafuse-gateway
git pull --ff-only
for f in Dockerfile.proxy Dockerfile.admin Dockerfile.migrate; do
  cp "$f" "$f.bak"  # 保留原版
  cp "$f.bak" "$f"  # 还原（去掉 .bak 的 sed 改动，重新加）
done
# 重做 Step 2 的 sed 改动
# 重做 Step 3 的 build（每次 build 后镜像大小有变化）
```

## 八、关联文档

- 官方文档：https://github.com/OctaFuse/octafuse-gateway/tree/main/docs
- 部署手册（官方）：https://github.com/OctaFuse/octafuse-gateway/blob/main/docs/operators/deployment/docker.md
- 路由策略：https://github.com/OctaFuse/octafuse-gateway/blob/main/docs/users/configuration.md
- 时间线报告：待补 `2026-08-07_部署Octafuse全程.md`
