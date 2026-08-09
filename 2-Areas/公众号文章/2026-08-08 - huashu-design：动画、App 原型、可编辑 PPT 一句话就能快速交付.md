---
title: "huashu-design：动画、App 原型、可编辑 PPT 一句话就能快速交付"
author: "青鱼学AI"
publish_date: "2026-08-08 09:05:09"
saved_date: "2026-08-09"
source: "wechat"
url: "https://mp.weixin.qq.com/s/2VfcvK96wf9UXPJfI1EtFw"
---
# huashu-design：动画、App 原型、可编辑 PPT 一句话就能快速交付
*——聊聊花叔的开源项目 huashu-design（花叔设计）*

---

前几天我在GitHub上刷到一个项目，叫huashu-design。点开README，里面全是demo：一段25秒的产品动画、一个能点的iPhone原型、一套演讲PPT。

我一开始以为是作者找设计团队做的展示物料。往下翻才知道：这些东西，全是这个工具自己跑出来的。不是Figma，不是AE，就是一句话prompt。

挺震撼的。

多翻了一会儿，我大概明白它在干什么：你给它一句话，几分钟到半小时，它还你一份能直接交付的设计。而且做出来的东西质量稳定，每次都靠谱，不是那种一眼就能看出是AI糊弄的水平。

![](https://mmbiz.qpic.cn/mmbiz_gif/5o3ZMFY5XrgWvMEonacTF7tbKeB546cEddrs8CV1S4JoJGEr23nJ3YsQ78HmmYPASic1yMtLR0N9soHkBuZibMTE7BXuTJaLQBUaiaftJQyeIs/640?wx_fmt=gif&from=appmsg)

*25 秒：打字 → 选方向 → 画廊展开 → 聚焦 → 品牌显形。这整段动画是 skill 自己跑出来的。*

---

## 一、它是什么

先说清楚一件事：它不是一个App，应用商店里搜不到。它是一个skill（技能包）。

skill就是给AI编程助手装的能力插件。你把它装进Claude Code、Cursor、Codex这些工具，助手就多了个本事——会做设计。装完没有按钮、没有面板，你在对话框里用大白话说一句话就行。

作者是花叔（花生），在AI开发者圈子里挺活跃：做过AppStore付费榜第一的「小猫补光灯」，写过《一本书玩转 DeepSeek》，开源的「女娲 .skill」在GitHub有一万两千多颗star。

---

## 二、它能做什么

挨个说。

### 产品发布动画

就是那种带节奏、有运镜、能配BGM的宣传短片。以前要么自己上After Effects熬，要么外包。你把脚本喂给它，说「做成60秒动画，导出 MP4 和 GIF」。**8到12分钟，拿到一个MP4（能插帧到 60 帧）、一个 GIF，还能自动配上背景音乐。外包两周的活，一杯咖啡的工夫。**

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/5o3ZMFY5Xrjn3KxHG3wPoIu2SDYOE6AecficcdEFRsZO8iantiaOPIwibybSkfLyKzcsbh1VNYeYoXUiaGz53Dqdfn7jIfvMFPK27tqBia8jCsLos/640?wx_fmt=gif&from=appmsg)

### 能点的 App 原型

产出是单文件HTML，套着精确的iPhone机身（灵动岛、状态栏都在），屏幕之间是真切换——点登录真的跳主页。它做完还会用Playwright自己把每个按钮点一遍，验证逻辑通不通，等于自己测过再交给你。**10到15分钟。**

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/5o3ZMFY5XrhM5VC9aWMcWiaiaTz0iaGZOEkuEjPuiamWLTrB7Ivej2hGtdlhv9gqm1Jp3g4pos0ojgtwv8ddP7HJ6aBY6yXZmzToPX1iaib8rSLpY/640?wx_fmt=gif&from=appmsg)

### 演讲 PPT

这个值得多说两句。大多数AI工具做PPT，给的是图片，没法改字。它做的是两层：一层HTML能在浏览器里演讲，一层导出的PPTX是真文本框，在PowerPoint里双击就能改字、换内容。背后有个脚本读HTML里每个元素的样式，逐个翻译成PowerPoint对象。**15到25分钟。**

