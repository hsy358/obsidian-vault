---
type: research-report
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: openclaw-2026-06-28
title: AgentSpace — GitHub 仓库研究
description: 1. Project Overview 2. Official Description 3. Core Functions 4. Technical Architecture 5. Comparison with Deloitte Solution 6. Deployment 7. Recommendations 8. References
tags:
- AI
- Agent
- Multi-Agent
- Collaboration
- Workspace
- Enterprise
- AgentRouter
- HKUDS
- TypeScript
- Apache-2.0
- Digital-Employee
- Feishu
source:
  url: https://github.com/HKUDS/AgentSpace
  fetched: 2026-06-28T08:00+08:00
  by: 小助 via web_fetch + web_search
---

# AgentSpace — GitHub 仓库研究

**Date:** 2026-06-28  
**Prepared for:** 何大人 · Internal Research  
**Sources:** https://github.com/HKUDS/AgentSpace · https://github.com/HKUDS

---

## 1. Project Overview

**AgentSpace**（`HKUDS/AgentSpace`）是 **香港大学数据科学实验室（HKUDS）** 于 2026-06-21 发布的 **v1.0 开源项目**，定位为 **"Agent-Native Collaborative Workspace"**——让人类和 Agent 作为同一团队的成员，在同一个工作空间内协作。

### 基本信息

| 维度 | 信息 |
|---|---|
| **GitHub** | https://github.com/HKUDS/AgentSpace |
| **维护方** | HKUDS（Data Intelligence Lab @ HKU） |
| **语言 / 框架** | TypeScript + Next.js + PostgreSQL |
| **最新版本** | v1.0（2026-06-21） |
| **许可证** | Apache 2.0 |
| **Stars** | 487（含星中，新兴项目） |
| **Forks** | 54 |
| **Issues / PRs** | 2 issues / 5 pull requests |
| **推荐运行时** | Node.js 24（daemon 要求 ≥ 20.20.0） |
| **数据库** | PostgreSQL 16（Docker Compose 一键部署） |
| **官网（托管版）** | https://hire-an-agent.online |

### HKUDS 实验室背景

HKUDS（Data Intelligence Lab @ HKU）是活跃的学术+开源实验室，主力语言为 Python。**AgentSpace 是该实验室罕见的 TypeScript 项目**，表明其面向企业级工程交付而非纯学术研究。其 pinned 仓库包括：

| 仓库 | Stars | 主题 |
|---|---|---|
| nanobot | 44.8k | 轻量级 AI Agent |
| CLI-Anything | 44.1k | CLI 原生化框架 |
| LightRAG | 37.1k | EMNLP2025 RAG |
| DeepTutor | 25.1k | 个性化 AI 助教 |
| AgentSpace | **487** | 企业 Agent 协作平台（新兴） |

---

## 2. 官方描述（英文原文）

> "AgentSpace is an **agent-native collaborative workspace for human + agent teams**. Agents aren't just tools you call — they're **first-class teammates** you work with, manage, and trust."

> "Feishu was built for humans. **AgentSpace is built for both.**"

> "The goal isn't a smarter chatbot. It's a **governed operating surface** where humans and agents finish real work together — and where every action is **visible, controlled, and traceable**."

### 核心理念

AgentSpace 的出发点是：**当前大多数 Agent 框架面向个人使用**，一旦企业团队想把 Agent 纳入日常运营，就会面临 5 大困境：

1. **Agents 私有化** — Agent 藏在个人终端里，团队其他人看不到
2. **上下文分散** — 消息、文档、审批、截图、运行时文件散落各处，没有共享 home
3. **执行碎片化** — 每个 Provider（Claude Code / Codex / OpenClaw / Gemini CLI）行为各异，切换成本高
4. **治理缺失** — 凭证、文档、工具调用、对外操作难以统一审计
5. **工作不持久** — 多天任务需要队列、交接、输出、retry、人工 checkpoint，没有框架支持

**AgentSpace 的解法：人类拥有方向和授权，Agent 负责协调和执行。**

---

## 3. Core Functions — 核心功能拆解

### 3.1 AgentRouter — 多 Runtime 统一调度层

