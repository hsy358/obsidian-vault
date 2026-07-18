---
title: "我为什么改造Multica再它读懂AgentWaker"
author: "code2rich"
publish_date: "2026-07-16 20:52:25"
saved_date: "2026-07-18"
source: "wechat"
url: "https://mp.weixin.qq.com/s/8BIwK9If5nBJwEtEbLNE3w"
---
# 我为什么改造Multica再它读懂AgentWaker
过去一段时间，我一直在做几件看起来不太相干的事。

我 fork 了 Multica，改它的 Agent 管理和运行链路；我又做了 AgentWaker，用目录、配置和技能文件描述一个 Agent 到底是谁；再往后，我给自己做了两个内容运营助手，一个负责微信公众号，一个负责小红书。

如果只看结果，它们很容易被理解成三个项目：一个任务平台、一个 Agent 模板仓库、两个自动写稿工具。

但我真正想解决的其实是同一个问题：

> **当 Agent 从一次性的聊天窗口走出来以后，怎样让它拥有稳定身份、明确边界、真实运行环境，以及可以复查的交付结果？**

这篇文章不是产品发布稿。我会从 Multica 原本解决什么讲起，再写我为什么改、改了哪些地方，AgentWaker 怎样接进来，最后把两个内容运营助手的实际运行结果摆出来。有效的地方会说清楚，不够顺的地方也不回避。

## Multica 吸引我的，不是“又一个看板”

Multica 的定位很直接：把编码 Agent 当成团队成员来管理。你可以给 Agent 分配 Issue，让它接手任务、发表评论、改变状态，并通过本地 daemon 把任务交给 Codex、Claude Code、Kimi、OpenClaw 等真实 CLI 运行时。

它不是在聊天窗口上多套一层壳。它真正有价值的地方，是把 Agent 放进了团队协作里：有工作区、有任务生命周期、有运行时、有定时触发，也有可复用技能。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/10icyou2Fib1R6BWt7ib4WUdcibxteWgVFLq8Rp67RG1u4LFVV4myCyGYQt5CuMRzvicNjoe5A3WjLVIC6xjXww1ricicjBky1klFrPiciaGSrmsScTc/640?from=appmsg)

图 1：Multica 仓库中的真实看板截图。

Agent 和人类成员共用同一套任务、状态和协作界面。

这和我自己的使用方式很接近。我不是只想偶尔让 AI 回答一个问题，而是希望它能持续接任务：今天查一个线上问题，晚上准备一篇内容，第二天继续根据结果做复盘。

但在实际使用中，我很快碰到一个缺口：Multica 很擅长管理“一个 Agent 正在做什么”，却不天然知道“这个 Agent 为什么是这个角色”。

你可以给 Agent 起名字、写提示词、挂技能，但当角色越来越多以后，身份、技能、工具、环境变量、中文展示、长期记忆和交付标准会分散在不同地方。换一台机器、重建一个 Agent，或者想批量升级角色时，就容易重新回到复制粘贴。

## 我对 Multica 的改造，核心是把“角色来源”补上

我的 fork 不是只改了几处界面文案。以第一次完整接入 AgentWaker 目录的提交为例，单个提交涉及 108 个文件、新增约 1.08 万行；从当时的上游节点到现在，这条分支累计推进了 28 个提交。

数字本身不重要。真正重要的是，这五项改造不是五个并列功能，而是同一条“角色供应链”的五个阶段：**先定义角色源，再由 daemon 扫描，交给 Multica 形成快照和计划，随后物化成可运行的 Agent，最后把运行结果送回任务与外部入口。**

