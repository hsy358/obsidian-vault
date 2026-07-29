---
title: "knowledge-work-plugins 拆解：Anthropic 官方开源，4 种组件、3 级加载、2 层记忆，纯文件的 AI 岗位插件集"
author: "术哥无界"
publish_date: "2026-06-10 08:30:00"
saved_date: "2026-07-29"
source: "wechat"
url: "https://mp.weixin.qq.com/s/1kUy7_iRcAHik8e9g4D7sA"
---
# knowledge-work-plugins 拆解：Anthropic 官方开源，4 种组件、3 级加载、2 层记忆，纯文件的 AI 岗位插件集
> 🚩 2026 年「术哥无界」系列实战文档 X 篇原创计划 第 *135* 篇，AI 星探「2026」系列第 *14* 篇大家好，欢迎来到 **术哥无界 | ShugeX ｜ 运维有术**。我是**术哥**，一名专注于 AI 编程、AI 智能体、Agent Skills、MCP、云原生、AIOps、Milvus 向量数据库的**技术实践者与开源布道者**！

> **Talk is cheap, let's explore。无界探索，有术而行。**

![](https://mmbiz.qpic.cn/sz_mmbiz_png/icibtH5FrDwPfDnenamTf1KBysCg6SyquUJ9fOpicQQNaibLAE8WgwRUQVOXauxtxF2e4Michl5C7ewnbT4BrKvHw367IQzJluPj1rPm4ozBZBZA/640?wx_fmt=png&from=appmsg)
封面图：knowledge-work-plugins 仓库全景GitHub 上有个仓库，2026 年 1 月底创建，5 个月内拿到近 2 万 Stars。不是什么框架，不是什么模型，而是一堆 Markdown 文件和 JSON 配置。

这个仓库叫 `knowledge-work-plugins`，是 Anthropic 官方开源的插件集合。它做的事情看起来很简单：给 Claude 装上不同岗位的专业技能。但翻完源码之后，我发现它的设计比表面看到的要讲究得多——渐进式披露、工具无关抽象、安全审查机制，这些不是拍脑袋想出来的，是从工程实践中长出来的。

今天这篇文章，我不打算罗列功能。我想从源码出发，聊聊这套插件体系背后的设计决策。

> **说明**：本文内容基于 knowledge-work-plugins 项目源码（anthropics/knowledge-work-plugins）和官方文档分析整理而成，源码分析基于笔者本地仓库版本。**文中的技术分析和设计模式解读仅供参考，实际效果请以你的项目环境和测试结果为准。**如果有实际使用经验，欢迎在评论区分享交流。

## 1. 不是功能按钮，是岗位封装

先说一个容易误解的地方。

knowledge-work-plugins 不是给 Claude 加了一堆功能按钮。它的定位是**岗位型插件市场**，每个插件对应一个企业职能：销售、客服、产品、法务、金融、数据、营销、HR、工程……截至目前有 19 个 Anthropic 官方插件 + 5 个合作伙伴插件（Slack/Salesforce、Apollo、Brand Voice、Common Room、Zoom）。

仓库结构是个典型的 Monorepo。除了各业务插件目录，`.claude-plugin/marketplace.json` 是市场注册表，`.github/workflows/` 下有 4 个 CI 脚本（插件扫描、MCP URL 检查、SHA 版本更新、失败回滚），`.github/policy/` 下是安全审查策略文件。

这个定位从 `marketplace.json` 里能看得很清楚。这个 634 行的 JSON 文件是整个仓库的注册表，50 多个插件按来源分成三类：Anthropic 自建的本地目录（如 `./engineering`）、外部 Git 仓库通过 SHA 固定版本的（如 Vanta、PlanetScale）、外部仓库子目录引用的（如 Zapier、Adobe）。

第三方插件通过 SHA 锁版本，仓库里还有 `bump-plugin-shas.yml` 自动更新 SHA、`revert-failed-bumps.yml` 回滚失败更新。这不是随便堆文件，是有供应链安全考量的。

为什么说这是**岗位封装**而不是**功能增强**？因为每个插件打包的不是单个能力，而是一套完整的工作流知识。以 engineering 插件为例，它包含 10 个 Skills（code-review、system-design、incident-response 等）、9 个 MCP 连接器（Slack、Linear、GitHub、PagerDuty 等）、6 大连接器类别。你装了这个插件，Claude 就具备了软件工程师的日常操作能力，而不只是会写代码。

## 2. 四种组件，各司其职

![](https://mmbiz.qpic.cn/mmbiz_png/icibtH5FrDwPfHmbDUuKdKA5boeA4icDcQrjJQia7ohtbZEuyMmCzbNhmkjmtog5f98AgKErreQW1xbfv6MYd9sVRkTffLI0AGjLLInzO0iaNbQ0/640?wx_fmt=png&from=appmsg)
插件四种组件架构图插件内部有四种组件：Skills、Commands、Agents、Hooks。翻完源码之后，我重新理解了它们的真实定位。

### Skills：给 Claude 的指令文档

Skills 是最核心的组件，也是最值得深挖的。每个 Skill 就是一个 `SKILL.md` 文件——纯 Markdown，加上 YAML frontmatter。frontmatter 有几个关键字段：`name`（必需，kebab-case，必须匹配目录名）、`description`（必需，含触发短语）、`argument-hint`（可选，用于自动补全）、`user-invocable`（可选，默认 true）。

**Skill 的内容是写给 Claude 看的，不是给用户看的**——这一点翻源码的时候反复确认过。它用祈使句写指令（`Parse the config file`），而不是文档式的描述。frontmatter 里的 `description` 用第三人称写触发条件（`This skill should be used when...`），Claude 会根据用户输入匹配这些触发短语，自动加载对应的 Skill。

比如用户说 `review this code`，Claude 会匹配到 code-review skill 的 `review this before I merge` 触发短语，然后把 `SKILL.md` 的内容加载到上下文中。

这里有一个精妙的设计：**渐进式披露（Progressive Disclosure）**。信息分三级加载：

- Level 1：元数据（始终在上下文中，约 100 词）——name + description
- Level 2：SKILL.md 正文（触发时加载，建议 1500-2000 词）——核心知识
- Level 3：references/、examples/、scripts/（按需加载，无限制）——详细参考
为什么要分三级？因为上下文窗口是有限的。50 多个插件的 85+ 个 Skills，如果全部加载，上下文早就爆了。分级加载意味着只有用户真正用到的 Skill 才会消耗上下文空间。

### Commands：Legacy 格式，但还有独门功夫

Commands 通过 `/plugin-name:command-name` 格式显式调用。源码注释里明确说了，新插件推荐全部用 Skills 格式。但 Commands 有几个 Skills 目前不支持的能力：`$ARGUMENTS` 位置参数、`@path` 文件引用、``!`` 内联 bash 执行、`allowed-tools` 工具限制。

Data 插件就是个典型——它的 6 个核心操作（`/analyze`、`/explore-data`、`/write-query` 等）都用 Commands 格式，因为这些操作需要参数化输入。Data 插件也是双模设计的一个好例子：连接了数据仓库时，可以直接查询、端到端分析、自动迭代；没连接时，用户可以粘贴 SQL 结果或上传 CSV/Excel 文件来分析。

### Agents 和 Hooks：标注为不常用

翻完整个仓库，Agents 和 Hooks 的使用率确实很低。component-schemas.md 里直接写了 Agents 在 Cowork 中 `uncommonly used`。Hooks 也只在少数插件中出现。

但 Hooks 的安全设计值得注意。审查 prompt（`.github/policy/prompt.md`，99 行）里专门有**Hook 范围**这个维度——Hook 必须通过项目相关性门控。比如一个 Hook 只能在 `vercel.json` 文件存在时触发，不能无差别地拦截所有操作。

## 3. ~~占位符：一个被忽略的架构决策

这部分是我觉得整个项目里最有意思的设计之一。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/icibtH5FrDwPcQ46rMqdEplom4MQsib49Xk93GctVXSbqaJOqRn5nrBD6o8tvrHGeVUG4xk1u3dlfb6fgWadlbVz6Q9HGDtjtr7Cic7uibkqOUyU/640?wx_fmt=png&from=appmsg)
渐进式披露示意图Engineering 插件的 `CONNECTORS.md` 里定义了 6 个连接器类别，每个类别有一个 `~~category` 格式的占位符：

类别

占位符

默认产品

替代方案

Chat

`~~chat`Slack

Microsoft Teams

Source control

`~~source control`GitHub

GitLab、Bitbucket

Project tracker

`~~project tracker`Linear、Asana、Atlassian

Shortcut、ClickUp

Knowledge base

`~~knowledge base`Notion

Confluence、Guru

Monitoring

`~~monitoring`Datadog

New Relic、Grafana

Incident management

`~~incident management`PagerDuty

Opsgenie、Incident.io

`~~` 占位符的本质是把工作流和具体工具**解耦**。插件描述的是**做什么**（查工单、发消息、看监控），而不是**用什么做**（Jira、Slack、Datadog）。企业定制插件时，只需要把占位符替换成自己用的产品名。

这带来了一个重要的工程效果：**Standalone + Supercharged 双模**。每个 Skill 在没有外部工具的情况下也能独立工作（用户可以粘贴代码、描述问题、上传文件）。连接了 MCP 工具之后，能力自动增强（自动拉取 PR diff、链接 ticket、查询监控数据）。

说白了，这个设计降低了使用门槛。你不连任何工具，插件也能用。连了工具，它更强。这是个很务实的工程选择。

不过话说回来，这种抽象也是有代价的。从源码来看，`~~` 占位符目前没有自动发现机制——用户得手动编辑 `CONNECTORS.md` 把占位符替换成实际产品。如果企业用的是一个不在列表里的工具，还得自己写 MCP Server 配置。这不算严重的限制，但确实是实际落地时会遇到的摩擦。

## 4. Engineering 插件拆解：以源码为证

光说设计理念不够落地，拿 Engineering 插件做个具体拆解。这是 19 个官方插件里功能最完整的一个，10 个 Skills + 9 个 MCP 连接器。

### Code Review：四维审查模型

`code-review/SKILL.md`（118 行）定义了 Code Review 的四个审查维度：

- **安全性**：检查输入验证、权限控制、敏感数据泄露
- **性能**：识别 N+1 查询、内存泄漏、不必要的同步操作
- **正确性**：逻辑错误、边界条件、竞态条件
- **可维护性**：代码复杂度、命名规范、注释质量
这个 Skill 的触发短语是 `review this before I merge` 和 `is this code safe?`。用户用自然语言表达 review 需求时，Claude 会自动匹配并加载这套审查框架。

### Incident Response：SEV 分级体系

`incident-response/SKILL.md`（158 行）是 10 个 Skills 里内容最多的。它定义了 SEV1 到 SEV4 的分级响应体系：

- SEV1：生产完全不可用，全团队响应
- SEV2：核心功能受损，相关团队响应
- SEV3：次要功能异常，排入 sprint 处理
- SEV4：体验层面的小问题，记录跟踪
除了分级，这个 Skill 还覆盖了状态更新模板和事后复盘（Post-Mortem）的结构化流程。触发短语包括 `we have an incident` 和 `production is down`。

### MCP 连接器：9 个 HTTP 类型

Engineering 插件的 `.mcp.json` 配置了 9 个 MCP Server，全部使用 `http` 类型（Streamable HTTP，新版传输方式）：

```
{  "slack": { "type": "http", "url": "https://mcp.slack.com/mcp" },  "linear": { "type": "http", "url": "https://mcp.linear.app/mcp" },  "github": { "type": "http", "url": "https://api.githubcopilot.com/mcp/" }}
```

有意思的是，Google Calendar 和 Gmail 两个服务的 URL 字段在源码里是空字符串。这说明这两个集成可能尚未完成。从源码中能确认的边界信息，比 README 上写的要诚实。

你在项目中用过类似的分级体系吗？不同团队对 SEV 的定义差异挺大的，欢迎在评论区聊聊你们的做法。

## 5. 两层记忆系统：Productivity 插件的创新

![](https://mmbiz.qpic.cn/sz_mmbiz_png/icibtH5FrDwPchjD0ZwFAJB1eegHKvRUzrsE5g4hy5tImicRV0MMWxLicY2n4H8QzZYia20wicy5ia8ZhUw2ibibSR3kcsowH3yPdyiaJmibic3BqMgOvSY/640?wx_fmt=png&from=appmsg)
两层记忆系统架构图Productivity 插件是所有插件里设计最复杂的一个。它的核心创新是一个**两层记忆系统**。

### 热缓存 + 深度记忆

系统分两层：

- **热缓存**（`CLAUDE.md`）：存储约 30 个人的常用信息和术语，覆盖 90% 的日常需求
- **深度记忆**（`memory/` 目录）：包含完整术语表（`glossary.md`）、人员档案（`people/`）、项目详情（`projects/`）、公司上下文（`context/`）

### 三级查找流程

当用户提到一个人名或项目代号时，系统按三级顺序查找：

- 先查 `CLAUDE.md`（热缓存）——能覆盖绝大多数日常场景
- 再查 `memory/glossary.md`（完整术语表）——解码工作场所缩写和昵称
- 最后查 `memory/people/`、`memory/projects/`（丰富细节）
- 以上都找不到 → 问用户，然后学习并记住

### 晋升与降级

`memory-management/SKILL.md`（323 行）定义了记忆条目的晋升（Promote）和降级（Demote）机制。频繁使用的信息会从深度记忆晋升到热缓存；长期未用的信息会从热缓存降级回深度记忆。

这个设计的巧妙之处在于，它模仿了人类记忆的习惯——你不需要记住所有同事的所有信息，只需要把常用的放在**快速访问**区。`start` Skill 会引导用户初始化整个记忆系统，把团队信息导入到对应层级。

说到底这解决的是一个真实问题：AI 上下文窗口就那么大，不可能把所有信息都塞进去。分级存储加动态调整，相当于在有限空间里把信息密度拉到最高。

一个典型的使用场景：用户说 `ask todd to do the PSR for oracle`。Productivity 插件会自动解析这句话的完整含义——谁是 Todd、PSR 是什么项目、Oracle 指的是哪个客户。这些信息不是硬编码的，而是从记忆系统中动态查找的。

## 6. 元编程：用插件创建插件

仓库里有一个特殊的插件 `cowork-plugin-management`，它本身的功能是创建和定制其他插件。这在软件工程里叫元编程（Metaprogramming）。

这个元插件有两个核心 Skills：

### create-cowork-plugin（270 行 SKILL.md）

五阶段引导式创建流程：Discovery（需求发现）→ Component Planning（组件规划）→ Design（设计）→ Implementation（实现）→ Review & Package（审查打包）。最终产物是一个 `.plugin` 文件（zip 格式）。

里面还附带了三级示例插件模板：Minimal（只有一个 plugin.json）、Standard（plugin.json + skills/ + .mcp.json）、Full-Featured（完整组件，包含 skills/、agents/、hooks/、MCP、commands/）。这降低了创建插件的门槛——从模板开始改，比从零开始写容易得多。

### cowork-plugin-customizer（149 行 SKILL.md）

三种定制模式：Generic setup（通用设置）、Scoped（限定范围）、General（全局）。定制流程四步走：收集上下文 → 创建 Todo → 逐项完成 → 搜索 MCP 注册表推荐连接器。

这个元插件的存在说明了一件事：Anthropic 不只想提供固定插件，而是想让整个插件生态能自我生长。企业可以根据自己的需求，用 AI 辅助来定制和创建新插件。

## 7. 安全审查：从 prompt.md 到 schema.json

这个仓库的安全审查机制，在同类项目中不常见。

### 四大审查维度

`.github/policy/prompt.md`（99 行）定义了插件安全审查的四个维度：

维度

检查内容

基础安全

恶意代码、隐私侵犯、欺骗功能、安全绕过

Hook 范围

Hook 是否有项目相关性门控（gated vs ungated）

遥测检测

未披露的外部网络调用（analytics、crash reporter）

行为匹配

plugin.json 的 description 是否与实际行为一致

### 结构化审查结果

`.github/policy/schema.json`（52 行）定义了审查输出的结构化格式。几个关键字段：

- `passes`：布尔值，是否通过审查
- `has_broad_scope_hooks`：是否有未门控的广泛 Hook
- `has_undisclosed_telemetry`：是否有未披露的遥测
- `description_matches_behavior`：描述与行为是否一致
只要出现恶意行为、广泛范围 Hook、未披露遥测、描述与行为不匹配中的任何一项，`passes` 就会被设为 `false`。

这套审查跑在 CI 里（`scan-plugins.yml`），意味着每次提交都会自动检查所有插件。对于第三方插件来说，这是很重要的供应链安全屏障。

不过话说回来，这套审查本质上是基于 LLM 的静态分析（审查 prompt 本身就是给 AI 的指令）。它能发现明显的恶意行为和文档不一致，但对于隐蔽的 prompt 注入攻击，可能还需要更强的防御手段。

## 8. 横向对比：它和竞品的真实差距

翻完源码之后，我对几个关键维度做了横向对比。

维度

Anthropic

Cursor

OpenAI (GPTs)

GitHub Copilot

扩展格式

Markdown + JSON（纯文件）

.mdc 规则文件

JSON 配置 + API

VS Code 扩展

岗位级封装

有（19 个岗位插件）

无（仅代码规则）

有（社区 GPTs，但非岗位导向）

无

外部工具连接

MCP 协议（开放标准）

MCP（部分支持）

Actions（需 OpenAPI schema）

VS Code API

非技术人员可定制

能（编辑 Markdown 即可）

不能（需要理解代码规则）

部分（自然语言描述）

不能

安全审查

有（CI 自动扫描 + Policy Schema）

无

部分（OpenAI 审核）

部分（Marketplace 审核）

渐进式披露

有（三级加载）

无（全量加载）

无（全量加载）

无

数据来自 GitHub API（2026-06-09）和各平台公开文档。

说几个关键数字和判断：

**MCP 是核心变量**。MCP 官方 servers 仓库有 86,953 Stars，已经成为 AI 工具连接的事实标准。knowledge-work-plugins 通过 MCP 连接 40+ 外部工具，这是它区别于 Cursor Rules 或 GPTs Actions 的关键。唐巧在他的博客里打了个比方：**CLI 是给 AI 用的手，MCP 是把工具常驻在 AI 桌上，Skill 是教 AI 怎么用好工具的说明书**。

**Cursor Skills 还在早期**。awesome-cursor-skills 项目 2026 年 4 月才创建，目前 398 Stars。虽然 Cursor 也在布局类似的技能扩展机制，但体量和成熟度差距明显。

**但 Anthropic 也有短板**。合作伙伴插件目前只有 5 个（Slack/Salesforce、Apollo、Brand Voice、Common Room、Zoom），相比 OpenAI GPT Store 的数量不在一个量级。而且 Cowork 产品本身的公开信息有限，这些插件在真实企业环境中的表现如何，目前还没有公开的案例研究。

## 9. 能力边界与实际落地建议

翻完源码之后有几个明确的限制：

**Skills 不是函数**。Skills 是给 Claude 的指令文档，不是可调用的函数。执行效果完全取决于 LLM 的理解能力。这意味着同样的 Skill，在不同模型上可能表现差异很大。

**MCP 连接依赖外部**。`.mcp.json` 里配置的 MCP Server 需要用户自行部署和认证。如果企业用的是内网部署的工具，可能还需要自建 MCP Server。

**部分集成未完成**。前面提到的 Google Calendar 和 Gmail 的空 URL 是一个例子。仓库里的内容不代表全部可用。

### 实际落地建议

如果你准备用这套插件，参考 txtmix.com 的建议，我调整后的落地优先级是：

- 先改 `.mcp.json`：连接你的企业工具（这是价值最大的环节）
- 再改 `skills/`：把团队特有的术语、流程、规范写进 SKILL.md
- 最后补 `commands/`：把高频操作封装成快捷命令
如果你是 Agent Builder，这套插件的设计模式（渐进式披露、工具无关抽象、双模设计）值得直接借鉴。不需要照搬整个架构，但三级信息加载和 `~~` 占位符这两个思路，在很多 Agent 场景下都适用。

## 总结

翻完整个仓库，我对 knowledge-work-plugins 的评价是：**设计理念清晰，工程实现扎实，但生态还在早期**。

纯文件驱动让非技术人员能直接定制插件行为，岗位级封装让 Claude 从通用助手变成特定领域的专家，MCP 协议提供了连接外部工具的标准路径。渐进式披露解决了上下文窗口有限的工程难题，安全审查机制在同类项目中属于超前设计。

但 5 个合作伙伴插件、未完成的集成、缺乏公开的企业部署案例，都说明这套体系还在成长中。如果你在做 AI Agent 相关的工作，现在关注它不算早。

**好啦，谢谢你观看我的文章，如果喜欢可以点赞转发给需要的朋友，我们下一期再见！敬请期待！**
