---
type: project-research
file_type: markdown
file_path: /root/vault/2-Areas/AI-Agent-研究/OpenRig/2026-09-29 - OpenRig GitHub 研究.md
source: 微信转发 + GitHub
uploaded_date: 2026-09-29
title: OpenRig - 多Agent编排工具
description: 用YAML声明式地把Claude Code、Codex等会话组织成可持久化、可恢复、可共享记忆的团队拓扑
tags: [AI-Agent, 多智能体编排, Claude-Code, Codex, OpenRig, tmux, YAML]
size_bytes: null
github_url: https://github.com/mvschwarz/openrig
install: npm install -g @openrig/cli
---

# OpenRig - 多 Agent 编排工具

## 项目信息

- **GitHub**: https://github.com/mvschwarz/openrig
- **npm**: `@openrig/cli`
- **Star**: ~15K（GitHub Trending 当日热门）
- **安装**: `npm install -g @openrig/cli`
- **依赖**: Node.js 22/24, tmux
- **平台**: macOS/Linux（Windows 不支持，WSL2 未测试）

## 核心定位

> "A harness wraps a model. A rig wraps your harnesses."  
> **Harness 包装模型，Rig 包装 Harness——用 YAML 定义 Agent 团队，一命令启动。**

把散落的 AI coding agent 终端会话变成一个**持久化、有组织、可协同的团队**。

## 核心概念

| 概念 | 含义 |
|---|---|
| **Harness** | 包装一个模型（类似 JevHarness 的 harness） |
| **Rig** | 包装多个 harness，成为一个可管理的系统 |
| **Seat** | Rig 中的一个 Agent 席位（如 owner、checker） |
| **Queue** | 任务队列，owner 从中取任务 |
| **cmux** | macOS 上的 tmux 自动化管理工具 |

## 架构特点

- **YAML 声明式定义**：用 YAML 文件声明 Agent 团队拓扑
- **tmux 会话管理**：每个 Seat 运行在独立的 tmux session 中
- **持久化上下文**：团队的工作和上下文保存在同一地址，可恢复
- **共享记忆**：多个 Agent 之间可以共享记忆
- **Claude Code + Codex 协作**：同一 Rig 中可以同时运行两种 Agent

## 典型工作流

```
用户 → 给 owner 发任务 → owner 从 queue 取任务
                           ↓
                    owner 执行 + 验证
                           ↓
                    问 checker 检查候选结果
                           ↓
                    返回结果 + 记录到 artifact
                           ↓
                    用户继续下一个任务
```

## 与 JevHarness 的关系

| | JevHarness | OpenRig |
|---|---|---|
| 核心抽象 | Harness（包装模型）+ Jev（轻量决策）| Harness（包装模型）+ Rig（包装 Harness）|
| 目标 | 单 Agent 的决策加速 | **多 Agent 协作编排** |
| 声明方式 | LLM 生成 harness 代码 | YAML 声明式定义团队拓扑 |
| 持久化 | 轨迹 + 奖励反思 | tmux session + 共享上下文 |
| 代表案例 | 宝可梦对战（25%→75%）| 软件开发团队（owner + checker）|

**共同思想**：都是"Harness"作为核心抽象，只是 JevHarness 聚焦决策层，OpenRig 聚焦多 Agent 协作层。

## 与德勤架构文档的关联

德勤架构设计中的 `pi-mono`/`codex` 模块，可能与 OpenRig 的思路有重叠：
- 都是多 Agent 协作框架
- 都关注可持久化、可恢复的执行上下文
- Task Graph / Task Collaboration Plane 在 OpenRig 中体现为 Queue + Owner/Checker 模式

## 待研究

- [ ] OpenRig 的 Rig 内部状态管理机制
- [ ] 与 Task Collaboration Control Plane 的具体映射
- [ ] OpenRig 的 cmux 实现
