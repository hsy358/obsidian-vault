---
title: "偷偷分享 DeepSeek Harness 热榜挖到的 2 个实⽤插件"
author: "苍何"
publish_date: "2026-08-16 13:02:19"
saved_date: "2026-08-17"
source: "wechat"
url: "https://mp.weixin.qq.com/s/XKmHlMJjsS1HHkxJPcg9Uw"
---
# 偷偷分享 DeepSeek Harness 热榜挖到的 2 个实⽤插件
这是苍何的第 579 篇原创！大家好，我是苍何。

太猛了，DeepSeek Harness 截至当前已经 112 k 的 Star 了，而这距发布仅仅过去三天。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zw8bZHsVSaArB50Jt09NjqNRccMaBiczGdpFhwniaPaOEeO80FFv8ufOiaRvgtZllE3c9yIbgIRJh1aK2Uo4WCrl3XgibZXPfBHMlgn6Yp4HW6M/640?from=appmsg)

而且还在以惊人的速度增长...

DeepSeek Harness 的核心就是：**一切皆插件**。

模型、工具、技能、会话甚至是 UI 都插件，可以自由插拔组合。

说个不确切的比喻，有点 Agent 时代的 Obsidian 感觉了，自由度太高了。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zw8bZHsVSaBZAickM1s9YYTcuPic37uPTSiaHclysVXy7b5hA628ReqsQQQHkcIv3ezOAE3Y6u2TIBUUict88D0IxtvFX8C630pJlXrp8lt4ckI/640?from=appmsg)

DeepSeek Harness 发布后，我第一时间就去搜集整理了官方和社区插件。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zw8bZHsVSaDVMRHbNA6z3NKTMRwX8ibcjPcy62EEgA47MdfUBM0iaZqnbPibXJRa9K7jQX0icjibtYejgb8a3zUoeptNsq7o4YDibdiaw58VFzPkuY/640?from=appmsg)

为了筛选出高质量的插件，也第一时间去看了 GitHub 插件热榜，当时就已经 1000 多的插件了，贡献者里和我一样，一堆的二次元。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zw8bZHsVSaAPGeib5njDic97yeRhXvy0ic6l2Y6DaW5UBtiaaPkABaAtdfLeCZnNYQlrZcUiaDP9wukrZ6EEDYYRP06CPwZbguMSBKpurdkVzB60/640?from=appmsg)

其中 colleague-skill （同事 skill）这个项目，我当时看直接冲到了 GitHub dsh-plugin 话题热榜第一。

