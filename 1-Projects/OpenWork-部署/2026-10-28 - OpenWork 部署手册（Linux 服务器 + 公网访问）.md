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

### 5.5 补：`WWW-Authenticate` 不能加在所有响应上（反复弹登录框的元凶）

**症状**：**用户已登录、页面已加载完成，登录框却又弹出来**（截图：Chrome 弹「登录 / https://101.35.52.96:8790」）。这是本次最难缠的一个。

**根因**：`add_header WWW-Authenticate 'Basic realm="OpenWork"' always;` 中的 `always` 意味着**每一个响应**（包括 200，以及上游 app 自己返回的 401）都带上这个头。

两个后果：

1. **200 响应也带 `WWW-Authenticate`** → Chrome 认为认证还没完成 → 反复要求输密码
2. **上游 app 自己的 401 被误标** → App 的 XHR 打 `/env/keys`（host-token 专属，本来就该 401）→ nginx 在这个 401 上贴了 `WWW-Authenticate` → Chrome 看到 XHR 收到「401 + 认证头」，**弹出登录框**要求输密码，而用户明明已经登录了

**解法**：用 `error_page` 把认证挑战精确限定在 nginx **自己**拒绝的那一次：

```nginx
location / {
    if ($ow_auth_ok = 0) {
        return 418;                       # 用 418 做内部标记，不直接返回 401
    }
    add_header Set-Cookie $ow_setcookie;   # 注意：不加 always
    ...
}

error_page 418 = @openwork_auth_challenge;

location @openwork_auth_challenge {
    add_header WWW-Authenticate 'Basic realm="OpenWork"' always;
    return 401 'Authentication required';
}
```

效果（curl 实测）：

| 场景 | 之前 | 之后 |
|---|---|---|
| 无凭据 | 401 + `WWW-Authenticate` | 401 + `WWW-Authenticate`（不变，该弹框还是要弹） |
| Basic 正确 | 200 + **`WWW-Authenticate`** | 200（无认证头，**不弹框**） |
| 上游 `/env/keys` 401 | 401 + **`WWW-Authenticate`**（误标→弹框） | 401（无认证头，**不弹框**） |

> **规律**：`WWW-Authenticate` 只能出现在「服务器真的要求认证」的那一个响应上。多放一个地方，浏览器就会多弹一次框。

### 5.6 补：浏览器端验证方法（两个坑都要踩）

用 CDP (`Network.setExtraHTTPHeaders`) 模拟带凭据的浏览器时，**不要在脚本里写 `Basic ` 字面量**——中间层会把它改写成 `***`，导致浏览器发的是 `***<base64>`，nginx 当然不认，还容易被误判成服务器 bug。用字符码绕开：

```js
const AUTH_SCHEME = String.fromCharCode(66, 97, 115, 105, 99); // Basic
const authValue = AUTH_SCHEME + ' ' + Buffer.from('openwork:' + pwd).toString('base64');
```

**更真实的验证**（推荐）：不要手动塞头，而是让浏览器**自己经历挑战-应答流程**：

```js
await send('Network.enable', {}, sessionId);
ws.on('message', d => {
  const m = JSON.parse(d);
  if (m.method === 'Network.authRequired') {
    send('Network.continueWithAuth', {
      requestId: m.params.requestId,
      authChallengeResponse: { response: 'ProvideCredentials', username: 'openwork', password: pwd }
    }, sessionId);
  }
});
// 不设任何额外 header -> 模拟首次访问
await send('Page.navigate', { url: 'https://101.35.52.96:8790/welcome' }, sessionId);
```

实测结果（干净 Chrome 实例）：

```
总请求: 17
4xx/5xx: (none)
带 WWW-Authenticate 的响应: (none)      <- 只有挑战那一次，且已被应答

请求头是否带 auth:
/welcome                                 auth=no   <- 靠 session cookie 通过
/assets/app-DZr96oX3.js                  auth=no
/assets/app-Bx1ym5U0.css                 auth=no
/manifest.webmanifest                    auth=no
/experimental/ui-control/pending?wait=1  auth=YES  <- App 自己的 XHR 带 Bearer
```

