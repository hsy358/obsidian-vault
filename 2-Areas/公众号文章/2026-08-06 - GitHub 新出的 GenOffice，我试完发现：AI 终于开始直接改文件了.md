---
title: "GitHub 新出的 GenOffice，我试完发现：AI 终于开始直接改文件了"
author: "郭震AI测评"
publish_date: "2026-08-06 09:30:00"
saved_date: "2026-08-08"
source: "wechat"
url: "https://mp.weixin.qq.com/s/tWk3fWkY4UPkjfi2CfkOAA"
---
# GitHub 新出的 GenOffice，我试完发现：AI 终于开始直接改文件了
你好，这里是郭震AI测评！

这两天 GitHub 上冒出一个很新的项目：创建不到一周，已经拿到 1700 多个 stars。

它叫 `GenOffice`，想把文档、表格、演示文稿和 PDF 放进同一个 AI 工作台。
项目地址：https://github.com/genspark-ai/genoffice

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/K0iaichBcoOwV8vk8ZtpFcuQEyQXJW5MoEwTfOoherfKRldUXFDNS97KocLfOkZQRbY6z652bkR1VkhD9cTFuvJqaISmRdakKcIia1ibTZyezag/640?from=appmsg)

我没有只看介绍，而是下载了官方 macOS 客户端，又把文档引擎、演示引擎和 Agent 核心测试跑了一遍。

先说结论：客户端完整度比我预期高，但它仍在 alpha 阶段，适合马上体验，不适合直接拿生产主文件硬测。

![](https://mmbiz.qpic.cn/mmbiz_jpg/K0iaichBcoOwVNNibrPK57VcQkyhwEgyVtrMA4gEtFvDrtbOVwP6XIiaEcONZRiaylibfaEIRanhIZiaa9GAQW4lklpIFqibtFYk68YTcf1E9ySv5E8/640?from=appmsg)

GitHub 当前正式版是 v0.5.83。主体代码采用 Apache-2.0，不过 `ee` 目录另有企业许可，项目名称和标识也不包含在代码许可里。

## 1 它不是给办公软件加个聊天框

第一次启动时，GenOffice 直接把自己的定位写得很清楚：文档、表格、演示和 PDF 都放进同一套桌面应用。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/K0iaichBcoOwWkeSUNmLJ03g5olJhQRnAlgKwpcKkzaBVmredMaQAnLx0prKSVzu5xWxnTMETU4ibpKn5ay7JPU6HNeyoDjDBKZZYFZic9sFWg8/640?from=appmsg)

进入工作台后，三个新建入口都带着 AI，旁边还能直接打开本地文件。

我更关心的是，这些入口背后是不是独立的小工具，还是一套真正共享的文件系统和 Agent 引擎。

