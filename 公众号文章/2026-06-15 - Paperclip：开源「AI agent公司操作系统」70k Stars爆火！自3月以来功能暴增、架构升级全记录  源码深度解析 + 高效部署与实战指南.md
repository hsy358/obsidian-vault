---
title: "Paperclip：开源「AI agent公司操作系统」70k Stars爆火！自3月以来功能暴增、架构升级全记录 | 源码深度解析 + 高效部署与实战指南"
author: "如此才是"
publish_date: "2026-06-15 08:00:00"
saved_date: "2026-06-15"
source: "wechat"
url: "https://mp.weixin.qq.com/s/uGPC0eMDTEhB9f-cOx8zyQ"
type: wechat-article
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
  source_url: https://mp.weixin.qq.com/s/uGPC0eMDTEhB9f-cOx8zyQ
---
# Paperclip：开源「AI agent公司操作系统」70k Stars爆火！自3月以来功能暴增、架构升级全记录 | 源码深度解析 + 高效部署与实战指南
### 从「员工」到「公司」，Paperclip正在重新定义AI agent的规模化落地

26年3月10日，曾在公众号发布过#Paperclip#项目的首篇介绍文章（链接：[有潜力但仍处于早期高速成长期的“高风险高回报”-开源AI代理编排平台 paperclip 助力零人类公司 ](https://mp.weixin.qq.com/s?__biz=MzY5MTAxODQ1MQ==&mid=2247484114&idx=1&sn=e84de5c2a62ca900d742e60d3bb732ef&scene=21#wechat_redirect)）。那时它刚起步，核心是解决“如何把多个AI agent（OpenClaw、Claude Code、Codex、Cursor等）协调成一个有目标、有预算、有治理的团队”的问题。

短短3个月过去，项目发生了翻天覆地的变化：

●GitHub Stars从初期的数千迅速攀升至**70.3k**，Forks 13k+，社区贡献者124人，Discord和X上讨论火热。

●发布了从v2026.403到v2026.609.0等十多个版本，新增/强化了**插件系统**、**Skills Catalog & CLI**、**多用户协作**、**Company Artifacts**、**视频附件与文档注解**、**Grok Build / Cursor Cloud适配器**、**全公司搜索**、**i18n基础**、**可折叠侧边栏**、**结构化交互**等大量生产级功能。

●Roadmap中多项核心功能已落地（插件、技能管理、例行任务、多用户、预算优化、审查批准等），从“核心编排引擎”进化成“完整可扩展的AI公司控制平面”。

Paperclip的定位从未改变：**如果OpenClaw是“员工”，Paperclip就是“公司”**。它不是聊天机器人、不是单一agent框架、不是拖拽式工作流工具，而是**开源、自托管的#多agent编排与治理平台**。提供组织结构图（Org Chart）、目标对齐（Goal Alignment）、心跳机制（Heartbeats）、预算硬控制（Budget Control）、治理审批（Governance）、工单系统（Ticket/Issue System）、插件扩展等企业级能力，让你真正像管理一家公司一样管理AI agent团队。

**图：Paperclip系统架构总览**

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/ibibCVXCYh6IddSiblo3lZInP8zSZPJTsZPEe1HldgNWxF8gvKAdcTByXKSnws2QbapRsPb8Ld0elZ7g6Gib98WGfqMSl7L75czGQpEbQdvrkLg/640?wx_fmt=jpeg&from=appmsg)

### 一、核心功能

Paperclip的核心不是“多一个agent管理界面”，而是**解决了多agent规模化运行时最难的编排、状态、成本、治理问题**。

#### 1. Bring Your Own Agent（自带agent，任何能接收心跳的运行时即可入职）

●支持Claude Code、Codex、Cursor、OpenClaw（HTTP/Webhook）、Bash/CLI、Grok Build、Cursor Cloud等。

●新增/强化：Grok Build本地运行时适配器（v2026.517）、Cursor Cloud适配器（v2026.512）、Claude Local模型动态发现、ACPX-Claude权限尊重改进。

●实现机制：通过`tools/agent-shim/`提供沙箱运行时shim；本地适配器要求CLI工具在PATH中；云适配器通过API集成。**只要能接收心跳（heartbeat），就能被“雇佣”**。

#### 2. Org Chart & Agents + Goal Alignment（组织结构图 + 目标对齐）

