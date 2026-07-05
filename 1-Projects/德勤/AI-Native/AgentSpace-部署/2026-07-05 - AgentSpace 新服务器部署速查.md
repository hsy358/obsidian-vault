---
title: AgentSpace 新服务器部署速查（命令化）
date: 2026-07-05
type: deployment-cheatsheet
status: ✅ 已验证
deploy_path: /root/AgentSpace
web_port: 1455
purpose: 给新服务器用 — 直接复制粘贴命令，25 分钟跑通
related:
  - 2026-07-02 - AgentSpace 本地部署与体验 SOP.md
  - 2026-07-05 - AgentSpace 部署踩坑与修复全集（归档版）.md
---

# 🛠 AgentSpace 新服务器部署速查

> **作者**：小助（OpenClaw / MiniMax-M3）
> **写于**：2026-07-05
> **验证环境**：腾讯云 Ubuntu 24.04 / 2 vCPU / 3.6 GiB / Node 22.22.2
> **目标**：在新服务器 25 分钟内跑通 AgentSpace Web + PostgreSQL + CLI

---

## 📋 部署前检查清单

```bash
# 1. 系统版本（要求 Ubuntu 22.04+）
cat /etc/os-release | head -3

# 2. Node 版本（要求 v22.19+，OpenClaw 硬要求）
node --version

# 3. 磁盘可用空间（要求 ≥10 GiB）
df -h / | tail -1

# 4. 内存可用（要求 ≥2 GiB，建议 ≥4 GiB）
free -h | head -2

# 5. 公网 IP（部署后给客户访问用）
curl -s ifconfig.me

# 6. 公网端口（需提前在云厂商安全组放通 1455）
ss -tlnp | grep 1455 || echo "1455 端口未监听"
```

**如果任何一项不达标，先解决再继续。**

---

## 🚀 部署 9 步走（每步独立可验证）

### Step 1：装 Docker Compose v2

```bash
apt-get install -y docker-compose-v2
mkdir -p ~/.docker/cli-plugins
cp /usr/libexec/docker/cli-plugins/docker-compose ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose
docker compose version   # 期望 v2.40.3
```

> ⚠️ **坑**：必须 `cp` 不能 `ln -s`（会报 `Text file busy`）

### Step 2：下载 AgentSpace 源码

```bash
cd /root
curl -fL --connect-timeout 15 --max-time 300 \
  -o AgentSpace.tar.gz \
  https://codeload.github.com/HKUDS/AgentSpace/tar.gz/refs/heads/main
tar -xzf AgentSpace.tar.gz
mv AgentSpace-main AgentSpace
rm AgentSpace.tar.gz
```

> ⚠️ **坑**：**不要用 `git clone`**，会卡死。codeload tarball 14 秒搞定。

### Step 3：配置 .env

```bash
cd /root/AgentSpace
npm config set registry https://registry.npmmirror.com

ENCRYPTION_KEY=$(node -e "console.log(require('crypto').randomBytes(32).toString('base64'))")
OAUTH_SECRET=$(node -e "console.log(require('crypto').randomBytes(32).toString('hex'))")

cp .env.example .env
sed -i "s|NEXT_SERVER_ACTIONS_ENCRYPTION_KEY=replace_with_base64_encoded_32_byte_key|NEXT_SERVER_ACTIONS_ENCRYPTION_KEY=$ENCRYPTION_KEY|" .env
sed -i "s|AGENT_SPACE_OAUTH_STATE_SECRET=replace_with_a_long_random_hex_string|AGENT_SPACE_OAUTH_STATE_SECRET=$OAUTH_SECRET|" .env
sed -i "s|AGENT_SPACE_GOOGLE_WORKSPACE_TOKEN_ENCRYPTION_KEY=replace_with_base64_encoded_32_byte_key|AGENT_SPACE_GOOGLE_WORKSPACE_TOKEN_ENCRYPTION_KEY=$ENCRYPTION_KEY|" .env

mkdir -p /var/lib/agentspace/workspaces
```

