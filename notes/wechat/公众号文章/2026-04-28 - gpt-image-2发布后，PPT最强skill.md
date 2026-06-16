---
title: "gpt-image-2发布后，PPT最强skill"
author: "AI Prime"
publish_date: "2026-04-28 11:13:13"
saved_date: "2026-05-31"
source: "wechat"
url: "https://mp.weixin.qq.com/s/nAzCfRg3TxGqxGusVKC20g"
type: wechat-article
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
  source_url: https://mp.weixin.qq.com/s/nAzCfRg3TxGqxGusVKC20g
---
# gpt-image-2发布后，PPT最强skill
先看一页ai ppt效果图，已经追上古法ppt了。

![](https://mmbiz.qpic.cn/mmbiz_png/CT8qWWQqv0icl3w9e1CS9YTL0eeRnsNZbV0Ytq8hIawoP2GBqM3xyzrxvib97r8EGuQlpPSPYlTqLXUNaO9eqiaj7ExN64J6oO51QQN6mQHQeM/640?wx_fmt=png&from=appmsg)

过去用 AI 做 PPT，最大的问题不是“能不能生成”，而是：

- 逻辑容易散
- 风格不稳定
- 生成完还要手工塞进 PPT
- 演讲备注还得另写一遍
`gpt-image-2` 这类高质量图像模型出来后，真正拉开差距的不是单张图能力，而是**能不能把 PPT 变成一条稳定流水线**。

我现在用的方案，它不是“让 AI 随便做几页图”，而是把 PPT 拆成 10 个可控步骤：分析、确认、大纲、提示词、生图、备注、合成、迭代。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/CT8qWWQqv0icbcFugJNDvr8NCPOugdsF0R8mzFoFRfdrMLbPMdtzhmyLYMfl4B9N0viaibmkXd7RB4McrQefI1ty5icXMxHFvJvwbhyTFEC7jHM/640?wx_fmt=png&from=appmsg)

## 一句话总结

这个skill的核心能力是：

> 先把内容变成结构化大纲，再把每页变成可复现的图片 prompt，最后批量生成整页幻灯片图片，合成为 PPTX，并自动把中文演讲稿写进备注。

这套流程最适合三类 PPT：

- 商务方案：客户交流、售前材料、解决方案
- 技术汇报：架构设计、产品能力、行业方案
- 公众号/路演：视觉冲击强、适合阅读和转发

## 为什么它比“直接让 AI 做 PPT”强

直接让 AI 做 PPT，通常是一口气生成。

结果是：第一页不错，第三页跑偏，第五页文字炸，第八页风格变了。你想改一页，还得整套重来，这个skill的做法完全不同。

它把 PPT 拆成这些中间产物：

文件

作用

`analysis.md`记录主题、受众、风格、页数建议

`outline.md`整套 PPT 的结构化大纲

`prompts/`每一页独立的生图提示词

`NN-slide-xxx.png`每一页生成后的整页图片

`speaker-notes.md`每页中文演讲人口述稿

`.pptx`最终 PowerPoint 文件

这意味着：每一步都能检查，每一页都能单独改，每张图都能复现。

## 完整流程：10 步做出一套 PPT

### 1. 输入资料

你可以给它：

- 一个主题
- 一份 Word
- 一组 PPT
- 多份参考材料
- 品牌图或视觉参考
- 直接粘贴的业务说明
它会先把原始内容保存下来，不直接开画。

### 2. 内容分析

系统会判断：

- 这是销售材料、技术材料，还是培训材料
- 面向高管、客户、专家，还是内部团队
- 适合几页
- 适合什么风格
- 重点应该是讲逻辑、讲产品，还是讲价值
分析结果会写入 `analysis.md`。

### 3. 方案确认

默认会先确认 5 件事：

- 风格
- 受众
- 页数
- 是否审核大纲
- 是否审核提示词
这一步很关键。PPT 不是图片合集，方向错了，后面越精美越浪费。

### 4. 生成大纲

