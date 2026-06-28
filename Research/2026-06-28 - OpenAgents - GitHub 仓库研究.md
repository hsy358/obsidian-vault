---
type: research-report
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: openclaw-2026-06-28
title: OpenAgents — GitHub 仓库研究
description: 1. Project Overview 2. Core Concepts 3. Supported Agents 4. Architecture 5. CLI Workflow 6. Comparison 7. Strengths & Limitations
tags:
- AI
- Agent
- Multi-Agent
- Collaboration
- Workspace
- OpenSource
- Apache-2.0
source:
  url: https://github.com/openagents-org/openagents
  fetched: 2026-06-28T10:50+08:00
  by: 小助 via web_fetch
---

# OpenAgents — GitHub 仓库研究

**Date:** 2026-06-28  
**Prepared for:** 何大人 · Internal Research  
**Sources:** https://github.com/openagents-org/openagents · https://openagents.org/

---

## 1. Project Overview

**OpenAgents**（`openagents-org/openagents`）是一个 **Apache 2.0 开源的 AI Agent 协作平台**。口号是 **"AI Agent Networks for Open Collaboration"**，核心理念可概括为 **"Slack for Agents"**。

### 痛点

> "Your agents are everywhere. One maintains your database on a server. Another manages your marketing and replies to users on Discord. A few more are building different projects in separate terminals, on separate machines. You have no single place to see them all, and no way to make them work together."

具体场景：用户报告 bug → marketing bot 收集信息 → 拉 infra agent 进同一对话 → 调试日志 → 协同修复。**今天是复制粘贴 + SSH 跨机 + 手工拼上下文**。

### 解法（两个核心 idea）

1. **统一 Workspace** — 一个 URL 接入所有 agent（无论跑在哪里），可在浏览器/手机看所有 agent 在干什么
2. **Agent 间协作** — 任意 agent 拉进同一会话线程，共享文件 / 浏览器 / 上下文，**无胶水代码**

### License & 立场

- **Apache 2.0** 全开源
- 明确反 vendor lock-in
- 无强制账号

---

## 2. Core Concepts

### 2.1 Workspace（持久化 hub）

- 类 Slack，但 for agents
- 任何支持的 agent 都能接入
- 共享 **threads / files / browser**
- 永久 URL：`workspace.openagents.org/abc123`

### 2.2 Agent（被托管的客户端）

| 维度 | 能力 |
|---|---|
| **接入方式** | CLI 一行命令 `agn connect <name> <token>` |
| **身份** | 每个 agent 一个 name + workspace token |
| **配置** | `agn env <agent> --set KEY=VAL` 注入环境变量 |
| **生命周期** | 后台 daemon（`agn up` 启动） |

### 2.3 协作原语

- **@mention**：线程中 @ 某个 agent，它会被拉入上下文
- **共享文件**：agent 上传代码/文档/报告 → workspace → 其他 agent 或人可读/写/下载
- **共享浏览器**：agent 打开网页、点击、截图、填表，**所有 workspace 成员可见**
- **Tunnels**：`agn tunnel` 一行把本地 dev server 暴露成公网 URL，agent 写完前端可立刻预览

---

## 3. Supported Agents

### 3.1 完整支持矩阵

| Agent | 状态 | 说明 |
|---|---|---|
| **OpenClaw** | ✅ Supported | 开源，**任意 LLM 后端**（这正是当前会话的 runtime） |
| **Claude Code** | ✅ Supported | Anthropic 官方 coding agent |
| **Codex CLI** | ✅ Supported | OpenAI 官方 coding agent |
| **Hermes Agent** | ✅ Supported | Nous Hermes CLI，含 tools / profiles / memory |
| **Cursor** | ✅ Supported | AI code editor |
| **OpenCode** | ✅ Supported | 开源 terminal agent |
| **GitHub Copilot CLI** | ✅ Supported | GitHub 官方 copilot |
| **Gemini CLI** | ✅ Supported | Google 开源 CLI agent |
| **Cline** | ✅ Supported (Beta) | 自主 coding agent CLI |
| **Amp** | ✅ Supported | Sourcegraph 的 coding agent（CLI execute mode） |
| **Aider** | 🧪 Beta | AI pair programming（多 provider，离线测试通过，真实 E2E 待补） |
| **Goose** | 🧪 Beta | Block 开源 agent（CLI headless，需 ≥ v1.37.0） |

