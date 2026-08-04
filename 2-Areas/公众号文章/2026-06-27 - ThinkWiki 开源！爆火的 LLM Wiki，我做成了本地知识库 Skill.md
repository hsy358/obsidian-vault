---
title: "ThinkWiki 开源！爆火的 LLM Wiki，我做成了本地知识库 Skill"
author: "大卫数智话"
publish_date: "2026-06-27 20:18:00"
saved_date: "2026-08-04"
source: "wechat"
url: "https://mp.weixin.qq.com/s/7CNauX-6JcwBB7613GegNA"
---
# ThinkWiki 开源！爆火的 LLM Wiki，我做成了本地知识库 Skill
![](https://mmbiz.qpic.cn/mmbiz_jpg/FQ9ichBMYQXhQWibGQU1gPlXpYViarlOvK3mDibCsgYyT3LzqDE406BAKyzj5FSTWejo8naxmnLHmtf2f42DVyg25Q/640?wx_fmt=jpeg&from=appmsg)

今年春天，Andrej Karpathy 在 GitHub 上发了一份 LLM Wiki 的思路。短短几周，这个概念就在 AI 圈里传开了。

LLM Wiki: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

我读到它的时候，有一种被印证的感觉。去年，我一直在做 ThinkDoc，企业级的知识管理平台和 AI 数据基础设施，支持多模态解析、融合检索、API 集成、智能体和私有化部署。

当 OpenClaw 这样的通用 Agent 跑在本地时，却需要一套 Agent 能长期维护的知识层，应该走 LLM Wiki 这条路。

于是，我开发了 ThinkWiki 并在 GitHub 上开源了。

![](https://mmbiz.qpic.cn/mmbiz_png/HPChZibVjmRzIxgEvYP6baBAoYSr5lHZqoRxsibWBRvRVJLDS9MNDjRIMQQMIzh8N2p2pY7rmCjicWMq1PPyB3kzibl2t9iaspSgq86kIF4AC7icA/640?wx_fmt=png&from=appmsg)

ThinkWiki 是一个面向 Agent 的本地知识库 Skill，数据留在个人电脑上，用对话就能建 wiki、收资料、做问答、看图谱。

项目地址：https://github.com/wzdavid/ThinkWiki

我自己用 OpenClaw 桌面版和 Trae 安装了这个 Skill，跑通了完整工作流。

这篇文章介绍 ThinkWiki 是什么、怎么用。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/HPChZibVjmRwv9fB7KnLPruxsWGWibnia1otbxTVGUBackBKRib6j34OG9cy3E9BhTgmeU1t28x9ONMnvM3fGsMhFoIcsDTkTw65frK3jq1knu8/640?wx_fmt=png&from=appmsg)

## 一、同为知识库，两种场景

我做了 2 款知识库，先把场景说清楚。

**ThinkDoc** 是企业级产品，运行在服务器上。它解决的是组织级知识管理：复杂版式文档的深度解析、多模态知识表示、混合检索、证据驱动的回答包、开放 API，以及和 Dify 等工作流平台的集成。企业需要多租户、分布式、私有化部署和稳定的工具契约，ThinkDoc 走的是 AI 数据基础设施这条路。

官方网站：https://bluedigit.ai/zh/thinkdoc

**ThinkWiki** 面向个人，运行在本地电脑上。你装着 Cursor、OpenClaw Desktop 或 Claude Code，想和 Agent 一起维护一份会生长的个人知识库，ThinkWiki 就是为此设计的。Markdown 是知识源，Agent 通过 Skill 对话驱动，不需要搭服务器，也不需要记一堆命令。

## 二、LLM Wiki 和 RAG，区别在哪

Karpathy 用三层架构描述 LLM Wiki：Raw 原始资料、Wiki 知识页、Schema 规则文件。

Agent 读一篇新材料，会同时更新概念页、决策页、来源页，补上交叉引用，标注矛盾。下次提问，Agent 读的是编译好的 wiki，而不是每次重新翻原始 PDF。

这和经典 RAG 的代价结构不同。

RAG 每次查询都要检索、重排、拼装，文档一多，chunk 切分和召回调参就是持续成本。

LLM Wiki 把合成前置到入库阶段，查询时读的是已经整理过的知识层。对个人研究笔记、项目决策记录、长期阅读积累这类场景，我觉得更自然。

ThinkWiki 完整实现了 Karpathy 提出的模式，并在上面加了我认为很关键的一层：可浏览、可治理的 HTML 工作台。

## 三、LLM Wiki 实现很多，为什么选择 ThinkWiki

Karpathy 提出 LLM Wiki后，GitHub 上很快冒出各种开源实现。有纯 AGENTS.md 协议的、有桌面应用的、有 VS Code 插件的、有完整 CLI 编译器的。

我开发的 ThinkWiki，有哪些不同呢？

**1. Agent Skills 规范，一次安装、多宿主可用**

ThinkWiki 遵循开放的 Agent Skills 规范（SKILL.md + 脚本目录），可以装到 Cursor、OpenClaw Desktop、Claude Code、Trae、Codex 等 Agent 上。

Agent Skills 规范：https://agentskills.io

用户不需要记 CLI 命令，直接与 Agent 对话交互：

> 帮我把这篇文章放进知识库：https://example.com/article根据我的知识库回答：什么是 AI 原生组织？生成知识图谱，在浏览器里打开工作台。

底层有统一的 `thinkwiki` 命令入口，Agent 在背后调用。这和纯 AGENTS.md 方案相比，多了一层确定性工具链。

页面生成、图谱构建、健康检查，结果是可复现的，不全靠 Agent 临场发挥。

我在 ThinkDoc 里做企业 API 的经验告诉我，关键路径需要确定性；ThinkWiki 把这件事带到了个人场景。

**2. HTML-first，知识库不只是一堆 Markdown 文件**

很多 LLM Wiki 实现停在文件层，你得到 `wiki/` 目录里的 Markdown，要自己用 Obsidian 或编辑器打开。

ThinkWiki 每次操作都会刷新 HTML 成果页：工作台首页、Inbox 复核页、本地浏览页、交互式知识图谱、图谱治理报告。

对话界面适合下指令，HTML 工作台适合阅读和治理。

![](https://mmbiz.qpic.cn/mmbiz_jpg/HPChZibVjmRzQqZ3ialibW2s3kbFJsOQNRv7lwYb4qJMDk9OleJaJhFEQKcfSibiaX09vlsM9pXKIyic6hDINUCHkzg8icILz63AuURpWItkG7FPrw/640?wx_fmt=jpeg)

在 OpenClaw 桌面版里让 Agent 执行 `serve`，用内置 browser 打开 http://127.0.0.1:8765/index.html，整个知识库可以像一个小产品一样浏览。这个分工是我日常用起来最顺手的部分。

**3. 内容知识图谱，而不只是文件链接图**

从 v1.6.0 起，ThinkWiki 默认生成内容知识图谱。节点包括 topic、concept、decision、claim 等语义实体，边包括 about、supports、contradicts、suggests_related_to 等关系，可以在 knowledge / document / suggested 三种视图间切换。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/HPChZibVjmRwWHToGT6wliaUHCInoRUo2XibpE928ibF02D7ZiaoucRjSKYuLv5wHjcaRic64pvia4QZ1Qqv13f4HODkkvzZicmskYU5b03uibmfEB3A/640?wx_fmt=jpeg)

图谱页带 Graph Insights，标出桥接页、弱连接页、建议补链。graph-report 列出孤立页面、高连接薄页、脆弱桥接、实体归并候选。v1.6.0 还加入了实体 alias 冲突复核和确定性归并流程。

知识库越大，结构和治理比单纯能看更重要。这部分设计借鉴了 ThinkDoc 里知识精炼和可信验证的思路，压缩到个人本地可用的粒度。

**4. Inbox 工作流，先采集、再复核、后入库**

网页、PDF、DOCX、公众号文章，都可以先 clip 到 inbox，不急着正式 ingest。Inbox 按 ready、review、weak 分组，告诉你哪些可以安全入库、哪些还要人工看一眼。微信公众号文章有专门的提取适配器，技术文里的代码块会尽量保留完整。

Agent 再聪明，偶尔也会抓错、截断、漏 metadata。先过 inbox，比直接写进 wiki 稳得多。batch-clip 和 batch-ingest 支持批量处理，适合一次性导入一个目录的资料。

## 四、OpenClaw 桌面版三分钟跑通

我自己验证 ThinkWiki 时，用的 Agent 是 OpenClaw 桌面版。这也是我开发和开源的项目，把 OpenClaw 的 Skill、模型、渠道能力封装成本地可安装的应用，普通用户装完就能聊，不用自己折腾 Node.js 和 CLI。

项目地址：https://github.com/wzdavid/openclaw-desktop

ThinkWiki 和 OpenClaw 桌面版搭配很顺。一个负责知识库，一个负责 Agent 交付，都在本机跑，数据不出电脑。

我自己的路径如下，供读者参考。

其他支持 Agent Skills 的宿主（Trae、Cursor、Claude Code 等）步骤类似，把仓库地址发给 Agent 即可。

**第 1 步，安装 ThinkWiki Skill**

在 OpenClaw 桌面版对话里发送：

> 帮我安装这个skill：https://github.com/wzdavid/ThinkWiki

Agent 会把 Skill 装到对应目录，执行 bootstrap 和 doctor 做自检。本机只需要 Python 3，ThinkWiki 首次使用会自动建好虚拟环境 `.venv`。

![](https://mmbiz.qpic.cn/mmbiz_png/HPChZibVjmRz0Ciclbic8WD36Xc90HYKiakoAuCOUu9L2wlv4zqoqWbJmc53D7WTZRNkuibxWmIlBtZR6BBjzdMMibm7EibEob8jD9ibQS27W7LibjkQ/640?wx_fmt=png&from=appmsg)

**第 2 步，创建知识库**

在 OpenClaw 桌面版对话里发送：

> 帮我在工作区创建一个名为 大卫的知识库 的本地知识库。

![](https://mmbiz.qpic.cn/mmbiz_png/HPChZibVjmRxkPZNV2wQdB9aqXYqUu1228rVIoDD0g31Ff25OZAXPCaKYZ4bf88hIBEj09Nic61hiaUpYHloKZib9wic7S1h6RUkJxcJiar0rJ1dc/640?wx_fmt=png&from=appmsg)

**第 3 步，采集和入库**

在 OpenClaw 桌面版对话里发送：

> 把这篇文章放进知识库： https://mp.weixin.qq.com/s/e6XOvzFXGTLtlXpbRsvciA

![](https://mmbiz.qpic.cn/mmbiz_png/HPChZibVjmRwBK5uI7Mha0UBupy6JDuy3cVe4FgyzKAAXyRamVhygiaP0L7foaWt3ibeWHXQiczjqoO0vQvVaF3DYUEDiboheq8kd0RzyULHGW6g/640?wx_fmt=png&from=appmsg)

**第 4 步，使用知识库**

在 OpenClaw 桌面版对话里发送：

> 基于知识库回答，如何用OpenClaw创建一个虚拟团队？

![](https://mmbiz.qpic.cn/sz_mmbiz_png/HPChZibVjmRzfPaiaNp6T1Ahlv47vASa3h7JI691ZNVmE4pEUdbY5sqkicOn69Jrxryq1yO3D7D21d4ia3gHs8icP0MMmBnd1IqCx4P4LdyXnVR0/640?wx_fmt=png&from=appmsg)

**第 5 步，浏览知识库**

在 OpenClaw 桌面版对话里发送：

> 我要查看知识库，给我链接

点击给到的链接，用系统浏览器打开 http://127.0.0.1:8765/index.html 即可。

![](https://mmbiz.qpic.cn/mmbiz_png/HPChZibVjmRwrDRPHicQ9JSRJicAKAAgaLYy3aVXj72U6F5edmZddDEyLSgR9ePWfGHK9mkqU2heria2CkoRykx9t7HD7rSPaMyZKF1ukibXg43U/640?wx_fmt=png&from=appmsg)

## 写在最后

Karpathy 的 LLM Wiki 让一个方向变得清晰：个人知识管理，可以从查询时检索，转向入库时编译。

ThinkWiki 的定位也很清晰：给 Agent 用的本地知识库 Skill。Markdown 是知识源，HTML 是可操作的工作台，图谱负责结构和治理。

它和 ThinkDoc 构成互补。你在企业里做知识底座和 AI 应用集成，看 ThinkDoc；你在自己电脑上和 Agent 共建一份会生长的 wiki，用 ThinkWiki。

ThinkWiki 和 OpenClaw 桌面版都已开源，ThinkDoc 面向企业客户授权许可使用。ThinkWiki 当前最新版本 v1.6.0，MIT 协议。

项目地址：https://github.com/wzdavid/ThinkWiki

欢迎 Star、试用、提 Issue 和 PR。

个人知识库这个方向，需要更多真实使用场景来打磨。你在任何一个 Agent 上安装和跑通之后，有任何反馈，对我来说都特别有价值。
