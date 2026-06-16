---
title: "OpenSpec + Superpowers workflow orchestrator（OpenFlow）：连接需求与工程的工作流编排器"
author: "幽人"
publish_date: "2026-05-15 11:12:56"
saved_date: "2026-06-03"
source: "wechat"
url: "https://mp.weixin.qq.com/s/8PT7nlj-Jcu8Xa6lwyApYQ"
type: wechat-article
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
  source_url: https://mp.weixin.qq.com/s/8PT7nlj-Jcu8Xa6lwyApYQ
---
# OpenSpec + Superpowers workflow orchestrator（OpenFlow）：连接需求与工程的工作流编排器
> 本文基于 GitHub 仓库 lininn/openflow 源码与文档进行深度分析

---

## 引言

在软件开发的漫长历史中，需求与实现之间的鸿沟始终是困扰团队的核心问题。需求文档往往以自然语言描述，抽象且模糊；而工程实现需要精确的代码、可验证的步骤、明确的交付物。当 AI 编程助手逐渐成为主流工具时，如何让 AI 理解需求、生成规格、继而完成可工作的代码？这需要一个结构化的桥梁。

OpenFlow 正是为解决这一痛点而生的工具。它是一个基于 OpenSpec 与 Superpowers 的工作流编排器，通过命令行接口与 AI Agent 技能（Skills）的配合，将需求捕获、规格生成、工程实现与验证归档串联成一条完整的流水线。

---

## 一、OpenFlow 是什么

### 1.1 核心定位

OpenFlow 的官方定义是：

> OpenSpec + Superpowers workflow orchestrator — bridging requirements specs and engineering execution, eliminating the format gap.

翻译过来：OpenFlow 是连接需求规格与工程执行的工作流编排器，消除两者之间的格式鸿沟。

从技术实现角度看，OpenFlow 是一个 npm 全局包 (`@lininn/openflow`)，通过 CLI 命令提供工作流管理能力。它并不嵌入 OpenSpec 或 Superpowers 的代码，而是一个独立的编排层，通过调用这两个工具的 CLI 与技能来完成完整的开发流程。

### 1.2 解决的问题

在没有统一工作流的情况下，AI 编程助手面临几个典型困境：

- • **需求模糊**：用户说"做一个贪吃蛇游戏"，AI 需要自行猜测技术栈、复杂度、边界条件
- • **规格缺失**：没有结构化的设计文档，代码写到一半发现需求变了
- • **进度不明**：做到哪里了？哪些功能已完成？哪些待验证？
- • **验收困难**：如何确认代码实现了设计？设计变更是否同步到代码？
OpenFlow 通过五个阶段的强制流程解决这些问题：每个阶段产出明确的文档，下一阶段基于上一阶段的产出继续，确保需求不丢失、变更可追溯。

---

## 二、核心架构

### 2.1 技术栈

OpenFlow 本身使用 TypeScript 开发（约占 98.6%），少量 JavaScript（约 1.4%）。这与其"CLI 工具 + AI Agent 技能"的定位相符——需要可靠的结构化代码，同时保持与各种 AI 平台的兼容性。

核心依赖包括：

- • **OpenSpec**：生成结构化规格文档（proposal.md, design.md, specs/, tasks.md）
- • **Superpowers**：提供 implementation planning 与执行能力

### 2.2 目录结构

克隆仓库后，主要目录结构如下：

```
openflow/├── .claude/              # Claude Code 技能配置├── .omc/                 # 项目配置（会话与记忆存储）├── bin/                  # CLI 入口脚本├── openspec/             # OpenSpec 规格模板│   └── changes/          # 变更目录结构├── scripts/              # 构建/辅助脚本├── src/                  # TypeScript 源码├── templates/            # 工作流模板├── package.json          # npm 包配置├── tsconfig.json         # TypeScript 配置├── CLAUDE.md             # Claude Code 行为指引├── AGENTS.md             # Agent 配置└── README.md             # 项目文档
```

这个结构体现了几个关键设计决策：

- 1. **CLI 优先**：bin/ 目录存放可执行入口，package.json 声明全局安装
- 2. **模板驱动**：templates/ 和 openspec/ 存放各阶段的文档模板，确保产出格式一致
- 3. **平台兼容**：.claude/ 目录存放 Claude Code 技能，.omc/ 目录存放 会话与记忆存储 配置，通过 `--tools` 参数支持多平台技能生成（Claude Code、Codex、Cursor），体现了"编排层"而非"绑定层"的定位

