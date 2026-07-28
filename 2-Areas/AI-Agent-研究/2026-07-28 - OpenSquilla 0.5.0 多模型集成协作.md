---
type: ai-agent-research
title: OpenSquilla 0.5.0 Preview — 多模型集成协作登顶 DRACO 双榜
source: 视频介绍 + GitHub + 量子位报道
discovered_at: 2026-07-28
status: 调研中
tags: [ai-agent, multi-model-routing, harness, cost-optimization, opensquilla, draco, hermes-借鉴]
related: [德勤/AI-Native, Hermes Agent v0.14, AgentRouter]
---

# OpenSquilla 0.5.0 Preview — 多模型集成协作登顶 DRACO 双榜

> **一句话总结**：OpenSquilla 不是"换更强的模型"，而是"换更好的组织方式"——4 个国产模型并行提案 + 1 个模型聚合，在 DRACO 榜单上**性能超 Opus 4.8 / 跑平 Fable 5，成本只花零头**。

## 📊 关键数据（DRACO 深度研究榜单 2026-07-06 发布）

### Brave Search 组（OpenSquilla 双榜第一）
| 方案 | 平均分 | 平均任务成本 | 备注 |
|---|---|---|---|
| **OpenSquilla 集成** | **64.09** | **$0.12** | 唯一同时拿下"最高分+最低成本"双标记 |
| Opus 4.8 | 59.11 | - | **+8.42% 分 / 成本 -92%** |
| GPT-5.5 | 53.28 | - | **+20.27% 分 / 成本 -86%** |

### DuckDuckGo 组
| 方案 | 平均分 | 平均任务成本 |
|---|---|---|
| **OpenSquilla 集成** | **60.85** | **$0.39** |
| Fable 5（Anthropic 最新旗舰） | 59.80 | $1.21 |

> 视频里说 60.82 vs 59.80，量子位原文是 60.85 vs 59.80——DuckDuckGo 组基本**打平 Fable 5，成本是 1/3**。

## 🏗️ 核心机制：多样性采样 + 共识聚合

- **4 个国产模型并行提案**（DeepSeek v4 / GLM-5.2 / Kimi K2.7 / Qwen3.7）
- **1 个模型聚合输出**（同一个集合里的某位，或单独选）
- **没有海外旗舰模型**（纯国产阵容）
- 互相补位：弥补单一模型漏信息源、算错数值、顾不全约束的固有短板

## 🧬 版本演进（一以贯之"少烧钱、真交付"）

| 版本 | 核心特性 |
|---|---|
| v0.1.0 | 智能路由（按任务难度自动选模型） |
| v0.2.0 | 一键迁移（从其他 Agent 框架切换） |
| v0.3.0 | **MetaSkill** 自组织技能协议 |
| v0.4.0 | **可验证编码**（红绿回归证据链）+ 签名桌面版 |
| v0.5.0 Preview | **多模型集成协作**（harness 层多模型路由） |

## 🔍 与 OpenClaw 关系

> "在 OpenClaw 基础上做的创新，路由和 MetaSkill 是它自己加的核心功能。" —— 苏米客

**这意味着**：OpenSquilla 走的是 **OpenClaw 思路的 Python 重写 + 商业化路线**，**不是 OpenClaw 的子项目**。

## 🏢 商业背景

- **团队**：基元律动（TokenRhythm）
- **首轮融资**：估值 1 亿美元
- **产品主张**：提升单位成本的 Agent 智能
- **GitHub**：https://github.com/opensquilla/opensquilla（6,295 stars，Apache-2.0）
- **技术报告**：《Agentic Routing》—— 阐述 harness 原生路由如何把日常 agent 流量转化为自我进化的数据飞轮

## ⚖️ 核心判断

### 1. 证明了一个趋势
> 国产基础模型单拎出来与海外旗舰仍有差距，但在 **Harness 层组织得当**的前提下，混用国产模型已能在真实任务上跑出更高、更稳的分数——即便面对最新一代旗舰，也能在**成本只有零头**的情况下咬住甚至反超。

### 2. 与德勤项目 MVP 的强关联

| OpenSquilla 特性 | 借鉴到 Hermes 德勤 MVP |
|---|---|
| 多模型路由（4 国产并行+1 聚合） | **执行器抽象层**核心能力（AgentRouter 已具备雏形） |
| 智能路由（按任务难度选模型） | Hermes dispatcher 的任务分级 |
| 成本节省 92% | **商务极强卖点**（企业级 Agent ROI 论证） |
| 国产模型矩阵 | 符合德勤客户**国产化合规**要求（金融/政务） |
| 可验证编码（红绿回归） | Hermes 当前**可能缺**这一层 |
| MetaSkill 自组织技能 | 类似德勤的"工作流模板市场"概念 |

### 3. 与 Hermes v0.14 的关系（明确边界）
- **不替代**：OpenSquilla 是 harness 层组织方式，Hermes 是 Agent 框架
- **借鉴点**：
  - 多模型并行提案 → Hermes MultiAgent 模式
  - 红绿回归证据链 → Hermes 工具调用的可验证性增强
  - MetaSkill 协议 → Hermes 的 Skill 自组织设计参考
- **风险点**：基元律动首轮估值 1 亿美元 → 商业化压力下开源协议可能收紧（虽然现在是 Apache-2.0）

## 🎯 行动建议

1. **立即可做**：在 Hermes v0.14 上验证"多模型并行提案 + 聚合"模式（不依赖 OpenSquilla，自己实现 adapter）
2. **短期研究**：读 OpenSquilla《Agentic Routing》技术报告 → 摘出可借鉴的数据飞轮设计
3. **中期规划**：在德勤 MVP 的"成本论证"PPT 里引用 DRACO 榜单数据（**60.85 分 vs Fable 5 59.80，成本 1/3** 这个数字非常能打）
4. **持续观察**：基元律动后续动作（如果开源协议变更 / 商业版定价 / API 化）

## 📚 参考资料

- GitHub: https://github.com/opensquilla/opensquilla
- 量子位 2026-07-06: https://www.qbitai.com/2026/07/443863.html
- Trendshift: https://trendshift.io/repositories/30002
- 苏米客深度分析: https://www.xmsumi.com/detail/3400
- DRACO 榜单：与 OpenSquilla 团队论文同步发布
