---
title: "又一个 DeepSeek Harness 神级插件诞生了！"
author: "JavaGuide"
publish_date: "2026-10-15 16:39:32"
saved_date: "2026-10-15"
source: "wechat"
url: "https://mp.weixin.qq.com/s/_CDvi_vyhF5d9lhVcaF0YQ"
---
# 又一个 DeepSeek Harness 神级插件诞生了！
用 DeepSeek Harness 跑任务，输入框旁边能看到上下文占用了多少，但光看一个百分比，很难知道里面到底装了什么。是对话记录越来越长，还是某次读文件、执行命令带回了太多内容？

我们发给 Agent 的任务要求，只是上下文的一部分。系统提示词、工具说明、技能目录、项目里的 `AGENTS.md`，以及执行过程中产生的回复和工具结果，也可能进入模型的请求。任务跑了很多步以后，要弄清哪部分占得多、从哪一步开始增长，单靠翻聊天记录会比较费劲。

最近有一个爆火的 DSH 插件 dsh-context，就是给 DeepSeek Harness 补上这部分查看能力的第三方开源插件。它把上下文按组成和执行步骤展开，可以查看具体内容、估算的 Token 占用，以及对应的注入记录和工具调用。

![](https://mmbiz.qpic.cn/mmbiz_png/icJuV9QZRqg7oAmS3eTEzrqnBIecKialCQiatPicNGSFmzgJeHnaouDcWOCQTia79jmhB4HOianXG7uFRQACb3zRgTphMzD2ujg9icFsutyG0CCcg8/640?wx_fmt=png&from=appmsg)
dsh-context 项目介绍想精简工具配置、缩短项目规则，或者查清一次任务为什么带入了大量内容，有这样一个面板，就能先找到具体来源，再决定改哪里。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/icJuV9QZRqg4Z2Cll1E55RXW9drpX6nuvL8l45NoVHlzdfTSQe0S3qlIojQ9AI6UOib9gFAqPu7KeJ1f2tOphcsMSwxiaeeEJym1Vlf0Hmvom4/640?wx_fmt=png&from=appmsg)
dsh-context 的 GitHub 仓库页面
## 装好以后，先打开一条已有任务

桌面端左侧打开“插件”，点击“添加插件”，输入 `dsh-context`，安装完成后点“立即启用”。启用后，左侧多了“上下文洞察”，会话顶部也出现了“上下文”和“编队”两个标签页。

英文界面对应的入口是 Plugins → Add plugin，输入包名后点击 Install。下面的英文截图展示添加插件窗口，本次本地实测的版本信息见后文。

![](https://mmbiz.qpic.cn/mmbiz_png/icJuV9QZRqg7vgVSzyxSfKLrs4sq6nM36zXw4YJgH5QUEic1Zd3Ems4M1zzP8uxzVaY6FxAUAu6kQxvPoX9drFOSn6gFaZibkfWRnmeibWZuRGc/640?wx_fmt=png&from=appmsg)
添加 dsh-context 插件的英文界面示例这次使用的 DeepSeek Harness 是 `0.2.0-rc.2`。安装向导显示了 `0.71.0`，但详情页和本地实际安装包都是 `0.70.0`，上下文页面另有更新提示。所以下面的体验以实际加载的 `0.70.0` 为准。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/icJuV9QZRqg77FJCBQFsVPIpbQBW2tWPYfZdshxJu9TkPkQfa2lhDztgiabQT3FbEQU8odmLP8ZnRLq0Hibib1GGWEOSXSkwCXcQQuTcnicDoecY/640?wx_fmt=png&from=appmsg)
本次实际加载的 dsh-context 版本我在本地 macOS 桌面端选了一条已完成的飞机动画任务，点击“上下文”，原来的执行记录就显示出来了：**1 轮、7 步、6 次工具调用**。这次回看没有重新生成动画，后面的 Token 数据都来自原任务。用户只发了一次要求，Agent 在内部反复请求模型、执行工具，直到给出最终回复。

## 累计用了多少，和当前装了多少

Harness 自带的本轮用量弹窗，可以看到未缓存输入、缓存读取和输出。这条任务的本轮用量是 `363,312` Token，输出中还单独列出了推理用量。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/icJuV9QZRqg5IzoImm3SY7wurNl1A1PcEobOfJqwtpxYyRwPribwKIDc05ygCScXNZpuVpQhAloG98L4v1JCWGzEnVmvEhS6LFicM2l8LviaicD0/640?wx_fmt=png&from=appmsg)
Harness 原生本轮用量明细dsh-context 的“Token 统计”显示总用量 `363.3k`，缓存命中率为 `95.72%`。这是整个会话多次请求累计的用量，包含输入和输出；前面的历史内容可能随后续请求再次计入输入，其中一部分命中了缓存。

