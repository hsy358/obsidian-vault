---
type: research
title: PlanWeave - 文件化循环工程系统（开源分析）
source_url: https://github.com/GaosCode/PlanWeave
analyzed_at: 2026-08-18
status: 调研
tags: [agent-framework, task-graph, file-backed, planning, executor-routing, acp]
hermes_relevance: 高（同类解法，可借鉴）
---

# PlanWeave — 文件化循环工程系统（v0.4.0）

> **一句话**：把模糊目标/聊天生成的 plan 转成 task graph（节点=文件、block=文档），每个 block 由专门 agent claim → 走 implement + review 两道关 → 记录每次 run → 整个 loop 可恢复。

---

## 1. 仓库速览

| 字段 | 内容 |
|---|---|
| **仓库** | https://github.com/GaosCode/PlanWeave |
| **版本** | 0.4.0 |
| **License** | MIT |
| **语言/运行时** | TypeScript / Node.js |
| **桌面端** | Electron（task canvas + Auto Run 控件） |
| **CLI** | `@planweave-ai/cli`（npm + Homebrew） |
| **可执行 Agent** | Codex / Claude Code / OpenCode / Pi / Grok（ACP 协议） |
| **发布日期** | 2025（按 v0.4.0 + MCP tunnel 设计推断近一年成熟） |
| **作者** | GaosCode |

---

## 2. 核心架构（5 层）

```
┌─────────────────────────────────────────────────┐
│  PlanWeave Desktop / CLI（前端 + 运行时）        │
├─────────────────────────────────────────────────┤
│  MCP Server（HTTP，本地 loopback）               │  ← ChatGPT/Web 接入点
├─────────────────────────────────────────────────┤
│  Plan Package（文件化项目模型）                   │
│   ├─ Canvas（画布，多个并行任务域）               │
│   ├─ Task（任务节点，含依赖）                     │
│   ├─ Block（实现/审查/反馈原子单元）              │
│   └─ project-graph.json（画布级依赖权威）         │
├─────────────────────────────────────────────────┤
│  Skills（7 个角色技能）                          │
│   plan-maker / plan-importer / plan-auditor      │  ← 上游：plan 构造
│   plan-coordinator（dispatcher only）            │  ← 中游：调度
│   plan-runner / plan-reviewer / plan-recovery    │  ← 下游：执行
├─────────────────────────────────────────────────┤
│  Executor Runtime                                │
│   ├─ ACP runners（codex-acp / claude-code-acp / opencode-acp / pi-acp / grok-acp）
│   ├─ Local review scripts（确定性检查）           │
│   └─ Manual（路由回当前 agent 的 native subagent）│
├─────────────────────────────────────────────────┤
│  Agent Host（远程设备）                          │  ← 跨设备 agent endpoint
└─────────────────────────────────────────────────┘
```

### 2.1 关键设计原则（README 直接引用）

> "**Files are nodes, documents are blocks**: the graph is not a decoration on top of chat. It is the project model."

- **Graph 是项目模型，不是聊天的装饰**
- **Scoped graph context**：agent 只看到当前 block + 相关图上下文（避免脏上下文）
- **Focused responsibilities**：每次 claim 只发一个 block 给一个 agent（避免无关 plan / 陈旧讨论 / 浪费 token）
- **Per-node and per-block agent routing**：不同 block 可走不同 executor
- **Review and feedback as first-class work**：review block 可产生结构化 feedback → 回到 implementation block
- **Local-first and file-backed**：plan、prompt、run record、artifact 全在 workspace 可查

---

## 3. 7 个 Skill（角色拆分）

### 3.1 上游：Plan 构造

| Skill | 职责 |
|---|---|
| `plan-maker` | 从模糊目标/稀疏 codebase → 写出 package-shaped draft → 走 validate/quality/import |
| `plan-importer` | 从 PRD/roadmap/issue/architecture notes 等**强源文档** → draft → validate → import |
| `plan-auditor` | 对已写好的 plan 做：覆盖度、lifecycle gap、contract drift、弱 prompt、**不可验证的完成标准**审查 |

> ⚠️ 注意 `plan-auditor` 的核心检查项之一就是"**unverifiable completion criteria**"——这跟何大人的 Goal-Driven Execution 里"verifiable goal"是同款理念。

