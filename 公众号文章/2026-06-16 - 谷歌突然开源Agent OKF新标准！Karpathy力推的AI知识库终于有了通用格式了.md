---
title: "谷歌突然开源Agent OKF新标准！Karpathy力推的AI知识库终于有了通用格式了"
author: "AI寒武纪"
publish_date: "2026-06-16 09:00:00"
saved_date: "2026-06-16"
source: "wechat"
url: "https://mp.weixin.qq.com/s/nhF1cy_lIQukq_niVFvRCA"
---
# 谷歌突然开源Agent OKF新标准！Karpathy力推的AI知识库终于有了通用格式了
![](https://mmbiz.qpic.cn/mmbiz_png/kJjlNiczXgKoxNibzicCL8x3kicbpcLuYFaecgXOvG7MGe6xtQ5qyzoA4pfOMsiabic8rsKKKB7icTecM6tfzmiaN6E7xe5l3wChBpRsjDGaIcoqnYE/640?wx_fmt=png&from=appmsg)

↑阅读之前记得关注+星标⭐️，😄，每天才能第一时间接收到更新

谷歌今天发布了一个叫 Open Knowledge Format（OKF）的开放规范。

它要解决的问题，几乎每一个做 AI agent 的团队都踩过：模型本身越来越强，但它需要的上下文知识，散落在各种地方，没有人整理，也没有格式通用。

开源地址：

https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf

### AI 能力越强，知识碎片化越致命

一家公司里，AI agent 需要用到的知识大多数是内部知识：某张数据表的字段含义、某个指标的业务定义、某个系统的接入路径、某个 API 的废弃通知。

这些东西现在住在哪？

到处都是。元数据目录、内部 Wiki、共享文档、代码注释、资深工程师的脑子里。每个系统有自己的 API，每个平台有自己的数据模型，互不兼容，互不流通。

结果就是：每个搭 agent 的团队，都在从头解决同一个问题——怎么把这些散的知识拼起来喂给模型。每家厂商都在重新发明同一套数据结构，而知识本身被锁死在创建它的那个平台里，出不来。

### 开发者已经摸索出了解法，但各做各的

过去一年，一个模式在开发者中悄悄流行起来：用 Markdown 文件给 AI agent 建一个知识库，让 agent 自己去读、去更新。

这个思路被 AI 研究者 Andrej Karpathy 表达得最清楚：LLM 不会感到无聊，不会忘记更新交叉引用，一次可以同时改 15 个文件。人类维护个人 Wiki 最终放弃，往往就是败在这些琐碎的更新工作上，而这恰恰是 LLM 最擅长的。

这个模式以不同的名字反复出现：接入编程 agent 的 Obsidian 知识库、AGENTS.md 和 CLAUDE.md 这类约定文件、数据团队用来当代码管理的元数据仓库。

但问题在于：每家做法都是定制的。Karpathy 的 Wiki 和你团队的 Wiki 和某家厂商导出的目录，长得像（都是 Markdown、都有 frontmatter、都有交叉链接），但它们并没有被设计成可以互通的。没有人约定每个文档应该有哪些字段，也没有人约定文件名代表什么含义。

知识还是被锁在各自的团队里，每次搭新 agent 都得重新造轮子。

### OKF 给的答案：一个格式，不是又一个平台

谷歌今天发布的 OKF，是一个格式规范，不是服务，不需要 SDK，不绑定任何云平台。

核心设计很简单：一个 OKF bundle 就是一个 Markdown 文件目录，每个文件代表一个概念（可以是数据表、数据集、指标、操作手册、API 等），文件路径就是这个概念的唯一标识。

目录结构长这样：

```
sales/├── index.md├── datasets/│   └── orders_db.md├── tables/│   ├── orders.md│   └── customers.md└── metrics/    └── weekly_active_users.md
```

每个文件有两个部分：顶部一小块 YAML frontmatter，用于存储可以被查询的结构化字段，下面是 Markdown 正文，写什么内容完全自由。

一个完整的概念文件长这样：

```
---type: BigQuery Tabletitle: Ordersdescription: One row per completed customer order.resource: https://console.cloud.google.com/bigquery?p=acme&d=sales&t=orderstags: [sales, revenue]timestamp: 2026-05-28T14:30:00Z---# Schema| Column        | Type      | Description                              ||---------------|-----------|------------------------------------------|| `order_id`    | STRING    | Globally unique order identifier.        || `customer_id` | STRING    | FK to [customers](/tables/customers.md). |# JoinsJoined with [customers](/tables/customers.md) on `customer_id`.
```

概念之间用普通的 Markdown 链接互相引用，整个目录就变成了一张关系图，比文件系统的父子层级丰富得多。

整个 v0.1 规范，一页纸能写完。

### 三个设计原则，缺一不可

**最小约束。** OKF 对每个文件只强制要求一件事：必须有 type 字段。其他字段、文件体的内容和结构，全由使用者决定。规范管的是互通的边界，不是内容本身。

**生产者和消费者彼此独立。** 人手写的知识文件，可以被 AI agent 读取。元数据导出流水线生成的 bundle，可以在可视化工具里浏览。一个 LLM 生成的 bundle，可以被另一个 LLM 查询。格式是契约，两端的工具可以独立替换。

**格式本身，不是平台。** OKF 不绑定任何云服务、数据库、模型厂商或 agent 框架。读写它不需要任何专有账号或 SDK。谷歌选择把它作为开放标准发布，因为知识格式的价值来自有多少人在用它，不是来自谁拥有它。

### 谷歌同步发布了三个参考实现

光有规范不够，谷歌同时发布了配套工具，目的是降低试用门槛。

一个**数据丰富 agent**：自动扫描 BigQuery 数据集，为每张表和每个视图起草一份 OKF 概念文档，然后再跑一遍 LLM，爬取权威文档，补充 schema、引用和关联路径。

一个**静态 HTML 可视化工具**：把任意 OKF bundle 转成一个可以交互的图视图，单个自包含文件，不需要后端，不需要安装，数据不离开本地。

三个**可以直接浏览的样例 bundle**：GA4 电商数据集、Stack Overflow、比特币公开数据集，都是用上面那个参考 agent 生成的，提交在 repo 里作为格式合规的活示例。

谷歌特别说明：这三个工具是概念验证，不是唯一实现方式。格式对工具没有要求，生产者和消费者的生态系统可以自由生长。

### 现在能做什么

谷歌已经更新了自己的 Google Cloud Knowledge Catalog，支持摄入 OKF 格式并把它提供给 agent 使用。

规范、参考实现和样例 bundle 都在 GitHub 上开放，目前是 v0.1，显式为向后兼容扩展而设计。

谷歌给开发者的行动建议是：读规范（很短），给你的数据源写一个生产者，给你的使用场景写一个消费者，对着自己的数据跑一下参考实现，有问题就提 issue 或 PR。

参考：

https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/

--end--

最后记得⭐️我，每天都在更新：如果觉得文章还不错的话可以点赞转发推荐评论

/...@作者：你说的完全正确（YAR师）
