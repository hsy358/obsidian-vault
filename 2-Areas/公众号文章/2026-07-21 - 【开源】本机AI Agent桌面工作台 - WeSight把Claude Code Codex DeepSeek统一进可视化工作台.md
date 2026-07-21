---
title: "【开源】本机 AI Agent 桌面工作台，将 Claude Code、Codex、DeepSeek统一到一个可视化工作台里，覆盖对话、工具、文件、IM 通道、技能、"
author: "soft张三丰"
publish_date: "2026-07-21 11:30:00"
saved_date: "2026-07-21"
source: "wechat"
url: "https://mp.weixin.qq.com/s/VXuInryLLGDMD_emDuyhiA"
---
# 【开源】本机 AI Agent 桌面工作台，将 Claude Code、Codex、DeepSeek统一到一个可视化工作台里，覆盖对话、工具、文件、IM 通道、技能、
# 项目由来：从“黑市”到开源的逆袭

2026年4月，一款名为WeSight的桌面工具悄然上线。令人咋舌的是，它的内测邀请码在二手市场一度被炒到999元。作者苍何在意识到封闭分发带来的局限性后，于2026年6月1日（儿童节）做了一个大胆的决定：彻底开源，将这份“儿童节礼物”献给社区。

## 为什么要做 WeSight？

随着 Claude Code、Codex、OpenClaw、DeepSeek-TUI 等终端原生 AI Agent 爆发，开发者陷入了“Agent 地狱”：

写代码要开一个终端跑 Claude Code，自动化任务又要开一个跑 OpenClaw；

每个 Agent 的模型配置（API Key、Base URL）散落各地，切换成本极高；

文件变更、权限弹窗、运行指标（Token/TPS）全在黑盒终端里，看不见摸不着。

WeSight 的定位非常清晰：不做新的 Agent，而是做“Agent 的驾驶舱”。它基于 Electron 构建，把散落在各处的本机 CLI 统一收进一个可视化工作台，让你“一个入口，管理所有 Agent”。

