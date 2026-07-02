---
title: 本地小模型的 Claude Code 来了，拆解它的完整 Harness！
author: Datawhale（作者：陈思州）
publish_date: 2026-07-02 22:01:30
saved_date: 2026-07-02
source: wechat
url: https://mp.weixin.qq.com/s/iiTmgbtrYHMMjQ7dn7CDrg
type: 公众号文章
tags:
  - AI
  - Agent
  - Harness
  - Zleap-Agent
  - 本地小模型
  - Workspace-first
  - Context
  - Tools
  - Memory
  - Runtime
  - Boundary
  - Hermes
  - OpenClaw
  - Claude-Code
  - 稀疏注意力
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: openclaw-2026-07-02
related:
  - /root/vault/1-Projects/德勤/AI-Native/笔记/2026-06-29-AgentSpace研究笔记.md
  - /root/vault/1-Projects/德勤/AI-Native/笔记/2026-07-01 - 第一阶段开源研究清单 v3.md
  - /root/vault/1-Projects/求职-德勤/面试准备/2026-07-02 - 何四燕_知识库智能咨询台Agent平台_技术方案与架构图.md
---

# 本地小模型的 Claude Code 来了，拆解它的完整 Harness！

> **公众号**：Datawhale
> **作者**：陈思州
> **发布日期**：2026-07-02 22:01（今晚 22 点刚发）
> **项目**：**Zleap-Agent** — github.com/Zleap-AI/Zleap-Agent
> **核心定位**：**「本地小模型的 Claude Code」**——一个完整的 Harness 设计，专为本地小模型 + 稀疏注意力

---

## 摘要

Zleap-Agent 用 **Workspace-first** 理念，把 Agent 的运行环境切成独立工作区，**Context / Tools / Memory / Runtime / Boundary 五件事** 全部围绕工作区组织。这是「**Prompt → Loop → Harness**」演进的最新案例。

---

## 一、背景：Prompt → Loop → Harness 的演进

| 阶段 | 关注点 | 现状 |
|---|---|---|
| **Prompt Engineering** | 这一轮怎么提示模型 | 已不够用 |
| **Loop Engineering** | 模型如何一轮轮观察、行动、接收反馈 | Boris Cherny（Claude Code 之父）"未来工作变成写循环"|
| **Harness Engineering** | 这些循环运行在什么系统里 | 长期稳定、可控、低成本工作 |

> **OpenClaw 之父 Peter Steinberger 同样观点**：未来使用编程 Agent，不应该只是给 Agent 写 prompt，而是设计一套循环机制。

---

## 二、Zleap-Agent 核心设计：**Workspace-first**

### 4 个 Workspace

| Workspace | 职责 |
|---|---|
| **Main** | 理解用户目标 + 任务调度 |
| **Web Search** | 搜索、网页阅读、引用整理 |
| **CLI** | 文件读取/编辑、命令执行、测试 |
| **业务** | 销售/财务/运营/研究等具体场景 |

每个 Workspace 独立配置：prompt / tools / memory / history / model / permission。

### Workspace vs 子 Agent vs 工具分组

- **子 Agent**：临时找另一个人帮忙（独立角色 + 上下文，做完交结果）
- **Workspace**：同一个人**切换工作台**（人不变，工具/资料/权限变）
- **工具分组**：仅按工具分类，无独立 prompt/memory

> **核心方法论**：**先选工作区，再组装上下文**（不让 Agent 每步加载全部工具、记忆和历史）

---

## 三、Harness 五件事

### 1. **Context**：不要问能塞多少，先问这一轮该看什么

> OpenClaw 实测数据：**一次运行 system prompt ≈ 38,412 字符，tool schemas ≈ 31,988 字符**——任务没展开就已经吃满大量上下文

**Zleap 解法**：Main Workspace 不直接承担所有上下文；进入具体 Workspace 后，模型只看到当前工作区的 prompt、工具、记忆和历史。

**Context 公式**：
```
Context = System Prompt + Workspace Prompt + Tools + Memory + History
```

**两种加载方式**：
- **Prefetch（预取）**：用户偏好、近期事件、常用经验（短/准/可控）
- **Agentic Recall（按需）**：旧记忆摘要 → 用户追问 → 读完整详情

