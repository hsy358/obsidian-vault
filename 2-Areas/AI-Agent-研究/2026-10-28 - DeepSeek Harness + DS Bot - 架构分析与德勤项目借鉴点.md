---
type: note
title: DeepSeek Harness (dsh) + DS Bot 插件 —— 架构分析与德勤项目借鉴点
date: 2026-10-28
tags: [AI-Agent, 开源分析, deepseek, harness, 插件架构, cordis, capability-seam, 德勤项目]
source: 何大人提供（视频中发现）→ 自主抓取分析
status: 已分析
---

# DeepSeek Harness + DS Bot：架构分析与德勤项目借鉴点

> 来源：何大人看视频时发现，给了两个地址
> - 插件本体（DS Bot）：`https://github.com/FeiZhuLulu/DeepSeek-Bot` → **实际重定向到 `https://github.com/Fei2411/DS-Bot`**
> - 宿主框架（DSH）：`https://github.com/deepseek-ai/deepseek-harness`
>
> ⚠️ 何大人给的插件地址是**旧名**，已改名。记笔记时以 `Fei2411/DS-Bot` 为准。

---

## 一句话结论

**DSH 是目前开源 Agent 框架里把"可插拔执行器"做得最彻底的一个**——它的 "Everything is a Plugin" + **Capability Seam** 三角色模型，正是德勤项目「执行器抽象层」可以直接借鉴的**设计范式**。

而 DS Bot 作为 DSH 上的插件，**其致谢名单里明确点名了 Hermes Agent / Hermes Bot Mode**，借鉴点是"每群成员一个独立 session + 交接时携带此前用户消息"。这对何大人 6-29 定的「Hermes 为德勤唯一框架」路线是**佐证**，不是替代。

---

## 一、DeepSeek Harness (dsh) 架构

### 1.1 定位

