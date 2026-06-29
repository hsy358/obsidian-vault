---
type: research-report
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: openclaw-2026-06-28
title: Paperclip — GitHub 仓库研究
description: 1. Project Overview 2. Core Concepts 3. Feature Breakdown 4. Architecture 5. Deployment 6. Comparison with OpenAgents 7. Deloitte Fit Analysis 8. Strengths & Limitations 9. Quick Reference
tags:
- AI
- Agent
- Multi-Agent
- Orchestration
- Enterprise
- OpenSource
- Apache-2.0
- Paperclip
source:
  url: https://github.com/paperclipai/paperclip
  fetched: 2026-06-28T08:00+08:00
  by: 小助 via web_fetch
---

# Paperclip — GitHub 仓库研究

**Date:** 2026-06-28  
**Prepared for:** 何大人 · Internal Research  
**Sources:** https://github.com/paperclipai/paperclip · https://paperclip.ing · https://docs.paperclip.ing

---

## 1. Project Overview

**Paperclip**（`paperclipai/paperclip`）是一个 **Apache 2.0 开源的 AI Agent 编排平台**，核心理念一句话概括：

> **"If OpenClaw is an employee, Paperclip is the company."**

如果说 OpenClaw 是一个 AI 员工，Paperclip 就是管理这些员工的**公司**。它不构建 agent，而是把已有的 agent（OpenClaw、Claude Code、Codex、Cursor 等）组织成有职级、有预算、有目标、有治理的公司结构。

### 核心定位

| 维度 | 说明 |
|---|---|
| **不是** | Chatbot / Agent 框架 / 工作流构建器 / 单 Agent 工具 / 代码审查工具 |
| **是** | Agent 公司控制平面——组织架构、预算、治理、任务分配、心跳调度、审计 |
| **目标用户** | 需要协调多个 AI Agent 24/7 运转的团队（20+ tabs 的重度用户） |

### 基本信息

| 项目 | 信息 |
|---|---|
| **GitHub** | https://github.com/paperclipai/paperclip |
| **官网** | https://paperclip.ing |
| **文档** | https://docs.paperclip.ing |
| **最新版本** | v2026.626.0（2026-06-26，昨天刚发布） |
| **最近 commits** | 122 条（活跃开发中） |
| **License** | Apache 2.0 |
| **技术栈** | TypeScript, React, Node.js, Python (SDK) |
| **维护方** | paperclipai 独立团队（非大厂背书） |
| **Stars** | 活跃开发中 |

---

## 2. Official Description（英文原文）

> "Open-source orchestration for teams of AI agents.
>
> Paperclip is a Node.js server and React UI that orchestrates a team of AI agents to run a business. Bring your own agents, assign goals, and track work and costs from one dashboard.
>
> It looks like a task manager. Under the hood: org charts, budgets, governance, goal alignment, and agent coordination.
>
> Manage business goals, not pull requests."

---

## 3. Core Concepts

### 3.1 公司隐喻（The Company Metaphor）

Paperclip 用真实公司的运作方式来组织 AI Agent：

```
公司使命（Company Mission）
  └── 目标（Goals）
        └── 项目（Projects）
              └── 任务（Issues）
                    └── Agent 执行（Agent Work）
```

每个任务都追溯到公司使命，Agent 始终知道自己**在做什么、为什么做**。

### 3.2 组织架构（Org Chart）

- Agent 有职级、头衔、汇报线、权限和预算
- 支持任意类型的 Agent：Claude Code、Codex、CLI agents（Cursor/Gemini/bash）、HTTP/webhook bots（OpenClaw）、外部 adapter 插件
- **"If it can receive a heartbeat, it's hired."** — 能接收心跳的都能雇佣

### 3.3 心跳机制（Heartbeat Execution）

- Agent 按调度计划唤醒、检查工作、执行任务
- 委托流在组织架构中上下流动
- 关键保障：原子执行（无重复工作）、持久化 Agent 状态（跨心跳恢复上下文）

### 3.4 预算管理（Budget & Cost Control）

- 按 Agent、项目、目标、任务维度追踪 token 和成本
- 每月预算上限，触达后自动停止 Agent
- 预警阈值 + 硬性停止，防止费用失控

### 3.5 治理与审批（Governance & Approvals）

- 审批工作流：任务需要上级 board 审核
- 执行策略：review → approval 多阶段
- 决策追踪、Agent 暂停/恢复/终止
- 完整审计日志（不可变）

### 3.6 多公司隔离（Multi-Company Isolation）

- 单实例部署可运行无限数量的公司
- 公司间数据完全隔离，审计轨迹独立
- 公司可导出/导入（secret 擦除 + 冲突处理）

---

