---
title: Paperclip 部署手册 + 避坑指南
date: 2026-07-06
type: deployment-handbook
status: active
service: Paperclip
port: 3100
public_url: http://101.33.212.119:3100
deploy_path: /root/projects/paperclip
---

# 🟧 Paperclip 部署手册 + 避坑指南

> **一句话**：多 Agent 调度平台 + 任务编排。Next.js + Postgres + Better Auth。

---

## 1. 项目信息

| 项 | 值 |
|---|---|
| 用途 | Agent 任务调度 / 工作流编排 / 团队协作 |
| 技术栈 | Next.js + Postgres 16 + Redis + Better Auth |
| 公网 URL | `http://101.33.212.119:3100` |
| 状态 | ✅ 200 OK（10h+ 稳定运行）|
| 部署位置 | `/root/projects/paperclip/` |

---

## 2. 硬件依赖

| 项 | 最低 | 当前服务器 |
|---|---|---|
| CPU | 2 核 | 8 核 ✅ |
| RAM | 8 GB | 30 GB ✅ |
| Disk | 50 GB | 315 GB ✅ |
| 关键 | Postgres 16 + Redis | 已部署（宿主）|

---

## 3. 一键部署（从 0 到 1）

```bash
# 1. 拉代码
mkdir -p /root/projects && cd /root/projects
git clone https://github.com/HsiYan/paperclip.git
cd paperclip

# 2. 装依赖
pnpm install

# 3. 改 .env
cp .env.example .env
sed -i 's|^DATABASE_URL=.*|DATABASE_URL=postgresql://postgres:***@host.docker.internal:5432/paperclip|' .env
sed -i 's|^REDIS_URL=.*|REDIS_URL=redis://host.docker.internal:6379/0|' .env
sed -i 's|^BETTER_AUTH_SECRET=.*|BETTER_AUTH_SECRET=paperclip-dev-secret|' .env  # ⚠️ 生产前必换真随机
sed -i 's|^NEXT_PUBLIC_APP_URL=.*|NEXT_PUBLIC_APP_URL=http://101.33.212.119:3100|' .env
sed -i 's|^PORT=.*|PORT=3100|' .env

# 4. 跑 migration
psql -h host.docker.internal -U postgres -d paperclip -f migrations/init.sql
# 或用 ORM 自带命令
pnpm db:migrate

# 5. 启
pnpm build
nohup pnpm start --port 3100 > /tmp/paperclip.log 2>&1 &
```

---

## 4. 配置（.env 关键项）

```bash
# === Database ===
DATABASE_URL=postgresql://postgres:***@host.docker.internal:5432/paperclip

# === Redis ===
REDIS_URL=redis://host.docker.internal:6379/0

# === Auth（关键：默认 secret 低熵，生产前必换真随机）===
BETTER_AUTH_SECRET=paperclip-dev-secret
# ⚠️ 真实生产：
# BETTER_AUTH_SECRET=*** rand -hex 32>

# === URLs ===
NEXT_PUBLIC_APP_URL=http://101.33.212.119:3100
PORT=3100

# === Better Auth ===
BETTER_AUTH_URL=http://101.33.212.119:3100
```

---

## 5. 启动命令（systemd 永久 service）

⚠️ **不要用 `nohup pnpm &`**！SSH session 注销时 systemd 会 kill 子进程（2026-07-06 教训）。

**正确方式**：用 systemd user service 管理。

```bash
# 1. 写 service file
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/paperclip.service << 'EOF'
[Unit]
Description=Paperclip Express dev server
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/projects/paperclip
Environment="NVM_DIR=/root/.nvm"
ExecStart=/bin/bash -c 'export NVM_DIR=/root/.nvm && . $NVM_DIR/nvm.sh && cd /root/projects/paperclip && exec pnpm dev:once'
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

# 2. enable + start
systemctl --user daemon-reload
systemctl --user enable paperclip.service
systemctl --user start paperclip.service

# 3. 验证
systemctl --user status paperclip.service
ss -tlnp | grep 3100
curl -sI http://localhost:3100
curl -s http://localhost:3100/api/health
```

