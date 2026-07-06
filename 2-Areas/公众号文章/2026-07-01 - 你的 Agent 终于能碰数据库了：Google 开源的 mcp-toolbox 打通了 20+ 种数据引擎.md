---
title: "你的 Agent 终于能碰数据库了：Google 开源的 mcp-toolbox 打通了 20+ 种数据引擎"
author: "OpenMCP"
publish_date: "2026-07-01 21:20:46"
saved_date: "2026-07-06"
source: "wechat"
url: "https://mp.weixin.qq.com/s/N3Ll-_lKClDCvqAjzbWo0Q"
---
# 你的 Agent 终于能碰数据库了：Google 开源的 mcp-toolbox 打通了 20+ 种数据引擎
## 前言

前阵子我在做一个用户系统的功能，Claude 帮写得飞起，但每次涉及到数据库——「users 表有几个索引？」「最近一周订单量趋势怎么样？」——它就卡住了。

「我无法访问你的数据库。」

我只能切到 DataGrip 查完，把结果粘回来，再让 Claude 继续。来回十几趟，人先废了。

这个痛点其实每个用 AI 写代码的人都经历过：AI 助手卡在应用层，数据库这堵墙怎么都穿不过去。Google 最近开源的 mcp-toolbox 就是来拆这堵墙的。

## mcp-toolbox

