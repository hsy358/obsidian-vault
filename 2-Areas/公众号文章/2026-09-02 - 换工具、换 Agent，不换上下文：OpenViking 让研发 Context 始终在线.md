---
title: "换工具、换 Agent，不换上下文：OpenViking 让研发 Context 始终在线"
author: "字节跳动技术团队"
publish_date: "2026-09-02 19:00:00"
saved_date: "2026-09-02"
source: "wechat"
url: "https://mp.weixin.qq.com/s/yoBTu5sIG8T19KWq_AYd-g"
---
# 换工具、换 Agent，不换上下文：OpenViking 让研发 Context 始终在线
研发的一天，往往要在多 Agent 之间切换，处理不同类型的任务。

群聊适合快速 Review 和团队协作、CLI 适合深挖代码，飞书文档分享结论、整理周报。面对不同任务，往往会选择不同的工具。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/FGB4hYw9Fee2iaESu8WvEc0MxSUSPoSIQ7gIP9gXWth0u5PW5HBc5QvdcKgehwfAt6tBeZR3LPn2Gy4ZILVDzsJuYuqkbc0GJ9zk6yCA6a4o/640?wx_fmt=png&from=appmsg)

**OpenViking：让上下文换窗口不掉队**

**真正麻烦的不是工具多，是 Context 跟不上人。**

群聊知道大家刚刚讨论了什么，却不了解完整代码；Coding Agent 能深入仓库，却未必知道团队长期形成的 Review 规则；到了飞书文档，又要重新解释这项工作的背景和结论。**每换一个窗口，研发都可能要重新复制资料、补充 Prompt、回忆历史决策。**

**OpenViking 是面向 AI Agent 的统一上下文数据库**。它不是另一个 Agent，而是位于不同 Agent 背后的共享 Context 层。OpenViking 产品介绍（复制链接至浏览器查看：https://docs.volcengine.com/docs/84313/2374478?lang=zh）

代码仓库、项目文档和 Review Guidelines 可以作为 Resource 保存；个人偏好、历史判断和 Code Learnings 可以沉淀为 Memory；可复用的工作方法则可以组织为 Skill。它们不再散落在不同工具中，而是以目录和文件的方式组织在统一的 viking:// 路径下。