![](https://mmbiz.qpic.cn/mmbiz_gif/5o3ZMFY5Xriaia6v0zhEPucuu6k4SZdaWIG4vibjJgL9LLNM7ugsic6AX8A1ofktc5I51kAmA6Dpgb0YdHbnN06p09jlXwibsV52EUpNzbt5ibTEk/640?wx_fmt=gif&from=appmsg)

### 设计方向顾问

前面三个，前提是你知道自己想要什么。但很多时候需求是模糊的，比如「做个介绍鹦鹉进化史的网站」，你自己也说不清要什么风格。

这时候它不会让你在文字里盲选——「要极简还是科技风」这种问题选了也白选，因为脑子里没画面。它会用三套不同的逻辑各做一版真实视觉摆出来：一套拿系统时间的秒数随机选风格（专门治AI总偷懒选极简的毛病），一套参考真实的获奖网站，一套按顶级设计师工作室的思路来。你看着三个页面，指着说「要这个感觉」，它再细化。比在文字里描述风格快得多。

![](https://mmbiz.qpic.cn/mmbiz_gif/5o3ZMFY5XrjVAsTBESKKUTtQWI0ybOQ8icicxUyKu5nJrAHuIOPX1pCJHcBb8lgKfRYibmJzibzz3A7JK8pG920zO4HlJmoKXYVtpS23x3yoDus/640?wx_fmt=gif&from=appmsg)

### 还有几个

- • 设计变体：同一个设计同时出几个版本并排对比，配色、字型实时调。
- • 信息图：杂志级排版，能导PDF、PNG、SVG。
- • 评审：拿一个现成设计给它，它从五个维度打分，给一份「保留什么、改什么」的清单。

---

## 三、为什么它能去除 AI 味

看到这你可能会想：AI做的设计，不都一个样吗？

脑子里大概有画面：紫蓝渐变、emoji当图标、圆角卡片加上左侧彩条。看着现代，看多了就一个感觉——廉价，一眼AI。花叔管这种叫AI slop（泔水），整个项目有一半功夫花在「怎么不做出这种东西」上。

怎么做到的？我印象最深的是它处理品牌色的方式。

这是个AI做设计的常见毛病：你让它「画一个 Stripe 风格的页面」，它会凭记忆给你调个紫色，但那个紫色大概率不是Stripe真正在用的那个紫。看起来像，其实哪儿都不对。

huashu-design的解法很死板：只要涉及具体品牌，强制走一套流程——先问你有没有品牌规范，没有就去扒官方品牌页，把logo、官网、截图都下载下来，用脚本把里面的颜色值全抠出来，按出现频率排序，滤掉黑白灰，最后写成一个文件固化下来。后面所有设计都引用这套真实色值。

这就像设计师接单，第一件事问你要VI手册，而不是凭印象发挥。

花叔做过A/B测试，加了这套流程的版本，**稳定性方差比早期版本低5倍**。说白了就是做出来的东西每次都靠谱，不会今天好明天崩。——这也是我前面说「质量稳定」的来源，它不是嘴上说说，是有具体机制在保这个稳。

另外它的工作方式也帮着保稳：不闷头憋大招，先给占位、给草稿，让你尽早看到，方向错了早改。尽早纠偏，最后交付的东西才不容易跑偏。

![](https://mmbiz.qpic.cn/mmbiz_gif/5o3ZMFY5Xriap6Z9NEDs7NAvvggAJgbrzAXtials5togX5ZicBw5AGUk2GRYkpe6Eo6F5OuXnY7Y6TmNZfWlFkUH5cicL6VOHpic8uRyZ7Ruic2wA/640?wx_fmt=gif&from=appmsg)

*上面这套流程拆成五步就是：*

![](https://mmbiz.qpic.cn/sz_mmbiz_png/5o3ZMFY5Xrh1mtGRLl4oOQR8Wy3uWAxSSwiaqQrV3gC6fNm81pULg1DdHPmIYV8cPmHiapIQGaa4j9Zd7yiaTiarP1EUtwdh0VQ7ol7KcEJWzgk/640?wx_fmt=png&from=appmsg)

---

## 四、和官方的 Claude Design 什么关系

如果你关注AI圈，可能知道Anthropic出了个官方产品叫Claude Design，浏览器里用的AI设计工具。这两个什么关系？

作者自己说过：Claude Design发布那天他玩到凌晨四点，但几天后发现自己再没点开过。不是它不好，是他更习惯让AI在终端里干活，不爱打开图形界面。于是他让AI拆解了Claude Design的机制（包括社区流传的提示词），做成了这个skill。

简单说，Claude Design是一个图形工具，huashu-design想让「图形工具」这层消失——一个在浏览器里点点拖拖，一个在对话框里说话。

![](https://mmbiz.qpic.cn/mmbiz_png/5o3ZMFY5XrgODWeIs4OyX0v6VoSDaG2oWpqswt6f4Bqb87ncEDibajcfzLMk3VJyibEsRdaOTBhHIYpCcRJYRhia41WhBeokSlxUT2GhAoO2lQ/640?wx_fmt=png&from=appmsg)

---

## 五、适合谁

适合的人：

- • 独立开发者，习惯在终端干活、不爱切到图形界面。
- • 创业者、indie hacker，要快速出原型、动画、PPT，又请不起设计团队。
- • 不会设计的工程师、产品经理。
- • AI 自媒体、内容创作者。
解决的痛点，看你中过几个：

- 1. 设计工具门槛高，Figma、AE学起来陡。
- 2. AI 出的东西一眼假。
- 3. 品牌颜色老出错。
- 4. 需求模糊，不知往哪做。
- 5. 格式转换麻烦，HTML变PPT、变带音乐的MP4自己搞很折腾。
- 6. Claude Design卡配额、只在浏览器里。
也得说边界。作者自己讲：这是一个80分的skill，不是100分的产品。它替代不了Figma的精细能力，做不了3D、物理模拟、粒子系统，完全空白品牌从零设计会掉到60–65分，也不能导出图层级PPTX拖进 Keynote改字。

但对不愿意打开图形界面的人来说，80分的skill比100分的产品好用。

---

## 六、如何安装

安装一行命令：

```
npx skills add alchaincyf/huashu-design
```

**有个坑**：装完检查一下安装目录（一般是 `~/.claude/skills/huashu-design/`），看 `references/`、`assets/`、`scripts/`、`demos/` 这几个子目录在不在。旧版 CLI 有个 bug 只同步单个文件，缺了就用不了。升级到新版（`npm i -g skills@latest`）或者 `git clone` 都行。

**安全这块**，核心的渲染、导出（MP4 / PDF / PPTX）100%在本地跑，不联网、不需要APIkey。需要联网的功能（配音、AI评审）隔在 `scripts/cloud/` 目录里，完全可选，用你自己的key，无telemetry，没有数据发往作者服务器。细节都写在SECURITY.md里。

价格：**2026 年 5 月 14 日起改成了MIT协议，个人和商用都免费。**公司内部用、做商单、做成自己的付费产品都行，不用打招呼。

---

## 七、我的感受

写到最后说说我自己的感受，就两点。

一是快。以前做个宣传动画、画个原型、排个PPT，要在好几个软件里切来切去，花大半天。现在一句话，十几分钟到半小时，东西就躺在文件夹里了。

二是稳。这是我最意外的——它做出来的东西质量不掉线，每次都靠谱。背后那套「先把品牌色抠准、再尽早给你看草稿」的死板流程，就是为了保这个稳。快的东西很多，又快又稳的不多。

如果你是被「设计」这件事卡过的人，建议装来试试。

GitHub：**github.com/alchaincyf/huashu-design**

> 💬 **互动**：你最想先用它做什么？动画、原型，还是 PPT？留言聊聊。