### 3.2 关键观察

- **OpenClaw 是头号 Supported**（在支持列表第一行）→ 推测项目作者本身可能就是 OpenClaw 用户 / 社区贡献者
- **多 provider 抽象**：所有 agent 都通过 `LLM_API_KEY` + `LLM_BASE_URL` 注入，支持自托管 / 代理 / 本地模型
- **Goose / Aider 还在 Beta**：离线单测都过，但真实模型 provider 的 E2E 未跑通——这是一个**严肃项目**，不会把没测的东西标 Supported

---

## 4. Architecture（从公开信息推测）

### 4.1 三层架构

```
┌─────────────────────────────────────────┐
│  Workspace Frontend (openagents.org)    │  ← SaaS / Self-host
│  - Web UI (浏览器)                      │
│  - Mobile (URL 接入)                    │
└──────────────┬──────────────────────────┘
               │ HTTPS / WebSocket
┌──────────────┴──────────────────────────┐
│  Workspace Backend (openagents.org)     │  ← 协同服务器
│  - Threads                             │
│  - File store                          │
│  - Shared browser (likely Playwright)  │
│  - Tunnel endpoint                     │
└──────────────┬──────────────────────────┘
               │ agn 协议（CLI daemon 长连接）
┌──────────────┴──────────────────────────┐
│  Agent Runtime (本地 / 云端 / 跨机)     │
│  - agn daemon（每台机器一个）           │
│  - OpenClaw / Claude Code / Aider ...   │
└─────────────────────────────────────────┘
```

### 4.2 CLI 工具链

```bash
# 1. 安装 launcher
curl -fsSL https://openagents.org/install.sh | bash   # macOS/Linux
irm https://openagents.org/install.ps1 | iex           # Windows

# 2. 安装 runtime（按 agent 类型）
agn install openclaw        # OpenClaw runtime
agn install aider           # Aider CLI
agn install goose           # Goose CLI（>v1.37.0）

# 3. 创建 agent 实例
agn create my-agent --type openclaw
agn create my-aider --type aider --path ~/code

# 4. 配置凭据
agn env openclaw --set LLM_API_KEY=sk-...
agn env aider --set AIDER_PROVIDER=anthropic \
              --set AIDER_MODEL=sonnet \
              --set LLM_API_KEY=sk-ant-...

# 5. 启动 daemon + 接入 workspace
agn up                       # 启动本地 daemon
agn connect my-agent <workspace-token>
```

### 4.3 配置文件（推测 ~/.openagents/）

```
~/.openagents/
├── daemon.log               # 守护进程日志
├── sessions/                # 各 agent 会话历史
│   └── aider/               # Aider 专用（per-channel chat history）
└── agents/                  # agent 配置 + 环境变量
```

---

## 5. CLI Workflow 详解（以 OpenClaw 为例）

### 5.1 安装 OpenClaw runtime

```bash
agn install openclaw
agn create my-agent --type openclaw      # 写入配置
agn env openclaw --set LLM_API_KEY=sk-...
agn up                                   # 启动 daemon
agn connect my-agent <workspace-token>  # 接入 workspace
```

### 5.2 几个关键设计

- **`agn create` 只写配置，不装 runtime**——分离 create / install（除非加 `--install`）
- **凭据只走环境变量**（不入 argv / 不入日志）→ 安全基线好
- **daemon 模式** → agent 一直在线，workspace 有任务即响应
- **Provider 兼容**：OpenAI / Anthropic / OpenRouter / Gemini / DeepSeek / OpenAI-compatible + 本地 Ollama

---

## 6. 与已有工具的对比

### 6.1 与类似项目

| 项目 | 定位 | 与 OpenAgents 区别 |
|---|---|---|
| **OpenHands** | 单 agent 自主编码 | OpenAgents 是**多 agent 协作层**，不替代单 agent |
| **Goose** | Block 出品的 coding agent | Goose 是**被托管的客户端之一**，OpenAgents 是 hosting 层 |
| **Aider** | Terminal pair programming | 同上，被接入者 |
| **Hermes** | Nous 出品的 CLI agent | 同上 |
| **Claude Code / Codex / Cursor** | 厂商 coding agent | 同上 |

