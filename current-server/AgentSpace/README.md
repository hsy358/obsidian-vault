---
title: AgentSpace 部署手册 + 避坑指南
date: 2026-07-06
type: deployment-handbook
status: active
service: AgentSpace
port: 1455
public_url: http://101.33.212.119:1455
deploy_path: /root/projects/AgentSpace
---

# 🟪 AgentSpace 部署手册 + 避坑指南

> **一句话**：自托管 Agent 编排平台（Next.js + 多 harness 路由）。架构上统一接入 Claude / Codex / OpenClaw / Hermes / OpenCode 五种 Agent 引擎。

---

## 1. 项目信息

| 项 | 值 |
|---|---|
| 用途 | 多 Agent 编排 / Harness 路由 / 执行器抽象层 |
| 技术栈 | Next.js 15 + Node 22 + React 19 + Tailwind 4 |
| 公网 URL | `http://101.33.212.119:1455` |
| 状态 | ✅ 200 OK（10h+ 稳定运行）|
| 部署位置 | `/root/projects/AgentSpace/` |

---

## 2. 硬件依赖

| 项 | 最低 | 当前服务器 |
|---|---|---|
| CPU | 2 核 | 8 核 ✅ |
| RAM | 4 GB | 30 GB ✅ |
| Disk | 30 GB | 315 GB ✅ |
| Node | 22.x | 22.23.1 ✅ |
| 包管理器 | pnpm 11 | 已装 |

---

## 3. 一键部署（从 0 到 1）

```bash
# 1. 拉代码
mkdir -p /root/projects && cd /root/projects
git clone https://github.com/HsiYan/AgentSpace.git
cd AgentSpace

# 2. 装依赖（pnpm workspaces monorepo）
pnpm install

# 3. 启 daemon（AgentRouter 核心）
cd packages/daemon
npm run build
./bin/agent-router.js detect
# 期望：5/5 harness 全部识别（claude / codex / openclaw / hermes / opencode）

# 4. 启 Next.js
cd ../..
pnpm dev --port 1455
# 或 build + start
pnpm build
pnpm start --port 1455
```

---

## 4. 配置（关键文件）

```bash
# /root/projects/AgentSpace/packages/daemon/config.json
{
  "agents": {
    "claude": { "bin": "claude", "args": [...] },
    "codex": { "bin": "codex", "args": [...] },
    "openclaw": { "bin": "openclaw", "args": [...] },
    "hermes": { "bin": "hermes", "args": [...] },
    "opencode": { "bin": "opencode", "args": [...] }
  },
  "router": { "strategy": "round-robin", "fallback": true }
}

# /root/projects/AgentSpace/.env.local
NEXT_PUBLIC_API_URL=http://101.33.212.119:1455
NODE_ENV=production
```

---

## 5. 启动命令（systemd 永久 service）

⚠️ **不要用 `nohup pnpm &`**！SSH session 注销时 systemd 会 kill 子进程（2026-07-06 教训）。

**正确方式**：用 systemd user service 管理。

```bash
# 1. 写 service file
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/agentspace.service << 'EOF'
[Unit]
Description=AgentSpace Next.js dev server
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/projects/AgentSpace
Environment="NVM_DIR=/root/.nvm"
ExecStart=/bin/bash -c 'export NVM_DIR=/root/.nvm && . $NVM_DIR/nvm.sh && cd /root/projects/AgentSpace && exec npm run dev:web'
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

# 2. enable + start
systemctl --user daemon-reload
systemctl --user enable agentspace.service
systemctl --user start agentspace.service

# 3. 验证
systemctl --user status agentspace.service
ss -tlnp | grep 1455
curl -sI http://localhost:1455
```

**临时启动**（dev 用，不推荐）：
```bash
cd /root/projects/AgentSpace
# 只用 dev 模式 (npm run dev:web)
nohup npm run dev:web > /tmp/agentspace.log 2>&1 &
```

**看日志**：
```bash
journalctl --user -u agentspace.service -f
```

---

## 6. 三维度验证

```bash
# 本地
curl -sI http://localhost:1455
# 公网
curl -sI http://101.33.212.119:1455
# AgentRouter
./packages/daemon/bin/agent-router.js detect
# 期望：5/5 harness identified
# 云端
# web_fetch http://101.33.212.119:1455
```

---

## 7. ⚠️ 避坑指南（按时间倒序）

### 坑 6: SSH session 注销杀进程（2026-07-06 实测）
- **现象**: AgentSpace 进程在 7-6 01:56 之后无了，查 ss 看不到 1455 端口
- **根因**: 之前用 `nohup npm run dev:web &` 启，root 在 `pts/4` 注销时 systemd 把 cgroup 里所有进程 kill
- **修法**: 用 `systemd-run --user` 或写 `~/.config/systemd/user/agentspace.service`（Type=simple, Restart=always）
- **永久规则**: ✅ **任何用户态服务必须用 systemd 管生命周期**，不要 `nohup &`

### 坑 1: OpenClaw 子进程 Node 版本错乱
- **现象**: agent-router detect 调用 OpenClaw 时报 `node: command not found` 或版本错
- **根因**: daemon 子进程的 `$HOME` 或 `$PATH` 缺失（nvm 不加载）
- **修法**: `/root/.local/share/pnpm/openclaw` 头部注入 nvm 加载：
```bash
#!/bin/bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
exec /root/.local/share/pnpm/store/v11/links/@/openclaw/.../openclaw "$@"
```
- **永久规则**: ✅ **daemon spawn 子进程必须显式加载 nvm/PATH**
- 详见：`/root/vault/1-Projects/德勤/AI-Native/AgentSpace-部署/2026-07-02 - OpenClaw 子进程 Node 版本修复.md`

### 坑 2: pnpm workspaces 链接错乱
- **现象**: `pnpm install` 报 `ELSPROBLEMS` 或包找不到
- **根因**: pnpm 11 + workspaces 配置（`packages/daemon` 是独立 package）
- **修法**: 用 pnpm workspaces 自动 link；不要手动 yarn install
- **永久规则**: ✅ **monorepo 项目用 pnpm workspaces，不要混用 npm/yarn**

### 坑 3: 端口 1455 不在腾讯云 NAT EIP 默认放通列表
- **现象**: 公网 curl 失败，本地 curl 通
- **根因**: 腾讯云轻量服务器 NAT 模式，部分高端口默认不放通
- **修法**: 在腾讯云控制台 → 防火墙 → 添加规则：1455/TCP 0.0.0.0/0
- **永久规则**: ✅ **新部署先看腾讯云防火墙是否放通端口**

### 坑 4: AgentRouter harness 识别不全
- **现象**: `./bin/agent-router.js detect` 报告 4/5 或 3/5 harness
- **根因**: 某个 harness 二进制不在 PATH（如 hermes 需要 `which hermes`）
- **修法**: 把缺失的 harness 二进制 symlink 到 /usr/local/bin 或 PATH 包含目录
- **永久规则**: ✅ **AgentRouter 部署后必跑 detect 验证 5/5**

---

## 8. 当前状态（2026-07-06 20:08）

| 服务 | 状态 |
|---|---|
| Next.js server | ✅ http://101.33.212.119:1455 |
| AgentRouter daemon | ✅ 5/5 harness identified |

---

## 9. 关联文档

- `/root/vault/1-Projects/德勤/AI-Native/AgentSpace-部署/`
- MEMORY.md "AgentSpace 部署 + AgentRouter 验证（2026-07-02）"