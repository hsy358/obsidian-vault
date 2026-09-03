---
type: github-repo-analysis
source: github_api + readme
repo: Prism-Shadow/penguin-harness
repo_url: https://github.com/Prism-Shadow/penguin-harness
provided_url: https://github.com/penguinharness/penguinharness (404 — 何大人给的链接是错的，实际主仓库在这里)
website: https://penguin.ooo/
npm_core: @prismshadow/penguin-core
docs: https://penguin.ooo/docs/
stars: 1957
forks: 205
language: TypeScript
license: Apache-2.0
size_kb: 22872
created: 2026-07-19
updated: 2026-09-03
analyzed_date: 2026-09-03
analyzed_by: 小助（MiniMax-M3）
topics:
  - agent
  - agentic-ai
  - ai
  - build-tool
  - claude-code
  - deepseek
  - deepseek-harness
  - desktop
  - harness
  - llm
  - rsi
  - self-evolving
authors:
  - Yaowei Zheng (hiyouga) — LlamaFactory 作者
  - PrismShadow AI Team
  - Fable 5
title: PenguinHarness — GitHub 仓库分析
description: LlamaFactory 作者 hiyouga 出品的开源「用 Agent 构建 Agent」自动化平台。RSI（递归自我改进）+ Skills 系统 + Goal mode + Trace 可观测，9 大模型家族 × 1000+ 模型，$0.02 生成 RAG App。架构：pnpm monorepo（cli/core/desktop/docs/landing/server/web 7 模块 + 12 内建插件）。
tags:
  - github-repo-analysis
  - ai-agent
  - harness
  - self-evolving
  - rsi
  - skill-system
  - llamafactory
  - claude-code
  - deepseek
  - desktop-app
related:
  - "[[2026-07-25 - Multica - GitHub 仓库分析]]"
  - "[[2026-07-25 - Block Buzz - GitHub 仓库分析]]"
  - "[[2026-08-25 - OpenConnector - GitHub 仓库分析]]"
  - "[[2026-09-02 - UUMit官网 - AI能力网络]]"
  - "[[2026-09-02 - 换工具、换 Agent，不换上下文：OpenViking 让研发 Context 始终在线]]"
  - "[[2026-09-03 - 给Agent加上知识图谱，开源版Palantir]]"
---

# PenguinHarness — GitHub 仓库分析

> 来源：https://github.com/Prism-Shadow/penguin-harness（1957★ · 205 forks · TypeScript · Apache-2.0）
> 创建 2026-07-19 · 最近更新 2026-09-03（5 周成长相当快）

---

## ⚠️ 链接修正

何大人给的链接 `https://github.com/penguinharness/penguinharness` 返回 **404**。
实际主仓库是 **`Prism-Shadow/penguin-harness`**（org 在 Prism-Shadow，不是 penguinharness）。
搜索结果里有 4 个相关项目（教程、fork、TUI wrapper），但都是衍生品。

---

## 📌 一句话定位

**PenguinHarness = 开源 + 本地优先 + 用 Agent 构建 Agent 的多 Agent 应用开发平台**。
主打「**RSI（Recursive Self-Improvement，递归自我改进）**」+ Skills 系统 + Goal mode + Trace 可观测，9 大模型家族 × 1000+ 模型。

> With LangChain, you build agents by hand — at 1× speed.
> With PenguinHarness, agents build agents — at 100×.

---

## 👥 团队（关键）