**手动改** `.env` 里的 `AGENT_SPACE_APP_URL`：
```bash
# 把内网 IP 换成公网 IP
sed -i "s|AGENT_SPACE_APP_URL=http://127.0.0.1:1455|AGENT_SPACE_APP_URL=http://<你的公网IP>:1455|" .env
```

### Step 4：装依赖

```bash
cd /root/AgentSpace
npm run setup   # ~20-60 秒，376 个包，730 MB
```

### Step 5：build daemon（**关键，不 build CLI 起不来**）

```bash
cd /root/AgentSpace/packages/daemon
npm run build
```

### Step 6：起 PostgreSQL

```bash
cd /root/AgentSpace
docker compose -f deploy/postgres/docker-compose.yml up -d
sleep 3
docker compose -f deploy/postgres/docker-compose.yml ps
```

### Step 7：初始化数据库

```bash
cd /root/AgentSpace
npm run db:pg:init
```

### Step 8：起 Web

```bash
cd /root/AgentSpace
nohup npm run dev:web > /tmp/agentspace-web.log 2>&1 &
sleep 8
```

### Step 9：验证 3 项

```bash
# 验证 1：Web 200 OK
curl -sI http://127.0.0.1:1455/ | head -1
# 期望: HTTP/1.1 200 OK

# 验证 2：CLI doctor 8/8
cd /root/AgentSpace && npm run cli -- doctor

# 验证 3：workspace status
cd /root/AgentSpace && npm run cli -- workspace status
```

**9 步全部通过 = 部署完成**。

---

## 🔧 OpenClaw 子进程修复（新服务器必跑）

AgentRouter → OpenClaw 链路如果跑不通，需要这步：

### 修复 1：wrapper 用绝对路径

```bash
cp /usr/local/bin/openclaw /usr/local/bin/openclaw.bak

cat > /usr/local/bin/openclaw <<'EOF'
#!/bin/sh
export NVM_DIR="/root/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
export PNPM_HOME="/root/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"
exec "/root/.local/share/pnpm/openclaw" "$@"
EOF
chmod +x /usr/local/bin/openclaw
```

### 修复 2：pnpm sh 脚本头部注入 nvm（**关键**）

```bash
cp /root/.local/share/pnpm/openclaw /root/.local/share/pnpm/openclaw.bak

cat > /root/.local/share/pnpm/openclaw <<'EOF'
#!/bin/sh
export NVM_DIR="/root/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
EOF

cat /root/.local/share/pnpm/openclaw.bak >> /root/.local/share/pnpm/openclaw
chmod +x /root/.local/share/pnpm/openclaw
```

### 防覆盖补丁脚本

```bash
cat > /root/bin/openclaw-patch.sh <<'EOF'
#!/bin/bash
PnpmSh="/root/.local/share/pnpm/openclaw"
if ! head -3 "$PnpmSh" | grep -q "nvm 加载"; then
    cp "$PnpmSh" "$PnpmSh.bak"
    cat > "$PnpmSh" <<'INNER'
#!/bin/sh
export NVM_DIR="/root/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
INNER
    cat "$PnpmSh.bak" >> "$PnpmSh"
    chmod +x "$PnpmSh"
    echo "[$(date)] openclaw pnpm sh 脚本已重新注入 nvm 加载"
fi
EOF
chmod +x /root/bin/openclaw-patch.sh

# 加到 crontab（每天凌晨 3 点检查一次，pnpm 升级后自动修复）
(crontab -l 2>/dev/null; echo "0 3 * * * /root/bin/openclaw-patch.sh") | crontab -
```

### 验证 AgentRouter 链路

```bash
cd /root/AgentSpace
./packages/daemon/bin/agent-router.js run \
    --harness openclaw \
    --cwd /root/AgentSpace \
    --mode medium \
    --session-id test-fix \
    "用一句话介绍 HKUDS/AgentSpace"

# 期望：最后 "exitCode": 0
```

---

## 🔁 启动 / 停止 / 重启 速查

### 启动（重启后）