●agent有角色、头衔、汇报线、权限、预算、Job Description。

●每个任务（Issue）携带完整的**目标祖先链（goal ancestry）**：Company Mission → Project Goal → Agent Goal → Task。

●agent通过运行时注入的`SKILL.md`上下文，始终知道“为什么做这件事”。

#### 3. Heartbeats & Routines（心跳 + 例行任务）

●**DB-backed wakeup queue with coalescing**：数据库驱动的唤醒队列，支持合并、预算检查、工作区解析、密钥注入、技能加载、适配器调用。

●agent按计划（如Copywriter每4小时、SEO Analyst每8小时）或事件（任务分配、@-mention）唤醒。

●Routines（例行任务）：支持cron、webhook、API触发，带并发和追赶策略。每次执行创建可追踪的Issue并唤醒指定agent。

●持久化状态：agent跨心跳恢复相同任务上下文，而非从头开始（liveness continuations + orphaned run recovery）。

#### 4. Ticket / Issue System（工单系统，生产级任务管理）

●Issues支持：公司/项目/目标/父子链接、原子检出（atomic checkout + execution locks）、 blocker依赖（自动wake-on-resolution）、子Issue checklist、长线程虚拟化、聊天式线程（带头像和转录）、视频附件（inline预览 + PWA控制，v2026.609新增）、富文本文档、标签、收件箱状态（Mine tab、blocked inbox、swipe-to-archive）。

●新增：Source-scoped recovery actions、successful-run handoff通知、Planning Mode、Issue References（反向链接）、Document Locks（快照保护）。

●完整工具调用、API请求、决策追踪 + **不可变审计日志**。

#### 5. Governance & Approvals + Execution Policies（治理与审批）

●用户作为“董事会”：批准雇佣、覆盖策略、暂停/恢复/终止agent、调整预算、审批执行策略（多阶段review/approval workflows）。

●结构化交互：proposals、forms、checkbox confirmation payloads（v2026.609强化，一致API/UI/CLI验证）。

●所有变更可回滚，配置带修订历史。

#### 6. Budget & Cost Control（预算与成本硬控制，防止跑飞）

●每月每agent预算，80%软警告，100%硬停止（auto-pause + cancel queued work）。

●原子性保障：Task checkout和budget enforcement使用事务（atomic），杜绝double-work和超支。

●细粒度追踪：按company/agent/project/goal/issue/provider/model统计token与成本。

●新增：Routines携带独立secrets（带修订和安全元数据）。

#### 7. Workspaces & Runtime + Plugins & Skills（工作区、插件、技能）

●工作区：项目级覆盖默认``

`~/.paperclip/instances/default/workspaces/<agent-id>`；支持git worktrees、operator branches；运行时服务（dev server、preview URL）。

●**Skills Catalog**（v2026.529首发为first-class）：`packages/skills-catalog/`提供bundled/optional分类的`SKILL.md`，运行时注入，无需重训。CLI支持install/reset/audit/export/assignment + Board UI + provenance模型。

●**Plugin System**（从v2026.416 beta到成熟）：实例级插件，out-of-process workers，capability-gated host services（scoped DB、API、UI构建块），支持本地开发脚手架 + watcher。插件可拥有独立DB schema，备份包含插件数据。

●新增：Modal Sandbox Provider（CI发布、冷启动超时）、Workspace Diffs查看器（split/unified）、Secrets Provider Vaults（AWS Secrets Manager导入 + 轮换保护）。

#### 8. Multi-Company Isolation + Portability + Artifacts（多公司隔离 + 可移植 + 产物管理）

●每个实体严格company-scoped，一次部署运行多个完全隔离的公司。

●Company Portability：export/import整个组织

（agents/skills/projects/routines/issues），带secret scrubbing和冲突处理（companies.sh已实现）。

●**Company Artifacts**（v2026.609重磅新增）：公司级Artifacts页面，索引agent产出的文件/媒体/文档，按任务堆栈分组，支持上传、富播放（视频缩略图）、PWA控制。

#### 9. 其他生产增强（UI/UX/可观测性）

●移动端就绪、可折叠侧边栏（持久化rail + hover peek，v2026.609）、全公司模糊搜索（issues/documents/agents/activity + snippets）、Inline Document Annotations（修订感知讨论线程）、i18n groundwork、OpenTelemetry tracing（opt-in，仅traces，通过`OTEL_EXPORTER_OTLP_ENDPOINT`激活）、匿名遥测（可通过`PAPERCLIP_TELEMETRY_DISABLED=1`或config完全关闭）。

