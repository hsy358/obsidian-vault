---
title: "压进我十年设计经验的 PPT Skills，迎来大波更新"
author: "歸藏的AI工具箱"
publish_date: "2026-05-11 08:30:00"
saved_date: "2026-06-21"
source: "wechat"
url: "https://mp.weixin.qq.com/s/MVXHToWtNVT_b68zxr7fSA"
---
# 压进我十年设计经验的 PPT Skills，迎来大波更新
![](https://mmbiz.qpic.cn/sz_mmbiz_png/ofWbZTuv4DXoQApmhVKHh654b6kh1B5gicrMJbWjn9gshSFrG6sxj6KneyOrqz78pH1PBbg6z3Oh7zc0nuFozXttmlbr47ycouWAUicKS05HQ/640?wx_fmt=png&from=appmsg)

上次开源 guizang-ppt-skill（github.com/op7418/guizang-ppt-skill） 之后，大家都非常喜欢，**短短几周 Github Star 来到了 6000 多**。

而且也被非常火的开源 open design 参考放了进去。

我也在线上线下非常多的地方看到了这个 PPT Skill 生成的 PPT。

![](https://mmbiz.qpic.cn/mmbiz_png/ofWbZTuv4DX7qqB9OAzoMKPNZKyQWbNng3rxgeUHckKbF7icYRDaNH77tWltjzNlrzL62P7XO0hqZbHico9KsLVJGC7cicIXJyHoaRD9iclcPeI/640?wx_fmt=png&from=appmsg)

发布之后，后台收到的问题里出现频率最高的是这几条：

能不能多几种风格？

配图能不能也帮我搞定？

做完 ppt 的封面要重新画一遍吗？

我自己一边用一边记，攒了两周。这次一次性把这些洞补上。

## 更新了什么

多了一套全新的视觉风格，配图能力直接接入 Codex，PPT 之外的封面也能顺手做了。

具体三件事：

•新增风格 B 瑞士国际主义。全程无衬线、单一高饱和锚点色、网格至上。

•Codex 接入 GPT-Image 2.0。直接生成符合调性的配图，胶片质感的人像、流程图、UI 截图美化。

•还能多平台封面生成。同一份内容直接拼出小红书、公众号、视频号等多种规格。

![](https://mmbiz.qpic.cn/mmbiz_png/ofWbZTuv4DVAq2gMEcGV0YNP3Bjcq8nBcE1QpquO6tfMTPZN8nWydMOxK5WbzgM10D4F1lGBc56twZ7icyic2f3AWFib8KSSpKicnSiaz5YTnc7U/640?wx_fmt=png&from=appmsg)

### 触发新风格

装好之后对 Claude 或 Codex 说一句："**帮我做一份瑞士风 PPT。**"

如果你之前已经安装的话也可以跟你的 AI 说：`帮我更新一下 guizang-ppt-skill`

它会反过来问你：克莱因蓝、柠檬黄、柠檬绿、安全橙，四套主题里选哪一套？

**克莱因蓝 IKB**，通用、商业发布、AI 产品，默认推荐

**柠檬黄**，年轻、运动、零售、Y2K 复古

**柠檬绿**，生态、可持续、Z 世代品牌

**安全橙**，警示、新闻、活力主题

![](https://mmbiz.qpic.cn/mmbiz_png/ofWbZTuv4DXD0DPxckxlwuu7Tu8V50Fk5cqM1J6hGianT2QQKic0mxArt14Wvpxt8Y8vuNjtmw6hW6OSFQWRxKWsf1KmujhOA4ibJCaF08IHmQ/640?wx_fmt=png&from=appmsg)

跟之前一样，不接受自定义 hex。

这条规则我专门写进了 SKILL.md 的硬约束里，原因之前那篇文章讲过，就不重复了。

### 几个最常用的版式

瑞士风内置了 22 个开箱即用的具名版式，覆盖封面、章节、数据、对比、收尾。

挑六个最有辨识度的说一下：

1Cover 封面。左半 IKB 底色压一行反白巨字，右半留白配 meta 信息。开场第一页几乎必用。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ofWbZTuv4DU4bibaom7LibtKhvRmgqLJ4ZBCWCjjCS30Tor7OibpZCnJu9KLECxuXRtxg5O89IUPL1czKJyRPOMPxGlAIy9GdWicwX7dt5icWEd4/640?wx_fmt=png&from=appmsg)

2Statement 巨字宣言。单句话占 9.6vw，整页只剩它和一行小字注脚。适合章节起手、抛核心论点。

![](https://mmbiz.qpic.cn/mmbiz_png/ofWbZTuv4DWMjIDwCRyZQ7KxCPsbY0fZAc9Q285zK0wk2Dbia5HuoKC2m8OIMqvn4K2XxuwqQxuxh4kS21omYiaS8Qb2SQyWSmqibiadqp1Ndc4/640?wx_fmt=png&from=appmsg)

3KPI Tower 柱阵。四根高度由数据决定的纯色柱子，柱子下面接一行类目。利润率分层、价格档位、转化漏斗这种纵向数字对比一眼就能读懂。

![](https://mmbiz.qpic.cn/mmbiz_png/ofWbZTuv4DU1Z02ZCaL5T5kZ7yOezIlWkLichkKUlCOFUfrxl5Hln4vib4JHInl5XtEJNlHVNFQ2wXBYSJNz3rD9wctF9qqymCa9LeXYW19K4/640?wx_fmt=png&from=appmsg)

4Loop Diagram 闭环图。同心圆环上分布编号步骤，一圈环绕收束。适合讲自学闭环、Agent 自动化循环、产品反馈飞轮这种循环结构。

![](https://mmbiz.qpic.cn/mmbiz_png/ofWbZTuv4DXW77RzWDHmGMvKGmoVlPCV8kARuUKkNicbhQQmxSxxEPMlHFibdsPYocVhbGknibzS61DUkbCib2m7BSf534pibvnL3AhQKeaqhkyU/640?wx_fmt=png&from=appmsg)

5Duo Compare 对照。中线一道发丝，左右各一组文字加数据。旧体系 vs 新方案、传统 vs AI、Before vs After 都用它。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ofWbZTuv4DWlp5WAYaVhfYzpPHGmrswJJaM85rRmkcrIBuQCQ0xkGMOwMgg7AdL2XdUmlMvAEZQxdJSNsbrd6xKmLc6gZdm7lOibiawD357qs/640?wx_fmt=png&from=appmsg)

6Closing Manifesto 收尾。左半 IKB 反白一句宣言，右半三条 takeaway 收束全篇。Deck 最后一页推荐固定用这个，和封面构成色彩闭环。

![](https://mmbiz.qpic.cn/mmbiz_png/ofWbZTuv4DWXazP5ec14A2qbfOcKgav46lkU2GiabqnZQurQI9dOov1fqKqOaVr8fwZNHqnolbwre0yZ9jH4oM68CcZFnDr1rWLjlUnK6tyI/640?wx_fmt=png&from=appmsg)

剩下还有横向时间线、Loop 闭环图、Three Forces 三力对峙、System Diagram 系统层级、Why Now 三论点支撑、Tech Spec 产品规格、Image Hero 案例图加 KPI 等等。

每个都对应一种典型内容形态。

你一开口说"我要做行业排名"或者"我要做产品 benchmark"，AI 自己会从这 22 个里挑最合适的，不用你记名字。

选完主题，剩下的流程跟上一版一样：6 个澄清问题，先出大纲和主题节奏表，对齐之后再写代码。

### 让 GPT-Image 2.0 帮你出图

如果你在 Codex 环境里用，PPT 写完它会主动问你："**要不要给这份 PPT 生成几张配图？**"

如果你需要他会自动帮你按照所选的 PPT 风格和内容生成合适类型配图：

人文纪实照片（胶片质感）、信息图（流程、对比、系统关系）、截图再设计（把你的原图按 PPT 比例重做一遍）、数据大字报、流程图、系统关系图

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ofWbZTuv4DUbKDZ2ibiatnpxCx2GeL16ztdoaakUS4aMSrToDeO0wFWzJRsW41mUgK8P1Knzlv0cxmndQLm6tmfALXCL4IQ7g4TozicEvC7z3c/640?wx_fmt=png&from=appmsg)

#### 生成图会自动适配你当前 deck 的风格和主题色。

具体怎么走：

电子杂志风，信息图就走电子墨水基调，黑白灰为主、少量低饱和强调色、细线条、网格、留白克制

瑞士风，信息图就走 Swiss modernism 基调，Helvetica/Inter 气质的无衬线短标签、12/16 列网格、直角

选了克莱因蓝 IKB，生成的图就用 IKB 蓝做唯一锚点色。选了柠檬黄、柠檬绿、安全橙也一样跟着换

文字语言跟着 deck 走，中文 deck 用中文标签，英文 deck 用英文

生成图不带 PPT 外壳，不会冒出页眉、页脚、页码、署名、装饰边框这些东西

![](https://mmbiz.qpic.cn/mmbiz_png/ofWbZTuv4DWUD5MDLiaIsXTXR3ekOLWUuTFuvO6jEykRvgsyAjaqQjdnJgIgdvh3XibbTiaYV9AV5cNKI5OBiaaiaMCdgWrB3TXoWJqnwuy7FBVo/640?wx_fmt=png&from=appmsg)

这个细节的好处是，整本 deck 的视觉一致性不用你来盯。

你不会遇到 PPT 是 IKB 蓝、配图却跑出一抹绿这种割裂，也不用一边写 PPT 一边给 GPT-Image 调 prompt。

跨工具的视觉漂移，是我自己用 AI 做内容这两年最折腾的隐形成本。

能在 Skill 这一层把它消化掉，用户就少操心一件事。

### 让它帮你做平台封面

PPT 做完，发出去之前永远要解决三种规格：公众号 21:9 头图、小红书 3:4 竖图、视频号横版封面。

直接说：``基于这份 PPT 的核心观点，给我一张 3:4 的小红书封面。``或者：``来一张 21:9 的公众号头图。``AI 会按 Skill 的视觉规则出图（同一套主题色、同一套字体、单焦点法则）。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ofWbZTuv4DVDVHSouicPeWdCSQvChZ2g4eibxic8qib6iaWZHDMNMuxn4t3UvNiabCQYJZI922LN8clVSHZu0dcuicY5y4WGN1miaGjX2bttibFj2sPI/640?wx_fmt=png&from=appmsg)

需要批量也行。小红书的轮播图机制下，让它"批量出 6 张，风格统一、字号一致、版式各异"，一次出齐。

公众号比较特殊，头图是 21:9，但分享卡用的是 1:1 的方图，两张需要视觉连贯。

做法是分两次生成，但用同一套色彩和文案：

第一张 21:9 主头图，主标题压在左侧，右侧留视觉锚点

第二张 1:1 方图，作为分享卡的视觉延伸，主元素和头图呼应

![](https://mmbiz.qpic.cn/mmbiz_png/ofWbZTuv4DX2c9yXsicxV4ZFjbuTdgJGSGOYKFO6ILWroG50CzLicRUibEE4WAPiaRPWjIkLGvFRtR1keIRF6noJHUJZ3p8fdp6smQo8GnHG8sk/640?wx_fmt=png&from=appmsg)

我自己常用的两套版式：纯色底 + 巨字 + 角标日期，或者左半图右半字的对开。

## 几个值得分享的小巧思

### 巧思一：用胶片质感对抗"AI 感"

写一个分享，讲"一个人做了一个产品"，需要一张能传递"独自工作"情绪的图。

以前的办法是去 Unsplash 翻半小时，或者放一张明显是 stock photo 的摆拍。

现在直接说：`"生成一张 16:10 的纪实照片，主题是深夜工作室一个人对着屏幕，自然光、低饱和、轻微胶片颗粒、Fujifilm 质感。"`

出来的图带克制的人文温度，看不太出塑料感。

我把这个判断写进了 `references/image-prompts.md`：

胶片质感是 GPT-Image 2.0 之于 PPT 配图最大的价值。它把"AI 生成"这个标签从图里去掉了。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ofWbZTuv4DUqyJEUBowkBIvSbrdBLK5D1KiaicYCRoQzOX9LSt8KLzHIz8R2jtcq1g7l7WBbVU6vbcmqHx6gXq5tbiagYX4uTvR8RIIe1kXniaU/640?wx_fmt=png&from=appmsg)

### 巧思二：把奇葩比例的截图重做一遍

很多内容创作者手头都有一堆原始截图：产品 UI、后台页面、数据看板，比例各异，留白也不一致。

塞进 PPT 之后整本视觉立刻乱掉。以前的解决办法是 Photoshop 修。

现在你只需要把原图丢给 Codex：

"按照 16:10 比例重做一版，保留所有 UI 元素，加点真实工作场景的环境，画面密度中等。"

它会重新生成一张符合 PPT 规范的图，关键信息一个不落，比例和留白完全统一。

这件事对产品测评类内容尤其有用。所有截图过一遍 GPT-Image 2.0，整本 PPT 立刻像同一个人做的。

![](https://mmbiz.qpic.cn/mmbiz_png/ofWbZTuv4DWvBO1AKcLN5wNavicUJEqQYBd7iboF66znP4SW7E911icQQe6O3ljiaAMds26ZAtqPSPPZwiaZ9LALk26SicD3Q1dAqFeCRdxqDibDfQ/640?wx_fmt=png&from=appmsg)

### 巧思三：用 PPT 模板"包裹"AI 图

这是我自己测出来的一个用法。

GPT-Image 2.0 生成的图单独发出去，AI 检测工具大概率会标"疑似 AI 生成"。

这件事在社交媒体这种平台上会影响推荐权重。

但把这张图放进 PPT 模板，再整体截图，结果就完全不一样了。

这件事的本质是把 AI 生成的素材组装成一个完整作品，添加了人工痕迹。

还是基于你的大纲事实的表达，没有虚构，只是避免被算法误伤。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ofWbZTuv4DUahN2jiaNUpM5Gicia8DPBshOPUcue8siazUoEp9jrthXpaVpPo0tBFiaG2vmmUvWMCQKs4G8jAMQE6l9WL4DvqicjfvibHqUldqbWkk/640?wx_fmt=png&from=appmsg)

## 它为什么好看

聊完攻略，最后聊聊设计思路。这套瑞士风的视觉规则到底从哪来。

我给它的视觉锚点是 Massimo Vignelli 加 Helvetica Forever。

纽约地铁系统、Unimark、Müller-Brockmann 那一脉的瑞士国际主义传统。

如果你打开过 *Helvetica Forever* 那本书，或者看过 Vignelli 给纽约地铁做的 1970 年版导视系统，就会认出这套语言。

把两种风格放在一起对比，差别一下就出来了：

![](https://mmbiz.qpic.cn/mmbiz_png/ofWbZTuv4DWPl0FDgruaKEQNgefMI8bvkXbuT2VAECE6vA0PNVTlNCNWZA4CHQrw6TTzDILcuhuiblLYmDrE5wCibYFXKzc1kgROabbWOIPe4/640?wx_fmt=png&from=appmsg)

简单说：A 适合讲故事，B 适合讲事实。

### 7 条设计纪律

瑞士风的视觉规则其实就七条，每一条都是行业沉淀，一百年前就有了。

我做的事，是把它们一条条写进 Skill，让 AI 替我执行。

1第一条，单一锚点色。一份 deck 里只允许一个高亮色。蓝就只有蓝，黄就只有黄，绝对不能蓝黄拼贴。这是瑞士风的灵魂。Less is more 不止是口号，要落到代码层面写成硬规则。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ofWbZTuv4DVPWQbzmG2R7lqwafRBwBDUCbn4AB2ymnpGuwx1LtI2vAeg6CFT1a3ClwCT7KUja4vPmRambjZaTLy6OE6yobjgSt60zMMrVEY/640?wx_fmt=png&from=appmsg)

2第二条，极致字号对比。主标题与正文比例至少 8:1。封面巨字宣言用 `min(11.6vw, 19vh)`，正文 1.1vw。视觉张力全靠这种对比拉出来，靠装饰是出不来的。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ofWbZTuv4DWI0Ug0TRCbuW5ha2bjMwk6sG6fwBYEvxeX6vW4BmfJic8L9VkPZjRml5Wpae4ogqBJ2vLqiaeibjvPbiaqicHKgtbUuVpLFdbHwaZ0/640?wx_fmt=png&from=appmsg)

3第三条，大字越大越细。主标题字重 200（ExtraLight），别用 700、800、900。瑞士风的大字像建筑蓝图上的标尺，要被看见但不能喧哗。这条我吃过亏，一开始写的是 800，整页瞬间像 PowerPoint。

![](https://mmbiz.qpic.cn/mmbiz_png/ofWbZTuv4DUR7iazMkxAdSebMVwjIzRiaemf440RFDXqic3RUib9bBNBQvy3NxoJYyhIDicjdVHXureAl1KGM1iaerxY2D99nVjXZeBXEcvdfpW2o/640?wx_fmt=png&from=appmsg)

4第四条，直角纯色。`border-radius`、`box-shadow`、`linear-gradient`，三件事一律砍掉。所有色块都是直角，所有边界都是 1px 发丝线。看上去苛刻，但你看到的所有"消费 app 感""SaaS 模板感"，都是这三个属性滥用出来的。

![](https://mmbiz.qpic.cn/mmbiz_png/ofWbZTuv4DWVSLTicoATiajRia2axlXXhkUMLLbibL2YYC2DYqIyBxorCicn8TM4obbd1vFicSDnIvY76wKoUDXjDXiazziaajxVIHwQWcVVoficnFFY/640?wx_fmt=png&from=appmsg)

5第五条，网格至上。16 列 grid 加 16px gap，所有元素吸附到网格，左对齐加大幅留白做非对称美学。不要居中，不要平均分布。

![](https://mmbiz.qpic.cn/mmbiz_png/ofWbZTuv4DXNmibaZ9FUBYCYboRhw4ibsMUIT02rJMMrE7UePmOD1gmIycTCGCr59gfD4QUpz5qESrc6nibRbDj8aIvvQ7sHeCsBDpfRLmzRkU/640?wx_fmt=png&from=appmsg)

6第六条，没有 WebGL 背景。风格 A 用 WebGL 流体做呼吸感，瑞士风刻意把这个去掉了。纯白底就是它的底色，任何动态背景都是干扰。

![](https://mmbiz.qpic.cn/mmbiz_png/ofWbZTuv4DXzkiacicJLNaPsVXWPdKYFh4QOh0xkjHNMvIqSUFib1ZIYIGcavPrHrVLKGic0YVNU0wgEJc0kl2iav9BFQvzDe905hr8GlLyojxiaA/640?wx_fmt=png&from=appmsg)

7第七条，封面/封底是色彩闭环。上面那个小巧思就是这条规则的产物。开场和收尾用同一个色彩主旋律首尾呼应，整本 deck 的"完成度"立刻就有了。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ofWbZTuv4DUcBe0VhM0VH5m02FYcfqsuoOWsX8iascrb9JBckRb43HHQdeGZKaKkKVV5d22wkX91LMaepjiaB4iamgiahe1rpEHiaozHQtgFqxicE/640?wx_fmt=png&from=appmsg)

## 写在最后

这次更新的核心，其实只回答了一个问题：人 × AI 协作做内容这件事，链条到底有多长？

之前那次开源，我把"做 PPT"这个环节做完了。

这次往前接了"配图生成"，往后接了"多平台封面"。再加一个新风格、一套新色彩闭环，整个链条就闭合了。

从写大纲、生成 PPT、配图、导出、到发布到不同平台。以前要打开 5 个软件，现在在一个对话里能走完。

为什么在市面上已经有了如此多的 PPT Skills 的情况下。

藏师傅的 PPT Skills 依然能获得如此大的使用量和关注量呢？

AI 永远只能做 70 分的事情。这两套模板的每一页版式，都是在 AI 的基础上，我通过人工一点一点的微调实现的。也就是说，我在用自然语言进行设计。

即使在 AI 时代，90 分的内容依然是弥足珍贵的。

Skill 已经更新到 GitHub：`github.com/op7418/guizang-ppt-skill`

更新方式跟上次一样。README 里有"给 AI 的安装 prompt"，复制粘贴给你的 Claude Code、Codex 或任何有 shell 权限的 AI Agent，它会自动拉取最新版本。

装好之后对它说一句"帮我做一份瑞士风 PPT"就会触发新风格。

**如果觉得对你有帮助，欢迎点赞分享，也欢迎在评论区贴一下你用这套 Skill 做的 PPT 或者封面。**

✦
