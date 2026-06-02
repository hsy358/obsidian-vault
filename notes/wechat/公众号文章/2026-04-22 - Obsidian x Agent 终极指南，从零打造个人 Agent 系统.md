---
title: "Obsidian x Agent 终极指南，从零打造个人 Agent 系统"
author: "空格的键盘"
publish_date: "2026-04-22 08:01:05"
saved_date: "2026-05-10"
source: "wechat"
url: "https://mp.weixin.qq.com/s/l38S21qKqi6eLaqFPZS0qw"
---
# Obsidian x Agent 终极指南，从零打造个人 Agent 系统
![](https://mmbiz.qpic.cn/sz_mmbiz_png/CFe2b8yvCoz0VYRAoO5wdw0YDlOeIyZ0HAHYdkpdzBIwdUPxr6LCc08IO6AXcP9fyEvt8wkAeYR9Ch2OfUiatfpgdKp3F3r0BJydThWtTMrM/640?wx_fmt=png&from=appmsg)

这应该是全网最完整的一份「Obsidian × AI 生产力」指南。

全文近万字，是我过去一年用 Obsidian + Claude Code 搭建个人 AI 生产力系统的完整思考。

**Obsidian 的价值，在 AI 时代被重新审视了。**

它是 AI 的操作系统，是 Claude Code 的工作台、是我个人上下文的资料库、是 Agent 能伸手就拿到所有材料的那张桌子。

过去这段时间，我把所有专栏、所有文章、所有选题、所有播客摘要、所有周计划，全搬进了一个 Obsidian Vault（存储库）。AI 在这套系统里读、写、跑脚本、管任务，所有动作都发生在一个本地文件夹里。

一个好的 Obsidian Vault，可以让 Agent 变成"懂你"的私人助理。

这篇文章一次讲完：

- Obsidian 价值与原理
- Obsidian 对 AI 产品设计和个人工作流的影响
- 完整的搭建与使用教程（入门 → 精通）
- obsidian 的常见功能和高阶功能
- 插件生态和 CLI 的使用
如果你是第一次听到"AI 生产力系统"，这篇文章是最合适的入门；

如果你已经在用 Obsidian，那我希望这篇能让你看到 Obsidian 被低估的那一面。

一、Obsidian 是什么：从本地编辑器到 AI 操作系统

大部分人第一次看 Obsidian，会觉得它就是一个"支持双链的 Markdown 编辑器"。

在我看来，Obsidian 更像是一个**本地文件夹的可视化编辑器**。

它只是帮你把一堆`.md`文件用图形界面打开、编辑、互相链接。

所有的文件都能以命令行的方式被 Agent 读取调用。

发生这一切行为的场所，obsidian 就是最合适的。

**在 obsidian 里，人类可以控制和看到 AI 在读取什么、在输出什么。**

1.1 把 Obsidian 理解成"AI 的工作桌"

这里有一个更直观的类比。

你请了一个助理，想让他帮你处理工作。你会怎么准备？

- 给他一张桌子（有权限能随时拿到所有材料）
- 桌上按分类摆好文件夹（客户资料、项目档案、个人偏好）
- 贴几张便利贴（写清楚哪些规则不能违反）
- 桌角放一本 SOP（不同任务按什么流程做）
- 给他一支笔，让他能随手记、随手写
Obsidian 就是这张桌子的数字版，Agent 就是那个助理。

![](https://mmbiz.qpic.cn/mmbiz_png/CFe2b8yvCowRNbN6VtsDawrq0eUhpLL4SzHFADibmTL7icukRAGNLGAUrMSC1EeXww6qhPLuHOhxiaib6ice0NtA83T2kia6qOCmypuWiaJAibway0I/640?wx_fmt=png&from=appmsg)

我的 obsidian 每个文件夹、文件都是由 AI 来读取和输出

![](https://mmbiz.qpic.cn/sz_mmbiz_png/CFe2b8yvCozzDRzQ2mjc6PwUGBGF329fEBnB2lch6EXBsh1AJ8iadIqGoL3f7rkPicRFCWMvJBjwjOtSzm5fPMpNeImWgRrRkpbwoKx6o9gIw/640?wx_fmt=png&from=appmsg)

Claude Code 进入这个文件夹的第一件事，就是读`CLAUDE.md`。

它告诉 AI：这里有什么、不能碰什么、不同任务应该走哪条线。

然后 AI 开始工作，过程中自己翻文件夹、读文档、查索引、写笔记。

整个过程里，我基本不用解释任何背景。

1.2 Karpathy 的 Obsidian 三件套：剪藏 + Wiki + 规则

先用一套具体的方法论把 Obsidian 的用法讲清楚。

这套方法来自 Andrej Karpathy，前 OpenAI 联创、前 Tesla AI 总监。

**① 剪藏：一切入口都是 Obsidian**

看到值得记的东西，不要收藏到浏览器、发给文件传输助手、丢进备忘录，而是**剪进 Obsidian**。

比如可以把文章用 Web Clipper （浏览器插件）一键保存到 obsidian 的Markdown文件、把推文复制正文贴进笔记、播客字幕整段存进来、一句想法开个新文件就写。

不需要管理目录、文件名称，所有原料在同一个文件夹里，AI 想用时随时可得。

不在 Obsidian 里的信息，对你的 AI 系统来说就等于不存在。

**② Wiki ：知识自己长成网**

剪完关键是用让 Agent 来调取他们。

比如读到一个重要概念，在笔记里写`[[概念名]]`，

告诉你的 Agent，让它根据这个概念来读取剪藏的内容中有哪些相关的，按 xx 规则整理到wiki 中。

这样子，你收藏的内容就被 Agent 关联起来，并创作出来新的内容。

久了之后，你的 Vault 是**一张自己长出来的 wiki**。

AI 读到任何一篇笔记，都能顺着双链拿到背景、案例、相关概念。这就是最好的上下文。

**③ 规则：给 AI 制定输入和输出的 md 规则文档**

光有原料和连接还不够，AI 不知道你希望它怎么工作。

所以 Karpathy 会在 Vault 里写一份**规则文档，**什么该做、什么不该做、不同任务怎么走。

- 可以写根据剪藏的内容，按照你的博客规则，来创作博客
- 根据剪藏的内容，按照你的论文写作规则，来创作论文
- 等等
可以把一些通用的规则写到 claude.md里，让Agent 执行时，每次都独立规则目录下的文档。

这三件事合起来就是一个完整的个人 AI 知识系统：

剪藏  →  把信息搬进来 。Wiki  →  让信息自己组织。 规则  →  告诉 AI 怎么用

1.3 我的 obsidian 运作机制：CLAUDE.md + 文件夹 + MD 文件

但是对于Karpathy 的方法并不适用于大多人。

因为它不仅需要你提供大量参考文件，还可能消耗你大量的 token。

下面是我的方法，这是我从众多知识管理的方案中提炼出来的适用于AI的。

Obsidian 作为 AI 操作系统的运行机制，可以拆成三层：

![](https://mmbiz.qpic.cn/mmbiz_png/CFe2b8yvCoy3OoECuaibayqXvvQFKQDRUOKv0a2KKC7nr4UereG4dQmSuMZjCuHianzXrvlppoWsibmNtib9SI5icHMHRnFAQcbiaLtH2y9RSnCjk/640?wx_fmt=png&from=appmsg)

Layer 1 是 AI 进入 Vault 时读的第一个文件。我的 CLAUDE.md 包含四件事：

- **项目概述：这个 Vault 是什么、目标是什么**
- **模块地图：每个文件夹的职责**
- **核心行为规则：比如"JSONL 只能追加不能覆盖""写文章前必读写作风格"**
- **任务路由表：不同类型的任务走哪个流程、读哪些文件**
Layer 2 是文件夹。编号 + 中文名：`00 收件箱`、`01 内容创作`、`02 选题管理`……编号保证排序稳定，中文名保证 AI 一看就懂。

Layer 3 是具体文件。命名、格式、结构都有规范：

- 文件夹：`序号 名称/`
- 独立文章：`MMDD-标题.md`
- 专栏文章：`章节号-标题.md`
- 索引文件：`xxx_index.jsonl`。用于记录 Agent 在这个文件夹下做了什么事情。
Agent 在我的 vault 需要输出内容时，通常它的执行步骤是，先读取 claude.md，然后判断是否需要调用 Skill，下一步去读取到指定的文件夹，在文件夹里读取`_index.jsonl`，查看这个文件夹做过什么，最后来输出内容。

每一步 Agent 都知道自己在做什么、读什么、写到哪里。

二、Obsidian 详细教程

这部分分两段：入门（今天就能装起来用）、精通（真的把它变成 AI 操作系统）。

2.1 入门：30 分钟搭起一个能用的 Vault

Step 1：装 Obsidian

去obsidian.md下载对应系统版本，双击安装，开箱即用。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/CFe2b8yvCozpa8JA7kOic4K9T6gibf7mHKibWPCYyiaQ7Y0Qeb5CojN4d6Zpm4WTYAicdfsw4XmGuDQPFgyB0ibnFcyGc2qopBicFd3Z7nCwSzicoGs/640?wx_fmt=png&from=appmsg)

打开后它会让你选一个本地文件夹作为 Vault（存储库）。

这个文件夹就是你未来所有笔记的根目录，选一个你能长期稳定管理的位置。

我个人推荐放在：

```
~/Documents/GitHub/obsidian
```

放在 GitHub 目录下是因为后续方便统一 Git CLI 来做版本管理。

如果你不熟悉 Git，mac 电脑放 iCloud 或者本地任意位置都行。

Step 2：理7 个核心功能

Obsidian 功能很多，但 80% 场景用这 7 个就够：

**① 双向链接**

任意笔记里写`[[笔记名]]`就能链接到另一篇笔记。被链接的那篇会自动显示"谁引用了我"。

![](https://mmbiz.qpic.cn/mmbiz_png/CFe2b8yvCozh4GDJrBrCnl5Oyfib3opK3bEKVB0cfb0x9N3vPPLSTfS1J9GvlNwFTqrZPlsrfnqmDamzT6ibzsdicXogrhn6ZCuUibyqzy6ZmuU/640?wx_fmt=png&from=appmsg)

**② 知识图谱**

所有双链可视化出来，就是图谱。节点是笔记、连线是引用。不是每天都用的功能，适合发现知识盲区，如果某个主题的笔记孤零零没有连线，说明你还没把它和其他东西关联起来。

在 Obsidian 左侧点击下图按钮，就能进入知识图谱

![](https://mmbiz.qpic.cn/sz_mmbiz_png/CFe2b8yvCowTK1mXqMH7yDHhxcjxZ0F0kupU438IKyKlcibuHesQqia2MQ4jEYNsQiayFjXDWzgDHWr1MvJdW7dib2ktIcS0BenUPictf91BQ3Tg/640?wx_fmt=png&from=appmsg)

**③ 笔记属性（YAML 元数据）**

每篇笔记顶部可以写一段结构化字段：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/CFe2b8yvCoyESQEz4vV33pT77KoHKw0r4tgIJk1wmjmbNb9LGMqdlCro4xNCImCPicwZxjq2o99j5OCNl2F962EO9A2beJTjcKiauURFA4shA/640?wx_fmt=png&from=appmsg)

AI 读笔记时，这是它看到内容的第一步。

**④ Daily Notes**

![](https://mmbiz.qpic.cn/sz_mmbiz_png/CFe2b8yvCowswLwVv65a9qf3mBHRIZg7hIKZsteelRhuUBatwj1pu8AO7ZiaGRKodia9LR4BWdymmd4xIxdzgCWPwmJHYuQk2CTt4QWGnEZMQ/640?wx_fmt=png&from=appmsg)

点击每日笔记，自动创建一个日期命名的笔记文件，比如`2026-04-15.md`。

我用它做一天的工作日志，结合 Calendar 插件还能看日历视图。

**⑤ Templates**

模板的价值是快速复制某个文件的框架到新建的文件在。

![](https://mmbiz.qpic.cn/mmbiz_png/CFe2b8yvCoz27fCkMAVN8ofYgAmMRxGlxO9Uljuzeom6AVzoicyUUdcNumIrNFP9ribKG8YlBpTSm84pKquFic3iaNuwFyOUNQDkEQoxMFCvQvI/640?wx_fmt=png&from=appmsg)

比如周复盘模板、选题模板、日报模板……这些都可以用模板。

**⑥ Canvas**

Obsidian 的内置白板。零散想法摊开来看、画概念关系图、导出成图片插文章。两种场景最好用：头脑风暴、画关系图。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/CFe2b8yvCowHYdPqoPjx707Za33ticfBz1slqicuEnHYp8hciaZgzmJwlgwel8SY1slQia1cPdia05xoaCle2BGPqRZmD4bkfVfeQoG8FtgZdfHM/640?wx_fmt=png&from=appmsg)

**⑦ Web Clipper**

Web Clipper 是官方浏览器扩展，在浏览器看到好文章点一下图标，就以 Markdown 存进 Vault。

![](https://mmbiz.qpic.cn/mmbiz_png/CFe2b8yvCozjmHw8fk9IB7CC7d7BAibe5EXIXbaacLUNy2g17LPKicFFowgZpV4NJHT5slujoXT3mbic2MvKydenF0Rft8NpyEciaiat82nayvkc/640?wx_fmt=png&from=appmsg)

下载地址：https://chromewebstore.google.com/detail/obsidian-web-clipper/cnjifjpddelmedmihgijeibhnjfabmlf

**8 Bases**

Bases 是 2025 年 v1.9 新增的能力，能把笔记集合变成结构化数据库视图（表格/卡片）。

![](https://mmbiz.qpic.cn/mmbiz_png/CFe2b8yvCoxRDDBFdBHhPuDpxnxcy9EyrggNY79Wb2ibnuY5U9VjLmNVMua5sMRTZ5mRUaxibnVsYn5gZ37ecD5IwMDJJmLF6Aic9vtSJDfVco/640?wx_fmt=png&from=appmsg)

Step 3：Markdown 语法

Obsidian 用 Markdown 写笔记。如果看到类似下面的文字加载着各种符号，不要慌，这就是 markdown 语法的标志。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/CFe2b8yvCozuxbwJBtmVuMVa8n4DJ1yRHVrc6gKjiaGeE9CjGLzGd9iaRce00lS7lXd0CIV63aC77KWKuia0zUjIsQLGJrf3Zywl4ouMPC11Lg/640?wx_fmt=png&from=appmsg)

在飞书、钉钉这类文档通常都自动渲染了 markdown 语法，下面是常见的语法符号。

**1 标题****#→ AI 理解文章结构。**`h1`是主题，`h2`是分论点，`h3`是细节。

**2 列表****- / 1.→ AI 理解"这些是并列/有序要点"，摘要时优先关注。**

**3 双链****[[...]]→ AI 理解"这个概念在系统里有专门文档"。**

**4 代码块 ```→ AI 识别"这段是代码不是正文"，不会把变量名当中文理解。**

**5 Frontmatter→ AI 读笔记的第一印象，用来分类和过滤。**

**6 标签****#tag→ AI 做分类检索。**

Markdown 不仅是给人看的，更是给 AI 看的结构化指引。

2.2  精通：把 Obsidian 变成 AI 操作系统

这一篇章详述应该如何让 AI 读懂你的 Obsidian 文件夹

Step 1：设计你的文件夹模块地图

这是整个系统的骨架。我的划分方法：

```
05 工具箱/       — 插件、脚本、Skill06 计划/         — 年度 → 周计划 → 每日 → 复盘07 系统方法/     — 工作流、迭代记录08 交付物/       — 工作交付、甲方内容09 image/        — 文章配图10 About me/     — 个人介绍、写作风格、审稿标准
```

**三个原则**：

- **序号 + 中文名：保证排序稳定、一眼能懂**
- **每个文件夹有 README.md：写清楚放什么、不放什么**
- **深度不超过 3 层：太深 AI 和你都找不到**
Step 2：写好你的 CLAUDE.md

这是 Agent 进入 Vault 的第一个文件。

一个合格的 CLAUDE.md 应该包含：

- **项目概述：Vault 是什么、核心理念**
- **模块地图：每个文件夹的职责**
- **核心行为规则：AI 必须遵守的铁律**
- **任务路由表：不同任务走哪个流程**
- **命名规范：文件怎么命名**
- **关键索引位置：核心 JSONL 在哪里**
我的claude.md规则是这几条：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/CFe2b8yvCoyQG4NnycY0uSmIXxiazS7qM1HE97YUiaX1WysT5tjGSTNe5X52E1SCfBjoo159ULUx5rjQ56gQVGiahyfgiadiaSicyeOOFIKicHhgY4/640?wx_fmt=png&from=appmsg)

- 操作 JSONL 文件时**只允许追加**，绝不覆盖
- 写文章前**必须先读**写作风格文件
- 创建新文件前确认应该放哪个子文件夹
- 写专栏文章**先拟大纲讨论**，切勿一次性输出几千字
- 每个文件夹下有 README，进入新文件夹时先读
这些规则仅让 claude code 对你的 obsidian 文件夹项目生效，退出这个文件夹后，以.claude.md的规则为准。

Step 3：建立索引文件

CLAUDE.md 是指南，JSONL 是Agent 对于每个文件夹的规则记录

我用四个 JSONL 贯穿整个系统：

- `daily_log.jsonl— 每日产出记录，在07 系统管理文件夹`
- `goals_tracker.jsonl— 年度目标追踪，在年度文件夹目标下`
- `articles_index.jsonl— 独立文章索引，在个人创作文件夹下`
- `series_index.jsonl— 专栏进度索引，在个人专栏更新文件夹下`
JSONL 的好处：每次执行完成任务，**AI 追加一行记录，读取成本极低，但可以让 AI 很好的按照文件夹规则输出执行**。

对比 JSON 或数据库，JSONL 的结构最简单、AI 操作最稳定。

我在 CLAUDE.md 里定了一条死规则：JSONL 只追加、不覆盖。

这条规则几乎是整个系统最重要的护栏。

Step 4：沉淀你的个人上下文

AI 懂不懂你，取决于你愿不愿意把自己的偏好、风格、历史沉淀下来。

我在`10 About me/`下有这几个文件：

- `我的介绍.md— 身份、背景、当前身份`
- `写作风格.md— 语言偏好、文章结构、禁忌`
- `内容定位.md— 写什么、不写什么、读者是谁`
- `审稿标准.md 一篇文章发布前要过哪些关`
- `性格特点.md— MBTI、决策倾向、沟通偏好`
这些文件的作用是——**让 AI 不需要再"了解你"，它打开文件就懂你**。

刚开始写这些很像写简历，但一旦写完，AI 的输出质量会跃升一个台阶。

Step 5：搭建你的三大工作闭环

我的系统里跑着三个核心闭环，互相喂养：

**闭环一：内容创作**

选题 → 素材 → 起草 → 审稿 → 发布 → 归档

每一步都绑定到一个文件夹或文件。AI 读到"写文章"这个任务，自动按这条线走。

**闭环二：知识管理**

信息来源（播客/文章/书）→ 消化（摘要/金句）→ 分类存档 → 选题反哺

这个闭环的关键是"消化"——原始信息进来不能直接放着，得经过一轮压缩和结构化，才能变成可检索的素材。

**闭环三：周复盘**

每日日志追加 → 周计划对比 → 年度目标追踪 → 下周规划

这个闭环的价值是让系统自己"跟踪自己"。每周末我让 AI 读本周`daily_log.jsonl`、对比`02 周计划`、计算年度目标进度，自动产出一份复盘。

三、插件生态：让 Obsidian 真正"活"起来

搭完文件夹、写完 CLAUDE.md，只是把骨架搭好。

要让 Obsidian 真正跑起来，还需要两样东西：**合适的插件**（把信息搬进来、管起来、输出出去），以及**CLI 能力**（让 AI 直接调用 Obsidian）。

截止 2026 年初，Obsidian 社区插件已经超过 2700 个。看着吓人，但按"采集 → 整理 → 输出"三个阶段来选，每个阶段 2-3 个就够了。

3.1：采集：把信息搬进 Vault

AI 生产力系统的第一个瓶颈，不是"怎么写"，而是"写什么"。没素材，AI 再强也是空转。

**① Web Clipper（官方）**

看到一篇好文章，点一下扩展图标，整篇以 Markdown 存进 Vault。标题、正文、链接、图片都保留。

比"收藏到浏览器书签然后再也不看"强在哪？存进 Vault 就是 AI 可以`grep`的素材，而不是躺在收藏夹里的死链接。

**② 微信读书插件**

在插件社区搜索“weread”就能下载

![](https://mmbiz.qpic.cn/mmbiz_png/CFe2b8yvCoxiao6s5xib9szDiamsib1h9iaVQR1iacmONJR3bichdV7ic37TaJL5bdvOvRdT1ibZ7Ac7zeGJB0OPK9PBKxTyEicD01fZRMFwibbdwIDzRg/640?wx_fmt=png&from=appmsg)

一键同步微信读书的所有划线、笔记、书评到 Vault。每本书一个文件，带 （书名、作者、进度）。

AI 写文章时能直接搜你划线过的段落，比从头搜互联网快得多，而且是你亲自筛选过的内容。

**③ RSS**

![](https://mmbiz.qpic.cn/mmbiz_png/CFe2b8yvCoyYVyBbic9AAbjPibLegibgg4p5tXlI9NN4nwasR9ibOXZmWkLSHDPy7nFibfRgSq0TRuFWH0FCFib6CKFWb8YicDtXvwmz8ia4AugsojU/640?wx_fmt=png&from=appmsg)

订阅播客字幕、技术博客、Newsletter 的 RSS。自动拉新内容，以笔记形式存到指定文件夹。

我的`每日播客/`文件夹就是这么来的——AI 每天自动从 RSS 拉字幕，整理成摘要等我消化。

3.2：整理：把信息变成可查询的知识

**① Dataview**

用类 SQL 语法查询你的笔记库。比如「所有`status: 待写`的笔记，按优先级排序」：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/CFe2b8yvCoyeYBpqBKAbzEN1NCdVaNnaQZdqkyjib6eLrtFkfrSVsL8icjL9jvc9O6Evr8kWW6wHGXeh2jNSQsc4tMGCbjibiaDUNMWxsA56uaU/640?wx_fmt=png&from=appmsg)

Dataview 帮你维护的结构化视图，反过来也会指导 AI 的行为——AI 看到选题看板就知道该优先写什么。

**④ QuickAdd**

解决"捕获一个想法要打开 Obsidian、找文件夹、新建文件"的摩擦。

![](https://mmbiz.qpic.cn/mmbiz_png/CFe2b8yvCoxQibiajAjSTpYZnZOnxQFMEOL1Nso0GABFia4icgxyaicmibkHOGFia6IawsaOdBQicpH5qLtaQ6TzXVccSrjqCqo6RZjKyWnzaGkpaXU/640?wx_fmt=png&from=appmsg)

我设了几个快捷键：

`Ctrl+Shift+A 新增一条选题，自动写入``02 选题管理`

`Ctrl+Shift+N 新增一条笔记到收件箱`

按一下，弹出输入框，写一句回车就完事。

3.3：输出：把知识变成产品

**① Kanban**

看板视图。每张卡片是一个笔记文件。我用它管文章写作进度：选题 → 写作中 → 待审 → 已发布。

Claude Code 能直接读取看板状态，知道每篇文章在哪个阶段。

![](https://mmbiz.qpic.cn/mmbiz_png/CFe2b8yvCoy0ib11sgicuPJibM5mRsibAG1eQPpKrVj1bHJa4wy7pISxSTziaFicoSGLCxMYjFb042sDWdpBPoeaDCZzlicgoLYZ8EjhcT2dDUS3uM/640?wx_fmt=png&from=appmsg)

**② Excalidraw**

在 Obsidian 里画手绘风格的流程图、架构图、概念关系图。画完能嵌入笔记，也能导出图片。

说实话我用得不多，因为大部分图我直接让 AI 生成。Excalidraw 更适合需要精细调整的场景。

四、CLI：Obsidian 真正的"AI 通道"

让 AI 能真正用起Obsidian 的关键，是 CLI。

![](https://mmbiz.qpic.cn/mmbiz_jpg/CFe2b8yvCoyicM7ef4LqUBHc9g2OV555DsHg1Y8iboXaq4zg2lg0JwJ3aaiaDmIEn3qhQ5aianqS84xgXCSjoVgaulPw9EnTN9TgX6Om8Kp5jEo/640?wx_fmt=jpeg)

Obsidian 本身支持**URI Scheme**，也就是通过`obsidian://`协议直接打开 Vault 中的任意文件、执行操作。

比如：

```
# 新建文件obsidian://new?vault=obsidian&name=新笔记&content=内容# 搜索obsidian://search?vault=obsidian&query=上下文工程
```

我们可以在终端里、Claude Code 里、Shortcuts 里、任意自动化工具里，**一行命令让 Obsidian 打开某个笔记或跳到某个位置**。

更合适的是，现在都可以让 Agent 执行上面的命令，我们用自然语言描述就可以了

我的用法：

- AI 起草完文章后，让它用 CLI 打开到写好的文件，方便我审稿
- Skill 调用时返回 URL 链接，点击就能跳到对应的参考文档
- 写文章时让 AI 插入相关笔记的 URL 链接，读者点击能跳到我的原始笔记
AI 能直接`cat`、`grep`、`rg`遍历整个 Vault，按需加载上下文。

本地文件加本地 CLI，就是目前为止 AI 读写个人知识最低成本的方案。

五、写在最后

obsidian 的同步，可以实现跨设备操作，在手机或其他电脑使用文件的，可以参考下面方式

- **官方会员：价格较贵，据反馈咸鱼可以低价拼团**
- **iCloud：适合 50GB 以内，毕竟 50GB 的 icloud 会员只要 6 元一个月**
- **NAS：适合 100GB 以上的，比较折腾，需要自己搭自动同步脚本**
- **Git：使用 github 同步，适合 10GB 以内的，太大不推荐**
很多人还把它当成一个"笔记 App"，觉得它门槛高、功能碎、学习曲线陡。

但我现在的看法是：**Obsidian 是个人 AI 生产力系统最好的起点**。

它把 AI 需要的三件事：**MD文本、结构化目录、CLI 调用、插件生态，**

做到了最简单、最开放、最可控。

搭建一套完整的 AI 生产力系统，听起来是个大工程。但其实拆开来看，就是：

- 选一个 Vault 位置
- 搭一套文件夹结构
- 写一份 CLAUDE.md
- 导入你的个人上下文
- 跑通一两个工作闭环
做完这五步，你就已经有一个"懂你"的 AI 助手了。

参考资料

- Obsidian 官网：https://obsidian.md
- Agent Skills 开放标准：https://agentskills.io
- Claude Code 文档：https://code.claude.com/docs
- 本文节选自我的 AI 生产力专栏系列第四章，obsidian 的使用教程
如果大家想要更系统的掌握 coding Agent、Obsidian、Skill、Vibecoding 的技能，欢迎订阅我的 AI 生产力专栏+社群。接下来就要更新 Obsidian 更详细系统的使用、还有 vibecoding 基础和 Coding Agent 的使用待更新。

![](https://mmbiz.qpic.cn/mmbiz_jpg/CFe2b8yvCoxP1nZVnPTby0aJ3QUXfxRZeicsqvMIs9q8uycvPf8vCSSKDiaT4yd7hjTLub9HKpflibDGk66HVeibicG2eOa4N0zS8ic3fJWWrlibRo/640?wx_fmt=jpeg&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=13)

我是空格，持续分享 AI 产品的思考与实践。
