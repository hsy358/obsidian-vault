---
type: research-note
source: web-fetch (loop.pingkai.cn/docs/quickstart)
url: https://loop.pingkai.cn/docs/quickstart
captured_date: 2026-07-01
publisher: 平凯星辰 (Pingkai Xingchen)
related:
  - /root/vault/2-Areas/公众号文章/2026-07-01 - 什么是 Loop？什么是平凯 Loop？.md
  - /root/vault/1-Projects/德勤/AI-Native/笔记/2026-06-29 - AI Native System 产品规划与功能架构开发说明.md
  - /root/vault/1-Projects/德勤/AI-Native/executor/
tags: [平凯, Loop, Agent, 执行器, 德勤-调研, R3]
---

# 平凯 Loop Quickstart 产品调研

> 评估：能否作为德勤 v0.3 的**第二执行器**（跟 Hermes / OpenClaw / Claude Code 并存）

## 一、产品定位（来自 quickstart）

> **Agent and person — Collaborate like colleagues**
> 让人和智能体在同一个团队工作区里协作，消息、任务、执行过程和结果始终连在一起。

**关键概念**：
- **工作区**（workspace）= 默认创建，含 `#all` 频道（公共协作区）
- **机器**（machine）= 跑智能体的本地机器（要装 Loop 客户端或 daemon）
- **智能体**（agent）= 创建在工作区里、绑定到具体机器
- **频道**（channel）+ **@提及** 触发智能体

## 二、5 步上手流程（最小闭环）

```
1. 注册 → 自动建工作区 + 默认 #all 频道
2. 连接第一台机器：loop daemon --server-url <url> --api-key <key>
3. 创建第一个智能体：选 Codex / Claude Code / OpenCode 作为运行环境
4. 在 #all 频道里 @智能体 → 第一次人机协作
```

**核心技术栈**：智能体运行环境 = **Codex / Claude Code / OpenCode**（不是自研，是"调度 + 用户体验包装"）。

## 三、跟德勤 v0.3 架构对比

| 维度 | 平凯 Loop | 德勤 v0.3 目标 | 一致性 |
|---|---|---|---|
| 工作区 | 自动建工作区 + #all 频道 | "项目空间"（Table 8 Row 1）| ✅ 同构 |
| Agent 注册 | 创建智能体 + 选环境 | "Agent 管理 + profile + Skill + 执行器绑定"（Table 16 Row 3）| ✅ 同构 |
| 执行器后端 | Codex / Claude Code / OpenCode | **Hermes / OpenClaw / Claude Code / LangGraph** 多 adapter | ✅ Loop 是适配层设计，**可借鉴** |
| 协作（频道+@mention）| #all 频道 + @智能体 | "协作沟通（频道+线程+@Agent+讨论记录）"（Table 8 Row 5）| ✅ 同构 |
| 任务线程 | "话题"概念 | "任务线程"（Table 9 Row 4）| ✅ 同构 |
| 可观测 | "消息、任务、执行过程和结果始终连在一起" | Table 17 Row 6 "基础日志和调用摘要" | ⚠️ Loop 弱，v0.3 要更强 |
| 沉淀 / Memory | "理解智能体记忆"（文档提到）| Table 16 Row 9 "项目 Memory" | ✅ 同构 |
| 审批 / 风险 | ❌ 文档未提及 | Table 16 Row 8 "人工审批" | ❌ Loop 没有 |
| 部署架构 | SaaS（公测免费） | Table 17 "可单独部署"（R9）| ❌ Loop 是 SaaS，不符合 |

## 四、评估结论

### 🟢 可借鉴
1. **"工作区 + 频道 + @Agent" 三件套** — 平凯 Loop 已验证这是 Agent 协作的最小可用界面
2. **机器（machine）/ 智能体（agent）/ 运行实例** 的三层拆分 — 借鉴到 R3 执行器抽象层
3. **Codex / Claude Code / OpenCode 作为执行器后端** — 跟德勤 v0.3 选的 Codex / Claude Code / Hermes / LangGraph 完全一致（说明业界共识）

### 🔴 不能直接用
1. **SaaS 形态** — 不符合 R9"模块化 + 容器化 + 单独部署"原则
2. **无审批/风险** — 咨询项目必须有审批节点
3. **不能接入 v0.3 已有数据模型** — Loop 是独立产品，不开放 schema
4. **公测期** — 稳定性 + 合规性未验证

### 🟡 试用价值
- **10 分钟注册 + 跑通 5 步** — 可以体验"Loop 范式"在产品层的真实感受
- 体验后**更新评估**：是否值得 fork 平凯 Loop 的前端 / 借鉴其调度逻辑？

## 五、建议行动（何大人决策）

1. **5 分钟抓 loop.pingkai.cn 主站**（不只是 quickstart），看完整功能列表 → 我可以并行抓
2. **你亲自注册体验** → 给我反馈哪个环节流畅 / 卡顿
3. **架构图对比**：我可以画"平凯 Loop vs 德勤 v0.3"对照图（d2 / mermaid）
4. **更新第一阶段研究清单 v2** — 加 "平凯 Loop" 到 R3 / R4 借鉴候选

## 六、参考链接

- 入口：https://loop.pingkai.cn
- Quickstart：https://loop.pingkai.cn/docs/quickstart
- 公司：北京平凯星辰 (Beijing Pingkai Xingchen)
- 公众号背书：[[2026-07-01 - 什么是 Loop？什么是平凯 Loop？|同公司上一篇文章]]