### 2.3 双层依赖检测机制

OpenFlow 的一大特色是"优雅降级"策略。它不强制依赖 OpenSpec 或 Superpowers，而是在两个层面进行检测：

**Init 时检测**：

- • 检测 OpenSpec → 引导安装
- • 检测 Superpowers → 显示安装提示
- • 即使缺失，技能文件仍然生成，只是部分功能需手动执行
**运行时检测**：

- • 每个 SKILL.md 文件中注入依赖检查逻辑
- • Build 阶段发现缺失 Superpowers 时，自动降级为手动按步骤执行
这种设计的核心理念是：**让工具先能用，再逐步完善**。开发者可以先用最简单的模式跑通流程，后续再安装完整依赖获得自动化能力。

---

## 三、工作流详解

OpenFlow 将软件开发划分为五个阶段，每个阶段对应一个 `/openflow` 子命令：

命令

阶段

描述

`/openflow proposal`proposal

轻量需求捕获 — 通过 3-5 个问题快速收敛需求

`/openflow brainstorming`brainstorming

深度设计 — 多轮权衡探索

`/openflow spec`spec

生成规格 + 自动翻译为 plan-ready.md

`/openflow build`build

执行实现（调用 Superpowers）

`/openflow close`close

验证一致性 + 归档

### 3.1 Proposal 阶段：需求的起点

**目标**：用最少的提问，把用户脑子里的需求变成可执行的变更描述。

**产出**：proposal.md

**关键问题设计**（3-5 个）：

- 1. 做什么 — 你想实现什么功能/变更？
- 2. 为什么 — 解决什么问题？给谁用的？
- 3. 成功标准 — 怎样算做完了？验收条件是什么？
- 4. 边界 — 什么不在范围内？
- 5. 现有约束 — 技术栈、兼容性、时间上的限制？
这些问题看似简单，实则抓住了需求的核心：功能意图、业务价值、验收条件、范围边界、技术约束。任何跳过这些问题的实现，都容易在中途发现"原来用户想要的是另一回事"。

**输出格式**：

```
# Proposal: <变更名>## 需求概述...## 详细描述### 1. 做什么### 2. 为什么### 3. 成功标准### 4. 边界### 5. 技术约束
```

### 3.2 Brainstorming 阶段：深度设计

**目标**：对于复杂需求，进行多轮权衡探索，挖掘隐藏的决策点。

与 proposal 的"快速收敛"不同，brainstorming 允许需求在早期保持一定的"模糊性"，通过多轮对话逐步澄清技术选型、架构决策、边界条件等。

**典型场景**：

- • 新功能涉及多个子系统，如何划分模块边界？
- • 性能要求与代码可维护性冲突，如何权衡？
- • 技术栈选型，A 方案成熟但灵活性差，B 方案现代但生态弱，如何选择？
这个阶段不追求产出完整文档，而是产出"决策记录"——记录每个关键决策的背景、选项、选择理由。

### 3.3 Spec 阶段：规格生成与翻译

**目标**：调用 OpenSpec 生成完整规格文档，并将之翻译为 Superpowers 可执行的 plan-ready.md。

这是 OpenFlow 的核心创新点：**翻译层**。

OpenSpec 生成的规格文档面向"人"阅读——设计决策、技术选型、任务清单。这些文档结构严谨、内容详尽，但对"执行"不够友好。

plan-ready.md 则是面向"机器执行"的格式：

- • 每个 OpenSpec Task 拆成 2-5 个细粒度步骤（对应 2-5 分钟工作量）
- • 每个步骤必须指明改哪个文件
- • 每个步骤必须有验证方式
- • 按执行依赖排序（不是按功能模块排序）
- • 记录来源路径，方便回溯
翻译层的存在，使得"规格"与"实现"之间的 gap 被弥合。规格文档不再是"写完就被遗忘"的静态文档，而是可以被逐条执行的行动清单。

**产出文件**：

```
openspec/changes/<变更名>/├── proposal.md         # 需求├── design.md           # 技术方案├── specs/              # 细项规格（多个 md 文件）│   ├── 01-canvas.md│   ├── 02-snake.md│   └── ...├── tasks.md            # 任务清单└── plan-ready.md       # 翻译后的执行计划
```

### 3.4 Build 阶段：执行实现

