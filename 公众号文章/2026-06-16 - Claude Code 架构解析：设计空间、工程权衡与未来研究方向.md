---
title: "Claude Code 架构解析：设计空间、工程权衡与未来研究方向"
author: "Beyond Known"
publish_date: "2026-04-29 16:46:40"
saved_date: "2026-06-16"
source: "wechat"
url: "https://mp.weixin.qq.com/s/hXZBlLiT3BfHbgvGndgneQ"
---
# Claude Code 架构解析：设计空间、工程权衡与未来研究方向
深刻而简洁的设计理念：其实Claude Code核心代码只有一个执行引擎，却能完成所有的软件开发任务，其背后的5大核心原则主要包含：

- Human Decision Authority
- Safety Security and Privacy
- Reliable Execution
- Capability Amplification
- Contextual Adaptability
1. 首先，先来聊一下Claude Code和Open Claw有什么不同

Claude

OpenClaw

本质

临时的会话的CLI进程(临时工)

持久的WS网关守护进程，多渠道控制平面（管家）

信任与安全机制

假设一个**不可信的模型**运行在**可信开发者的机器**上，安全机制作用于每一次Agent的工具调用里

假设**单个可信操作者**管理一个网关实例，作用于网关入口，以身份与访问控制为起点。

Agent运行时与工具编排

AgentLoop()完成上下文组装、模型调用、工具分发和恢复。

AgentLoop嵌套在网关分发层内部，是一个控制平面的组建，而非控制平面本身。网关的 agent RPC 先验证参数、解析会话，再立即返回；嵌入式 runner 执行 agentic loop 的同时，通过网关协议向外发送生命周期和流式事件。

扩展机制

MCP、插件、技能、钩子

manifest-first插件系统，插件向**中央注册表**注册能力，网关读取注册表后暴露工具，**跨所有 agents 生效**。

记忆、上下文与知识管理

基于文件的记忆，用 LLM 扫描文件头进行记忆检索

基于文件的记忆，包括工作区引导文件与系统提示文件，支持向量保存经整理后的长期记忆

多Agent系统

父 agent 派生子 agent，用 worktree 实现文件系统级隔离

多 agent 路由各有独立工作区，子 agent 委派进行后台运行。

overview

虽然两种系统在安全性评估，agent loop是组件还是架构中心；以及可扩展形式方面不同，但是两个系统是可叠加的，而非互斥的替代品，即网关级系统与任务级工具是可以组合的。

---

2. 下面本文将由五个核心问题展开，深入研究Claude Code

-
-
-

```
Q1: AI Agent 该不该有自己的判断？ A1: 首先，人类保留对系统行为的最终决策权。但是在实际中93%由Claude发起的决策问题，人类都是同意的。这种同意疲劳\的存在，允许AI在边界之内是决策行动自由的，而将边界决策交给人类。
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/fZ4CDtE50s9S6tdiakpQQ2HHUgMawPM7Lia9cg4l6aric8fhtqMx62b0TGyEXrWjpqLbbq4aRJ1KEwLKibBON43Qe9LJRLL0xWa183TIOczLgH4/640?wx_fmt=png&from=appmsg)

这个问题背后涉及到了Anthropic的关心的AI安全的问题：

1. Deny-first with human escalation安全兜底 ：**拒绝规则永远胜过询问规则，询问规则胜过允许规则**。当没有任何规则能匹配一个操作时，系统不是静默执行，也不是静默拒绝，而是**上升（escalate）给人类来决定**。

2. Progressive Trust（渐进信任）的机制：用户每次手动批准一个工具调用，这个批准可以被保存为永久规则。比如你第一次允许 AI 运行 `npm test`，下次就不用再问了。信任是通过真实的、具体的交互**积累**出来的，而不是一开始就全盘授予的。

**3.Bubble 模式：**子 agent 无法自行扩大权限，必须通过 bubble 模式把权限请求"冒泡"给父终端的人类来处理，防止子 agent 绕过人类的控制。

---

-
-

```
Q2: Claude Code的系统结构设计和传统的脚手架有什么区别？A2: 复杂层级设计解决来自IDE/Web/Vs Code/CLI等输入的一切问题。全局共享一套基础设施。
```

系统结构设计

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/fZ4CDtE50s87PEynwG6IHTTnTlWQE0Yk1ZrlVaeel3akPYuZ6dfr8lwibomBoM5Xu0k17FTysJV58YxyQT5VSwCwZFcKH8zlibUwI3uKxTqTI/640?wx_fmt=jpeg)

- Surface layer：信息输入流（User+Interfaces）
- Core layer ：queryLoop()执行Agent loop以及context compression（Agent loop）
- Safety/action layer ：真正的执行层，拿到action许可后进行工具调用，hook事件记录，沙盒运行以及子Agent的queryLoop()（Permission system+Tools）；
- State layer ：进行agent 运行时状态记录，context管理，记忆更新，持久化存储（State & persistence）
- Backend layer：Linux的shell执行与外部的MCP，SSE与HTTP等请求（ Execution environment）
scaffold还是harness ？

Scaffolding

Harness

类比

一本操作手册

基础的操作条件与环境

作用对象

模型的**推理过程**

模型**决策的执行**

干涉什么

干涉模型怎么想

不干涉推理，只管执行是否安全可靠

具体物理层

状态图、规划器、思维链模板

- 工具本身就是按照这个流程设计的。

权限系统、上下文管理、工具路由、沙箱

- 真实的 bash shell、真实的文件读写、原生工具本身不携带任何关于"应该怎么用它们"的隐含结构
Claude Code

越少越好

越完善越好

git例子

-
-
-

```
## 任务场景：帮我找出这个仓库里最近一周引入的 bug，修复它，然后提交。## Scaffold：运行git log获取最近七天的提交；对每个提交查看改动；运行改动文件找到失败的位置；生成修复方案；重新验证提交;## Harness:如果用 Harness（操作环境）来做,系统什么步骤都不预设，只给模型准备好一套原生工具和基础设施：
```

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
#工具层（模型可以自由调用）： 1.bash：执行任意 shell 命令（包括  2.git diff、 3.git commit……） 4.read_file：读取任意文件write_file：修改文件 5.grep：搜索内容#基础设施层（模型感知不到，但一直在运行）： 1.权限系统：git commit 这个操作需要用户确认才能执行 2.上下文管理：如果 git diff 输出太长，自动截断，防止撑爆上下文 3.错误恢复：某个工具调用失败了，自动重试，不崩溃 4.会话存储：把整个过程记录下来，随时可以恢复
```

