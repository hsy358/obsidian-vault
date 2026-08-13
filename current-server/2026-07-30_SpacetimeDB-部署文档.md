# SpacetimeDB 部署文档（2026-07-30）

## 一句话总结

**SpacetimeDB v2.7.0 部署成功**——单二进制数据库 + 服务器 + 反代三层架构，外网 `http://101.33.212.119:3030/` 可访问健康端点，`/v1/identity` POST 可签发 JWT。与现有 Guyu / AgentOS / Dify 完全隔离（独立端口、独立数据目录、独立 systemd unit）。

## 架构

```
笔记本 / 客户端 WebSocket
       │
       ▼ HTTP/HTTPS
┌─────────────────────────────────┐
│  nginx 8080/3030 反代           │  systemd nginx (PID 1519537)
│  listen 0.0.0.0:3030 / [::]:3030│  反代 /v1, /v1/database, /v1/identity, WS
└────────────┬────────────────────┘
             │ proxy_pass http://127.0.0.1:3003
             ▼
┌─────────────────────────────────┐
│  spacetimedb-standalone server  │  systemd spacetimedb.service
│  listen 127.0.0.1:3003          │  数据 /var/lib/spacetimedb/data
│  data-dir /var/lib/spacetimedb  │  JWT 密钥 /root/.config/spacetime/
└─────────────────────────────────┘
```

## 部署步骤

### 1. 下载官方二进制

| 项 | 值 |
|---|---|
| 版本 | v2.7.0-hotfix3 |
| 文件 | `spacetime-x86_64-unknown-linux-gnu.tar.gz` |
| 官方 sha256 | `d25c6c9e4ec5d52fe43cd7d37aaf43b9f4d4fa2d228b6ecd241ba75bdae99831` |

**下载方式**：GitHub release 直链（`https://github.com/clockworklabs/SpacetimeDB/releases/download/v2.7.0-hotfix3/spacetime-x86_64-unknown-linux-gnu.tar.gz`）在国内被严重限速（~13 KB/s）。**改走 `gh-proxy.com` 镜像**，1.9 MB/s 30 秒拉完：

```bash
curl -sSL --max-time 300 -o /tmp/spacetime-x86_64-unknown-linux-gnu.tar.gz \
  https://gh-proxy.com/https://github.com/clockworklabs/SpacetimeDB/releases/download/v2.7.0-hotfix3/spacetime-x86_64-unknown-linux-gnu.tar.gz

sha256sum /tmp/spacetime-x86_64-unknown-linux-gnu.tar.gz
# 验证: d25c6c9e4ec5d52fe43cd7d37aaf43b9f4d4fa2d228b6ecd241ba75bdae99831
```

**其它可用镜像**：`https://ghfast.top/...`（速度约 294 KB/s，比 gh-proxy 慢）。

### 2. 安装到 /usr/local/bin

```bash
cd /tmp && mkdir -p spacetime-pkg
tar -xzf spacetime-x86_64-unknown-linux-gnu.tar.gz -C spacetime-pkg

cp /tmp/spacetime-pkg/spacetimedb-cli /usr/local/bin/spacetimedb-cli
cp /tmp/spacetime-pkg/spacetimedb-standalone /usr/local/bin/spacetimedb-standalone
chmod +x /usr/local/bin/spacetimedb-cli /usr/local/bin/spacetimedb-standalone

ln -sf /usr/local/bin/spacetimedb-cli /usr/local/bin/spacetime

spacetime --version
# 期望: spacetimedb tool version 2.7.0; spacetimedb-lib version 2.7.0;
```

**包结构**：
- `spacetimedb-cli` (48 MB)：CLI 工具，提供 `spacetime start` 命令
- `spacetimedb-standalone` (133 MB)：独立服务器二进制，被 CLI 启动

### 3. 创建数据 + 日志目录

```bash
mkdir -p /var/lib/spacetimedb/data
mkdir -p /var/log/spacetimedb
```

### 4. systemd 单元（/etc/systemd/system/spacetimedb.service）

```ini
[Unit]
Description=SpacetimeDB standalone server v2.7.0
Documentation=https://spacetimedb.com/docs/
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/var/lib/spacetimedb
Environment="HOME=/root"
ExecStart=/usr/local/bin/spacetimedb-cli start \
  --listen-addr 127.0.0.1:3003 \
  --data-dir /var/lib/spacetimedb/data \
  --non-interactive
Restart=on-failure
RestartSec=5
StandardOutput=append:/var/log/spacetimedb/stdout.log
StandardError=append:/var/log/spacetimedb/stderr.log
LimitNOFILE=65535

NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=read-only
ReadWritePaths=/var/lib/spacetimedb /var/log/spacetimedb /root/.config/spacetime

[Install]
WantedBy=multi-user.target
```

