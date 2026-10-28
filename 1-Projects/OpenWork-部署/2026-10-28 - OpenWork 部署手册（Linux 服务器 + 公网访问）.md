---
title: "OpenWork 部署手册（Linux 服务器 + 公网访问）"
source: self
url: https://github.com/different-ai/openwork
saved_date: 2026-10-28
tags: ["OpenWork", "部署", "Linux", "systemd", "nginx", "Node24", "HTTPS", "MiniMax"]
description: "2026-10-28 在 101.35.52.96 部署 OpenWork Server web 模式的完整过程、踩坑与配置（含 HTTPS + MiniMax 接入）"
---

# OpenWork 部署手册

> 2026-10-28 实测部署。服务器：101.35.52.96（Ubuntu 24.04 / 2C3G / 59G 盘）

## 部署结果

| 项 | 值 |
|---|---|
| 服务地址 | **`https://101.35.52.96:8790`**（自签证书，浏览器需手动信任） |
| 门禁 | HTTP Basic Auth（用户 `openwork`） |
| 模型 | MiniMax-M3 / MiniMax-M3.1-Flash（已接入，workspace 默认 MiniMax-M3） |
| 密码 | `/root/.openwork_web_password`（已生成，14 位随机） |
| 版本 | openwork-server 0.18.63（OpenCode 期望 1.18.33，实际跑 1.19.4） |
| 托管 | systemd `openwork-server.service`，开机自启 + 自动重启 |
| 内部监听 | 127.0.0.1:8788（仅本地） |
| 状态 | ✅ 运行中，端点全部 200 |

**已验证端点**：`/` `/health` `/status` `/capabilities` `/workspaces` `/workspace/:id/skills` `/workspace/:id/plugins` `/experimental/connect/skills` 全部 200，SSE `/workspace/:id/events` 正常。

**已验证端到端**：UI 完整渲染（截图归档），模型下拉可见 MiniMax-M3 / MiniMax-M3.1-Flash；通过 UI 同一路径 `/workspace/:id/opencode2/api/session/:id/prompt` 真实提问「1+1等于几」→ MiniMax-M3 返回 `2`（finish=stop）。

截图：`截图/2026-10-28 - OpenWork Web UI 完整渲染（MiniMax 模型下拉）.png`

## 资源占用

| 项 | 占用 |
|---|---|
| 内存 | server 主进程 ~180MB + OpenCode engine ~270MB + opencode2 ~280MB ≈ **730MB 峰值 890MB** |
| 磁盘 | node 24.22.1 = 681MB，opencode-ai 二进制 = 410MB，`~/.config/openwork` = 215MB（其中 opencode-v2-verified 201MB） |
| 合计新增 | **约 1.3GB** |

⚠️ 本机磁盘已用 93%（剩 4.4G），后续扩 workspace 要留意。

## 部署步骤（可复现）

### 1. Node 24（关键：不能用系统 node 22）

openwork-server 的 `engines` 是 `node >=24.22.1 <25`，**运行时会硬拒** node 22/25+。

nvm 官方源太慢（实测 8 分钟没下完），改用 npmmirror 二进制直装：
```bash
curl -sL -o /tmp/node24.tar.xz \
  https://cdn.npmmirror.com/binaries/node/v24.22.1/node-v24.22.1-linux-x64.tar.xz
mkdir -p ~/.nvm/versions/node/v24.22.1
tar xJf /tmp/node24.tar.xz -C ~/.nvm/versions/node/v24.22.1 --strip-components=1
~/.nvm/versions/node/v24.22.1/bin/node -v   # v24.22.1
```

### 2. 装 openwork-server + opencode

```bash
export PATH=~/.nvm/versions/node/v24.22.1/bin:$PATH
npm install -g openwork-server
npm install -g opencode-ai
```

### 3. 踩坑：engine 自动下载失败 ⚠️

`openwork-server web` 首次启动会去 GitHub 拉 OpenCode 引擎：
```
Downloading OpenCode 1.18.33 (opencode-linux-x64-baseline.tar.gz)
    from https://github.com/anomalyco/opencode/releases/download/...
→ TypeError: fetch failed / UND_ERR_SOCKET
```
**当前网络到 GitHub release CDN 不稳，会直接崩掉整个 server 进程。**

