---
title: "Open Design：把 Agent 变成设计引擎的本地开源工作台"
author: "山行AI"
publish_date: "2026-08-07 19:00:02"
saved_date: "2026-08-08"
source: "wechat"
url: "https://mp.weixin.qq.com/s/LWZZKCGLhRw66Bp4siiQLw"
---
# Open Design：把 Agent 变成设计引擎的本地开源工作台
QUOTE

Open Design 不是又一个“画布工具”。它更像是给 Claude Code、Codex、Cursor、OpenClaw 这类编码 Agent 外接了一间设计工作室：brief 进来，设计系统定调，插件和 skill 负责生成，最后产出真实文件。

01

本地优先

macOS / Windows 桌面 app，BYOK 和本地 daemon 是核心。

02

Agent-native

复用 Claude Code、Codex、Cursor、OpenClaw 等本地 CLI。

03

资产化

skills、templates、design systems、plugins 都是可版本化目录。

Open Design 的定位很直白：**开源版 Claude Design 替代品**，同时也是一个本地优先的桌面设计工作台。它支持 macOS 和 Windows，围绕 DESIGN.md、skills、design templates、plugins 和 MCP，把设计产物从“聊天里的截图”拉回到可以导出、可以复用、可以交给工程继续做的文件系统里。

NOTE

截至 2026-08-07，GitHub API 显示这个仓库已经有 **84,261 Star**、**9,811 Fork**，主语言是 **TypeScript**，许可证是 **Apache-2.0**，当前根包版本是 **0.16.2**。这几个数字不等于项目成熟度，但说明它至少已经不是一个没人验证的小实验。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WHl70lu0cr44jp7XW4KR3cUeQ8RWyy7ozHCV1r4klx0Yp0A6r3T6oCZem5tNd9EF3HAJLVxIuEt14OgnwjY3cxzUfgIUxiae2cwxKavQddMs/640?from=appmsg)

— Open Design 官方 Hero 图

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WHl70lu0cr4L2kuxuJepwHeowaOTCbcNibpMfCcMlL54rqb25JEwPFeQrKZ3yhaT4XmzCX04qr3J3viaLkdbpOpN2ckJ4SogbW3NnqfP7zaGU/640?from=appmsg)

— Open Design 功能架构图

    01

      WHAT

### 它到底解决什么问题

Claude Design 的关键变化，是让 LLM 不再只输出文字，而是直接交付设计 artifact。Open Design 接住了这个思路，但把它换成了开源、本地优先、可组合的版本。

它的核心判断是：未来的设计生产，不一定从一个空白画布开始。更常见的路径可能是：产品经理写 brief，团队已有品牌系统，Agent 读到设计约束，选择合适的模板和 skill，然后把原型、仪表盘、PPT、图片或视频直接生成出来。

所以 Open Design 的重点不是“让 AI 画得更炫”，而是把设计流程拆成几层可维护的资产：

层作用DESIGN.md团队品牌契约，约束颜色、字体、组件和表达方式Functional skills告诉 Agent 如何完成具体设计任务Design templates定义原型、deck、dashboard、image、video 等渲染形态Plugins把工作流、模板、场景和能力打包分发MCP / CLI adapters让 Claude Code、Codex、Cursor、OpenClaw 等 Agent 能直接调用

换句话说，它想做的不是“网页生成器”，而是一个 **Agent 时代的设计资产操作系统**。

    02

      PRODUCT

### 产品形态：一个入口，多种产物

README 里的产品 tour 很清楚：Open Design 从 Home 进入，用户选择 skill、设计系统和 brief；Automation 管重复流程；Design System 管品牌契约；Plugin 管扩展；Integrations 管外部系统和 MCP。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WHl70lu0cr4yBy5RtFam191MzIeIqN1AYXLG2FX8HMNZQpb787x0ZJpCQ2t6pYUB4qTk9tPzibIVpibhqstG9GV2YicjaBM8NHQGJ2Kva86IibU/640?from=appmsg)

— Home 首页：从一个入口选择 skill、设计系统和 brief

![](https://mmbiz.qpic.cn/mmbiz_png/WHl70lu0cr5cvKFxETM1vJDSOBfO7JMvsIucsLqcM8ic8ItUWqWocCBxBqq7EAibyG5zKnurMYbpibSICnFeSG2fb3by4L9Rl3ibliciauLbvObnU/640?from=appmsg)

— Automation：把重复设计流程变成可调度自动化

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WHl70lu0cr5glvkrrI6pCH9mqq5Ie3ynEwoNqbk52g4kFkmoJHu1GicuLlYUcQNq9JALzREmxDzf6lNqEnpE9YKibaqKZTgiaoZibVyfZqhnM2U/640?from=appmsg)