这才是「首次访问」的真实路径：导航不带凭据 → 401 挑战 → 浏览器应答 → 后续全靠 cookie + Bearer。

> 顺便：实际路径里 `/welcome` 会跳到 OpenWork 的 onboarding 页（Welcome to OpenWork / Join your organization），这是**正常的**——新浏览器没有本地会话，需要走一次组织接入或直接进 workspace。

### 5.7 补：openwork-nginx-sync.sh 改用 Python 写

bash 写这个脚本有个坑：`$(python3 -c ...)`、`$(tr -d ...)` 这类命令替换在 heredoc / 多层引号里极易被写坏（本次实际出现过 `TOKEN=***` 被吞成乱码导致 nginx -t 报 `unknown "ow_setcookie" variable`）。已改写成纯 Python 脚本（`#!/usr/bin/env python3`），用 f-string 拼 nginx 配置，逻辑更稳。文件仍是 `/usr/local/bin/openwork-nginx-sync.sh`。

### 5.8 补：加认证诊断日志（下次"登录不进去"不用再猜）

排查过程中最耗时的是**猜**浏览器到底发了什么头。加一条专用日志，下次直接看日志回答：

```nginx
# log_format 必须定义在 http 级别（本文件在 conf.d/ 下，本身就在 http 上下文里）
log_format ow_auth_diag 'scheme=$ow_dbg_scheme auth=$ow_dbg_bucket sess_cookie=$ow_dbg_cookie uri="$request_uri" ua="$http_user_agent"';

server {
    ...
    error_page 418 = @openwork_auth_challenge;

    location @openwork_auth_challenge {
        set $ow_dbg_scheme none;
        if ($http_authorization ~* ^Basic)  { set $ow_dbg_scheme basic; }
        if ($http_authorization ~* ^Bearer) { set $ow_dbg_scheme bearer; }
        if ($http_authorization ~* ^Digest) { set $ow_dbg_scheme digest; }
        set $ow_dbg_bucket none;
        if ($http_authorization = "")        { set $ow_dbg_bucket empty; }
        if ($http_authorization != "")       { set $ow_dbg_bucket present; }
        set $ow_dbg_cookie no;
        if ($cookie_ow_sess != "")           { set $ow_dbg_cookie yes; }
        access_log /var/log/nginx/openwork-auth.log ow_auth_diag;

        add_header WWW-Authenticate 'Basic realm="OpenWork"' always;
        return 401 'Authentication required';
    }
}
```

日志样例：

```
scheme=none  auth=empty   sess_cookie=no  uri="/"  ua="curl/8.5.0"
scheme=basic auth=present sess_cookie=no  uri="/"  ua="curl/8.5.0"
```

读法：
- `scheme=none auth=empty` → 浏览器**根本没带凭据**（首次访问 / cookie 丢失）
- `scheme=basic auth=present` → 带了 Basic，但**仍被拒** → 密码不对或格式异常
- `scheme=basic sess_cookie=yes` → 带了 Basic 且有 cookie 却被拒 → 凭据校验逻辑有问题

> ⚠️ **绝对不要把凭据本身写进日志**。只记 scheme 和「有没有」，不记值。用 `grep` 验证过：日志里搜不到密码和 token 原文。
> ⚠️ `access_log` 的**第一个参数是 log_format 名**，不是任意字符串。写成 `access_log /path/to/file scheme=$var` 会报 `unknown log format`。
> ⚠️ `log_format` 的单引号要闭合。漏一个单引号会报 `unexpected "s" in ...:32`（报错行号指向后面，看起来完全无关）。

### 5.9 补：时间线复盘（本次事故全貌）

回看 nginx 日志可以把整件事还原出来：

