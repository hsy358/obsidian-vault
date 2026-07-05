---
title: Paperclip 公网部署完整指南（踩坑 + 解决办法）
date: 2026-07-05
type: deployment-guide
status: active
project: 德勤 AI Native Workspace
server: 新服务器（101.33.212.119）
author: 小助（OpenClaw）
repo: paperclipai/paperclip（v0.14）
---

# 📋 Paperclip 公网部署完整指南

> **背景**：把 paperclip AI agent 平台从本地部署开放成公网可访问的部署。  
> **服务器**：腾讯云 Ubuntu 24.04 / 2C3.6G / IP `101.33.212.119`  
> **部署时间**：2026-07-05（凌晨 2:00 起，11:48 上线公网 UI）  
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
Linux 主机监听 0.0.0.0:3100
    ↓
tsx src/index.ts（PID 229093, dev 模式）
    ↓
Better Auth（cookie + session）
    ↓
Drizzle ORM → PostgreSQL 12+
    ↓ schema: public
业务表（user, companies, agents, invites, sessions...）
```

---

## 🛠 三、完整部署步骤（8 步）

### Step 1：克隆 + 装依赖
```bash
cd /root/projects
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pnpm install
```

### Step 2：装 PostgreSQL（systemd 模式，**不要用 Docker**）

```bash
# Ubuntu 24.04
apt install -y postgresql postgresql-contrib

# 起服务
systemctl enable postgresql
systemctl start postgresql

# 创建 paperclip 数据库 + 用户
sudo -u postgres psql -c "CREATE USER paperclip WITH PASSWORD 'paperclip';"
sudo -u postgres psql -c "CREATE DATABASE paperclip OWNER paperclip;"
```

**注意**：password 用 `paperclip`（默认密码），生产前必须改。

### Step 3：跑 onboard

```bash
pnpm --filter @paperclipai/cli exec paperclipai onboard
```

交互提示回答（关键决策）：
- Database mode：`postgres`（不选 embedded-postgres，原因是 systemd PG 更稳）
- Connection string：`postgres://paperclip:paperclip@localhost:5432/paperclip`
- Server bind：**`lan`**（不是 loopback / tailnet）
- Deployment mode：**`authenticated`**（不是 local_trusted）
- Exposure：**`public`**
- Serve UI：**`yes`**
- Auth base URL mode：**`explicit`**
- Auth public base URL：**`http://101.33.212.119:3100`**
- Agent JWT secret：自动生成（保存到 .env）

onboard 完成后自动生成 1 个 `bootstrap_ceo` invite（3 天有效）。

### Step 4：手动补 config（**踩坑 1**）

`onboard` 默认会把 `exposure` 设成 `private` / `bind` 设成 `loopback`——必须手动改。

```bash
# /root/.paperclip/instances/default/.env
DATABASE_URL=postgres://paperclip:***@localhost:5432/paperclip
PORT=3100
SERVE_UI=true
PAPERCLIP_DEPLOYMENT_MODE=authenticated
BIND=lan                                    # ← 关键：lan 而不是 loopback
HOST=127.0.0.1
EXPOSURE=public                             # ← 关键：public 而不是 private
PAPERCLIP_AUTH_BASE_URL_MODE=explicit
PAPERCLIP_AUTH_PUBLIC_BASE_URL=http://101.33.212.119:3100
BETTER_AUTH_SECRET=<openssl rand -base64 32>
PAPERCLIP_AGENT_JWT_SECRET=<自动生成>
PAPERCLIP_ALLOWED_HOSTNAMES=["101.33.212.119", "localhost", "127.0.0.1"]
```

**两份 .env 必须一致**（双源覆盖机制）：
- `/root/.paperclip/instances/default/.env`（用户级）
- `/root/projects/paperclip/.env`（项目级，优先级更高）

### Step 5：腾讯云安全组放通 3100

⚠️ **腾讯云控制台** → 安全组 → 入站规则 → 添加：
- 协议：TCP
- 端口：3100
- 来源：`0.0.0.0/0`（测试用）或限制特定 IP