— Design System：将 DESIGN.md 沉淀为品牌契约

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WHl70lu0cr6ZE1CuvvyWhENwmmtvEAEqoiapkBnak9043qNXSYAf3eYhLSicgn4GUrH3L47Vhj1OUNz9QrcY0QtIUqHYcA4MYTibEt6mH3KzL4/640?from=appmsg)

— Plugin：浏览、安装和分发工作流插件

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WHl70lu0cr6YeH1w72g7SX3ibXl7LHwwydXiaOVUKRU6Hqy3IL2vqBpBE8RVWacLLRNCly1ahzM1Xk9iaEwwGuFX95Jt2bI2jZPMvt85eiag5I4/640?from=appmsg)

— Integrations：连接外部系统与 MCP 工具

进入项目的 Studio 后，同一套设计系统可以产出多种 artifact：网页/桌面/移动原型、实时仪表盘、HyperFrames 动效、deck、图片和视频。这一点很关键，因为它把“设计工具”从单一画布，改成了多输出面的工作台。

![](https://mmbiz.qpic.cn/mmbiz_png/WHl70lu0cr5Xib74IIbtYhYOVo0mnbw1esW8LgfS3v0I6aVfHnnuyQnjiau99HbN3ibuB5kFFtuXUjoAklcvVXKlibYeia4J3wp86NBc46WsgIw8/640?from=appmsg)

— Studio Prototype：在沙箱 iframe 中预览 HTML 原型

![](https://mmbiz.qpic.cn/mmbiz_png/WHl70lu0cr48tMtUCn4CQ1NpWkRVMctJqeM7GaibvDHCGqdDh5Qvia3sx357UTc1KHNyU9CXO8dZpR324ED3mhPkB2A2icdR6hCrYC5HzxdXNA/640?from=appmsg)

— Studio HyperFrame：程序化动效并导出 MP4

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WHl70lu0cr6uB1GTEoFkZnYgYUFZ2ib5WyF6mzmPNcwPxhBbic9fHlmcQhElJzHeicjaUJGzasDIdMRWwcxiahsy7H3qt8d4wXVYL7ChiaLMFBHE/640?from=appmsg)

— Studio Deck：演示文稿和 PPTX/PDF 导出

![](https://mmbiz.qpic.cn/mmbiz_png/WHl70lu0cr6vlSs97XiatM2icicTOicLR4veTkQCR6AVpVx09YeJzTRvsLNLEMFgX1fGVvcsDeicbSUeKia36rs7Sh7CSfBR4ISXZzAPgAUnsaheY/640?from=appmsg)

— Studio Image：品牌级图片和视觉资产生成

    03

      ARCH

### 架构模式：本地 daemon 是中枢

从 README 给出的架构图看，Open Design 不是纯前端工具。它大致分成三层：

1**前端与桌面壳**：Next.js 16 / Electron，负责 chat、文件工作区、iframe 预览、设置、导入和 MCP UI；

2**本地 daemon**：Node 24 + Express + SQLite，提供 /api/skills、/api/design-templates、/api/plugins、/api/chat、/api/proxy/*、MCP stdio server 等能力；

3**外部 Agent/runtime**：daemon 根据 runtime definitions 调用本机已有的 Claude Code、Codex、Cursor、OpenCode、OpenClaw、Hermes 等 CLI，让它们成为设计生成引擎。

这里的设计很有意思：Open Design 本身并不试图“再造一个 Agent”。它更像一个中间层，负责把 brief、设计系统、模板、文件系统和现有编码 Agent 串起来。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WHl70lu0cr5YzGiagoS3XurQUPByNoeazMmurU2n46lk1rHx0hBLCwZ1wUPnQ2eyVo5HQ0nlfa3ico8addj1a0XUIz0gwpafVQgaOto4Dz6Hk/640?from=appmsg)

— Open Design 工作流图

README 里的完整工作流可以压成一句话：

    .
    .
    .
    text

  brief → plugin → direction → design system → artifact → handoff → memory

也就是说，一个 PM 提交需求后，系统先选择插件和方向，再绑定设计系统，由 Agent 生成 artifact，最后导出 HTML、PDF、PPTX、MP4 或交给工程继续开发。它不是单次生成，而是希望把确认过的字体、截图、配色和产物记下来，下次少返工。

    04

      AGENT

### Agent 兼容：把 CLI 当设计引擎

Open Design 的另一个卖点是 **agent-native**。它提供 skills、CLI 和 MCP server，主流 coding agents 可以通过一行命令接入：

    .
    .
    .
    bash

  od mcp install <agent>

README 列出的已支持对象包括 Claude Code、Codex CLI、Cursor、OpenCode、OpenClaw、GitHub Copilot、Hermes、Kimi、Antigravity、Pi Agent 等。仓库描述里还提到“25 distinct local CLI executables”，也就是说它的路线是复用你电脑上已经安装的 Agent，而不是把所有模型、执行器和上下文都塞进一个云产品。

![](https://mmbiz.qpic.cn/mmbiz_png/WHl70lu0cr7b7H5auVRW1picxmpTID87Mhf2VgTuDD3XXm4iaNqSQIUQiccH0gA8tdItSObZbdfKX485jMzbjAD5JA1UCw8KYTYoNdq8ibFGOH0/640?from=appmsg)

— Open Design 支持的 coding-agent CLI

如果没有本地 CLI，它也提供 BYOK proxy：通过 /api/proxy/{anthropic,openai,azure,google,ollama,senseaudio}/stream 接 OpenAI-compatible endpoint，并在 daemon 边缘做 SSRF 防护。这个设计把“本地优先”和“模型可替换”放在了比较核心的位置。

    05

      ASSETS

### Skills、模板和插件：真正的护城河在文件夹里

README 里有三组很关键的数字：

资产README 中的数量与描述Functional skills100+，遵循 `SKILL.md` 约定Design systems151 个以 `DESIGN.md` 为中心的品牌系统包Official plugins277 个官方插件，外加 183 个可 remix 的 reference examples

这也是 Open Design 和普通 UI 生成器的差别。UI 生成器通常把能力藏在模型和服务端里；Open Design 则把能力尽量落到可读、可改、可版本化的目录里。

比如 design templates 覆盖 prototype、deck、image、video、audio、utility 等 mode；plugins 则可以表达 Figma migration、code migration、media generation、plugin authoring、share-to-community 等场景。一个插件目录里通常会有 open-design.json，如果是 agent skill 或 scenario，还会包含 SKILL.md。

这会带来两个结果：

对个人开发者来说，Open Design 更像一个“设计技能仓库”；

对团队来说，它有机会变成一套“品牌规范 + 生成规范 + 工程交付规范”的统一目录。

    06

      OUTPUT

### 能做哪些东西

Open Design 的 demo 覆盖面很宽。默认输出面是单页 HTML artifact，可以读 DESIGN.md，在沙箱 iframe 里即时预览，并下载为源码。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WHl70lu0cr5CSkmFicweH3joYmtCsXUfq20V6Ogvc7euDMVROUBstSZnX6YachI93D0y4IybWFUjEfgEAIVHD0xpF2VI3hUEpqmeWfydu7PA/640?from=appmsg)

— Entry view：统一输入界面

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WHl70lu0cr4Hiahoykskm16GH1Z8xoibKEzqg9g5qHnlcXx0B7ShSeyxV7e3zEBt9fwdt5ZvYnSpbxXlKrVv7G3c16ThJZyMJxUNwrdkCv3yA/640?from=appmsg)

— 移动端 onboarding 原型示例

它也支持 live artifacts 和 dashboards。比如 KPI wall、decision room、GitHub dashboard 这类页面，都可以作为可编辑 artifact 反复调整。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WHl70lu0cr7kmtD1g3ABc0E377H0Qv1Erb2KmmsEEYibhksMA8Fr6g7CDoib22J7ZT4t9KtA3QPQlBWQJTwiabniaazOvaz37pZqc9Xv2ib8WEfQ/640?from=appmsg)

— Live dashboard：可编辑 KPI wall

Deck 方向则走 HTML deck / PPTX / PDF 的路线，README 里提到 guizang-ppt 以及 html-ppt-* 模板族。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WHl70lu0cr7dC2oRkxB1GYqZKzdy0hZVc5Rtz7t2XtvedD400hvUGe8KfWJkeMEicFQgia6wuFZJ0YD77mU9ZQd7aCFpmebbJUZiaUYYicnJZY4/640?from=appmsg)

— Deck mode：杂志式 PPT 示例

图片和视频也是一等产物。README 写到 gpt-image-2、ImageRouter、自定义 API，以及 HyperFrames 的 HTML + CSS + GSAP 到 MP4 渲染链路。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WHl70lu0cr6kjJhyI2TFsjvYPjsNoSk5ibziaw74vqkZjJNurdxgUfzRu8hHpltCChE7LeQkl7QVSsf23cm6ibiaiaU5tCLnH96mzHGPMN0mdHVs/640?from=appmsg)

— 图片生成示例：手绘城市美食地图

![](https://mmbiz.qpic.cn/mmbiz_png/WHl70lu0cr7HG7cf6mAcwZCvurrsfYGI0rH9gkyiagRAdrwL5RoMl2eNHiaoBMRHpfVJXCkEzibXGhk3DQZdic7wKxtKmBBtZlg6Mdm9OnPGHTM/640?from=appmsg)

— HyperFrames 示例：SaaS 产品宣传片块

    07

      START

### 上手方式

如果只是使用，官方推荐下载桌面 app，macOS 和 Windows 都支持。Linux AppImage 属于 optional lane。

如果要在 Agent 里使用，可以走 MCP：

    .
    .
    .
    bash

  od mcp install <agent>

从源码运行则是常见的 pnpm 工程路径：

    .
    .
    .
    bash

  git clone https://github.com/nexu-io/open-design.git

cd open-design

corepack enable && pnpm install

pnpm tools-dev run web

Docker 路线也给了入口：

    .
    .
    .
    bash

  git clone https://github.com/nexu-io/open-design.git

cd open-design/deploy

cp .env.example .env

echo "OD_API_TOKEN=$(openssl rand -hex 32)" >> .env

docker compose up -d

有一个小坑值得提前知道：macOS 和 WSL2 里，系统自带的 /usr/bin/od 是八进制 dump 工具，可能会遮住 Open Design 的 od 命令。桌面 app 用户最好从 Settings 里的 MCP server 页面复制客户端专用片段。

    08

      COMPARE

### 和 Claude Design、Figma、v0 这类工具怎么比

维度Claude DesignFigmaLovable / v0 / BoltOpen Design开源否否否Apache-2.0本地/自托管受限受限云端为主macOS、Windows、Docker、Vercel webAgent-nativeAnthropic 内部闭环不是主路线云端 Agent25 个本地 CLI + BYOK品牌系统专有Theme/token有限151 个 `DESIGN.md` 系统产物类型Design artifact设计文件Web/app 为主HTML、PDF、PPTX、MP4、ZIP、Markdown现有代码库刷新不是核心设计到工程需转换以生成新项目为主通过 Agent + `DESIGN.md` 更新真实 repo

我的理解是：Figma 仍然是专业设计协作的主场，v0/Lovable 更偏从 prompt 到应用，而 Open Design 想占的位置更窄也更工程化：**给编码 Agent 一个本地设计生产层**。

    09

      BOUNDARY

### 优势和边界

它的优势很明确：

1**开源和本地优先**：适合重视隐私、可控部署和可审计链路的团队；

2**复用现有 Agent**：不用等某个单一厂商把全链路做完；

3**资产可版本化**：skills、templates、design systems、plugins 都是目录；

4**导出真实文件**：HTML、PDF、PPTX、MP4 这些产物能继续进入工程和内容流程；

5**设计系统前置**：比“先生成再修风格”更接近团队长期使用方式。

但边界也别忽略：

项目覆盖面很大，学习曲线不会低；

插件、模板、runtime、MCP、daemon、桌面壳全都在一个系统里，运维复杂度比单一网页工具高；

README 的 roadmap 里还有 comment-mode surgical edits、AI-emitted tweaks panel、Plugin SDK / CLI、Figma/Pencil 迁移插件等未完成项；

它依赖外部 Agent 和模型质量，Open Design 解决的是编排和资产层，不是让每个生成结果天然高级。

所以我会把它看成一个正在快速长大的“Agent 设计基础设施”，不是一个已经可以无脑替换所有设计流程的万能软件。

    ∞

      THE END

### 适合谁关注

如果你只是偶尔让 AI 生成一张 landing page，Open Design 可能显得重。但如果你在做下面几类事情，它就很值得看：

想把公司品牌规范变成 Agent 可读的 `DESIGN.md`；

想让 Codex、Claude Code、Cursor 直接生成可交付原型；

想把 PPT、dashboard、图片、视频统一纳入一个生成工作台；

想研究 MCP、skills、plugins 如何成为 Agent 的长期资产层；

想把旧代码库刷新到新的品牌设计规范。

它最让我感兴趣的地方，不是“开源版 Claude Design”这个口号，而是它把设计能力拆成了目录、协议和本地运行时。这样一来，设计不再只是一个页面里的生成按钮，而可以成为团队仓库里可维护的一部分。

文末声明：本文由山行整理自：nexu-io/open-design（https://github.com/nexu-io/open-design），如果对您有帮助，请帮忙点赞、关注、收藏，谢谢～

END
