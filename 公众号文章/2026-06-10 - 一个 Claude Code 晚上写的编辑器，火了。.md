---
title: 一个 Claude Code 晚上写的编辑器，火了。
author: 开源日记
publish_date: '2026-06-10 15:10:18'
saved_date: '2026-06-10'
source: wechat
url: https://mp.weixin.qq.com/s/WTU2hw6F0nn2pzdPoVIbug
type: wechat-article
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
  source_url: https://mp.weixin.qq.com/s/WTU2hw6F0nn2pzdPoVIbug
description: 你睡觉的时候，Claude Code 写了这个项目。
timestamp: '2026-06-10T15:10:18'
resource: https://mp.weixin.qq.com/s/WTU2hw6F0nn2pzdPoVIbug
tags:
- AI
- Claude
- notes
- 公众号
---
# 一个 Claude Code 晚上写的编辑器，火了。
你睡觉的时候，Claude Code 写了这个项目。

这并不是一个概念，而是正在发生的事。

AI 经过几天的爆肝之后，一个可以在浏览器中直接编辑 .docx 文件的编辑器就诞生了。

第一月 500  星，两个月之后就达到了 1700+，这个项目很有意思。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/VDCUoW3UiblLrj3NUhum1TGnSezj0FlxL9iahqyFiafSW2T9hWhzwCfibu48ptpCGzdfKMX3ib7Hx5AqxGJian0WZkiaTEVhEV8JArOAmagYkPZSE8/640?wx_fmt=png&from=appmsg)
它可以直接编辑 .docx 文件。

**编辑完后保存，文档原有格式不会丢。**

之后不管用 Word，LibreOffice 还是 Google Docs 打开，都可以继续编辑。

## 开发的方式比较特别

作者 Jedrzej Blaszyk 最初是因为用户需要在网页上编辑 Word 文档里的模板变量。

他找了找现有的开源方案，要么许可证不友好，要么转换来转换去格式就丢了。

干脆自己写一个。

但不是传统的一行一行敲代码，而是让 Claude Code 自动开发。他给个方向，Agent 自己迭代，用 Playwright 做视觉验证。

几天之后，编辑器就跑起来了。

很多的功能已经接近了 Google Docs。

## 这个项目填补了三难之间的空白

**01 格式不丢。**

这个前面说过了，它直接操作 .docx 里的 XML，而不是转成 JSON 或 HTML 再转回来。

我试了一下，上传一个带复杂表格的文档，在线编辑后下载，用 Word 打开，表格边框，合并单元格都还在。

**02 数据在本地，常用功能都有。**

完全在浏览器本地运行，没有后端，数据不会上传。

常用的功能都有。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/VDCUoW3UiblICM3ibm6lcJibJpDy0NIQwXfBcYRurTssWH3equJCJ2gBSkCO9u0nAlh6pLAiaEy24728UzB98xMwKgud4cMdXIGA7sd6Pw4vaTA/640?wx_fmt=png&from=appmsg)
插入表格。

