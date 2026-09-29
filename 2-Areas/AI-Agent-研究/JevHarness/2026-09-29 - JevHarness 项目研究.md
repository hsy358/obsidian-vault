---
type: project-research
file_type: markdown
file_path: /root/vault/2-Areas/AI-Agent-研究/JevHarness/2026-09-29 - JevHarness 项目研究.md
source: 微信转发
uploaded_date: 2026-09-29
title: JevHarness - AI Agent 决策框架
description: "三权分立"架构的 AI Agent 决策框架，LLM生成流程+Harness执行+Jev轻量决策
tags: [AI-Agent, 决策框架, 开源, Jev]
size_bytes: null
github_url: https://github.com/TianyuCodings/JevHarness
---

# JevHarness - AI Agent 决策框架

## 项目信息

- **GitHub**: https://github.com/TianyuCodings/JevHarness
- **定位**: AI Agent 配套决策框架

## 核心架构："三权分立"

| 角色 | 职责 | 特点 |
|---|---|---|
| **LLM** | 生成 | 负责深度推理，一次性生成任务专属决策流程 |
| **Harness** | 执行 | 负责执行层工具调用和状态管理 |
| **Jev** | 决策 | 每轮轻量高速决策，模糊判断 |

## 核心思路

1. **离线生成 + 线上冻结**：开发者用 LLM 一次性生成任务专属的决策流程（特征、问题、判据、动作逻辑），冻结后线上只靠代码加 Jev 模型做模糊判断
2. **降本降延迟**：大幅降低延迟和成本（不需要每轮都调用 LLM）
3. **持续优化**：支持用奖励和运行轨迹持续自我优化
4. **自带 Coding Agent 能力**：可回放每一步决策方便调试

## 实战案例

- **宝可梦对战测试**：5 轮迭代，胜率从 **25% → 75%**

## 关键价值

> 用 LLM 做"一次性规划"，用 Jev 做"实时执行决策"——兼顾深度和速度

## 待研究

- [ ] Jev 模型的具体实现
- [ ] 与 OpenClaw 的集成可能性
- [ ] Harness 的状态管理机制
