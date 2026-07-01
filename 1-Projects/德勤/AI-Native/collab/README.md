---
title: 协作空间（频道 + 线程 + 评论 + 文件共享）
date: 2026-07-01
type: collaboration-spec
project: 德勤 AI-Native
status: active
tags:
  - 德勤
  - AI-Native
  - collaboration
  - vault-para
---

# 协作空间（vault PARA）

本目录提供一个基于 Obsidian / Markdown / PARA 的轻量协作层，用于支持：
- 项目频道（channel）
- 任务线程（thread）
- 人与 Agent 的评论往来（comment）
- 文件挂载与引用（file share）

目标是先满足 v0.3 文档中的“协作可见”验收：
- 人可以在任务下和 Agent 讨论
- Agent 输出可以挂到对应任务
- 所有内容都能落到 vault 内可追踪路径

不包含：
- 实时推送
- 通知中心
- emoji/reaction
- 完整前端 UI
- 服务端持久化部署

## 目录结构

```text
collab/
├── README.md
├── templates/
│   ├── channel.md
│   └── thread.md
└── demo-project/
    ├── channels/
    ├── threads/
    ├── comments/
    └── files/
```

建议后续按项目复制为：

```text
/1-Projects/<项目>/collab/
  channels/
  threads/
  comments/
  files/
```

## 对象设计

### 1. 频道（channel）

用于承载项目级上下文，如：
- `#ai-native-product`
- `#delivery-weekly`
- `#mvp-build`

一个频道文件是一个 Markdown 文档，包含：
- channel_id
- project
- owner
- members
- related_tasks
- linked_threads
- linked_files

频道本身不承载全部消息，而是汇总该频道下面的线程入口。

### 2. 线程（thread）

线程对应一个具体任务、议题或交付物讨论。

一个线程文件至少需要：
- thread_id
- channel_id
- task_id
- status
- owner
- participants
- mentioned_agents
- deliverables

正文中使用时间线记录讨论。

### 3. 评论（comment）

评论是最细粒度交互单元。当前阶段不单独做数据库对象，直接内嵌在线程 Markdown 中，或将 Agent 单次输出作为独立文件放在 `comments/`。

推荐两种模式：
- 短评论：直接写在线程时间线中
- 长输出：单独存为 `comments/<timestamp>-<author>.md`，在线程中引用

### 4. 文件共享（files）

`files/` 放和线程相关的附件占位、说明文件、交付物 sidecar 或链接说明。

当前阶段不强制实际二进制托管方式，但至少要做到：
- 在线程 frontmatter 或正文中可引用文件路径
- 文件与任务/线程有关联
- Agent 输出可以作为交付物挂到 thread

## @Agent 约定

在 Markdown 中使用 `@agent-name` 表示指向某个 Agent。

示例：
- `@hermes`：通用协作 Agent
- `@researcher`：研究型 Agent
- `@builder`：执行型 Agent

当前阶段 `@agent-name` 只是约定语法，不包含自动执行器；其价值在于：
- 统一文档内引用方式
- 为后续解析器 / 触发器预留结构
- 明确每段消息的责任主体

推荐同时在 frontmatter 中保留：
- `mentioned_agents`
- `agent_owner`
- `agent_response_files`

## 命名建议

### 频道文件

```text
channels/<channel-slug>.md
```

例如：
- `channels/ai-native-mvp.md`

### 线程文件

```text
threads/<date>-<task-slug>.md
```

例如：
- `threads/2026-07-01-mvp-task-01-collab-foundation.md`

### 评论输出文件

```text
comments/<timestamp>-<author>-<topic>.md
```

例如：
- `comments/2026-07-01T2355-hermes-collab-proposal.md`

## 推荐工作流

1. 先创建一个项目频道文件
2. 每个任务创建一个线程文件，并关联 `task_id`
3. 人在 thread 中提问，使用 `@agent-name`
4. Agent 输出短内容直接回写 thread
5. Agent 长内容单独落到 `comments/`，再在线程中引用
6. 若有交付物，放入 `files/` 或引用 vault 中其他正式路径

## Demo 内容

`demo-project/` 已包含：
- 1 个项目频道
- 2 个任务线程
- 1 个 Agent 响应文件
- 文件共享说明占位

可直接作为后续前端或解析器输入样例。