**目标**：按照 plan-ready.md 执行代码实现。

**执行流程**：

- 1. **TDD 铁律**：先写失败测试，再写实现代码（注意：这适用于有测试框架的项目，简单的单文件 HTML 项目可跳过）
- 2. **每个 task 一个 commit**：保持提交粒度细、可追溯
- 3. **多任务可派子代理并行**：复杂项目可并行执行独立任务
- 4. **编译/测试不通过不让提交**：质量门槛
**断点恢复**：

Build 阶段支持中断后继续。实现计划文件（存放于 `docs/superpowers/plans/` 目录或直接使用 `openspec/changes/<变更名>/plan-ready.md`）中用 checkbox 标记任务状态，全部勾选即表示完成。中断后再次执行 openflow build 时，会检查这些文件，从未完成的 task 继续。

### 3.5 Close 阶段：验证与归档

**目标**：验证代码实现与设计文档一致，确认规格变更全部体现，然后归档。

**验证维度**：

- 1. **设计一致性**：逐项检查 design.md 中的技术决策是否在代码中体现
- 2. **规格完整性**：检查 specs/ 目录中每个规格变更是否已实现
**处理不一致**：

Close 阶段的核心原则是"不改代码，只记录问题"。发现不一致时：

- • 记录到 `openspec/changes/<变更名>/close-issues.md`
- • 询问用户：是否需要开启新变更来修复？
这种设计避免了"边验证边改需求"的恶性循环，确保每个变更的生命周期是封闭的。

**归档操作**：

```
# OpenSpec CLI 可用时openspec archive <变更名># 手动归档mv openspec/changes/<变更名> openspec/changes/archive/<日期>-<变更名>/
```

---

## 四、CLI 命令详解

安装 OpenFlow 后，可用的命令如下：

```
# 初始化项目openflow init --tools claude,codex,cursor,opencode# 检查状态openflow status# 更新技能openflow update
```

### 4.1 init 命令

```
cd your-projectopenflow init --tools claude
```

init 命令会执行一系列自动化操作：

- 1. 检测并引导 OpenSpec CLI 安装
- 2. 检测 Superpowers 并显示安装提示
- 3. 检查项目是否已初始化 OpenSpec
- 4. 生成 openflow 技能到 `.claude/skills/openflow/`
`--tools` 参数指定目标 AI 平台，支持逗号分隔多个值（claude, codex, cursor，opencode）。这体现了 OpenFlow 的平台无关性——它不是只绑定某一个 AI 助手。

### 4.2 status 命令

显示依赖安装状态与项目中活跃的变更。帮助用户快速了解：

- • OpenSpec/Superpowers 是否已安装？
- • 当前有哪些正在进行中的变更？

### 4.3 update 命令

当 npm 包升级后，重新生成项目技能。确保本地技能与最新版本同步。

---

## 五、与类似工具的对比

### 5.1 传统项目管理工具

Jira、Linear 等工具管理的是"任务"——Ticket、子任务、看板。它们不关心需求如何转化为代码，也不关心 AI 如何参与这个过程。

OpenFlow 的关注点是"需求到代码的转化过程"，这是传统工具不涉及的层面。

### 5.2 AI 编程框架

LangChain、AutoGPT 等框架关注的是"如何让 AI 完成任务"。它们处理的是"给定一个目标，AI 如何自主完成"，但不关心这个目标是怎么来的、怎么验证的。

OpenFlow 处理的是"目标如何定义"与"完成质量如何验证"，这是上游与下游的关系。

### 5.3 其他工作流编排器

工具

关注点

与 OpenFlow 的关系

Inngest

事件驱动的工作流

互补（执行层）

Orchflow

多 Agent 任务编排

互补（任务分发层）

AgentLoom

多 Agent 应用编排

互补（运行时层）

Sheenflow

数据管道编排

互补（数据层）

OpenFlow 的独特之处在于：**它不执行代码，它编排的是"人（或 AI）如何写代码"的过程**。它是一个"元工具"——管理其他工具的工作流程。

---

## 六、实际使用案例

为了更好地理解 OpenFlow 的工作方式，我们以一个假想的项目为例，完整走一遍流程。

### 场景：开发一个 Todo 应用

**用户需求**："帮我做个 Todo 应用"

**Proposal 阶段**：