**为什么 ExecStart 用 `spacetimedb-cli` 而非 `spacetimedb-standalone`**：CLI 启动时会自动查找 `~/.config/spacetime/` 里的 JWT 密钥对（`id_ecdsa` + `id_ecdsa.pub`），找不到就报错。直接用 `spacetimedb-standalone` 必须显式传 `--jwt-{pub,priv}-key-path`，部署更繁琐。

**首次启动前必须先手动跑一次 CLI**，让它生成 JWT 密钥对：

```bash
HOME=/root /usr/local/bin/spacetimedb-cli start \
  --listen-addr 127.0.0.1:3003 \
  --data-dir /var/lib/spacetimedb/data \
  --non-interactive
# 看到 "Starting SpacetimeDB listening on 127.0.0.1:3003" 后 Ctrl+C 退出
# 生成 ~/.config/spacetime/{cli.toml, id_ecdsa, id_ecdsa.pub}
```

### 5. systemd 启用 + 启动

```bash
systemctl daemon-reload
systemctl enable spacetimedb.service
systemctl start spacetimedb.service
systemctl status spacetimedb.service
# 期望: Active: active (running)
```

### 6. nginx 反代（/etc/nginx/sites-available/spacetimedb.conf）

```nginx
upstream spacetimedb_upstream {
    server 127.0.0.1:3003;
    keepalive 32;
}

server {
    listen 3030;
    listen [::]:3030;
    server_name _;

    client_max_body_size 50M;
    access_log /var/log/nginx/spacetimedb.access.log;
    error_log /var/log/nginx/spacetimedb.error.log;

    location / {
        proxy_pass http://spacetimedb_upstream;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
        chunked_transfer_encoding off;
    }
}
```

```bash
ln -sf /etc/nginx/sites-available/spacetimedb.conf /etc/nginx/sites-enabled/spacetimedb.conf
nginx -t
systemctl reload nginx
```

### 7. 端口规划

| 端口 | 监听方 | 用途 |
|---|---|---|
| `127.0.0.1:3003` | spacetimedb-standalone | 内部上游（仅本机） |
| `0.0.0.0:3030` | nginx | 对外反代（笔记本/外网） |
| `[::]:3030` | nginx | IPv6 反代 |

**端口 3003 vs 3030 的原因**：nginx `listen 3003` 默认 bind 到 `0.0.0.0:3003`，与 `127.0.0.1:3003` (spacetime server) 冲突（0.0.0.0:3003 包含 127.0.0.1:3003）。nginx error log 会反复报 `bind() to 0.0.0.0:3003 failed (98: Address already in use)`，server 静默启动失败。**改用 3030 解决**。

### 8. 验证

```bash
# 本地（直接走 spacetimedb-standalone）
curl http://127.0.0.1:3003/v1/health
# 期望: {"package_name":"spacetimedb-client-api","version":"2.7.0","nodes":[0],"schedulable":true}

# 走 nginx 反代（127.0.0.1）
curl http://127.0.0.1:3030/v1/health
# 期望同上

# 走主机内网 IP
curl http://10.1.0.13:3030/v1/health
# 期望同上

# 走外网 IP（笔记本访问入口）
curl http://101.33.212.119:3030/v1/health
# 期望同上

# 注册 identity（自动签发 JWT token）
curl -X POST http://101.33.212.119:3030/v1/identity
# 期望: {"identity":"<64-hex>","token":"eyJ..."}
```

## 端点清单

| 端点 | 方法 | 状态 | 用途 |
|---|---|---|---|
| `/` | GET | 404 | 无根路径 |
| `/v1/health` | GET | 200 ✅ | 健康检查 |
| `/v1/database` | GET/POST | 405/200 | 数据库列表 / 创建 |
| `/v1/identity` | POST | 200 ✅ | 签发 identity + JWT |
| `/v1/module` | - | 404 | 模块上传（CLI 用） |
| WebSocket `/` | - | - | 客户端实时订阅 |

## 公网访问

| 用途 | URL |
|---|---|
| 健康检查 | http://101.33.212.119:3030/v1/health |
| 注册身份 | `POST http://101.33.212.119:3030/v1/identity` |
| 客户端 SDK | `ws://101.33.212.119:3030/` |
| CLI 控制台 | `spacetime --server local publish <db> <module>` |

## 部署产物

### systemd 服务

```
/etc/systemd/system/spacetimedb.service   # service unit
/usr/local/bin/spacetimedb-cli             # CLI (spacetime → spacetimedb-cli)
/usr/local/bin/spacetimedb-standalone      # standalone server binary
```

### 数据 + 配置

```
/var/lib/spacetimedb/data/                 # 数据库 WAL + snapshot
/var/log/spacetimedb/stdout.log            # access 日志
/var/log/spacetimedb/stderr.log            # error 日志
/root/.config/spacetime/cli.toml           # CLI 配置（指向 maincloud + local）
/root/.config/spacetime/id_ecdsa           # JWT 私钥（**勿提交 git**）
/root/.config/spacetime/id_ecdsa.pub       # JWT 公钥
```

