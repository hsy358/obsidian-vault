---
title: Paperclip 公网部署完整指南（精确版）
date: 2026-07-05
type: deployment-guide
status: corrected
project: 德勤 AI Native Workspace
server: VM-0-13-ubuntu（8C30G + 315G 磁盘）
author: 小助（OpenClaw）
repo: paperclipai/paperclip
---

# 📋 Paperclip 公网部署完整指南（**精确版**）

> **背景**：把 paperclip AI agent 平台从本地部署开放成公网可访问的部署。  
> **服务器**：腾讯云 Ubuntu 24.04.4 LTS / **8 核 30 GiB / 315 GB 磁盘** / 公网 IP `101.33.212.119`  
> **部署时间**：2026-07-05 01:55 起，11:48 上线公网 UI  
> **当前状态**：✅ 公网 UI 跑通 + bootstrap admin 已注册 + onboarding 完成

---

## 🎯 一、部署目标

```
本地开发 / 单元测试
    ↓
server-only 模式（无 UI）
    ↓
公网 + UI + 认证模式（authenticated）
    ↓
多用户测试 / onboarding
```

---

## 📐 二、架构图

```
浏览器（任何地方）
    ↓ HTTP
腾讯云 NAT（IP 101.33.212.119:3100）
    ↓
Linux 主机（VM-0-13-ubuntu）监听 0.0.0.0:3100
    ↓
tsx src/index.ts（PID 229093，**dev 模式**）
    ↓
Better Auth（cookie + session）
    ↓
Drizzle ORM → PostgreSQL 16（systemd 服务）
    ↓ schema: public
业务表（user, companies, agents, invites, sessions...）
```

---

## 🛠 三、完整部署步骤（8 步）

### Step 1：环境依赖

| 依赖 | 版本 | 验证命令 |
|---|---|---|
| OS | Ubuntu 24.04.4 LTS | `cat /etc/os-release` |
| CPU | 8 核 | `nproc` |
| 内存 | 30 GiB | `free -h` |
| 磁盘 | 315 GB | `df -h /` |
| Node.js | v22.23.1 | `node -v` |
| pnpm | 9.15.4 | `pnpm -v` |
| PostgreSQL | 16（systemd）| `systemctl status postgresql` |

### Step 2：装 PostgreSQL（**systemd 模式，不可用 Docker**）

```bash
apt install -y postgresql postgresql-contrib
systemctl enable postgresql
systemctl start postgresql

# 创建 paperclip DB + 用户
sudo -u postgres psql -c "CREATE USER paperclip WITH PASSWORD 'paperclip';"
sudo -u postgres psql -c "CREATE DATABASE paperclip OWNER paperclip;"
```

**注**：本机还有另一个 PostgreSQL DB（AgentSpace 用，密码 `agent_space`，**别混淆**）。

### Step 3：克隆 paperclip

```bash
cd /root/projects
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pnpm install
```

### Step 4：跑 onboard

```bash
pnpm --filter @paperclipai/cli exec paperclipai onboard
```

交互提示回答：
- Database mode：`postgres`（**不选 embedded-postgres**）
- Connection string：`postgres://paperclip:***@localhost:5432/paperclip`
- Server bind：**`lan`**（不是 loopback / tailnet）
- Deployment mode：**`authenticated`**
- Exposure：`private`（先 default，onboard 完后改 .env）
- Serve UI：`yes`
- Auth base URL mode：default（onboard 完后改 .env）

onboard 完成会自动生成 1 个 `bootstrap_ceo` invite（3 天有效）。

### Step 5：手动改 .env（**双源必须同步**）

⚠️ **踩坑**：paperclip 同时加载两份 .env，必须保持一致：
- `/root/.paperclip/instances/default/.env`（用户级）
- `/root/projects/paperclip/.env`（项目级，**优先级高**）

完整 .env：
```bash
DATABASE_URL=postgres://paperclip:paperclip@localhost:5432/paperclip
PORT=3100
SERVE_UI=true
PAPERCLIP_DEPLOYMENT_MODE=authenticated
BIND=lan                                # ← 关键
HOST=127.0.0.1
EXPOSURE=public                         # ← 关键
PAPERCLIP_AUTH_BASE_URL_MODE=explicit
PAPERCLIP_AUTH_PUBLIC_BASE_URL=http://101.33.212.119:3100
BETTER_AUTH_SECRET=<openssl rand -base64 32>
PAPERCLIP_AGENT_JWT_SECRET=<自动生成>
PAPERCLIP_ALLOWED_HOSTNAMES=["101.33.212.119", "localhost", "127.0.0.1"]
```