### 3.2 中游：调度（核心 dispatcher）

**`plan-coordinator` 的铁律**（直接抄自 SKILL.md）：

> "The coordinator thread is a **dispatcher only**: it must not implement blocks, review gates, feedback fixes, edit target source files, edit Plan Package files, or write implementation/review artifacts itself."

> "`plan-runner`, `plan-reviewer`, and `plan-recovery` are role instructions for **worker subagents**. They are not permission for the coordinator to switch roles inside the same thread."

这是最值得我们抄的一条 —— **明确禁止 coordinator 多重角色混淆**。

### 3.3 下游：执行（worker 角色）

| Skill | 职责 |
|---|---|
| `plan-runner` | 执行**一个** implementation block → 出具 completion report |
| `plan-reviewer` | 执行**一个** review gate → 出具 `passed` / `needs_changes` 结构化结果 |
| `plan-recovery` | 处理 doctor findings / stale current refs / orphan results / state drift / blocked / diverged / submit retry |

> ⚠️ **plan-recovery 不能包含 implementation 或 review 工作**（明文规定）—— 这条边界也比很多 Agent 框架清晰。

---

## 4. Subagent Packet（dispatcher → worker 的 handoff 标准）

`plan-coordinator` 给每个 worker subagent 的 handoff 必须包含 10 项：

1. **explicit instruction**：`Use skill: plan-runner / plan-reviewer / plan-recovery`
2. **block ref 或 feedback id**
3. **claim ownership**：`already claimed` 或 `claim required`
4. **block type + expected skill**
5. **effective executor + 为什么选它**
6. **rendered prompt 路径/内容 + source prompt paths**
7. **expected report/result artifact**
8. **submit command 或 return 指令**
9. **validation commands / observable completion criteria**
10. **scope boundaries + 不要碰的文件清单**

> 💡 **借鉴价值**：这就是 Hermes dispatcher 缺的那块"subagent 契约"。我们现在的 Hermes 任务 description 是自由文本，应该升级成结构化 Packet。

---

## 5. Executor Routing（最聪明的设计）

```text
claim / claim-next → 读 effectiveExecutor 字段
   ├─ manual        → 路由到 current agent 的 native subagent
   ├─ = current     → 同上（不通过 PlanWeave runner）
   └─ ≠ current     → PlanWeave runtime 接管（ACP runner）
```

**关键规则**：
- 如果 effectiveExecutor 是 manual 或当前 agent → 走 native subagent 链路
- 如果是其他 agent → 走 PlanWeave runtime + ACP runner
- **`plan-runner` 只在 manual 或 current-agent 场景下分配**（明文禁止在非当前 executor 上自审自跑）
- **不要把 review gate 发给 current-agent 的 implementation subagent**
- **非当前 executor 失败时不要 fallback 到当前 agent**（除非用户显式授权）—— 这避免了"我自己的 agent 假装成功了"

> ⚠️ 这条 "**don't fall back to current agent on executor failure**" 是德勤 MVP 里要重点借鉴的 —— Hermes 当前 dispatcher 在执行器失败时是直接 fallback 到主进程手动跑，会污染上下文。

---

## 6. Claim Ownership 协议

`already claimed` vs `claim required`：
- coordinator 已经 claim → subagent 不再 claim/claim-next（防止双重认领）
- 必须 subagent 自己 claim → 给出**精确 ref/task**，claim 错就停

> 💡 借鉴：Hermes kanban 当前是"dispatcher claim → 直接交给 subagent"，没有显式所有权传递。可以加一个 `claim_ownership` 字段。

---

## 7. Coordinator Loop（dispatcher 循环）

1. Check current and status **before claiming**
2. Prefer explicit claims (known refs) > automatic claim (let PlanWeave choose)
3. Preview with `claim-next --dry-run --json` before real claim
4. For each assigned item, record: ref, task, block type, effective executor, prompt source, submit command, agent owner
5. Keep only active subagents running; close completed after report submission
6. **Re-run status/current after every submit**, before assigning more work
7. If `blocked` / `diverged` / stale → **stop dispatching dependent work**, route to recovery

> 💡 第 6 条"每次 submit 后再 check status" 防止"派出去一堆但不知道谁完成了" —— Hermes kanban 当前缺少这个 sanity check。