AgentRouter 是 AgentSpace 的**核心执行引擎**，负责：
- 将任务路由到正确的 harness/provider runtime（Claude Code、Codex、OpenClaw、Hermes 等）
- **跨 runtime 保持 Agent 身份、指令和上下文稳定**——切换 harness 时只换 harness，Skills / Knowledge / Permissions 不变
- 统一规范化 events、sessions、outputs、diagnostics

**支持的 Agent 矩阵：**

| Provider | Execution Path | Diagnostics |
|---|---|---|
| **Claude Code** | AgentRouter（主力） | stream-json events, session fallback, tool approval bridge |
| **Codex CLI** | AgentRouter（主力） | JSON events, session fallback, runtime tool capability diagnostics |
| **OpenCode** | AgentRouter（2026-06-24 迁入） | JSON events, session propagation, timeout/nonzero/empty diagnostics |
| **OpenClaw** | AgentRouter（主力） | health/preflight, auth/profile/model/tool/protocol diagnostics, missing session fallback |
| **Hermes Agent** | AgentRouter（主力） | text output, executable compatibility, timeout diagnostics |
| Gemini CLI | legacy provider-runtime | one-shot CLI |
| NanoBot | legacy provider-runtime | one-shot CLI |

> OpenClaw 已在 AgentRouter 主力路径上（2026-06-22 支持），而非 legacy path——**对 OpenClaw 用户意义重大**。

**快速测试命令：**
```bash
agent-router harnesses
agent-router detect
agent-router run --harness claude --cwd /workspace/project "summarize this repo"
agent-router run --harness openclaw --cwd /workspace/project --mode medium "review this diff"
```

### 3.2 Digital Employee Board — 数字员工看板

概念：**把私有 Agent 变成可见、可借用、可复用的"数字员工"**

- 展示每个数字员工：角色、Owner、Skills、Knowledge、就绪状态、runtime 绑定
- 团队成员可申请访问、借用 Agent，无需从零配置
- Owner 审核队列和 Admin 审批路径清晰——人类保留 100% 访问控制权
- **核心价值：让优秀的 Agent 可见，同时不放弃控制权**

### 3.3 Multi-Agent Collaboration — 多智能体协作

- 支持 **War Room（作战室）** 模式：多 Agent 协调高风险运营决策
- 复杂请求（证据收集、预算核查、审批准备、执行、输出交付）**无需人工交接**即可推进
- Runtime 输出文件、执行事件、任务历史**附加在 Workspace 而非埋在终端里**
- Human approval gates：**高影响操作路由到人工审批**，Agent 继续工作，人类保持控制

### 3.4 Permission Control Plane — 权限控制平面

- 统一治理：Workspace 角色、Channels、文档、Skills、Knowledge、Runtimes、Daemon tokens、Google credentials
- 支持：文档访问请求、Runtime 工具审批、知识提案审核、Agent 粒度的 Google Workspace 委托
- 支持按**资源树**或**执行者**查看权限
- 可撤销、审计、诊断权限漂移——在问题发生前解决

### 3.5 Skills, Knowledge & Google Workspace 集成

- **Skills**：Agent 技能定义（可复用）
- **Knowledge**：Agent 知识库（可共享）
- **Google Workspace 委托**：Agent 可代表用户访问 Google Docs/Sheets/Drive（带审批）

### 3.6 通讯层：Feishu 集成（2026-06-27）

> "AgentSpace is introducing a Claude Tag-like **Feishu integration** so teams can connect AgentSpace agents to Feishu conversations while keeping governance in AgentSpace."

- 实现路径：类 Claude Tag 的飞书对话集成（分支：`codex/feishu-integration`）
- 飞书用户可直接在飞书对话中调用 AgentSpace 治理下的 Agent
- 治理、审批、审计仍保留在 AgentSpace 侧

---

## 4. Technical Architecture — 技术架构

### 4.1 系统架构图

