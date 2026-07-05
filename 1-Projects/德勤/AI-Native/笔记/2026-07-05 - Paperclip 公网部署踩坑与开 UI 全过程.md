---
title: Paperclip 公网部署踩坑与开 UI 全过程
date: 2026-07-05
type: deployment-kb
status: ✅ 已跑通（公网 UI + bind 0.0.0.0）
deploy_path: /root/projects/paperclip
web_port: 3100
public_url: http://101.33.212.119:3100
purpose: Paperclip 从 local_trusted 升级到 authenticated 模式的完整改动 + 6 个实战坑
related:
 - 2026-06-28 - Paperclip - GitHub Deep Research.md
 - 2026-07-05 - AgentSpace 部署踩坑与修复全集（归档版）.md
---

# 🚀 Paperclip 公网部署踩坑与开 UI 全过程

> **作者**：小助（OpenClaw / MiniMax-M3）
> **写于**：2026-07-05 11:38
> **对象环境**：腾讯云 Ubuntu 24.04 / 2 vCPU / 3.6 GiB / Node 22.23.1
> **前后对比**：onboard 默认（loopback/UI 关）→ 公网 UI 可用

---

## 0. 最终结论（先看这里）

| 维度 | 结果 |
|---|---|
| 部署模式 | `local_trusted` → **`authenticated (private)`** |
| Bind | `loopback (127.0.0.1)` → **`lan (0.0.0.0)`** |
| UI | `disabled` → **enabled @ `http://101.33.212.119:3100`** |
| 公网访问 | ✅ HTTP 200（实测） |
| Claim admin | ⚠️ **必须**用一次性 URL 把 local-board 转给真用户 |
| 安全审计 | ⚠️ HTTP 明文 + Better Auth 低熵密钥 — 投产前必修 HTTPS |

---

## 1. 完整修改清单（4 个文件）

### 1.1 `/root/.paperclip/instances/default/config.json`

```diff
  "server": {
-    "deploymentMode": "local_trusted",
-    "exposure": "private",
-    "bind": "loopback",
-    "host": "127.0.0.1",
+    "deploymentMode": "authenticated",
+    "exposure": "private",
+    "bind": "lan",
+    "host": "127.0.0.1",
    "port": 3100,
-    "allowedHostnames": [],
-    "serveUi": false
+    "allowedHostnames": [
+      "101.33.212.119",
+      "101.35.52.96",
+      "localhost",
+      "127.0.0.1"
+    ],
+    "serveUi": true
  },
+  "auth": {
+    "baseUrlMode": "explicit",
+    "publicBaseUrl": "http://101.33.212.119:3100",
+    "disableSignUp": false
+  }
```

### 1.2 `/root/.paperclip/instances/default/.env`

```diff
  PORT=3100
- SERVE_UI=false
+ SERVE_UI=true
+ PAPERCLIP_DEPLOYMENT_MODE=authenticated
+ BIND=lan
+ HOST=127.0.0.1
+ EXPOSURE=private
  BETTER_AUTH_SECRET=paperclip-dev-secret
  PAPERCLIP_AGENT_JWT_SECRET=18d9c2…7926
```

### 1.3 `/root/projects/paperclip/.env`（项目级）

同上 1.2（两份 .env 同步，否则 paperclip 启动时会混乱）

### 1.4 安全建议（未改，待何大人决策）

- ⚠️ `BETTER_AUTH_SECRET=paperclip-dev-secret` **必须**改成 32+ 字符高熵密钥
- 命令：`openssl rand -base64 32`
- 不改会有低熵警告 + 投产风险

---

## 2. 6 个实战坑（症状 → 根因 → 解法 → 教训）

### 坑 #1：banner 显示 loopback 但 config 写的是 lan

| 项 | 内容 |
|---|---|
| 症状 | config.json 写 `bind: "lan"`，banner 仍显示 `Bind loopback (127.0.0.1)` |
| 根因 | paperclip 启动时**先读 .env，再读 config.json**，.env 里没有 BIND 变量时 schema 校验可能失败 → `readConfigFile()` catch → 返回 null → 走默认（loopback）|
| 解法 | **同时**改 config.json 和 .env 两份（外加项目级 .env）|
| 教训 | Paperclip 多源配置优先级混乱，**改配置三个地方都要改** |
| 等级 | 🔴 必踩 |

