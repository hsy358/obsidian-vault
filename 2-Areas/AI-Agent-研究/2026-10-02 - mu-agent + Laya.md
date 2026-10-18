---
title: "mu-agent：内置判定内核的 Coding Agent"
source: github
url: https://github.com/lvy010/mu
npm: https://www.npmjs.com/package/mu-agent
saved_date: 2026-10-02
tags: ["Coding-Agent", "Judge", "Decision-Engine", "mu-agent"]
description: "mu：内置 35 个判定点的 Coding Agent，判定核可插拔（Jev 商业 API / Laya 开源平替）"
---

# mu-agent + Laya

## mu (μ) — 带判定核的 Coding Agent

**仓库**: [github.com/lvy010/mu](https://github.com/lvy010/mu)
**NPM 包**: [mu-agent](https://www.npmjs.com/package/mu-agent)
**基于**: [pi](https://github.com/earendil-works/pi)（底层框架）
**版本**: 0.1.x（快速迭代中）

### 核心思路

> 一个 Coding Agent 每轮对话要做数百个决策：什么进 context、命令是否安全、发现是否值得告知另一个 Agent、工作何时完成。全交给大模型 → 贵且慢。全写死规则 → 错误太多。mu 的解法：**判定核（Judge）** — 用小模型快速回答单个有界问题，每轮 35 个判定点，大模型专注干活。

### 判定点（Decision Points）

每轮结构：
```
you ──▶ input.preflight · task.frame · input.interjection
         │
         ▼
       model ──▶ tool call ──▶ tool.risk · tool.constraint · tool.approval ──▶ runs
       ▲                                                                     │
       │    tool.admission   chunk by chunk: 进 context 或归档到指针
       │    context.forget · context.compact   context 膨胀时触发
       └─────────────────────────────────────────────────────────────────────┘

turn ends ──▶ turn.completion · turn.drift · turn.rewind · memory.applied · board.read · cache.warming
```

**35 个判定点**，每个都是一个小问题 + 短回答，答案决定下一步行动。

判定点可配置状态：`active` / `shadow`（只记录不执行）/`off`，每个点可指定自己的 judge。

### Judge 架构（可插拔）

| Judge | 类型 | 说明 |
|---|---|---|
| **Jev** | 闭源商业 API | 商业判定服务 |
| **Laya** | 本地开源 | `github.com/NandhaKishorM/laya`，可完全平替 |
| **`llm:<provider>/<model>`** | 任意 LLM | 通用接口 |

支持 cascade 写法：`laya,jev`（Laya 判不过再走 Jev）

---

## Laya — 开源判定引擎

**仓库**: [github.com/NandhaKishorM/laya](https://github.com/NandhaKishorM/laya)
**PyPI**: `pip install laya`
**npm**: `laya-ts`
**HuggingFace**: [convaiinnovations/laya](https://huggingface.co/convaiinnovations/laya)

### 核心能力

> **Non-autoregressive System 1 decision engine** — 单次 forward pass 完成 typed decision（yes/no / choice / score），100+ 语言，**33ms 延迟**，带 router 自动选 checkpoint。

**技术方案**：用 RLCD（Reinforcement Learning against Critically Discrete Scoring Rules）训练。

### 关键特性

- **多语言**：100+ 语言单 pass 判定
- **极低延迟**：~33ms（GPU），适合实时判定场景
- **Router**：根据请求自动选最合适的 checkpoint
- **长文档**：laya-multilingual 支持 8,192 token，16-18/20 准确率
- **集成**：LangChain / LangGraph / LlamaIndex / CrewAI / ONNX Runtime

### Laya vs Jev

| | Laya | Jev |
|---|---|---|
| 类型 | 开源本地 | 闭源商业 API |
| 延迟 | ~33ms | 依赖网络 |
| 定制性 | 高（可微调） | 低（API 黑盒）|
| 维护成本 | 自己托管 | 付费即用 |

---

## 对德勤项目的参考价值

### 判定核架构（最值得借鉴）
mu 的 35 个判定点 × 小模型判定 = 大模型 token 节省 + 决策质量提升。德勤 MVP 的 **Executor 调度层** 可借鉴：把"路由决策"从大模型抽出来，用 Laya 这类小模型承担。

### Laya 作为 Hermes 执行器抽象层组件
Laya 可作为 Hermes 的**本地判定器**插件，闭源 Jev 作为商业备选。架构上 Laya/pi → 类似于 Hermes 的 Executor Adapter 设计。

### 判定点可插拔设计
```
tool.risk ──▶ laya,jev  （Laya 先判，失败走 Jev）
```
这种 cascade 设计值得参考：本地开源优先、兜底商业 API，保证判定质量。