![](https://mmbiz.qpic.cn/mmbiz_gif/FGB4hYw9Fec4EI9lEULOtp28cib3EnoDibLHryJTfh7DOxqKxric5XRibPuibiachXHoMecGq38cMj5dbsictqUZ71qYicgWConG2z74JO6o6wIv2IA/640?wx_fmt=gif&from=appmsg)

面对一个新任务，Agent 可以先读取 L0 摘要，再查看 L1 目录概览，最后按需加载 L2 完整内容。一次任务结束后，还可以通过 Session Commit 从对话和执行过程里提取新的经验，写回长期 Memory。

![](https://mmbiz.qpic.cn/mmbiz_gif/FGB4hYw9FedQNLsIpnQuXSTDmoTz8AiaGS8fS4Hv5nJD32SiamEt34qof7gicORiajxZoxpRuKKlXm6EP2P3nnm2BRk1VeibO9pBnR4PblCXw2Ng/640?wx_fmt=gif&from=appmsg)

因此，**OpenViking 承接的不是某一个工具的聊天记录，而是一个研发持续积累的代码背景、项目规则、技术决策、执行经验和个人习惯**。Agent 可以变化，工作界面可以变化，这份 Context 仍然能够继续使用。

**主流 Agent 极简接入OpenViking**

让 Context 不掉队可复用，第一步不是反复搬运数据，而是**让不同 Agent 都能访问同一个 OpenViking**。

OpenViking 提供了主流 Agent 的现成接入入口。访问 OpenViking  产品控制台（复制链接至浏览器查看：https://signin.volcengine.com/auth/login?redirectURI=https%3A%2F%2Fconsole.volcengine.com%2Fvikingdb%2Fopenviking%2Fregion%3Aopenviking%2Bcn-beijing%2F），进入“接入 Agent”页面，可通过 MCP、CLI、API 和 SDK 等通用方式完成集成，也可以**直接选择已经适配的主流 Agent**：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/FGB4hYw9Fecv3CAnIcibeeicGUicQ0aNny4k3r11zltCJc95lPibQNY0BZWD54Vr0V4oRKLaPQNywbJRYtt8QcdLrLNujQ6azs454xDhxgDJWEo/640?wx_fmt=png&from=appmsg)

- **Coding Agent**：Codex、Claude Code、TRAE 等均可直接安装插件。
- **AI 同事**：在办公 IM 中具备任务执行能力的 Agent，目前支持 OpenClaw、Hermes 插件集成。
- **办公场景 Agent**：已上架豆包工作插件市场，搜索 OpenViking 即可一键添加。

![](https://mmbiz.qpic.cn/mmbiz_png/FGB4hYw9FeeC9V37evfiaVXMamRJ5dU464w0qLYnnzhUpd2zvqerJ6geYtibxKLFweV90TtAuQJ3Naeqsj8kndbicDRFKr3qbIv0MuZf1iczG9I/640?wx_fmt=png&from=appmsg)

接入后，不同 Agent 都可以直接调用和沉淀同一份 OpenViking 。

**工作一｜PR Review：AI 同事 × OpenViking**

早上十点，研发打开飞书。群里已经有几个 PR 待 Review，一处文档修改准备合入，版本发布也需确认。

**这些任务不复杂，但如果专门打开 IDE，再向 Agent 重讲项目背景，反而太重**。他直接在群里 ***@ 接入 OpenViking  的 AI 同事***：

帮我看一下这个 PR，按之前的规范 Review。如果只是小问题，直接修好并提 PR。

AI 同事读取当前讨论，同时从 OpenViking 调取相关代码、项目规范和历史 Review Guidelines。它完成 Review，处理小型修改，检查 CI，再推动合入或发版。

在 OpenViking 中，这些信息并不是被拼成一段很长的 Prompt。这些知识和记忆的沉淀都是自动化的，无需用户手动导入。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/FGB4hYw9FeckTt5VePazibzajtXSJFYXhrWBOQ5bJMkXQVvc8CicMyvSJrdzbsfYVYj236v9V3sIlqfib8N93JibHbBz2s6qTOlCTbROIqfrsl4/640?wx_fmt=png&from=appmsg)

AI 同事在工作中调用 MCP，将相关代码、项目规范和 Review Guidelines 实时写入 viking://resources/{project}/。

群聊中的任务过程则通过自动化 Hook 持续写入用户的 Session。任务结束后，Session Commit 会自动提取其中的表达习惯、Review 偏好、经验和判断，分别沉淀至 viking://~/memories/preferences/ 和 viking://~/memories/experiences/。

**新确认的 Review 规则也会写回 OpenViking**。下一次，无论由谁来处理，都可以继续沿用。

**任务侧**

**Step 1：**

群聊中，AI 同事结合当前讨论和 OpenViking 中的项目规则，给出 Review 结论。

**Step 2：**

Review 后，AI 同事完成修改、检查，并推动代码合入。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/FGB4hYw9FeeQCCMWXI160yhvQu3aQgEZqzn8Kj7hGI15G3R4MIde3mRoYXLD6icaIttRyabA0qMvaetabrYaD3DtbFZVN5eatzNrAmR3pS9I/640?wx_fmt=png&from=appmsg)

**Step 3：**

从确认到发版，研发通过短消息确认版本状态，AI 同事推进后续发布流程。

**OpenViking 侧**

存储相关代码、项目规范和历史 Review Guidelines，记录新的Review 规则。

**工作二｜深度 Coding：Claude Code × OpenViking **

下午，研发开始处理另一项更复杂的任务。它需要阅读更多代码，理解现有实现，并反复核对方案。IM 的短消息窗口已经不够用了。

他转到 CLI，打开***接入 OpenViking  的 Claude Code***。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/FGB4hYw9Fee7dURB1micyQBvYdKAfMKibuxVDblEGSkTPOpmcIhKR8lsicoamMjFrDgfWIVlc0wqpibR7nRriazj7mobB3vXic4gHcMLlW6CeHWBI/640?wx_fmt=png&from=appmsg)

Claude Code 从 OpenViking 读取代码仓库、决策记录、Review Guidelines 和历史 Code Learnings。研发不必重新描述团队规则，便可以直接分析复杂 PR、查找 Agent Review 的当前实现。

任务结束时，Claude Code 通过 Session Commit 抽取新的实现理解、技术判断和 Code Learnings。下一次即使更换 Session，也可以从长期 Memory 中继续调用，而不必重新翻找这次对话。

在 CLI 中，他继续追问、细化问题、查看代码和 Review 结论。如果涉及开发，就在这里修改代码、检查 Diff、运行测试。

**任务结束前，****Claude Code 还把本次形成的实现理解、技术判断和 Code Learnings 主动存回 OpenViking**。新的经验，继续服务后续任务。

**任务侧**

**Step 1：**

Claude Code 从 OpenViking 调取已有 Review Guidelines，在 CLI 中展开更深入的代码检查。

![](https://mmbiz.qpic.cn/mmbiz_gif/FGB4hYw9FeewXlbYmU1iamVXYeWiboQVsez4HbnVb91FLoCOJR2iaVX7ZKWsiawF3A0icKOloFhlgYCeOEFwy8ibX7eSGCTUY1rkKDHad4jCkFKlQ/640?wx_fmt=gif&from=appmsg)

**Step 2：**

研发连续追问，Claude Code 检索代码并定位定位 Agent Review 的关键实现，逐步形成可执行的结论。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/FGB4hYw9FeeWM7ZWCvrxjJDwmDeic9gynWOgBnR75USicFCfUJ4h0VPicSK1JicWzhVbMlo8IiabSLgic96yUlPxrUZZcL9Cgtt6ytmP6vHfBZXiaU/640?wx_fmt=png&from=appmsg)