---

## 8. NEEDS_COORDINATOR Fallback（关键设计）

`plan-runner` 和 `plan-reviewer` 在以下场景**必须停手并返回 NEEDS_COORDINATOR**：

- prompt 是空的 / 矛盾的 / 过时的 / 被 blocked / diverged / 指向不存在的 source
- assigned block 因 plan 缺陷（bad dependencies / missing prompts / invalid acceptance / wrong review gate / stale task scope）无法完成
- `effectiveExecutor` 是 manual 或 current agent 但**没有 native subagent tool 可用**

> 💡 这是一种**诚实的失败信号**——子 agent 不会装作成功，而是显式升级。这跟何大人的"verifiable goal + 失败标准"理念完全一致。

---

## 9. ACP（Agent Client Protocol）支持

显式支持的 ACP profile：
- `codex-acp`
- `claude-code-acp`
- `opencode-acp`
- `pi-acp`
- `grok-acp`

ACP preflight 自动协商认证方式（用 agent 已配置的 non-interactive credentials）。如果需要用户交互，CLI/Desktop 显式展示下一步，**不会自动启动交互登录**。

> ✅ **不持久化 agent credential 到 run metadata**（隐私设计，重要）

> 💡 **这跟 AgentSpace 里的 AgentRouter 是同款理念** —— 把 Claude Code / Codex / OpenClaw / Hermes 都当可插拔执行器，通过 ACP/HTTP 协议统一调度。

---

## 10. 与 Hermes v0.14 对比表（核心参照）

| 维度 | PlanWeave | Hermes v0.14 | 借鉴优先级 |
|---|---|---|---|
| **Plan 模型** | 文件化 graph（canvas/task/block/project-graph.json）| Kanban board（任务扁平） | 🟡 中（graph 是更强的表达，但需要重构） |
| **Dispatcher 角色** | 显式 dispatcher only（禁止自执行）| Hermes dispatcher 同样是 dispatcher，但**没有强制隔离** | 🔴 高（必须抄） |
| **Worker 角色技能** | 7 个独立 SKILL.md（plan-maker / coordinator / runner / reviewer / recovery 等） | 主要靠任务 description 字符串驱动 | 🔴 高（拆 skill） |
| **Subagent Packet** | 10 项结构化 handoff | 自由文本任务描述 | 🔴 高（结构化） |
| **Claim Ownership** | `already claimed` / `claim required` 显式协议 | dispatcher claim 后直接交 | 🟡 中（加字段） |
| **Executor Routing** | block 级别 effectiveExecutor → manual/current/non-current 三态路由 | dispatcher 直接调用，executor 选择未结构化 | 🔴 高（这是德勤 MVP 重点） |
| **Review 反馈回路** | review block → structured feedback → 回到 implementation block | 没有显式 review gate | 🟡 中（先跑 MVP 再加） |
| **NEEDS_COORDINATOR 升级** | worker 显式 fallback 信号 | 当前没有此机制 | 🔴 高（最值得抄） |
| **跨设备 Agent Host** | 支持（远程设备登记 + Agent Endpoint）| 无 | ⚪ 远期 |
| **可视化** | Electron Desktop canvas（实时任务图）| 文本界面 | ⚪ 远期 |
| **本地优先 + 文件化** | ✅ 所有 run 写到 workspace | 部分（Hermes kanban 是数据库） | 🟡 中 |

---

## 11. 5 个可立刻借鉴到 Hermes 的设计点

### 借鉴 1：Coordinator Dispatcher-Only 铁律 🟥
- **现在**：Hermes dispatcher 偶尔会自审自跑（任务描述模糊时 fallback）
- **抄**：写进 `~/.hermes/AGENTS.md` 或 dispatcher 的 system prompt："你只负责路由，禁止直接执行 implementation/review/recovery"
- **落地**：1 小时（改 prompt 即可）

### 借鉴 2：Subagent Packet 结构化 Handoff 🟧
- **现在**：Hermes 任务 description 是 markdown 自由文本
- **抄**：把 task description 模板改成 10 字段结构化 Packet（ref / claim_ownership / block_type / effective_executor / prompt_path / expected_artifact / submit_command / validation / scope / files_not_to_touch）
- **落地**：半天（改 kanban schema + dispatcher 拆字段）
- **收益**：dispatcher 出错率 ↓、人工 review 友好度 ↑、下游 agent 不再"猜任务"