![](https://mmbiz.qpic.cn/mmbiz_jpg/K0iaichBcoOwVMnrNlQvajB0EDnTaQGnxuqB7jaxPM1Xmgiau4EGD9oBibbItvq3MpU2EJ0DOQ93dKy8jKYfbZnm2TRujooCCkialgzoljRvKr18/640?from=appmsg)

从源码结构看，它不是四个页面拼在一起。文档、表格、演示、PDF 各有编辑器和文件引擎，同时共用 Agent Core、模型服务抽象和项目存储。

![](https://mmbiz.qpic.cn/mmbiz_jpg/K0iaichBcoOwXdZAzv0G7iaIDg3gpalu8fM5CPgPMHm5rnJ1ic7mBpHfFK80b7OtFuXgF5f9Xsqs8MgZicex4ZChMpHma72eHGyXKtd7RYeicFicdg/640?from=appmsg)

文档编辑器能新建 `.docx`，左侧就是 AI 面板，还提供全文总结、润色和修订追踪入口。

我没有登录，所以没有发起 AI 生成；但本地编辑器、分页画布、样式区和空白文档都正常打开。

![](https://mmbiz.qpic.cn/mmbiz_jpg/K0iaichBcoOwWjIt9nAp26uSrWkbzX5sQyFTpZeODlkDjVibz7yH0X0UMGrI2XicEA1GnhklkS1oFHZpIcV4hSqLKtQV9Ru2VYlgGmONtjll8Co/640?from=appmsg)

最值得注意的是它的“窄修改”思路：原文件保留为真相源，只重写发生变化的段落或对象，没碰过的内容尽量原样留下。

这比“AI 重新生成整份文件”靠谱得多，因为复杂办公文件最怕的就是改一句话，整套样式都变了。

![](https://mmbiz.qpic.cn/mmbiz_jpg/K0iaichBcoOwWgvDFkopLM1Jvsh76oWtwMrhc9tVFyXypaNzBpHcwDR9LNy1YFgA9ia24bldREH723A3mMibTPmN6UsJx9NqgdWJyhpxqic4qtbI/640?from=appmsg)

表格编辑器也不是简化版网页表格。公式、条件格式、合并单元格、工作表保护都能看到，AI 入口则负责建表、分析和检查数据问题。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/K0iaichBcoOwX2XfVLVXhKPWomea9b5HAFQ0QO7F76vlYw84ZKSIvftuHyNvqQetJeC1icWoZf04laHGo96caqD5iajrrgPVxtto3Z4X9pllStk/640?from=appmsg)

演示编辑器提供整套生成、美化、事实核查和配图入口，空白画布、缩略图、备注和格式工具也已经齐了。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/K0iaichBcoOwXPbwqer3xHm5VdDqMpBung3djy7WbeDOI9kuE7IOeAAVZ42ib1nzAVm7VvmD9qXCAq3fyDSEcPGaLr6yfwAzSibhA0nzljXpAA0/640?from=appmsg)

## 2 我跑了源码测试，也检查了安装包

GenOffice 把五个桌面应用放在同一个仓库里，上层编辑器负责交互，下面是文件解析、渲染、补丁和导出，再往下才是共享 Agent 核心。

![](https://mmbiz.qpic.cn/mmbiz_jpg/K0iaichBcoOwU6kExiaddF9CxfttVFkctsesY4XuiaopCVOvWCEfl7jmia9fSkpicNTolye6IxRuVc7gKgSC0JcJYkibJzXHBaSib9yU4Uk3TPibZvZY/640?from=appmsg)

我先从 GitHub Releases 下载了 138MB 的 Apple 芯片版本，没有复制到“应用程序”目录，只在只读磁盘映像里启动。

签名检查显示它使用 Developer ID、开启强化运行时，并带有公证票据；系统评估结果为 accepted。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/K0iaichBcoOwWWN1vtGV7fnib2NqxsF4mKc0OCM5b7sNUgy9yBePVib7FbExMOsePSR3icaykMDq6MwSkfujIIUibR40HqibqEy5zOEZDFoF1eAbwM/640?from=appmsg)

源码侧，我在临时目录完成依赖安装，再跑三个最接近文章核心的测试包。

结果是：DOCX 引擎 428 项通过、1 项跳过；PPTX 引擎 520 项通过；Agent Core 45 项通过，一共 993 项通过。

![](https://mmbiz.qpic.cn/mmbiz_jpg/K0iaichBcoOwUvXItltl0t05MXibb3IcCpWsCUwQaKM96XRFJCib6BBFiaETgVcgyiaOxR0rwVQqoUffn1cH4fSAqj4Nkz0pbbXK4ryehJxeaWV0U/640?from=appmsg)

这能证明核心解析和 Agent 循环有真实测试支撑，也能证明客户端确实能打开三类编辑器。

但它不能证明复杂文件一定零损回写，更不能证明完整 AI 生成已经在我这台机器上跑通。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/K0iaichBcoOwWLgqbCHQue86Pia4QBIuLibFPdic026C03HPib3J74U3icC0FpKibf6AXTn9JmqsqvjGnopYia5Sglleh8IeExPzxHpysdmJ9Z1Oxgfg/640?from=appmsg)

## 3 值得试，但先用副本

GenOffice 的普通编辑功能免费、无广告、无水印；完整 AI 功能需要登录，客户端也明确提示可能消耗积分。

所以这次我没有登录、没有上传文件，也没有调用模型。

![](https://mmbiz.qpic.cn/mmbiz_jpg/K0iaichBcoOwUrrrzeYG3L4Qr5lEblOs4YhasEbwtqcfnRVYLPEHLYkfCibv9kHvtwDoUne0Vxh22OPZlo4ZsMPUmeZCia1veOH0YcHu2oRk1icc/640?from=appmsg)

还有两个现实提醒。

第一，客户端自己标注为 alpha，更新速度很快；第二，源码依赖安装完成后，审计仍提示 1 个中等级别依赖问题。它不等于已经存在可利用漏洞，但说明现在还不是“闭眼上生产”的阶段。

![](https://mmbiz.qpic.cn/mmbiz_jpg/K0iaichBcoOwV4QPqSiaZcY5AtXSvYM67NMpYicQVy2P599u1s53adKHtTYuLdXcVz7PpEnFHg8NjC3851UsZ3Jax1hCxh7tLGosFQ7QLsXU8wU/640?from=appmsg)

我建议第一次只拿复制件测试：一份带标题和表格的文档、一张含公式的表格、一套带母版的演示文稿。

重点看四件事：打开后版式是否一致、AI 只改了目标内容、保存后还能被原软件打开、公式和母版有没有丢。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/K0iaichBcoOwUwAibA5iax28lXhokL4VYERhib85uZVKlKt0IqftQQTZVzJMrxp68hZyiaicLWsZCwbqfyiaVGpvm8icUNWlzSqD8ia4uic3d7YaTMbQ1w/640?from=appmsg)

## 最后总结一下

一句话判断：GenOffice 值得马上体验，但只用副本做测试。

最适合：内容团队、产品运营，以及关注 Office 文件引擎和 Agent 工具调用的开发者。

需要注意：完整 AI 生成仍要登录，alpha 阶段不要拿唯一一份生产文件冒险。

![](https://mmbiz.qpic.cn/mmbiz_jpg/K0iaichBcoOwVia9zbo6oLiacq0n0JklicibCFjiblfa7CsShp5FVfjsYQY4iaTic3Tmq2P59opNTmakr3Q6DInVq4qmiaiaIlFwyvPaZeXOLQHmJtr6ibw/640?from=appmsg)

全文约 1700 字，17 图，如果你觉得这篇文章对你有帮助，也欢迎给我一个三连击：点赞、转发和在看；如果可以，再帮我点一个⭐️。谢谢你看到这里，我们下篇再见。