```
┌─────────────────────────────────────────────────────────┐
│                    Human Members                        │
│         (Web UI / Feishu / Direct Input)               │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌───────────────┐     ┌────────────────┐
│  Web Frontend │     │  CLI (agent-   │
│  Next.js :1455│     │  space CLI)    │
└───────┬───────┘     └───────┬────────┘
        │                     │
        └─────────┬───────────┘
                  ▼
         ┌──────────────────┐
         │ @agent-space/    │
         │   services      │
         └────────┬─────────┘
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
┌─────────┐ ┌──────────┐ ┌──────────┐
│   DB    │ │  Domain  │ │  Queue   │
│PostgreSQL│ │          │ │(Tasks/   │
│         │ │          │ │Approvals/│
│         │ │          │ │Notifs)   │
└────┬────┘ └──────────┘ └────┬─────┘
     │                       │
     │              ┌────────┴────────┐
     │              ▼                  ▼
     │     ┌──────────────┐  ┌──────────────────┐
     │     │agent-space-  │  │ @agent-space/     │
     │     │  daemon      │  │  docs/knowledge/  │
     │     │  (remote     │  │  attachments/     │
     │     │   execution) │  │  Google Workspace │
     │     └──────┬───────┘  └──────────────────┘
     │            │
     │     ┌──────┴────────────────────────────────┐
     │     ▼                                        ▼
     │  ┌──────────────┐                    ┌───────────────┐
     │  │ AgentRouter  │                    │Legacy Provider│
     │  │  (主力路径)   │                    │   Runtime     │
     │  └──┬─────┬─────┘                    │  (Gemini/Nano)│
     │     │     │     │                    └───────────────┘
     │  ┌──┴─┐┌──┴─┐┌──┴─┐┌──┐
     │  ▼    ▼    ▼    ▼
     │ Claude Codex OpenClaw Hermes   ← AgentRouter Harnesses
     │ Code
     └──────────────────────────────► Runtime Output / Diagnostics / Sessions
```

### 4.2 技术栈

| 层级 | 技术 |
|---|---|
| **Frontend** | Next.js（TypeScript） |
| **Backend Services** | `@agent-space/services` |
| **Domain Layer** | `@agent-space/domain` |
| **Database** | `@agent-space/db` / PostgreSQL 16 |
| **Daemon** | `agent-space-daemon`（Node.js ≥ 20.20.0） |
| **Queue** | Tasks / Approvals / Notifications |
| **Runtime Harnesses** | Claude Code、Codex、OpenClaw、Hermes（AgentRouter） |
| **Legacy Runtimes** | Gemini CLI、NanoBot |
| **Deploy** | Docker Compose（PostgreSQL）、Self-host 或 Platform |

### 4.3 部署模式

| 模式 | 适用场景 | 启动方式 |
|---|---|---|
| ☁️ **Platform（托管）** | 快速上手，无需基础设施 | 访问 hire-an-agent.online |
| 🖥️ **Self-hosted（本地）** | 企业要求数据/基础设施/Provider CLI 完全自控 | Docker Compose + `npm run dev:web` |

**本地部署步骤：**
```bash
git clone <your-agentspace-repo-url>
cd AgentSpace

npm run setup
cp .env.example .env

# 启动 PostgreSQL
docker compose -f deploy/postgres/docker-compose.yml up -d
npm run db:pg:init

# 启动 Web
npm run dev:web
# 访问 http://127.0.0.1:1455
```

**Remote Daemon 部署（企业内网 Agent 执行）：**
```bash
# 打包 daemon
npm run daemon:pack

# 在远程机器安装
npm install -g ./agent-space-daemon-0.1.3.tgz

# 启动 daemon
agent-space-daemon start \
 --foreground \
 --server-url "https://your-agentspace-domain" \
 --daemon-token "adt_xxx" \
 --daemon-id "daemon-prod-01" \
 --device-name "prod-daemon-host-01" \
 --runtime-name "Remote Agent" \
 --task-timeout "43200000" \
 --state-dir "$HOME/.agent-space-daemon"
```

### 4.4 CLI 命令

```bash
# 通用命令
npm run cli -- help
npm run cli -- doctor --json
npm run cli -- workspace status --json
npm run cli -- db status --json
npm run cli -- im channels --json
npm run cli -- channel list --json
npm run cli -- task list --json
npm run cli -- daemon status --json

# 数据库
npm run db:pg:status -- --json
npm run db:pg:init
npm run db:pg:migrate -- --dry-run --sqlite-path data/agent-space.sqlite --json
```