![](https://mmbiz.qpic.cn/mmbiz_png/icJuV9QZRqg5o6wvZYQict4Fh6ygEYHNiaktyLibCnS7zdTBwib6KPoO9koODXveZHiatyIXxqFyiaMic9jm0hVZ5NuuOLcwFmnygDhSnGodfX8dsN8/640?wx_fmt=png&from=appmsg)
整个会话累计的 Token 用量往下看“当前上下文”，显示的是 `54.6k / 1.0M tokens`，占用 `5.5%`。它回答的是当前上下文窗口装了多少内容。判断离窗口上限还有多远，应看这里，不能拿累计的 `363.3k` 直接除以窗口大小。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/icJuV9QZRqg7bmOiaxsjAfUWySwaTibn6gD9JN7KBp8wdr1icuXibWYtl19GBl733Ed6DqJZRwo4B3NHX8h5SA3TP0tib8WLicEMOtACbibEfdkpK4Q/640?wx_fmt=png&from=appmsg)
当前上下文的占用与组成这一页还把内容分开列了出来：系统提示词、工具定义、用户消息、注入内容、技能注入、助手消息和工具结果。本次回看中，助手消息约 `31.1k`，工具定义约 `6.8k`，技能注入约 `3.0k`。我输入的那段任务要求，估算只有约 `73` Token。

若工具结果占了大头，就去找哪次读取或命令输出带回了大量内容；工具定义占得多，就检查模型收到了哪些工具说明。这条动画任务里，助手消息的估算占比最高，我会先展开这一类查看。

不过，**分类数字旁边的 ≈ 要一起看**。插件用固定密度启发式估算各类内容的 Token，供应商上报的实际用量则另列。截图中的分类合计与顶部占用数并不完全一致，适合用来定位主要来源，不能当成精确的逐项分账。

## 回到第一步，看看模型出发时带了什么

“上下文浏览器”右上角可以选择历史步骤。我切到第 1 轮、第 1 步，助手消息和工具结果都是 0，工具定义却已有 27 项，估算约 `6.8k`，占这一步估算上下文的 `55%`。

![](https://mmbiz.qpic.cn/mmbiz_png/icJuV9QZRqg4MicXaMQZm6ZsUI269ynjTQK9Qy7ia8cIOHz7ApqjecabgmSYBibtGgUmH5M51aibZC1qOkbJDX8EyickLic4hprUyJiaTIsO4M6rRFo/640?wx_fmt=png&from=appmsg)
第一步请求的上下文组成系统提示词、工具说明、技能目录和项目指令，先于第一条助手消息进入了上下文。展开“工具定义”，还能看到具体工具的来源包、估算大小和调用次数，列表支持按大小、次数或名称排序。我试了按大小排序，可以把较长的工具说明放到前面检查。

“上下文事件”则记录了另一部分来路。这次有 3 条注入：`skill-catalog`、`runtime-context`，以及项目里的 `AGENTS.md`。点击技能目录，能看到当时注入的技能名称和简介。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/icJuV9QZRqg6kH9jib3AVWVAaK60pKdibw2kMpwDRKBogwCZpMTHMyd23soZ11PU5usFqO3a6ZKjeO6o1sa8dwEq5LtH2tl2LTQMZAMRN77EPU/640?wx_fmt=png&from=appmsg)
技能目录、运行时状态和项目指令的注入记录这里还有一个容易混淆的数字：页面显示技能加载次数为 0，但技能注入约有 `3.0k`。展开后看到的是可用技能目录；目录进入上下文，与调用某个技能、加载它的完整说明，是两件事。

以后要精简一套配置，我会先看这些实际内容，再决定删哪项工具或规则。只看插件装了多少个，很难判断它们在这条任务里占了多少。

## 一轮对话里的七步，可以分别回看

趋势图按模型请求画柱子，同一轮里的多次请求也会分开显示。飞机任务只有一轮，却有七根柱子，能看到上下文在执行期间怎样增长。图下方还列出某一步的用户要求、新进入的内容，以及模型回复或发出的工具调用。

