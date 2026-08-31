---
title: "开源版 AI Office 来了：HermesOffice 把本地 Agent 塞进文档、表格和 PPT"
author: "科技Duang实验室"
publish_date: "2026-08-08 00:08:00"
saved_date: "2026-08-31"
source: "wechat"
url: "https://mp.weixin.qq.com/s/A-sAtD3_tGF1p1yrbFKH7g"
---
# 开源版 AI Office 来了：HermesOffice 把本地 Agent 塞进文档、表格和 PPT
如果给办公软件接入 AI，你会怎么做？

最常见的答案，是在右侧加一个聊天框：选中一段文字，让 AI 润色；上传一份表格，让 AI 总结；再把答案复制回文档。

HermesOffice 想换一种思路：**AI 不只是回答问题的助手，而是能读取办公文件状态、提出修改方案，并在你确认后真正动手的 Agent。**

更关键的是，这套 Agent 默认运行在本机。文档、表格、幻灯片和 PDF，不必先交给某个云端办公账号。

项目地址：

https://github.com/criptogus/HermesOffice

## 它到底是什么？

HermesOffice 是一个面向 macOS 和 Windows 的开源 AI 办公套件，包含五个 Electron 应用：统一入口，以及 Docs、Sheets、Slides、PDF 四个编辑器。

它并非从零开始。项目是 GenOffice 的一个轻量分支，底层编辑引擎和应用代码继续跟随上游，自己的重点则放在 Hermes Agent 集成、产品身份和未来的协作能力上。

目前可以处理的核心格式包括：

●Docs：`.docx` 文档

●Sheets：`.xlsx` 表格

●Slides：`.pptx` 演示文稿

●PDF：查看、批注、表单、签名和页面操作

每个编辑器里都有同一套 AI 面板，但它不是把整个文件粗暴塞进提示词。Docs 可以按内容块生成修改、保留快照和差异；Sheets、Slides、PDF 则让 Agent 通过工具调用读取并操作当前文件状态。

## 真正有意思的，是“窄范围修改”

很多开源 Office 项目最大的问题，不是打不开文件，而是打开、修改、保存之后，原有排版就变了。

HermesOffice 的文档引擎采用了一种更谨慎的方式：打开 DOCX 时保留原始压缩包和 XML 片段，只重新生成被修改的段落，其余内容尽量原样写回。

换句话说，AI 改了第三段，就不应该顺手重做整份文档。

这种“只动脏块”的思路，比多一个写作按钮重要得多。因为在真实办公场景里，页眉页脚、批注、修订、公式、样式和复杂分页往往比正文更脆弱。AI 如果每次都重建整个文件，生成得再快，也很难让人放心。

项目对表格和幻灯片也采取类似原则：原始文件是事实来源，编辑器只提交尽可能小的修改，让未触碰的内容继续保留。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaaibkCQLP8QDMibqOicmUtYrHfMcCcFYtdjxKuDEtdtqZpUWENzsib1JMCpS7o5NvOZBIW3scNGBf1REvpHiafdmIYuyW2xXZR7yWCSSo6AEvibcg/640?from=appmsg)

## AI 为什么可以留在本机？

HermesOffice 默认连接 Nous Research 的 Hermes Agent。

应用通过 OpenAI 兼容接口访问本机 `127.0.0.1:8642` 上的 Hermes 网关。真正运行的是一个带记忆、技能、工具和 MCP 能力的完整 Agent，而不只是一次普通的模型调用。

这带来三个很现实的价值。

第一，**隐私边界更清楚。** 项目默认不要求 Genspark 账号，也不依赖第三方代理；网关、会话和文件都可以留在自己的电脑上。

第二，**AI 可以形成连续工作。** 同一文档拥有稳定会话，Agent 不必每次都从零理解上下文。

第三，**能力可以扩展。** Hermes 的技能、工具和 MCP 让 AI 有机会从“帮你写一段话”，进化成“读取表格、修改报告、制作演示文稿并保留操作记录”的工作伙伴。