-
-

```
Q3:如何实现 Agent 的能力可以稳定增长与无限扩展？A3:大道至简的循环，AgentLoop保证所有的行为在一个loop内实现，可扩展的工具与hook扩展任务
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/fZ4CDtE50s9S6tdiakpQQ2HHUgMawPM7Lia9cg4l6aric8fhtqMx62b0TGyEXrWjpqLbbq4aRJ1KEwLKibBON43Qe9LJRLL0xWa183TIOczLgH4/640?wx_fmt=png&from=appmsg)

不同的可扩展需求，对上下文的消耗代价不同，一种机制无法同时覆盖所有情况。

机制

能做什么

上下文代价

注入点

**MCP 服务器**

连接外部服务，给模型新工具

高（工具 schema 很大）

工具

**插件（Plugin）**

不是一个新的运行时机制，而是把其他几种机制打包在一起的容器

中

取决其他三种

**技能（Skill）**

注入领域专用指令改变模型思维方式

低（只有描述文字）

assemble()

**钩子（Hook）**

拦截工具执行生命周期，事件驱动自动化

零（默认不占上下文）

execute()：工具执行前后

重点想说一下Hook机制

- 想到了一个很贴切的比喻希望大家用好Hook：古代皇帝的史官，在旁边默默记录，皇帝做什么他写什么，皇帝不需要理会他，他也不干预决策。但史官手里的权力是真实的：他写什么、怎么写，决定了一件事的"后续"——正如 PostToolUse 钩子可以把执行结果写入日志、触发外部系统、修改返回内容。
- 钩子**不是**模型主动调用的，而是**系统在特定事件发生时自动触发的**。
- ## 模型不需要"知道"这个钩子存在。工具之所以占上下文，是因为模型必须"读"工具的说明才能知道怎么用它，但是钩子不需要这些。它完全在模型的视野之外运行，就像一个你看不见的后台进程。

##

---

##

-

```
Q4: 记忆是 AI 最贵的东西，它是怎么省的?A4: Context window，CLAUDE.md，auto-compact
```

**这里推荐大家可以先去去看一下: Memory in the Age of AI Agents这篇综述，对智能体记忆的范围进行清晰界定，并将其与相关概念加以区分，包括大语言模型（LLM）记忆、检索增强生成（RAG）以及上下文工程（context engineering）。补充如下：**

![](https://mmbiz.qpic.cn/mmbiz_png/fZ4CDtE50sibObeuE9vKpF77k4Oq7volJczRTUjbuW8hONsa40KdPGl7pWAx2McRApT2KHK2dyes0g7CPVibRuoGSEkrPdVFxuPia8WDyWqEpY/640?wx_fmt=png&from=appmsg)

** 压缩机制**

**1.Budget Reduction单条输出过大,代价最低，始终激活**

**2.轻量裁剪Snip：历史时间跨度过长进行轻量裁剪**

**3.微压缩Microcompact：缓存开销与细粒度处理**

**4.上下文折叠Context Collapse ： 整体历史过长, 读时投影，不破坏原数据**

**5. 寓意摘要Auto-compact ：所有手段仍不够,调用模型做语义摘要，代价最高**

**压缩之外**

在五层压缩流水线之外，还有若干其他子系统决策同样体现了"上下文即瓶颈"这一约束：

- **CLAUDE.md 延迟加载：基础的 CLAUDE.md 层级文件在会话启动时载入，但额外的嵌套目录指令文件和条件规则仅在 agent 读取对应目录中的文件时才被加载，从而防止未被使用的指令白白消耗上下文。**
- **工具模式延迟注入：启用 ToolSearch 时，部分工具在初始上下文中只包含其名称；完整的模式定义仅在需要时按需加载。**
- **子 agent 仅返回摘要：子 agent 向父 agent 返回的只是摘要文字，而非其完整的对话历史。**
- **单条工具结果预算上限：每个工具的单次输出被限制在可配置的大小上限内，防止某一个冗长的输出占用不成比例的上下文空间。****跨session压缩方式**
## Immutable data（不可变数据）：磁盘上已写的内容永远不变。
**   Structural sharing（结构共享）**：原始消息（第1-8行）和压缩后的视图（摘要+第9行之后），共享同一份底层数据，只是通过不同的"导航路径"（UUID 链）来决定读哪些、跳过哪些。

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
第1行：用户说"帮我修复 auth.test.ts"第2行：AI说"好的，我先看看代码"第3行：工具调用：读取 auth.test.ts第4行：工具结果：[文件内容，很长]第5行：AI说"发现问题了，是第23行"第6行：工具调用：修改 auth.test.ts第7行：工具结果：修改成功第8行：AI说"修好了，跑一下测试"第9行：工具调用：执行 npm test第10行：工具结果：测试通过... （越来越长）
```

