---
title: "腾讯又开源了一款AI神级项目，“开源版WorkBuddy”，支持私有化部署！"
author: "冰河技术"
publish_date: "2026-10-19"
saved_date: "2026-10-19"
source: "wechat"
url: "https://mp.weixin.qq.com/s/th-dTGRy1i-lnmfNX1OjLQ"
---
# 腾讯又开源了一款AI神级项目，“开源版WorkBuddy”，支持私有化部署！
**大家好，我是冰河~~**

前阵子刷 GitHub，看到腾讯云放了个叫 Octop 的项目。MIT 协议，自己部署，多用户，多 Agent。我第一反应是：这不就是 WorkBuddy 的开源版吗？

装完用了一阵，发现这个判断只对了一半。

像，确实像。但真把两者摆在一起看，它们面向的根本不是同一拨人。这篇文章不打算堆功能表，就聊聊我实际用下来的感受，以及它和 WorkBuddy 到底差在哪。

![](https://mmbiz.qpic.cn/mmbiz_png/mciaHGibPzCISZibIUslg1HhFdichzNic2Jvv0g4a8WickqQXwya79bN6G6kDxLzwVBkCPrLicdnnR9XVNic18BiaQEB7atm2xjH30ibx2lhUBJPYC26o/640?wx_fmt=png&from=appmsg)

## 一、它到底是什么

Octop 的官方定位是开源、自托管的 AI 助手。名字取自章鱼，触手多，暗示能同时处理好几件事。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/mciaHGibPzCIS3Yzj2x3K3ZEzAL7ic0xdibzbd4epXictcCfAKRjSxPERrIsSAJj46UjPvCp0vuglcxMWhBbQhWBJEW1nTVB8rgiauOP2SUhq6sKA/640?wx_fmt=png&from=appmsg)

它支持多用户。部署一套，可以开多个账号，给家里人一人一个，或者小团队一人一个，都行。每个账号下面还能再养几个分工不同的 Agent。

装完之后你手上会有三样东西：一个 Web 控制台、一个命令行工具，以及微信、飞书这类聊天软件的接入能力。这些全跑在同一个进程里，不需要再单独装 Redis、MySQL 之类的中间件。

项目今年 7 月初才公开，现在 GitHub 上已经攒了 5k 星。底子是腾讯云内部那套 LightClaw ACE，重新做了一遍之后放出来的。

## 二、它和 WorkBuddy 像，但不是替代关系

网上有人管它叫“开源版 WorkBuddy”。这个叫法不算离谱，但容易把两者的关系想简单。

官方从来没说过 Octop 是 WorkBuddy 的开源版，这个标签是网友自己贴的。说像，是因为 WorkBuddy 那套玩法，Octop 基本都有：专家、Skills、MCP、知识库、定时任务，两边重合度很高。而且本来就是同一家公司的产品。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/mciaHGibPzCIQe6wfmpEgGQWBtpc5vF8KeWicDwWL77ZrXianc37pbWRecIgp7vLCS1yyYnjWiarusXdTlibPBrGGcL12pcPo2a2EVUUNNBW6Wtus/640?wx_fmt=png&from=appmsg)

真正的区别在交付方式。

WorkBuddy 是云端 SaaS。登录账号就能用，模型和算力都在云上，按积分付费。适合不想折腾的人。

Octop 更像一套需要自己组装的工具。安装、配模型、配专家，都得自己来。但好处也很直接：数据在自己手里，模型想换就换。OpenAI 兼容的接口、阿里的 DashScope、本地的 Ollama，都能接，不用绑死在某一家身上。

所以它俩不是谁替代谁。腾讯现在两条线同时在推：不想折腾的普通用户，直接用 WorkBuddy；有私有化需求、想把数据和模型攥在自己手里的开发者和团队，就去折腾 Octop。

## 三、接进微信之后，我才真的开始用它

Octop 支持把 Agent 接到各种消息平台上。微信、QQ、企业微信、飞书、钉钉都行，海外的 Telegram、Discord 也支持。

