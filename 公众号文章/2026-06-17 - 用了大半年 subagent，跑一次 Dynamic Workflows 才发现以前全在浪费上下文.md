---
title: 用了大半年 subagent，跑一次 Dynamic Workflows 才发现以前全在浪费上下文
author: 林月半子的AI笔记
publish_date: 2026-06-01 17:59
saved_date: '2026-06-17'
source: wechat
url: https://mp.weixin.qq.com/s/KmlyQ0UxWyoZ2ha9i0nx-g
tags:
- AI
- Agent
- Claude
- claude-code
- dynamic-workflow
- multi-agent
- subagent
- token-optimization
- 公众号
type: article-summary
description: Anthropic 发布 Dynamic Workflows（Claude Code v2.1.154+），让 AI 自己写编排脚本，调度几十上百个
  subag...
timestamp: '2026-06-01T17:59:00'
resource: https://mp.weixin.qq.com/s/KmlyQ0UxWyoZ2ha9i0nx-g
---
# 用了大半年 subagent，跑一次 Dynamic Workflows 才发现以前全在浪费上下文

> **摘要存档**（原文 20 万字，本文档只存核心要点，保护版权）

## 核心论点

Anthropic 发布 **Dynamic Workflows**（Claude Code v2.1.154+），让 AI 自己写编排脚本，调度几十上百个 subagent 并行干活。

## 三者区别

| 工具 | 角色 | 协作规模 | 谁握计划 |
|---|---|---|---|
| **Subagent** | 跑腿小弟 | 单任务 | 主 Agent 逐轮判断 |
| **Skill** | 按手册操作 | 单次执行 | 调用方决定 |
| **Workflow** | 流水线作业 | 多 Agent 并行 | AI 自己写编排脚本 |

## Dynamic Workflows 关键特性

- **动态生成**：AI 看到任务后临场写 JavaScript 脚本
- **后台运行**：脚本在独立 session 跑，主 Agent 全程睡觉
- **最后叫醒**：主 Agent 只在结尾被叫醒读结果
- **类比 n8n**：n8n = 静态路由；Dynamic Workflows = 动态路由

## 触发方式

1. **prompt 含 "workflow" 关键词** → 触发
2. **`/effort ultracode`** → 自主决定是否用 workflow

## 与何大人项目的关联

### 命中问题（2026-06-16 何大人反思）
- 12:48 提出多 Agent 并行架构
- 12:50 批评 PPTOS token 消耗大

### 本文给的方案
- **subagent 隔离上下文** = 我之前写的 token 优化方案
- **Dynamic Workflows 后台运行** = 主 Agent 睡觉，避免上下文堆积
- **AI 自己写编排脚本** = 未来方向

### 落地路径
- 短期：手写编排逻辑（我之前计划的 orchestrator + qa + executor）
- 中期：subagent 隔离上下文（已实施）
- 长期：等类似 Dynamic Workflows 能力在 OpenClaw 落地

## 值得借鉴的设计

1. **后台 subagent + 末尾汇总** — 主 Agent 上下文不被中间结果污染
2. **动态编排** — 不写死流程，AI 现场生成
3. **脚本即调度** — 用 JavaScript/DSL 写调度，逻辑可读

## 一句话总结

> "subagent 适合跑腿，skill 适合按手册，workflow 适合多 Agent 并行的流水线"

## 相关文章引用

- vault 里已存的多 Agent 研究：Routa / Goose / Harnss / Hermes（2026-06-12）
- MEMORY.md "多 Agent 并行处理" 段（2026-06-16 何大人建议）
- MEMORY.md "PPTOS token 优化" 段（2026-06-16 何大人建议）
- vault/公众号文章/2026-06-16 - Claude Code 架构解析.md（OpenClaw vs Claude Code）