-
-
-
-
-
-
-

```
第1行：用户说"帮我修复 auth.test.ts"第2行：AI说"好的，我先看看代码"... （第3-8行，原封不动）第9行：[compact_boundary 标记]  ← 新追加第10行：[摘要：我们在修复auth认证bug，已完成代码修改，测试通过]  ← 新追加第11行：AI说"修好了，跑一下测试"  ← 原来的第8行后续内容...
```

Git 也是同样的道理：两个分支共享大量相同的文件内容，不是各自存了一份拷贝，而是通过不同的指针链指向同一批底层 object，只在真正不同的地方才存不同的内容。

---

-
-

```
Q5: Claude Code的哪个设计是关键？A5: 强大的文件系统，因为他维护整个Agent生命周期所有事件的记录保证高效运转，以及长期跨session的持久化记忆。
```

Multi-agent的文件系统结构

-  完全相同工具池：子agent 看到的工具 schema，由构建版本和 feature flag 决定的部分和父 agent **完全相同**；
- 重新组装：但在此基础上，子 agent 还会被额外施加任务特定的工具限制。它只能在父 agent 能看到的范围之内，再进一步被收窄。权限只能向下传递、不能向上扩展。
文件系统的形式

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
~/.claude/projects/my-project/  ├── abc123.jsonl          ← 父 agent 的 transcript（主链）  ├── abc123.meta.json      ← 父 agent 的元数据  │  ├── sub_explore_001.jsonl ← Explore 子 agent 的 transcript（旁链）  ├── sub_explore_001.meta.json  │  ├── sub_plan_002.jsonl    ← Plan 子 agent 的 transcript（旁链）  └── sub_plan_002.meta.json
```

文件锁的存在：

在文件系统上创建一个特定名称的锁文件。谁创建了这个锁文件，谁就拥有这个任务。其他 agent 看到锁文件已经存在，就知道这个任务已经被人领走了，去领下一个。这个设计的代价是**吞吐量较低**（文件锁比消息队列慢），但换来了两个好处：

- **零依赖：不需要安装 Redis、RabbitMQ 这些外部服务，直接在文件系统上跑；**
- **完全可调试：任何 agent 的状态都是一个普通的 JSON 文件，打开就能看，无需专门的调试工具。**
跨session会话的历史重建：

1. Claude Code：`--resume` 系统不存储"会话的当前状态快照"，而是存储所有发生过的消息和工具调用（transcript）。恢复时，`conversationRecovery.ts` 把 transcript 从头重放，重建出会话状态。

2. Claude Code 中：从某个会话 fork，新会话和旧会话共享 transcript 历史，各自向前发展。

3.Claude Code上次会话的临时权限授权，在会话结束后自动回收，下次必须重新授权。每个会话是一个独立的"信任域"（isolated trust domain），权限不跨域传播。

---

3. 未来可能研究方向

Harness：AI agent 会犯错但不报错——它悄悄走偏了，用户不知道，系统也没有任何警告。现有的 harness 没有专门的失败检测机制，这是架构问题而非模型能力问题。

**When（何时主动）**：AI 现在是被动响应的，用户问它才动。能不能让它主动发现问题、主动提建议？论文提到 KAIROS 功能——主动建议能提升12-18%的任务完成率，但频率太高用户满意度会下降（47% vs 80-90%）。

引用：

[1]. Dive into Claude Code: The Design Space of Today’s and Future AI Agent Systems

[2].Memory in the Age of AI Agents: A Survey
