---
title: "刚刚，一篇最全Agent Harness综述来了！"
author: "Datawhale"
publish_date: "2026-05-27 23:58:30"
saved_date: "2026-06-09"
source: "wechat"
url: "https://mp.weixin.qq.com/s/pG39PRnZFjSIxwYcPKD47A"
tags:
  - AI-Agent
  - Agent-Harness
  - 工程化
type: wechat-article
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
  source_url: https://mp.weixin.qq.com/s/pG39PRnZFjSIxwYcPKD47A
---

# 刚刚，一篇最全Agent Harness综述来了！

# Datawhale干货 最新：Agent Harness

分享目前看到最系统、也最工程化的一篇 Agent Harness 综述，CMU、Yale、JHU、Virginia Tech、Amazon 等联合出品：《Agent Harness Engineering: A Survey》。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zW6S9vt0cS8NIWoAfPgbAibamC2iaRjn2yU07PlVHrYwmgQLl3gMOg8V1TctOb4jYmicTGxvGAoj3zOC8GZ6cKylOG4blfniaia4MH0kSo9ZynWQ/640?wx_fmt=png&from=appmsg)

论文主页地址：https://picrew.github.io/LLM-Harness/

这篇论文把 Agent 真正跑起来时，包在模型外面的那层工程系统讲透了。

它用 ETCLOVG 七层框架拆解 Agent Harness，覆盖执行环境、工具接口、上下文管理、生命周期编排、可观测性、验证评估和安全治理。同时梳理了 170+ 个开源 Agent Harness 项目，串起从 Prompt Engineering、Context Engineering 到 Harness Engineering 的工程演进。

---

## 光换模型，可能不是 Agent 最有效的升级

论文开头就提出了一个判断：学术界长期把 Agent 研究重点放在模型上。

模型能不能规划？能不能调用工具？能不能记住上下文？能不能和其他 Agent 协作？这些当然重要。

但问题是，当 Agent 开始进入长任务、真工具、真实环境之后，失败往往不是因为模型"不够聪明"，而是因为系统没把它管好。

论文列了几组结果：

- 有研究只改了编辑工具格式和周边 harness，不改模型本身，编码 benchmark 上最高带来 **10 倍提升**
- 固定的 GPT-5.2-Codex Agent，通过重构系统 prompt、加入中间件上下文注入、自验证 hooks，在 Terminal-Bench 2.0 上从 **52.8% 提升到 66.5%**
- Meta-Harness 通过自动优化 harness，在 Terminal-Bench-2 上做到 **76.4%**，超过手工设计方案

**核心洞察：**

> 同一个模型，换一套执行外壳，表现可以完全不一样。

很多团队还在把问题归因于"模型不够强"。真实情况可能是：模型已经够强了，是你的工具接口、上下文、沙箱、验证和权限系统太弱。

---

## Agent 工程经历了三次迁移

从 2022 到 2026，Agent 工程大概经历了三个阶段：

### 第一阶段：Prompt Engineering

大家主要卷提示词。怎么写 system prompt，怎么放 few-shot，怎么让模型按步骤推理。工程对象很窄，就是把一段输入文本调好。

### 第二阶段：Context Engineering

Agent 开始跑更长的任务后，问题变成：模型每一步到底该看见什么？不是所有资料都塞进去，而是要决定哪些信息该进上下文，哪些记忆要检索，哪些工具结果要压缩，窗口满了怎么办，长期任务中哪些状态要保留。

### 第三阶段：Harness Engineering

当模型已经能处理更复杂任务时，瓶颈转到模型外部：谁来维护状态？谁来调工具？谁来限制权限？谁来注入反馈？谁来验证进度？谁来记录 trace？谁来在失败后恢复？

**三阶段的核心区别：**

| 阶段 | 解决什么问题 |
|---|---|
| Prompt Engineering | 怎么跟模型说话 |
| Context Engineering | 模型该看见什么 |
| Harness Engineering | 怎么让模型在真实世界里可靠干活 |

---

## ETCLOVG 七层框架

一个完整的 Agent Harness 包括七层：

### E - Execution（执行环境）

Agent 在哪里跑？本地、容器、浏览器、桌面、远程沙箱？边界在哪里？

### T - Tooling（工具接口）

工具怎么描述，怎么发现，怎么调用，怎么防止模型乱选工具？

### C - Context（上下文和记忆）

短期上下文、会话状态、长期记忆怎么管理？

### L - Lifecycle（生命周期和编排）

一个 Agent 是单轮执行，还是多轮循环？是一个 Agent 干到底，还是 planner、executor、reviewer 分工？

### O - Observability（可观测性）

每次模型调用、工具调用、检索、报错、重试、token 成本、延迟，都要能追踪。

### V - Verification（验证和评估）

结果对不对？失败到底是模型错了、工具错了、上下文错了，还是测试环境错了？

### G - Governance（治理和安全）

Agent 有什么权限？能不能发邮件、改代码、写数据库？

---

## 面试重点速记

1. **Agent Harness 的本质**：包在模型外层的工程系统，决定了模型在真实环境中的表现
2. **三次工程迁移**：Prompt Engineering → Context Engineering → Harness Engineering
3. **ETCLOVG 七层**：Execution / Tooling / Context / Lifecycle / Observability / Verification / Governance
4. **核心观点**：换模型不一定是升级 Agent 最有效的方式，优化 Harness 可能带来 10 倍提升
5. **170+ 开源项目**：梳理了从提示词工程到 Harness 工程的完整工具链

---

> 论文主页：https://picrew.github.io/LLM-Harness/