**临时启动**（dev 用，不推荐）：
```bash
cd /root/projects/paperclip
nohup pnpm dev:once > /tmp/paperclip.log 2>&1 &
```

**看日志**：
```bash
journalctl --user -u paperclip.service -f
```

---

## 6. 三维度验证

```bash
# 本地
curl -sI http://localhost:3100
# 公网
curl -sI http://101.33.212.119:3100
# Auth endpoint
curl -s http://localhost:3100/api/auth/get-session
# 期望：401（未登录）或 200（已登录）
```

---

## 7. ⚠️ 避坑指南（按时间倒序）

### 坑 6: SSH session 注销杀进程（2026-07-06 实测）
- **现象**: Paperclip 进程在 7-6 01:56 之后无了，查 ss 看不到 3100 端口
- **根因**: 之前用 `nohup pnpm dev:once &` 启，root 在 `pts/4` 注销时 systemd 把 cgroup 里所有进程 kill
- **修法**: 用 `systemd-run --user` 或写 `~/.config/systemd/user/paperclip.service`（Type=simple, Restart=always）
- **永久规则**: ✅ **任何用户态服务必须用 systemd 管生命周期**，不要 `nohup &`

### 坑 1: BETTER_AUTH_SECRET 是默认值（低熵）
- **现象**: 容器启动 warn log "BETTER_AUTH_SECRET is using default low-entropy value"
- **根因**: `.env.example` 里 secret 是 `paperclip-dev-secret` 占位符
- **修法**: dev 阶段保留；生产前用 `openssl rand -hex 32` 替换
- **永久规则**: ✅ **生产 secret 必用 `openssl rand -hex 32` 真随机**

### 坑 2: pg_hba 没加 docker 网段
- **现象**: 报 `no pg_hba.conf entry for host "172.18.0.x", user "postgres", database "paperclip"`
- **根因**: postgres 默认只 trust localhost
- **修法**: `/etc/postgresql/16/main/pg_hba.conf` 加：
```
host all all 172.16.0.0/12 trust
host all all 10.0.0.0/8 trust
```
- **永久规则**: ✅ **Postgres 16 默认只 trust loopback，docker 容器连需手动加网段**

### 坑 3: postgres 监听 localhost only
- **现象**: docker 容器连 PG 报 `Connection refused`
- **根因**: `postgresql.conf` `listen_addresses='localhost'`
- **修法**: 改 `listen_addresses='*'`
- **永久规则**: ✅ **多服务共享 PG 必改 listen_addresses='*'**

### 坑 4: redis protected-mode 拒绝外部连接
- **现象**: 报 `DENIED Redis is running in protected mode`
- **根因**: `/etc/redis/redis.conf` `protected-mode yes`
- **修法**: dev 改 `protected-mode no`；生产必须加密码+ACL
- **永久规则**: ⚠️ dev 阶段 protected-mode 关闭；生产用密码+ACL

### 坑 5: db migration 没跑就启动
- **现象**: 启动报 `relation "users" does not exist`
- **根因**: 跳过 `pnpm db:migrate`
- **修法**: 启动前必跑 migration
- **永久规则**: ✅ **启动前必跑 db:migrate**（不是 first run 才跑）

---

## 8. 当前状态（2026-07-06 20:08）

| 服务 | 状态 |
|---|---|
| Next.js server | ✅ http://101.33.212.119:3100 |
| Postgres 数据库 | ✅ paperclip db 已迁移 |
| Redis | ✅ 复用宿主机 |

**已知遗留**：BETTER_AUTH_SECRET 是默认 dev 值，生产前必换。

---

## 9. 关联文档

- `/root/vault/current-server/2026-07-05_md_paperclip-公网部署完整指南.md`
- `/root/vault/current-server/2026-07-05_md_paperclip-测试访问信息.md`
- `/root/vault/current-server/2026-07-05_md_反思-记忆污染.md`