●新UI：富Issue附件（视频）、结构化checkbox交互、信息架构刷新（项目/agent表面、实例设置移至公司设置）。

**图：Paperclip核心功能卡片**

![](https://mmbiz.qpic.cn/mmbiz_jpg/ibibCVXCYh6Idg9J7B3KyTcFX01OEb2nVMnFOrtXBqR9D2JttZiaUb4YezfzTIcJFzsbB3kIfuNSaeYwZlB7QsolXpQOfsjVADvT9lJ67Ia92E/640?wx_fmt=jpeg&from=appmsg)

### 二、安装方法

#### 推荐快速开始（npx，一键onboard）

```
●●●bashnpx paperclipai onboard --yes
```

●默认trusted local loopback模式，自动创建embedded PostgreSQL，启动服务器于`http://localhost:3100`。

●认证/私有模式：

```
●●●bashnpx paperclipai onboard --yes --bind lan  # 或  npx paperclipai onboard --yes --bind tailnet
```

●私有npm registry问题 workaround：

```
●●●bashnpx --registry https://registry.npmjs.org paperclipai onboard --yes
```

#### 源码安装与开发（推荐深度用户）

```
●●●bashgit clone https://github.com/paperclipai/paperclip.gitcd paperclippnpm install          # Node 20+ + pnpm 9.15+pnpm dev              # 同时启动API + UI（watch模式），http://localhost:3100# 或pnpm dev:server       # 仅serverpnpm dev:once         # 无watch，自动应用migrationspnpm paperclipai run  # 一键运行（自动onboard + health check + repair）
```

**数据库与配置**：

●默认embedded PostgreSQL（数据在``

`~/.paperclip/instances/default/db`），无需手动安装。

●生产用外部Postgres：设置`DATABASE_URL`。

●自动逻辑备份（每60min，保留30天）：``

`~/.paperclip/instances/default/data/backups`。

●手动备份：`pnpm paperclipai db:backup`。

●重新配置：`paperclipai configure`（支持--section database/storage等）。

**Worktree支持**（多实例开发神器）：

```
●●●bashpaperclipai worktree init# 或创建带实例的新worktreepnpm paperclipai worktree:make paperclip-pr-432
```

自动创建隔离的`.paperclip/config.json`、实例目录、唯一端口，避免DB冲突。

**其他常用命令**：

●`pnpm build / typecheck / test / test:e2e / db:generate / db:migrate`

●`paperclipai configure`、`paperclipai db:backup`

### 三、高效使用方法与最佳实践

1.**定义清晰的目标层级**：先在Company设置Mission，再建Project/Goal，任务自动继承祖先上下文。

2.**hireagent**：通过UI或API添加agent → 选择适配器 → 设置预算、角色、汇报线 → 注入对应`SKILL.md`（Skills Catalog提供开箱即用模板）。

3.**创建任务**：Issue支持子任务、blocker、文档附件（现支持视频 + 注解）。使用Planning Mode做前置规划。

4.**例行工作**：用Routines配置cron/webhook触发，自动创建Issue并唤醒agent，无需人工kick-off。

5.**成本控制**：严格设置每月预算，监控Dashboard上的per-agent/project/goal花费。原子保障让你放心放手。

6.**治理流程**：对高风险操作（如部署、预算调整）开启Execution Policies多阶段审批。利用Pause/Resume/Terminate随时干预。

7.**多用户协作**：支持First-Admin Claim + invite flows，适合团队或“董事会”模式。

8.**产物管理**：agent生成的文件/视频/文档自动进入Company Artifacts页面，支持按任务分组和富预览。

9.**扩展**：用Skills Catalog管理上下文，用Plugin System添加知识库、自定义追踪、队列等（无需fork核心）。

10.**移动/远程**：Tailscale + Mobile Ready Dashboard，随时随地管理“公司”。

**避坑建议** ：

●心跳依赖稳定网络/DB；使用worktree时注意seeding模式（minimal/full）。

●插件/本地适配器开发时启用`allowLocalPathSources`（仅dev）。

●遥测默认开启，生产建议显式关闭。

●大量Issues时开启密度控制 + 虚拟化列表。

### 四、技术原理与架构

**整体架构**（见上图）：

●**Monorepo**：pnpm workspace，核心`server/`（Node.js API + 业务逻辑）、`ui/`（React + Storybook）、`packages/`（@paperclipai/skills-catalog、teams-catalog、routines等）、`skills/`、`tools/agent-shim/`。

●**数据库**：PostgreSQL（embedded或external），所有核心实体严格company-scoped，实现真·多租户隔离。

●**服务器**：健康检查`/api/health`，公司列表等REST API；集成OpenTelemetry（traces only）。

●**心跳执行引擎**（核心难点）：

○DB-backed wakeup queue + coalescing。

○每次心跳：预算检查 → 工作区解析 → 密钥/技能注入 → 适配器调用 → 结构化日志 + cost event + session state + audit trail记录。

○恢复机制：liveness continuations记录中断状态；orphaned run自动恢复。

●**原子性保障**：Task checkout、budget enforcement使用数据库事务，彻底杜绝重复执行和超支。

●**运行时技能注入**：`SKILL.md`（markdown + assets/scripts）在心跳时动态加载到agent上下文，无需模型重训。Catalog支持验证、manifest构建、trust level（markdown_only / assets / scripts_executables）。

●**插件系统**：out-of-process workers + capability-gated host services（scoped DB/API/UI）。插件可声明自己的schema，备份自动包含。CLI提供本地开发脚手架。

●**工作区与隔离**：默认`~/.paperclip/instances/default/...`，支持per-company Codex home、git worktrees、project-specific workspace覆盖。secrets使用local_encrypted或外部provider（AWS Secrets Manager）。

●**可观测与遥测**：opt-in OpenTelemetry；匿名usage telemetry（hash repo路径 + per-install salt），可完全禁用。

●**UI/前端**：React，近期优化了长列表虚拟化、scroll pinning、collapsible rail、video playback、annotations等。

**为什么“特殊”** ：

●Atomic execution + Persistent agent state + Runtime skill injection + Governance with rollback + Goal-aware execution + Portable company templates + True multi-company isolation。

这些特性在源码中通过严格的DB scoping、事务边界、revisioned config、recovery routines实现，远非简单“任务队列 + dashboard”。

**图：2026年3月以来重大里程碑时间线**

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/ibibCVXCYh6Id2Sf1L1jvwd9Krg16ISIFsV5iboPQOZNOnXe0Rul1Vpe02iaN0iaDlic9HMrUcz2QBRF6ulkcBXBpY43deb0L8dJ7JHqyPORp0b3c/640?wx_fmt=jpeg&from=appmsg)

