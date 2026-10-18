---
type: project-research
file_type: markdown
file_path: /root/vault/2-Areas/AI-Agent-研究/JevHarness/2026-09-29 - JevHarness 项目研究.md
source: 微信转发
uploaded_date: 2026-09-29
title: JevHarness - AI Agent 决策框架
description: "三权分立"架构的 AI Agent 决策框架，LLM生成流程+Harness执行+Jev轻量决策
tags: [AI-Agent, 决策框架, 开源, Jev, Claude-Code]
size_bytes: null
github_url: https://github.com/TianyuCodings/JevHarness
website_url: https://jev-harness.tianyuchen99.chatgpt.site
---

# JevHarness - AI Agent 决策框架

## 项目信息

- **GitHub**: https://github.com/TianyuCodings/JevHarness
- **定位**: AI Agent 配套决策框架（Claude Code 插件形式）
- **安装**: `/plugin marketplace add https://github.com/TianyuCodings/JevHarness.git`

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

## 性能数据（宝可梦对战实测）

| 指标 | 中位数 | P95 | 样本数 |
|---|---|---|---|
| 初始 harness 全决策 | 678 ms | 1,495 ms | 238 |
| 选中的 harness 全决策 | 568 ms | 657 ms | 113 |
| 选中 harness 单次 Jev 请求 | 269 ms | 348 ms | 226 |

## 实战案例

- **宝可梦对战测试**：5 轮 reflection，胜率从 **25% (3/12) → 75% (9/12)**
- 附带交互式 demo + 本地 replay viewer

## 关键价值

> 用 LLM 做"一次性规划"，用 Jev 做"实时执行决策"——兼顾深度和速度

## 技术细节

- **Harness 包含**：code、features、state、instructions、criteria、control flow
- **Code 计算有用的事实**，Jev 基于这些事实做模糊决策
- **开发期**：LLM 可以修改 harness 和 memory
- **冻结后**：只执行 code + Jev calls，不再需要 authoring LLM

## 关键概念

- **GEPA**：可能是某种进化/优化机制（待查）
- **Reward Reflection**：用奖励信号做自我反思
- **Train/Eval 分离**：训练集评估 decision quality，Eval 用于选择最佳 harness

## 与 OpenClaw 的关联

- OpenClaw 现有 `skills/jev-filter/` 本质上是通用 Jev 决策
- JevHarness 的思路可以借鉴：**任务专属的 Jev 规则 = LLM 生成 + 冻结**
- OpenClaw 的心跳/cron 过滤阈值能否用 LLM 生成？

## 待研究

- [ ] Jev 模型的具体实现（是调用哪个模型？）
- [ ] GEPA 机制的具体含义
- [ ] OpenClaw Jev Filter 借鉴 JevHarness 的可行性