![](https://mmbiz.qpic.cn/sz_mmbiz_png/FLXkujJbPnfs6q61OQLJqIYOtzgkMBwzAvvia61X0Rv0LUcvZ1dD1p0h621gRW8lj6q3qGWSLuw2Ob2E2qydCsRSbTH6egtHT0GtTXAkZCh8/640?wx_fmt=png&from=appmsg)

图 2：我对 Multica 的改造总览。上半部分是角色从目录进入运行时的主链，下半部分是 env/.env 从读取、脱敏、加密到任务注入的配置支线。

### 1. 角色源：把目录登记到工作区，而不是上传一个压缩包

AgentWaker 是本地目录。工作区只记录目录属于哪个 daemon、它的绝对路径和同步策略；真正访问文件系统的是运行在那台机器上的 daemon。这样远端服务器和浏览器都不需要猜测本地路径，也不会越过机器边界读取文件。

### 2. 扫描：daemon 只识别契约，不执行仓库里的脚本

daemon 会校验路径、识别 `PROFILE.yaml`、角色指令、技能、能力依赖和声明过的配置文件，并为内容计算哈希。它返回的是结构化、脱敏后的清单，而不是把整个仓库不加区分地打包上传。

### 3. 快照与计划：先看变化，再决定是否应用

Multica 服务端保存不可变快照，并把这次扫描与上一个已应用版本比较。角色新增了什么、技能改了什么、哪些能力需要重新绑定，都先进入计划；确认后再原子应用。这个设计比一次性导入更重，但它换来了差异检测、来源追踪和回滚空间。

### 4. 运行时物化：角色、技能、共享能力和配置各归其位

应用快照时，Multica 不只是复制一段 system prompt，而是分别创建或更新 Agent、角色技能、共享能力和绑定关系。像信息采集、视觉生成这样的通用能力只维护一份，角色再声明自己的权限和使用方式，避免半年后出现十几份相似技能却没人知道该改哪一份。

中文内容也在这一层进入展示字段：界面可以显示中文画像和技能说明，但英文源仍然负责实际运行。显示友好和执行稳定因此不会混在一起。

### 5.配置支线：.env 必须参与同步，但不能到处可见

`.env.example` 只能说明需要哪些变量，不能让 Agent 真正运行。因此链路会读取角色作用域内准确的 `env/.env`；扫描预览、日志和普通 API 只显示变量名、配置状态和摘要；应用时由服务端解析并加密保存；准备任务时再与人工配置合并，冲突时手工值优先。

我不想用“先明文存着，以后再加密”的方式糊过去。平台一旦开始统一管理内容平台 token、API key 和运行路径，秘密管理就是主链，不是可以以后再补的附件。

### 6. 运行与入口：让角色真正接任务，并留下证据

角色物化以后，还要进入真实工作。我增加了 Agent Runs 页面，让工作区和单个 Agent 都能查看执行记录；同时接入微信 ClawBot / iLink，让微信也能成为 Agent 的任务入口，而不是只能回到 Web 控制台。

## AgentWaker 解决的是另一半：角色到底是什么

Multica 是控制面，AgentWaker 更像角色源代码。

在 AgentWaker 里，一个正式角色不是一个孤零零的 Markdown，而是一套有契约的目录： `PROFILE.yaml` 描述机器可读身份与路由， `agent-soul/` 保存身份、工作方式、工具和记忆边界，角色技能目录定义怎样做事， `capabilities.yaml` 声明共享能力依赖， `env/` 和 `mcp/` 则接住真实运行配置。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/10icyou2Fib1QKyrmz3UPDKvAz4j8pmk8dibBpHw4bQcRbQmLybq8881Jcd1lrU9H4QsiccPWLkDx9ABafOmH6pgiaKQWn8Zz6GknyibSzj8pj9HA/640?from=appmsg)

图 2：当前 AgentWaker 角色画像库的真实本地页面。仓库登记了 14 个正式角色，每个角色都能进入自己的画像与契约详情。

截至本文写作时，仓库有 14 个正式角色和 2 个共享能力。刚刚重新运行全量验证后，角色模板、schema、MCP、语言边界、运行时存储、secret 检查和集成校验全部通过。

我很在意这个验证器。因为角色一多，最危险的不是少写一段漂亮文案，而是某个角色的路径错了、MCP 文件变成空文本、环境变量引用不存在，或者中文版不小心替代了英文运行源。没有机器校验，角色库很快会变成看起来齐全、实际无法重建的资料夹。