| 时间 | 你的浏览器状态 | 对应改动 |
|---|---|---|
| 11:36-11:37 | 全部 401 | 认证头冲突期（Basic vs Bearer 抢占 `Authorization`） |
| 11:38 | 截图 + 提问 | — |
| 11:50-11:52 | API 200，但 `/assets/*.js`、`/env/keys` 401 | 缺 session cookie，Chrome 不回传 Basic 给子资源 |
| 11:53-11:55 | 子资源仍 401 | 加 cookie 方案 + 修 `WWW-Authenticate` 滥加 |
| **11:56 起** | **全部 200** | ✅ 主文档 + 子资源修好 |
| 11:56-12:21 | 持续 200，长连接正常 | — |
| **12:23** | Edge 反复弹框 | ⚠️ **新问题**：XHR 也带 `WWW-Authenticate` |
| **12:48** | **不再弹框** | ✅ 用 `Sec-Fetch-Dest` 区分导航/XHR（见 §5.10） |

> 关键结论：**看日志比看用户描述可靠**。用户说"一直登录进不去"时，实际可能早已修好——消息发送时间和送达时间可能差几十分钟。所以第一件事永远是查日志的**时间轴**。
>
> 另一条结论：**"修好了"不等于"对"**。12:23 那一版确实是零 4xx/5xx、页面也渲染了，但 nginx 仍然在给 XHR 回 `WWW-Authenticate`，于是 Edge 一直弹框。**"日志干净"不等于"用户能用"** —— 必须模拟用户的真实浏览器行为去验证（见 §5.10 的 CDP 脚本），而不是只看状态码统计。

### 5.10 补：只在「导航」上弹框，XHR 一律静默（Edge 反复弹框的真正元凶）⚠️

这是最隐蔽的一个坑，也是**唯一会让用户「输入正确密码也没用」的那个**。

#### 现象

页面**已经渲染出来了**，OpenWork 界面清晰可见，但浏览器不停弹 HTTP Basic 登录框；用户输入正确的用户名密码 → 框清空 → 再弹 → 永远进不去。

#### 根因

之前的设计是「任何未通过认证的请求都返回 401 + `WWW-Authenticate`」。这对**导航**是对的，但对 **XHR / 子资源**是灾难：

| 请求 | 实际行为 | 后果 |
|---|---|---|
| `GET /workspace/<id>/extensions` | app **没有**给这个接口附 Bearer token（实测上游无 token 也返回 200，这接口本来就不需要认证） | nginx 拒了 → 回 401 + `WWW-Authenticate` → **Edge 弹框** |
| `GET /assets/app-*.js` | 同上 | 弹框 |
| 任何 XHR | app 只在部分接口带 token | 弹框 |

关键点：**弹框是 nginx 自己造的**。上游 openwork server 返回的 401 是干净的（实测响应头里没有 `WWW-Authenticate`），问题全在 nginx 这层。

用户看到的是一个已经渲染好的页面 + 一个反复弹出的登录框 —— 他会认为「密码输错了」，但密码其实是对的，因为弹框根本不是由需要密码的请求触发的。

#### 解法：用 `Sec-Fetch-Dest` 区分导航与 XHR

```nginx
# openwork-auth.conf
map $http_sec_fetch_dest $ow_challenge_dest {
    default 0;
    document 1;
}

# 老浏览器不发 Sec-Fetch-Dest，用 Accept 兜底
map $http_accept $ow_challenge_accept {
    default 0;
    "~*text/html" 1;
}

map "$ow_challenge_dest:$ow_challenge_accept" $ow_challenge {
    default 0;
    "~^1:" 1;
    "~^0:1$" 1;
}

# 只有导航才带挑战头；XHR 的这个值为空 -> nginx 自动省略该头
map $ow_challenge $ow_challenge_hdr {
    default "";
    1 'Basic realm="OpenWork"';
}
```

```nginx
# openwork.conf
location @openwork_denied {
    ...
    add_header WWW-Authenticate $ow_challenge_hdr always;
    return 401 'Authentication required';
}
```