解法：自己装 opencode 二进制，用 `OPENWORK_OPENCODE_BIN` 指过去，绕过下载：
```bash
export OPENWORK_OPENCODE_BIN=/root/.nvm/versions/node/v24.22.1/bin/opencode
```
> 注：`/health` 里 `opencodeInstalledVersion` 仍显示 `null`，但实际 engine 已在跑（`status` 里能看到 `baseUrl`），属显示口径问题，不影响使用。

### 4. systemd 服务

`/etc/systemd/system/openwork-server.service`：
```ini
[Unit]
Description=OpenWork Server (web mode)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/openwork-workspace/demo
Environment=NODE_ENV=production
Environment=PATH=/root/.nvm/versions/node/v24.22.1/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=OPENWORK_OPENCODE_BIN=/root/.nvm/versions/node/v24.22.1/bin/opencode
ExecStart=/root/.nvm/versions/node/v24.22.1/bin/openwork-server web --port 8788 --allowed-hosts 127.0.0.1,localhost
Restart=always
RestartSec=10
StandardOutput=append:/var/log/openwork-server.log
StandardError=append:/var/log/openwork-server.log

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload && systemctl enable --now openwork-server
```

### 5. nginx 反代 + 门禁

`/etc/nginx/conf.d/openwork.conf`：
```nginx
server {
    listen 8790;
    server_name _;
    client_max_body_size 250m;

    auth_basic "OpenWork";
    auth_basic_user_file /etc/nginx/.openwork_auth;

    location / {
        proxy_set_header Authorization "Bearer <client-token>";
        proxy_pass http://127.0.0.1:8788;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 600s;
        proxy_send_timeout 600s;
    }
}
```

**关键坑（踩了两次）**：Basic Auth 和 app 自己的 Bearer token 抢同一个 `Authorization` 头，直接叠加会死循环——浏览器发 Basic，app 收到 Basic 当 Bearer 校验失败返 401，nginx 又返 401 要 Basic。

解法：**nginx 侧强制覆盖上游的 Authorization 头**（`proxy_set_header Authorization "Bearer <token>"`），让 app 永远看到正确的 Bearer，浏览器那层只管 Basic。

> 注意：nginx worker 是 www-data，htpasswd 文件必须 `chmod 644`（600 会 Permission denied → 500）。系统没装 `htpasswd` 命令，用 `openssl passwd -apr1` 生成。

### 5.1 补：必须上 HTTPS（否则页面空白）⚠️

**这是最大的坑**：用 `http://` 访问时页面只有「Starting OpenWork」空白壳，UI 永远起不来。

根因：OpenWork Web UI 启动时调用 `crypto.randomUUID()`，而该 API **只在 secure context（HTTPS 或 localhost）可用**。公网 IP + 明文 HTTP = 非安全上下文 → 抛异常 → React 挂载失败 → 空白页。控制台可见 `TypeError: crypto.randomUUID is not a function`。

解法：自签证书 + nginx TLS 终结。
```bash
openssl req -x509 -nodes -newkey rsa:2048 -days 3650 \
  -keyout /etc/nginx/ssl/openwork.key -out /etc/nginx/ssl/openwork.crt \
  -subj "/CN=101.35.52.96"
# nginx server 块加：
listen 8790 ssl;
listen [::]:8790 ssl;
ssl_certificate     /etc/nginx/ssl/openwork.crt;
ssl_certificate_key /etc/nginx/ssl/openwork.key;
ssl_protocols TLSv1.2 TLSv1.3;
```
> 浏览器首次访问会报「自签证书不受信任」→ 高级 → 继续前往。也可在 headless Chrome 加 `--ignore-certificate-errors`。

### 5.2 补：nginx token 别硬编码（server 重启 token 会变）

app 的 client token 存在 `~/.openwork/openwork-server/web-tokens.json`，**server 重装/重启可能重新生成**。硬编码在 nginx 里就会突然全站 401。