### 4.5 AgentRouter 快速测试

```bash
agent-router harnesses                    # 列出所有 harness
agent-router detect                       # 检测环境
agent-router run --harness claude --cwd /workspace/project "summarize this repo"
agent-router run --harness codex --cwd /workspace/project --model gpt-5.1 "fix tests"
agent-router run --harness opencode --cwd /workspace/project --model openrouter/openai/gpt-4.1 "summarize this repo"
agent-router run --harness openclaw --cwd /workspace/project --mode medium "review this diff"
```

---

## 5. 与德勤方案的匹配度分析

### 5.1 企业 Workspace 理念 ✅ 高度匹配

| 德勤方案要素 | AgentSpace 对应 | 匹配度 |
|---|---|---|
| **Workspace 作为统一入口** | Next.js Web UI + Feishu 集成双入口 | ✅ 强 |
| **数字员工（Digital Employees）** | Digital Employee Board，有角色/Owner/Skills/Knowledge | ✅ 强 |
| **多 Agent 协作** | AgentRouter 统一调度 + War Room 协作模式 | ✅ 强 |
| **治理与审计** | Permission Control Plane + 完整 Audit Trail | ✅ 强 |
| **Human-in-the-loop** | Approval Gates，TabTabTab 审批流 | ✅ 强 |
| **知识共享** | Skills + Knowledge 库，支持 Google Workspace | ✅ 中 |
| **通讯协作层** | Feishu 集成（飞书） | ✅ 强 |
| **OpenClaw 作为 Agent Runtime** | OpenClaw 在 AgentRouter 主力路径（2026-06-22 支持） | ✅ 强 |

### 5.2 与 OpenAgents 的对比

| 维度 | AgentSpace | OpenAgents |
|---|---|---|
| **定位** | 企业级治理 + 数字员工管理 | 开发者协作平台（"Slack for Agents"） |
| **治理深度** | Permission Control Plane + Audit Trails | 无企业级治理 |
| **数字员工概念** | ✅ 有（角色/Owner/Skills/可转让） | ❌ 无 |
| **Human Approval Gates** | ✅ 有（高影响操作审批） | ❌ 无 |
| **Feishu 集成** | ✅ 有（2026-06-27） | ❌ 无 |
| **语言** | TypeScript/Next.js | Python |
| **部署** | Self-hosted / Platform | Platform SaaS |
| **学术背景** | HKUDS（学术 + 企业应用） | 社区驱动 |
| **Stars** | 487（新兴） | 社区项目 |

**结论：** AgentSpace 相比 OpenAgents 更偏向**企业治理**，而 OpenAgents 更偏向**开发者协作**。两者定位互补。

### 5.3 匹配场景

| 德勤场景 | AgentSpace 如何支持 |
|---|---|
| **德勤 AI Native 组织 Workspace** | Digital Employee Board + Multi-Agent Collaboration |
| **企业 Agent 生命周期管理** | Recruit / Assign / Transfer / Audit 全链路 |
| **高风险操作审批** | TabTabTab Approval Gates |
| **Agent 跨团队复用** | 数字员工可申请借用，Owner 保留控制 |
| **企业知识管理** | Skills + Knowledge 库 + Google Workspace 集成 |
| **飞书作为通讯入口** | Feishu 集成（2026-06-27） |

---

## 6. Deployment Assessment — 部署评估

### 6.1 部署要求

| 依赖 | 最低版本 | 备注 |
|---|---|---|
| **Node.js** | ≥ 20.20.0（daemon）；推荐 24 | TypeScript 全家桶 |
| **npm** | 11.x | |
| **PostgreSQL** | 16（推荐） | Docker Compose 一键部署 |
| **Docker** | 支持 Docker Compose | 仅自托管模式 |
| **可选 Provider CLI** | codex / claude / gemini / opencode / openclaw / nanobot / hermes | 按需安装 |
| **可选** | Google OAuth / Google Workspace | 企业知识集成 |

