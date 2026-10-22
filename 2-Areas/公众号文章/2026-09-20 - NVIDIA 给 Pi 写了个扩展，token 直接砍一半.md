---
title: "NVIDIA 给 Pi 写了个扩展，token 直接砍一半"
author: "呼拉拉"
publish_date: "2026-09-20 10:18:42"
saved_date: "2026-10-22"
source: "wechat"
url: "https://mp.weixin.qq.com/s/50QI6AL983R7XA6BgPwamQ"
---
# NVIDIA 给 Pi 写了个扩展，token 直接砍一半
来源：NVIDIA 官方博客（nvlabs.github.io/SoL-Pi）与 GitHub 仓库 NVlabs/SoL-Pi。号外！！大厂英伟达给PI写扩展了！

01｜一条命令，装上了 NVIDIA 的扩展

`pi install git:github.com/NVlabs/SoL-Pi`

装 Pi 的扩展大多来自社区开发者的个人仓库，这次后面跟的是 NVIDIA 官方实验室。

NVlabs 给一个开源 coding agent 写扩展，这事不多见。Pi 刚过 10.6 万 Star，各路团队基本都在观望，NVIDIA 直接交了代码。

这个扩展叫 SoL-Pi，干的事一句话能说完：**长任务的 token 消耗砍掉将近一半，分数基本不掉。**