![](https://mmbiz.qpic.cn/mmbiz_png/zw8bZHsVSaDQXr8GKeBk5ddSU6zV0SZ3mHnoXNytwox4yW67K4XgmweHW8yiaQyNsflL2l0mZZFL5ZsJytEshrynmpao8Z0xG5QVHVjWvTaM/640?from=appmsg)

这个 skill 当时出来的时候就火的一塌糊涂，可以蒸馏同事。

目前这个项目已经 22.4 k 的 star 了，增长速度还是非常快的。

![](https://mmbiz.qpic.cn/mmbiz_png/zw8bZHsVSaD4Nrn9uczIFNTuO9Ytol259VjhliaGZIzDAGz0vFuY0LNicMJIJ8Sze6Nfk7sPFMSl5ljKn9iakEDgQTYE460Q8Ewb6957c2tmRc/640?from=appmsg)

如今已经升级为 dot-skill，任何人都能被蒸馏成 Skill，亲友、公众人物，甚至自己。模型是支持微信记录、PDF 等多源数据喂入。

当然了，后面基于这一思路也出现非常多的蒸馏类的开源项目，都还挺火的。

> 开源地址：https://github.com/titanwings/colleague-skill

安装也巨简单，如果你想把它放进 Claude Code 或 Codex，可以直接复制以下提示词即可：

```
●●●帮我安装该技能：https://github.com/titanwings/colleague-skill/blob/dot-skill/docs/lang/README_ZH.md
```

如果要在 DeepSeek Harness 中安装，可全局安装到 ~/.dsh/skills/dot-skill，或按项目安装到 .dsh/skills/dot-skill，之后直接调用 /dot-skill。

![](https://mmbiz.qpic.cn/mmbiz_png/zw8bZHsVSaBaATqicE10fibPOmjOwmyicjx214YkX0piaVuLYFQgGvR4UmGY6k87ibdCwSToG9tEOw9Ddw9ktdB9t4r5KOyHE31XXO5gia6ibt1iceQ/640?from=appmsg)

使用场景还挺多的，比如，把项目群聊和业务文档喂给它，就能蒸馏出一个熟悉团队背景的「AI 同事」，用来答疑、梳理信息或协助推进任务。

我看还有个排名第三的插件也非常有意思，叫 OpenBiliClaw，它可以让 Agent 能够连接和使⽤ B 站内容。

![](https://mmbiz.qpic.cn/mmbiz_png/zw8bZHsVSaC9nbhibmy0ib4QJnzjoCNg8QECzyTaKg0hdUtm7UYkLAtXx0cv2QrGjoEUv7BAxd7juibcxaVNhZ0Gic2ibpoD2PxicncqRYa5icL7D4/640?from=appmsg)

这是一个纯本地、私有、开源的自进化跨平台内容发现 Agent：从你的跨平台使用、反馈和对话中持续深化心理画像，带着对你的理解主动去 B 站、小红书、抖音、YouTube、X、知乎、Reddit、Linux.do、Bangumi、V2 EX、微博与开放 Web 找内容。

这个还挺有意思的，将各个平台的我们的数据连起来了，深度理解你后，再根据对你的理解跨平台主动搜寻你会喜欢的内容。

这个项目从 B 站起步，现已覆盖小红书、抖音等多平台。

最新也支持 DeepSeek Harness，让 DSH 里的 Agent 也能读推荐、答探测、闭环学习。

```
●●●OpenBiliClaw：https://github.com/whiteguo233/OpenBiliClawOpenBiliClaw · DSH 客户端插件：https://github.com/whiteguo233/dsh-openbiliclaw
```

你可以直接在你的 DeepSeek Harness 中装上该插件，享受真正的个性化跨平台推荐。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zw8bZHsVSaBFicbXsrCWJ9kAEeibEwISdWXmOqicn99hKsLJ2NJYWYd8lZRXMpHDuN9Bx1iaibA8lWV4mR6Vt1liatrWJLvVcSkicYciarDyIsxicelM/640?from=appmsg)

> 这个很有意思，大家可以去 GitHub 看下最新更新，也可以提 Issue。

写到这里，不知道你有没有发现一个很有意思的巧合。

**8 月 13 日晚，DSH 插件热榜排名第一和第三的两个项目，作者竟然都是 B 站 UP 主。**

榜一 colleague-skill 的作者，是 B 站 UP 主「只是路过的 titanwings」（周天奕）；

![](https://mmbiz.qpic.cn/mmbiz_png/zw8bZHsVSaBlNbcPoWVA4tp8uj12gUHO9k30ll1065yJFstKX6G577LcJDlmTa4pqvTMoTVA9QzdZg8ia7ovM3DYfuNRuHWtkpjMFPKFmSFU/640?from=appmsg)

榜三 OpenBiliClaw 的作者，则是 BIP 参赛选手、B 站 UP 主「littlewish」。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zw8bZHsVSaDzSxQ6hgwI2V0Ik8GUvgYNQukl5N1s5xSo1UrVmU0FzdNEtAC1X5ULBgAt8TicAyMmZNMnyRxSLyylmH6Yd9BfIhibXwm6aeLhI/640?from=appmsg)

一个在琢磨怎么把团队经验蒸馏成 Skill，一个在尝试让 Agent 真正理解和连接内容。

方向完全不同，但他们做的事情很像：**把新概念讲给大家听，也把想法写成代码、做成开源项目，再交给真实用户使用和反馈。**

这也是我觉得这两个项目特别有意思的地方。

以前提到 B 站的开发者生态，大家首先想到的可能是编程教程、技术分享和学习视频。

但现在，越来越多开发者开始把自己做的工具和开源项目带到 B 站：用视频讲清楚项目解决了什么问题，再把感兴趣的用户带到 GitHub 参与 Star、Fork、提 Issue，甚至一起贡献代码。

内容、开源项目和真实用户，就这样形成了一个很自然的反馈闭环。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/zw8bZHsVSaCQ5rTxuaPv0gpy8iasXoicrAmAOYbFgU7sez4M0tcb4XBwf0e6ibEnef8hOHcWfQLS84yTVDziaA45QD1zoezAibzlZt1P9vaQvkibc/640?from=appmsg)

当然，两个项目还不足以代表整个行业，排名也只是 8 月 13 日晚的一次热榜快照。

但至少从这两个案例可以看到，B 站已经不只是一个看技术内容的地方，也正在成为国内开源开发者展示成果、找到早期用户和获得真实反馈的内容场域。

有些人表面上在 B 站当 UP 主，背地里已经在 GitHub 上造下一代 Agent 插件了。

不得不说，B 站的二次元浓度是真的高，开发者浓度也越来越高了。

最后，我觉得 DeepSeek Harness 用足够开放、足够自由的方式，又一次从技术底层打开了一扇门。

你可以换模型、接工具、装 Skill，也可以把某个一闪而过的想法写成插件，丢进社区。也许几个小时后，它就会被某个素不相识的人装上、使用、提出建议，然后继续生长。

这种感觉其实很让人兴奋。

项目发布才几天，上千个插件便冒了出来。有人在蒸馏同事，有人在连接 B 站，也有人在认真解决工作和生活里那些很小、很具体的问题。

每一个插件背后，都是一个开发者真实的需求，也是一句：“这个问题，也许我能试着解决。”

开源最动人的地方就在这里：一个人的灵感被写进代码，另一个人的需求让它继续生长，最终汇成一群人共同推动的浪潮。

DeepSeek Harness 才刚刚开始。下一次刷新热榜时，上面也许会出现更多来自普通开发者、B 站 UP 主，甚至来自你我的插件。

我很期待。

毕竟，一个真正有生命力的生态，就是这样被无数个具体、真诚又有点疯狂的想法，一点点长出来的。
