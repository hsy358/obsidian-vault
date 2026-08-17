---
title: "10 万星的 Deepseek Harness，终于有了精装修。"
author: "开源日记"
publish_date: "2026-08-16 14:20:25"
saved_date: "2026-08-17"
source: "wechat"
url: "https://mp.weixin.qq.com/s/PYKih2z3V2cNFIbLpjf1QQ"
---
# 10 万星的 Deepseek Harness，终于有了精装修。
DeepSeek 开源的 Agent 框架 DSH 最近太火了。

开源没几天，但打上dsh标签的插件仓库已经达到了700多个，并且还在不断增加中。

有人给它换上新衣服，有人塞进去一些小游戏，也有人直接在里面养上了电子宠物。

最近 GitHub 上就有一个挺会整活的项目。

它叫 **dsh-web-ui**，已经拿下 **2900 多个 Star**。

简单说，它就是给 DSH 的 Web UI 来了一次精装修。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/VDCUoW3UiblJe6PU1ESjzsibZbRCC3FG76aAE77DW746ibl6lJoV0MmtyN5TrH4ENgU4uyAh3ibc7WUNo3JFKCiaiaCvatDnP5Q21jeKqTWmWLLBE/640?wx_fmt=png&from=appmsg)
默认的DSH Web UI比较简陋，可以聊天、可以让Agent干活，但是看板、Git视图这些基本上都没有。

该项目把任务看板、Git 图谱、文件预览、Token 统计、移动端远程、电子宠物等全部都塞了进去。

就像别人把毛坯房交给你，你马上就开始装修一样。

## 先看看它到底改了什么

安装完毕之后，最明显的变化就是侧面栏了。

原来的网页界面一下子多了好多入口。

任务看板、Git视图、右侧边栏、实时Token统计等都已经安排好了。

![](https://mmbiz.qpic.cn/mmbiz_png/VDCUoW3UiblIMribRuyemBMK3u37vibOxDA9NY2wnicxo8Wd8icLZkkEJADeMw6bu91bxJWz2GFdkfGZDKYhOKHrjjYAicrufxJSszk4gr0IkIMww/640?wx_fmt=png&from=appmsg)
我认为最实用的是任务看板。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/VDCUoW3UiblKpBFFuDLoQxxMsxcDNOStNzwIYCvo1Vaic7wy0HHBPKWxGDzUqrQ5P48JnuUN4NGRpckUJmU3KibKK5DI20N3xgiahaDM7yuibG88/640?wx_fmt=png&from=appmsg)
任务可以依据待办、进行中、已完成、失败等状态来管理。

点击执行，真正的DSH Agent就开始工作了，完成之后的状态会自动更新，并且可以直接回到对应的执行会话中。

还可以和cron一起使用。

比如设置：

每周早上 9 点自动更新项目。