解法：拆成独立 include 文件 + systemd 定时同步。
```bash
# /usr/local/bin/openwork-nginx-sync.sh
TOKEN=$(python3 -c "import json;print(json.load(open('/root/.openwork/openwork-server/web-tokens.json'))['token'])")
printf 'proxy_set_header Authorization "Bearer %s";\n' "$TOKEN" > /etc/nginx/conf.d/openwork-token.conf
nginx -t && systemctl reload nginx
```
```nginx
# openwork.conf 的 location / 里
include /etc/nginx/conf.d/openwork-token.conf;
```
挂到 `openwork-server.service` 的 `ExecStartPost=` / `ExecReload=`，另加 `openwork-nginx-sync.timer`（每 30 分钟）。

### 5.3 补：认证头不能只用 auth_basic ⚠️（页面卡 "Starting OpenWork" 的第二个原因）

**症状**：浏览器里页面永远停在 `Starting OpenWork`，但 HTML 本身 200、控制台无明显报错。

**根因**：OpenWork Web UI 的 JS 在每个 XHR/fetch 上显式带 `Authorization: Bearer <client-token>`（token 由服务端注入 index.html 的 `__OPENWORK_BOOTSTRAP__`）；而浏览器导航请求带 `Authorization: Basic ...`。两者在**同一个头字段**上冲突。

- nginx 用 `auth_basic` → 只认 Basic → App 自己的 XHR 全被 401 → 前端拿不到 `/capabilities` `/status` 等数据 → 永远停在启动壳
- 加 `proxy_set_header Authorization "Bearer ..."` → **只覆盖了发往上游的头，没管入站判定** → nginx 照样把 App 的 XHR 拒了

**解法**：用 `map` 同时认两种头，替掉 `auth_basic`：

```nginx
# /etc/nginx/conf.d/openwork-auth.conf（由 openwork-nginx-sync.sh 生成）
map $http_authorization $ow_auth_ok {
    default 0;
    "~*^Basic\s+\Q<b64 of openwork:password>\E$"    1;
    "~*^Bearer\s+\Q<client-token>\E$"                1;
}
```
```nginx
server {
    ...
    add_header WWW-Authenticate 'Basic realm="OpenWork"' always;  # 仍然弹 Basic 框
    location / {
        if ($ow_auth_ok = 0) { return 401 'Authentication required'; }
        include /etc/nginx/conf.d/openwork-token.conf;  # 发往上游一律用 Bearer
        proxy_pass http://127.0.0.1:8788;
        ...
    }
}
```

> 安全性：Bearer 接受的那个 token 就是服务端塞进 index.html 的 client token，拿到页面就等于拿到它，不算扩大攻击面。真正的门禁仍是 Basic（外网用户必须过口令）。

**排查手法**（下次再遇到空白页先看这个）：
```bash
tail -100 /var/log/nginx/access.log | grep 8790 | awk '{print $9}' | sort | uniq -c
# 如果看到大量 401 且 URL 都是 /capabilities /status /experimental/* → 就是这个认证头冲突
```

> 附带：开 `map` 后 `/env/keys` `/env/status` 仍返回 401，这是**正确的**——那是 host-token 专属接口（会读环境变量明文），web 模式下就不该给远程用户。

### 5.4 补：必须加 session cookie，否则子资源 401（第二个必踩的坑）

**症状**：主文档 200、`/experimental/*` 等 API 全 200，但 **`/assets/app-*.js`、`/assets/app-*.css`、`/manifest.webmanifest` 返回 401**。日志里特征很明显：

```
39.144.156.34 - - [28/Oct/2026:11:53:45 +0800] "GET /assets/app-DZr96oX3.js HTTP/1.1" 401 23
39.144.156.34 - - [28/Oct/2026:11:53:45 +0800] "GET /assets/app-Bx1ym5U0.css HTTP/1.1" 401 23
```

**根因**：**真实 Chrome 不会在子资源请求（module script / CSS / manifest）上可靠地回传缓存的 Basic 凭据**。导航请求带 `Authorization: Basic`，子资源可能完全不带 `Authorization` 头 → 被上一版的 map 判为未认证 → 401 → 脚本和样式加载不出来 → 页面永远停在启动壳。

