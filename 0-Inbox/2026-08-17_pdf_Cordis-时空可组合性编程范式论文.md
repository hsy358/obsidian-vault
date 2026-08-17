---
type: document-metadata
file_type: pdf
file_path: 0-Inbox/2026-08-17_pdf_Cordis-时空可组合性编程范式论文.pdf
source: https://github.com/cordiverse/paper/blob/main/paper.pdf
uploaded_date: 2026-08-17
saved_date: 2026-08-17
title: "A Programming Paradigm for Spatiotemporal Composability"
title_cn: "时空可组合性编程范式"
authors:
  - "Yifan Shi（北京大学 + DeepSeek-AI）"
  - "Wei Zhang（北京大学）"
  - "Tianyi Cui（DeepSeek-AI）"
publish_date: 2026-08-13
commit_sha: "948a07b"
repo_stars: 1900
repo_forks: 1400
size_bytes: 2140840
md5: a03e0e059a2f1664873db76c5d5324ea
page_count: 88
pdf_version: 1.7
related_repo: "https://github.com/cordiverse/cordis"
trending_status: "GitHub Trending #1 同日发布（与 DeepSeek Harness 同期）"
tags:
  - cordis
  - deepseek
  - agent-harness
  - programming-paradigm
  - effect-system
  - coeffect
  - spatiotemporal-composability
  - formal-methods
  - plugin-system
  - 调研笔记
  - 论文
---

# A Programming Paradigm for Spatiotemporal Composability

> **时空可组合性编程范式** —— 北京大学 + DeepSeek-AI 联合出品（2026-08-13），88 页形式化论文

## TL;DR