### 坑 #2：bind 字段是枚举，不是字符串 IP

| 项 | 内容 |
|---|---|
| 症状 | 写 `bind: "0.0.0.0"` → CLI 报 `Invalid enum value. Expected 'loopback' \| 'lan' \| 'tailnet' \| 'custom', received '0.0.0.0'` |
| 根因 | Paperclip 的 `bind` 字段是枚举（4 个值），不是 IP 地址字符串 |
| 解法 | 用 `bind: "lan"`（4 个值含义见下表）|

| 取值 | 含义 | host 解析 |
|---|---|---|
| `loopback` | 仅本机 | `127.0.0.1` |
| `lan` | 所有 LAN 接口 | `0.0.0.0` |
| `tailnet` | Tailscale 地址 | 自动检测 |
| `custom` | 自定义 IP | 需 `customBindHost` 字段 |

| 教训 | **schema 校验失败是静默回退的**（readConfigFile catch 直接返回 null），不会被发现 |
| 等级 | 🔴 必踩 |

### 坑 #3：`local_trusted` 锁死 loopback

| 项 | 内容 |
|---|---|
| 症状 | `bind: "lan"` 仍报 `local_trusted requires server.bind=loopback` |
| 根因 | 部署模式硬约束：`local_trusted` 模式**只允许 loopback**（无需认证的本地信任场景）|
| 解法 | 改 `deploymentMode: "authenticated"`（可对外 + 需要登录）|
| 教训 | 想公网暴露 Paperclip，**必须切换到 authenticated 模式** |
| 等级 | 🔴 必踩 |

### 坑 #4：`exposure: "public"` 触发 schema 拒绝（静默）

| 项 | 内容 |
|---|---|
| 症状 | 设 `exposure: "public"` + 没设 `auth.baseUrlMode`，schema 校验失败但**没有任何错误输出**，整个 config 被丢弃 |
| 根因 | `server.exposure === "public"` 必须配 `auth.baseUrlMode === "explicit"` + `auth.publicBaseUrl` |
| 解法 | 要么设 `exposure: "private"`（公网仍可访问，只是 metadata 不标 public），要么同时设 `auth.baseUrlMode=explicit` + `publicBaseUrl=http://101.33.212.119:3100` |
| 教训 | **schema 校验失败会静默回退默认**——调试时必须看 banner 上的 deploy 字段，反推 config 是否被接受 |
| 等级 | 🔴 必踩 |

### 坑 #5：`.env` 有项目级 + 实例级两份，可能不同步

| 项 | 内容 |
|---|---|
| 症状 | 改了 `/root/.paperclip/instances/default/.env` 没改 `/root/projects/paperclip/.env` |
| 根因 | paperclip 启动时既读项目根目录 .env，也读实例目录 .env，**优先级取决于 launch 方式** |
| 解法 | **两份都改**（保持同步）|
| 教训 | paperclip 多实例/多配置源混乱——生产最好只用实例目录 .env |
| 等级 | 🟡 注意 |

### 坑 #6：`pnpm paperclipai allowed-hostname <ip>` 用法特别

| 项 | 内容 |
|---|---|
| 症状 | `pnpm paperclipai allowed-hostname add 101.33.212.119` → `too many arguments for 'allowed-hostname'. Expected 1 argument but got 2` |
| 根因 | 这个子命令**不要 `add`**，直接传 IP 作为位置参数 |
| 解法 | `pnpm paperclipai allowed-hostname 101.33.212.119`（一次性加）|
| 教训 | paperclipai CLI 各子命令风格不统一（有的要 add，有的直接传参），要看 `--help` |
| 等级 | 🟢 一次性 |

---

## 3. 重启 SOP（4 步走）