![](https://mmbiz.qpic.cn/mmbiz_png/mciaHGibPzCITOGHcUyAymTRVjDTGUuiaItC4JMLXcdR06PoXwdZYWJlBJx1ug13vjLM4OIPx9WiaSWmLYmMs2mc50XRZibpSFAaGVsOcLxKYhnk/640?wx_fmt=png&from=appmsg)

配好通道以后，在群里 @ 一下就能派活，结果直接回到手机上，不用专门去开网页。

这个功能是我用得最多的。

我以前装过不少 AI 助手，基本都是新鲜两天就忘了打开。网页版尤其容易吃灰，收藏夹里躺着一堆，真想用的时候又想不起来。接进微信之后完全不一样，它就在聊天列表里，顺手就用了。

这个改动看着小，但对使用频率的影响特别大。

## 四、专家、记忆、知识库，这些是它的底子

Octop 最核心的玩法，是一个账号下面养一队专家 Agent。

![](https://mmbiz.qpic.cn/mmbiz_png/mciaHGibPzCIRV1icWj0ncxBqbWMLGUXUOtD5M0zGBnPhLoLKYLWO7vjHEqtgdP0VzYwHELdqnEd4B9uKu0HrVLCQZMX4vCEhyDiamia8OWax82g/640?wx_fmt=png&from=appmsg)

它内置了一批角色，运维工程师、热点记者、写作助手之类的都有。专家市场里还有几十个可以直接装。每个专家都有自己独立的工作区、模型配置、技能和记忆，互相之间不串。

它还给每个 Agent 配了 MBTI 人格，一共 16 种模板可以选。不满意的话，也可以自己写系统提示词。这个设计有点玩票的意思，但换个人格之后，聊起来确实没那么像在跟机器说话。

![](https://mmbiz.qpic.cn/mmbiz_png/mciaHGibPzCIQzgdvzHyxw9iciaumB6IxbnRa1XR5C8tVDrINOf4r5d9ib8RaD5eEUKqicibiczjjnkpiaWUpX0TntEq9mb8ic73L0iakaqOO1SYUe1vYo/640?wx_fmt=png&from=appmsg)

知识库这块，你可以把自己的文档丢进去。它回答问题的时候会自己去里面翻相关内容，还会告诉你出处。向量模型可以用本地的，这样既不用花 API 的钱，文档内容也不用传到外面去。

记忆也存在工作区里。聊过什么、你的偏好是什么，它都会记下来。换台机器，把目录拷过去，记忆也能跟着走。

有记忆和没记忆，体验差得挺多。很多助手聊完就忘，下次再聊跟见了陌生人一样，什么都要从头说一遍。Octop 这块做得比较实在。

定时任务也可以用大白话配，不用写 cron 表达式。比如跟它说，每天下午六点帮我写个日报，到点它自己就跑了。也可以让它每周五下午把这周没干完的事汇总成一份周报。

## 五、它不只是聊天，还能动手

浏览器自动化、终端命令、远程桌面，这些能力都是内置的。

![](https://mmbiz.qpic.cn/mmbiz_png/mciaHGibPzCIRgd47S04VdFiciaKafiasz6w3O34qWk2ODXP29icC6FjpeiaV0QicGialuBnFgyCicnXWicZnxFpfXVdnJFiaficdub3ANdG6vleGlVAxNOA/640?wx_fmt=png&from=appmsg)

开了浏览器功能之后，它可以自己去开网页、填表单、截图。终端那边，它能自己敲命令排查问题。远程桌面可以在控制台里直接看屏幕、动键鼠，Windows、Mac、Linux 都支持。

它还支持 ACP 协议，可以把写代码的活委派出去。日常杂活它自己干，真到写代码的时候，就丢给 Claude Code、Codex、CodeBuddy 这些专门的编程 Agent，它自己在中间调度。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/mciaHGibPzCIRU7Hhn8kvJVJsnVZwYGJaaPJK5DBLXT8oibjCxghXAp4mNYd5vkLjFrOxEjao4E4WbksXQkU7X1G5iabz1K1ibzAs6JzTJXaGhTY/640?wx_fmt=png&from=appmsg)

这个思路挺清楚：不什么都自己扛，该外包就外包。

## 六、安装不算难，但模型得自己准备

我装的时候用的是一键脚本。macOS 和 Linux 直接跑：

```
curl -fsSL https://finnie-1258344699.cos.ap-guangzhou.myqcloud.com/octop/install.sh | bash
```

Windows 用 PowerShell 跑对应的命令就行。不想碰命令行也没事，官方做了桌面客户端，Mac、Windows、Linux 的版本都有，下载安装包双击装就完事了。甚至连飞牛 NAS 的应用中心里都能直接装。

装完以后跑一下 `octop init` 做初始化，设置一个管理员账号，然后 `octop run` 启动。浏览器打开 `http://127.0.0.1:8088` 就能开始用。如果部署在服务器上，建议用 Docker，官方有现成的 compose 文件。

有一点得提前说清楚：模型要自己配。你需要准备一个模型服务商的 API Key，或者用 Ollama 跑本地模型也行。软件本身免费，但模型调用的费用得自己出。

## 七、适合谁，不适合谁

Octop 现在更新得挺勤。Roadmap 里写了个 AgentTeams，说是以后要支持一个协调者自动调度多个专家一起干活。这个思路和 WorkBuddy 的专家团是一样的。

但它不是适合所有人。

完全不想碰配置的人，直接用 WorkBuddy 这类成品服务更省心。打开网页就能用，不用管模型、不用管部署。

但如果你想把数据留在自己手里，想自己挑模型，或者想给团队、给家里搭一套自己的 AI 助手，那在我试过的开源自托管助手里，Octop 算是完成度比较高的一个。

工具这东西，没有高下，就看你愿意为控制权付多少折腾成本。

开源地址：https://github.com/TencentCloud/Octop

**好了，今天就到这儿吧，我是冰河，我们下期见~~**

推荐阅读：

[给大家推荐一款AI短剧生成平台](https://mp.weixin.qq.com/s?__biz=Mzg4MjU0OTM1OA==&mid=2247515806&idx=1&sn=6214e0ec2a9ebc09b1c68eb23e818eae&scene=21#wechat_redirect)

[给大家推荐一款可直接使用的AI-CR系统](https://mp.weixin.qq.com/s?__biz=Mzg4MjU0OTM1OA==&mid=2247515790&idx=1&sn=5aeda9e93df686b5e753cb9870fda0da&scene=21#wechat_redirect)