### 借鉴 3：NEEDS_COORDINATOR Fallback 信号 🟧
- **现在**：Hermes worker agent 失败时只输出错误，不显式升级
- **抄**：在每个 worker agent 的 prompt 里加："如果遇到 X 类情况，输出 `NEEDS_COORDINATOR: <原因>` 并立即停手"
- **落地**：2 小时（改 3 个 agent prompt）
- **收益**：失败可观察、可决策；不会"装作成功"

### 借鉴 4：Effective Executor Routing（三态） 🟧
- **现在**：Hermes dispatcher 自己决定用什么 executor，没有 block 级别 override
- **抄**：在 Hermes kanban task 上加 `effective_executor` 字段（值：`manual` / `hermes` / `codex` / `claude-code` / `openclaw` 等），dispatcher 据此路由
- **落地**：1 天（schema + dispatcher 改造）
- **收益**：德勤 MVP 的"执行器抽象层"有了具体参考实现

### 借鉴 5：Re-check Status After Every Submit 🟨
- **现在**：Hermes dispatcher 派出去就忘，靠 cron/timer 回收
- **抄**：dispatcher 在每次 submit 完成后**主动** `hermes status` + `hermes current` 再派下一个
- **落地**：半天（dispatcher 加 hook）
- **收益**：避免并发踩踏、状态一致性

---

## 12. 不需要借鉴的部分

| PlanWeave 特性 | 不抄理由 |
|---|---|
| Electron Desktop 桌面 GUI | 德勤 MVP 是 CLI/API 优先；GUI 远期可选 |
| ChatGPT MCP tunnel | 我们用 OpenClaw 主连微信，不需要 ChatGPT 桥接 |
| Plan package 文件化（manifest.json/project-graph.json 等）| 太重，Hermes kanban 用数据库足够；除非未来需要 file-driven 重放 |
| Multi-canvas 跨画布依赖 | 现阶段 MVP 跑 1-2 个 canvas 就够，graph 复杂度反而是负担 |
| 协作 + 多成员 assignment | 德勤 MVP 内部团队规模小，Hermes 单一用户跑 |

---

## 13. 立即可行动作（给何大人参考）

按 ROI 排序：

| # | 动作 | 工作量 | 收益 | 建议时机 |
|---|---|---|---|---|
| 1 | 把 Hermes dispatcher prompt 改成"dispatcher only" | 1 h | 防自审自跑 | 本周 |
| 2 | 给 Hermes worker agent 加 NEEDS_COORDINATOR 信号 | 2 h | 失败可观察 | 本周 |
| 3 | 升级 Hermes task schema 加 10 字段 Packet | 0.5 d | 结构化 handoff | 下周 |
| 4 | 给 Hermes task 加 `effective_executor` 字段 + dispatcher 三态路由 | 1 d | 执行器抽象层有参考 | 下周 |
| 5 | 写一份 `hermes-dispatcher-architecture.md` 对照 PlanWeave | 4 h | 设计沉淀 | 本周 |

---

## 14. 参考链接

- **GitHub 主页**：https://github.com/GaosCode/PlanWeave
- **README（英）**：https://raw.githubusercontent.com/GaosCode/PlanWeave/main/README.md
- **README（中文）**：https://github.com/GaosCode/PlanWeave/blob/main/readme/README.zh-CN.md
- **DEVELOPMENT.md**：https://github.com/GaosCode/PlanWeave/blob/main/DEVELOPMENT.md
- **Skills 目录**：https://github.com/GaosCode/PlanWeave/tree/main/skills
  - `plan-coordinator/SKILL.md`
  - `plan-runner/SKILL.md`
  - `plan-reviewer/SKILL.md`
  - `plan-recovery/SKILL.md`
  - `plan-maker/SKILL.md`
  - `plan-importer/SKILL.md`
  - `plan-auditor/SKILL.md`
- **ACP Agent Host**：https://github.com/GaosCode/PlanWeave/blob/main/packages/agent-host/README.md
- **Releases（Desktop）**：https://github.com/GaosCode/PlanWeave/releases