![](https://mmbiz.qpic.cn/mmbiz_png/7GmUyVicIZk7dRKv4o0mBFtoAu2ibh8qKdRQicFdW3CTYlvbjsF3xI9hpWyfPef6QSRRFIaITwu2xUAjtyZLbN0D86QYeFGnBYIARTHRQtP4Hw/640?wx_fmt=png&from=appmsg)
简单说：一个 MCP 服务器，让 Claude Code、Codex、Gemini CLI 这些 AI 编程助手直接连接你的数据库——查表结构、跑 SQL、甚至帮你写参数化查询，全在对话里完成。

❌ 过去（AI 碰不到数据库）

users 表有哪些字段？ 👤

🤖 我无法访问你的数据库，你可以把建表语句贴给我看看。

🟢 现在（接上 mcp-toolbox 后）

users 表有哪些字段？ 👤

🤖 users 表有 12 个字段：id (bigint PK)、name (varchar)、email (varchar)、created_at (timestamp)……需要我查一下最近一周的新注册用户数吗？不只是「能查」。这玩意其实有两层用法，面向完全不同的场景：

**第一层：开箱即用**。 一条命令 `npx @toolbox-sdk/server --prebuilt=postgres --stdio`，你的 AI 助手立刻获得 list_tables、get_schema、execute_sql 这些标准工具。不用写一行配置，数据库直接暴露给 Agent。适合开发调试、快速探索——你在 IDE 里问一句「帮我看下 orders 表最近 100 条记录」，它当场把结果喂给你。

**第二层：自定义工具框架**。 这才是 mcp-toolbox 真正厉害的地方。你可以写一个 tools.yaml，把 SQL 模板化、参数化，精确控制 Agent 能跑什么查询、不能碰哪些表。比如定义一个「按用户名搜索酒店」的工具，Agent 只能执行你写好的那条 *SELECT * FROM hotels WHERE name ILIKE '%' || $1 || '%'* ，没法 DROP TABLE，也没法绕过参数注入。

这种「给 Agent 发受限武器」的设计思路，跟那些直接把整个数据库权限丢给 AI 的方案完全不是一个量级。你想想，生产环境的数据库，你敢让一个 LLM 自由跑 SQL 吗？mcp-toolbox 的做法是：**你定义好工具边界，Agent 在边界内执行**——连接池、IAM 鉴权、OpenTelemetry 全链路追踪它都帮你管了。

支持的数据库多到离谱：

- PostgreSQL
- MySQL
- MariaDB
- SQL Server
- Oracle
- MongoDB
- Redis
- Elasticsearch
- CockroachDB
- ClickHouse
- Snowflake
- Neo4j
- Trino……
连 Google Cloud 家的 AlloyDB、BigQuery、Cloud SQL、Spanner、Firestore 全在列表里。基本上你公司用的数据库，它都接得上。

**还有个让我拍大腿的功能：Skills 生成**。 你定义好一个 toolset 之后，一行命令 `toolbox skills-generate` 直接把它导出成一个 Agent Skill 包，装进 Gemini CLI 就能用。从数据库工具到可分发的能力包，一步到位。

### 怎么装？

最省事的方式是用 npm 直接跑——不需要手动下载二进制：

`npx @toolbox-sdk/server --prebuilt=postgres --stdio`

如果你要跑自定义配置的生产环境，建议用二进制或 Docker。安装方式官方仓库列得超全：Linux/macOS/Windows 二进制、Homebrew、Docker、源码编译都有。

装好之后在你的 MCP 客户端配置里加上：

```
{  "mcpServers": {    "toolbox": {      "type": "http",      "url": "http://127.0.0.1:5000/mcp"    }  }}
```

SDK 也覆盖了主流语言——Python、JS/TS、Go、Java，而且每个语言都接了主流 Agent 框架：LangChain、LlamaIndex、Genkit、ADK，基本你用什么技术栈都能 10 行代码以内接上。

> ❝来源：googleapis/mcp-toolboxstar：15.8k许可：Apache-2.0

> ❝⚠️ 注意事项：预置工具（prebuilt mode）会给 Agent 开放 execute_sql 权限，开发环境玩玩可以，生产环境务必用自定义 tools.yaml 模式做权限控制。另外部分 Google Cloud 数据库（AlloyDB、BigQuery、Spanner 等）依赖 GCP 鉴权，本地开发需要先配好 gcloud 凭证。

### 能派上用场的地方

- **AI 辅助开发**：在 Claude Code / Codex 里直接查表结构、验证查询结果，不用切窗口
- **数据分析探索**：让 Agent 帮你跑探索性 SQL，一边看结果一边迭代问题
- **生产 Agent 工具层**：把数据库操作封装成受限工具，给 LangChain / LlamaIndex Agent 安全调用
- **团队工具分发**：用 Skills 生成功能把数据库工具集打包，团队成员一键安装

### 最后

**mcp-toolbox** 是目前数据库 MCP 服务器里支持引擎最多、生态最完整的一个——15.8k star、4 个语言 SDK、20+ 数据库、自带 UI 测试界面和可观测性。从「想让 Agent 帮我查个表」到「给生产 Agent 搭一套安全的数据库工具层」，它都能兜住。

不过它也不是唯一的选择。同类里还有几个有意思的选手，各自侧重点不太一样

## 同类工具

### bytebase/dbhub

3k star。零依赖、token 高效的多数据库 MCP 服务器，支持 Postgres、MySQL、SQL Server、MariaDB、SQLite。跟 mcp-toolbox 比，它走的是极简路线——单个二进制、零外部依赖、专注做「让 Agent 安全读写数据库」这一件事。没有 SDK 生态、没有自定义工具框架、没有 Skills 生成，但胜在轻和快。

> ❝如果你只需要「Agent 能查数据库」，dbhub 更轻；如果你需要「给生产 Agent 搭一套完整的数据库工具平台」，mcp-toolbox 更合适。

### centralmind/gateway

528 star。同样是「通用数据库 MCP 服务器」，但它把重心放在了自然语言翻译上——自动把你的日常问法转成 SQL，对 LLM 做了深度优化。跟 mcp-toolbox 的自定义工具框架思路不同：gateway 让你「随便问」，它来翻译；mcp-toolbox 让你「定义好工具边界」，Agent 在边界内执行。

> ❝gateway 强调自然语言灵活性，mcp-toolbox 强调安全和可控性。生产环境倾向后者。

三者的关系：mcp-toolbox 做「全功能数据库 MCP 框架」，dbhub 做「轻量零依赖直连」，gateway 做「自然语言翻译层」。不互斥，看你更在乎生态完整还是轻量极简。

## 相关资源

- 📦 googleapis/mcp-toolbox：https://github.com/googleapis/mcp-toolbox
- 🌐 官方文档：https://mcp-toolbox.dev/documentation/introduction
- 🔌 Gemini CLI 扩展：https://github.com/gemini-cli-extensions/mcp-toolbox
- ☁️ Google Cloud 托管版 MCP Server：https://cloud.google.com/blog/products/databases/managed-mcp-servers-for-google-cloud-databases

---

点个关注，带你一起围观最前沿的 Agent 工具生态！

💬 你平时用 AI 写代码的时候，查数据库是切出去还是让 Agent 直接来？来评论区聊聊你的工作流，或者告诉我你用的什么数据库，我帮你看看 mcp-toolbox 支不支持。