**OpenAgents 的护城河**：**中立的多 agent 协作层**——不被某家 LLM 或某家 agent 厂商绑定。

### 6.2 与 OpenClaw 现状的关系

当前 OpenClaw（`~/.openclaw/workspace/`）是一套**单 agent 工作台**（memory + skills + protocols + tools）。OpenAgents 是 OpenClaw 的**上层协作层**：

```
OpenAgents (workspace 协作)
   ↓ 接入
OpenClaw / Claude Code / Codex / Aider / Goose ...
   ↓ 各 agent 自己的 runtime
LLM API / 本地模型 / 文件系统 / shell
```

**何大人的环境天然兼容**——OpenClaw 已经在 Supported 列表第一位。

---

## 7. Strengths, Weaknesses & Known Limitations

### ✅ 强项

1. **真开源 + 协议中立**：Apache 2.0，不绑 LLM，不绑 agent
2. **覆盖广**：12 个主流 agent 全部支持（含所有 coding agent 巨头）
3. **设计用心**：Beta 不当 Supported 标——测试纪律严
4. **共享浏览器**：独此一家——其他协作平台做不到
5. **Tunnels**：一键预览 agent 写的本地前端
6. **OpenClaw 友好**：头号支持对象，零摩擦接入

### ⚠️ 弱项 / 风险

1. **Beta 比例高**：12 个 agent 里 3 个 Beta（Aider / Goose / Cline），真实 E2E 待补
2. **云端依赖**：核心服务在 `openagents.org`，**自托管方案不明确**（README 没提 self-host 路径）
3. **新兴项目**：仓库开发活跃度、生态规模待观察
4. **共享浏览器的隔离性**：多人共享浏览器会话，安全边界需用户自觉
5. **Tunnel 安全**：暴露本地端口到公网，敏感开发环境需谨慎

### ❓ 待观察

- 背后团队 / 公司 / 资金来源（README 无任何公司信息）
- 商业模式（云服务收费？纯社区？）
- 与 AAIF（Linux Foundation 下 AI Agent 基金会）的关系（看到 Goose 在 AAIF）

---

## 8. 对何大人的潜在价值

### 🎯 直接相关

| 场景 | 价值 |
|---|---|
| **多 agent 协同开发** | 当前 OpenClaw 是单 agent 工作台 → OpenAgents 可升级到多 agent 协作 |
| **远程调试 / 部署** | agent 跑在服务器 / 笔记本 / 多个云 → 统一 workspace 查看 |
| **agent 之间的接力** | 例：让 Claude Code 写代码 → Aider 优化 → Goose 写测试，全程在一个 thread |
| **共享浏览器调试** | agent 抓取截图、填表、点网页，全过程可视化（其他平台做不到） |

### 🚀 可能的下一步

1. **试用 OpenClaw 接入 OpenAgents** —— 既然 OpenClaw 是头号支持，配置应该是最简的
2. **关注 Aider / Goose Beta** —— 想用 Aider 写 pair programming，可以一起测 E2E
3. **研究 self-host 路径** —— 如果担心 openagents.org 跑路，自托管方案要不要弄一份

---

## 9. Quick Reference

| 项目 | 信息 |
|---|---|
| **GitHub** | https://github.com/openagents-org/openagents |
| **官网** | https://openagents.org/ |
| **License** | Apache 2.0 |
| **CLI 工具** | `agn`（launcher + daemon + connector） |
| **支持 agents** | 9 ✅ + 3 🧪 Beta |
| **核心特性** | Workspace 协作 / 共享文件 / 共享浏览器 / Tunnels |
| **安装** | `curl -fsSL https://openagents.org/install.sh | bash` |

---

**研究完成。** 本文档已存档到 vault：`/root/vault/Research/2026-06-28 - OpenAgents - GitHub 仓库研究.md`

何大人要看哪部分深挖？要不要我顺手做个"OpenAgents 接入 OpenClaw" 的实操笔记？