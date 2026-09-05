---
type: github-repo-analysis
source: github_readme + docs/architecture/product-concepts.md + ROADMAP.md + docs/development/community-dev-agent-prompt.md
repo: tabtin-ai/TabTin
repo_url: https://github.com/tabtin-ai/TabTin
website: https://tabtin.com/
docs: /tabtin-ai/TabTin/blob/main/docs/
license: AGPL-3.0-only（商业授权需联系）
company: Shanghai Mofan Technology Co., Ltd. (larchiveai.com)
status: Public Preview（公开预览）
analyzed_date: 2026-09-05
analyzed_by: 小助（MiniMax-M3）
topics:
  - agent
  - multi-agent
  - collaboration
  - workspace
  - harness
  - pluggable
  - desktop
  - electron
  - django
  - celery
  - centrifugo
  - agpl
authors:
  - Shanghai Mofan Technology Co., Ltd.（上海魔帆科技）
title: TabTin — GitHub 仓库分析（人 + 多 Agent 协作工作空间）
description: 开源「人 + 多 Agent」协作平台。核心：5 大原则（过程可见/权限可控/结果可检查/工作可交接/责任有人承担） + 5 个核心概念（Organization / Workspace / Agent / App / Device） + 可插拔三层（部署者配置 / 开发者 Adapter / 用户扩展）覆盖模型/IM/存储/搜索/实时协作/工作应用/Agent Harness。
tags:
  - github-repo-analysis
  - multi-agent
  - collaboration
  - workspace
  - harness
  - pluggable
  - agent-runtime
  - task-handoff
  - agpl-warning
related:
  - "[[2026-06-12 - Hermes Desktop - Deep Research]]"
  - "[[2026-07-09 - Yuxi - Deep Research]]"
  - "[[2026-08-29 - Multica - Managed Agents Platform（Notion 链接还原）]]"
  - "[[2026-09-03 - PenguinHarness - GitHub 仓库分析]]"
---

# TabTin — GitHub 仓库分析

