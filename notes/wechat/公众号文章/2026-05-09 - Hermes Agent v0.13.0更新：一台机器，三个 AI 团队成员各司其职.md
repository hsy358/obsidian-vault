---
title: "Hermes Agent v0.13.0更新：一台机器，三个 AI 团队成员各司其职"
author: "量子智元"
publish_date: "2026-05-09 09:00:00"
saved_date: "2026-05-10"
source: "wechat"
url: "https://mp.weixin.qq.com/s/JH4CUsG_K_KjsqX4GA827g"
type: wechat-article
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
  source_url: https://mp.weixin.qq.com/s/JH4CUsG_K_KjsqX4GA827g
---
# Hermes Agent v0.13.0更新：一台机器，三个 AI 团队成员各司其职
在折腾 Hermes 的时候，碰到一个挺常见的问题——**一个 Agent 什么都管，context 越来越乱**。日历提醒、代码审查、论文检索全混在一起，记忆库里夹杂着各种碎片。找了一圈，发现 Hermes 其实内置了一个 Profile 机制，专门解决这个问题。

简单说就是：**在同一台机器上跑多个完全独立的 Agent**，各自有自己的配置、密钥、记忆和会话，互不干扰。这篇就记录一下实际操作过程。

## 01 | 为什么一个 Agent 不够用

把所有任务塞给同一个 Agent，短期内没问题。但时间久了会发现几件烦人的事：

你让 Agent 帮你管代码仓库，它顺便记住了你今天心情不好、想换工作。你让它帮你查论文，它的上下文里还夹着你上周让它安排的婚礼筹备清单。更麻烦的是，**不同任务需要不同的 API 密钥和不同的模型**——研究任务想用 DeepSeek-R1 做深度推理，日常闲聊用便宜的 Haiku 就够，但你没法在同一个 Agent 里同时配两套。

> 记忆污染是个隐性问题。你以为 Agent 记住了重要的事，但它其实把鸡毛蒜皮的碎事也一起存进去了。时间久了，质量会肉眼可见地下降。

Profile 就是为了解决这个问题——让每个角色只知道它该知道的事情。

## 02 | 三步创建你的 Agent 团队

先确认一下本地有没有安装 Hermes，命令行跑一下 `hermes --version`。有的话直接开始。

**第一步，创建专用 Profile：**

# 创建编码助手，并从当前配置克隆
hermes profile create coder --clone

# 或者完全从零开始（空配置）
hermes profile create researcher