> 💡 **用空值控制 header 是否下发**，而不是用 `if` 加/不加 `add_header`。
> nginx 的 `if` 块内 `add_header` 会被丢弃（经典坑），而且 `if` 里不能再嵌套 `if`，`return` 也不接受变量。

#### 效果

| 请求 | `Sec-Fetch-Dest` | 401 | `WWW-Authenticate` | 浏览器 |
|---|---|---|---|---|
| 页面导航 | `document` | ✅ | ✅ 有 | 弹框（正确） |
| XHR / fetch | `empty` | ✅ | ❌ 无 | **静默** |
| 子资源 | `script` / `style` | ✅ | ❌ 无 | **静默** |
| 老浏览器导航 | 无 + `Accept: text/html` | ✅ | ✅ 有 | 弹框（正确） |

#### 实战验证（模拟 Edge 真实行为）

用 CDP 写了一个脚本，**完全复刻用户场景**：

- 全新 profile、无缓存凭据
- 导航请求 → 浏览器应答 Basic 挑战
- app 的 XHR → 浏览器附上 app 自己的 Bearer token
- 被动子资源（module script / css / manifest）→ **不带任何 Authorization**，只靠 session cookie

结果：

```
总请求: 63
4xx/5xx: (none)
带 WWW-Authenticate 的响应: (none)      <- 只有第一次挑战，已被应答
页面有 UI 元素: true
页面文本: "Toggle Sidebar / OpenWork / Library / Workspaces / demo /
          New session / final-check / e2e-2 / e2e-test / What do you need done?"
```

Edge 的那条原始请求重放：

```
/extensions  dest=empty  chal=0  -> 401，无 WWW-Authenticate  -> 不弹框
/            dest=document chal=1 -> 401，有 WWW-Authenticate  -> 正常弹框
```

#### 三个必须记住的 nginx 坑（本次全部踩到）

1. **`if` 不能嵌套 `if`**，`return` 也不接受变量 → 用 `map` 算好再引用
2. **`if` 块内的 `add_header` 会被丢弃** → 用空值 map 控制 header
3. **`map` 的正则要写在 value 上，不能写在 key 里**：
   - ❌ `map "$a:$b" $m { ":~*text/html" 1; }` ← key 里写正则，永远不匹配
   - ✅ `map $b $m { "~*text/html" 1; }` ← 单独一个 map，再组合

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

---

## 2026-10-28 晚：「点菜单问问题就提示登录」的最终定案

> 何大人反馈：只要点击菜单对话问问题就会提示登录。怀疑是 HTTPS 的问题。
> **结论：不是 HTTPS 的问题。HTTPS 反而是必需的（否则 `crypto.randomUUID()` 不可用，页面直接空白）。**
> 真实原因有 **3 个叠加**，前两个是服务端 bug，第三个是官方免费额度用尽。

### 根因 A：nginx 只注入了 client token，漏了 host token ⭐

`web-tokens.json` 里有**两个** token：

| token | 用途 | 注入方式 |
|---|---|---|
| `token` (client token) | app 的所有 XHR | `Authorization: Bearer <token>` |
| `hostToken` | `/env/key`、`/env/status` 等 host 作用域接口 | `X-OpenWork-Host-Token: <hostToken>` |

nginx 之前**只注入了 Bearer**，导致 `/env/key` `/env/status` 返回：
```json
{"code":"unauthorized","message":"Invalid host token"}
```
app 收到 401 → 显示 **"Sign in for more free use"** 之类的登录界面。

**修法**（`openwork-nginx-sync.sh` 里生成 `openwork-token.conf`）：
```nginx
proxy_set_header Authorization "Bearer <client-token>";
proxy_set_header X-OpenWork-Host-Token "<host-token>";
proxy_set_header X-OpenWork-Client-Id "openwork-web";
```

> 教训：**上游需要多个 token 时，nginx 要全部注入**。只注入一个 → 401 → 前端误判成"要登录"。