### Step 6：腾讯云安全组放通 3100

腾讯云控制台 → 安全组 → 入站规则 → 添加 TCP:3100 来源 0.0.0.0/0。

**不开公网连不上。**

### Step 7：起服务（**dev 模式**，tsx）

```bash
cd /root/projects/paperclip
nohup pnpm --filter @paperclipai/server exec tsx src/index.ts \
  > /tmp/paperclip.log 2>&1 &

# 看日志
tail -f /tmp/paperclip.log
```

进程名：`tsx src/index.ts`，监听 `0.0.0.0:3100`，**非生产模式**。

**生产模式**（建议改但未启用）：
```bash
pnpm build
pnpm --filter @paperclipai/server start
```

**守护进程**（建议改但未启用）：
- 当前用 nohup，session 退出可能被 SIGHUP
- 建议加 systemd unit 或 pm2 守护

### Step 8：验证 + onboarding

```bash
# 本机
curl -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3100/

# 公网
curl -o /dev/null -w "%{http_code}\n" http://101.33.212.119:3100/

# 期望：200
```

浏览器打开 `http://101.33.212.119:3100/`，用 bootstrap invite 注册管理员 → 走完 4 步 onboarding。

---

## 🐛 四、踩坑全清单（11 个）

### 坑 1：服务器配置记忆错误
**症状**：文档里写 2C3.6G，实际是 8C30G  
**原因**：从老服务器 101.35.52.96 拷贝过来的记忆  
**教训**：**每次部署文档必须现查硬件配置**（`nproc` + `free -h`），不能凭印象

### 坑 2：`bind: loopback` 让公网连不上
**症状**：`curl http://101.33.212.119:3100/` → connection refused  
**原因**：onboard 默认 bind=loopback，只听 127.0.0.1:3100  
**解决**：`BIND=lan` + `HOST=127.0.0.1`  
**教训**：onboard 完成后必须检查 `bind` 字段

### 坑 3：`local_trusted` 模式锁 bind 为 loopback
**症状**：改了 `BIND=lan` 但仍然只听 loopback  
**原因**：`local_trusted` 强制 bind=loopback  
**解决**：`PAPERCLIP_DEPLOYMENT_MODE=authenticated` + `BIND=lan`  
**教训**：部署模式必须先于 bind 设置

### 坑 4：`serveUi: false` 不返回 UI
**症状**：首页返回 404 / 纯 JSON  
**原因**：UI 静态文件没被 serve  
**解决**：`SERVE_UI=true`  
**教训**：生产模式默认是 true，但 onboard 偶尔会重置

### 坑 5：缺 `auth.publicBaseUrl` 导致回调 URL 错乱
**症状**：登录成功但 cookie 域名错乱  
**原因**：默认 baseUrlMode=auto，没设公网 URL  
**解决**：
```
PAPERCLIP_AUTH_BASE_URL_MODE=explicit
PAPERCLIP_AUTH_PUBLIC_BASE_URL=http://101.33.212.119:3100
```  
**教训**：测试登录必须用公网 IP

### 坑 6：`exposure: "public"` 需要 `baseUrlMode=explicit`
**症状**：设了 `EXPOSURE=public` 但其他用户访问还是被限制  
**原因**：schema 验证：public 必须配 explicit base URL  
**解决**：见坑 5

### 坑 7：schema 验证失败被静默吞掉
**症状**：config.json 字段设错，服务读到默认值  
**原因**：`readConfigFile()` 用 try-catch，schema 错就 fallback 默认  
**解决**：检查 `$meta` 字段 + 看服务日志  
**教训**：silent-failure 是 paperclip 配置的最大隐患

### 坑 8：双 .env 不一致
**症状**：改了一份 .env 但生效的是另一份  
**原因**：项目级 .env 优先级高，用户级可能被覆盖  
**解决**：`diff` 两份，强制同步  
**教训**：改配置前先 `diff /root/.paperclip/instances/default/.env /root/projects/paperclip/.env`

