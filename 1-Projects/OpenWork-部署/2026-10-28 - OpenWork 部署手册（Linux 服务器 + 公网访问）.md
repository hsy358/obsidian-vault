---
title: "OpenWork 部署手册（Linux 服务器 + 公网访问）"
source: self
url: https://github.com/different-ai/openwork
saved_date: 2026-10-28
tags: ["OpenWork", "部署", "Linux", "systemd", "nginx", "Node24"]
description: "2026-10-28 在 101.35.52.96 部署 OpenWork Server web 模式的完整过程、踩坑与配置"
---

# OpenWork 部署手册

> 2026-10-28 实测部署。服务器：101.35.52.96（Ubuntu 24.04 / 2C3G / 59G 盘）

## 部署结果

| 项 | 值 |
|---|---|
| 服务地址 | `http://101.35.52.96:8790` |
| 门禁 | HTTP Basic Auth（用户 `openwork`） |
| 密码 | `/root/.openwork_web_password`（已生成，14 位随机） |
| 版本 | openwork-server 0.18.63（OpenCode 期望 1.18.33，实际跑 1.19.4） |
| 托管 | systemd `openwork-server.service`，开机自启 + 自动重启 |
| 内部监听 | 127.0.0.1:8788（仅本地） |
| 状态 | ✅ 运行中，端点全部 200 |

**已验证端点**：`/` `/health` `/status` `/capabilities` `/workspaces` `/workspace/:id/skills` `/workspace/:id/plugins` `/experimental/connect/skills` 全部 200，SSE `/workspace/:id/events` 正常。

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

## 认证 token 在哪

- app client token / host token：`~/.openwork/openwork-server/web-tokens.json`（0600）
- app 自身配置：`~/.config/openwork/server.json`
- Basic Auth 口令：`/root/.openwork_web_password`（0600），哈希在 `/etc/nginx/.openwork_auth`（0644，给 nginx worker 读）

## 运维命令

```bash
systemctl status openwork-server
systemctl restart openwork-server
tail -f /var/log/openwork-server.log
curl -s -u "openwork:$(cat /root/.openwork_web_password)" http://101.35.52.96:8790/health
```

## 还没做的

- [ ] 未配模型（需要 API key 才能真正跑 agent）
- [ ] 未配工作区（当前只有一个 demo 目录 `/root/openwork-workspace/demo`）
- [ ] 未上 HTTPS（公网明文 HTTP + Basic Auth，密码会裸奔）
- [ ] 未审遥测（`ee/packages/telemetry`、`den-diagnostics` 存在，虽然本地部署没走 Den）
- [ ] 未接 OpenWork MCP 到 OpenClaw（`https://api.openworklabs.com/mcp/agent` 需要 OpenWork 账号）

## 备注

- 桌面 App（Electron，300MB+）**没装**——服务器无桌面环境，装了没意义
- 只部署了 server 模式；OpenWork Den（企业控制面）需要 MySQL + Redis，本次未部署