![](https://mmbiz.qpic.cn/mmbiz_png/VDCUoW3UiblJ5oOodXbMd9qFpMqeyWjeulp7taHq2g1uQ4emqcxZ7JwpzrW5Z4UKUxoVQLvGQxAV6Yb0LmW00icWLx7qVXRQO6eP69iavEQpv8/640?wx_fmt=png&from=appmsg)
到点以后，Agent 自己开工。

这时候它已经不太像聊天窗口，更像一个 Agent 工作台了。

## 右侧面板，也挺符合开发者习惯

打开项目之后，在右边就会出现文件树和预览。

可以查看和编辑代码、Markdown、PDF、Excel 等各种格式的文件，修改之后可以保存回原文件。

![](https://mmbiz.qpic.cn/mmbiz_png/VDCUoW3UiblLSll4558515gnTbCp1SJpRFf9iaob05viccsQD2iaXplo3piaUydvm8nHYx4mmlgMFPIu41KLoT9kUQGuydf4boUp0wEibOAXI9H20/640?wx_fmt=png&from=appmsg)
Git 的 stage、丢弃变更，也可以直接在面板里操作。

以前要打开多个窗口，现在尽量把它们合并到一个工作区中。

## 比较有意思的是它的宠物功能

前面的功能还挺正经。

直到我看到了这只鲸鱼娘。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/VDCUoW3UiblLuU9Mx2UPsbQibbZ3icWLpDrfp9iblSoH6AzEgJxfL1Hu4M54S96MKVvzzNuLkIwvEK4t0bSicuKfIcsV33wtBfRUXNhna9iby6r8Y/640?wx_fmt=png&from=appmsg)
它会根据 Agent 的状态切换动画。

思考、等待、工作、完成，各有不同状态。

还可以摸头、喂食小鱼干，亲密度会慢慢增长。

![](https://mmbiz.qpic.cn/mmbiz_png/VDCUoW3UiblJlScC8RfRQzcWkHN81093POpkoicPYv8RtPibgvCKicf5sQbRzTXGXk4EVUQo65ZRERWtWF8pAMiasicZYUnPvcsZ1mibZFdh92FhZc/640?wx_fmt=png&from=appmsg)
这东西当然不是刚需。

但是我觉得很有趣。

别人在研究怎样使Agent更专业的时候，它就开始研究怎样让 Agent 更人味”了。

而且宠物可以拖动、可以隐藏，不会一直挡住工作区。

## 手机也能接着干活

移动端远程也是该项目比较实用的部分。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/VDCUoW3UiblKw5vFK46Fys4YC3VlWV0Im0w0FPMcMCPMmfzrib54GFbN9K4o3KGhKtBmRJN9SVRYmh2GPGUFGNHudqFkS1zFgW7NZccdbrQx0/640?wx_fmt=png&from=appmsg)
手机扫码配对后还可以继续查看和操作工作区。

新建会话、发送消息、切换模型都可以，Agent 的思考过程以及工具调用也可以展开查看。

也就是说，电脑上的任务没有跑完，出了门也可以继续。

不过公网访问时，权限和安全配置一定要自己确认好。

## 真正有意思的，其实是插件

看到这里可能会觉得：

不就是给 DSH 加了一堆 UI 功能吗？

其实这个项目最有趣的地方就是这些东西本身也是插件。

皮肤可以单独安装，看板可以单独安装，宠物也可以单独安装。

嫌麻烦的话，还有聚合包，一次全部装进去。

正好踩到了DSH的核心理念上：

**Everything is a Plugin。**

框架提供了Agent的能力，社区不断地往里面塞东西。

有的人做生产工具，有的人做专业插件，还有的人负责整活。

**这才是我觉得这个项目真正值得关注的地方。**

## 皮肤只是其中一个开始

比如 Windows XP 皮肤。

![](https://mmbiz.qpic.cn/mmbiz_png/VDCUoW3UiblLAp5lKVmcrDrQtA3j2wISNLETCKVUIaJY8JfdUBCFrib3VwIwjxwn7yjLe6zxODjzLFyzM5VetxJta1ELtd1D0ywwwenIdwPLU/640?wx_fmt=png&from=appmsg)
蓝色的标题栏、经典的开始菜单，一打开就有一种熟悉的感觉。

它当然没什么生产力提升。

但是它说明了一个问题：

**Agent 的界面开始变成可以被社区自由改造的东西。**

今天是XP，之后可能会是赛博朋克、Linux 风格，或者完全不一样的工作流程。

这才是插件生态起来以后真正有意思的地方。

## 这么有趣，想必大家都已经迫不及待想要试一试了

前提是先把 DSH 的 Web 环境跑起来。

直接执行下面的命令。

```
git clone https://github.com/zhu1090093659/dsh-web-ui.gitcd dsh-web-uipnpm install && pnpm -r builddsh plugin --profile web add link:$(pwd)/packages/dsh-web-ui-alldsh web
```

重启以后，新的插件入口就会出现。

只想要皮肤的话可以单独安装相应的插件。

## 不过，它现在还不是装完就用

这里也得说一下边界。

首先，你得先会用 DSH。

Node.js、命令行、插件安装等门槛还在，所以它更适合已经在折腾 DSH 的开发者。

其次，它高度依赖 DSH 本身。

官方更新之后，插件也要跟着进行相应的适配。

移动端远程也要注意安全问题，特别是自己开通公网访问的时候，Agent 的文件和命令权限不能随便开放。

## 写在最后

我觉得 dsh-web-ui 最有意思的地方，不是它功能多。

而是 **DSH 开始出现真正的社区生态了。**

有人做看板，有人做远程，有人做皮肤，还有人养电子宠物。

Agent 不再只是一台“会干活的聊天窗口”，它变成了一个可以自己搭建、自己修改的工作平台。

有兴趣的可以试试看。

开源地址：https://github.com/zhu1090093659/dsh-web-ui

平时我会持续地分享一些有趣的开源项目，有兴趣的朋友可以关注一下。

可以回复关键词聊天，找你想要的项目。

![](https://mmbiz.qpic.cn/mmbiz_png/VDCUoW3UiblJgOFbc7WYLfRP4fEDxiaHmoyBB1QdcJJXfCH5easy5oCZq0opvkDv6sySz3g1gOSCHRZH3KmHmEz6VztCHQ4jofb6FTqaybPdA/640?wx_fmt=png&from=appmsg)