![](https://mmbiz.qpic.cn/sz_mmbiz_png/kHVuibicqZ5k7ZgOib4thN0Wvxt3IPZhHJ8U3kdpkNTRwdc7ia0icXLTqWNZ7icibKeUKicDBVYWKyd6IL48uIQzF1bEgXS8ewZuC8Wxx7zObczJ8cU/640?from=appmsg)

创建 coder profile，系统自动生成同名命令 coder

加 `--clone` 参数会把当前的 config.yaml、.env 和 SOUL.md 复制过去，**但记忆和会话是完全独立的**——这一点很关键，老 Agent 的历史不会带过来。

**第二步，查看当前 Profile 列表：**

hermes profile list

![](https://mmbiz.qpic.cn/sz_mmbiz_png/kHVuibicqZ5k45jqjw4sS38KQ3TiaKSZk5MuClA1SFicCAicPLQcG1H7iaW75OYibEHPSFZL0ULJ2QxRKHV6Cq5grhXn8Y3RNdcGcgrOz9aCXJrRvQ/640?from=appmsg)

◆ 表示当前激活的 default profile，其他 profile 独立运行

**第三步，用 -p 参数切换调用，或直接用同名命令：**

# 方式一：直接用生成的同名命令
coder chat
researcher chat

# 方式二：用 -p 参数指定 profile
hermes -p researcher chat

# 设置默认 profile
hermes profile use coder
创建之后，每个 profile 都有自己的目录，完全隔离：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/kHVuibicqZ5k4rY0MqJQF0p2WuennGHyKeeJN1fAmDTytlicoic5WMdaZuCzemh7VuiaAD0e3pjvsaIU1I1NNia6icXSic5eT0xXtorWLe2lcd3etKA/640?from=appmsg)

每个 profile 是一个独立的 Hermes 主目录，互不干扰

## 03 | 每个 Agent 的人格定制

创建完 profile 之后，最重要的一步是**编辑它的 SOUL.md**——这是每个 Agent 的人格定义文件，决定它的专长边界和行为风格。

# 编辑 coder profile 的人设
vim ~/.hermes/profiles/coder/SOUL.md

# 或者用 Hermes 自己编辑
coder config edit
我自己的三个 profile 大概是这样分工的：

![](https://mmbiz.qpic.cn/mmbiz_png/kHVuibicqZ5k5xqlOSTjh1eXicDWoTndw4K7qxDDpGTA7UCkSu62ZAArp0oHRV2g5Dkhz2R3C2DKYDH1jYe7nSdCpGpgLIFZ0zeueyUTK3Z7hE/640?from=appmsg)

三个 Profile 各自独立配置，模型、记忆、Gateway 完全隔离

> **编码助手**（coder）：专注代码审查、重构和 CI/CD，用 claude-sonnet-4，记忆里只存代码相关的上下文。
>
> **研究 Agent**（researcher）：论文检索、知识整理，换 DeepSeek-R1 做推理，记忆里只有文献笔记。
>
> **个人助理**（personal）：日程提醒、内容创作，用轻量的 claude-haiku，快而不贵。

## 04 | 进阶：每个 Agent 有独立 Gateway

这个功能我觉得最实用。**每个 profile 可以跑独立的 Gateway 进程**，配不同的 Telegram Bot Token——这意味着你可以有三个 Telegram bot，分别对应三个 Agent 角色。

# 在 coder profile 的 .env 里配置独立的 bot token
vim ~/.hermes/profiles/coder/.env
# 加入: TELEGRAM_BOT_TOKEN=your_coder_bot_token

# 启动 coder 的 Gateway
coder gateway start

# 或者后台运行
coder gateway install   # 安装为系统服务
系统会自动检测 token 冲突，防止两个 profile 抢同一个 bot。手机里三个不同的 Telegram bot，分别对应**「写代码的」「查资料的」「管日程的」**——找起来不费劲，也不会互相污染上下文。

## 05 | 几个实用细节

用下来几个细节值得注意：

**指定工作目录。**想让某个 profile 默认在特定项目里工作，在它的 config.yaml 里设置：

# ~/.hermes/profiles/coder/config.yaml
terminal:
  cwd: /path/to/your/project
**完整备份。**需要备份整个 Agent 状态（含记忆和会话历史），用 `--clone-all`：

hermes profile create backup --clone-all
**干净删除。**删除 profile 会同时停掉 Gateway、移除服务、清理命令别名和所有数据：

hermes profile delete old-bot
**隔离原理。**本质上是通过 HERMES_HOME 环境变量实现的。运行 `coder chat` 时，系统自动设置 `HERMES_HOME=~/.hermes/profiles/coder`，之后所有文件读写都限定在这个目录里——配置、密钥、记忆、技能库、cron 任务全部独立。

## 06 | 配合 Kanban 做真正的多任务

Profile 解决了「多个 Agent 怎么配置隔离」的问题，但多个 Agent 真正协同工作，还需要一个共享的任务队列。Hermes 的 Kanban 功能就是干这个的——**不同 profile 之间可以共享一块看板，推任务、认领、汇报进度。**

# 创建一个跨 profile 的看板
hermes kanban init myteam

# coder profile 认领编码任务
hermes -p coder kanban create "重构登录模块" --assign coder

# researcher profile 认领研究任务
hermes -p researcher kanban create "调研 GRPO 最新论文" --assign researcher

# 查看整体进度
hermes kanban list
三个 Agent 各自在自己的看板上推任务，互不干扰又能看到彼此进度。这才是 Profile + Kanban 组合使用的正确姿势。

我觉得这套机制最大的价值不在于"高效"，而在于**清洁**——每个 Agent 只知道它该知道的事。编码助手不会记得你昨天问研究 Agent 的论文，个人助理也看不到你项目里的技术债。长期用下来，每个 Agent 的记忆质量都会比混在一起高很多。

你现在是一个 Agent 干所有的事，还是已经拆分开了？欢迎评论区聊聊你的用法。

⭐点赞、转发、关注和推荐一键三连⭐