![](https://mmbiz.qpic.cn/mmbiz_png/icJuV9QZRqg6Zu7iadPKJluDXeshfXRrdPSeicHvia8xTGyVwpvmwgHWjnhEVctOVGraC0UQq0rWHFCkE2Y97BbBKj97scj8zXgibVQmYquCh500/640?wx_fmt=png&from=appmsg)
七个步骤的上下文趋势排查某一步突然增长时，可以回到对应请求，在浏览器里展开那一类内容，核对具体文本和工具输出。页面也提供“全量／增量”切换，以及压缩、剪枝等事件记录。这个历史任务里的压缩和剪枝次数都是 0，本次没有验证发生压缩后的还原效果。

插件还把文件操作接到了同一条查看路径上。“文件活动”列出飞机 HTML 的两次写入操作，展开后分别是 `write` 和 `edit`。点击其中的 `edit`，上下文浏览器就跳到了对应调用，能看到 `file_path`、`old_string`、`new_string` 和工具返回结果。

![](https://mmbiz.qpic.cn/mmbiz_png/icJuV9QZRqg7hkh8ysqUWmJXMulWlz7etwvL1ym8DxibxkCmZ6POVNkxYibonWzSqzbX9YaB70HSDQzmr614FB3FIl9fiaT6icgvvZGN0HCDqLia4/640?wx_fmt=png&from=appmsg)
从文件活动跳转到具体 edit 调用这条记录里，原来一次传入四个参数的 `ctx.lineTo(...)` 被拆成了两次调用，工具返回文件更新成功。回看时，可以直接对照修改前后的代码，不必在长对话里逐条翻找。

文件活动里的增删行数按工具参数估算。要验收最终代码，仍要打开文件、检查 Git Diff，再做相应的运行验证。这次回看核对的是调用记录，没有重新验收动画代码。

## 日常用，可以从 /context 开始

不想离开对话时，在输入框里输入 `/context`，从候选菜单执行，就会弹出当前组成和上下文浏览器。我在同一会话里验证了这个入口，弹窗打开后，轮次和步数仍是原来的 1 轮、7 步。

左侧“上下文洞察”适合先找任务：可以按时间范围查看汇总，再搜索会话标题、按 Token 总用量等条件排序，点击卡片进入具体会话。本次安装后，历史统计最初尚未出现，稍后回到页面才看到了回填的记录，刚启用时可以给它一点加载时间。

下面的英文界面展示了跨会话总览的布局，图中的会话数量和用量属于示例，与上面的本地任务分别统计。

![](https://mmbiz.qpic.cn/mmbiz_png/icJuV9QZRqg6BZP5kAibDkyAaOQhGqAGcW1L5oKguqZ7LfgttbEChF500phE9dUgDBZppQ5n5pturABjEsH0P1albBUKsib8RczeEdY83HAQAQ/640?wx_fmt=png&from=appmsg)
上下文洞察的跨会话总览示例“编队”页用于查看当前 Agent、父 Agent 和子 Agent 的关系。这条任务没有子 Agent，我没有据此验证多 Agent 统计。

可以把 dsh-context 留在 Harness 里，用它回看那些输入不长、执行过程却很长的任务。下一次想精简上下文时，先找到占用最大的那类内容，展开看一眼，再决定改哪项配置。

![](https://mmbiz.qpic.cn/mmbiz_png/nKBz2uVsouzicNYTcZ6smN0I4Q0Rm0oDd0ToWJIPpSFp0YUEJ3CYyxlFG4bR5Gs1IT4h28icZxgZ0tJ2jK4pFWPA/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1&randomid=eyim9p00&tp=webp#imgIndex=9)

**⭐️推荐阅读**:

- [AIGuide：AI 应用开发、AI 编程实战与面试指南](https://mp.weixin.qq.com/s?__biz=Mzg2OTA0Njk0OA==&mid=2247555122&idx=1&sn=96278bed8e2b414434398b56785ea2bd&scene=21#wechat_redirect)（对标 JavaGuide，完全开源免费）
- [JavaGuide： Java 面试指南和后端通用面试复习资料](https://mp.weixin.qq.com/s?__biz=Mzg2OTA0Njk0OA==&mid=2247552140&idx=1&sn=551aeaa2298099436d22ac4983b17c49&scene=21#wechat_redirect)（Github 157k+ Star）
- [《SpringAI 智能面试平台》（2.0 版本已开源）](https://mp.weixin.qq.com/s?__biz=Mzg2OTA0Njk0OA==&mid=2247552320&idx=1&sn=a7e4e5a8d957446e6bb032d78b2fa5fb&scene=21#wechat_redirect)(Star 数量 **3k+**)
