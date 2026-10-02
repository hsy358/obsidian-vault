---
title: "HiFox — 多 Agent 协作平台"
source: hifox
url: https://hifox.com/
saved_date: 2026-10-02
tags: ["Agent-Platform", "Multi-Agent", "Collaboration", "Kanban"]
description: "一站式 Agent 统一指挥管理平台，支持看板协作 + Jira 双向同步"
---

# HiFox — 多 Agent 协作平台

**官网**: [hifox.com](https://hifox.com/)
**定位**: 多人与多 Agent 的协作空间 / Agent 统一指挥管理平台

## 核心定位

> AI Coding 进入看板协作时代！把 Agent 变成真正的队友，像指派任务给同事一样，直接把任务指派给 Agent。

**不是新 Agent** — HiFox 不替代 Claude Code/Codex/Cursor/本地 Agent，而是把它们接入统一的团队协作管理层。

## 核心功能

### 接入各种 Agent 工具
- 直接接入 **Claude Code、Codex、OpenCode、OpenClaw、Hermes、Pi** 等
- Token 消耗直接用已有的 Coding Plan / API Key
- 支持 20+ Coding Agent

### 任务指派（看板）
- 从需求、缺陷到支持任务，都可以像分配给同事一样交给 Agent
- 任务上下文、执行进展、结果回传集中在一处

### 多 Agent 并行
- 多个任务同时推进
- 每个 Agent 在独立 worktree 执行（代码变更互不干扰）
- 进度、阻塞、结果统一回到收件箱

### 团队共享 Agent、技能、上下文
- 像管理团队成员一样管理 Agent
- Prompt、技能、执行经验沉淀成团队能力

### 自动化流程
- 站会、周报、缺陷分流、状态同步、需求补全
- 用自动化触发 Agent，减少研发摩擦

## 专项管理（类 Jira 功能）

- 需求与任务
- 史诗（Epics）
- 迭代（Sprints）
- 处理人（人/Agent 均可）
- 评审与评论
- 分流（Routing）

## Jira 双向同步

接入 Jira 等项目管理系统，保持双向同步。团队继续用原有系统，Agent 执行接入进来。

支持：Jira / Linear / TAPD / PingCode / Teambition / 云效 / 禅道 / ONES / GitHub issue / GitLab issue / Asana / Shortcut

## 版本与价格

| 版本 | 适合 | 价格 |
|---|---|---|
| 公网 SaaS | 中小团队 / 个人开发者 | **免费**，不限席位 |
| 私有化部署 | 大型团队，专人服务 | 付费（按人数）|

## 对德勤项目的参考价值

- **看板式 Agent 协作** → 德勤 MVP 的 Workspace 多 Agent 调度可用类似 UX
- **多 Agent 并行 + 独立 worktree** → Hermes 多 Executor 隔离执行的设计参考
- **Jira 双向同步** → 德勤交付场景里企业已有的 Jira/Confluence 集成方案
- **团队共享 Agent 上下文** → 德勤 AgentSpace 的团队级上下文管理设计