大纲会写进 `outline.md`。

每一页不是只有标题，而是包含：

- 页面标题
- 页面类型
- 叙事目标
- 关键内容
- 视觉方案
- 版式建议
也就是说，`outline.md` 是整套 PPT 的剧本。

### 5. 审核大纲

如果你选择审核，它会先给你看每页的标题和结构。

这一步适合做三件事：

- 删掉重复页
- 调整讲述顺序
- 补上缺失的商业闭环
先改逻辑，再生成图片，这是效率最高的。

### 6. 生成每页 prompt

确认大纲后，它会为每一页生成独立 prompt：

```
prompts/01-slide-cover.mdprompts/02-slide-market-window.mdprompts/03-slide-pain-points.md...
```

这里的价值非常大。

因为后面如果某一页不满意，不需要重做全套，只改这一页 prompt，再单独重生这一页。

### 7. 用 Image Gen 生成整页图片

最新版流程里，生图优先使用系统自带 Image Gen，走gpt-image-2生图通道。

如果主通道某一页连续失败 3 次，才会 fallback 到用户提供的兼容图片接口。

### 8. 自动生成演讲人备注

这是很多 PPT 工具没有做好的地方。

这个skill 会生成 `speaker-notes.md`，格式类似：

```
## Slide 1 - 标题这里是这一页的中文口述稿。
```

它写的不是图片提示词，而是真正适合演讲时说的话：

- 解释这一页在讲什么
- 点出关键业务价值
- 衔接下一页
- 控制在口播可用的长度

### 9. 合成为 PPTX

生成的图片会按顺序铺满 PPT 每一页。

同时，`speaker-notes.md` 会被写入 PowerPoint 的备注区。

最终得到的是一个真正可交付的 `.pptx`，不是一堆散图。

### 10. 单页迭代

后期改稿非常简单：

需求

做法

改某一页画面

改对应 prompt，重生这一页

改某一页话术

改 `speaker-notes.md`

增加一页

新增 prompt，生成图片，更新大纲和备注

删除一页

删除图片和 prompt，重新编号并合成

换首页风格

只重生第 1 页，再 merge

这才是 AI 做 PPT 应该有的工作流。

## 最强的地方：可控

我最看重的不是它能生成多漂亮的图，而是它把所有中间过程都保存了。

这意味着：

- 逻辑可控：有 `outline.md`
- 视觉可控：每页有 prompt
- 结果可控：每页是独立图片
- 备注可控：有 `speaker-notes.md`
- 迭代可控：可以单页重生
- 交付可控：最终是 PPTX
AI 生成内容最大的坑，就是过程不可追踪。

这套 skill 反过来，把过程全部显式化。``

## 什么时候一定要审核 prompt

下面几类 PPT，我建议必须审核 prompt：

- 客户正式汇报
- 品牌色要求强
- 涉及复杂架构图
- 页面文字较多
- 需要参考图片风格
- 对首页视觉冲击要求高
因为图片模型很强，但它不懂你的最终审美偏好。

最稳的方式是：先让它生成 prompt，再人工看一眼方向。

## 实战经验：别追求一次成片

真正高效的做法是：

- 先把大纲做对
- 再把 prompt 做稳
- 批量生成第一版
- 挑 2-3 页重点改
- 最后合成 PPTX
不要一开始就纠结每页细节。

PPT 的质量，先由结构决定，再由视觉决定，最后才是局部微调。

## 结论

`gpt-image-2` 之后，PPT 的上限被大幅抬高。

但真正能稳定交付的，不是“单次生成”，而是“工程化流程”。

这个skill强就强在这里：

它把做 PPT 变成了一个可复现、可审核、可并发、可单页迭代、可自动写备注的流水线。

一句话：

> 以后做 PPT，不要只问 AI 能不能生成。要问它能不能重来、能不能单页改、能不能写备注、能不能最终交付 PPTX。

### 关注后私信发送 ppt ,获取基于gpt-image-2的最强ppt skill