不开放的话，公网连不上。

### Step 6：起服务（dev 模式）

```bash
cd /root/projects/paperclip
nohup pnpm --filter @paperclipai/server exec tsx src/index.ts \
  > /tmp/paperclip.log 2>&1 &

# 看日志
tail -f /tmp/paperclip.log
```

进程：`tsx src/index.ts`，监听 `0.0.0.0:3100`。

**生产模式**（未启用，但建议）：
```bash
pnpm build
pnpm --filter @paperclipai/server start
```

### Step 7：验证公网

```bash
# 本机
curl -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3100/

# 公网（必须从外网或 curl 测）
curl -o /dev/null -w "%{http_code}\n" http://101.33.212.119:3100/

# 期望：都是 200
```

### Step 8：浏览器访问 onboarding

- 浏览器打开 `http://101.33.212.119:3100/`
- 用 bootstrap invite URL 注册管理员
- 走完 4 步 onboarding（Company / Agent / Task / Launch）

---

## 🐛 四、踩坑全清单（11 个）

### 坑 1：`bind: loopback` 让公网连不上
**症状**：`curl http://101.33.212.119:3100/` → connection refused  
**原因**：默认 onboard 把 `bind` 设成 `loopback`，只听 `127.0.0.1:3100`  
**解决**：`BIND=lan` + `HOST=127.0.0.1`（绑定 0.0.0.0 但走回环 host）  
**教训**：onboard 完成后必须检查 `bind` 字段

### 坑 2：`local_trusted` 模式锁 bind 为 loopback
**症状**：改了 `BIND=lan` 但仍然只听 loopback  
**原因**：`local_trusted` 部署模式强制 bind=loopback，不生效  
**解决**：`PAPERCLIP_DEPLOYMENT_MODE=authenticated` + `BIND=lan`  
**教训**：部署模式必须先于 bind 设置

### 坑 3：`serveUi: false` 不返回 UI
**症状**：`curl http://101.33.212.119:3100/` 返回 404 或纯 JSON  
**原因**：UI 静态文件没被 serve  
**解决**：`SERVE_UI=true`  
**教训**：生产模式默认是 true，但 onboard 偶尔会重置

### 坑 4：缺 `auth.publicBaseUrl` 导致回调 URL 错乱
**症状**：登录成功但 cookie 域名错乱 / callback 跳到 localhost  
**原因**：默认 baseUrlMode 用 `auto`，没设公网 URL  
**解决**：
```
PAPERCLIP_AUTH_BASE_URL_MODE=explicit
PAPERCLIP_AUTH_PUBLIC_BASE_URL=http://101.33.212.119:3100
```  
**教训**：测试登录必须用公网 IP，不能用 localhost

### 坑 5：`exposure: "public"` 需要 `baseUrlMode=explicit`
**症状**：设了 `EXPOSURE=public` 但其他用户访问还是被限制  
**原因**：schema 验证：public 必须配 explicit base URL  
**解决**：见坑 4  
**教训**：exposure / baseUrlMode / publicBaseUrl 三者强耦合

### 坑 6：schema 验证失败被静默吞掉
**症状**：config.json 里某字段设错，但服务启动后读到的还是默认值  
**原因**：`readConfigFile()` 用了 try-catch，schema 错就 fallback 默认值  
**解决**：检查 `config.json` 的 `$meta` 字段 + 看服务日志  
**教训**：silent-failure 是 paperclip 配置的最大隐患

### 坑 7：双 .env 必须同步
**症状**：改了一份 .env 但生效的是另一份  
**原因**：paperclip 同时加载 `/root/.paperclip/instances/default/.env` 和 `/root/projects/paperclip/.env`，后者优先级高  
**解决**：两份必须同步（推荐脚本化：`diff -u` 检查）  
**教训**：改配置前先 `grep` 看所有 .env 文件