**Step 3：**

任务结束前，**把本次 Code Learnings 写回 OpenViking**，新理解和技术判断被保存下来，后续 Agent 可以直接复用。

**OpenViking 侧**

存储代码仓库、决策记录、Review Guidelines 和历史 Code Learnings，并记录本次任务新的实现理解、技术判断。

**工作三｜研发协作：飞书 × OpenViking **

CLI 中完成了深入分析，接下来还要得让同事看明白，且能用上。

研发回到飞书。***群聊中的 Agent 可以从 OpenViking  取回刚刚形成的代码结论，直接参与讨论、补充背景***。

OpenViking 中的资源和记忆不属于 Claude Code，也不绑定某一次 CLI Session。Claude Code 刚刚沉淀的实现结论已经拥有统一的 Viking URI；回到飞书后，群聊中的 Agent 和豆包工作可以检索相同的项目 Resource 和用户 Memory，再把相关内容带回讨论和文档。

**新的讨论结论如果再次通过 Session Commit 保存，也会继续进入用户 Memory，形成“读取—协作—再沉淀”的闭环。**

这样，研发不用从 CLI 复制一段、再到群聊解释一遍、最后又在文档里重写一遍。

**任务侧**

**Step 1：**

**回到群聊，刚刚的代码结论仍然可用**。飞书中的 Agent 读取 OpenViking，直接补充背景并参与讨论。

**Step 2：**

**在飞书文档里继续修改**。豆包工作调取 OpenViking  中的代码结论，在文档内完成补充和优化。

**OpenViking 侧**

提供来自另个 Agent 存入的代码结论、项目规则。

**工作四｜周报沉淀：豆包工作 × OpenViking**

周五傍晚，准备写周报。

这一周，他在群聊里 Review 过多个 PR，也在 CLI 中完成了复杂调研和开发。再靠自己翻聊天记录、Git Commit 和 Session，周报又会变成一次重复整理。

他**在飞书周报文档中打开豆包工作**：

基于 OpenViking 中过去一周的工作，按项目进展、关键决策、风险问题和下周计划生成周报。

***豆包工作从 OpenViking 取回本周沉淀的 PR、任务、Code Learnings、测试结果和未完成事项，直接写进文档。***

研发继续在文档中调整：“补充这个 PR 的实际影响”“技术细节再短一点”“把未完成问题放到下周计划”。

最终周报也会成为 OpenViking 中可检索的新资料。下一周的工作，从这份最新 Context 继续。

**一天里的不同任务、不同 Agent，背后是同一份 Context**

上午，AI 同事在群聊里接手短而快的协作。下午，Claude Code 在 CLI 中处理复杂代码工作。需要分享时，Context 回到飞书；周五，豆包工作再把一周内容沉淀为文档。

***他们做的不是同一件事，也不需要强行接力。***

***OpenViking 串起来的，是同一个研发长期积累的代码、规则、决策、经验和个人习惯。***

![](https://mmbiz.qpic.cn/sz_mmbiz_png/FGB4hYw9FecRZiaq0JjicrrPOjn96gic6e7wRasJdN40l3AVeibmoicheKgsAvS3vFxeBA1a8SZNHWnd6B7QHj6Il22DKo3unXFiazOkD1t60j2fU/640?wx_fmt=png&from=appmsg)

具体来看，OpenViking 在这一天里串起了五项能力：**统一组织项目 Resource、按需加载 L0/L1/L2 分层 Context、记录任务 Session、持续提取长期 Memory，以及让同一份 Context 跨 Agent 调用**。

它不是一段被反复复制的公共 Prompt，也不是某个 Agent 私有的聊天历史。工具跟着任务变化，Context 始终跟着人。

---

**加入我们，共建 Agent 上下文的未来！**

🚀** 上手试用**：访问 https://www.volcengine.com/product/openviking-service，无需自行部署，即可将常用 Agent 接入 OpenViking，体验上下文的持续积累与跨任务复用。

🌟 **给个 Star**：访问我们的 GitHub 仓库 https://github.com/volcengine/OpenViking，为我们点亮一颗Star，你的 Star 是我们前进的最大动力！

💬 **加入社区**：扫描下方飞书二维码，加入官方交流群，与顶尖开发者一起探讨 Agent 上下文的无限可能。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/FGB4hYw9Fef1JogvyaUevWFiaLs6PCqmmt8UIeGs6PYiaKDTL00hxG2fzKVd5Y4MLq4TVibdCaq1SVMsKcgVrgIGY7Sxlvia1Gb8wsHRZJcQ4NQ/640?wx_fmt=jpeg&from=appmsg)