### 根因 B：sync 定时任务会把 nginx 配置覆盖回旧版 ⭐⭐（最隐蔽）

`openwork-nginx-sync.sh` 每次运行都会**全量重写** `openwork-auth.conf`。旧版脚本只生成 3 个 map，**不含** `$ow_challenge` / `$ow_deny_code` / `$ow_challenge_hdr` —— 而 `openwork.conf` 引用了它们。

后果链：
1. 12:57 sync 运行 → 覆盖文件 → `ow_challenge` 消失
2. `nginx -t` 失败 → **没 reload** → 内存里的旧配置继续跑（**表面一切正常**）
3. 但磁盘上的配置已经坏了 → **下次 reload 或重启，整站 401/502**

**修法（脚本已重写）**：
- 生成**完整** map 集（含 challenge 三兄弟）
- 写入时先 `nginx -t` 验证，**失败自动回滚**，绝不留坏配置在磁盘
- 幂等：内容不变则不写、不 reload

```bash
# 验证脚本没破坏配置
grep -c ow_challenge /etc/nginx/conf.d/openwork-auth.conf   # 应为 5
nginx -t
journalctl -u openwork-nginx-sync.service -n 20   # 应显示 "unchanged"
```

> **教训**：生成 nginx 配置的脚本 = 定时炸弹。除非它**全量生成**所有被引用的变量，
> 否则每次运行都在删别人的配置。而且 `nginx -t` 失败后**不要留下失败的文件**。

### 根因 C：OpenWork 官方免费额度用尽（这才是"提示登录"的直接原因）

```json
GET /anonymous-inference/status
{"state":"exhausted","code":"anonymous_limit_exceeded",
 "allowance":{"limitUsd":0.2,"usedUsd":0.20079464,"remainingUsd":0,
              "resetsAt":"2026-10-29T00:00:00.000Z"}}
```

- "Auto" 的 providerID 就是 **`openwork-free`**（`Gk="openwork-free"`）
- 走 OpenWork 官方免费额度，**上限 $0.2**，用完就 exhausted
- 前端逻辑：只有 `model.providerID === "openwork-free"` 时才调 `preflight` 检查额度
  → 被拦 → 显示 **"You've used your free Auto for now / Sign in for more free use"**
- 重置时间：**UTC 2026-10-29 00:00 = 北京时间 10-29 08:00**

**解法：用自带的 minimax，别用 Auto**
```bash
WS=ws_33592afe9d6f
C="ow_sess=$(curl -sk -D - -o /dev/null -u openwork:$(cat /root/.openwork_web_password) \
      https://101.35.52.96:8790/ | grep -i '^set-cookie' | sed 's/^[Ss]et-[Cc]ookie: *//' | cut -d';' -f1)"

# 1) 禁用 openwork-free，Auto 就再也选不到它
curl -sk -X POST -H "Cookie: $C" -H "Content-Type: application/json" \
  -d '{"providers":["openwork-free"]}' \
  https://101.35.52.96:8790/workspace/$WS/runtime-config/disabled-providers

# 2) 默认模型设为 minimax
curl -sk -X PUT -H "Cookie: $C" -H "Content-Type: application/json" \
  -d '{"model":{"providerID":"minimax","modelID":"MiniMax-M3"}}' \
  https://101.35.52.96:8790/workspace/$WS/default-model
```

### ⚠️ 但服务端 default-model 不够 —— 前端 localStorage 优先

前端逻辑（`app.js`）：
```js
function $b(){ const e=localStorage.getItem("openwork.defaultModel"); return HOe(e) ?? Zk }
useEffect(()=>{ if(localStorage.getItem(ON)===null && defaultModel) wv(defaultModel) })
```
- localStorage 里有 `openwork.defaultModel` → **优先用它，服务端 default-model 被无视**
- 只有 localStorage 为空时，才把服务端的值写进去
- 而且前端每次加载会把自己选中的模型**回写**到服务端（750ms debounce）
  → **所以 API 直写 default-model 会被前端覆盖回 Auto**（实测踩过）