> 来源：https://github.com/tabtin-ai/TabTin（AGPL-3.0-only · Public Preview · 2026 年中由 Shanghai Mofan Technology 开源）
> 公司：Shanghai Mofan Technology Co., Ltd.（[larchiveai.com](https://larchiveai.com)） · 官网：[tabtin.com](https://tabtin.com/)

---

## 📌 一句话定位

**TabTin = 开源、生产级的「人 + 多 Agent」协作工作空间**——**不是**给开发者写 Agent 的开发框架，**而是**给「已经在用 Agent 干活」的个人和团队协作、接续、复用的工作平台。

> 它要回答的根本问题：
> **AI 提高了个人产出，却没有自动提高团队效率——一个人已经完成的工作，能不能直接成为下一位同事的起点？**

---

## ⚠️ 重要风险提示（开篇先看）

| 项 | 状态 | 含义 |
|---|---|---|
| **License** | **AGPL-3.0-only** | 商业产品**不能直接 fork / 修改 / 集成**。想用得联系 contact@larchiveai.com 谈单独商业授权 |
| **状态** | Public Preview | 核心链路可跑，但「不同组件成熟度不一致」，Community Server 主要本机运行 |
| **移动端** | 不提供独立 Agent 执行环境 | 必须依赖已配好的桌面端 + 设备绑定，电脑不在线就不能用 |
| **Project 能力** | ROADMAP「下一版本重点推进」 | 团队级功能还在建 |
| **可插拔** | 方向已确认，**实现未到位** | 当前替换默认模块仍需修改较多内部代码 |

> 🚨 **结论**：TabTin 的**代码不能直接进 Hermes/德勤 MVP 的商业仓库**（AGPL 传染）。
> ✅ **架构理念**（5 原则 + 5 概念 + 可插拔三层 + 任务续接）可以借鉴。
> 借鉴方式 = 重写实现，而不是 fork。

---

## 🧭 5 大原则（产品方法论）

TabTin 把所有设计收口到 5 条协作原则上：

| # | 原则 | 含义 |
|---|---|---|
| 1 | **过程可见** | Agent 怎么干、引用了什么、调用了什么，都可被检查 |
| 2 | **权限可控** | Agent 不会自动获得全部权限；交接不绕过资源权限 |
| 3 | **结果可检查** | 任务产出可被 Review、可被追溯 |
| 4 | **工作可交接** | 任务续接 + 交接包——已完成工作的复用 |
| 5 | **责任有人承担** | Agent 执行，但**重要判断、责任确认、结果验收仍由人完成** |

> 🔑 这 5 条与德勤 Agent 平台的「治理、合规、可审计」诉求**完全对位**——尤其第 2、4、5 条是咨询客户最关心的。

---

## 🧱 5 个核心概念（领域模型）

```
Organization（组织/租户）
└── Workspace（成员私有执行现场）
    ├── 工作根
    ├── 文件
    ├── 终端
    ├── Skill
    └── Checkpoint
└── Agent（AI 身份：角色/规则/模型/Skill/记忆/执行偏好）
└── App（工作应用：文档/表格/终端/浏览器/消息/集成）
└── Device（实际执行环境：终端/文件/浏览器/设备控制）
```

### 概念关键边界

| 概念 | 定义 | 关键边界 |
|---|---|---|
| **Organization** | 组织与租户边界 | 不同 Organization 默认隔离 |
| **Workspace** | 成员私有执行现场 | **每个 Workspace 只有一个执行根** |
| **Agent** | AI 身份 | **Agent 表示"谁参与"，不表示"在哪里执行"** ⭐ |
| **App** | 工作应用 | 人和 Agent 操作同一份 App 结果 |
| **Device** | 实际运行环境 | 必须遵守 Organization + 成员 + Workspace 权限 |

> ⭐ **最关键的架构原则**：**Agent ≠ 执行位置**。身份（Agent）和执行环境（Device）是两个独立概念。
> 这点和 Hermes/OpenClaw 的「可插拔执行器」思路一脉相承。

---

## 🔄 任务交接的两种方式

### 方式 A：任务续接（Handoff）
- 发送方把 Agent 任务**转交给同一 Organization 的成员**
- 系统**冻结可共享的必要会话上下文**
- 记录任务中引用的文档、表格、云端文件、本地文件
- 接收人**选择自己的 Agent 和 Workspace**，创建**独立的续接任务**
- 材料是否可用仍受**原资源权限约束**

### 方式 B：交接包（Handoff Bundle）
- 在团队会话中发送：**工作目标 + 当前进展 + 下一步 + 风险**
- 可引用 Agent 会话、相关消息、文档、表格
- 接收人**查看 / 确认 / 接手**

### 交接的硬约束（产品承诺）
- ❌ **不是**共享所有成员本地目录的远程文件系统
- ❌ **不是** Agent 自动获得全部权限
- ❌ **不是**绕过已有资源权限
- ✅ 双方本地环境保持独立
- ✅ 交接材料遵守 Organization + 资源权限

> 💡 借鉴价值：在 Hermes-based 德勤 MVP 里，「任务交接」是**组织控制**的核心动作之一——这部分设计可以直接参考。

---

## 🏗️ 架构组件（按部署栈）

| 组件 | 技术栈 | 说明 |
|---|---|---|
| **桌面客户端** | Electron | 主力入口，Agent Runtime 在这里 |
| **Web 平台** | tabtin-web（React?） | 浏览器入口，**全量预览**才启动 |
| **移动端** | iOS / Android | **配套入口**，**不能独立执行 Agent**——必须桌面端绑定 |
| **Community Server** | Django + Celery | 后端，社区版主要本机运行 |
| **实时协作** | Centrifugo（WebSocket 服务） | 多人协作 + 实时通知 |
| **Collab** | （协作服务） | 任务协作状态 |
| **Agent Runtime** | 内部实现（细节未公开） | Agent 执行框架 |
| **AdminDash** | 后台管理系统 | 运管后台 |

### 启动模式

| 模式 | 命令 | 启动内容 | 适用 |
|---|---|---|---|
| **快速预览** | `node scripts/dev.mjs community` | Community 后端 + Collab + Centrifugo + Electron | 桌面端开发 / 快速体验 |
| **全量预览** | `pnpm dev` | 后端 + AdminDash + tabtin-web + Electron | 完整本地联调、跨端验收 |
| **单服务调试** | `node scripts/dev.mjs backend/admindash/tabtin-web/electron` | 单服务 | 局部调试 |

> 🇨🇳 中国大陆网络环境：`node scripts/dev.mjs community --region cn`

---

## 🔌 ROADMAP 重点：可插拔体系（三层）

TabTin 自己承认「部分基础模块当前采用默认实现，开发者要替换为其他服务时，仍需修改较多内部代码」——所以建立了可插拔方向：

```
┌─────────────────────────────────────────┐
│ 第 1 层：部署者通过配置选择不同实现       │  ← 不写代码
├─────────────────────────────────────────┤
│ 第 2 层：开发者按统一接口编写 Adapter     │  ← 写适配器
├─────────────────────────────────────────┤
│ 第 3 层：用户/管理员可安装/启用/切换扩展  │  ← 装插件
└─────────────────────────────────────────┘
```

### 可插拔覆盖范围

| 模块 | 状态 | 备注 |
|---|---|---|
| **模型** | 方向 | 多 LLM Provider 切换 |
| **IM** | 方向 | 实时通讯后端可替换 |
| **存储** | 方向 | 文件/数据库后端 |
| **搜索** | 方向 | 向量/全文检索 |
| **实时协作** | 方向 | Centrifugo 可换 |
| **工作应用** | 方向 | 文档/表格/演示可换 |
| **Agent Harness** | 方向 ⭐ | **Agent 执行框架可插拔**——这个最关键 |

> 🔥 **Agent Harness 可插拔 = 和 MEMORY.md 里「执行器抽象层」完全吻合**
> 也就是：Hermes / OpenClaw / Codex / Claude Code 都可以作为可插拔的 Agent 执行器接进来。

---

## 🎯 与德勤 AI Native MVP / Hermes 的关联

### 直接可借鉴的 5 点

| # | 借鉴点 | 在 Hermes-based 德勤 MVP 里的落地位置 |
|---|---|---|
| 1 | **Agent ≠ 执行位置** | Hermes 的 Agent 配置（角色/规则/Skill/记忆）和 Device 配置（终端/文件/浏览器）必须**解耦存储**——这是设计前提 |
| 2 | **Agent Harness 可插拔** | 写一个 **Harness Adapter 接口规范**（继承、状态机、checkpoint、tool call），Hermes/OpenClaw/Codex 都能接 |
| 3 | **5 大原则作为验收清单** | 德勤 MVP 验收标准可以**直接抄这 5 条**——客户买账 |
| 4 | **任务续接 + 交接包** | Hermes 的组织控制核心动作：冻结上下文 + 引用资源 + 接收人独立任务 |
| 5 | **App = 人和 Agent 操作同一份** | 文档/表格/演示应用必须**双端可编辑**——不能搞"Agent-only 工作区" |

### 不要借鉴的 3 点

| # | 项 | 不借鉴原因 |
|---|---|---|
| 1 | **AGPL-3.0 协议** | 商业产品不能 fork。**架构理念可抄，代码一行不抄** |
| 2 | **Django + Celery 后端** | Hermes 走 Node.js 全栈。Django 引入需要跨语言协作 |
| 3 | **Centrifugo 实时协作** | Hermes 已有自己的实时通道方案 |

### 与现有研究的横向对比

| 项目 | 关系 |
|---|---|
| **Hermes Desktop** | Hermes 是德勤 MVP 的 Agent 框架；TabTin 的 Agent Harness 可插拔 = 给 Hermes 加 adapter |
| **Yuxi（AGENTS.md 范式）** | TabTin 的「5 原则」也是给 Agent 系统的设计约束——可以借鉴到 MEMORY.md |
| **Multica** | 同样是「多 Agent 协作平台」，但 Multica 偏 SaaS，TabTin 是自托管 + 开源 |
| **PenguinHarness** | PenguinHarness 是「用 Agent 构建 Agent」的开发平台；TabTin 是「人 + Agent 协作」的工作平台——**不是同一类** |

---

## 📊 关键指标速览

| 指标 | 值 |
|---|---|
| License | AGPL-3.0-only |
| 状态 | Public Preview（公开预览） |
| 公司 | Shanghai Mofan Technology Co., Ltd.（上海魔帆科技） |
| 官网 | tabtin.com |
| 后端 | Django + Celery |
| 实时协作 | Centrifugo |
| 桌面 | Electron |
| 移动 | iOS + Android（配套入口，不能独立执行） |
| Agent Runtime | 内部实现，细节未公开 |
| 商业授权 | contact@larchiveai.com |

---

## 🎯 借鉴清单（3 条硬约束）

> 来源：MEMORY.md「Goal-Driven Execution」准则——只写可立刻执行的借鉴动作

### 借鉴 1：把 TabTin 的 5 大原则**翻译**到 MEMORY.md（可执行版）
```text
1. 过程可见 — 每个 Agent 任务的引用、调用、产出都记日志
2. 权限可控 — Agent 默认最小权限，跨 Workspace 不共享执行根
3. 结果可检查 — 任何任务产物都可以被 Review
4. 工作可交接 — 任务续接 = 冻结上下文 + 引用资源 + 接收人独立任务
5. 责任有人承担 — Agent 不签字，人签
```
**验收**：MEMORY.md 加上「德勤 Agent 5 原则」章节，5 行内说清每条

### 借鉴 2：Harness Adapter 接口规范（可执行版）
- **输入**：Hermes 的 Agent 配置 + 用户的 prompt
- **输出**：可被 Hermes / OpenClaw / Codex 任何一种 Runtime 执行
- **核心抽象**：Agent（身份）+ Workspace（执行现场）+ Skill（能力）+ Checkpoint（状态）
- **验收**：写一份 `vault/1-Projects/德勤/AI-Native/executor/adapter-spec.md`，列出 4 个接口签名

### 借鉴 3：任务交接的「冻结上下文」数据模型（可执行版）
- 冻结字段：会话 ID + 引用的资源 ID + 已完成的 checkpoint
- 不冻结：本地执行目录 / 设备状态 / 临时文件
- 验收：在 `vault/1-Projects/德勤/AI-Native/handoff/` 下产出「交接数据 schema」JSON

---

## ❓ 还需要深入研究的问题

1. **Agent Runtime 具体怎么实现的？**——README 没暴露细节，需要看 `packages/` 源码
2. **可插拔层的接口规范长什么样？**——ROADMAP 只说方向，没看到接口定义
3. **Workspace 的 Checkpoint 怎么存？**——是文件快照还是状态机序列化？
4. **移动端为啥不能独立执行 Agent？**——技术限制 vs 产品策略？
5. **AGPL-3.0 商业授权价格区间？**——需要联系 larchiveai.com 询问

---

## 🔗 相关链接

- 主页：https://github.com/tabtin-ai/TabTin
- 官网：https://tabtin.com/
- 产品概念：https://github.com/tabtin-ai/TabTin/blob/main/docs/architecture/product-concepts.md
- ROADMAP：https://github.com/tabtin-ai/TabTin/blob/main/ROADMAP.md
- 本地开发指南：https://github.com/tabtin-ai/TabTin/blob/main/docs/development/community-dev-agent-prompt.md
- Community 快速开始：https://github.com/tabtin-ai/TabTin/blob/main/docs/development/community-quickstart.md
- Electron 开源开发：https://github.com/tabtin-ai/TabTin/blob/main/apps/tabtin-electron/docs/open-source-development.zh-CN.md
- 商业授权：contact@larchiveai.com

---

**分析人**：小助（MiniMax-M3） · **日期**：2026-09-05 · **何大人指示**：收到链接后默认存档到 vault + 分析