### 2. **Tools**：工具不是越多越好，关键是当前可见

> 工具越多：模型动作空间越大 + 权限面越宽 + 审计成本越高

**Zleap 解法**：**工具跟 Workspace 绑定**，不再全局暴露。Main 保留调度/管理工具；CLI 才有文件/命令工具；Web Search 才有搜索工具。

**效果**：tool schema 成本↓ + 误调用概率↓ + 权限审计压力↓

### 3. **Memory**：人 / 事 / 经验 三分区

> **核心论点**：保存数据 ≠ 写入数据库。记忆影响未来推理，写错/取错/串到别的任务都会污染后续行为。

**Zleap 的两条记忆线**：

| 线 | 类型 | 例子 |
|---|---|---|
| **A 线** | people notes（用户偏好 + 稳定画像 + Agent 自认知）| "我喜欢先看结论" |
| **B 线** | core records（工作事件 + 可复用经验）| "某客户卡在合同审批" |

**经验记忆准入规则**（脱敏 + 可复用）：
- ✅ 可复用流程、失败模式、验证习惯、恢复策略
- ❌ 公司名、客户名、项目名、财务事实、私有路径、一次性任务结果

### 4. **Memory Dream**（离线整理器）

> 不在用户实时对话里抢上下文，后台从清理过的会话材料中提取稳定画像和可复用经验

**事件/工作记忆走另一条链路**，经验记忆经过脱敏 + 可复用性判断。

### 5. **Recall 双速**

| 模式 | 用途 | 速度 |
|---|---|---|
| **Prefetch Fast** | 用户画像/近期事件/常用经验 | 不走 LLM，快 |
| **Agentic Recall** | 主动 recall | 走检索 + rerank，精 |

> 全部走 LLM → 慢 + 贵；完全不做精排 → 召回不稳。**快取和精取分开**才能兼顾。

### 6. **Runtime**：可复盘的轨迹

> **WildClawBench 数据**：同一个模型切换不同 harness，**表现最高相差 18 个百分点**
> **Agentic Harness Engineering**：多轮 harness 演化，Terminal-Bench 2 pass@1 **从 69.7% → 77.0%**（收益主要来自 tools/middleware/memory，不是改 system prompt）

**Zleap 解法**：运行状态和记忆用 **PostgreSQL 持久化**，而不是只在进程内存。失败可回滚、可审计。

### 7. **Boundary**：数据/工具/模型/记忆 4 边界

| 边界 | 控制点 |
|---|---|
| **数据边界** | 敏感数据本地处理，不出内网 |
| **工具边界** | 按 Workspace 暴露，不全局开放 |
| **模型边界** | 不同 Workspace 绑不同模型（本地小模型 + 强云端模型混搭）|
| **记忆边界** | 按用户/工作区/类型分区，不跨用户污染 |

---

## 四、5 个核心 Workspace 设计模式

```
Main Workspace（调度）  →  CLI Workspace（文件/命令）
                       →  Web Search Workspace（搜索）
                       →  业务 Workspace（销售/财务/运营/研究）
                       →  财务/敏感 Workspace（本地小模型，敏感数据不出内网）
```

---

## 五、跟德勤 v0.3 的关联

### 1. 高度同构（设计哲学一致）

| Zleap-Agent 设计 | 德勤 v0.3 对应 |
|---|---|
| **Workspace-first** | R4 协作最小单元（任务板 + 话题）|
| **5 个 Workspace 独立配置** | R3 执行器抽象（每 harness 独立 prompt/tools/memory）|
| **Tool 跟 Workspace 绑定** | R3 harness 注册机制 |
| **Memory 3 分区** | R5 KB（短期/长期/经验记忆）|
| **Boundary 4 边界** | R7 安全审批（数据/工具/模型/记忆 4 边界完全一致！）|
| **PostgreSQL 持久化** | R1 数据模型（已经用 PG）|

### 2. **R7 安全审批借鉴价值最高**