- 官方开源的 agent harness，MIT 协议
- 论文标题：**"DeepSeek Harness: Everything is a Plugin"**
- 底层是 **[Cordis](https://github.com/cordiverse/cordis)** 框架，设计出自论文 *A Programming Paradigm for Spatiotemporal Composability*（arxiv 2608.25512）
- 状态：**developer preview，迭代极快，会有 breaking change**
- 文档：https://deepseek-harness.github.io/deepseek-harness/
- 启动：`npx @deepseek-ai/dsh web` → 默认 `http://127.0.0.1:3080`

### 1.2 核心理念：没有特权内核

> **"There is no privileged core to patch"**

**每一个部分都是插件**——包括模型适配器、工具注册表、session log、agent loop 本身。所以每一块都能从配置里替换掉。

插件通过 Cordis 的 shared context 贡献三样东西：
1. **Services**（服务）
2. **Typed events**（类型化事件）
3. **Reversible effects**（可回滚的副作用 —— 插件卸载时自动回滚）

### 1.3 Profile / Bundle —— 配置分层（借鉴价值高）

| 概念 | 含义 |
|---|---|
| **Profile** | 具名的组合，存放在 Harness home。列出它叠加哪些 bundle、装哪些 out-of-tree 插件、用户的 `cordis.patch.yml` |
| **Bundle** | Cordis 配置行 + 代码的分发格式。上层覆盖它插入的一切 |

内置 profile 模板：`web`、`headless`、`sdk`、`sdk-minimal`、`acp`

**叠加顺序**（对上层 patch 生效）：
```
profile 的有序 bundles → profile 的 cordis.patch.yml → home patch → --patch overlay
```

**Patch 语义**：按 id 定位某一行 → **整体替换其 config**，或插入新行。`preset` patch 可以在声明内部操作 `config.plugins`。

**HMR 由 YAML 控制**：base 开 config-only `dsh-hmr`；headless/SDK/ACP 关掉；`sdk-minimal` 不带。profile patch 可覆盖。

> 💡 **借鉴点**：德勤交付要求「整套系统可以单独部署 + 模块化打包」。DSH 的 profile/bundle 二元模型正好回答了"怎么把一堆可插拔组件打成一个能独立部署的包"——**不是打包代码，而是打包配置行**。

### 1.4 Capability Seam —— 三角色模型（⭐ 最有价值）

> **A seam is a swappable capability with three roles**:
> - **Service Definition** —— 声明接口
> - **Service Provider** —— 实现接口
> - **Consumer** —— 使用接口（通常是面向模型的 tool）
>
> **"一个包可以承担多个角色，但只有一个角色不构成 seam；加一个能力 = 设计三个角色"**

文档原话：**"Seams are why one provider swap changes the whole product."**

典型收益（DSH 自己的例子）：
- 文件系统 provider 和子进程 provider **共享同一个执行世界** → 把它们指向远程 sandbox，Bash / PTY / LSP 全部跟着搬走，**不需要 fork provider**
- Subagent provider 在同一接口后面差异巨大：从"全新的子 agent"到"委派到另一个产品的 turn"

**这正是德勤"执行器抽象层"要的东西。**

### 1.5 核心包一览

| 包 | 职责 | ctx key |
|---|---|---|
| `core/session` | append-only 的 `SessionEvent` log + 内存 store | `ctx.sessions` |
| `core/system-prompt` | prompt 段落与 tool schema 组装 | `ctx.systemPrompt` |
| `core/tools` | 带作用域的工具注册表 + 受控执行管线 | `ctx.tools` |
| `core/agent` | `Agent` 接口、live registry、`agent/*` 事件 | `ctx.agents` |
| `core/agent-loop` | 实现该接口的默认驱动 | `ctx.agentLoop` |
| `core/scope` | per-agent 作用域化注册原语 | 无（library） |
| `llm/llm` | 消息与流式词汇表 + 适配器 seam | `ctx.llm` |

### 1.6 事件三域（扩展点分类法）

| 事件域 | 语义 | 何时用 |
|---|---|---|
| **Session events** | 持久事实，append 进 log，通过 `session/event` 广播 | 事实必须**跨 reload 存活** |
| **Agent events** (`agent/*`) | 携带活的 `Agent`：inbox / step / status / request / validation / continuation | 观察或拦截**进行中**的工作 |
| **Capability events** | 把 policy 和 adapter 挂到某个 seam（`fs/*`、`tools/*`、`telemetry/*`） | **不 import agent loop** 地加能力 |

### 1.7 Turn / Step 流转（状态机范式）

```text
turn/start
  claim next-step input plus one queued message
  snapshot Session model selection; assemble prompt sections + step-admitted tool schemas
  -> agent/pre-step; project runtime context at fallback
     reject | enter(messages, startsRequestSeries?)
     reject, or a first enter rewritten empty -> close the turn with no step
     step/start
     agent/request -> prepareCall (cancellation commits neither system nor users)
     reconcile system/message using the prepared call capability
     append entered messages as user/message; reconcile retained runtime context
     log request/header and request/context as needed
     derive and freeze model history from the log
     stream the bound prepared call -> llm/stream -> agent/assistant-stream start
       agent/assistant-stream chunk*
       assistant/message | assistant/attempt -> agent/assistant-stream end
     tool/call* -> tools/pre-execute -> tools/execute -> tools/post-execute -> tool/result*
     step/end
     tools owe another request, or next-step input arrived -> claim -> next step
  -> agent/turn-stopping
turn/end
```

**`turn/*`、`step/*`、`system/message`、`user/message`、`assistant/message`、`assistant/attempt`、`tool/*` 是持久 session 事件**；其余是活扩展点。

**关键设计点**：
- `agent/pre-step` listener 可以 **accept / rewrite / reject** 认领到的消息
- waterfall 类事件（`agent/pre-step`、`agent/request`、`llm/stream`、`tools/*`）listener **必须调 `next()`** 才往下走；`agent/turn-stopping` 是串行的、**没有 `next()`**
- `prepareCall()` 在 system prompt 和已接受的 user 消息 commit **之前**绑定 adapter；两个异步阶段任一取消 → **两边都不 commit**
- 重试**不重复** assembly 或 `agent/pre-step`

### 1.8 Session Log —— "模型可见 = 已记录"

> **"Model-visible means logged. Every model request must be reconstructable from the log."**

- 每个 `assistant/message` 内嵌**产生它的完整紧凑流**
- `assistant/attempt` 保留失败/重试/取消/流错误的尝试，**但不加入模型历史**
- **Projection seam**：`ctx.sessionProjections` —— 已注册单元 fold 已 commit 的事件；carrier 通过 `snapshot()` 读选定的客户端视图
- 文件格式：JSONL v0 用 `session.jsonl[.zstd]`，v1+ 用 `session.vN.jsonl[.zstd]`
- **已 commit 的 generation 路径永不重命名/替换/删除**；相邻迁移包各自只负责一步 `vN -> vN+1`

> 💡 **借鉴点**：德勤 MVP 若要支持"审计/回放"，这个"模型可见即已落盘 + 投影 seam"是现成的答案。

### 1.9 「新行为放哪」对照表（可直接抄）

| 目标 | 机制 |
|---|---|
| 加模型 provider | 在 `ctx.llm` 注册 adapter |
| 加面向模型的能力 | 在 `ctx.tools` 注册；schema 自动进入 prompt 组装 |
| 给某个 session 换能力集 | 组合 agent preset；该处 service 行需要 `isolate` realm |
| 加 shell 执行 | 注册 `ctx.shell` backend；本地的通过 `ctx.subprocess` spawn |
| 加持久终端 | 注册 `ctx.terminals` backend + `dsh-tool-terminal` |
| 加人类命令 | 注册 `ctx.commands`；**不经 model turn 直接派发** |
| 管理后台任务 | 注册 `ctx.jobs`；`job_*` 工具读/停 |
| 从外部 webhook 启动 session | 注册 `ctx.webhookRuntime` 上的可信规则 + 挂 provider adapter |
| 加文件访问或策略 | 注册 `ctx.fs` provider 或监听 `fs/*` 事件 |
| 约束 spawn 出的进程 | 用 `ctx.sandbox` backend；consumer 在 spawn 前包 argv |
| 拦截 request/tool/turn | 用 `agent/*` 或 `tools/*` 事件；`agent/turn-stopping` 可停 turn |
| 加面向模型的上下文 | 调 `agent.inject()`；落到下一次 admitted request |
| 加 UI / 编辑器集成 | 驱动 `ctx.agents`，从 `session/event` 渲染 |
| 加 Web Client Chat 节点 | 注册 `ConversationNodeDefinition` + keyed renderer |
| 加持久 session 状态 | 扩展 `SessionEventMap`；从 log 渲染与重放 |
| 在 turn 边界 fork | `ctx.agents.create({ sessionId, seed, inheritedEventCount, meta: { isSeeded: true } })` |
| 换 session 存储后端 | 实现 `SessionPersistence`（create/open/stat/list/export） |
| 把注册作用域限定到某个 agent | 用 `agent.ctx` |

### 1.10 其他工程细节

- **应用启动一律走具名 profile**：`web` / `headless` / `sdk` / `sdk-minimal` / `acp`
- 有脚本 `verify-application-entrypoints` 把每个 package bin / 可执行入口 / root demo / `start:web` `dev:web` 脚本分类，**拒绝任何绕过 `dsh` 的 Node 应用路径**
- **Python SDK** 走同一套架构：runtime wheel 内打包标准 `dsh` CLI，客户端默认启 `dsh --profile sdk`
- **Desktop 应用**（Electron）在签名资源里带**完全一致的 dsh 生产运行时**，独占保留的 `$DSH_HOME/profiles/desktop`
- **安全公告**：README 顶部要求先读 `SAFETY.md`

---

## 二、DS Bot 插件

### 2.1 是什么

把 DSH 变成"一队长期存活的 Bot"——你建自己的 bot，然后和它们、和彼此、在群聊里对话协作。

- 仓库：`Fei2411/DS-Bot`（旧名 `FeiZhuLulu/DeepSeek-Bot` → `dsh-bot` 包名 → 现 `ds-bot`）
- 协议：Apache License 2.0
- 插件源码在 `ds-bot/` 子目录
- **独立社区项目，非 DeepSeek 官方**
- 兼容：dsh `0.2.1-rc.2`（Web）/ `0.2.0-rc.2`（Web + Desktop）

### 2.2 安装方式（四种）

| 场景 | 方式 |
|---|---|
| Desktop app | 自带 DSH，不用另装。Win: `DeepSeek-Bot--win-x64.exe`；macOS: `--mac-arm64.zip` / `--mac-x64.zip`；Linux: `--linux-x86_64.AppImage`（需 FUSE2）或 `--linux-amd64.deb` |
| DSH Desktop 插件 | 侧栏 Plugins → Add plugin → 填 `ds-bot`；国内走 Mainland China 镜像 |
| DSH Web 插件 | `npx @deepseek-ai/dsh@0.2.1-rc.2 plugin --profile web add ds-bot`（需 Node ≥ 22.19 + pnpm） |
| Docker（NAS / 常开服务器） | `docker/` 目录构建 DSH Web + DS Bot 镜像，CI 发布到 GHCR。**容器就是 bot 的沙箱**：能完全访问挂载进去的东西，仅此而已 |

### 2.3 核心功能

- **长期存活的 Bot**：每个 Bot 是 "DS Bot" workspace 里的一个 dsh Session，有自己的名字、角色、指令、模型
- **工作文件夹**：Bot 可在指定文件夹工作；换文件夹后对话**在新的 part 继续**，旧文件夹文件保留。设到 `$DSH_HOME` 等 dsh 数据目录会被拒绝
- **权限预设**：只读 / Workspace / 完全访问。**只有你能设权限，Bot 不能改**
- **Bot 协作工具**：`message_bot`（给别的 Bot 发消息）、`create_bot` / `update_bot`、`ask_user`（问你问题但不阻塞其他 Bot）、`show_view`（在自己聊天里画卡片：文本/指标/表格/进度/选项/确认/短表单）
- **群聊**：成员轮流发言，各自先读最新消息；`@Name` 传话；`+ → Reference a chat` 把别的 Bot 的聊天作为上下文；**每个成员在每个群里有自己的隐藏 Session**，群永远读不到 Bot 的私聊；无话可说就 `[PASS]`
- **角色权限表**：

  | 谁 | 能做什么 |
  |---|---|
  | 你 | 一切 |
  | Main Bot（可多个） | 管理所有群；增删 Bot |
  | 群 admin | 只管自己的群（名、公告、成员、回复模式） |
  | 成员 | 群内发言、@ 另一个成员、从外部往群里发消息 |

- **长对话不撑爆上下文**（⭐ 值得抄）：dsh 自己的 compaction **不在 Bot 的 Session 上跑**。turn 结束超过 check line（模型上下文窗口的 `checkRatio` 比例，默认 0.8）时，一次小的独立模型调用（**context steward**）读最新消息**决定一次**：
  - 工作还在进行 → **就地压缩成 checkpoint**：交接摘要 + 你最近的原话
  - 工作已到停止点 → Bot 写交接说明，**在新的 part 继续**
  - 两种情况你看到的都是**同一个聊天，没有标记**。早期部分和被压缩的消息仍可全文检索（`node:sqlite` FTS5），通过 `read_own_chat` 访问
- **记忆**：每个 Bot 一份、每个群一份、团队共享一份。详见下节
- **Web 搜索**：`auto` provider，优先级 = ① profile 指定的 searchProvider ② 当前模型路由自带的搜索 ③ 无 key 兜底（Bing/DuckDuckGo 结果页）④ 都失败 → 明确告诉模型不要瞎猜地址
- **Bot 浏览器**（Desktop / 桌面 app）：每个 Bot 一个独立 partition `bot:<id>`，登录和 cookie 归该 Bot 独占。`read_browser` 读 DOM（非截图），转 Markdown，链接和表单控件标 `[#n]`。**只读**——不能点击/输入/滚动。限制：40 万字符、15 万节点、1.5 秒。**永不读密码/信用卡/一次性验证码字段**。**不读跨域 iframe、closed shadow root、canvas**
- **Secrets**：Bot 调 `request_secret` → 卡片让你填，**Bot 永远看不到值**。值注入为环境变量 `DSH_SECRET_<NAME>`。**工具结果保存前、每次请求模型前，所有 secret 副本替换成 `[secret:<NAME>]`**。存 `<DSH_HOME>/bot/secrets.json`，权限 600，原子写
- **Usage**：按时间/Bot/模型看 token 用量。**从 session log 读**，所以老聊天也计入；无 log 的调用（checkpoint、交接说明、steward、图片解读、dsh 标题与压缩）在插件运行时按流式计数。**只算 token，不算成本**

### 2.4 记忆体系（⭐ 结构设计值得抄）

**存储格式**：纯 Markdown，**Agent Memory Repo** 格式 —— 一条一行，以 `[source: …; added: …]` 结尾。

**三个 scope**：
| Scope | 谁读 |
|---|---|
| Bot 自己的记忆 | 只有该 Bot |
| 群记忆 | 该群的成员，且**只在那个群里**读（不在自己私聊、不在别的群） |
| 团队记忆 | 每个 Bot 都读 |

**写入规则**：Bot 写自己的；群的任一成员写群记忆；Main Bot 和群 admin（任意群）也写团队记忆。

**自动审阅**：每轮结束后一次 memory review 读对话里新增的内容，**自己** keep/update/remove 条目 → **记忆不依赖 Bot 主动调 `remember`**。Bot 私聊由自己的模型审进自己的记忆；群聊由 admin 的模型（或第一个成员）**整群审一次**，**只进群记忆**。只保留你说的内容，用你的语言写，**拒绝存 key/密码/身份证号**。

**工具**：`remember`（存或替换，`replace`）、`forget`（删）、`recall`（搜全部/读整个主题/列出）

**进 prompt**：Bot 自己和团队的 `MEMORY.md` 进 Bot 的 system prompt；群 Session 里排在它们之后。**Session 启动时冻结该段**，以保住 provider 的 prompt cache；改动从下一个 part 或 checkpoint 生效，`recall` 立即能找到。

**固定上限**：单条 ≤ 300 字符、`MEMORY.md` 4,000、单个 topic 16,000、一个 scope 40 topics。超限保存会失败并提示怎么腾空间。

**安全原则（重要）**：**记忆是数据，不是指令**。看起来像 key/token 的条目被拒；并明确告诉 Bot 不要保存网页/文件/工具结果"要求它记住"的东西。

**历史**：`journal.jsonl` 记每次改动的前后文；删 Bot/群 → 记忆移到 `archive/`。

### 2.5 致谢名单 —— ⭐ 直接命中德勤路线

DS Bot 明确说明「学了这些项目的设计，**不含其代码**」：

| 上游项目 | DS Bot 从它借鉴了什么 |
|---|---|
| [AgentMemoryRepo](https://github.com/AgentMemoryRepo/agentmemoryrepo) | Bot 记忆的 Markdown 格式 |
| [OpenAI Codex](https://github.com/openai/codex) | 让用户消息紧挨摘要的 checkpoint；用于聊天检索的 message anchors |
| [OpenMausBot](https://github.com/milind-soni/OpenMausBot) | 群聊轮次与 @ 转发 |
| **[Hermes Agent](https://github.com/NousResearch/hermes-agent)** + **[Hermes Bot Mode](https://github.com/NousResearch/Hermes-Bot-Mode)** | **每群成员一个独立 session；交接时携带此前的用户消息** |
| [OpenCode](https://github.com/sst/opencode)、[goose](https://github.com/block/goose)、[pi](https://github.com/badlogic/pi-mono)、[Gemini CLI](https://github.com/google-gemini/gemini-cli) | 何时压缩长对话；交接说明装什么 |
| [obelisk](https://github.com/tommy0103/obelisk) | 用 SQLite 全文索引做聊天检索 |

> 🎯 **这条对何大人意义重大**：
> 1. **Hermes Bot Mode 的"每群成员独立 session + 交接带上下文"已被外部实现者验证并借鉴** → 何大人 6-29 定的「Hermes 为德勤项目唯一 Agent 框架」是**有社区共识支撑**的
> 2. **DSH 自己不提供多 bot 编排**，得靠插件补 → 说明**"多 agent 协作"是框架之上的插件层**，这正是 DSH 的架构哲学
> 3. 但 DSH 的 **context steward / checkpoint 机制**（不打断同一个 Session，就地压缩）比 Hermes Bot Mode 的做法更细 → 值得对照

### 2.6 配置（`cordis.patch.yml`）

```yaml
- id: bot
  name: ds-bot
  config:
    workspace: /path/to/workspace   # Bot 工作目录；默认 <home>/workspace
    home: /path/to/bot-data         # 团队数据；默认 $DSH_HOME/bot
    checkRatio: 0.8                 # 模型可用窗口的多少比例触发 steward
    browser: true                   # 强制开关 Bot 浏览器；默认仅 Desktop 开
    memory: true                    # 关掉就没有记忆工具/面板
    memoryReview: true              # 关掉则记忆只靠 Bot 自己调 remember
    diagnosticsFile: false          # 错误日志只留内存；默认 <home>/logs/diagnostics.jsonl
    updateCheck: true
    updateRegistry: https://registry.example/
    github: false                   # 隐藏 GitHub connector
```

### 2.7 模型与上下文窗口

- 模型 provider 用 dsh 的 `llm-pi-ai` 插件配
- 每个 Bot 跑自己的模型
- **必须给每个模型配 `contextWindow`**，DS Bot 的所有阈值都从它推：
  - usable window = window − reply reserve（`maxTokens`）
  - hard line = usable × 95%
  - check line = usable × `checkRatio`
  - 没配 `contextWindow` → 用适配器默认（`llm-pi-ai` 是 **262,144** tokens，可能不对）
  - 报不出窗口 → 按 **500,000** 算
- 发图需要 provider 有 `defaultInput: [ text, image ]`

### 2.8 数据与备份

全部留在本机：`bot/` 和 `sessions/` 在 DSH home（默认 `~/.dsh`）。**卸载插件不删数据**。

---

## 三、对德勤项目的借鉴点（按 MEMORY.md 边界组织）

> 按 6-29 定的边界：不做「X 替代 Hermes」的选型，只问「X 的什么技术能借鉴到 Hermes-based 德勤 MVP 的哪个组件」。
> 产品路线已定：**Hermes Agent v0.14 是德勤项目 Agent 框架的唯一选择**。以下都是**借鉴**，不是替代。

### 借鉴点 1：Capability Seam 三角色 → 执行器抽象层的形状 ⭐⭐⭐

DSH：**Service Definition（声明）/ Service Provider（实现）/ Consumer（使用）**，"加一个能力 = 设计三个角色"。

**映射到德勤**：
- Hermes v0.14 → **Service Provider**（具体执行器实现）
- 德勤自研的 `ExecutorAdapter` 接口 → **Service Definition**
- Dispatcher / 各业务编排 → **Consumer**

**可抄的具体设计**：
- **一个包可以承担多个角色，但只有一个角色不构成 seam** → 强制检查：新增执行器时，三个角色是否齐备
- **"Seams are why one provider swap changes the whole product"** → 正好回应"每种执行器都能接、整套系统能单独部署"的交付目标
- **"provider swap 不需要 fork"** → 德勤的 adapter 层必须做到：换执行器 = 换一个 provider 实现，**不改 consumer 一行代码**

> 这条应该成为德勤执行器抽象层的**设计评审清单**。

### 借鉴点 2：Profile / Bundle → 「可单独部署 + 模块化打包」的答案 ⭐⭐⭐

**核心洞见**：DSH 打包的不是代码，而是**配置行**。
- Bundle = Cordis 配置行 + 代码
- Profile = 有序 bundle 叠加 + patch 层
- 交付物 = 一个 profile + 若干 patch 文件，**不是另一个可执行文件**

**映射到德勤**：德勤交付要求"每个组件独立可部署 + 模块化打包"。DSH 给的答案是：
- 组件 = bundle
- 部署形态 = profile（配置组合）
- 定制 = patch（按 id 整体替换 config 或插入新行）
- **不追求"一个万能部署包"，而是"N 个 profile"**

> 这直接回答了 MEMORY.md 里"怎么把组件独立可部署"的问题。

### 借鉴点 3：Session Log「模型可见即已记录」→ 审计与可回放 ⭐⭐

- 每个 model request 都能从 log 重建
- `assistant/message` 内嵌产生它的完整紧凑流；`assistant/attempt` 保留失败尝试但不入模型历史
- **Projection seam**：注册单元 fold 已 commit 事件 → carrier 通过 `snapshot()` 读视图
- 已 commit 的 generation 路径**永不重命名/替换/删除**；相邻迁移包各管一步

**映射到德勤**：
- 审计要求 → 「模型可见即落盘」是天然答案
- 多视图（给客户看 / 给运维看 / 给监管看）→ projection seam 而非复制数据
- **格式版本化 + 只进不出的迁移链** → 交付后不能随意改历史

### 借鉴点 4：事件三域分类法 → 扩展点设计规范 ⭐⭐

| DSH | 德勤对应 |
|---|---|
| Session events（持久，跨 reload 存活） | 业务事实事件（工单状态、交付里程碑） |
| Agent events（活的，可拦截进行中的工作） | 执行器运行时事件（step / tool call / 取消） |
| Capability events（挂 seam，不 import loop） | 策略与权限事件（审批、沙箱、数据脱敏） |

**规则**："事实要跨重启存活 → 用 session event；观察/拦截进行中的工作 → 用 agent event；加策略但不侵入主循环 → 用 capability event。"

### 借鉴点 5：Turn / Step 状态机 + waterfall 规则 ⭐⭐

- turn = 零或多个 step；step = 一次模型请求 + 它调的工具
- **waterfall 类事件（`agent/pre-step` / `agent/request` / `llm/stream` / `tools/*`）listener 必须调 `next()`**；`agent/turn-stopping` 串行且**没有** `next()`
- `prepareCall()` 在 commit 之前绑定 adapter；异步阶段取消 → **两边都不 commit**
- 重试**不重复** assembly / pre-step

**映射到德勤**：这正是何大人熟悉的 LangGraph 状态机思路，但 DSH 给了一个**更严格的取消/提交语义**——"取消时 system 和 user 消息都不落库"。德勤 MVP 若要支持"任务可中断且状态干净"，这个语义值得抄。

### 借鉴点 6：context steward / checkpoint → 长任务不掉出上下文 ⭐⭐⭐

DS Bot 的做法**绕开了 dsh 原生 compaction**：
- turn 结束超过 check line → 一次小模型调用（steward）**读最新消息决定一次**
- 工作进行中 → **就地压缩成 checkpoint**：交接摘要 + 用户最近原话
- 工作到停止点 → 写交接说明，**在新的 part 继续**
- **用户看到的始终是同一个聊天，没有标记**；早期内容仍可 FTS5 全文检索

**这个设计的妙处**：压缩不是"把历史清掉"，而是"把当前状态浓缩成 checkpoint，历史仍可检索但不再占 context"。德勤 MVP 面向的是**长周期交付任务**（不是单轮问答），这个模式几乎可以照搬。

> 且 DS Bot 的 checkpoint 借鉴自 **OpenAI Codex**，而 Codex 的 message anchors 思路又和 Hermes 系一脉相承 —— 值得对照 Hermes 现有做法。

### 借鉴点 7：记忆「数据而非指令」+ 三层 scope ⭐⭐⭐

- **安全原则**：记忆是数据不是指令；像 key/token 的条目被拒；**明确告诉 Bot 不要保存外部内容"要求它记住"的东西**（prompt injection 防御）
- 三层 scope：Bot 私有 / 群共享（只在群里读）/ 团队共享
- **每轮自动审阅**（不依赖 Bot 主动调 remember）→ 记忆的准确性不靠模型自觉
- **Session 启动时冻结记忆段** → 保住 provider 的 prompt cache
- 固定上限（条目 300 / MEMORY.md 4000 / topic 16000 / scope 40 topics），超限**失败并提示怎么腾空间**
- `journal.jsonl` 记每次改动的上下文；删除时移到 `archive/`

**映射到德勤**：德勤要面向金融机构/政务，记忆的**可审计性和防注入**是硬要求。DS Bot 的"记忆是数据不是指令"应该直接进德勤的设计约束。

> ⚠️ 何大人自己的 `MEMORY.md` 体系（Agent Memory Repo 格式，`[[topic]]` 链接 + `memory/YYYY-MM-DD.md`）和 DS Bot 的格式**几乎一致** —— 说明这套格式已是事实标准，德勤若做记忆模块可直接对齐。

### 借鉴点 8：Secret 遮蔽 → 交付给金融/政务客户的硬需求 ⭐⭐⭐

- Bot 调 `request_secret` → 卡片让你填，**Bot 永远看不到值**
- 值只作为环境变量 `DSH_SECRET_<NAME>` 注入
- **工具结果保存前 + 每次请求模型前，所有 secret 副本替换成 `[secret:<NAME>]`**
- 存储 `secrets.json` 权限 600、原子写、**不进 state.json、不进日志**
- 本地 MCP 命令需你批准才跑

**德勤场景**：客户 API key、数据库口令、涉密凭证——这套"值永不到达模型"的机制是**能不能过客户安全评审**的问题。建议直接作为德勤 MVP 的基线要求。

### 借鉴点 9：能力分级与「只有人能设权限」⭐⭐

- 权限预设：只读 / Workspace / 完全访问
- **只有你能设权限，Bot 不能改**
- Bot 想设到团队工作区外的文件夹 → **要你批准**
- 本地 MCP 命令 → **要你批准**
- 删 Bot → 连带删它的 secret、浏览器数据

**映射到德勤**：AI Native MVP 给企业客户时，"**Agent 不能自我提权**"必须是一等设计目标，而不是事后补丁。

### 借鉴点 10：Hermes 被外部验证 ⭐⭐⭐（战略层面）

DS Bot 的致谢名单明确写着借鉴 **Hermes Agent + Hermes Bot Mode** 的"每群成员独立 session + 交接带此前用户消息"。

**含义**：
1. 何大人 6-29 定的「Hermes v0.14 是德勤唯一框架」**有社区共识支撑**，不是孤军判断
2. 面试/汇报时这是**可引用的第三方佐证**（"连开源社区的 DS Bot 都在借鉴 Hermes 的多 bot 编排方式"）
3. 但 **DSH 在两处比 Hermes 做得更细**：
   - context steward 的 checkpoint 机制（就地压缩 + 保持同一聊天可见）
   - Capability Seam 的三角色形式化
   → **这两点是德勤 MVP 可以超越现有开源的地方**，即差异化亮点

---

## 四、风险与边界

| 项 | 判断 |
|---|---|
| DSH 成熟度 | **developer preview，明确会有 breaking change**。德勤交付不能把它放在关键路径上 |
| 协议 | DSH = MIT ✅；DS Bot = Apache 2.0 ✅。均可商用 |
| 官方性 | DS Bot 是**独立社区项目**，非 DeepSeek 官方 |
| 文档 | 中文文档有（`README.zh.md`、`architecture.zh.md`），但英文版更新更快 |
| 依赖 | Cordis（`cordiverse/cordis`）；DSH 论文 arxiv 2608.25512 |
| 安全 | DSH README 顶部要求先读 `SAFETY.md` —— 上生产前必须读 |
| 与何大人路线的关系 | **借鉴，不是替代**。Hermes v0.14 仍是德勤唯一 Agent 框架（6-29 决策）；DSH 提供的是**架构范式**（seam / profile / projection），不是执行器 |

---

## 五、落地建议（按优先级）

| 优先级 | 动作 | 产出物 |
|---|---|---|
| P0 | 把 **Capability Seam 三角色**写成德勤执行器抽象层的**设计评审清单** | `1-Projects/德勤/AI-Native/executor/` 下一份评审清单 |
| P0 | 把 **Profile/Bundle** 模型写进交付方案，回答"独立可部署 + 模块化打包" | 架构设计文档补充 |
| P1 | 对照 **context steward checkpoint** 与 Hermes 现有 compaction，实现差异分析 | `executor/` 或 `架构设计/` 下一份对比笔记 |
| P1 | 把 **secret 遮蔽** 和 **「记忆是数据不是指令」** 写进德勤 MVP 的**安全基线** | 架构设计文档补充 |
| P2 | 实际跑一遍 DSH（`npx @deepseek-ai/dsh web`）验证 seam 抽象的真实手感 | 验证笔记 |
| P2 | 深入读 `SAFETY.md` + `docs/architecture.md` 全文 | 补充本文档 |
| P2 | 评估「用 DSH 跑一个 adapter 试接 Hermes」，验证 seam 抽象是否真的可插拔 | 概念验证（PoC） |

---

## 六、参考链接

- DSH 仓库：https://github.com/deepseek-ai/deepseek-harness
- DSH 文档：https://deepseek-harness.github.io/deepseek-harness/
- DSH 架构（英文）：https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md
- DSH 架构（中文）：https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.zh.md
- DSH 安全公告：https://github.com/deepseek-ai/deepseek-harness/blob/master/SAFETY.md
- Cordis：https://github.com/cordiverse/cordis
- 论文：*A Programming Paradigm for Spatiotemporal Composability* — https://arxiv.org/abs/2608.25512
- DS Bot 仓库：https://github.com/Fei2411/DS-Bot（旧：`FeiZhuLulu/DeepSeek-Bot`）
- DS Bot 插件文档：https://github.com/Fei2411/DS-Bot/blob/main/ds-bot/README.md
- Agent Memory Repo（记忆格式）：https://github.com/AgentMemoryRepo/agentmemoryrepo
- Hermes Agent：https://github.com/NousResearch/hermes-agent
- Hermes Bot Mode：https://github.com/NousResearch/Hermes-Bot-Mode

---

## 关联笔记

- [[2026-09-29 - OpenRig - 离散 AI Agent 编排层（多智能体协作实践）]]
- [[2026-10-28 - OpenWork - GitHub 仓库分析]]
- [[HarnessRouter]]（德勤项目下的 harness 相关）
- 德勤项目：`1-Projects/德勤/AI-Native/executor/`
