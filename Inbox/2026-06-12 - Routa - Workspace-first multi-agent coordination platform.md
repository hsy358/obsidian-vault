# Routa - Workspace-first Multi-agent Coordination Platform

**Source:** https://github.com/phodal/routa

## 概述

Routa 是一个工作区优先的多 Agent 协调平台，专注于软件交付。与单线程聊天不同，Routa 将目标、任务、会话、追踪、证据和审查状态都显示在看板（Kanban）上，而非埋在单一聊天窗口里。

## 核心理念

**问题：** 单 Agent 聊天适合孤立任务，但在需要分解、实施、审查、证据收集和发布决策的场景下会崩溃。

**Routa 的解法：**
- 工作从 workspace 开始，而非隐藏的全局仓库状态
- 看板泳道在不同专家之间路由工作
- 会话、追踪、笔记、产物、代码库都是持久对象
- Provider 运行时通过适配器标准化

## Kanban 流程与专家角色

看板每列都有不同的专家 prompt，卡片每经过一列都会变得更严格：

| 阶段 | 专家 | 职责 |
|------|------|------|
| Backlog | Backlog Refiner | 将需求改写为标准 YAML story，含验收标准、约束、依赖、INVEST 检查 |
| Todo | Todo Orchestrator | 重新验证，生成可执行简报（执行计划、关键文件、依赖计划、风险笔记） |
| Dev | Dev Crafter | 实施实现、运行验证、提交代码、生成 Dev Evidence |
| Review | Review Guard | 独立验证每条验收标准，拒绝缺失证据、范围蔓延、脏 git 状态 |
| Done | Done Reporter | 追加完成总结 |
| Blocked | Blocked Resolver | 分类 blocker，说明根因，路由回正确泳道 |

**三核心角色：**
- **ROUTA Coordinator**：只规划，不直接编辑文件，写 spec，等批准，委托工作，调用 GATE 验证
- **CRAFTER Implementor**：保持任务范围，避免重构和范围蔓延，提交小单元
- **GATE Verifier**：只验证验收标准，证据是强制的，不允许部分通过

## 投递门（Review Gate）

Review Gate 是 stacked decision path，不是单一审查员：

- **Harness Monitor**：回答"发生了什么"——展示追踪、变更文件、命令、git 状态、归因
- **Entrix Fitness**：回答"什么应该是真的"——强制硬门、证据要求、文件预算或策略检查
- **Gate Specialist**：回答"卡片能否移动"——验证验收标准，路由到 Done/Dev/人工升级

## 技术架构

**双后端设计（同一产品，非两个独立产品）：**
- **Web:** Next.js 页面 + route handlers（`src/`）
- **Desktop:** Tauri shell + Axum 服务端（`apps/desktop/` + `crates/routa-server/`）

**共享边界：** 两个运行时保留相同的 workspace、session、task、trace、codebase、worktree、review 语义

**集成面：** ACP、MCP、A2A、AG-UI、A2UI、REST、SSE

**技术栈：**
- 前端：Next.js + TypeScript
- 桌面：Tauri
- 后端：Rust (Axum)
- CLI：Node.js/npm, Rust/Cargo

## 功能亮点

- 创建 workspace 范围的概览、看板、会话、团队视图、代码库视图
- Agent 会话管理（create/prompt/cancel/reconnect/streaming/trace 检查）
- 路由工作跨专家泳道（队列 + 每看板自动化）
- 本地仓库管理、工作树、文件搜索、Git 引用、提交检查
- 导入 GitHub 仓库作为虚拟工作区
- MCP 工具和自定义 MCP 服务器
- 定时任务、Webhook、后台任务、工作流运行
- 审查变更（发现、严重性、追踪、harness 信号、fitness 报告）

## 启动方式

| 方式 | 适用场景 | 启动方式 |
|------|----------|----------|
| Desktop | 完整产品体验，本地优先 | 下载 GitHub Releases |
| CLI | 终端优先工作流和脚本 | `npm install -g routa-cli` |
| Web | 自托管或浏览器优先 | Docker Compose 或源码运行 |

## 文档

- [官网](https://phodal.github.io/routa/)
- [架构文档](https://github.com/phodal/routa/blob/main/docs/ARCHITECTURE.md)
- [快速开始](https://github.com/phodal/routa/blob/main/docs/quick-start.md)
- [Fitness 规则](https://github.com/phodal/routa/blob/main/docs/fitness/README.md)

## 相关链接

- Slack 社区：https://join.slack.com/t/routa-group/shared_invite/zt-3txzzfxm8-tnRFwNpPvdfjAVoSD6MTJg
- Bilibili 演示：https://www.bilibili.com/video/BV16CwyzUED5/
- YouTube 演示：https://www.youtube.com/watch?v=spjmr_1AQLM