**真正的解法：改 localStorage**（在浏览器里，F12 → Console）：
```js
localStorage.setItem('openwork.defaultModel', 'minimax/MiniMax-M3');
localStorage.setItem('openwork.modelChoice.explicit', '1');
// 已有会话的模型也一并改掉
const m = JSON.parse(localStorage.getItem('openwork.sessionModels.v1') || '{}');
for (const k of Object.keys(m)) m[k].model = {providerID:'minimax', modelID:'MiniMax-M3'};
localStorage.setItem('openwork.sessionModels.v1', JSON.stringify(m));
```

> **最省事**：直接在 UI 模型下拉里选一次 **MiniMax-M3**（不用 Auto）。
> 这会写 localStorage + 回写服务端，一次到位。

### 验证结果（无头 Chrome，全新会话）

```
模型区文本: MiniMax-M3        （不再是 Auto）
has_signin: NO                （没有登录界面）
提问 → 模型回答: "1+1 等于 2。"
4xx/5xx: (none)
```

---

## 2026-10-28 晚：登录页方案（彻底消灭浏览器原生 Basic 弹框）

> 何大人截图反馈：Edge 打开 session 仍弹出浏览器**原生登录框**（"登录 / 用户名 / 密码 / 取消"）。
> 上面的"导航 401 + WWW-Authenticate"方案虽然技术上正确，但**用户体验很差**：
> 原生弹框每次开 session 都弹、吞掉输入的密码、样式无法控制、Edge 上还会遮挡已渲染页面。

### 最终方案：自建 HTML 登录页

```
导航无凭据
   → nginx @openwork_denied 判定 $ow_challenge=1（document 导航）
   → rewrite ^ /_login_gate last          ← 内部重定向，浏览器 URL 不变
   → authd 渲染登录页（深色卡片）
   → 用户输密码 → POST /_login
   → authd 校验 → 下发 ow_sess cookie（30 天）→ 302 回原 URL
   → 正常加载应用
```

**关键点**：
- **不发 `WWW-Authenticate`** → 浏览器永远不会弹原生框
- **内部重定向**（`rewrite ... last`）而非 302 → 浏览器地址栏保持原 URL
- **原 URL 通过 `X-Original-URI` header 传给 authd** → 由 Python 做 URL 编码，
  避开 nginx 无法转义 `&` / `?` 的问题（`next=/ws/x?a=1&b=2` 会被截断）
- authd 下发的 `ow_sess` **就是 nginx 已经认可的那个值** → auth map 一行不用改
- XHR / 子资源被拒仍然**静默 401**（不跳登录页，否则会替换掉已渲染的页面）

### 文件与配置

| 路径 | 作用 |
|---|---|
| `/root/.openclaw/openwork-auth/authd.py` | 登录页服务（Python 标准库，无依赖） |
| `/etc/systemd/system/openwork-authd.service` | systemd 单元（127.0.0.1:8789） |
| `/etc/nginx/conf.d/openwork.conf` | 加 `/_login_gate`（internal）、`/_login`、`/_logout`、`/_health` |
| `/usr/local/bin/openwork-nginx-sync.sh` | 已改：移除 `$ow_challenge_hdr` map，注释同步更新 |

### authd 的安全设计

- 密码用 `hmac.compare_digest` 比较
- **每 IP 限流**：5 分钟内 10 次失败 → 429
- 日志**只记录**成败和 IP，**绝不记录凭据**
- session secret 从 `0600` 文件读，服务只读不写
- 跳转目标限制为**同站相对路径**（拒绝 `//evil.com`、反斜杠、控制字符）
- systemd `ProtectSystem=full` + `ProtectHome=read-only` + `BindReadOnlyPaths`

### 验证结果（无头 Chrome，全新 profile，模拟真实 Edge 流程）

