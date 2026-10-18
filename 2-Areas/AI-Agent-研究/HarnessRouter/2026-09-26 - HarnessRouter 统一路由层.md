---
title: "HarnessRouter — Agent 统一路由层"
description: Agent 界的 OpenRouter，统一接入 Codex/Claude Code/Hermes/DeepSeek Harness 等
source: https://github.com/HarnessRouter/harnessrouter
author: HarnessRouter
uploaded_date: 2026-09-26
tags: [HarnessRouter, Agent框架, 统一路由, 开源, UHP协议]
file_path: /root/vault/2-Areas/AI-Agent-研究/HarnessRouter/2026-09-26 - HarnessRouter 统一路由层.md
---

# HarnessRouter — Agent 统一路由层

> GitHub：https://github.com/HarnessRouter/harnessrouter
> 许可：Apache-2.0（社区版）

## 是什么

**HarnessRouter** 是一个开源的 Agent 框架统一路由层，被称为"**Agent 界的 OpenRouter**"。

它把多种 harness 收拢到同一个 **UHP 统一协议**下，对外提供兼容 **OpenAI Responses** 的 API。

## 支持的 Harness（部分）

- Codex
- Claude Code
- Hermes
- DeepSeek Harness
- Gemini CLI
- OpenClaw
- ……十几种

## 核心价值

- **一次对接，任意切换**：产品只需对接 HarnessRouter，就能在任意 harness 之间切换
- **不用重复造轮子**：统一处理会话、流式、文件、取消和错误处理
- **单 Docker 容器自托管**：部署简单，密钥和数据都在自己机器上
- **Apache-2.0 许可**：开源可用

## 架构定位

```
你的产品
    ↓ （OpenAI Responses 兼容 API）
HarnessRouter（UHP 统一协议层）
    ↓
Codex / Claude Code / Hermes / DeepSeek Harness / ……
```

## 与 OpenClaw 的关系

HarnessRouter 已支持接入 OpenClaw 作为 harness 之一。

这意味着：
- OpenClaw 可以通过 HarnessRouter 对外提供统一 API
- 其他 harness（Codex、Claude Code 等）也可以通过 HarnessRouter 被统一调用

## 相关项目

- Jev（决策引擎）— 可作为 harness 接入
- Hermes Agent v0.14（德勤项目选用框架）
- OpenClaw（当前 Agent 平台）

---

*存档时间：2026-09-26*