### nginx

```
/etc/nginx/sites-available/spacetimedb.conf
/etc/nginx/sites-enabled/spacetimedb.conf   # 软链
/var/log/nginx/spacetimedb.access.log
/var/log/nginx/spacetimedb.error.log
```

## 部署耗时

| 阶段 | 耗时 | 说明 |
|---|---|---|
| 下载（gh-proxy.com 镜像） | 30 秒 | GitHub 直链被限速，gh-proxy 1.9 MB/s |
| SHA256 验证 + 解压安装 | 10 秒 | 56 MB → 48 + 133 MB |
| 写 systemd + nginx 配置 | 2 分钟 | |
| JWT 密钥生成（首次 CLI 启动） | 5 秒 | 自动生成 id_ecdsa 对 |
| systemd 启用 + 启动 | 1 秒 | |
| nginx reload + 验证 | 5 秒 | |
| **总计** | **~3 分钟** | |

## 不影响现有服务（已验证）

| 现有服务 | 状态 | 验证 |
|---|---|---|
| nginx systemd | active running | PID 1519537 |
| agentos 反代 (8001) | 200 OK | `curl 127.0.0.1:8001` |
| agnos-ui 反代 (3002) | 200 OK | `curl 127.0.0.1:3002` |
| Docker 容器（19 个） | 全 Up/healthy | `docker ps` |
| MySQL 3306 / Redis 6379 / Postgres 5432 | 不变 | 端口未触碰 |
| 端口 3000（Dify+Langfuse） / 5173 / 5050 / 8443 等 | 不变 | 端口未触碰 |

## 已知限制 / 待办

| # | 项 | 影响 | 解决方案 |
|---|---|---|---|
| 1 | 数据未持久化测试 | restart 后数据保留需要 `--data-dir` 持久目录，已配 | 当前重启测试已确认 |
| 2 | 未发布模块 | 服务器在跑但无业务数据库 | `spacetime publish` 或用 `spacetime dev --template chat-react-ts` 起 demo |
| 3 | JWT 密钥未备份 | 重装系统会丢所有 identity 映射 | 备份 `/root/.config/spacetime/id_ecdsa*` 到 vault |
| 4 | SSL 未配置 | 笔记本直连 HTTP（无 TLS） | nginx 加 `listen 443 ssl` + Let's Encrypt；当前 HTTP 即可用 |
| 5 | 日志未轮转 | stdout/stderr.log 会无限增长 | 加 `/etc/logrotate.d/spacetimedb` |
| 6 | 防火墙入站规则 | 3030 端口对外 | 确认腾讯云安全组已放行 3030（已测 101.33.212.119:3030 通） |
| 7 | v2.7 MCP server 端点 | 文档：`POST /v1/database/:name/mcp` | 待发布数据库后验证 |

## 路径硬规则（给未来的我）

- ✅ 二进制位置：`/usr/local/bin/spacetimedb-{cli,standalone}`（CLI 别名 `spacetime`）
- ✅ 数据目录：`/var/lib/spacetimedb/data`
- ✅ 日志：`/var/log/spacetimedb/{stdout,stderr}.log`
- ✅ JWT 密钥：`/root/.config/spacetime/id_ecdsa{,.pub}`（**勿 commit**）
- ✅ 公网入口：`http://101.33.212.119:3030/`
- ✅ systemd 启停：`systemctl {start,stop,restart,status} spacetimedb`
- ✅ reload 配置：`systemctl reload spacetimedb`（不丢连接）
- ❌ 不要手动 `kill` spacetimedb-standalone 进程（systemd 会自动拉起）
- ❌ 不要把端口改成 3003（与 spacetime server 冲突）
- ❌ 不要用 `spacetimedb-standalone` 直接 ExecStart（需手动 JWT 路径，更繁琐）

## 教训总结

1. **GitHub release 直链被限速**——这台机对 `release-assets.githubusercontent.com` 几乎拿不到速度。**走 `gh-proxy.com` 镜像**（已写入避坑）：`curl https://gh-proxy.com/https://github.com/...`。
2. **nginx `listen 3003` 默认 bind 0.0.0.0:3003** —— 与同一端口的 `127.0.0.1:3003` 冲突（0.0.0.0 包含 127.0.0.1）。**对外端口和上游端口必须分开**（这里用 3030 对外 / 3003 内）。
3. **`spacetimedb-standalone` 需要显式 JWT 路径** —— 用 `spacetimedb-cli start` 让 CLI 自动管理密钥对（写在 `~/.config/spacetime/`）。
4. **nginx reload 用 `systemctl reload nginx`，不要 `nginx -s reload`** —— 这台机有 supervisord 起的 daemon-off nginx，`nginx -s reload` 可能发给错的进程。
5. **server 块必须有 `location /` + `proxy_pass`** —— 只有 server-level `proxy_set_header` 不会反代，会返回 nginx 默认 404。