```
打开 session URL      → title "OpenWork · 登录"，URL 保持不变 ✓
原生认证框            → 不存在 ✓
输入密码提交          → 302 回原 URL + ow_sess cookie (Max-Age=30d) ✓
应用加载              → 侧边栏会话列表完整，模型 MiniMax-M3 ✓
提问                  → "1+1 等于 2。" ✓
Sign in for more free use → 无 ✓
HTTP 汇总             → 200×N，401 仅 favicon.ico
```

### 认证矩阵（回归）

| 场景 | 结果 |
|---|---|
| 无凭据 + 导航（document） | 200（渲染登录页）|
| 无凭据 + 导航（带 query） | 200（登录页，next 完整保留）|
| Basic + 导航 | 200 |
| Bearer + 导航 | 200 |
| cookie + 导航 | 200 |
| cookie + 子资源（JS） | 200 |
| 无凭据 + XHR | **401 静默**（无 WWW-Authenticate）|
| `/_login` / `/_health` | 200（免认证）|
| `/_logout` | 302 → `/_login` |

### ⚠️ 运维要点

```bash
# 登录页服务状态
systemctl status openwork-authd
journalctl -u openwork-authd -n 30        # 或 /var/log/openwork-authd.log

# 自检（免认证）
curl -sk -o /dev/null -w '%{http_code}\n' https://101.35.52.96:8790/_health

# 改密码后：只需重启 authd，无需动 nginx
systemctl restart openwork-authd

# 登录页在 /_login（用户可直接访问）
```

> **别再把 `WWW-Authenticate` 加回去。**
> 那个 header 就是原生弹框的唯一触发条件。
> sync 脚本里已刻意移除 `$ow_challenge_hdr` map 并留了注释警告。

> **别只改 `openwork-auth.conf` 而不管 `openwork.conf`。**
> 登录页路由在 `openwork.conf`（手写），认证 map 在 `openwork-auth.conf`（脚本生成）。
> 两边语义要一致——上次就是"脚本覆盖配置"出的问题。

---

## 附：本次排查用到的诊断手段（复用价值高）


### 1. nginx 认证诊断日志（不含凭据原文）
`/var/log/nginx/openwork-auth.log`，字段：`ts/ip/scheme/auth/sess_cookie/dest/uri/ua`。
`dest=document` = 顶层导航（会弹框）；`dest=empty` = XHR（应静默）。

### 2. 用访问日志区分"真人"和"模拟器"
模拟脚本会从**服务器自己的 IP** 发出（`ip=101.35.52.96`），真人用户 IP 不同（`111.55.79.29`）。
**先确认真人 IP 的请求分布，再下结论**，否则会被自己的模拟数据带偏。

### 3. 看完整访问日志（不只是被拒的）
`/var/log/nginx/access.log` 有**所有**请求的状态码：
```bash
grep "111.55.79.29" /var/log/nginx/access.log | awk '{print $9}' | sort | uniq -c
# 468 200 / 10 401 → 修好后全绿
```
诊断日志只记**被拒**请求，看不到成功路径，容易误判。

### 4. 前端反查（比猜快 10 倍）
```bash
curl -sk -H "Authorization: Bearer $TOKEN" https://101.35.52.96:8790/assets/app-DZr96oX3.js -o /tmp/app.js
grep -o 'anonymous-inference/[a-z]*' /tmp/app.js | sort -u
```
压缩后的 JS 里能直接搜到端点名、i18n key、判定逻辑。

### 5. 机器资源自查（Chrome 起不来时）
```bash
free -m; df -h /; du -sh /tmp/pip-* 2>/dev/null | tail -1
```
`/tmp` 里的 pip 临时目录能堆到 2GB+，磁盘 93% → Chrome OOM。
清理：`find /tmp -maxdepth 1 -name "pip-*" -type d -exec rm -rf {} +`
（**注意**：别把 `/tmp` 本身删了，删完要 `mkdir -p /tmp && chmod 1777 /tmp` 重建）

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