### 坑 9：vite/next 跨源拦截
**症状**：从公网 IP 访问，前端调 API 报 CORS  
**原因**：Next.js dev server 默认只允许 localhost  
**解决**：`next.config.mjs` 加 `allowedDevOrigins: ['101.33.212.119', 'localhost']`  
**教训**：所有 dev server 都有 origin 白名单

### 坑 10：bootstrap invite 是 CEO 类型
**症状**：把 bootstrap URL 转给测试者，但接受了后只给 owner 权限  
**原因**：`bootstrap_ceo` 类型只给 owner  
**解决**：手动创建 `company_join` 类型 invite（30 天有效）  
**教训**：测试用 invite 必须用普通 `company_join`

### 坑 11：HTTP 非 HTTPS 显示 "不安全"
**症状**：浏览器顶部 "不安全" 警告  
**原因**：默认 HTTP  
**解决**（未做）：nginx + Let's Encrypt  
**教训**：测试用 HTTP OK，生产必须 HTTPS

---

## 🔧 五、配置错误排查 SOP（7 步）

```bash
# 1. 硬件
nproc; free -h; df -h /

# 2. 进程
ps -ef | grep "tsx src/index.ts" | grep -v grep

# 3. 端口
ss -tlnp | grep :3100

# 4. config.json
cat /root/.paperclip/instances/default/config.json | python3 -m json.tool

# 5. .env（两份必须 diff）
diff /root/.paperclip/instances/default/.env /root/projects/paperclip/.env

# 6. 日志
tail -50 /tmp/paperclip.log

# 7. DB
PGPASSWORD=*** psql -h localhost -U paperclip -d paperclip -c "\dt"
```

---

## 📊 六、当前状态（2026-07-05 14:28）

| 组件 | 状态 |
|---|---|
| 硬件 | ✅ 8C30G + 315G |
| PostgreSQL 16（systemd）| ✅ 运行中 |
| tsx dev server | ✅ PID 229093，0.0.0.0:3100 |
| 启动方式 | ⚠️ nohup（非 daemon，session 退出可能被 kill）|
| Public UI | ✅ HTTP 200 |
| bootstrap CEO | ✅ hesiyan2008@126.com |
| onboarding | ✅ Company `Deloitte` |
| Agents | ⚠️ 1 个 `AI Native`（status=error，待修）|
| 测试 invite | ✅ 已生成 30 天 `company_join` invite |

---

## ⚠️ 七、未解决的 5 个安全风险

| 风险 | 严重度 | 修复 |
|---|---|---|
| HTTP 明文传输 | 🔴 P0 | nginx + Let's Encrypt |
| `BETTER_AUTH_SECRET` 低熵（`paperclip-dev-secret`）| 🔴 P0 | `openssl rand -base64 32` |
| DB password 明文 `paperclip` | 🟡 P1 | 改密码 + vault 存 secret |
| Invite URL 聊天明文传 | 🟡 P1 | 短期发短链 |
| 进程靠 nohup（非 daemon）| 🟢 P2 | 加 systemd unit 或 pm2 |

---

## 🎯 八、生产化清单（待办）

- [ ] nginx + Let's Encrypt（HTTPS）
- [ ] 高熵 `BETTER_AUTH_SECRET`
- [ ] DB password 改强 + 存 vault
- [ ] 加 systemd unit（开机自启 + 守护）
- [ ] 跑生产模式（`pnpm build && pnpm start`）
- [ ] 加监控 + 告警
- [ ] DB 备份策略（dump / cron）

---

## 🔄 v1 错误修正记录

| 错项 | 修正 |
|---|---|
| ❌ "2C3.6G" | ✅ **8C30G + 315G** |
| ❌ "PostgreSQL docker" | ✅ **systemd 服务** |
| ❌ ".env 双源一致" | ✅ **实际两份不一致**，要 diff 同步 |
| ❌ "启动方式未说" | ✅ **tsx dev 模式 + nohup** |
| ❌ "未说主机名" | ✅ **VM-0-13-ubuntu** |

---

**作者**：小助 — OpenClaw (MiniMax-M3) — 2026-07-05 14:30  
**v1 → v2 修正**：何大人 13:08 指出硬件错 + 部署步骤错，立即核查重写