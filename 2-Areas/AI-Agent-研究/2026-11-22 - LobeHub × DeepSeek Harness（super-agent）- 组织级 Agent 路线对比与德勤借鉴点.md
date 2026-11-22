---
title: LobeHub × DeepSeek Harness（super-agent）—— 组织级 Agent 两条路线对比与德勤借鉴点
date: 2026-11-22
type: comparison-note
tags: [AI-Agent, LobeHub, DeepSeek-Harness, super-agent, dsh, 组织级Agent, Acceptance, 多智能体, 德勤项目, 架构参考]
sources:
  - https://mp.weixin.qq.com/s/QVu2luIrRTtNvsH-U65A8g （赛博禅心《如何让 Super-agent 成为同事：LobeHub 的组织实验》，2026-11-01）
  - https://github.com/deepseek-ai/deepseek-harness
  - https://github.com/deepseek-ai/dsh-superagent-prototype
  - https://github.com/lobehub/lobehub
  - https://github.com/lobehub/acceptance
  - https://lobehub.com/docs/usage/agent/agent-team
  - https://lobehub.com/docs/usage/agent/agent-profile
  - https://lobehub.com/blog/self-evolving-harness
  - https://lobehub.com/blog/heterogeneous-agent-runtime
related_notes:
  - 2026-10-28 - DeepSeek Harness + DS Bot - 架构分析与德勤项目借鉴点.md
  - 2026-11-03 - DeepSeek Super-agent - 设计分析与德勤借鉴点.md
  - 2026-11-05 - Agent Autoloop × DeepSeek Super-agent - 异同对比.md
  - 2026-11-05 - 德勤 Agent 平台借鉴清单 v1（Autoloop×Super-agent×DSH）.md
  - 2026-10-28 - Anthropic Knowledge Work Plugins - AI Native 组织 Workspace 对标分析.md
  - 2026-11-19 - rust-anything - AI Agent 驱动的渐进式 Rust 重写（录制-对拍-闸门）与德勤执行器验收借鉴.md
---

# LobeHub × DeepSeek Harness（super-agent）：组织级 Agent 的两条路线

> **取材**：何大人转来赛博禅心《如何让 Super-agent 成为同事：LobeHub 的组织实验》（2026-11-01，文彬访谈），叠加两路官方信息核实（GitHub API + 官方文档，2026-11-22）。
> **前提不变（2026-06-29 决策）**：**Hermes Agent v0.14 是德勤项目 Agent 框架的唯一选择**。LobeHub / DSH 两条路线都只作**架构借鉴**，不做产品二选一。
> **标注规则**：本文对每条结论标口径 —— 【官】官方文档/仓库原文、【推】推断。

---

## 零、先说结论

> **这两者根本不在同一层：**
> **DeepSeek Harness / super-agent = 一套「运行时 + 领域模型」的架构范式（可白嫖的骨架）。**
> **LobeHub = 一套「组织操作系统」的成品产品（大半闭源，是竞品而非素材）。**

**对德勤的直接含义**：
- **LobeHub 值得抄的是零件**：Acceptance（Apache-2.0，可直接用）+ Task 工单链 + 异构 runtime 纳管 + tracing-first 自改进。
- **LobeHub 值得警惕的是整体**：它的 `LobeHub Community License` **禁止 fork 衍生分发**（需商业授权）→ 跟 Apple HALO 一样，**不能进客户交付物**。
- **DeepSeek 路线才是"能进交付物"的**：dsh = MIT、super-agent 原型 = MIT、DS Bot = Apache-2.0，三者协议都干净。
- **最值得注意的一条**：LobeHub 的 `lh hetero` 官方支持把 **DeepSeek Harness、OpenClaw、Hermes** 一起纳管 → **LobeHub 在做的正是我们德勤要做的"执行器抽象层"那一层**。这意味着我们的抽象层设计**有了一个真实的商业对标物**，且那个对标物已经把 Hermes 当成了可插拔执行器之一。

---

## 一、DeepSeek Harness（dsh）× super-agent 详细介绍

### 1.1 先把三个东西分清楚（此前 vault 笔记混用了）

| 名字 | 是什么 | 协议 | Star | 官方性 |
|---|---|---|---|---|
| **`deepseek-ai/deepseek-harness`**（dsh） | **Agent 运行时底座**，"一切皆插件"。模型/工具/会话/沙箱/存储/Agent Loop/调度/UI 全部由 Cordis 插件组装 | MIT | **285,000+** | ✅ **DeepSeek 官方** |
| **`deepseek-ai/dsh-superagent-prototype`** | **组织级自治调度原型**。在 dsh 之上做 Router/Worker + Policy/Mandate/Ticket 领域模型 | MIT | 24,187 | ✅ 官方，但**官方定位 "research prototype for reference only, not an official DeepSeek product"** |
| **`Fei2411/DS-Bot`**（旧名 `FeiZhuLulu/DeepSeek-Bot`） | **社区插件**，把 dsh 变成"一队长期存活的 Bot"：群聊、多 Bot 协作、context steward、记忆、secret 遮蔽 | Apache-2.0 | — | ❌ **独立社区项目** |