![](https://mmbiz.qpic.cn/mmbiz_png/VDCUoW3UiblJN4y3mJARRg9a6nlhyghBgmdd58icg98cwqhRZjovicCyHdfK8vxUKI8X7LD6elLKia3pVnwk43SjogibxAnV6bQiaeDAFQ12fwV6k/640?wx_fmt=png&from=appmsg)
支持多语言。

![](https://mmbiz.qpic.cn/mmbiz_png/VDCUoW3UiblJH5odantPp2h1OibicfUmhkhnb9FLMFTHpZuc6Z1sM79O3qxkNBTgSS2T3MSqDvwZT3I6SdRdRNr7ibvJlspDIEfYlAraSOhNia4Y/640?wx_fmt=png&from=appmsg)
**03 修改标记。**

这是 Word 中经典的修订模式功能，但在网页编辑器中很少见。

该项目支持建议模式，打开之后你所做的所有修改都会被标记为“建议”，不会直接修改原文。

![](https://mmbiz.qpic.cn/mmbiz_png/VDCUoW3UiblI7D6libN1UBZOBuyt0qXK3aiaHQOfbfVaR9hBgEfbRpOUddHKh3cuefOAVaLLdZ0lGq5tUASMk0f5pLsY44Gn7RWUExY2Paalqo/640?wx_fmt=png&from=appmsg)
其他人可以接受或拒绝每一个修改建议，就像在 Word 中审阅修订一样。

另外，修订记录将以标准的 OOXML 格式（`w:ins`，`w:del` 标记）保存，在 Word 和编辑器之间切换的时候，修订历史也不会丢失。

**04 评论系统。**

类似 Google Docs，选中文本就能添加评论，可以回复，讨论，最后标记为"已解决"。

评论会保存在 .docx 文件的 comments.xml 里，换到 Word 打开也还在。

![](https://mmbiz.qpic.cn/mmbiz_png/VDCUoW3UiblJjiano5aWsrowd06y6jKQhhcPQJr159fzd1QBiaibPtqdYwcZAllnpoavCxxSpqohL9zqMcn7PqveqTL2jHo8Nwlqia3vicQ33KyDw/640?wx_fmt=png&from=appmsg)

## 还有一个地方我很在意，那就是为AI Agent做了适配。

**05 实时协作。**

基于 Yjs，可以多人同时编辑，实时光标显示。

评论和修改后，其它人可以马上看到。

协作后端可以选 y-webrtc，PartyKit，Liveblocks 或者 Hocuspocus。

**06 Agent SDK。**

作者为该项目做了一个 Agent 工具包，里面包含了 14 个和文档有关的工具。

AI 可以读取文档，添加评论，提出修改意见，并且可以处理修订的结果。

并且还可以和 MCP Server 一起使用，直接连接到 Claude Desktop 等客户端。

和单纯的生成内容不同，它让 AI 直接参与到文档协作的过程中。

它不是写完就走，而是用批注，修改的方式来和人一起打磨文档。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/VDCUoW3UiblIagiaEjfZyZ5AjdKAopkoIP8JElicaGS470OLkE9AKZCrWOPZVhhg5Mej8WHMcjic60QiawJ2ecTKBaicUVQr0FI41xAoibtF4LA2QI/640?wx_fmt=png&from=appmsg)
这个功能我还没深入试，但思路挺有意思。

## 看完这些功能，估计不少朋友已经想上手试试了

最简单的方式是直接访问官网 Demo：https://docx-editor.dev/editor

上传一个 .docx 文件就能编辑，保存。

如果要集成到项目里，React 项目可以用 `npm install @eigenpal/docx-editor-react`，Vue 3 也有支持（目前还是 Beta 版）。

![](https://mmbiz.qpic.cn/mmbiz_png/VDCUoW3UiblKnltIjzEibWic9T6EbqicOjpc399voe0Qiav0CVibAYaFT1KcawaagaYE1BSFp3ld4ETjCTRLVPkLK0icaVsiaYq5KwdJOA58QQnVTgk/640?wx_fmt=png&from=appmsg)

## 需要注意的地方也说一下

Vue 支持还是 Beta 版，Next.js 需要通过动态导入来处理 SSR。

协作功能的后端需要自己配置。

另外，目前没有拼写检查，邮件合并，表单字段，PDF 直接导出这些功能。

## 写在最后

经常有人抱怨说，AI写的代码质量很差。

看了这个项目之后，我认为很多问题并不是出在 AI 上，而是在模型的选择上和使用方法上。

作者用 Claude Code 晚上完成了真正可用的项目。

docx-editor 属于值得借鉴的 AI 编程实践案例。

不管你是想要在网页上处理 Word 文档，还是对 AI 编程感兴趣，都可以试一试这个项目。

项目基于 Apache-2.0 协议开放，感兴趣的同学可以去 GitHub 仓库看看源码和文档。

开源地址：https://github.com/eigenpal/docx-editor

既然看到这了，欢迎随手点赞，在看，转发，也可以给我个星标⭐，接收最新的文章，我们下期见！