![](https://mmbiz.qpic.cn/mmbiz_png/6wEpbjZhHQxxOJcPV81mzvAxdgeU20ABZrccFVI0zayAJEPLWUzIusdfgMuyNRS8pSZNOHIzvHJDc8uVV7wFpD1CKJDGNGW1uK7PJ8wK5QY/640?wx_fmt=png&from=appmsg)

界面展示

![](https://mmbiz.qpic.cn/mmbiz_png/6wEpbjZhHQyR4KZ4HZiaS6J1KuyFxmS3M2racdibIF36LehEXVgxqRiaLibqpWHnrpZYPBXcOADwCtoGzvxjY3vpcaxpK8jaOUNuOYj8IfGXGhc/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_png/6wEpbjZhHQyWJIl86r1spd3DVKicyCjhvyXJibR1wh6icItDrxicJtGD3N5wICv8A6TESbyYjiaHk784tqIy8UPW8NmyqFN8lXOvc1V2J58uviawA/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/6wEpbjZhHQxNsY9tzy03ZOKEpoOIfAPYAOibTwhta59ZZ4M7KRhY15QryeruIIYq6VNLSjZ0tick8uKIl6fIiaqSV1IDEoibGyKWvH4AFIdABz8/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_png/6wEpbjZhHQyP4QqePbq1pDxrQicGytxhzDBDEmyJAwK0aYMlLAn9RdJY9XfkcpjlgyG86JdgcqagS0tMM8GPWwTicuv6uQUbiaARiam94nzgwyk/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_png/6wEpbjZhHQzplj9U79jvHgmp6OCY5Zaa8srTUgCmJ5Q0lKEo1QicrdIOJvZSFw8fuUuYIdLmezhs209ibpSVUc3aqCMU3A3JndrUNZicS1Hhqk/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_png/6wEpbjZhHQxeHdYq4AgFS32KkGjVCRc9cia9c9Uob5K0ibtzKLuMuUhRf11G7QY7GSxX4Yupj7JYVWyaQAonA2w8ngQAdWucyFlB9VjQLbmls/640?wx_fmt=png&from=appmsg)

---

# 核心原理：Harness 抽象与进程隔离

WeSight 并非强制接管你的 Agent，而是采用上层 Harness（ harness 抽象层）+ 进程隔离的架构：

引擎适配层：通过 externalAgent适配器或直接调用本机 CLI（如 Claude Code、Qwen Code），支持一键安装或复用你已有的终端配置，数据主权归本机所有。

统一模型路由：在 Setting 层集中管理 OpenAI、Anthropic、DeepSeek、Ollama 等 10+ 供应商，引擎可选择“跟随 WeSight 配置”，实现一次配模型，全局所有 Agent 通用。

可视化渲染层：React + TypeScript 前端将 Agent 的工具调用（Tool Call）、文件 Diff、权限请求实时渲染为 GUI 面板，而非冰冷的文本流。

IM 与 Runtime 桥接：通过 Gateway 模式将飞书等 IM 消息路由到指定 Agent 引擎，支持“受 WeSight 管理”和“系统级常驻”两种模式，即便关闭工作台，Bot 也能响应。

---

# 职场 AI 应用场景

在真实的办公环境中，WeSight 可以这样落地：

## 研发协作流水线

组建Agent Team：用 Claude Code（产品经理角色）写需求分析，Codex（开发角色）生成本地代码，OpenClaw（测试角色）跑沙箱验证。所有上下文隔离但在同一界面流转，右侧实时工作区直接看 Diff，不用切终端。

## 飞书/IM 异步操控

下班后或手机端在飞书群里 @WeSight-Bot，指令会被路由到本机运行的 DeepSeek-TUI 或 Hermes Agent 执行长任务（如夜间构建、日志分析），第二天上班在 Dashboard 看 TTFT、耗时和产物。

## 自动化研究与日报

利用SkillHub的定时任务功能，每天 8:00 自动触发内置 Runtime 抓取行业新闻、汇总邮箱、生成 Markdown 日报并推送到桌面，配合桌面宠物提醒你查看。

## 成本与效能审计

AI Runtime Dashboard 记录每次调用的 Token 消耗、TPS、工具耗时。团队 Leader 可据此判断是哪个 Agent 步骤太慢，或是哪个模型性价比最高，优化 Prompt 和引擎选型。

---

# 赚钱场景与变现案例

虽然 WeSight 本身是开源免费的，但它降低了对 Agent 的编排门槛，衍生出一些变现可能：

## 私域/社群代运营自动化

结合 WeSight 的IM Agent Hub与微信/飞书监控能力（基于 wechat-cli 底座），为商家搭建“社群智能管家”：自动总结群聊精华、触发关键词告警、定时发早报。按群数量或消息量向商家收取运维费。

## 定制化 Skill 售卖

在 SkillHub 生态中开发垂直领域技能（如“法务合同审查 Skill”、“电商竞品爬虫 Skill”），封装好后提供给其他 WeSight 用户付费安装或订阅更新。

## 本地化 Agent 部署顾问

针对中小团队不懂如何配置 Claude Code + 模型路由的痛点，利用 WeSight 的一键环境准备能力，提供“企业本机 AI 工作台搭建服务”，赚取部署与培训费用。

## 长任务托管（算力套利）

利用本机闲置 Mac 跑 Codex/Qwen Code 的定时重构任务或研报生成，通过 OpenRouter 等低成本模型供应商执行，产出结构化数据卖给需要资讯的研究机构（需注意合规）。

---

#  WeSight 的核心优点

极致的“复用”：不绑架用户，已有的 CLI 配置直接复用，无需迁移成本。

可观测性（Observability）：把 Agent 从黑盒变白盒，TTFT、TPS、工具耗时全记录，这是纯终端做不到的。

桌面级体验：GUI Diff、权限面板、像素风工作室与桌面宠物，让冷冰冰的编码 Agent 有了“同事感”。

开源透明：MIT 协议，数据安全在本机，不依赖云端调度器。

---

# 与同类平台的对比

![](https://mmbiz.qpic.cn/sz_mmbiz_png/6wEpbjZhHQx1ufsf5kx7FmyQLZTGnKBZnsA05cjQ3CQYeeeuon3rYfa95dylq0ia7HibDhmMqV2G6ut7ROS3k7Fg3ySySg2dEic9H5haa66M4s/640?wx_fmt=png&from=appmsg)

总结：如果你已经在终端里跑 Claude Code 或 OpenClaw，苦于切换和监控，WeSight 是目前唯一专注“本机聚合与可视化”的开源方案；如果你只需要一个写代码的编辑器，Cursor 更合适；如果你是搞多 Agent 底层研发的，CrewAI 更底层。

开源地址

-

```
关注公众号 回复 20260721 获得
```

[8元解锁820+优质项目！别再瞎找资料了！AI、低代码、Agent实战教程一网打尽，永久更新！](https://mp.weixin.qq.com/s?__biz=MzI3MTQyNDc5MA==&mid=2247504934&idx=1&sn=d781838f7483fbdf5292f17c22f54c50&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/6wEpbjZhHQzSZhP4iaca2QASvab1X7a7ia1ZRmRTGB1b2BcavQMH0fTJrl8aicJDyCK4D497n4rycQ3euxDL5bfg7ONGEPEBnfOMzIGuiaj5Sr4/640?wx_fmt=png&from=appmsg)