```
问题 1: 这个 Todo 应用有什么功能？用户: 能添加、删除、标记完成问题 2: 需要什么技术栈？用户: Web 技术就行问题 3: 成功标准是什么？用户: 能正常添加删除就行→ 生成 proposal.md
```

**Spec 阶段**：

```
设计决策：- 单页应用，localStorage 持久化- 纯前端，无需后端生成文件：- design.md: 技术方案- specs/01-storage.md: 存储逻辑- specs/02-ui.md: 界面组件- tasks.md: 任务清单- plan-ready.md: 执行计划
```

**Build 阶段**：

```
按 plan-ready.md 逐步执行：- [ ] 创建 HTML 骨架- [ ] 实现 localStorage 封装- [ ] 实现添加功能- [ ] 实现删除功能- [ ] 实现标记完成- [ ] 验证所有功能
```

**Close 阶段**：

```
验证：- design.md 中的技术决策是否在代码中体现？- specs/ 中的每个功能是否已实现？归档：- 移至 archive/2026-01-15-todo-app/
```

---

## 七、设计哲学

### 7.1 格式即契约

OpenFlow 的核心信条是：**格式即契约**。

每个阶段产出的文档都有明确的格式要求。proposal.md 必须是那样的结构，plan-ready.md 必须是这样的格式。这种"格式强制"带来的好处是：

- • AI 可以准确理解要做什么
- • 人类可以快速检查产出是否符合预期
- • 不同项目之间可以对比进度

### 7.2 不改规格，只记录问题

Close 阶段的一个核心原则是"不在这个阶段改代码"。发现不一致时，记录到 close-issues.md，留给下一个变更处理。

这避免了一个常见的陷阱：验证过程中发现问题，顺手改了，然后忘记记录。长期下来，"设计文档"与"实际代码"之间的差异越来越大，最终文档完全失去参考价值。

### 7.3 优雅降级

"没有 OpenSpec？手动创建目录。没有 Superpowers？手动执行步骤。"

这种降级策略让工具始终可用，即使在最简陋的环境下也能跑通流程。开发者可以先关注"流程跑通"，再逐步完善"自动化程度"。

### 7.4 平台无关

OpenFlow 通过 `--tools` 参数支持多种 AI 平台（Claude Code、Codex、Cursor）的技能生成。它本身不与某一特定平台绑定，技能文件根据指定的平台生成相应格式。这种设计确保了技术选型的灵活性——用户可以根据团队实际使用的工具来配置。

---

## 八、局限性与适用场景

### 8.1 局限性

OpenFlow 不是万能的，有一些天然的局限：

- 1. **对简单项目略重**：对于"改一个 typo"这种微小变更，完整的五阶段流程过于繁琐
- 2. **依赖人工输入质量**：Proposal 阶段的问题设计依赖于提问者的经验，问题不好答案就不会好
- 3. **AI 能力依赖**：Build 阶段的成功很大程度上取决于 AI 的代码能力，AI 写不好，再好的流程也救不回来
- 4. **文档维护成本**：每个变更都生成一堆文档，需要团队有文档文化

### 8.2 适用场景

OpenFlow 最适合：

- • **中等复杂度项目**：功能点较多，需要结构化需求
- • **AI 辅助开发**：团队使用 Claude Code、Codex 等 AI 助手
- • **需求易变场景**：需要清晰追踪需求变更
- • **多人协作**：需要统一的需求传递格式
对于极其简单的脚本修改，或者完全不需要 AI 的纯人工项目，OpenFlow 反而增加了不必要的开销。

---

## 九、总结

OpenFlow 的价值在于：**它为 AI 编程时代重新定义了"需求到代码"的桥梁**。

传统的软件工程中，这个桥梁是需求文档、设计会议、任务分配。现在，这个桥梁可以是一系列结构化的 Markdown 文件，外加一个编排它们的 CLI 工具。

它的核心贡献不是"自动化"——毕竟手动也能跑通流程。它的核心贡献是"结构化"——让每个阶段的产出都有格式约束、让每个决策都有文档记录、让变更的生命周期清晰可追溯。

当 AI 成为编程的主力军时，如何让 AI 理解人的意图、如何验证 AI 的产出、如何管理 AI 生成的代码？这些问题会越来越重要。OpenFlow 是一次有意义的探索——它不一定是最完美的答案，但它指出了一个方向。

---

## 参考资料

- • OpenFlow GitHub 仓库
- • OpenSpec 项目
- • Superpowers 项目