![](https://mmbiz.qpic.cn/sz_mmbiz_png/VziaU7h07w0APlwIic6vsDCS73JOH5vS9tq3SoUQS0JK7QCw3vPvh76FyUcTTa73746mrkrKa0l7DBwzPKOIYDTdkic6r5tWPqibGNS6VWhMFqQ/640?wx_fmt=png&from=appmsg)

02｜它管的就是你天天心疼的那几件事

先划边界：SoL-Pi 不换模型，不改 Pi 内核，纯走 Pi 的公开扩展 API。四个机制默认全关，想用哪个开哪个。

四个机制，每个都能对上号。

**Action Fusion**，管的是「改完就跑」这件事。你让 Pi 改个文件，它十有八九接着要跑测试看看结果。现在的流程：改完，等模型决策一轮，再发命令，再等结果。Action Fusion 把这两步并成一次调用，本地直接改完就跑——像出门顺手把门带上，不用回头再确认一遍。博客里有句原话我觉得说得很准：「removing the middle model decision」——砍的就是中间那轮你根本不需要参与的决策。

**ObservationPack**，管的是上下文里的大输出。跑长任务最直观的体感就是上下文在涨：几十 KB 的日志、几千行的文件，每轮请求都重新发一遍，token 就是这么烧的。ObservationPack 把大输出存到本地，上下文里只留一个句柄加一小段摘录，要用再按页取回。像仓库给你一张提货单，货还在架上。

**Evidence-Preserving Reducer**，管的是「谁帮你读日志」。几千行的测试日志，真正影响下一步决策的可能就两三行。这个机制让更便宜的模型先读——像让实习生先看，关键页我自己复查——读出一份诊断摘要，但摘要里的每一条引用都要逐行对回原文，对不上就作废。便宜模型只负责找，不做判断。

**Online Context Compact**，管的是「什么时候压缩上下文」。一般 harness 都是等上下文快爆了才压缩，它改成每干完一个子任务，就考虑把这段收进柜子，不等爆仓。

四个机制各管一段，凑在一起就是四个字：**少烧 token。**

![](https://mmbiz.qpic.cn/sz_mmbiz_png/VziaU7h07w0Cd3D70MNjeM153G5AiaCUiafXIqRGTXIYYNjTAJu9kqU2Ump2KibVC9mI0hXqWm4yLGZxHbdRIvOicc1WthzjHw08Bg2icss9hqfN8/640?wx_fmt=png&from=appmsg)

03｜这些数字，我打算这么验

博客给了组数：51 个长任务里 token 少用 45%-49%，分数保住约 94%；对比 Codex、Claude Code 自带的 harness，每小时账单还能多省 8.75 到 13.50 美元。

它省的是哪部分钱？对着四个机制想一遍就清楚了：ObservationPack 省的是大文件大日志的重复发送，Action Fusion 省的是「改完再跑」中间那轮决策，Compact 省的是干完没收的上下文。**这三笔，恰好是我看着 /session 数字蹭蹭涨的主力。**它不是魔法，是把该省的钱都省了。

我的验法：装上，先开那两个开关——是哪两个、配置文件放哪，第 05 节直接给你抄——挑一个日常要跑构建的长项目照常干活，一周后用 `/session` 对比前后的 token 和花费。不用跑基准测试，自己的账单就是最诚实的评测。

建议你也这么试。一条命令的事，最坏的结果就是卸载。

04｜这四个机制不是人拍脑袋想的

比省 token 更有意思的是这四个机制怎么来的。

NVIDIA 没开会定方案，而是铺了 535 个训练环境，扔进 152 个提案方向，交给一套自动科研循环：agent 生成轨迹、独立分析、提出机制、另一个 agent 实现和审查，训练集先筛一轮，最后放到完全隔离的留出集上验收。

留出集的任务，循环里没有任何 agent 见过。跑不出分，直接淘汰，不给返修。

**152 个进去，4 个出来。存活率大约四十分之一。**

筛掉它们的不是评审的口味，是留出集里跑不出来的分数。

这套流程本身可能比四个机制更值得记：AI 给 Agent 做研究，第一批实体成果长这样。

![](https://mmbiz.qpic.cn/mmbiz_png/VziaU7h07w0CcCvNcgnEwzd0MEqnvhvMbAM83Xg9zux4tN72ZC9R4ZqfjPHXGUakLAIQDyIscEUCSyTtqI1Otp1Vo0TolrCK2LvMefDWySAM/640?wx_fmt=png&from=appmsg)

05｜上手：配置文件放哪，先开两个

配置只有一个文件：`sol-pi.json`。SoL-Pi 按顺序找两个地方——

· 只在当前项目用：放在项目根目录的 `.pi/sol-pi.json`（要求这个项目是受信任的）
· 全局都用：放在 `~/.pi/agent/sol-pi.json`

两个都不存在，就用默认值：四个机制全关。项目级优先级更高，两个文件不会合并。

我上面说要先开的那两个就在这里配。官方 README 原样给了份保守配置，直接抄：

`{  "version": 1,  "actionFusion": true,  "observationPack": true,  "evidencePreservingReducer": false,  "onlineContextCompact": false}`

官方示例里还带一行 `cacheWriteReadRatio: 12.5`，那是 Compact 专用的经济阈值，Compact 没开就用不上，我省了。

`actionFusion` 和 `observationPack` 就是那两个：纯本地完成，不多花模型调用，也不打断任务，开了没有副作用。`evidencePreservingReducer` 会把日志发给配置的便宜模型，涉及敏感代码和日志的，先想清楚再开。

配完该干嘛干嘛，一周后 `/session` 见分晓。

06｜冷静面

三句话说完代价。

第一，短任务感知不强。这套机制都是为长任务设计的，十分钟以内的活，开不开没区别。

第二，它省的是钱，不是提分。94% 的意思是可能丢 6%。博客照实写着：Terminal-Bench 4 上 Pi 解出 18/63，SoL-Pi 解出 15/63——账单省了 61 美元，少解出 3 道题。**这笔账 NVIDIA 没藏。**

第三，它服务的是天天跑长任务、看着账单心疼的人。偶尔用用 agent 的，没必要折腾。

月底对账单的时候，你会不会想起这篇文章呢？

往期回顾：

[· 从 Claude Code 搬到 Pi：我装了这 6 个扩展，把熟悉的体验补了回来](https://mp.weixin.qq.com/s?__biz=MzkwMzg2Nzc1NQ==&mid=2247483674&idx=1&sn=a3318d79d1b7363a3ca20792168bd2f6&scene=21#wechat_redirect)

[· 刚装完 Pi，先改这 5 个地方](https://mp.weixin.qq.com/s?__biz=MzkwMzg2Nzc1NQ==&mid=2247483731&idx=1&sn=598d267cd1ba77656dd94220885d6fef&scene=21#wechat_redirect)

#Pi #AI编程 #NVIDIA #英伟达 #AI编程工具 #开源项目