```bash
cd /root/AgentSpace
docker compose -f deploy/postgres/docker-compose.yml up -d
sleep 3
nohup npm run dev:web > /tmp/agentspace-web.log 2>&1 &
sleep 5
curl -sI http://127.0.0.1:1455/ | head -1
```

### 停止（保留数据）

```bash
pkill -f "next dev --hostname 0.0.0.0 --port 1455"
pkill -f "node.*AgentSpace/apps/web"
cd /root/AgentSpace && docker compose -f deploy/postgres/docker-compose.yml stop
```

### 完全卸载

```bash
cd /root/AgentSpace
docker compose -f deploy/postgres/docker-compose.yml down -v
rm -rf /root/AgentSpace /var/lib/agentspace
```

---

## ⚠️ 上线前必做（投产 blocker）

1. **HTTPS**：nginx 反代 1455 + Let's Encrypt / 自签证书（**当前 HTTP 密码明文**）
2. **公网安全组**：确认云厂商已放通 1455 入站
3. **密码安全**：等 AgentSpace 项目侧加 bcrypt（当前是明文提交）
4. **内存监控**：3.6 GiB 跑 PG + Web 会触发 swap，建议加 swap 监控

---

## 📊 资源占用参考

| 组件 | 磁盘 | 内存 |
|---|---|---|
| AgentSpace 目录 | 730 MB | - |
| PostgreSQL 16（容器）| ~200 MB | ~200 MB |
| Next.js dev | - | ~500 MB |
| **合计** | **~1 GB** | **~700 MB** |

最低配置：**2 vCPU / 4 GiB 内存 / 20 GiB 磁盘**

---

## 🆘 故障排查速查

| 症状 | 看这个 |
|---|---|
| `docker compose: command not found` | 重跑 Step 1 |
| `git clone` 卡死 | 重跑 Step 2（用 codeload）|
| `Cannot find module 'agent-space-daemon/dist/index.js'` | 重跑 Step 5（漏 build）|
| Web 起不来 | `tail -50 /tmp/agentspace-web.log` |
| CLI doctor 失败 | `npm run cli -- doctor` 看具体哪项 |
| AgentRouter exitCode=1 | 重跑 §OpenClaw 子进程修复 |
| 公网访问 502 | 检查安全组 1455 端口 + nginx/防火墙 |
| 公网访问"不安全" | HTTP 是预期，**上 HTTPS 前不要给客户看** |

---

## 📁 部署完交付的产物

新服务器部署完后，请把以下信息反馈给何大人：

```bash
# 跑这个脚本，自动收集部署信息
cat > /tmp/collect-info.sh <<'EOF'
echo "=== 公网 IP ==="
curl -s ifconfig.me
echo ""
echo "=== Node 版本 ==="
node --version
echo ""
echo "=== AgentSpace 版本 ==="
cd /root/AgentSpace && git log -1 --oneline 2>/dev/null || echo "无 git（tarball 安装）"
echo ""
echo "=== Web 状态 ==="
curl -sI http://127.0.0.1:1455/ | head -1
echo ""
echo "=== CLI doctor ==="
npm run cli -- doctor 2>&1 | tail -5
echo ""
echo "=== 进程 ==="
ps aux | grep -E "next|node.*AgentSpace|postgres" | grep -v grep | awk '{print $11, $12, $13}'
EOF
chmod +x /tmp/collect-info.sh && /tmp/collect-info.sh
```

---

## 📚 关联文档（不熟时翻这里）

- 📖 完整踩坑归档：`2026-07-05 - AgentSpace 部署踩坑与修复全集（归档版）.md`
- 📖 原部署 SOP：`2026-07-02 - AgentSpace 本地部署与体验 SOP.md`
- 📖 OpenClaw 修复细节：`2026-07-02 - OpenClaw 子进程 Node 版本修复.md`
- 📖 登录页安全审计：`截图/2026-07-04_img_AgentSpace登录页_首次访问.md`

---

**作者**：小助 — OpenClaw (MiniMax-M3) — 2026-07-05
**预期部署耗时**：25 分钟（含首次踩坑）
**预期重复部署耗时**：10 分钟（按本文档命令粘贴即可）