> **踩坑复盘**：上一版的无头验证之所以“通过”，是因为我用 `Network.setExtraHTTPHeaders` 给**每一个**请求都手动塞了 Authorization，等于人为制造了一个比真实 Chrome 更宽松的环境。**测试方法本身有缺陷，必须模拟真实浏览器的 header 行为。**

**解法**：Basic 认证通过后**下发一个 session cookie**，子资源靠 cookie 走（cookie 在同源子资源上必定回传）。

```nginx
# openwork-nginx-sync.sh 生成
map $http_authorization $ow_auth_basic { default 0; "~*^Basic\s+\Q<b64>\E$" 1; }
map $http_authorization $ow_auth_bearer { default 0; "~*^Bearer\s+\Q<token>\E$" 1; }
map $cookie_ow_sess $ow_auth_cookie { default 0; "~^\Q<secret>\E$" 1; }
map "$ow_auth_basic:$ow_auth_bearer:$ow_auth_cookie" $ow_auth_ok {
    default 0; "~^1:" 1; "~^0:1:" 1; "~^0:0:1" 1;
}
# 仅当 Basic 匹配时下发 cookie；值为空时 nginx 自动省略该 header
map $ow_auth_basic $ow_setcookie {
    default "";
    1 "ow_sess=<secret>; Path=/; HttpOnly; SameSite=Lax; Secure";
}
```

```nginx
location / {
    if ($ow_auth_ok = 0) { return 401 'Authentication required'; }
    add_header WWW-Authenticate 'Basic realm="OpenWork"' always;
    add_header Set-Cookie $ow_setcookie always;
    include /etc/nginx/conf.d/openwork-token.conf;
    proxy_pass http://127.0.0.1:8788;
    ...
}
```

**验证方法**（覆盖三种情况）：

```bash
A="openwork:$(cat /root/.openwork_web_password)"
# 1. 无凭据 -> 401
curl -sk -o /dev/null -w "%{http_code}\n" https://101.35.52.96:8790/
# 2. Basic -> 200 + Set-Cookie
curl -sk -u "$A" -D- -o /dev/null https://101.35.52.96:8790/ | grep -E "HTTP|Set-Cookie"
# 3. 只带 cookie（模拟子资源）-> 200
C=$(curl -sk -u "$A" -D- -o /dev/null https://101.35.52.96:8790/ | grep -i '^set-cookie' | sed 's/.*ow_sess=\([^;]*\).*/\1/')
for p in /assets/app-DZr96oX3.js /assets/app-Bx1ym5U0.css /manifest.webmanifest; do
  curl -sk -H "Cookie: ow_sess=$C" -o /dev/null -w "$p %{http_code}\n" "https://101.35.52.96:8790$p"
done
```

实测：1→401，2→200 + `Set-Cookie: ow_sess=...`，3→三个子资源全 200。

> 注：`/env/keys`、`/env/status` 仍 401 是**正确的**——host-token 专属接口（会读环境变量明文），web 模式下不该给远程用户。

### 5.5 补：openwork-nginx-sync.sh 改用 Python 写

bash 写这个脚本有个坑：`$(python3 -c ...)`、`$(tr -d ...)` 这类命令替换在 heredoc / 多层引号里极易被写坏（本次实际出现过 `TOKEN=***` 被吞成乱码导致 nginx -t 报 `unknown "ow_setcookie" variable`）。已改写成纯 Python 脚本（`#!/usr/bin/env python3`），用 f-string 拼 nginx 配置，逻辑更稳。文件仍是 `/usr/local/bin/openwork-nginx-sync.sh`。

## 接入 MiniMax（已实测跑通）

### 根因：baseURL 用错协议 → 404

OpenWork 用 `@ai-sdk/openai-compatible` 拼 `/chat/completions`，所以 baseURL 必须是 **OpenAI 兼容端点**，不能填 Anthropic 兼容端点。

| baseURL | 结果 |
|---|---|
| `https://api.minimaxi.com/anthropic/v1` | ❌ `HTTP 404 page not found`（拼成 `/anthropic/v1/chat/completions`） |
| `https://api.minimaxi.com/v1` | ✅ 正常 |