> ⚠️ **口径纠正**：**"super-agent" 不是 dsh 的别名**，它是 dsh 生态里的**另一个仓库**（dsh-superagent-prototype），实现方式是 **DSH Bundle**。说"DeepSeek Harness 就是 super-agent"是不准确的。

### 1.2 dsh 架构要点（对德勤直接可用的部分）

- **"There is no privileged core to patch"** —— 没有特权内核，模型适配器/工具注册表/session log/**agent loop 本身**都是插件。
- **Capability Seam 三角色**：`Service Definition`（声明接口）/ `Service Provider`（实现）/ `Consumer`（使用，通常是面向模型的 tool）。
  - 官方原话：**"A seam is a swappable capability with three roles"**、**"Seams are why one provider swap changes the whole product"**。
  - **一个包可以承担多个角色，但只有一个角色不构成 seam** → 加一个能力 = 设计三个角色。
  - 官方例子：文件系统 provider 与子进程 provider 共享同一执行世界 → 指向远程 sandbox 时，Bash / PTY / LSP **全部跟着搬走，不需要 fork provider**。
- **Profile / Bundle**：打包的是**配置行**不是代码。
  - Profile = 有序 bundle 叠加 + patch 层；Bundle = Cordis 配置行 + 代码。
  - 内置 profile：`web` / `headless` / `sdk` / `sdk-minimal` / **`acp`**。
  - 叠加顺序：profile bundles → `cordis.patch.yml` → home patch → `--patch overlay`。
- **Session Log「模型可见 = 已记录」**：每个 model request 必须能从 log 重建；`assistant/message` 内嵌产生它的完整紧凑流；`assistant/attempt` 保留失败/重试但不入模型历史；**已 commit 的 generation 路径永不重命名/替换/删除**。
- **事件三域**：Session events（持久事实）/ Agent events（活的，可拦截进行中的工作）/ Capability events（挂 seam，不 import agent loop）。
- **Turn/Step waterfall**：`agent/pre-step` / `agent/request` / `llm/stream` / `tools/*` 的 listener **必须调 `next()`**；`agent/turn-stopping` 串行且**没有 `next()`**。`prepareCall()` 在 commit 之前绑定 adapter，异步阶段取消 → **两边都不 commit**。
- **DeepSeek 官方 LLM 路线**：走 **Anthropic 风格 Messages API**（`https://api.deepseek.com/anthropic`），上下文 **1,048,576 token**。
- **规模**：117 MB / 52 顶层目录 / pnpm monorepo / TS + Python 双栈。
- ⚠️ **无 IM 通道**：dsh 自带 `feishu` / `dingtalk` / `wecom` 的 **connector**（工作流集成，如补全 PR 描述），**不是 IM 通道**；真正的 IM 通道由 DS Bot 插件提供。
- ⚠️ **context steward 是 DS Bot 的**，不是 dsh 核心（vault 旧笔记需修正口径）。

### 1.3 super-agent（原型）要点

- **Router / Worker 两层**：**Router 永远不拆任务、不亲自干活**，只对人说话和派单；Worker 隔离并行。
  - **Router 可以根本没有 shell** → 用轻量模型即可；Worker 才上最强模型。
- **事件驱动而非 prompt 驱动**：群聊消息 / PR 评论 / CI 结果都是 Trigger。
- **后续对话绕过 Router**：Worker 订阅自己的 Thread，后续消息直达 Worker（**消融实验显示：走直达时完成时间相同，但 Router 决策多 ~30%、缓存 token 23.23M → 31.77M**）。
- **领域模型 13 个概念**（最有工程价值）：
  `Source → Trigger → Thread → Eval → Mandate → Ticket → Assignment`，外加 `Correlation` / `Channel` / `Policy` / `Subscription`。
  - **Mandate 不可变**；**Ticket 只有 Eval 能创建**；**Ticket 自己定状态，不跟随 Executor 状态**；**Assignment 一个 Ticket 生命周期内可有多个**（→ 天然支持换执行器/重试/迁移）。
  - **人只是 Trigger 的元数据**；拒绝 Principal/Membership 实体。
- **授权三档**：explicit / inferred / not admitted + 每 Source 一张 Admission 表。
- **observe 模式**：未经规则允许的主动行为先进 observe，只记录"它本来会做什么"。
- **引擎纪律**：Engine 是 Trigger/Thread/Decision/Ticket/Assignment 的**唯一写入者**，全同步 + 单事务；**Outbox 是唯一 receipt 写入者**（事务内入队、提交后执行）。
- **Watchdog**：独立 session + 定时器，核查每个 Worker 是否真在推进；维护者可用自然语言问"哪里卡住了"。
- **思考边界**：回复 **≤100 字**；面板**只显示"需要人处理"的**；一次只问一个结构化问题。
- **实测**（DeepSeek 自测，官方称 preliminary）：Super-agent p50 **12.4 分钟** / p95 **15.7 分钟**；单 session+subagent 5 轮全部没委派、p95 **29.5 分钟**。
- **官方自己留的 4 个未解问题**：① Router session 规模上限 ② session 消失后人怎么协作 ③ **不同 agent 实例之间的上下文边界与通信** ④ **凭证能被使用但永不进入模型上下文**。
  → **这 4 条恰好就是德勤项目要答的题。**

### 1.4 DS Bot 补的（社区插件层）

- **多 Bot 群聊**：每群成员在每个群里有自己的**隐藏 Session**；`@Name` 传话；`+ → Reference a chat`；无话可说 `[PASS]`；**群永远读不到 Bot 的私聊**。
- **context steward checkpoint** ⭐：turn 结束超过 check line（上下文窗口 `checkRatio`，默认 0.8）→ 一次**小模型调用**决定一次：
  - 工作进行中 → **就地压缩成 checkpoint**（交接摘要 + 用户最近原话）；
  - 工作到停止点 → 写交接说明，在新 part 继续；
  - **用户看到的始终是同一个聊天、没有标记**；早期内容仍可 **FTS5 全文检索**。
- **记忆三层 scope**：Bot 私有 / 群共享（只在群里读）/ 团队共享；**每轮自动审阅**（不依赖模型自觉调 remember）；**记忆是数据不是指令**；条目 ≤300 字符、`MEMORY.md` ≤4000。
- **Secret 遮蔽** ⭐：`request_secret` → 卡片让你填，**Bot 永远看不到值**；值注入为 `DSH_SECRET_<NAME>`；**工具结果保存前 + 每次请求模型前**所有 secret 副本替换成 `[secret:<NAME>]`；`secrets.json` 权限 600、不进日志。
- **权限预设**：只读 / Workspace / 完全访问；**只有人能设权限，Bot 不能改**。
- **致谢名单**里明确借鉴 **Hermes Agent + Hermes Bot Mode**（每群成员独立 session + 交接带此前用户消息）→ 何大人 6-29 的 Hermes 路线有社区共识支撑。

---

## 二、LobeHub 详细介绍

### 2.1 它是什么

- **双 slogan**：「**Super-Agents on Your Team**」（GitHub README）/「**Your Chief Agent Operator (CAO)**」（官网 & Product Hunt #1147569，2026-05-18）。
- **定位**：不是 Agent 框架，是**组织级 Agent 协作平台**——把 Agent 组织成团队，让它们在 IM 里接活、干活、被验收。
- **产品线**：Web / macOS / Windows / Linux / 移动端；`@lobehub/cli`（命令 `lh`）；Coding Agents 页；Task Board；Acceptance；Team Workspace；Pages；Agent/Skills/MCP 市场。
- **市场体量**（官网 llms.txt，2026-11-21）：Agents 319,538+ / MCP Servers 127,261+ / Skills 361,792+。
- **部署形态**：**Cloud SaaS + 可私有化自建**。自建 = Docker Compose（PostgreSQL / Redis / RustFS / SearXNG / agent gateway），一键 Vercel / Zeabur / Sealos / 阿里云。Enterprise = 私有部署 + 商业授权 + 白标 + 用户管理 + 私有模型 + 审计。
- **定价**（2026-11-22）：Free $0 / Basic $9 / Plus $18 / Pro $90 每月（年付 10% off）；按 **Credits** 计，Free ≈ 50 agent task/月、**$0.01/agent task**。**未发现「Agent 席位」独立计价项**。Workspace 套餐 Free / Pro / Business（共享 credit pool + 成员限额 + 预算池）。限额：每人最多 3 个免费 workspace，同时最多加入 20 个。
- **无自研模型** ⭐：LobeHub Provider 只是转售 OpenAI / Claude / Gemini / Moonshot 系列；Enterprise 的 "Ready for your own model" 是让客户用**自己的数据** post-train **自己的**模型。

### 2.2 组织模型（官方口径 —— 与公众号文章有出入）

官方实体：**Agent（"unit of work"）→ Agent Group / Group Chat → Task → Workspace**。

> ⚠️ **口径纠正**：**官方没有「Personal Agent / 主管 Agent / 执行 Agent」三层命名的描述**。文章里的说法是文彬访谈口述的产品叙事，官方文档对应的机制是 **Agent Group 内置的 Orchestrator**。

- **Orchestrator**（Agent Team 模式）：理解目标并派活、协调发言顺序、总结结论、维持话题。
- **Agent Group 四种模式**：Sequential / Parallel / Iterative / Debate。
- **Agent 岗位要素**（`agent-profile`）：名字 + 头像、模型 + reasoning effort、**Agent Tools 与 User Tools（连接器权限三态：直跑 / 需审批 / 关闭）**、Core Instructions（角色目标·工作方法·响应要求·边界）、Skills、Memory、Resources、Web Search、Channels、Stats；Agent Builder 自动生成整套配置；Publish / Export / Copy to / Move to。
  - **未见独立的「权限矩阵」字段** —— 权限挂在连接器与 Workspace 角色上。
- **交接三条路**：① Orchestrator 派活 ② **Task = 工单**（Assignee 指定 Agent；状态 running / awaiting review / failed / retry；评论线程追问；Artifacts；Acceptance 报告；Scheduled / 固定间隔自动化）③ Group Chat 内消息带 `<author_name>` 标记做 Agent-to-Agent 互评。
- **IM 入口**（覆盖很广）：Discord / Slack / Telegram / LINE / QQ / **WeChat（需付费 plan）** / WeCom / Feishu / Lark / DingTalk / WhatsApp / iMessage。
- **Proactive Bot**（v2.3.0 起默认开）：wake / skip / defer 三态 + **Wake Records 审计面板**。
- **「Lobe Agent Index」= `lobehub/lobe-chat-agents`**（MIT，1,253★，读 index.json 提供 Agent 列表）。
  > ⚠️ **纠正**：`github.com/lobehub/agent-index` **不存在（404）**；CLI 也不在 GitHub（是 npm `@lobehub/cli`）。

### 2.3 运行时与工程架构

- **harness 四层**：Model Runtime / **Agent Runtime（cloud-native, step-level agent loop）** / Context Engine / Environment（Page, Task, Group, IM）。
  - Agent Runtime 是**状态机**，**单步执行 → trace 天然产生**。
- **网关**：参考实现 `device-gateway` / `agent-gateway` 绑 **Cloudflare Workers + Durable Objects**；`lobehub/lobehub-gateway` 是 **Go 重写**，明确**无 Cloudflare Workers / Durable Objects / Redis / PostgreSQL 依赖**。
  > ⚠️ **纠正**：文章里"跑在 Vercel"**只对 Web/API 面成立**，实时设备通道依赖 Cloudflare DO。
  > ⚠️ **纠正**：**未找到官方「队列 + Redis 驱动多步 Agent 循环」的表述**。Redis 的明确用途是自建 GitHub 集成的 OAuth 连接请求 + Docker Compose 组件。
  > ⚠️ **纠正**：**「Remote Tool Calling」不是 LobeHub 官方术语**（文章里文彬用了，但官方文档无此说法）。
- **工具执行面**：Cloud Sandbox（Python / JS / TS、shell、文件生成）、本地终端、Execution Devices（桌面 App / CLI / 浏览器配对）、设备网关下发；**未配置 sandbox 时显式报错，不静默降级**。
- **自改进 harness** ⭐（`lobehub.com/blog/self-evolving-harness`）：
  - 靠 **Agent Operation Tracing**（每次执行落 execution snapshot，**可回放**），开源于 `packages/agent-tracing`；
  - 四个演化维度：**Context strategy / Tool orchestration / Error awareness / Model adaptation**；
  - **9 轮巡检实测**：错误模式累计 31 → 104、**新增模式 31 → 0**、自主发现 20+ 个 harness 缺陷、agent 成功率 ~75% → >95%；自评处于 **L3（agent 主导、人保留判断）**，L4 未达成。
- **主仓 packages/ 实证**：agent-runtime、model-runtime、context-engine、tool-runtime、conversation-flow、**agent-tracing**、agent-manager-runtime、heterogeneous-agents、device-sandbox、chat-adapter-{feishu,dingtalk,wecom,wechat,qq,line,imessage}、builtin-tool-self-iteration、eval-dataset-parser、eval-rubric。

### 2.4 ⭐ Acceptance —— 这条最值钱，且协议干净

`github.com/lobehub/acceptance`：**Apache-2.0**，104★，JavaScript。

- **README 原话**：把请求变成 **observable checks** → **跑真实产品** → 产出含 **截图 / 录屏 / 日志** 的报告链接。
- **检查面**：Web（浏览器）/ CLI（终端）/ Electron / macOS native / iOS Simulator。
- **本地产物**：`.acceptances/` + `report.html`。
- **CLI**：`lh acceptance feedback`（读回评审意见并驱动下一轮）、`lh acceptance publish .acceptances/<subject>`。
- **打回是单条 check 级别**：已通过的 check 保持通过，被打回的 check 保留轮次历史，**你的批注成为下一轮的 lesson**。
- **安装**：`lh acceptance install` / `npx skills add lobehub/acceptance --skill acceptance` / Claude Code plugin。
- **GitHub 集成**（Alpha）：PR 合并 → 关联 acceptance 判通过且 task 完成；CI 失败 → 唤醒开 PR 的 agent（附失败 check + Actions log 尾部），**每个 PR 最多 3 次**，draft PR 不唤醒；review feedback → 仅 repo owner / member / collaborator **及 `chatgpt-codex-connector[bot]`** 能唤醒，作者本人评论忽略。

### 2.5 ⭐ 异构 runtime 纳管（对我们最关键的一条）

- `lh hetero` 支持 **15 个异构 runtime**：**DeepSeek Harness**、Amp、Claude Code、CodeBuddy、Codex、GitHub Copilot、Cursor、Factory Droid、Devin、Grok Build、Kimi Code、OpenCode、Pi、Qoder、TRAE CLI。
- Connect External Agents 文档另列 13 个 coding CLI + 2 个个人 agent 平台，含 **Claude Code、Codex、OpenClaw、Hermes**。
- **ACP 支持**：GitHub Copilot CLI 走 `copilot --acp --stdio`（session/new、session/load、session/set_config_option、session/prompt、session/cancel；权限请求转成 approval card）。
- 官方自述 "next generation of agent harness"，并与 Manus / Claude Cowork / OpenClaw 各有对比页。

### 2.6 ⭐ Benchmark 数据核查（重要纠正）

| 说法 | 核查结论 |
|---|---|
| FrontierHarness v1.0：Codex 66.7%/$3.47、Claude Code 63.3%/$18.34 | ✅ **属实**。但官方是 Runta + Baseten + Z.ai，21–22 harness × 5 模型 × 62 任务 |
| 「**LobeHub** 70% 通过率、$1.68 单任务成本中位数」 | ❌ **未找到任何官方或榜单出处**。**FrontierHarness 榜单中没有 LobeHub**。判定为**未证实，疑与别处数据混拼**。**汇报时不可引用** |
| LobeHub 自有基准 | **Lobe Eval**（2026-09-08）：30 Case × 3 次 = 90 Outcome，Pass³ 主指标，17 个模型配置；榜首 Claude Fable 5.1 = Pass³ 86.7% / Pass¹ 91.1%；**报告无成本列** |

### 2.7 ⭐ 开源 / 闭源边界（决定能不能进交付物）

| 仓库 | 协议 | 可否进客户交付物 |
|---|---|---|
| `lobehub/lobehub`（85,966★） | **LobeHub Community License**（Apache-2.0 + 附加条款） | ⚠️ **不可**：可商用作前后端服务（不改源码）；**基于其开发并对外分发衍生作品须购买商业授权**；贡献者代码可被官方用于商业用途；官方保留调整协议权利。**与 Apple HALO 同一类坑** |
| `lobehub/acceptance` | Apache-2.0 | ✅ **可以直接用**（含改写） |
| `lobehub/lobe-chat-agents` | MIT | ✅ |
| `lobehub/lobe-ui` / `lobe-icons` / `local-replica` | MIT | ✅ |
| `lobehub-typescript` | Apache-2.0 | ✅（OpenAPI SDK） |
| `lobehub-gateway` / `lobe-chat-plugins` / `lobehub-python` | **无 license** | ⚠️ 默认版权，不可直接用 |
| `lobe-vidol` | Apache-2.0 | ✅ |
| `lobe-tts` / `awesome-rsi` | MIT / CC0 | ✅ |
| Workspace（角色 / 共享 credit pool / 预算池） | **Cloud only** | ❌ 闭源 |
| 多玩家实时协作（Rooms） | **Cloud 能力，自建退化为单写者** | ❌ |
| Enterprise 私有化套件 / WeChat 连接 | 商业授权 | ❌ |

### 2.8 仓库清单核实（GitHub API，2026-11-22）

存在：lobehub/lobehub(85,966★, NOASSERTION)、acceptance(104★)、lobe-chat-agents、lobe-chat-plugins(无 license)、local-replica、lobehub-gateway(无 license)、lobe-ui、lobe-icons、awesome-rsi、lobot、lobe-vidol、lobe-tts、lobehub-typescript、lobehub-python(无 license)。
**不存在**：`lobehub/agent-index`（404）、`lobehub/cli`（404，CLI 以 npm `@lobehub/cli` 分发）。

---

## 三、两条路线详细对比

### 3.1 分层定位

```
        ┌──────────────────────────────────────────────────────────────┐
 L4 组织层 │  LobeHub：Workspace / Agent Group / Orchestrator / Task  │
        │  super-agent：Router+Worker / Policy / Ticket / Mandate     │
        ├──────────────────────────────────────────────────────────────┤
 L3 运行时 │  LobeHub：agent-runtime / model-runtime / context-engine  │
        │  dsh：Cordis 插件 / Capability Seam / Profile-Bundle         │
        ├──────────────────────────────────────────────────────────────┤
 L2 执行器 │  Claude Code / Codex / OpenClaw / Hermes / DSH / ...      │
        │  （两边都在这一层做异构纳管 —— ⭐ 同一战场）                    │
        ├──────────────────────────────────────────────────────────────┤
 L1 底座   │  LobeHub：自建（PG/Redis/RustFS/SearXNG/Go gateway/CF DO）│
        │  dsh：Cordis（时空可组合性编程范式, arXiv 2608.25512）        │
        └──────────────────────────────────────────────────────────────┘
```

### 3.2 逐维度对比

| 维度 | **LobeHub** | **DeepSeek Harness / super-agent** |
|---|---|---|
| **形态** | 成品 SaaS + 可自建（企业级组织操作系统） | 开源框架 + 研究原型（架构范式） |
| **官方性** | LobeHub 公司（融资方：LobeChat 团队） | dsh = DeepSeek 官方；super-agent = 官方"研究原型"；DS Bot = 社区项目 |
| **协议** | 主仓 = LobeHub Community License（**衍生分发需商业授权**）；acceptance = Apache-2.0 | dsh = **MIT**；super-agent = **MIT**；DS Bot = **Apache-2.0** |
| **可否进客户交付物** | ⚠️ 主仓不行；零件可以 | ✅ 全部可以 |
| **核心抽象** | Agent / Agent Group / Orchestrator / Task / Workspace | Source / Trigger / Thread / Eval / Mandate / Ticket / Assignment |
| **授权模型** | 连接器三态权限 + Workspace 角色 + Agent 岗位 Core Instructions；**无显式不可变授权对象** | **Policy 版本化 + Mandate 不可变 + Admission 表三档**（explicit / inferred / not admitted） |
| **执行器纳管** | ⭐ `lh hetero` 15 个异构 runtime（含 dsh / OpenClaw / Hermes）+ ACP | dsh 自带 `acp` profile；super-agent 用自己的 DSH Executor + Worker session |
| **多 Agent 协作** | Group Chat 四模式 + Orchestrator + `<author_name>` 互评 + Task 工单 | Router/Worker 两层 + Thread 订阅 + Agent-to-Agent 交接（跨项目提需求） |
| **IM 入口** | ⭐ 12+ 渠道（Discord/Slack/飞书/企微/钉钉/QQ/微信/LINE/iMessage…） | dsh **无** IM 通道（只有 feishu/dingtalk/wecom 的**工作流 connector**）；DS Bot 插件提供群聊 |
| **运行时解耦** | Agent Runtime 状态机 + step-level trace；设备网关（CF DO / Go） | dsh：Cordis 插件 + Profile/Bundle；super-agent：计算/状态/机器分离（云端循环 + 本地 daemon） |
| **多步推进机制** | 官方文档未明确「队列+Redis 驱动」 | dsh：Passes（每 2 秒一轮）+ effect 队列；super-agent：Effect/Outbox 事务内入队、提交后执行 |
| **沙箱/工具执行** | Cloud Sandbox / 本地终端 / Execution Devices / 设备网关下发 | dsh：`ctx.shell` / `ctx.terminals` / `ctx.sandbox` backend 可换；super-agent：Executor 在领域外 |
| **长上下文** | Context Engine（细节未公开） | ⭐ **DS Bot context steward**：就地压缩 checkpoint + 历史 FTS5 可检索 + 用户视角无感 |
| **记忆** | Agent 岗位含 Memory 字段（细节未公开） | ⭐ 三层 scope + 自动审阅 + **"记忆是数据不是指令"** |
| **Secret 安全** | 未见同等级机制公开 | ⭐ `request_secret` + 值永不到达模型 + 保存前/请求前双重遮蔽 |
| **验收闭环** | ⭐⭐ Acceptance（observable checks + 截图/录屏/日志 + 单条打回 + 批注成为下一轮 lesson + GitHub 集成） | observe 模式（只记录不放行）；无自动验收工具 |
| **自改进 harness** | ⭐ Agent Operation Tracing（可回放 snapshot）+ 四维演化 + 9 轮实测（新增错误模式 31→0、成功率 75%→95%） | 无（super-agent 只有 Watchdog 停滞检测） |
| **可观测/审计** | Wake Records 审计面板 + Task/Acceptance 链路 | Event sourcing + `why` 审计链（Autoloop）+ Outbox + Session Log 投影 seam |
| **组织成熟度分级** | ⭐ **自动驾驶 L1–L5**（L1 问答 / L2 个人助手 / L3 团队成员 / L4 自治业务单元 / L5 自演进组织）；自评 **L3**，跨项目提需求已有 L4 雏形 | 无公开分级 |
| **部署** | Cloud SaaS + Docker Compose 自建 + Vercel/Zeabur/Sealos/阿里云一键 | 本地 `npx @deepseek-ai/dsh web`；self-host 需自写 Docker；**本机已部署 0.1.0-rc.6（2026-08-15，公网 :5181）** |
| **商业化** | SaaS 订阅（$0–$90/月）+ Enterprise 私有化 + 白标 | 完全开源，无商业版 |
| **成本** | Credits 计费，$0.01/agent task | 自带模型成本；super-agent Router 决策 1.6–6.4 s/次、缓存 token 多 23%–30% |

### 3.3 两句话概括

> **LobeHub 是「产品化的组织操作系统」：把多 Agent 协作做成了可订阅、可审计、有验收报告的 SaaS，代价是核心闭源 + 商业授权。**
> **DeepSeek 路线是「架构范式开源化」：把人、授权、事件、工单、执行器的关系写成可审计的形式化对象，代价是原型阶段、文档先行、还没有好用的验收工具。**

### 3.4 ⭐ 三条互补性发现（对德勤最有用）

1. **两者在 L2 执行器层是同一战场，且 LobeHub 已经在纳管 Hermes 和 OpenClaw。**
   → 我们的"执行器抽象层"不是空想，**有一个真实的商业对标物已经这么做了**。可以在汇报里直接说：LobeHub 用 `lh hetero` + ACP 把 15 个异构 runtime 纳管，我们要做的是**面向金融/政务交付**的那一版（可审计、可单部署、可私有化）。

2. **LobeHub 的 Acceptance 正好补 DSH/super-agent 最弱的一环（验收），而 DSH 的 Capability Seam / Mandate / context steward 正好补 LobeHub 没公开的骨架。**
   → **两者叠加 ≈ 我们德勤 MVP 的完整目标形态**（组织模型取 super-agent，验收取 Acceptance，执行器抽象取 seam，交付形态取 Profile/Bundle 配置行）。

3. **自律分级 L1–L5 是可以直接搬去跟客户画图的现成框架**（LobeHub 自评 L3，目标 L4/L5）。
   → 德勤交付叙事可以是"我们不只做 L3 的工具，我们要交付让客户自己爬到 L4 的组织能力"。

---

## 四、对德勤的借鉴点（新增，编号接 v1 清单）

| # | 借鉴点 | 落点 | 来源 | 级别 |
|---|---|---|---|---|
| **L-1** | ⭐ **Acceptance 机制**：需求 → observable checks → 跑真实产品 → 截图/录屏/日志报告 → 单条打回 → 批注沉淀为下一轮 lesson | 执行器验收闸门（补内核下限第 9 条"等价性验收"） | LobeHub acceptance（**Apache-2.0，可直接用**） | **P0** |
| **L-2** | **Task = 工单链**：Assignee / 状态(running·awaiting review·failed·retry) / 评论线程 / Artifacts / Acceptance 报告 / Scheduled 自动化 | 内核治理层的工单模型（与 super-agent Ticket 合并） | LobeHub + super-agent | **P0** |
| **L-3** | **Tracing-first 自改进 harness**：每次执行落可回放 snapshot；四维演化（Context strategy / Tool orchestration / Error awareness / Model adaptation）；**新增错误模式 31→0** | 内核可观测性 + 自我优化闭环 | LobeHub `packages/agent-tracing` | **P1** |
| **L-4** | **异构 runtime 纳管 + ACP**：`lh hetero` 纳管 15 个 runtime；ACP session 协议 | 执行器抽象层的**协议选型**：优先 ACP 互通，而不是自造 | LobeHub + dsh `acp` profile | **P1** |
| **L-5** | **自动驾驶 L1–L5 组织成熟度分级** | 客户沟通/交付目标叙事框架 | LobeHub 官方 | **P1** |
| **L-6** | **Wake Records 审计面板 + 主动三态（wake/skip/defer）** | 内核的"主动行为审计"面板 | LobeHub v2.3.0 | **P1** |
| **L-7** | **Orchestrator + Agent Group 四模式（Sequential/Parallel/Iterative/Debate）** | 编排层模式库（DSH/DSH-executor 侧） | LobeHub | **P2** |
| **L-8** | **Agent 岗位 = 名字+模型+工具权限+Core Instructions+Skills+Memory** 的可导出配置 | 执行器/Agent 配置的**交付格式**（可导出 = 可交接给客户） | LobeHub `agent-profile` | **P2** |

### 明确不抄 / 要避的坑

- ❌ **不要 fork `lobehub/lobehub` 作交付底座** → LobeHub Community License 要求衍生分发购买商业授权。
- ❌ **不要引用「LobeHub 70% / $1.68」** → 未证实，FrontierHarness 榜单无 LobeHub。
- ❌ **不要照搬「三层 Agent」当官方架构** → 官方是 Agent / Group+Orchestrator / Task / Workspace；三层是访谈叙事。
- ❌ **不要假设自建版有 Workspace 治理与多人实时协作** → Rooms 是 Cloud 能力，自建退化为单写者。
- ⚠️ **不要把「Vercel 300 秒限制」「队列+Redis 推进」「Remote Tool Calling」当官方事实引用** → 均未在官方文档找到出处；实况是 CF Workers + Durable Objects（参考实现）/ Go 重写（无 CF 依赖）。

---

## 五、vault 已有相关笔记汇总（2026-11-22 清点）

> 结论：**DSH / super-agent 这条线 vault 里已经覆盖得很深（4 篇 + 1 份借鉴清单 + 1 份部署记录）；LobeHub 此前是空白，本篇补上。**

### A. 直接相关（同一条线）

| 笔记 | 位置 | 覆盖了什么 | 状态 |
|---|---|---|---|
| `2026-10-28 - DeepSeek Harness + DS Bot - 架构分析与德勤项目借鉴点.md` | 2-Areas/AI-Agent-研究 | dsh 架构 / Capability Seam / Profile-Bundle / Session Log / 事件三域 / Turn-Step / DS Bot 记忆·secret·context steward / 10 条借鉴点 | ✅ 最全，**口径需按本篇 §1.1 修正** |
| `2026-11-03 - DeepSeek Super-agent - 设计分析与德勤借鉴点.md` | 同上 | super-agent 五块架构 / 领域模型 13 概念 / 消融数据 / 9 篇文档 / 4 个未解问题 / P0-P2 借鉴点 | ✅ 完整 |
| `2026-11-05 - Agent Autoloop × DeepSeek Super-agent - 异同对比.md` | 同上 | Autoloop vs Super-agent 九项相似 + 根本区别 + 体量实测（7.0× / 1.66× 测试比）+ "小内核+厚治理" | ✅ 完整 |
| `2026-11-05 - 德勤 Agent 平台借鉴清单 v1（Autoloop×Super-agent×DSH）.md` | 1-Projects/德勤/AI-Native | 8 条内核下限 + P0×10 / P1×7 / P2×5 + 实测数据表 + 5 条下一步 | ✅ **本篇应升 v2** |
| `2026-11-05 - Agent Autoloop - GitHub 仓库分析.md` + `本机实跑验证记录.md` | 同上 / AI-Agent-研究 | 源码级 + 本机全闭环实跑 | ✅ |
| `current-server/deepseek-harness/README.md` + `部署报告.md` | current-server | **本机已部署** `@deepseek-ai/dsh@0.1.0-rc.6`，pm2 保活，公网 `http://101.33.212.119:5181/dsh/`，源码备份 `/data/.deepseek-harness.bak/` | ✅ 可用（注意：rc.6 已是旧版本） |

### B. 同赛道但不同范式（可作对照）

| 笔记 | 一句话定位 | 与本主题的关系 |
|---|---|---|
| `2026-10-28 - Anthropic Knowledge Work Plugins` | Anthropic 官方「AI Native 组织 Workspace」对标物；123 插件 / 252 skill / 纯文件无代码 / `~~占位符` tool-agnostic / 定制 SOP | ⭐ **组织 Workspace 的官方答案**，与 LobeHub 同为"平台"路线，但走**文件生态**而非**运行时** |
| `2026-11-19 - rust-anything` | 录制—对拍—闸门验收范式（补内核下限第 9 条） | ⭐ 与 Acceptance 同属"验收闸门"，**两份应合并成一条验收基线** |
| `2026-07-25 - Multica` | Claude Code/Codex/OpenClaw/Hermes 之上的 **Agent 团队管理与任务控制平面**（42k★，Go+TS，Modified Apache-2.0 source-available） | ⭐ **与 LobeHub 最像的开源对标物**，许可同样受限 |
| `2026-07-25 - Block Buzz` | Block 的开源人类+Agent 协作工作区（Nostr relay，签名事件统一建模） | 组织协作的另一种底座选型 |
| `2026-10-02 - HiFox` | 多 Agent 统一指挥管理平台（看板 + Jira 双向同步，接入 Claude Code/Codex/OpenClaw/Hermes/Pi） | 看板式任务分派范式 |
| `2026-09-29 - OpenRig` | 离散 Agent 编排层（tmux 持久化 + YAML 拓扑 + MCP 自治集成） | 编排层另一种实现（进程级） |
| `2026-09-29 - OpenRig 部署决策矩阵` | 部署形态选型 | 同上 |
| `2026-08-25 - OpenConnector` | Agent ↔ SaaS 的工具调用层 + **凭据隔离层**（Agent 永远不接触明文密钥） | ⭐ 与 DS Bot 的 secret 遮蔽同题，可合并成"凭证隔离"设计 |
| `2026-08-24 - AI-Native SDLC V-Bounce 模型`（中/英） | AI-Native 研发范式 | 交付流程范式 |
| `2026-09-28 - 零信任 Agent 平台架构图` | 零信任 Agent 架构 | 安全基线参考 |
| `2026-09-25 - AI-Native 研发范式实践手册`（阿里 PDF） | 阿里实践手册 | 甲方视角对标 |
| `2026-11-05 - JevAgentHarness` | 决策模型与 LLM 共享控制权、Wilson 下界阈值拟合 | **我们与 LobeHub"自改进 harness"最可比的一块**（阈值拟合 vs 经验拍板） |
| `2026-08-22 - openai-codex` | Codex 仓库分析 | 执行器之一 |
| `2026-07-30 - Harness Handbook` | 论文核心要点 | harness 概念谱系 |

### C. 明显缺口（vault 里还缺的）

1. **LobeHub 此前零覆盖**（本篇补上）。
2. **没有一篇把"组织级 Agent 平台"横向排过序** —— 现在至少有 5 个可对标物（LobeHub / Multica / HiFox / Anthropic KW Plugins / Block Buzz），散在各处，**建议出一张横评表**。
3. **ACP 协议在 vault 里几乎没有独立笔记** —— LobeHub 与 dsh 都以 ACP 互通，这是跨执行器的事实标准，值得单开一篇。
4. **验收基线目前散在三处**（rust-anything 闸门 / super-agent observe / Acceptance）→ 应合并成德勤"执行器验收基线 v1"。
5. **JevAgentHarness 的阈值拟合 vs LobeHub 的"9 轮巡检"自改进** 两种自改进方法论没有对比过。

---

## 六、建议的下一步

| 优先级 | 动作 |
|---|---|
| 1 | **本机跑一遍 Acceptance**（`lh acceptance install` 或直接 `npx skills add lobehub/acceptance`），用德勤内核 v0.1 的 24 条用例做一轮真实"Agent 自检 + 人工打回"，看能不能替代我们手写的用例报告 |
| 2 | **借鉴清单升 v2**：新增"LobeHub"章节（L-1 ~ L-8 八条），并把 8 条内核下限扩到 **9 条**（加"等价性验收闸门"） |
| 3 | **出「组织级 Agent 平台横评表」**：LobeHub / Multica / HiFox / Anthropic KW Plugins / Block Buzz / dsh+super-agent，维度=开源边界·许可·纳管执行器·IM 入口·授权模型·验收·组织分级·部署形态 |
| 4 | **ACP 单独立一篇**：会话协议 + 权限请求（approval card）+ 为什么它比自造执行器协议更有生命力 |
| 5 | **合并「执行器验收基线 v1」**：Acceptance（可观测证据）+ rust-anything（等价性对拍）+ super-agent observe（首投灰度）三合一 |

---

*编制：2026-11-22。数据源：GitHub API（2026-11-22）+ lobehub.com 官方文档 + deepseek-harness 官方文档 + 赛博禅心公众号（2026-11-01）。所有结论已标口径，未找到出处的均已显式标注"未证实"。*
