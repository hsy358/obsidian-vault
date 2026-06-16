---
title: "Obsidian+opencode+draw.io：让架构图绘制融入笔记工作流！"
author: "和小丁一起成长"
publish_date: "2026-03-24 07:15:57"
saved_date: "2026-05-10"
source: "wechat"
url: "https://mp.weixin.qq.com/s/8q187UgOVOqRz2m9WKwcpg"
type: wechat-article
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
  source_url: https://mp.weixin.qq.com/s/8q187UgOVOqRz2m9WKwcpg
---
# Obsidian+opencode+draw.io：让架构图绘制融入笔记工作流！
# 一、写在前面

之前写了两篇在vscode和opencode中使用draw.io的文章：
《vscode+opencode+draw.io用自然语言就能轻松画架构图》
《opencode+draw.io+skill让你更专注于画图逻辑》

但是我发现一个问题：Obsidian逐渐成了我的主要工作平台，是否能在Obsidian中使用draw.io呢？

我大致研究了下，还果真行，这篇文章记录下**如何用Obsidian+opencode+draw.io画架构图**。

# 二、准备工作

## 1、安装Diagrams插件

在社区插件市场搜索draw.io，发现有两个可选的插件：

![](https://mmbiz.qpic.cn/mmbiz_png/kJgMlSXdCicf7utua91OUx8lvob5YO4WyDcldhcpXHxGZicQ4NzzM7cqJFoZgjIaX6icEJfB4FUibX3BvAo7336AbrPg62JBEiciayyHMVt7T9E94/640?wx_fmt=png&from=appmsg)

其实我也不知道该选哪个，只是发现左边这个最近有更新，就选择了这个。

安装后启用这个插件即可：

![](https://mmbiz.qpic.cn/mmbiz_png/kJgMlSXdCiccl5PKaiaVl733VHACKwgrv9w2oPwYuCbBhA85kV5vGfbuZO2J33QDNNK8ObQ0rO3S84jRMzqibiaslaOt94XEtIXCpp5sucsPTnM/640?wx_fmt=png&from=appmsg)

安装好之后，Obsidian的左上角应该有**New diagram**的图标。

![](https://mmbiz.qpic.cn/mmbiz_png/kJgMlSXdCicficZCRHKsPuGUoLzFyGtiaq2nlkaWibHt5Mn4W3Vgh6IzxHDWLrV1OFHBEe7qeLNvXQEVEv3A7EbYFcAU4rL2PRPIiaiajg0lK3jib4/640?wx_fmt=png&from=appmsg)

这样，插件应该就算是安装好了。

## 2、安装opencode

这个就不详细说了，如果还不会安装，请翻前面的文章《走了不少弯路，终于完成了Obsidian与OpenCode对接》。

# 三、画图试用

到此为止，所有的准备工作都做好了，下面举两个例子。

## 例子一：画微服务架构图

在opencode对话框里输入：

```
请画一个微服务架构图
```

下面就是画出来的效果：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/kJgMlSXdCicdo7I670aILu0H5ZI2uaBrvoBnCd5YrGMhenaoob8CGBgmRhiaLicOdiatJfbQiberMqAzRWknAiaVc8TYcibdfDfNumvOMgEU6tJ0RU/640?wx_fmt=png&from=appmsg)

说实话，有点土，这个时候可以用之前的画架构图的skill来美化下。
美化后的效果如下：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/kJgMlSXdCiccPeriaAZKHhofoqulkJSVXYdJTD5hcbiaQGpFcjODfbibb9f5svkYX0Pib9MaytKAB8EQkftgqAICiaCPjicJw5YycWTJyaVfjuCvrg/640?wx_fmt=png&from=appmsg)

## 例子二：画TELOS运作泳道图

上篇《用Obsidian+OpenCode搭建了自动进化笔记系统》中完整复刻了TELOS系统，但是这个系统还是比较复杂，当时我并没有完全搞懂其内部的运作原理。

现在有了draw.io工具，正好可以以画微服务架构图为契机，画出TELOS的运作流程图。
在对话框中输入：

```
现在从你收到“画微服务架构图”的指令开始，请你把TELOS的整个运作流程用draw.io画出来。生成的draw.io图文件放在当前打开的文件的同级目录下。
```

下面这个就是画出来的效果，当然我也做了一点手工微调，主要是把重叠的箭头撑开。

![](https://mmbiz.qpic.cn/mmbiz_png/kJgMlSXdCicdR9sIvWyq2ibzubPWe80C7cdtAU2B0f2a6ZDicdIIJ1Yphrfy5abroZhoGfPqU6b8p1KGDTelz4iaiaGUPagNfaI8uzrUVV4w6iarw/640?wx_fmt=png&from=appmsg)

有了这个图，也就能更容易地理解TELOS系统的运作过程了。

# 四、写在最后

这篇文章记录下**如何用Obsidian+opencode+draw.io画架构图**。感兴趣的同学可以亲自尝试下，有疑问也可以在评论区交流。