- **Yaowei Zheng（[hiyouga](https://github.com/hiyouga)）** — **LlamaFactory 作者**！AI 微调领域最有名的开源项目之一
- **PrismShadow AI Team** — 团队
- **Fable 5** — 协作方（Anthropic 关联项目）

> LlamaFactory 是何大人 / 中国 AI 圈非常熟悉的项目 — **这意味着 PenguinHarness 不是「又一个玩具 Agent 框架」，而是 LlamaFactory 同级别作者做的严肃工程产品**。

---

## 🎯 3 个核心卖点（README Why PenguinHarness）

### 1. 🏆 Outstanding results at tens of times less cost
- "**Best accuracy on data analysis — at 1/70 of Claude Code's cost**"
- 跟 **DeepSeek** 深度优化（fewer tool calls、fewer tokens）
- 内置 benchmark 套件（roadmap 即将公开发布）

### 2. ⚡ 一句话生成可运行 Agent App
- 输入："Collect the docs from https://github.com/ericbuess/claude-code-docs and build a RAG app..."
- 输出：完整 docs 专家 Agent（带 retrieval、cited sources、example questions）
- 成本：**$0.02（¥0.2）on DeepSeek V4 Pro**

### 3. 🧬 原生 Agent 自进化引擎（PenguinHarness Skills）
- Skills 系统：跑 benchmark → 找 lost points → 发版 N+1
- 每个 round 前快照、每次请求 Trace 可观测
- **Goal mode + Continual learning** session hooks

---

## 🧩 内建插件（12 个，3 类）

| 类别 | 插件 |
|---|---|
| **Office Productivity** | data-analysis, use-firecrawl, use-bento-slides, humanizer, goal, continual-learning |
| **Software Development** | software-development, **use-claude-code** |
| **AI App Development** | **agent-development**, model-development, skill-porting, agent-tuning |

**关键 4 个**：
- **`agent-development`** — 用 Agent 自动构建 Agent（项目核心）
- **`agent-tuning`** — Agent 微调（LlamaFactory 血统）
- **`skill-porting`** — 把别的 Agent 的 skill 移植过来
- **`continual-learning`** — 持续学习 hook

---

## 🤖 支持模型（9 大家族 × 1000+ 模型）

| 模型 | 提供商 |
|---|---|
| **DeepSeek V4** | DeepSeek, OpenRouter, Fireworks AI, SiliconFlow, TokenDance, Qwen Token Plan, Qwen Pay-As-You-Go |
| **Kimi K3** | Moonshot AI, OpenRouter, Fireworks AI, TokenDance, Qwen Pay-As-You-Go |
| GLM 5.3 | Z.AI, OpenRouter, TokenDance |
| Hunyuan 3 | OpenRouter |
| Qwen 3.8 Max | Qwen, OpenRouter, TokenDance |
| GPT 5.6 | OpenAI, OpenRouter |
| Gemini 3.7 Flash | Google Gemini, OpenRouter |
| Claude 5 | Anthropic, OpenRouter |
| Inkling | OpenRouter, Fireworks AI |

> 任何 OpenAI-protocol 端点都可接入（点 preset 或自定义 endpoint）。
> **重点支持 DeepSeek + Kimi**（中国模型优先） — 跟 LlamaFactory 一脉相承。

---

## 🏗️ 架构（pnpm monorepo）

### packages/ (7 模块)
- **cli** — 命令行客户端
- **core** — 核心库（`@prismshadow/penguin-core`，npm 已发布）
- **desktop** — 桌面应用（macOS / Windows / Linux AppImage / deb）
- **docs** — 文档站
- **landing** — 营销站
- **server** — 后端服务
- **web** — Web UI（multi-session chat, agent/skill/model management, usage stats, Trace, evaluation center）

### plugins/ (12 个内建插件)
（见上面表格）

---

## 🖥️ 安装 & 部署（多形式）

| 形式 | 命令 / 说明 |
|---|---|
| **Desktop** | macOS dmg / Windows installer / Linux AppImage & deb（双击即用，内嵌 server，自动登录） |
| **CLI 在线安装（Linux/macOS）** | `curl -fsSL https://penguin.ooo/install.sh \| sh` |
| **CLI 在线安装（Windows）** | `irm https://penguin.ooo/install.ps1 \| iex` |
| **npm** | `npm install -g @prismshadow/penguin-cli` |
| **离线包** | 每个 GitHub Release 一个包（含 SHA256 校验）— **air-gapped 环境友好** |
| **运行时** | Node ≥ 24（在线安装包自带 runtime） |

### CLI 核心命令
```bash
penguin config model add --provider deepseek --model-id deepseek-v4-flash-vision-exp --api-key sk-... --set-default
penguin run -m "Create hello.txt containing Hello, Penguin"   # 一次性任务
penguin chat       # 交互式 REPL (/compact, /clear, /exit)
penguin server     # headless service（和 Web App 用同 API）
penguin web        # 启动 Web（http://127.0.0.1:7364）
```

### TypeScript SDK
```ts
import { createAgent, isCompleteModelMessage, userText } from "@prismshadow/penguin-core";

const agent = await createAgent({ agentId: "default_agent" });
const session = await agent.createSession({ workspaceDir: process.cwd() });

for await (const output of session.run([userText("Create hello.txt containing hi")], {
  approve: async () => "allow", // per-tool-call approval
})) {
  if (isCompleteModelMessage(output) && output.payload.type === "text") {
    console.log(output.payload.text);
  }
}
```

> **关键点**：CLI + SDK **天然就是给 Agent 用的**（"made to be driven by agents, and agents building agents"）。

---

## 🛣️ Roadmap（关键待办）

- [ ] Public release of the benchmark suite（公开评测套件）
- [x] Desktop app ✅
- [x] Windows support ✅
- [ ] Agent company and templates（**Agent 公司** — 大方向）
- [ ] Company-level self evolving（**公司级自进化**）
- [ ] **OpenShell integration (permission-governed shell)** ← **跟 OpenClaw 相关！**
- More to come…

> 「**Agent company**」和「**Company-level self evolving**」明确指向 **multi-agent orchestration + RSI** — 不是单 Agent 玩，而是**让一群 Agent 形成「公司」自动演进**。

---

## 📚 与 vault 现有研究的横向对位

| 项目 | 定位 | 跟 PenguinHarness 的对位 |
|---|---|---|
| [[2026-07-25 - Multica]] | Agent 团队管理控制平面（执行器层） | **PenguinHarness = Agent 构建平台（构建层）**，Multica 是 Agent 团队管理（管理层） |
| [[2026-07-25 - Block Buzz]] | Hive-Mind 协作工作区（事件签名化） | PenguinHarness **没有事件签名模型**，但都强调「多 Agent 协作」 |
| [[2026-08-25 - OpenConnector]] | SaaS 工具调用网关 | 互补：OpenConnector = 工具层，PenguinHarness = Agent + Skill 层 |
| [[2026-09-02 - UUMit官网]] | Agent 找 Agent + 撮合结算 | **完全不同**：UUMit = 网络层（发现 + 撮合），PenguinHarness = 构建层 |
| [[2026-09-02 - OpenViking]] | Context 数据库（文件式） | 互补：OpenViking = Context 持久化，PenguinHarness = Agent 自身构建 |
| [[2026-09-03 - Semantica]] | 知识图谱 Context 层（图式） | 互补：Semantica = 强监管场景，PenguinHarness = 通用 R&D |
| Hermes (vault/1-Projects/德勤) | dispatcher + chat | Hermes 是**执行器**，PenguinHarness 是**构建平台** — PenguinHarness 可以「构建出 Hermes-like 的执行器」 |
| OpenClaw (本地) | 可插拔执行器 + AgentSpace 1455 端口 | **不冲突**：PenguinHarness 可以构建 skill 跑在 OpenClaw 上；OpenShell 集成是未来可能路径 |

**核心判断**：
- PenguinHarness 是 **Agent 构建层**（Meta-Agent / Agent-of-Agents）
- OpenClaw / Hermes 是 **执行层**
- OpenViking / Semantica 是 **Context 层**
- UUMit 是 **网络层**
- Multica 是 **管理层**
- OpenConnector 是 **工具层**

→ **六层架构补齐了**："工具 → 执行 → 构建 → Context → 管理 → 网络"

---

## 🎯 与德勤 MVP 的对位 — 强相关 ⭐

德勤 AI Native MVP 关心的核心是「**AI Native 组织 Workspace + Agent 智能体平台**」。
PenguinHarness 直接对位"**用 Agent 构建 Agent + 自进化**"这条线。

**最值得抄的 4 个机制**：
1. **Skills 不是 Tool、不是 RAG，而是 Skill** — 跟 OpenViking 的 viking:// Skill 对位（德勤 workspace 资源抽象也可以用 Skill 命名）
2. **Goal mode + Continual learning session hooks** — 每轮任务自动沉淀（**v3 教训**：写过 5 条风控规则没一条执行 → PenguinHarness 把"自进化"做成默认行为，可直接借鉴）
3. **Trace view** — 每次请求可观测（Hermes 已经在做这件事 → 对齐方向）
4. **1/70 Claude Code cost** — 深度 DeepSeek 调优（fewer tool calls, fewer tokens）— 给德勤客户做**TCO 论证**时是关键论据

**OpenShell integration**：roadmap 里明确「**permission-governed shell**」 — 跟 OpenClaw 路线重合度极高。

---

## 🧪 我的判断（5 条）

### 1. **不是玩具，是严肃工程产品**
- 1957★（5 周）
- LlamaFactory 作者（hiyouga）
- 完整的 Desktop + CLI + npm + 离线包
- 12 个内建插件 + 9 大模型家族
- Apache 2.0 + 论文 citation BibTeX
→ **这是 AI Agent 领域 2026 H2 值得持续观察的项目**。

### 2. **不是 OpenClaw / Hermes 替代品**
按 MEMORY.md 2026-06-29 何大人明确的研究边界：
- PenguinHarness 是 **构建层**（Agent-of-Agents）
- OpenClaw / Hermes 是 **执行层**
- 两者**不冲突、可叠加**：PenguinHarness 可以"构建"出 Hermes-like 的执行器，跑在 OpenClaw 上
- ❌ **不**做产品层面的"二选一"决策

### 3. **不立即动手，但持续观察**
按 Simplicity First：
- 现在没有强需求要在 OpenClaw 上"用 Agent 构建 Agent"
- 5 周 1957★ 说明增长势头好，等 v1.0 / benchmark 公开再做判断
- **监控点**：OpenShell integration 上线 + benchmark 公开 + 公司级 self evolving 实现

### 4. **Skill 系统是一个有价值的概念**
不管是 OpenViking 的 viking:// Skill，还是 PenguinHarness 的 Skills：
- 都把"能力"抽象为**独立单元**（不是 Tool、不是 RAG、不是 Prompt）
- 都有"可移植 + 可继承 + 可优化"属性
- 德勤 MVP 资源抽象可以借鉴 Skill 这个概念

### 5. **「Agent 公司 + 公司级自进化」是值得跟踪的大方向**
roadmap 明确说要做 Agent company + Company-level self evolving — 这是**多 Agent 形成组织并自演进**的概念，**跟我们 AI Native 组织 Workspace 主题 100% 重合**。

---

## 📎 原始资料

- 仓库主页：https://github.com/Prism-Shadow/penguin-harness
- 官网：https://penguin.ooo/
- 文档：https://penguin.ooo/docs/
- npm 核心包：https://www.npmjs.com/package/@prismshadow/penguin-core
- README（已抓取，14866 字节）：`/tmp/penguin_readme.md`
- 顶层文件树（API 获取）：已展示在分析中
- BibTeX 引用：
  ```bibtex
  @software{penguinharness2026,
    author  = {{PrismShadow Team}},
    title   = {PenguinHarness: Efficient Self-Improving Harness for Everyone},
    year    = {2026},
    url     = {https://github.com/Prism-Shadow/penguin-harness},
    license = {Apache-2.0}
  }
  ```

## 🔗 同主题其他资源（GitHub 搜索结果）

| 仓库 | 描述 |
|---|---|
| xiaoshancha/deepseek-harness-tutorial | 基于 PenguinHarness 用 deepseek-v4-flash-vision-exp 开发 |
| hiyouga/penguinharness-tutorial | PenguinHarness 线上教程书 Web 平台（官方教程） |
| gateszhangc/penguinharness-lat | （低关注度 fork） |
| swsgbl/penguin-tui | Claude Code-style TUI（Apache-2.0，基于 Prism-Shadow/penguin-harness） |