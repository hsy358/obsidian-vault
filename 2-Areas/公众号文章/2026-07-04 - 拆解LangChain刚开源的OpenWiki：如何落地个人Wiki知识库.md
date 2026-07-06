---
title: "拆解LangChain刚开源的OpenWiki：如何落地个人Wiki知识库"
author: "小码AI笔记"
publish_date: "2026-07-04 22:09:18"
saved_date: "2026-07-06"
source: "wechat"
url: "https://mp.weixin.qq.com/s/jkHueFnhWV5QMfnGTcwa2w"
---
# 拆解LangChain刚开源的OpenWiki：如何落地个人Wiki知识库
![](https://mmbiz.qpic.cn/mmbiz_png/BibWcHmNCicv4lDNEeUiarphtgNVRg36E3DOEdDFuPKd3fWlHsOx0FnIgMJwcV58ApnLyZs1lASRuvz2HprtgRBaia0hkYmfUlia7vOuM9A5icJm4/640?wx_fmt=png&from=appmsg)

看到LangChain AI 刚刚开源了个项目OpenWiki，看它的名称和实现就是把wiki知识库这条路线在实际的应用中落下来，项目介绍：

> OpenWiki is a CLI that writes and maintains agent documentation for your codebase.OpenWiki是一个CLI，用于为你的代码库编写和维护面向Agent的文档。

Github上面的Star数量在快速增长中，当前版本是 v0.0.1，估计还在早期阶段。技术栈为 TypeScript、Ink（React 终端 UI 框架）、LangChain/LangGraph、DeepAgents，内置支持 5 个 LLM Provider，包括OpenRouter。

今年初Karpathy基于自己的AI/AGENT使用经验提出个人LLM Wiki概念：AI不需要每次从原始文档检索，让 Agent增量构建和维护一套持久化的 wiki：一套结构化的、内部互相链接的 Markdown 文件，然后保持持续的更新。随后社区很快出现了围绕这套思路的实现和讨论。

Agent特别擅长一次更新十几数十个文档，并且能厘清文档之间的关系（链接）。

六月份，Google Cloud 发布了 OKF（Open Knowledge Format）v0.1，目标是把这类 LLM wiki 的思路做成一套开放规范。OKF 定义的是一套开放的、厂商中立的最小交换约定：知识以 Markdown 文件目录的形式组织，每个MD概念文件带 YAML frontmatter，文件路径构成概念的ID。它的目标是让不同生产者写出的知识bundle能被不同消费者（人或者Agent）更稳定地应用。

Karpathy 的wiki思路和 OKF 的开放格式规范，是两个背景点。其目标都是给Agent准备"持续化更新的知识文档"这条路线。

我也在之前发布了几篇文章介绍了OKF和WIKI知识库：

[谷歌发布OKF（Open Knowledge Format）规范，它与Karpathy的LLM-wiki是什么关系？](https://mp.weixin.qq.com/s?__biz=Mzk0MzY4NzUzMQ==&mid=2247484230&idx=1&sn=9169887ece86b85f82dd2c86c2c8172c&scene=21#wechat_redirect)

[图解谷歌OKF（Open Knowledge Format）仓库，理解开放知识格式的落地路径](https://mp.weixin.qq.com/s?__biz=Mzk0MzY4NzUzMQ==&mid=2247484245&idx=1&sn=b3bc610e34d1458ab4e3afe9d814f789&scene=21#wechat_redirect)

[拆解开源知识库OpenKB：Karpathy的wiki 理念，如何被PageIndex做成无向量知识库](https://mp.weixin.qq.com/s?__biz=Mzk0MzY4NzUzMQ==&mid=2247484328&idx=1&sn=0363841cae909270a0e735e37ccbcf61&scene=21#wechat_redirect)

OpenWiki不光是维护Wiki，而且消费Wiki，内置了Agent模式支持问答，实现是基于自家的Agent SDK。

## 它做了什么？

从项目介绍可以看出OpenWiki落地的不是通用个人知识库，而是"给代码仓库维护 Agent 可读文档"这条路线：

> 输入一个代码仓库，输出一套结构化 Markdown 文档

![](https://mmbiz.qpic.cn/mmbiz_png/BibWcHmNCicv7X1Hjrq1SkWHFhnKORh5oddsrxicFISsRon9EmQhxzoYww38OibniaR61ruwhu7MPpZTbBfXtf8GBcA9kCOU0oa07VKAO07Oz9kE/640?wx_fmt=png&from=appmsg)

生成产物落在仓库的 `openwiki/` 目录下，这套文档虽然主要给 Agent 使用，但看项目prompt里的约束要求，它既要对人友好，也要对coding agents 友好。它和 OKF 也是有一点差异：OpenWiki 输出的是仓库内文档，不是严格按 OKF 组织的可交换 knowledge bundle（知识包）。当代码迭代跟新的时候update模式会把 git 变更摘要以及上次更新的元数据一起交给 OpenWiki（内置的内部Agent，下同），再按 prompt 约束做尽量小的增量更新。

## OpenWiki 项目结构

OpenWiki 实现了完整的工具链：CLI、内置 Agent、LLM 路由、对话持久化，几乎全套完备，可以独立运行。

![](https://mmbiz.qpic.cn/mmbiz_png/BibWcHmNCicv7t5XD0u5tHrDJDG7gGCP3GcNLe2drYHIKabRgJsiapZHuKgWqTj8ibL6VtZm38c80oUZ2vrqhCE21XOLQl7zr7MfsWVb2BpI7T0/640?wx_fmt=png&from=appmsg)

CLI工具层是基于 Ink（一个TUI框架）构建的。一个设计细节：init 或 update 命令跑完后会自动退出（`shouldAutoExitStartupRun`），不需要用户手动 Ctrl+C，让 CLI 同时能当交互式聊天工具，也能当一次性命令用，看来也很适合配合Skill+CLI的模式一起使用。

OpenWiki不只是Wiki文档管理。它的默认模式是聊天：直接运行 `openwiki` 不带任何参数，打开的是一个交互式问答界面，内置包含了文件系统工具和 shell 后端接入代码仓库，可以随时开启回答。

具体的三种模式的分工：

- **chat**（默认）：交互式问答。OpenWiki 可以读代码、跑 git 命令、搜索文件，但不会主动修改文档。用户明确要求改文档时才动手，也就是说自身就是一个相对完备的Agent。
- **--init**：首次扫描代码库，从零生成一套结构化Wiki文档
- **--update**：基于 git 变更证据增量更新已有Wiki文档
如果看 chat 模式的 system prompt：

> "This is an interactive chat turn. Answer the user's message directly. Do not create or update OpenWiki documentation unless the user explicitly asks you to modify documentation."翻译：这是一个交互式聊天轮次。直接回答用户的消息。除非你明确要求你修改文档，否则不要创建或更新OpenWiki文档。

这意味着 OpenWiki 的定位不是"一个能管理文档的纯 CLI"，而是一个"懂你代码库的 Agent"，Wiki文档管理只是它的能力之一。

CLI生成的wiki文档落在仓库里的 `openwiki/` 目录，后续 init、update 或 chat 都把它当作仓库内现成文档来消费。SQLite会把线程状态写到 `~/.openwiki/openwiki.sqlite`，它只持久化当前线程的状态（消息历史、工具结果等），每次CLI启动都会启动新的会话ID，也就是说它当前不跨会话。

> 但我觉得这会不会太重了？大部分情况我们需要的只是一个简单的wiki管理实现。

Agent 运行时用 DeepAgents 组装，DeepAgents 是 LangChain 生态里的高层抽象，把模型、工具、状态管理打包成一个可运行的 Agent（开箱即用的Agent开发框架，对于快速Agent应用开发倒是一个不错的选择）。创建 Agent 的关键代码：

-
-
-
-
-
-
-
-
-
-
-
-

```
const agent = createDeepAgent({  model,  tools: [],  checkpointer,  backend: new LocalShellBackend({    maxOutputBytes: 100_000,    rootDir: cwd,    timeout: 120,    virtualMode: true,  }),  systemPrompt: createSystemPrompt(command),});
```

checkpointer 用 SQLite 持久化线程状态，LocalShellBackend 把文件系统操作限制在目标仓库内（`virtualMode: true`），Agent 主要通过 DeepAgents 提供的文件系统 / shell 能力读写文件、跑 git 命令。输出通过 LangGraph 的 stream API 流式返回，前端可以实时解析渲染。

LLM 路由支持 5 个 Provider，配置集中在 `constants.ts`：

Provider

封装类

默认模型

OpenRouter

ChatOpenRouter

GLM 5.2

Anthropic

ChatAnthropic

Haiku

OpenAI

ChatOpenAI

GPT 5.4 mini

Baseten

ChatOpenAI（自定义 baseURL）

GLM 5.2

Fireworks

ChatOpenAI（自定义 baseURL）

GLM 5.2

从默认配置看，5 个 Provider 里有 3 个把 GLM 5.2 放在了首位，兜底的 `DEFAULT_MODEL_ID` 也是 OpenRouter 的 GLM 5.2，看来LangChain还是比较偏爱GLM5.2的。

## Wiki管理的Prompt工程

![](https://mmbiz.qpic.cn/sz_mmbiz_png/BibWcHmNCicv4owkKuqCjxvibBBMibGE5H5njDHqBR7Yy4mcEH7CY1sZan2iaF5PJ16n63kbKwiaFRM8riaKE1OdYUms6UPicHkba0PRPkMuZIjyYOw/640?wx_fmt=png&from=appmsg)

我认为这是Wiki管理最核心的部分，基于OKF或者Karpathy的描述来看，Wiki的管理并不必然需要完整的代码工程，可能一个简单的Skill流程描述+一些简单的脚本就能落地，而且也有很多开源项目这么实现的。系统提示词定义了 Agent 的行为边界：

**角色定位**：expert technical writer, software architect, and product analyst （资深技术文档撰写者、软件架构师和产品分析师）

**证据纪律**：每个重要声明必须有源文件、现有文档或 git 历史作为证据。不发明文件、模块、API 或行为。不穷举扫描，用有针对性的发现方式。不读 .env 文件或泄露密钥。

**Git 纪律**：prompt 明确要求 Agent "use git heavily where it helps explain why code exists, not just what code exists"（在能够帮助解释代码存在原因（而不仅仅是代码存在什么）的地方，大量使用 Git。）。不只是看代码是什么，还要用 git log、git show、git blame 理解重要文件和工作流是怎么演变过来的。重点关注近期提交和高信号历史，不过度追溯。

**已有文档纪律**：仓库里已有的 README、docs/ 目录、根目录文档文件、runbook、SKILL.md 都被视为主要资料来源。prompt 要求"summarize and link to existing docs when they are still useful instead of duplicating them wholesale"（总结并链接到仍有用的现有文档，而非原样复制。）。如果已有文档和源码或 git 历史矛盾，以当前源码为准，同时指出可能过时的文档。

**subagent 分工策略**：prompt 鼓励在大或陌生的仓库里默认使用 1-2 个只读 subagent 并行探索不同领域（现有文档、运行时架构、数据层、API 接口等）。subagent 只能读不能写，最终由主 Agent 综合所有发现并写入Wiki文档。

**规划纪律**：写文档之前，先创建临时的 `openwiki/_plan.md`，列出要写的页面、证据来源和遗留问题。写完后删除这个规划文件。

**文档结构**：prompt 只硬性要求 `openwiki/quickstart.md` 做入口；仓库足够大时，再按主要区块分目录，比如 architecture/、workflows/、operations/ 这类。不允许出现只有一行的空壳页面 —— 内容少就合并到 quickstart。像 OpenWiki 项目自己的这份 wiki，目前就是 `architecture/`、`cli/`、`agent/`、`operations/` 各放一篇实质的文档。每个文档要有实际解释价值：这个领域做什么、为什么存在、从哪里开始、需要注意什么、关键源码引用。

**自动注入 AGENTS.md**：prompt 还要求 Agent 检查仓库根目录的 AGENTS.md 和 CLAUDE.md，补上一个固定的 OpenWiki 引用段落，指向 `openwiki/quickstart.md`，引导 AI 编程 Agent 在做代码修改时先读 openwiki/。

> 以上是我们重点需要关注的内容：学习这些Prompt的规则和约束，不需要使用这个cli壳子，可以自己定制自己的Wiki Skill。

## 增量更新：只改需要改的

增量更新不是让模型在对话里临时自己跑 git diff，而是分两步：宿主进程先收集 git 证据，OpenWiki 拿到证据后再做影响面评估。

![](https://mmbiz.qpic.cn/mmbiz_png/BibWcHmNCicv40gO1juic9V5AzOcWB6oKMbnwjHxlCZtgDU32rcKqwElkr1Fu8JCqo7n6lIAKvQNiaOAice0HlIibyzd7Y2m3nO8gcCepeaD8sDhI/640?wx_fmt=png&from=appmsg)

**第一步：运行时收集 git 证据**。在 OpenWiki 启动之前，CLI 先跑一系列 git 命令，把结果组装成一个稳定的上下文块交给 OpenWiki 的内部Agent：

- `git status --short`：当前工作区状态
- `git rev-parse HEAD`：当前 commit hash
- `git log <上次gitHead>..HEAD --name-status --oneline`：上次更新以来的提交和变更文件（如果记录了 gitHead）；如果没有 gitHead 但有时间戳，就用 `--since` 查询；如果都没有，取最近 20 条提交
- `git diff --name-status HEAD`：未提交的本地变更
那么 OpenWiki 拿到的是一个比较全面的、结构化的 git 变更摘要，不需要自己去猜"上次更新之后改了什么"。

**第二步：OpenWiki 做影响面评估**。prompt 要求 OpenWiki 在编辑之前先建立映射：

> 源文件变更 → 受影响的文档页面 → 需要改什么 → 为什么

如果一个页面找不到对应的源码、工作流、产品或已有文档变更，就不能变更。

系统提示词给了明确的预算约束：

- 少于 5 个源文件的变更：最多更新 1-2 个 wiki 页面
- 优先保留现有结构和措辞，倾向于"替换一句过时的话"而不是"新增一段"
- 不做纯格式调整：不重新排列表、不统一空行、不润色措辞
- 如果 wiki 已经是准确的，可以什么都不改
**内容快照防抖**：OpenWiki Agent层跑完之后，CLI 层会对 `openwiki/` 目录做一次 SHA-256 哈希，和运行前的哈希对比。只有内容真的变了，才写入 `.last-update.json`（这个文件记录了变更时间戳）。如果 OpenWiki 跑了一圈但文档没有任何变化（比如代码改了但不影响文档），元数据就不会更新。这防止了定时任务反复跑但文档没变时的元数据抖动。

## 最后

一个小小的思考：这些工作里有多少是必须的？

OpenWiki 自带了完整的 Agent 运行时，但我们常用的是 Codex、Claude Code、OpenCode 这类编程 Agent，它们本身就具备更加完善的 shell 访问能力、文件读写能力和多轮对话能力等更高层的能力。内置Agent运行时有些过重了，或者这本身就是LangChain的一种产品`示例`？

Karpathy 最初的 LLM Wiki 定义更像是一份可以直接复制进 agent 指令的 schema，不一定非要这类全面的独立工具。所以 OpenWiki 中真正有价值的部分是那套 **Prompt 工程和增量更新机制**：

> subagent 分工策略、规划纪律、文档结构规范、影响面评估、软预算约束，这些是真正可复用的东西。它们大部分写在 prompt 里，少数保障逻辑比如 git 证据预收集、内容快照防抖、元数据写入则落在运行时。

CLI 和 Agent 运行时不是必需的基础设施。甚至 `openwiki --update` 这个命令本身也不是必须的：增量更新的逻辑（读 git diff、评估影响面、只改受影响的页面）完全可以写成 prompt 指令，让已有的编程 Agent 自己去执行。你不需要一个专门的 CLI 来触发更新，你只需要告诉 Agent："检查最近的代码变更，更新 wiki 里受影响的页面。"

如果你已经在用 Claude Code 或 Codex等智能体，把上面的这些策略沉淀为 skill/Agents.md，让当前环境的 Agent 执行，应该可以达到同样的效果。

---

## 参考链接

GitHub：https://github.com/langchain-ai/openwiki