## 4. Feature Breakdown

### 4.1 已完成功能（✅）

| 功能 | 说明 |
|---|---|
| Plugin 系统 | 实例级插件，进程外 worker，支持能力门控宿主服务 |
| OpenClaw 接入 | 官方支持 OpenClaw / claw-style agent 作为员工 |
| 公司导入/导出 | `companies.sh` 脚本，整组织迁移 |
| AGENTS.md 配置 | 易于理解的 agent 配置文件 |
| Skills Manager | Agent 技能管理 |
| 定时任务 | Cron/webhook/API 触发的周期性任务 |
| 预算管理 | Token/成本追踪与硬性停止 |
| Agent 审批 | Review & Approval 阶段 |
| 多人用户 | 多人共享 board 访问 |

### 4.2 Roadmap 中的功能（⚪）

| 功能 | 状态 |
|---|---|
| Cloud / Sandbox agents（Cursor / e2b / Novita） | 规划中 |
| Artifacts & Work Products | 规划中 |
| Memory / Knowledge | 规划中 |
| Enforced Outcomes | 规划中 |
| MAXIMIZER MODE | 规划中 |
| Deep Planning | 规划中 |
| Work Queues | 规划中 |
| Self-Organization | 规划中 |
| Automatic Organizational Learning | 规划中 |
| CEO Chat | 规划中 |
| Cloud Deployments | 规划中 |
| Desktop App | 规划中 |

---

## 5. Technical Architecture

### 5.1 系统架构图

```
┌──────────────────────────────────────────────────────────────┐
│ PAPERCLIP SERVER                                             │
│                                                              │
│ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐     │
│ │Identity & │ │ Work &    │ │Heartbeat  │ │Governance │     │
│ │ Access    │ │ Tasks     │ │Execution  │ │& Approvals│     │
│ └───────────┘ └───────────┘ └───────────┘ └───────────┘     │
│                                                              │
│ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐     │
│ │ Org Chart │ │Workspaces │ │ Plugins   │ │ Budget    │     │
│ │ & Agents  │ │ & Runtime │ │           │ │ & Costs   │     │
│ └───────────┘ └───────────┘ └───────────┘ └───────────┘     │
│                                                              │
│ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐     │
│ │ Routines  │ │ Secrets & │ │ Activity  │ │ Company   │     │
│ │& Schedules│ │ Storage   │ │ & Events  │ │Portability│     │
│ └───────────┘ └───────────┘ └───────────┘ └───────────┘     │
└──────────────────────────────────────────────────────────────┘
   ▲           ▲           ▲           ▲
┌─────┴─────┐ ┌─────┴─────┐ ┌─────┴─────┐ ┌─────┴─────┐
│  Claude   │ │  Codex    │ │   CLI     │ │  HTTP/    │
│   Code    │ │           │ │  agents   │ │  webhook  │
│           │ │           │ │           │ │    bots   │
└───────────┘ └───────────┘ └───────────┘ └───────────┘
                                                       ↑
                                                   OpenClaw
```

### 5.2 控制平面模块

| 模块 | 职责 |
|---|---|
| **Identity & Access** | 双部署模式（trusted local / authenticated），board 用户，Agent API keys，短期 run JWTs，公司成员关系，邀请流程，OpenClaw 接入 |
| **Org Chart & Agents** | Agent 角色/头衔/汇报线/权限/预算；支持 Claude Code、Codex、CLI agents、HTTP bots、外部 adapter |
| **Work & Task System** | Issue 含公司/项目/目标/父级链接，原子 checkout + 执行锁，一级 blocker 依赖，评论/文档/附件/标签/收件箱状态 |
| **Heartbeat Execution** | DB 后端唤醒队列（含合并），预算检查，workspace 解析，secret 注入，skill 加载，adapter 调用；生成结构化日志、成本事件、会话状态、审计轨迹 |
| **Workspaces & Runtime** | 项目 workspace，隔离执行 workspace（git worktrees），运行时服务（dev servers、preview URLs） |
| **Governance & Approvals** | Board 审批工作流，执行策略含 review/approval 阶段，决策追踪，预算硬性停止，Agent 暂停/恢复/终止，完整审计日志 |
| **Budget & Cost Control** | 按公司/Agent/项目/目标/Issue/provider/model 追踪 token 和成本；预警阈值 + 硬停止 |
| **Routines & Schedules** | Cron/webhook/API 触发的周期性任务；并发和 catch-up 策略 |
| **Plugins** | 实例级插件系统，进程外 worker，能力门控宿主服务，作业调度，工具暴露，UI 贡献 |
| **Secrets & Storage** | 实例和公司级 secrets，加密本地存储，provider 后端对象存储，附件和工作产出 |
| **Activity & Events** | 变更操作、心跳状态变更、成本事件、审批、评论、工作产出记录为持久活动 |
| **Company Portability** | 整组织导出/导入——agents/skills/projects/routines/issues，含 secret 擦除和冲突处理 |