### 6.2 部署复杂度评估

| 维度 | 评分 | 说明 |
|---|---|---|
| **上手难度** | 🟡 中等 | Docker + npm + PostgreSQL，有一定门槛 |
| **自托管复杂度** | 🟡 中等 | Docker Compose 封装较好，但 daemon 远程部署需手动配置 |
| **运维复杂度** | 🟡 中等 | PostgreSQL 需要维护，Daemon 需要 systemd 管理 |
| **生产就绪度** | 🟢 良好 | v1.0，Apache 2.0，企业特性完整，但新兴项目需观察稳定性 |
| **飞书集成成熟度** | 🟡 Beta（分支中） | 2026-06-27 才宣布，真实可用性待验证 |

### 6.3 风险评估

| 风险 | 等级 | 说明 |
|---|---|---|
| **项目新鲜度** | 🟡 中 | 2026-06-21 才 v1.0，生态待建立 |
| **Stars 487 偏少** | 🟡 中 | 新兴项目，Community 规模小 |
| **TypeScript 非 HKUDS 主流** | 🟢 低 | 可能意味着更严谨的工程化 |
| **飞书集成未合入主线** | 🟡 中 | 代码分支中，合入时间未知 |
| **PostgreSQL 运维** | 🟡 中 | 企业需有 DBA 能力 |

---

## 7. 使用建议

### ✅ 推荐场景

1. **德勤 AI Native Workspace 方案参考** — AgentSpace 的数字员工 + 治理理念与德勤方案高度吻合，可作为技术方案原型参考
2. **企业 Agent 治理平台 POC** — 如果企业需要：数字员工管理 + Human Approval + Audit Trail，AgentSpace 是目前最接近的开源实现
3. **OpenClaw 的上层编排层** — AgentSpace 的 AgentRouter 已将 OpenClaw 列为主力 harness，可考虑作为 OpenClaw 的企业协作层
4. **飞书用户** — AgentSpace 已支持/正在支持飞书集成，适合飞书办公的企业

### ⚠️ 注意事项

1. **v1.0 新兴项目**：建议做 PoC 而非生产直接部署；等待 3-6 个月生态成熟
2. **Feishu 集成未合入主线**：如需飞书集成，需跟踪 `codex/feishu-integration` 分支进展
3. **PostgreSQL 运维**：生产环境需要专业的数据库运维能力
4. **Provider CLI 依赖**：不同 harness 需要安装对应 CLI（Claude Code / Codex 等），部署时要考虑授权

### 🔮 潜在下一步

| 行动 | 价值 |
|---|---|
| **AgentSpace + OpenClaw 集成测试** | AgentRouter 已支持 OpenClaw，测试接入可行性 |
| **跟进 Feishu 集成合入时间** | 飞书用户的关键功能 |
| **参考 Digital Employee Board 设计** | 为德勤方案提供 UI/UX 参考 |
| **做 AgentSpace PoC** | 在测试环境部署，验证企业 Agent 治理流程 |

---

## 8. Quick Reference — 参考链接

| 项目 | 信息 |
|---|---|
| **GitHub** | https://github.com/HKUDS/AgentSpace |
| **官网（Platform）** | https://hire-an-agent.online |
| **维护方** | HKUDS（Data Intelligence Lab @ HKU） |
| **License** | Apache 2.0 |
| **语言** | TypeScript + Next.js |
| **Stars / Forks** | 487 / 54 |
| **最新版本** | v1.0（2026-06-21） |
| **推荐 Node.js** | 24 |
| **数据库** | PostgreSQL 16 |
| **AgentRouter 支持** | Claude Code、Codex、OpenCode、**OpenClaw**、Hermes（主力） |
| **Legacy 运行时** | Gemini CLI、NanoBot |
| **特色功能** | Digital Employee Board、Permission Control Plane、Approval Gates、Feishu 集成 |
| **本地部署** | `npm run dev:web`（http://127.0.0.1:1455） |
| **Feishu 集成分支** | `codex/feishu-integration` |

---

**研究完成。** 本文档已存档到 vault：`/root/vault/Research/2026-06-28 - AgentSpace - GitHub Deep Research.md`