- **作者**：Yifan Shi, Wei Zhang（北京大学 PKU）+ Tianyi Cui（DeepSeek-AI）
- **GitHub**：[cordiverse/paper](https://github.com/cordiverse/paper)（1.9k★ · 1.4k fork · commit `948a07b`）
- **配套框架**：[cordiverse/cordis](https://github.com/cordiverse/cordis)（GitHub Trending #1，3.9k★）
- **发布同日（2026-08-13）**：DeepSeek Harness（DSH）也上线 Trending
- **核心论点**：现代软件（从插件系统到 **self-evolving agent harnesses**）需要 dynamic composition，但形式化基础不发达 —— 提出**两个正交维度**：
  1. **Temporal composability**：组件卸载时**完全撤销副作用**
  2. **Spatial composability**：声明 + 反应式管理**组件间依赖**
- **解决方案**：把经典 effect / coeffect 概念**提升为运行时机制**
  - **Revertible effects**：每个 context transformation 携带 inverse operation，runtime 跟踪
  - **Reactive coeffects**：context 每次变更根据 coeffect 规范**自动通知**组件
- **统一**：effect context 和 coeffect context → **单一 context type** → 构成一个编程范式
- **实现**：**Cordis** —— meta-framework
  - 核心库：effect tracking + coeffect resolution
  - 组件加载器：declarative configuration + **hot module replacement**

---

## 章节结构（88 页形式化论文）

| 章节 | 内容 |
|---|---|
| **1. Introduction** | 1.1 Dimensions of Composability · 1.2 Motivating Examples（**Plugin Systems / Self-Evolving Agent Harnesses / Coarse-Grained Workaround**） · 1.3 Contributions |
| **2. Preliminaries** | 2.1 Effects · 2.2 Coeffects · 2.3 Relationship to Dynamic Composability |
| **3. Revertible Effects and Reactive Coeffects** | 3.1 Revertible Effects（Effect Context / Revertible Effect Functions / Independence of Effects）· 3.2 Reactive Coeffects（Coeffect Context / Specification and Notification / Isolation and Interception）· 3.3 **The Context Paradigm**（Unified Context / Observational Equivalence） |
| **4. A Calculus of Dynamic Composition** | 4.1 Components and Fibers · 4.2 The Base Calculus · 4.3 Transitions in Progress（Withdrawal / Iteration / Asynchrony / Failure）· 4.4 Metatheory（Preservation / Temporal Composability / Spatial Composability / Progress / Confluence） |
| **5. Implementation and Case Study** | 5.1 Core Library（Effect Tracking / Coeffect Operations / Component Lifecycle / Context Access）· 5.2 Component Loader（Declarative Configuration / Hot Module Replacement）· **5.3 Case Study: Koishi** |
| **6. Discussion** | 6.1 System Boundary · 6.2 Service Multiplexing · **6.3 Access Control and Sandboxing** · 6.4 Language Independence · 6.5 Mutual Dependencies · 6.6 Dependency Typing · **6.7 Co-Design with Languages and OS** |
| **7. Related Work** | Effect/Coeffect Systems · Programming Paradigms · Temporal Composability · Spatial Composability |
| **8. Conclusion** | |

---

## 关键定义（论文形式化）

### Revertible Effect
> *Every context transformation carries an inverse that the runtime tracks.*
> 每次 context 变换都带 inverse，runtime 可回滚 —— 这是**插件可插拔 + 无残留**的数学基础。

### Reactive Coeffect
> *Each change of the context notifies a component against its coeffect specification.*
> context 变化时**主动通知依赖它的组件** —— 这是 hot-reload / 跨组件依赖自动同步的数学基础。

### Context Paradigm
> *We unify the effect context and the coeffect context into a single context type, which constitutes a programming paradigm.*
> effect + coeffect → 单一 context type → **新的编程范式级别的工作**。

### Spatiotemporal Composability
- **Temporal**：撤销性（withdrawal 章节详述） —— 让组件可以干净卸载
- **Spatial**：反应式（notification 章节详述） —— 让组件自动响应 context 变化
- **Metatheory**：从单组件 → 整套 interleaved 组件，composability 性质被证明可传递（Preservation / Progress / Confluence 定理）

---

## 📚 Motivating Examples 论文自带的（§1.2）

1. **Plugin Systems** —— 经典插件场景：装/卸插件不应留下残留
2. **Self-Evolving Agent Harnesses** —— **明确点名为例子**（Cordis 的目标场景）
3. **The Coarse-Grained Workaround** —— 现有方案的痛点（多半靠 restart 解决，缺乏形式化）

> 这跟 MEMORY.md 里德勤项目的"self-evolving / 插件化"思路**完全同源** —— Cordis 提供了**形式化证明**为什么这种设计是对的。

---

## 💡 我的提炼（4 个核心 takeaway）

1. **"卸载不残留"不是工程经验，是数学性质** —— Temporal Composability 定理（§4.4.2）证明：组件卸载后状态等价于"从未加载过"。这是 Agent Harness 跑 long-running 任务时**不用 restart 就能热替换**的关键。
2. **"自动响应依赖变化"是 coeffect 范式** —— Spatial Composability 定理（§4.4.3）证明：组件依赖的 context 变化会自动通知并安全处理。这是 plugin 改配置 / 模型切换 / 工具上下线时**所有依赖方自动同步**的数学保证。
3. **Plugin + Agent + LangGraph 的统一理论** —— 论文把这三种东西看作**同一个数学对象的不同实例**（都是 component + context transformation），意味着 plugin 系统的形式化经验可以直接迁移到 Agent runtime。
4. **DeepSeek Harness 的理论锚** —— DSH 8-13 发布 + Cordis 8-13 同日 Trending + 论文 §1.2.2 明确说 "Self-Evolving Agent Harnesses" 是 motivating example → **DSH = Cordis 的工业实现**。

---

## 🤔 跟德勤项目的对应（按 7-8 偏好不强挂，列给判断）

| 德勤目标 | Cordis 对应 | 借鉴价值 |
|---|---|---|
| M6 执行器抽象层（多 harness 适配） | Component + Context Paradigm（§3.3） | ✅ 每个 harness adapter 是一个 component，inverse operations 让"卸载干净"是数学性质 |
| 插件化 + 热替换 | HMR 章节（§5.2.2）+ Temporal Composability 定理 | ✅ 不依赖 ad-hoc 经验，有形式化保证 |
| **Self-improving loop**（loopany 提到的） | Self-Evolving Agent Harnesses（§1.2.2） | ⚠️ DSH 的 agent 演化能力是论文的直接动机 |
| **公网部署 + 沙箱**（AgentSpace 安全） | Access Control and Sandboxing（§6.3）· Service Multiplexing（§6.2） | ✅ 论文有专门章节讨论 |
| **组件依赖声明** | Reactive Coeffects（§3.2）· Coeffect Context | ✅ 比 LangGraph 的 StateGraph 更形式化 |

**潜在研究切入点**（你判断要不要纳入德勤项目）：
- ✅ 读 **§3.1 Revertible Effects + §4.4.2 Temporal Composability** 理解"插件无残留"的数学
- ✅ 读 **§3.2 Reactive Coeffects + §4.4.3 Spatial Composability** 理解"依赖自动同步"
- ✅ 读 **§6.3 Access Control and Sandboxing** 看公网 Agent 安全的形式化讨论

---

## 📎 原始来源

- **PDF**：https://github.com/cordiverse/paper/blob/main/paper.pdf
- **论文仓库**：https://github.com/cordiverse/paper（1.9k★）
- **框架仓库**：https://github.com/cordiverse/cordis（3.9k★ · Trending #1）
- **作者 1**：Yifan Shi —— 北京大学 + DeepSeek-AI
- **作者 2**：Wei Zhang —— 北京大学
- **作者 3**：Tianyi Cui —— DeepSeek-AI
- **同期事件**：DeepSeek Harness 8-13 发布 → Cordis 同日 Trending → 印证论文是 DSH 理论锚
- **外部解读**：[remio.ai - Cordiverse Cordis Hit GitHub Trending, but DeepSeek Is the Real Story](https://www.remio.ai/post/cordiverse-cordis-hit-github-trending-but-deepseek-is-the-real-story)