## 两者联动后，流程才真正闭合

![](https://mmbiz.qpic.cn/mmbiz_png/10icyou2Fib1TRrgqTJp3LMWvdsQYTUyuQwx2NhqgDsDwKyGdPfudCNnU1AuvIJz3ib7t8g0JlewTDcI1mmhexeoiaKmRgHfIKnpjIibD41ZUtBU/640?from=appmsg)

图 3：本文对应的实际分工。角色契约留在 AgentWaker，文件访问由本地 daemon 负责，Multica 保存快照、应用角色并调度真实运行时。

这条链路现在可以概括成五步：

- 在 AgentWaker 里维护角色、技能、能力依赖和环境配置；
- 在 Multica 工作区里登记这个目录源和负责读取它的 daemon；
- daemon 扫描目录、校验契约、生成哈希和脱敏清单；
- Multica 生成计划并应用，创建或更新 Agent、技能、共享能力和加密配置；
- Issue、定时任务或外部入口触发 Agent，运行结果再回到任务、作品、草稿或发布记录中。
我希望保留的是“源—快照—应用—运行—证据”这条链，而不是做到第三步就宣布完成。只有这样，一个内容运营 Agent 今天换了技能、明天补了环境变量、后天需要回滚时，系统才知道变化从哪里来。

## 两个运营助手，是我拿这套系统做的真实实验

有了控制面和角色源，最自然的验证不是再造一个 demo，而是找两件会重复发生、又有明确外部结果的工作。

我选了微信公众号和小红书。

它们看起来都叫“内容运营”，实际工作方式差别很大。因此我没有做一个通用社媒 Agent 到处复制，而是拆成两个角色：公众号助手负责技术选题、证据核验、长文、配图、即页预览和草稿；小红书助手负责平台语境下的选题、短笔记、封面与轮播卡片、发布检查、互动和复盘。

### 微信公众号助手：目标不是自动群发，而是可靠进入草稿

公众号文章最费时间的部分，通常不只是写正文。还包括查源、控制声明、准备封面和正文图、转换微信兼容 HTML、上传素材、创建草稿，以及再读回来确认标题、摘要、封面和图片没有错。

我给它设置的边界也很明确：可以连续完成调研、成稿、即页预览和草稿写入，但不能擅自正式发布、群发或删除内容。

![](https://mmbiz.qpic.cn/mmbiz_png/10icyou2Fib1TE1UzmwDuTiaAs2aBvL4X1Xdlic9Z44EJqGZ0S2ibSuTGXHKAoP2b0PT5xCK5oj7jnGetaSib9c75I08cgosrYmaHHYHfKE0EZ9Io/640?from=appmsg)

图 4：一篇真实文章写入公众号草稿后的回读结果。标题、作者、摘要、封面和 6 张正文图均匹配；正式发布、群发和预览发送均为 false。

上面不是模拟数据。对应文章是《Agent 技术栈全景图：从模型、工具到生产运维，一次讲清 9 层架构》。本地保存的 draft receipt 记录了草稿创建成功和回读结果，正文包含 6 张图、6 个图注、6 个二级标题。

![](https://mmbiz.qpic.cn/mmbiz_png/10icyou2Fib1RnHnaQbbxpAPfNkIfLcz33BYjlvuJ7MAUVHoVBpy1ZVBwiauxcVIF5KoXIDMbQwibIvbBjXa2gJbzxYt7Bv50QRkcNib239AtjGU/640?from=appmsg)

图 5：公众号助手在那次任务里实际生成并进入草稿的正文总览图，不是本文临时补画的示意图。

当然，这套流程还不够优雅。生成的图片不够精致，内容信息选题，文章结构等都有很大的优化空间。

但从选题，到上传到微信公众号草稿箱，已经全程自动化。

### 小红书助手：不谈“爆款”，先证明链路真的跑通

小红书更偏图卡和短内容，节奏也更快。这个助手会先查看近期内容避免重复，再确定角度，生成标题、正文和 5—7 张图卡，做发布检查，得到明确授权后调用本机 `xhs` CLI 发布，之后再读取账号作品和指标。

![](https://mmbiz.qpic.cn/mmbiz_jpg/10icyou2Fib1T2qOfQJCEfO38uOhGwQc05AhR4A8LTdhT7ACxFatQic7JYUpOibeBUQ3LFNGafjCjz1YiavLV7loahS7ShkryFic0uzIf5icwXsojk/640?from=appmsg)

图 6：小红书助手 2026 年 7 月 14 日实际发布笔记使用的封面，主题是“原链接不变，内容自动更新”。

本文写作时我重新执行了只读状态检查。账号 `code2rich` 当前登录有效。最近一篇《Vibe Coding 做完的页面，怎么发给别人直接打开看？》发布于 7 月 15 日 21:57，当次回读是 77 次浏览、6 个赞、5 个收藏、2 次分享和 2 条评论。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/10icyou2Fib1RiaKAo7bQ5cVg5kmDbIAWjc80IeDePO0Qa6MPiaIeAwK45ib0HMcsm0B67SawAVfefhKC1k48eAPrUemwbnbQgKLbywfArBAlXFU/640?from=appmsg)

图 7：小红书账号的当次只读回读结果。会话 token 和平台访问标识已经从图片中删除。

这些数字很小，我反而愿意把它们放出来。它们不是“增长案例”，更不是爆款证明，只能证明一件事：这条链路真的从角色、选题和图片走到了平台发布，并且可以再读回来。

我认为这是自动化内容系统更健康的起点。先确保内容真实、动作有授权、结果能核验，再讨论怎样优化标题、选题和发布时间。如果一开始只追求一个夸张的结果，Agent 很容易学会制造看起来漂亮的报告，而不是改善真实工作。

## 即页在这里承担的，是“发布前的中间层”

我之前写即页时，最核心的判断是：AI 生成内容越来越快，但内容从本地文件变成可查看链接，仍然有流转成本。

在这套系统里，即页不替代公众号或小红书。它做的是发布前的中间层：长文先生成一个自包含 HTML，图片、排版和结构在浏览器里完整预览；确认后再进入微信草稿。需要分享过程稿、复盘页或素材说明时，也可以直接保留一个链接。

这比把一大段 HTML 直接塞进微信后台更容易检查，也让“生成内容”和“写入平台”不必绑死在一个动作里。

## 我现在怎样看这套东西

如果只评价功能，它还远没到“完成”。AgentWaker 的能力版本和回滚可以继续加强；Multica 的源同步需要更完整的 UI 和运行状态聚合；内容助手还要改善长期选题去重、跨任务素材复用和平台回读。

但我已经比较确定三件事。

**第一，Agent 需要源代码式的角色管理。**

身份、技能、权限、环境和记忆不能永远散落在聊天记录里。它们需要目录、schema、版本和校验器。

**第二，角色定义和任务运行应该分层。**

AgentWaker 管角色契约，Multica 管工作区、任务、运行时和状态。两边通过明确的源同步协议连接，比把所有东西塞进一个平台更容易维护。

**第三，自动化是否可信，要看证据而不是演示。**

代码提交、校验结果、daemon 状态、草稿回读、作品 ID、平台指标，这些都比一句“任务已完成”更重要。

我做 Multica 改造、AgentWaker 和两个运营助手，本质上不是为了证明 AI 可以替我写多少字，而是想把 Agent 从一次性工具，慢慢变成可以长期协作、可以升级、也可以追责的工作单元。

这条路目前还很工程化，也不够轻。但对我来说，它比再做一个看起来聪明的聊天窗口更值得。

相关项目：

Multica 上游： github.com/multica-ai/multica

我的 Multica fork： github.com/code2rich/multica

AgentWaker： github.com/code2rich/agentwaker

即页：https://jpage.cn