```bash
# 1. 杀干净（避免 3100/3101 冲突）
for pid in $(ps -ef | grep -E "paperclip|tsx src/index" | grep -v grep | awk '{print $2}'); do
  kill -9 $pid
done

# 2. 验证端口空
ss -tlnp | grep ":3100"  # 应该空

# 3. 启动
cd /root/projects/paperclip
nohup pnpm --filter @paperclipai/server exec tsx src/index.ts > /tmp/paperclip.log 2>&1 &
disown

# 4. 验证
sleep 5
grep -E "Bind|Server|UI" /tmp/paperclip.log | head -10
curl -sS -o /dev/null -w "127.0.0.1:3100 \u2192 HTTP %{http_code}\n" http://127.0.0.1:3100/
curl -sS -o /dev/null -w "101.33.212.119:3100 \u2192 HTTP %{http_code}\n" http://101.33.212.119:3100/
```

**期望 banner**：
```
Deploy          authenticated (private)
Bind            lan (0.0.0.0)
Server          3100
UI              http://localhost:3100
```

---

## 4. Claim admin 流程（必须做）

启动后日志里会出现**一次性 claim URL**：

```
BOARD CLAIM REQUIRED
This instance was previously local_trusted and still has local-board as the only admin.
Sign in with a real user and open this one-time URL to claim ownership:
http://localhost:3100/board-claim/<hex>?code=<hex>
```

**操作步骤**：
1. 浏览器打开 `http://101.33.212.119:3100`
2. 用邮箱注册第一个账号（自动成为 admin）
3. 把上面的 `localhost:3100` 替换为 `101.33.212.119:3100`，访问 claim URL
4. local-board admin 转移给真实用户

⚠️ claim URL **只能用一次**且**有时效**——尽快操作

---

## 5. 安全风险清单（投产前必修）

| 风险 | 等级 | 解法 |
|---|---|---|
| HTTP 明文传输 | 🔴 P0 | nginx + Let's Encrypt HTTPS |
| BETTER_AUTH_SECRET 低熵 | 🔴 P0 | `openssl rand -base64 32` 生成 |
| Better Auth baseURL 未设置 | 🟡 P1 | 设 `auth.publicBaseUrl=http://<公网域名>` |
| 端口 3100 腾讯云安全组未放通 | 🟡 P1 | 控制台放通（仅 101.35.52.96 需放通，101.33.212.119 已通）|
| Paperclip dev 模式（tsx）非生产 | 🟢 P2 | `pnpm build && pnpm start` 生产模式 |

---

## 6. 时间线

| 步骤 | 时间 | 备注 |
|---|---|---|
| 看 Paperclip 状态汇报 | 11:30 | 用户问 |
| 改 config.json（serveUi + bind）| 11:33 | 重启后仍是 loopback |
| 发现 .env 优先级（坑 #1）| 11:34 | 同步改 .env |
| `bind: "0.0.0.0"` 校验失败（坑 #2）| 11:35 | bind 是枚举 |
| `local_trusted` 锁死（坑 #3）| 11:35 | 改 deploymentMode=authenticated |
| `exposure: "public"` 静默拒绝（坑 #4）| 11:37 | 改 exposure=private + auth 配 |
| 杀老进程占端口（3100 vs 3101）| 11:38 | kill -9 全清 |
| 公网 HTTP 200 验证 | 11:39 | ✅ 完成 |

**总耗时**：~9 分钟（4 个 schema 坑 + 1 个进程坑 + 2 个调研）

---

## 7. 给新服务器部署的提醒

| 项 | 本服务器 | 新服务器 |
|---|---|---|
| Paperclip 路径 | `/root/projects/paperclip` | 建议同 |
| 部署模式 | `authenticated` | 必须 |
| Bind | `lan` | 必须（不是 loopback）|
| 公网端口 | 3100 | 需提前放通 |
| HTTPS | ❌ | **投产前必修** |
| Auth 密钥 | ⚠️ 低熵 | 用 `openssl rand -base64 32` |

---

**作者**：小助 — OpenClaw (MiniMax-M3) — 2026-07-05 11:39
