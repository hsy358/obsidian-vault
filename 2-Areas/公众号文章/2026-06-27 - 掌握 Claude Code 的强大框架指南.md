---
title: "掌握 Claude Code 的强大框架指南"
author: "AI大模型观察站"
publish_date: ""
saved_date: "2026-06-27"
source: "wechat-monitor"
url: "https://mp.weixin.qq.com/s/RoTmyj9EZNQwC5lQw49Uhg"
---

---
title: "掌握 Claude Code 的强大框架指南"
author: "AI大模型观察站"
publish_date: "2026-04-02 08:36:00"
saved_date: "2026-06-27"
source: "wechat"
url: "https://mp.weixin.qq.com/s/RoTmyj9EZNQwC5lQw49Uhg"
---
# 掌握 Claude Code 的强大框架指南
### 让你从第一天就高效使用 Claude 的两大习惯体系

![](https://mmbiz.qpic.cn/mmbiz_png/oTNSJmwicgJKB0ysIFJAvUP9K4JSenicuQE727vAWOpUBOL34Pxu9CeCwc1C6wrqBicQVYjnYVcgtEzBMeibiaUmEcSsxZBWoZWNESqaeVM0DKqs/640?wx_fmt=png&from=appmsg)
我是一名工程师，每天都在用 Claude Code。大多数人对 AI 的心智模型还停留在 ChatGPT 时代：你输入一个问题，它给你一个答案。Claude Code 则不同。它是一个 agent（智能体），会读取、写入、编辑你的真实文件，执行终端命令，直接在你的代码库上操作。这让它非常强大，但如果缺乏结构化方法，强大也会带来新问题。

现在写出代码本身已经不难了。真正“写得好”远不止于 prompt。没有正确的习惯，你很容易生成“AI 劣质堆料”，最终还得自己重写。我就是这样踩过坑。后来我把有效（和无效）的做法整理成了一个简单的框架，用来高效使用 Claude Code。

这个框架有两类：一次设置、让每次会话都更聪明的 compounding habits（复利式习惯），以及在当下帮你保持正确轨道的 session habits（会话习惯）。两者结合，能给你一套可复用的系统，从 Claude Code 获得更稳定、更可信的输出。

![](https://mmbiz.qpic.cn/mmbiz_png/oTNSJmwicgJIzZS53mqtdFicGxRbG7ZC0vzwkm20KZ8XHoeNY0Eu5LNLhQIGdZibmZcPAvicv8noKSx6pmmaK0OT4QB5FUj7qVQtqVfchnHoj1I/640?wx_fmt=png&from=appmsg)
高阶用户的最佳实践框架
## 入门

前往 code.claude.com/docs 按说明安装。你需要 Claude Pro、Max、Team 或 Enterprise 账户。

安装完成后，打开终端，`cd` 到你的项目文件夹，输入 `claude`。就这样。你会话中的权限将覆盖该目录中的一切。

![](https://mmbiz.qpic.cn/mmbiz_gif/oTNSJmwicgJIicGk6IWf0RlPIJgXib0sFMY0mUGLGpwdHS6W3z0EKEkszxxnAI64F0zBsn1IlcRtuiaZkiaaiaibVricyAFO4hQ0K6DLEmetibwWJhYE/640?wx_fmt=gif&from=appmsg)
演示：打开 Claude Code
## 你现在就该掌握的快捷键

按 `Shift+Tab` 在三种模式间切换。**Normal** 模式让 Claude 使用全部工具，但在执行高风险操作前（如写文件、运行 shell 命令）会征求你的同意。**Auto-Accept** 允许 Claude 在不询问的情况下应用文件编辑，但仍会就 shell 命令进行确认；当你足够信任它时，这更快。**Plan** 模式将 Claude 限制为只读，可用来探索项目和提出方案，但不能修改任何内容。

![](https://mmbiz.qpic.cn/mmbiz_gif/oTNSJmwicgJLefsKTibfTOOq8VfSbwWt6uL7dywhPG6dVdqcoFyPVILZcbldUHyBwQUpIFjke9zxFXf6BoyfJaNJNqIAk2pMDyS97281Mfia5w/640?wx_fmt=gif&from=appmsg)
演示：模式切换除了切换模式，我几乎一直在用这些快捷键：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/oTNSJmwicgJLOibO2cicQLvwujepHIwltHHruc5YqibPMsIbAia5dP9yn0u4evzGZTBBHPG5xqiaEasmopvLgXwSQKbr2iahxkoZPo6pXgHFOl76zI/640?wx_fmt=png&from=appmsg)
快捷键表我最常用的斜杠命令有：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/oTNSJmwicgJJg2cS0uJQibxcB83NRibdTherrQeuc2kRexS8yzZlJTibnGRBmCteAmPib9OoicpB2j2eicsJ7KOLfQqNGegb0t2e3fU5miay9zoMFq4/640?wx_fmt=png&from=appmsg)
斜杠命令表输入 `?` 可查看所有可用的快捷键和命令。

当你熟悉模式和快捷键后，真正的杠杆来自你的习惯。

## 高阶用户习惯

为了从 Claude Code 中榨取最大价值，你并不需要复杂的配置。Claude Code 的创建者 Boris Cherny 提到他自己的配置“出乎意料的朴素”。他并不重度定制，因为这个工具本身就很强大。优势来自习惯，而不是复杂的配置。

### 复利式习惯（Compounding Habits）

- 设置 `CLAUDE.md` 并持续更新。输入 `/init` 会在项目根目录创建 `CLAUDE.md`。Claude 在每次会话开始都会读取它，所以里面的内容，Claude 每次“天生就懂”。把你的技术栈、构建与测试命令、以及你想强制执行的规则都写进去。控制在 200 行以内。如果 `CLAUDE.md` 过长，就把规则拆分到 `.claude/rules/` 文件夹中的独立文件。Claude 会用同样的方式加载它们，你还可以按编辑的文件范围限定规则。详见 rules 文档。
- 关键习惯：每当 Claude 做错了什么，就在 `CLAUDE.md` 里加一条备注，避免下次再犯。Anthropic 的 Claude Code 团队内部就是这么做，并称之为“compounding engineering（复利式工程）”。每一次修正都会沉淀为长期上下文，让 Claude 不再犯同一类错误。不仅出错时要更新 `CLAUDE.md`，当你的技术栈改变、约定演进，或者你对代码库有了新的认知，也要更新。团队协作时，这种“复利”更快，因为一个人加的每条规则都会自动让所有人的会话收益。
- 给 Claude 加 feedback loops（反馈回路）。让 Claude 在每次更改后运行测试、linter 或构建命令。没有反馈回路时，Claude 改完就默认“能跑”，然后继续前进；有了反馈回路，它能自行发现问题。Cherny 提到光是这点就能让产出质量提升 2–3 倍。另一个复利式好处是：一旦你把反馈回路写进了 `CLAUDE.md`，之后的每次会话都会“白拿”这些能力。比如加一行：`Always run pytest after changing Python files` 就够了。

### 会话习惯（Session Habits）

- 复杂任务先用 Plan 模式。如果任务会改动多个文件或需要调研，先切到 Plan 模式。对于一两行的小改（比如修个拼写），可以跳过。Cherny 自己的大多数会话也从 Plan 模式开始。如果哪里不对，请求它修改方案；当你满意后，切到 Normal 或 Auto-Accept 并让它实施。这是核心会话习惯：十秒规划，省十分钟返工。
- 具体明确，并直接引用文件。不要只说“修一下认证的 bug”，而是像这样：“修复 `@utils.py` 第 42 行附近的 off-by-one 错误，它会跳过最后一项。”前置细节越充分，后续往返纠偏就越少。
- 保护你的 context window（上下文窗口）。每次读文件、命令输出、来回对话，都会占用上下文。现在 Claude 会帮你管理，并在过重时提示你压缩或清理。对于大型任务，要更有意识：用 `/compact` 做摘要并释放空间，或在不相关任务间用 `/clear` 清空。调研型工作可以用 subagents（子代理）把重输出隔离在独立上下文里（下面“功能”一节有更多说明）。
- 保持任务小而清晰。“给我做一个包含认证、支付、结账的完整电商网站”其实是一口气塞了十个任务。任务越大，Claude 越容易丢失需求或引发连锁错误。把它拆开：先“为完整电商网站（含认证、支付、结账）制定一个计划，并分成若干波次”。逐波执行，每波之间清理一次 context window。小任务还能形成更干净的检查点，出问题时回滚成本更低。
想深入了解上述所有习惯，参见 最佳实践文档。

## 常见陷阱

- Claude 忽略了你的项目约定。它写的代码能跑，但不符合你的风格，比如你用 `camelCase`，它却写了 `snake_case`。这几乎总是因为 `CLAUDE.md` 里缺了对应规则。加上一条类似 `Always use camelCase for variables and PascalCase for classes`，从那一刻起 Claude 就会遵循这个约定。这就是复利式工程的实践：每一次纠偏的编码，都会让后续每次会话更好。
- 复杂任务开始“失控螺旋”。Claude 开始编辑你意料之外的文件，或改动滚雪球。停止它（`Ctrl+C`），必要时用 `Esc+Esc` 回退，切到 Plan 模式，把任务拆小。然后逐个子任务推进。

## 值得了解的功能

Claude Code 提供多项功能，能解锁更进阶的工作流。

- `claude -p`（pipe mode）用于管道模式。`claude -p` 让 Claude 以非交互方式运行，可用于脚本与自动化。例如，把它接到 git pre-commit 钩子：`git diff --cached | claude -p 'review these staged changes for bugs'`，即可在每次提交前自动审查代码。完整参数见 CLI 参考。
- `--worktree` 支持并行会话。用 `claude --worktree feature-auth` 创建隔离的 git worktree。你可以在不同分支上并行运行多个 Claude 会话而不冲突。详见 worktree 文档。
- 内置 subagents（用于上下文隔离）。Claude Code 内置的 subagents（Explore、Plan 以及通用型）各自运行在独立的 context window 中。需要时 Claude 会自动生成 subagent，所有冗长输出会留在 subagent 的上下文里，只把摘要返回给主会话。你也可以主动指挥它们：“启动三个 subagents，分别并行调研认证模块、数据库层和 API 路由，然后汇总发现。”经验法则：如果一个任务涉及超过约五个文件，考虑把它隔离到一个 subagent。见 subagents 文档。
- 内置 skills。Claude Code 自带一批可用 `/` 触发的 skills。例如，`/simplify` 会从复用性、质量与效率角度审视你的代码，并直接应用修复。新 skills 会持续增加，在会话里输入 `/` 可查看当前可用项。见 skills 文档。
- 自定义 subagents 与 skills。你可以自己构建。最简单的方式就是直接让 Claude 生成，比如“创建一个审查安全问题的 subagent”或“创建一个部署到 staging 的 skill”，它会为你生成对应文件。想深入了解 Claude Code 的扩展系统（skills、subagents、plugins），我有另一篇文章： A Mental Model for Claude Code: Skills, Subagents, and Plugins。如果你想手动构建，参见 subagents 文档 与 skills 文档。

## 就是这些

从 Claude Code 中获益最多的人，并不是在写“魔法 prompt”。他们在两类习惯上同时投资：让每次会话都比上次更聪明的 compounding habits（如 `CLAUDE.md`、feedback loops），以及让每个任务都按轨道前进的 session habits（如规划、具体化、context 管理、小步推进）。这就是整个框架。

而随着工具进步，这些习惯也在“复利”。context window 在变大，模型的自我纠错能力在增强，每一次改进都会放大一个维护良好的 `CLAUDE.md` 和自律会话习惯的价值。框架不变，结果会越来越好。