### 五、自3月10日以来项目发展与进步点

自3月以来，Paperclip以惊人速度迭代（几乎每周有实质更新）：

●**4月**：Inbox全面重构（Mine tab、keyboard shortcuts、swipe）、Issue Chat Thread + 结构化交互、Execution Policies多阶段审批、Blocker Dependencies自动唤醒、Plugin System初版、Multi-User Access + invite flows、Sub-Issue Checklists、Long Issue Threads虚拟化、Pause/Resume Agents、Productivity Review自动生成 stalled work issue。

●**5月**：Skills Catalog & CLI（install/reset/audit/export + Board UI）、Grok Build Adapter全支持、Cursor Cloud Adapter、Workspace Diffs查看器、Modal Sandbox Provider、Routines with Secrets + revision history、Local Cloud Upstream Sync、Full Company Search + fuzzy + snippets、Planning Mode、Blocked Inbox Tab、Source-scoped Recovery Actions、Issue Document Locks、Scalable Issues Board（density controls）、i18n groundwork、Local Plugin Development scaffolding。

●**6月（最新v2026.609）**：Company Artifacts页面（文件/媒体/文档索引 + 任务分组 + 上传 + 富播放）、Collapsible Sidebar Rail、Rich Video Attachments（inline预览）、Checkbox Confirmation Interactions、Information Architecture Refresh、Automated PR Quality/Security Gates（commitperclip）。

**总体进步**：从“能跑多agent”的核心引擎 → 具备**完整内容管理（Artifacts + Annotations）、强扩展性（Plugins + Skills first-class）、生产协作（Multi-User + Search + Video）、治理闭环（Approvals + Recovery）、UI/UX成熟（Linear-like polish）**的平台级产品。社区生态（awesome-paperclip）也在快速成长。