### 坑 8：vite/next 跨源拦截
**症状**：从 `http://101.33.212.119:3100` 访问，前端调 API 报 CORS  
**原因**：Next.js dev server 默认只允许 `localhost`  
**解决**：在 `next.config.mjs` 加 `allowedDevOrigins: ['101.33.212.119', 'localhost']`  
**教训**：所有 dev server 都有 origin 白名单

### 坑 9：bootstrap invite 是 CEO 类型，不能给普通测试者
**症状**：把 bootstrap URL 转给测试者，但接受了后只给 owner 权限  
**原因**：`invite_type=bootstrap_ceo` 设计为"第一次管理员注册"，不是普通 join  
**解决**：手动创建 `company_join` 类型 invite（30 天有效，both join_types）  
**教训**：测试用 invite 必须用普通 `company_join` 类型

### 坑 10：onboard 完成后 invite 已过期
**症状**：`/invite/pcp_bootstrap_xxx` 显示 "Invite not available"  
**原因**：bootstrap_ceo 默认 3 天有效期，过期了  
**解决**：重新跑 `paperclipai auth bootstrap-ceo` 或手动 DB 插入 invite  
**教训**：invite 必须监控，过期前手动续期

### 坑 11：HTTP（非 HTTPS）显示 "不安全"
**症状**：浏览器顶部 "不安全" 警告  
**原因**：paperclip 默认 HTTP，密码 / token 明文传输  
**解决**（未做）：nginx 反代 + Let's Encrypt  
**教训**：测试用 HTTP OK，生产必须 HTTPS

---

## 🔧 五、配置错误排查 SOP

```bash
# 1. 看进程
ps -ef | grep "tsx src/index.ts" | grep -v grep

# 2. 看端口
ss -tlnp | grep :3100

# 3. 看 config.json
cat /root/.paperclip/instances/default/config.json | python3 -m json.tool

# 4. 看 .env（两份）
diff /root/.paperclip/instances/default/.env /root/projects/paperclip/.env

# 5. 看日志
tail -50 /tmp/paperclip.log

# 6. 看 DB
PGPASSWORD=*** psql -h localhost -U paperclip -d paperclip -c "\dt"

# 7. 看 health endpoint
curl http://101.33.212.119:3100/api/health
```

---

## 📊 六、当前状态（2026-07-05 13:00）

| 组件 | 状态 |
|---|---|
| PostgreSQL（systemd）| ✅ 运行中，DB `paperclip` |
| tsx dev server | ✅ PID 229093，0.0.0.0:3100 |
| Public UI | ✅ HTTP 200 |
| bootstrap CEO | ✅ 已注册 hesiyan2008@126.com |
| onboarding | ✅ Company `Deloitte` 已建 |
| Agents | ⚠️ 1 个 `AI Native`（status=error，待修）|
| 测试 invite | ✅ 已生成 30 天有效 `company_join` invite |

---

## ⚠️ 七、未解决的 5 个安全风险

| 风险 | 严重度 | 修复 |
|---|---|---|
| HTTP 明文传输 | 🔴 P0 | nginx + Let's Encrypt |
| `BETTER_AUTH_SECRET` 低熵 | 🔴 P0 | `openssl rand -base64 32` |
| DB password 明文 `paperclip` | 🟡 P1 | 改密码 + vault 存 secret |
| Invite URL 在聊天明文传 | 🟡 P1 | 短期发短链 + 监控 accepted_at |
| RSC payload 偶发泄露凭证 | 🟡 P1 | 待 paperclip 升级修复 |

---

## 🎯 八、生产化清单（待办）

- [ ] nginx + Let's Encrypt（HTTPS）
- [ ] 高熵 `BETTER_AUTH_SECRET`
- [ ] DB password 改强 + 存 vault
- [ ] 跑生产模式（`pnpm build && pnpm start`）
- [ ] 加 systemd unit（开机自启）
- [ ] 加监控 + 告警
- [ ] 备份策略（DB dump / cron）

---

**作者**：小助 — OpenClaw (MiniMax-M3) — 2026-07-05  
**归档位置**：`/root/vault/current-server/2026-07-05_md_paperclip-公网部署完整指南.md`