### 5.3 技术栈

```
前端:    React + TypeScript
后端:    Node.js（API Server）
数据库:  PostgreSQL（本地开发用 embedded；生产用外置）
CLI:     Python SDK + TypeScript SDK
部署:    Docker 支持
可观测性: OpenTelemetry（opt-in，需装 @opentelemetry/* peer deps）
```

---

## 6. Deployment Assessment

### 6.1 快速启动

```bash
# 方式 1: npx 一键（推荐，本地模式）
npx --registry https://registry.npmjs.org paperclipai onboard --yes

# 方式 2: Git clone + pnpm
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pnpm install
pnpm dev   # 启动 API server at http://localhost:3100
```

**要求：** Node.js 20+，pnpm 9.15+

### 6.2 部署模式

| 模式 | 说明 |
|---|---|
| **本地开发** | 单 Node.js 进程 + embedded Postgres + 本地文件存储，无需任何配置 |
| **生产模式** | 对接自己的 Postgres，任意 Node.js 部署方式 |
| **远程访问** | Tailscale 模式（solo 用户手机访问），或 LAN 模式 |
| **Docker** | 支持 Docker 部署 |

### 6.3 与 OpenClaw 的集成方式

Paperclip 通过 **HTTP/webhook adapter** 将 OpenClaw 接入为 Agent：

```
Paperclip 控制平面
  └── HTTP Adapter → OpenClaw（作为公司员工）
        └── OpenClaw 的 skills / memory / tools 全都可用
```

关键路径：OpenClaw 本身支持 webhook 触发和 HTTP 工具调用，天然适配 Paperclip 的 adapter 架构。

### 6.4 自托管评估

| 维度 | 评分 | 说明 |
|---|---|---|
| **自托管难度** | 🟢 低 | 一行命令 `npx paperclipai onboard --yes`，embedded DB 无依赖 |
| **数据控制** | 🟢 高 | 完全自持，无云服务依赖 |
| **多人协作** | 🟡 中 | 已有多人用户支持，但共享 board 体验待完善 |
| **规模化** | 🟡 中 | 单实例多公司隔离；大规模多团队有待验证 |
| **运维成本** | 🟢 低 | Docker + Postgres 标准栈 |

---

## 7. 与德勤方案的匹配度分析

### 7.1 德勤 AI-Native 评估框架回顾

基于德勤《AI-Native 商业化白皮书》的组织控制平面需求：

| 维度 | 德勤需求 | Paperclip 现状 | 匹配度 |
|---|---|---|---|
| **组织树** | 层级结构/角色/汇报线 | ✅ Org Chart & Agents 模块完整支持 | 🟢 高 |
| **目标管理** | 目标对齐 / 任务分解 | ✅ Goals → Projects → Issues 链路完整 | 🟢 高 |
| **心跳机制** | 定时唤醒 / 状态保持 | ✅ Heartbeat Execution 模块，DB-backed 唤醒队列 | 🟢 高 |
| **预算管理** | 成本追踪 / 硬性停止 | ✅ Budget & Cost Control 模块，token 预算 + 硬停止 | 🟢 高 |
| **任务分配** | Issue 系统 / 原子 checkout | ✅ Work & Task System，atomic checkout + 执行锁 | 🟢 高 |
| **治理审计** | 审批流 / 不可变日志 | ✅ Governance & Approvals + Activity & Events | 🟢 高 |
| **多人协作** | 多用户 / 权限隔离 | ✅ 已支持多人用户 + Board 访问 | 🟡 中（体验待完善） |
| **SSO** | 企业级身份认证 | ⚪ 未来规划（路线图无明确时间线） | 🟡 待观察 |
| **Plugin 生态** | 可扩展性 | ✅ Plugin 系统完整，支持自定义 tracing/queues 等 | 🟢 高 |
| **多公司隔离** | Portfolio 管理 | ✅ Company Portability，单实例多公司完全隔离 | 🟢 高 |

### 7.2 关键优势

1. **完整公司模型**：Paperclip 是目前最完整实现"Agent 即公司员工"理念的平台
2. **OpenClaw 头号支持**：官方明确支持 OpenClaw 作为 Agent 类型，接入最简单
3. **预算硬性停止**：彻底解决多 Agent 并行运行时的 token 费用失控问题
4. **原子执行**：Issue checkout + 执行锁，从架构上杜绝重复工作

### 7.3 潜在顾虑