MiniMax key 放在两个地方（engine v2 配置）：
- `/root/.config/openwork/opencode-v2/state/config/opencode.json` → `providers.minimax.settings.apiKey`
- `~/.local/share/opencode/auth.json` → `{"minimax":{"type":"api","key":"sk-cp-..."}}`

### 用官方 API 改配置（别手改 sqlite）

server 提供 host-token 保护的接口，**必须用 `x-openwork-host-token` 头**（不是 `Authorization: Bearer`）：
```bash
HT=$(python3 -c "import json;print(json.load(open('/root/.openwork/openwork-server/web-tokens.json'))['hostToken'])")
CT=$(python3 -c "import json;print(json.load(open('/root/.openwork/openwork-server/web-tokens.json'))['token'])")

# 改 provider（PATCH，不是 PUT）
curl -u "openwork:$(cat /root/.openwork_web_password)" \
  -H "x-openwork-host-token: $HT" -H "Authorization: Bearer $CT" \
  -X PATCH http://127.0.0.1:8788/runtime-config/providers \
  -H "Content-Type: application/json" -d @provider.json
# → {"ok":true,"changed":true,...,"reload":"reloaded"}

# 设 workspace 默认模型
curl -u "openwork:$(cat /root/.openwork_web_password)" \
  -H "Authorization: Bearer $CT" -X PUT \
  http://127.0.0.1:8788/workspace/$WS/default-model \
  -H "Content-Type: application/json" \
  -d '{"model":{"providerID":"minimax","modelID":"MiniMax-M3"}}'
```
> `default-model` 的 body 必须是 `{"model":{...}}` 嵌套结构，直接给 `{"providerID":...}` 会 400。

### 认证分三段，别搞混

| 层 | 头 | 值 |
|---|---|---|
| nginx 门禁 | `Authorization: Basic ...` | 浏览器弹框输入 |
| nginx → app | `proxy_set_header Authorization` | 强制覆盖成 `Bearer <client-token>` |
| app 内部管理接口 | `x-openwork-host-token` | host token |

**curl 走公网时不要手动加 `Authorization: Bearer`**，会覆盖 Basic 头导致 401（nginx 只认 Basic）。

### UI 实际调用的接口（和 curl 测试一致）

```
POST /workspace/:wsId/opencode2/api/session              # 建会话
POST /workspace/:wsId/opencode2/api/session/:sid/prompt  # 发消息
     body: {"text":"...","model":{"providerID":"minimax","modelID":"MiniMax-M3"}}
GET  /workspace/:wsId/opencode2/api/session/:sid/message # 读回复
```
> 注意路径是 `/api/session/:id/prompt`，不是 `/message`（后者 404）。

## 运维命令

## 认证 token 在哪

- app client token / host token：`~/.openwork/openwork-server/web-tokens.json`（0600）
- app 自身配置：`~/.config/openwork/server.json`
- Basic Auth 口令：`/root/.openwork_web_password`（0600），哈希在 `/etc/nginx/.openwork_auth`（0644，给 nginx worker 读）

## 运维命令

```bash
systemctl status openwork-server
systemctl restart openwork-server
tail -f /var/log/openwork-server.log
curl -sk -u "openwork:$(cat /root/.openwork_web_password)" https://101.35.52.96:8790/health
/usr/local/bin/openwork-nginx-sync.sh    # 手动同步 nginx token
```

## 还没做的

- [x] 配模型（MiniMax-M3 / M3.1-Flash）
- [x] 上 HTTPS（自签证书）
- [ ] 未配更多工作区（当前只有一个 demo 目录 `/root/openwork-workspace/demo`）
- [ ] 未审遥测（`ee/packages/telemetry`、`den-diagnostics` 存在，虽然本地部署没走 Den）
- [ ] 未接 OpenWork MCP 到 OpenClaw（`https://api.openworklabs.com/mcp/agent` 需要 OpenWork 账号）
- [ ] 未换自签证书为可信证书（Let\'s Encrypt 需域名，当前只有 IP）

## 备注

- 桌面 App（Electron，300MB+）**没装**——服务器无桌面环境，装了没意义
- 只部署了 server 模式；OpenWork Den（企业控制面）需要 MySQL + Redis，本次未部署