Zleap 的 4 边界 = **德勤 v0.3 R7 应该明确列出的 4 边界**：
- 数据边界（出不出内网）
- 工具边界（能不能调这个工具）
- 模型边界（用哪个模型）
- 记忆边界（记忆属于哪个用户/工作区）

**之前 AgentSpace 调研时 R7 还是模糊的，Zleap 给了清晰的 4 维度**。

### 3. **Context 装配公式** 直接可借鉴

```
Context = System Prompt + Workspace Prompt + Tools + Memory + History
```

**5 元素** = 德勤 v0.3 每次 Agent 调用应携带的最小上下文。

### 4. **Memory Dream** 值得做

离线记忆整理器（不抢在线上下文）= 跟 AgentSpace / Hermes 的「session 整理」机制同构

### 5. **Hermes Channel Fracture 案例** 引用

文中引用了 Hermes Agent 的 Channel Fracture 案例（**记忆写入路径有 skip_memory=True 隐性 bug**）—— **这跟何大人 MEMORY.md 里记录的 Hermes 实战问题直接对应**。

### 6. 调研建议

- **优先级**：**P1 升级为 P0 候选**（之前 v3 清单是 P2 暂缓）
- **理由**：
  - 数据驱动的 Harness 设计（**PG 持久化** vs OpenClaw/Hermes 内存驱动）
  - 5 件事拆解比 OpenClaw 的"Harness"更工程化、更可借鉴
  - 跟德勤 v0.3 R3/R4/R5/R7 直接同构
  - 中国本土项目（Zleap-AI），更贴近德勤中国客户场景
- **横向对比**：
  - 跟 OpenClaw（同为 Memory/Harness 主题，但是不同设计哲学）
  - 跟 Hermes（Channel Fracture 案例被引用）
  - 跟 AgentSpace（Workspace 概念同构）
  - 跟 Paperclip（组织控制同构）

---

## 六、跟何大人简历的关联

| 何大人简历项目 | Zleap 借鉴价值 |
|---|---|
| **平安云知识库与 Agent 智能体平台** | Memory 3 分区 + Memory Dream 直接对应知识库运营 |
| **集团知识管理 / 数据中台** | Boundary 4 边界（数据/工具/模型/记忆）是多 BU 协同的关键 |
| **徽商银行财富智能推荐系统** | Workspace-first 模式适合金融多业务线隔离 |
| **面试稿 4 份中的"ReAct / Planner-Executor"** | 跟 Zleap "Loop Engineering" 完全同构 |

---

## 七、金句

> "**Workspace-first** 的方法可以先总结成一句话：**先选工作区，再组装上下文**。"

> "模型层做**稀疏注意力**，是为了让模型不要看所有 token；Harness 层做 **Workspace**，是为了让 Agent 不要加载所有上下文。"

> "当上下文、工具、记忆都会不断膨胀时，怎么让 Agent **只看该看的那部分**。"

---

## 八、总结

| 维度 | Zleap-Agent | 德勤 v0.3 应吸收 |
|---|---|---|
| **设计哲学** | Workspace-first | R4 协作最小单元 = Workspace |
| **Harness 5 件事** | Context / Tools / Memory / Runtime / Boundary | R3/R5/R6/R7 对应 |
| **记忆 3 分区** | 人 / 事 / 经验 | R5 KB 子模块划分 |
| **4 边界** | 数据 / 工具 / 模型 / 记忆 | **R7 安全审批核心** |
| **持久化** | PostgreSQL | R1 已有 PG，对得上 |
| **本地小模型** | 支持本地部署 + 稀疏注意力 | R9 单独部署 + 成本控制 |

**Zleap-Agent 应该是 v0.3 第一阶段研究清单 v4 的 P0 候选**。

---

**作者**：小助（OpenClaw · MiniMax-M3）— 2026-07-02 23:25 存档  
**判断**：⭐⭐⭐⭐ **必读 + 必借**：这是今年看到的**最工程化、最结构化的 Harness 设计拆解**，直接对应德勤 v0.3 R3/R4/R5/R7 四个模块。建议何大人**面试前再 review 一次**（特别是 Boundary 4 边界和 Memory 3 分区，可以直接当"知识库项目"的技术细节补充）。