1. **SSO 缺失**：企业级客户强需求的 SSO 未上线，路线图无明确时间线
2. **Cloud Deployments 规划中**：大规模云端部署方案尚未成熟
3. **生态成熟度**：独立团队维护，插件生态（awesome-paperclip）仍在早期
4. **OpenTelemetry 需手动安装**：可观测性为 opt-in，默认不开启

---

## 8. 使用建议

### 8.1 最佳场景

| 场景 | 建议 |
|---|---|
| **多 Agent 并行管理（20+ tabs）** | ⭐ 核心场景，Paperclip 为此而生 |
| **AI 公司自动化运营** | ⭐ CEO → CTO → 工程师 → 设计师 → 营销，完整 org chart |
| **成本敏感的多 Agent 部署** | ⭐ 预算硬停止，token 追踪到每个 Issue |
| **需要治理和审计的企业** | ⭐ 不可变审计日志 + 审批流 |
| **Solo 开发者** | ⚠️ 可能过度工程，单个 OpenClaw 够用 |

### 8.2 与 OpenAgents 的关系

| 维度 | Paperclip | OpenAgents |
|---|---|---|
| **定位** | Agent 公司管理（自上而下） | Agent 协作平台（横向协作） |
| **核心模型** | 公司 org chart + 预算 + 治理 | Workspace + Thread + 共享文件/浏览器 |
| **Agent 角色** | 员工（受雇于公司） | 协作参与者（平等的会话成员） |
| **协作粒度** | 任务分配 + 审批 + 审计 | 即时消息 + @mention + 共享上下文 |
| **多 Agent 调度** | 心跳驱动 + 预算控制 | 按需拉入会话 |

**两者互补**：Paperclip 负责"谁该干什么、预算够不够"；OpenAgents 负责"Agent 之间怎么实时协作"。

### 8.3 推荐探索路径

```
1. [立即] 用 npx paperclipai onboard --yes 本地跑起来（5 分钟）
2. [本周] 配置 OpenClaw 作为 Agent 员工，体验 Org Chart + 心跳
3. [下周] 配置一个多 Agent 公司结构，测试预算硬停止
4. [长期] 关注 SSO + Cloud Deployments 路线图更新
```

---

## 9. Strengths, Weaknesses & Known Limitations

### ✅ 强项

1. **公司级 Agent 编排**：目前最完整的"Agent 即员工"建模，含 org chart、预算、审批、审计
2. **OpenClaw 头号支持**：官方接入最顺畅，AGENTS.md 配置风格一致
3. **预算控制扎实**：token 追踪 + 硬性停止，从架构上防止费用失控
4. **原子执行设计**：Issue checkout + 执行锁，无重复工作
5. **自托管友好**：一行命令启动，无需外部依赖
6. **多公司隔离**：单实例管理多个完全隔离的公司 portfolio
7. **Plugin 系统**：可扩展，不需 fork 核心代码

### ⚠️ 弱项 / 风险

1. **SSO 未实现**：企业客户强需求，路线图无明确时间线
2. **Cloud Deployments 在路上**：大规模云端部署方案未成熟
3. **独立团队维护**：无大厂背书，长期可持续性需观察
4. **可观测性默认关闭**：OpenTelemetry 需手动装 peer deps
5. **多 Agent 协作体验弱**：设计以任务指派为主，实时协作不如 OpenAgents

### ❓ 待观察

- SSO 上线时间线
- Cloud Deployments 进展
- 插件生态（awesome-paperclip）活跃度
- 与 OpenClaw 的深度集成案例

---

## 10. Quick Reference

| 项目 | 信息 |
|---|---|
| **GitHub** | https://github.com/paperclipai/paperclip |
| **官网** | https://paperclip.ing |
| **文档** | https://docs.paperclip.ing |
| **Discord** | https://discord.gg/m4HZY7xNG3 |
| **License** | Apache 2.0 |
| **最新版本** | v2026.626.0（2026-06-26） |
| **技术栈** | TypeScript, React, Node.js, Python SDK |
| **数据库** | PostgreSQL（embedded 开发 / 外置生产） |
| **安装** | `npx paperclipai onboard --yes` |
| **开发模式** | `pnpm dev`（Node.js 20+ / pnpm 9.15+） |
| **Agent 支持** | OpenClaw, Claude Code, Codex, Cursor, Gemini, bash, HTTP bots |
| **核心特性** | Org Chart / 心跳调度 / 预算硬停止 / 审批流 / 审计日志 / 多公司隔离 |
| **自托管** | ✅ 完全支持，Docker 可用 |

---

**研究完成。** 本文档已存档到 vault：`/root/vault/Research/2026-06-28 - Paperclip - GitHub Deep Research.md`