**Roadmap剩余亮点**（部分已接近）：Memory/Knowledge、Self-Organization、Automatic Organizational Learning、CEO Chat、Cloud deployments、Desktop App、MAXIMIZER MODE等。核心策略是“thin core + rich edges via plugins”。

Paperclip已经从一个有潜力的想法，进化成**目前开源世界里最务实、最深入的多AI agent公司级编排平台**。真正解决了“20个Claude Code标签页失控”“成本跑飞”“上下文丢失”“缺乏治理”的痛点，同时保持了极高的可扩展性和自托管自由度。

如果你正在用OpenClaw、Claude Code、Cursor等构建AI工作流，或者想尝试**零人工/低人工的AI公司**，强烈建议现在就`npx paperclipai onboard --yes`跑起来。结合之前的文章（3月10日版），你会看到这3个月项目在功能深度、工程成熟度、社区势能上的巨大飞跃。

**推荐阅读顺序**：

1.快速onboard跑起来（10分钟）

2.阅读本文 + 官方Docs + DEVELOPING.md

3.尝试Skills Catalog + 自定义Plugin

4.部署生产实例 + 连接真实业务目标

**—— 如此才是**

**把复杂的技术，讲成你真正能用上的生产力**

**零基础也能玩转卫星！开源Ground Station + SDR 打造个人地面站全攻略**

**OpenClaw & Hermes刷屏后，GitHub  Mercury Agent如何打动用户？ 灵魂驱动+权限铁闸+24/7永动 vs 两大竞品**

**苹果M系列芯片的福音！无需H100、无需云GPU，本地MacBook就能微调Gemma 4多模态模型**

**开源Minecraft终极杀手！12.7K星GitHub神器Luanti（原Minetest）完整中文攻略：零基础安装、2800+模组随便玩、服务器+源码编译**

**AI 直接操控 Unity/Godot/Unreal 编辑器！用 OpenClaw + TomLeeLive 插件，聊天就能把你的游戏梦想变成现实**

[开源项目Paseo，AI编码代理跨设备统一指挥中心：统管Claude Code、Codex、OpenCode（以及Copilot、Pi等）](https://mp.weixin.qq.com/s?__biz=MzY5MTAxODQ1MQ==&mid=2247484927&idx=1&sn=b4d7d4aed5a5ad7263bff54b50c395a5&scene=21#wechat_redirect)

[老婆/女朋友每天早上纠结45分钟穿什么？GitHub 开源AI衣柜神器 Wardrowbe 彻底解放！完整自托管安装+使用教程](https://mp.weixin.qq.com/s?__biz=MzY5MTAxODQ1MQ==&mid=2247484594&idx=1&sn=2a9832be4fd2b3d423f9c62fbae5b0a3&scene=21#wechat_redirect)

[Notebook LM平替，开源Open Notebook：隐私零泄露、18+AI模型随意切、1-4人定制播客秒生成](https://mp.weixin.qq.com/s?__biz=MzY5MTAxODQ1MQ==&mid=2247484913&idx=1&sn=a3307c1fb6b981881b22ca1c1ca407e2&scene=21#wechat_redirect)

[30MB Rust无头浏览器Obscura：击败Chrome、V8真实JS+CDP全兼容，AI Agent与爬虫的隐形核武器](https://mp.weixin.qq.com/s?__biz=MzY5MTAxODQ1MQ==&mid=2247485078&idx=1&sn=84152e9774e0eab3d16839db3a7657de&scene=21#wechat_redirect)

[Rust重写的jcode：性能碾压Cursor Claude Code 139倍的下一代Coding Agent Harness，人类级内存图谱+多会话Swarm](https://mp.weixin.qq.com/s?__biz=MzY5MTAxODQ1MQ==&mid=2247485066&idx=1&sn=2a563ec1e199af1807b6541f91d0842b&scene=21#wechat_redirect)

[Warp开源震撼发布！5年Rust GPU终端+Oz Agentic开发环境完整拆解：功能全览、源码编译教程、核心架构深度解析](https://mp.weixin.qq.com/s?__biz=MzY5MTAxODQ1MQ==&mid=2247485052&idx=1&sn=f612497afd348acd327221233af635c2&scene=21#wechat_redirect)
