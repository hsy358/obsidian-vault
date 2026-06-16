---
title: "Skill写得好好的，换模型就翻车？缺的不是能力是Harness"
author: "小爽爽学智能体鸭"
publish_date: "2026-05-06 07:56:14"
saved_date: "2026-05-10"
source: "wechat"
url: "https://mp.weixin.qq.com/s/CnvED2wgoWREcJBG8QD-aQ"
type: wechat-article
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
  source_url: https://mp.weixin.qq.com/s/CnvED2wgoWREcJBG8QD-aQ
---
# Skill写得好好的，换模型就翻车？缺的不是能力是Harness
![](https://mmbiz.qpic.cn/mmbiz_jpg/Ik6q9molrolpNsrLbicMVibNq3cZVtJgVm5v6beyEBH3geeWoBjcrRWictFj3UJ4Ric1lzTnKhLxOaaO4yISa5uzpRT27RmxPcEOWhL1TJYYTMY/640?wx_fmt=jpeg)

你有没有遇到过这样的情况？

Skill明明用得好好的，可一旦切换不同模型，或者任务稍微复杂一点，同样的Skill突然就翻车了。

反复几次，你可能开始怀疑：

是不是Skill写得不够好？是不是得用最强模型才行？

![](https://mmbiz.qpic.cn/sz_mmbiz_png/Ik6q9molrol01QngAYQz7GrhFy3HXCkcNyg5PZ6bVUmcP1jibQXmIVJ6iaqgqIgt0nbF4o4y8o6tv9ib7L0DTBfxQtwKuibYu46uXXMyTB1S6IY/640?wx_fmt=png&from=appmsg)

模型能力是影响效果的一个关键因素，但有些时候，**问题不出在Skill本身，也不出在模型，而是这个Skill缺了一套"规矩"**。

它知道要做什么，但不知道边界在哪、怎么算做完、搞砸了怎么改。

一个月前，我在散步，脑里浮现skill和harness。一个harness of skills的想法在我脑中生长开来。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/Ik6q9molrol5d6t1Pib9dBicibT2iccWiayaEXZfNLph7ukKQrFlELcxNAC1XodEro2tLnbgux42sZNaepBoMmckUtQg9Rd3a5dCwVCNdIVB5Wzo/640?wx_fmt=jpeg)

于是就有了这篇文章主题的出现：

Skills中的Harness思维。（文末有提示词）

![](https://mmbiz.qpic.cn/mmbiz_jpg/Ik6q9molromjmIaibG7VbmvEZFtGuUN7DPqVZy9Is6iaeT6KrQQ3UPCqrpRQKC8NCNUr8gn6qCNbARzzPnF5RsKbVReFTc9AmFWzZZSFUVfjE/640?from=appmsg&wx_fmt=jpeg)

## 01 设计Skills得有Harness思维

Skill是为了复用才被造出来的。

但问题来了：

为什么同一个"审查代码"的Skill，丢给不同的模型，结果可能就是一个天上一个地下呢？

因为**模型也有强弱**，就像同个事情你交给能力强的A，还有能力差一点的B，结果可能会有所不同。

·**强模型**

就像经验丰富的大厨，你说"做顿好的"，它看看冰箱里的食材就能给你整出一桌宴席。

 ·**弱模型**

则像个刚入门的学徒，你说"做顿好的"，他可能就给你煮了碗泡面，还忘了放调料包。

![](https://mmbiz.qpic.cn/mmbiz_png/Ik6q9molromBgVjcroSlEdXQPenLrKfbQwXHdwFNUlq709UYHoH5swVUib2CzPsLOeicH0N1HmjJdjzma7buA2EGkbEHjqtQO6t22HcBZhcMA/640?wx_fmt=png&from=appmsg)

你看，Skill好坏是一回事，但有没有给它画好"跑道"，才是决定它会不会跑偏的关键。

没有Harness思维的Skill，就像一张写满"盐少许、糖适量"的模糊菜谱。全程靠厨师手感，换个水平差点的厨师，做的菜就没法吃。

所以得把菜谱改成这样："盐3克，糖5克，180度烤20分钟。出炉用牙签戳一下，拔出无残留，才算熟。"

**这就是Harness思维。**

就像同一个事情，你只要写好SOP以及边界规范，能力强的A和能力弱的B，做得结果差距也就不会特别大。

**Harness思维要解决的核心问题就一个：**

**把AI天马行空的发挥空间，收窄到一个可控的范围里，让你的Skill不管在哪个模型上跑，都能交出一样稳的结果**。（不一定要最好，但是要稳。）

![](https://mmbiz.qpic.cn/mmbiz_jpg/Ik6q9molrokRCMDZsxFG6XnOicDCQbesicviboCuYgiaCUv0QJPnwX46gsvxpsMfFRVEhop1k5CnP6icUrQpcth9hh1y3kWvicic0aoAonLm9g5Mh0/640?from=appmsg&wx_fmt=jpeg)

## 02 Harness思维到底是个啥？

**一句话讲清楚：**

**提示词是告诉AI"做什么"，而Harness是给它划死"在哪做、怎么做、怎么算完、搞砸了怎么改"。**

我们可以把它想象成一个"工程夹具"。

它把那些飘忽不定的"灵机一动"，变成了一步一个脚印的"在轨运行"。

这整套"夹具"，由五层结构组成：

· **任务层**

放在Skill的功能描述和指令里。

就解决一个问题"什么情况下要启动？具体干什么？红线在哪不能碰？"

· **上下文层**

就是核心指令和参考文档。

告诉它"干活时该参考哪些资料，哪些细节等用到时再去翻"，别一上来就被信息淹没了。

· **工具层**

那些可执行的脚本。

把"每次都一样的重复操作"给固化下来，别让它每次临时发挥写代码，又慢又不稳。

 ·**验证层**

嵌在指令里的检查清单。

负责"干完活怎么检查、怎么才算合格"。

· **记忆层**

一个结构化的复盘模板。"这次踩了什么坑？怎么记下来，下次自动避开？"

这五层凑齐了，Harness就不再是虚的概念，而是你Skill里能实实在在抓住的东西。

![](https://mmbiz.qpic.cn/mmbiz_jpg/Ik6q9molroke0iamiaPv0NCXGSqRBqzVzanANFmmicPRWTiaRgpYXtq8ahYDbUCbVTPGuIWwGCh0oEFiaPqfktecZxSf3WzADibKgPzY2gloQOCicM/640?from=appmsg&wx_fmt=jpeg)

## 03 把Harness思维融进Skill里

**核心玩法就一个闭环"规矩-干活-检查-长记性"，再加上七条原则和具体怎么写的方法。**

### 先搭好那套核心的闭环

这套闭环得跑通这五步：

"干活前先看规矩→一小步一小步改→跑验证→没通过就对着报错修那一点→重试直到成功→最后沉淀经验"。

· **第一步：干活前看规矩**

AI上手第一件事不是改代码，是读规矩。它得自己搞清楚这任务是它该干的吗？边界在哪？以前有没有类似的坑可以避开？

· **第二步：小步修改**

一次就改一个明确的问题，别动辄大动十几处。步子迈大了容易扯着。

· **第三步：验证**

严格按照你Skill里定好的步骤，一项项检查。

· **第四步：失败不重写**

**这是最关键的心态。验证挂了，别吼它"重新写！"** 让它只看报错信息，只修报错的那一行，最多重试3次。

·**第五步：沉淀经验**

任务做完了，不管是成是败，都得按一个固定模板把经验记下来。下次再干活，这就是现成的"错题本"。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/Ik6q9molronPV8xGBb6dLT0oLd2FoLLJhDld9ticARBM1m2lnpZCm6ljP9AVK4Ano27FfxHwpKqWtialiaFuoHy9GWCmvASocpEib8iaVzgGcCmQ/640?from=appmsg&wx_fmt=jpeg)

### 记住这七条原则

**原则一：验证层只写目标，别写死命令。**

不要在你的Skill里写死"现在运行npm run"，因为这换个项目可能就跑不通了。你的Skill只用说"代码必须符合风格规范"，至于用什么命令去查，那是这个项目自己的事。

**原则二：功能描述是触发信号。**

别光顾着说明自己，要带上"触发关键词"和"使用场景"。它就是AI在众多Skill里找到你的那个"搜索引擎关键词"。

**原则三：确定性的操作就写成脚本。**

像数据格式检查这种每次一样的活，直接写成脚本。AI调用就行，既省`Token`又稳当。

**原则四：学会渐进式披露。**

核心的、常用的指令写简洁些。具体的、复杂的细节扔到参考文档里随用随取。别把所有东西都堆在脸上。

**原则五：记忆层必须结构化。**

最没用的记录就是"有个错误，下次注意"。你得记下来"哪个文件、改了什么、报了什么错、最后怎么修好的"。这样的经验才能真的帮到下次。

**原则六：模块化设计。**

一个Skill就干好一件事。代码审查的、测试生成的、部署的，都分开。用的时候再组合，比搞一个"万能工具箱"强多了。

**原则七：安全审查是内置项。**

特别是能分享的Skill，得留个心眼检查下脚本里有没有往外面发数据、注释里是不是藏了啥不该有的指令。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/Ik6q9molromRmYS7hh2DybZ0Z4icUoRbdJ8duIJ8Tsbyhak88NPrAIwJEXACF18qk4tmJYibRSyWlIDR9L77jhwicHYficWhsL4GqXfoygiaMcIk/640?wx_fmt=png&from=appmsg)

## 04 手把手写好那几块核心指令

动手写Skill，核心就是写好下面这四块东西。

### ① 功能描述：用一句话，让AI明白啥时该用它

· 公式：做什么+触发词+使用场景。

· 反例：`功能:处理文件`（太短了，AI完全不知道什么时候该叫你）

· 正例：`功能描述:从PDF里提取文本和表格。当用户提到PDF、表单或文档提取时用你。`（这就非常清晰了）

### ② 执行指令：一步步告诉它，上手先干嘛、后干嘛

· 公式：步骤编号+一个动作+做完了怎么检查。

· 要点：每一步就说一个动作，别塞太多；而且每一步都得说清楚"干成了怎样，干不成又怎样"。

举个例子，体会一下"强模型版"和"弱模型版"的差别：

如果你用的是强模型，第二步的风控检查可以写成："检查代码是否存在SQL注入风险。"

但如果你手上是个弱模型，就得拆细了写："检查代码里有没有用字符串拼接的方式拼SQL查询。如果有，标注出来，建议改用参数化查询。"

### ③ 验证规则：教会AI自己检查自己

· 公式：检查什么+通过标准+没通过咋办+最多试几次。

· 要点：每步后面都要有"通过了就下一步/没通过就只修报错点"的明确分叉路；更要记得设置重试上限，防止它在原地死循环。

![](https://mmbiz.qpic.cn/mmbiz_png/Ik6q9molromTPnE390KibTke1KzkxicQQkqnvZcqZoWUvGt1JibrO2VczfRv9WThD1IHiamobTpcthiccMhDDvuknrugJAicXQnpYyw8Pib7Zh5BO8/640?wx_fmt=png&from=appmsg)

**弱模型注意**：

如果你的模型容易在失败后"慌张乱改"，在这一步里额外加一句："验证失败时，一次只能改一处，改完立刻重新验证。"

好，先歇口气。

前面这三块，功能描述、执行指令、验证规则，基本构成了你这个Skill的"运行时骨架"。它们管的是"干活前、干活中、干活后怎么检查"。

但还有一个更关键的东西没讲：怎么让它越干越聪明？

这就是第四块——沉淀模板。

### ④ 沉淀模板：教会它总结经验，越用越聪明

· 公式：任务小结+踩坑记录+新学到的经验+可复用的代码/命令。

· 要点：每次任务收工，AI都得按这个格式交一份报告。下次开工，先去读读上次的"错题本"。

这四块东西串起来，就是一个有机的整体：

·**功能描述**

是AI的"开关"，让它判断接不接这活。

·**执行指令**

是AI的"说明书"，告诉它活怎么干。

·**验证规则**

是AI的"质检员"，让它自己把关。

·**沉淀模板**

是AI的"错题本"，让教训不再重演。

![](https://mmbiz.qpic.cn/mmbiz_jpg/Ik6q9molrokiaAp186guUR1AILqTusRspcftB9r1KQna13q2qSe6DRib2Rlo6Tzd7f0NSEUxSTltqiakVrYSHohk6M2fVgWuNYhWlWjJkiaiaSRA/640?from=appmsg&wx_fmt=jpeg)

### 一键优化：让"改造过程"本身也自动化

好了，如果你觉得"道理我都懂了，但真要动手改还是有点烦"，没关系。我给你准备了一份现成的提示词。（见文末）

如果你想了解更多细节，或者手上模型比较特殊需要微调，下面这段话可能对你有用。

### 模型换了，策略也得跟着"微调"

换模型就像带不同性格的实习生，规矩的骨架不用变，但说话的松紧程度要调一调。

·对"悟性高"的强模型：你可以给它更多自主空间，指令不用写得太死，它会自动考虑周全。

·对"一根筋"的弱模型：指令就得像拆乐高一样，越细越好。

不管是强是弱，有验证层兜底就不怕。

· **强模型**：测试挂了，它能自己看懂日志，精准定位去修。

 ·**弱模型**：测试一挂就容易慌，开始瞎改没报错的地方。所以你得给它加一条死命令："一次只能改一处，改完马上跑测试"。

![](https://mmbiz.qpic.cn/mmbiz_png/Ik6q9molrokth6xhFARCLCDYicXnWxTKJpsK49xljceXv2DoO2dBgnzljMPiclrY0ZFbAciclJibOcUvQdolEj6baIibmkmkXOyicwMnGIkPiaUPYo/640?wx_fmt=png&from=appmsg)

还有沉淀记忆的时候：

· **强模型**：能自己复盘出高质量的经验教训。

· **弱模型**：可能就扔给你一句"刚才有个报错，注意一下"。对弱模型，你最好强制它按照复盘模板，一项项填空，填不满不让过。

**最后的心法：记住，管你模型换得多勤快，只要你Skill里有实打实的"自动检查"在压阵，它就翻不了天。**

## 05 举个简单例子：代码审查Skill

光说不练假把式，来看下"代码审查"这个Skill，是怎么在Harness这套东西下跑起来的。

它的Skill指令长这样：

-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-

```
name: 代码审查description:   审查代码里的安全漏洞、性能问题和风格问题。  当用户要求审查代码、检查错误或安全审计时用你。  支持 Python、JavaScript、TypeScript。## 执行步骤### 第一步：安全扫描（最高优先级）跑这个：python 脚本/安全扫描.py {要查的文件}主要查：SQL注入、跨站脚本攻击、有没有密码硬编码。更细的清单看这里：参考资料/安全检查清单.md### 第二步：风格检查确认改的代码符不符合项目的风格规范。具体怎么查，听项目自己的配置文件。### 第三步：复杂度分析跑一下：python 脚本/复杂度分析.py {要查的文件}单个函数复杂度超过 10 就标出来提醒。## 边界- 只读不写，不许动业务逻辑。- 只查这次改的那些文件，别到处瞎翻。## 验证规则1. 跑一下安全扫描   - 通过了 → 下一步   - 没过 → 只修扫描出问题的的那一行，再扫一次（最多试 3 次）2. 确认风格检查通过   - 通过了 → 下一步   - 没过 → 改完重查3. 确认所有测试都通过   - 通过了 → 搞定，交活   - 没过 → 查原因，只改跟这个错误相关的代码，然后回到第 1 步## 限制整个检查流程最多跑 3 圈。超了就别自己瞎弄了，停下来告诉我哪没过。## 输出格式最后，用 模板/审查报告.md 生成一份审查报告。
```

### 跑一遍给你看

用户："帮我审查下这段代码"（上传了一个`login.py`）

· **干活前先看规矩**：

它先读功能描述，知道要用"代码审查"这个Skill。然后看执行指令，确认了流程是：安全扫一遍→风格查一遍→复杂度看一遍。接着翻记忆层，发现一条老笔记："上次鼓捣login模块时，容易出SQL注入的坑"。

· **小步修改与验证**：

它跑了安全扫描脚本→叮！发现一处SQL注入风险。

跑了风格检查→发现5处缩进不对。

跑了复杂度分析→有一个函数复杂度飙到15了，超标。

· **交付**：AI把这三项问题怎么修，都整理到报告里，交了出来。

· **沉淀经验**：忙活完了，它自己得记下两笔：

第一条记错题本："login模块又发现硬编码密钥了，下回审查这个模块，这条得优先查。"

第二条更新规则："复杂度检查的默认指标，现在改成4个。"

你看，这么一套跑下来，**一次经验都没浪费**。

![](https://mmbiz.qpic.cn/mmbiz_jpg/Ik6q9molronS9XTtPuFlA7b0qeXhAOdVUkumlFNRibYtylaKIZkbg7dNYZgYSWAkdK1AVmiaHPZdcBbnPjWz3DCE7zte9fWNyXyiaQUYDCY4kQ/640?from=appmsg&wx_fmt=jpeg)

## 06 最后的话

**Harness思维，从头到尾其实只做了一件事：让你的Skill不管摊上哪个模型，都能稳如老狗，给出一致的结果。**

虽然不是最优的结果，但是是最稳的结果。

对于简单任务，稳就够了；对于复杂任务，稳是必要但不充分条件。

毕竟强模型和弱模型之间，本身就存在能力的差距。就像人一样，有些复杂任务，还是得能力强的人来做。

· **它的稳定**

来自于验证层那个死磕到底的循环：不改完、不通过，绝不交付。

· 它的可复用

来自于任务层清晰的边界，和验证层"只定目标，不定命令"的策略。换个项目，换个模型，照样能跑。

 · **它还能持续进化**

靠的就是记忆层那一套沉淀机制。每跑一次，你手上的Skill就越"聪明"一分。

**提示词，决定了AI怎么开始；而Harness，才真正决定了AI能不能把事儿办成。**

把Skill加上Harness，你的AI编程体验，就是从"抽卡碰运气"，彻底变成了"流水线稳赢"。

![](https://mmbiz.qpic.cn/mmbiz_jpg/Ik6q9molrolKficMjib4uwTpCiaQluwicQoZoHiacYYNEJBqjBiaom7eXX6ql1aDg578zPQenpBkeNxLczic83mxvwhVFSF7TYZnr7KRKOHckncnoI/640?from=appmsg&wx_fmt=jpeg)

## 附录：提示词

只需要把它发给你常用的AI Agent，然后把你的Skill内容贴在最后，它就会自动帮你把整个Skill改造成Harness模式。

**你的角色**
你是一位 AI 工程化专家，擅长把普通的 Skill 改造成稳定、可复用的 Harness 模式。

**你的任务**
按照下面的 Harness 框架，帮我优化我提供的 Skill 文件。

**改造框架（四个层次）**

**1. 任务层 — 优化功能描述和执行指令**

- **功能描述**：必须包含“核心功能 + 触发关键词 + 使用场景”。格式如：“做什么。当用户提到[关键词]或[场景]时使用。”
- **执行指令**：每一步只做一个动作，编号分步。每一步都要说清楚“做什么”和“怎么检查它做对了”。同时明确指出“只改什么、不改什么”的边界。
**2. 验证层 — 加入自检规则**

- 为每一步都设置“通过 → 下一步 / 失败 → 只修报错点并重试”的分支路径。
- 限制最多重试 3 次。失败时，强调“只修报错点，别推倒重来”。
**3. 记忆层 — 加入复盘模板**

- 每次任务结束，都要求按下面的格式记录：
- 任务摘要（做了什么、结果如何）
- 失败记录（尝试了什么、为什么失败、最终怎么解决的）
- 新增经验（因为这事，新立了什么规矩？为什么？）
- 可复用配置（把这次验证过的代码或命令存下来）
**4. 工具与安全**

- 看到能写成脚本的重复操作，优先提供脚本。
- 脚本需要返回明确的成功/失败标志。
- 顺便检查并移除所有网络请求、系统调用等危险操作，以及注释里藏着的可疑指令。
**输出格式**
直接给我优化后的完整 Skill 文件内容，别漏掉任何部分。

**现在，请优化下面的 Skill**
[把你的 Skill 内容粘贴在这里]

发过去，等几分钟，你就能拿到一个改造好的Skill。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/Ik6q9molronF3pcbPVicT27ibfxmRHeb5zkukyPgR250FH4cMLjRz9kJ5QhVF9AEgo42QgKkhXGsYv5MOricw8SkZYBkbsC5MdmxKs94THgmEY/640?wx_fmt=png&from=appmsg)

碎碎念，我最开始使用skill，用的coze，因为我想解决一个问题，就是我日常只有手机，如何快速输出思考，并且发布呢?而扣子就有APP端去调用skill的能力，而且自带生图。

于是，作为一个小白，我开启了一段 vide skill之旅。

也就有了标题skill，排版skill，插图skill，图标图skill...的出现。

在使用过程中，我发现扣子调用skill之后，输出不太稳定，于是我在skill设计过程中强制加入了交互流程。

也就是通过skill调用的过程中，它需要一一跟我确认，我完全确认之后，才输出。

后来，coze变成了agent claw模式，出现了一个非常大的问题，就是它有自主模式(风格和记忆)，它现在开始自主去跳过我的步骤，以它的想法直接返回结果。很多时候，返回的结果不符合我的预期。

于是我就得出一个结论，就是skill有一个作用是给模型直觉加上思维链路，也就是工程思维。([历史文章](https://mp.weixin.qq.com/s?__biz=MzIxODc1MTM2Nw==&mid=2247491224&idx=1&sn=6a5fd7ab51f364cdb71c15d72b428c22&scene=21#wechat_redirect))

随着坑不断踩，我发现龙虾并不"稳定"，因为多了soul个人风格注入。同时我又发现模型可能有情绪向量。各种因素，我觉得目前coze并不好用。([情绪向量](https://mp.weixin.qq.com/s?__biz=MzIxODc1MTM2Nw==&mid=2247491407&idx=1&sn=fed0d0ea6b461d385417c3a6b2c99356&scene=21#wechat_redirect))

最近几天，开始尝试本地，开始用gpt5.5，加上平时看到理论，就会进行思考，逼自己发出一篇文章。慢慢开始有自己的思考，就是harness工程思维。

以前vide出来的skill，还需要再重构，不过不是现在。

回顾过往，浪费了很多时间。

从一个小白，开始瞎搞，然后开始发布相关文章。踩了不少坑。虽然能力不强，有些过程也没必要踩，但也是一种成长的过程。