当然，本地并不等于零门槛。用户仍需安装 Hermes Agent、启用本地 API Server、配置访问密钥，并保证网关在使用 AI 面板时保持运行。

## 四件套，各自能做什么？

Docs 强调 DOCX 的原格式往返、分页视图、修订、评论、样式和公式，并允许 AI 以内容块为单位提出修改。

Sheets 基于开源 Univer 核心构建界面，通过 Rust sidecar 处理 XLSX 导入导出，同时加入图表、透视表、切片器、条件格式和公式追踪。它目前的 Agent 交互也最接近理想状态：先提出操作，再展示差异，最后由用户确认并原子化应用。

Slides 使用自研 PPTX 解析、渲染和编辑引擎，覆盖母版、图表、裁剪、墨迹和文字排版等能力。

PDF 则基于 pdf.js 与 pdf-lib，提供阅读、批注、表单、印章、签名、页面管理和打印。

这套组合的野心很明显：不是另做一种 AI 文档格式，而是继续使用大家已有的 Word、Excel、PowerPoint 和 PDF 文件。

## 但现在，它还不是普通人的下载即用产品

这一点必须说清楚。

截至本文撰写时，项目 README 明确标注：签名版安装包仍在制作中。普通用户暂时需要使用上游 GenOffice，或者自行拉取代码，通过 `npm run dist:mac`、`npm run dist:win` 构建安装包；Sheets 的构建还需要 Rust 工具链。

路线图也很坦诚：多应用之间的 AI 信任体验尚未统一，协同编辑还不存在，运行时插件系统和内置 MCP Server 仍处于设计阶段，端到端测试覆盖也需要加强。

所以，HermesOffice 目前更适合三类人：

●想研究 AI 原生办公软件架构的开发者

●重视本地运行、开放格式和隐私边界的技术团队

●愿意测试早期项目并参与贡献的开源爱好者

如果你只是想找一款稳定替代 Microsoft Office 的日常工具，现在还不必急着迁移。

![](https://mmbiz.qpic.cn/mmbiz_png/iaaibkCQLP8QCj4fRldPA0PGpXvFzoKsamjD7aHF9h7H29Ued7SiaFMlwMBmhgLFrNYguDH1gq26EpDAQ6lib0IWY5IWjOEyjyxqcQbgibyp6hAA/640?from=appmsg)

## 它最值得关注的，不是“免费 Office”

HermesOffice 真正抛出了一个很好的问题：**未来的办公软件，究竟应该把 AI 放在哪里？**

是放在云端聊天框里，偶尔生成一段内容；还是让 Agent 进入文件内部，理解结构、调用工具、提出可逆修改，并为每一次操作留下可审计记录？

项目的长期路线图已经给出了方向：让不同角色的 Agent 进入文档，引入项目记忆，让外部 Agent 通过 MCP 编辑文件，同时把所有修改纳入可见、可批准、可回滚的信任流程。

这条路比“加一个 AI 按钮”难得多，但也更接近知识工作的真实需求。

眼下的 HermesOffice 仍然年轻，安装门槛和产品完成度都不适合被包装成成熟神器。不过，它拥有少见的 Office 文件处理底座，又选择了本地 Agent、开放格式和可审计修改这条路线。

如果团队能把签名发布、统一审批体验和 MCP 接口逐步做出来，它或许会成为“Agent 如何真正进入办公文件”的一个重要开源样本。

先别急着卸载现有 Office，但这个仓库，值得点个 Star 后继续观察。

## 项目信息

开源地址：

https://github.com/criptogus/HermesOffice

参考资料：

HermesOffice README：

https://github.com/criptogus/HermesOffice

Hermes 集成说明：

https://github.com/criptogus/HermesOffice/blob/main/docs/hermes-integration.md

公开路线图：

https://github.com/criptogus/HermesOffice/blob/main/ROADMAP.md
