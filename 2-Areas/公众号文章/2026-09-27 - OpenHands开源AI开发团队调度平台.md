---
type: article-metadata
file_type: wechat
title: OpenHands 开源 AI 开发团队调度平台
source: 何大人分享
url: https://github.com/All-Hands-AI/OpenHands
uploaded_date: 2026-09-27
tags: [OpenHands, Agent调度, Claude Code, Codex, 多Agent编排]
description: OpenHands 三层架构：统一控制台 + 自动化编排 + 分布式执行
---

# OpenHands 开源 AI 开发团队调度平台

## 三层架构

### 1. 统一控制台
把 Claude Code、Codex 等原本各自独立的 Coding Agent 纳入同一个面板管理，状态、配置、日志一目了然。

### 2. 自动化编排
通过事件触发（比如 GitHub 新开 Issue 或 PR）自动派发任务，让 Agent 自己读代码、改 Bug、写功能、跑测试，不再需要人工一步步接力。

### 3. 分布式执行
不同 Agent 可以跑在不同机器或云端，结果统一汇总回 OpenHands 控制台，相当于用一套系统管一支 AI 开发团队。

## 项目地址
https://github.com/All-Hands-AI/OpenHands

## 关联研究
- AgentRouter（AgentSpace 内置多 harness 识别）→ `/root/vault/1-Projects/德勤/AI-Native/AgentSpace-部署/`
- Jev Filter → `/root/.openclaw/workspace/skills/jev-filter/`
- CLM（Stanford 对比语言模型）→ `/root/vault/2-Areas/公众号文章/2026-09-27 - 斯坦福CLM开源16ms干翻Jev150ms.md`

## 思考
- OpenHands 定位：多 Agent 调度平台
- 与 AgentSpace/AgentRouter 的关系：AgentSpace 是单节点多 harness，OpenHands 可能是多节点多 Agent
- 与德勤项目的关联：交付多 Agent 协作系统时，OpenHands 是竞品还是可集成组件？
