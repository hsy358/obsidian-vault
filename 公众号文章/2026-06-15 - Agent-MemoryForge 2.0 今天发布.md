---
title: "Agent-MemoryForge 2.0 今天发布"
author: "未署名（轻量发布文章）"
publish_date: "2026-06-15"
source: "wechat"
url: "https://mp.weixin.qq.com/s/09ccKnDHeWKacVKPjuqAZw"
description: "Agent-MemoryForge 2.0 发布 - 面向真实企业 agent 系统的生产级 Memory Layer"
type: wechat-article
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
  source_url: https://mp.weixin.qq.com/s/09ccKnDHeWKacVKPjuqAZw
---

# Agent-MemoryForge 2.0 今天发布

> 来源：微信公众号文章（轻量产品发布，无完整正文，description 包含全部核心信息）

## 产品定位

Agent-MemoryForge 2.0 今天发布。

这次 2.0 最大的变化是，把 Agent-MemoryForge 明确升级成一个面向真实企业 agent 系统的**生产级 Memory Layer**。

它的核心定位是：

- 客户自己的 LangChain、LangGraph、OpenAI Agents SDK、自研 agent 继续负责**推理、规划、工具调用和回答**
- Agent-MemoryForge 负责**可审计、可隔离、可检索、可沉淀的长期记忆系统**

2.0 里，作者也把 Orbyt 中一部分经过验证的记忆与 context 管理能力集成了进来，让 Agent-MemoryForge 不只是**存储记忆**，而是能**参与记忆选择、上下文组装和召回治理**。

## 2.0 新增和稳定的关键能力

1. **API-first 集成**，并提供官方 Python SDK
2. **tenant / workspace / user 三层记忆隔离**
3. **workspace 级 MCP 配置、加密 secrets 和 tool policy**
4. **STM、WM、preferences、semantic、graph 多类记忆分工**
5. **异步 distillation**，避免把记忆沉淀阻塞在用户请求链路里
6. **pgvector 语义召回 + SQLite FTS + Neo4j graph + Redis queue/metrics** 的组合架构
7. **Portal 管理**：用户、workspace、quota、usage、memory inspection、tool config 和 traces
8. 支持 **OpenAI-compatible Responses API 和 Chat Completions API**

## 目标

让企业**不用重写自己的 agent 平台**，也能拥有一套**稳定、可运营、可追踪、可扩展的 agent memory infrastructure**。

## 项目地址

- GitHub: https://github.com/hellangleZ/Agent-MemoryForge
