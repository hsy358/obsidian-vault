---
title: AI-Native R&D 全流程方案 v1.0
author: OpenClaw 小助（综合 13 篇存档文章 + 最新联网搜索）
publish_date: '2026-06-17'
saved_date: '2026-06-17'
type: research-report
okf_metadata:
  schema: okf-v0.1-inspired
  version: 1.0
  inputs:
  - 13 篇 vault/公众号文章（6-14 ~ 6-17）
  - 4 组 web 搜索结果（中英文各 2 组）
status: implementable
description: 1. Harness 先行：基础设施先固化（OpenClaw / Claude Code） 2. Skill 模块化：每个环节一个 Skill，可复用
  3. S...
timestamp: '2026-06-17T00:00:00'
tags:
- AI
- Agent
- Claude
- Harness
- OKF
---
# AI-Native R&D 全流程方案 v1.0

> **目标**：可直接落地实施的"AI 原生研发全流程"方案
> **范围**：从需求到运维，覆盖 7 阶段
> **基线**：OpenClaw + Claude Code + Codex + skill 体系

---

## 一、定位与边界

### 1.1 解决什么问题

| 传统 SDLC | AI-Native SDLC | 关键转变 |
|---|---|---|
| 写代码是核心 | 写规格/编排是核心 | "从写代码到写意图" |
| 8 个中断（随时找开发者）| 3 个 Checkpoint（高价值审查）| "从频繁打断到集中审查" |
| 单 Agent 辅助 | 多 Agent 编排 | "从助手到舰队" |
| 静态流程（n8n）| 动态工作流（AI 写编排）| "从死流程到活编排" |
| 知识散落（文档/注释/人脑）| 统一 OKF 知识库 | "从碎片到标准" |

### 1.2 核心原则

1. **Harness 先行**：基础设施先固化（OpenClaw / Claude Code）
2. **Skill 模块化**：每个环节一个 Skill，可复用
3. **Subagent 隔离**：长任务用 subagent 跑，主上下文干净
4. **OKF 知识化**：所有产物入 vault
5. **/goal 自主**：每个阶段设可验证完成条件
6. **模拟盘不接券商**：金融场景安全铁律
7. **人类在 3 个 Checkpoint**：需求审查 / 架构批准 / 上线门控

---

## 二、参考架构

### 2.1 SDLC 6 层（基于 arxiv 2604.26275）

```
┌──────────────────────────────────────────────┐
│ L6 治理层  OKF 规范 / 安全 / 合规 / 审计     │ ← vault 03-资源
├──────────────────────────────────────────────┤
│ L5 编排层  Dynamic Workflows（6 模式）        │ ← sessions_spawn
├──────────────────────────────────────────────┤
│ L4 知识层  vault + agentic-stack 4 层记忆   │ ← context-recovery
├──────────────────────────────────────────────┤
│ L3 工具层  Skills (67) + MCP + CLI           │ ← workspace/skills
├──────────────────────────────────────────────┤
│ L2 模型层  Claude Code / Codex / OpenClaw    │ ← minimax M2.7/M3
├──────────────────────────────────────────────┤
│ L1 运行时  OpenClaw gateway + 隔离 session   │ ← cron + isolated
└──────────────────────────────────────────────┘
```

### 2.2 6 种 Dynamic Workflow 编排模式（Anthropic）

| 模式 | 用途 | R&D 阶段 |
|---|---|---|
| **Classify and Act** | 分类后路由 | 需求分类 / Bug 分类 |
| **Fan Out and Synthesize** | 多 agent 并行 + 汇总 | 竞品调研 / 多模块并行开发 |
| **Adversarial Verification** | 对抗验证（生成 vs 挑刺）| 测试 / Code Review |
| **Generate and Filter** | 多生成少筛选 | 设计方案 / 文案候选 |
| **Tournament** | 锦标赛多模型 PK | 关键决策（架构方案）|
| **Loop Until Done** | 循环直到完成条件 | /goal 类任务 |

### 2.3 3 个 Checkpoint（augmentcode 模式）

**传统 SDLC**：8 个中断点
**AI-Native SDLC**：3 个 checkpoint
1. **需求审查门**：spec 完成后人工确认（10 min）
2. **架构批准门**：架构方案 + 选型理由确认（30 min）
3. **上线门控**：测试 + 安全 + 性能达标后批准发布（20 min）

人类总投入：~1h/项目（其余时间 AI 跑）

---

## 三、7 阶段 R&D 流程

### 阶段 1：需求 / 立项

**输入**：模糊需求（语音/文字/链接）

**Harness 配置**：
```
工具：ai-native-requirement-analysis skill
subagent：vault/Research 检索同类项目
编排：Fan Out（5 路并行调研）+ Synthesize
/goal：PRD 含 5W1H + 风险清单 + 替代方案
```

**输出**：`/root/vault/Research/{date} - {项目名} - PRD.md`（OKF frontmatter）

**质量门**：
- [ ] PRD 含 5W1H（Why/What/Who/Where/When/How）
- [ ] 风险清单 ≥ 3 条
- [ ] 替代方案 ≥ 2 个
- [ ] OKF metadata 完整

**Checkpoint 1**：需求审查门（何大人 10 min 确认）

---

### 阶段 2：架构 / 设计

**输入**：PRD（已审批）

**Harness 配置**：
```
工具：mck-ppt-design skill（咨询风架构图）
subagent A：库选型调研（vault + web_search）
subagent B：竞品架构对比
subagent C：风险评估
编排：Tournament（3 个架构方案 PK）
/goal：架构图 + 选型理由 + 可行性验证 + 风险缓解
```

**输出**：
- `/root/vault/Research/{date} - {项目名} - 架构方案.pptx`
- `/root/vault/Research/{date} - {项目名} - 选型对比.md`

**质量门**：
- [ ] 架构图清晰（白底+深蓝+红 accent）
- [ ] 选型理由 ≥ 3 个维度对比
- [ ] 风险评估 + 缓解措施

**Checkpoint 2**：架构批准门（何大人 30 min 决定）

---

### 阶段 3：编码 / 实现

**输入**：架构方案（已批准）

**Harness 配置**：
```
工具：Claude Code v2.1.154+（/goal + /deep-research）
subagent A：模块 1 独立开发（隔离 context）
subagent B：模块 2 独立开发
subagent C：模块 3 独立开发
编排：Fan Out（多模块并行）+ Loop Until Done
/goal：代码 + 单元测试 + 集成测试全过
```

**输出**：
- git 仓库（多分支）
- `coverage > 80%` 报告

**质量门**：
- [ ] CI 全绿
- [ ] 单测覆盖率 ≥ 80%
- [ ] Code Review 通过（Adversarial Verification）

---

### 阶段 4：测试 / QA

**输入**：通过 Code Review 的代码

**Harness 配置**：
```
工具：superpowers-systematic-debugging skill
subagent A：边界用例生成
subagent B：性能压测
subagent C：安全扫描
编排：Adversarial Verification（生成用例 vs 攻击用例）
/goal：0 critical bug + p99 < 200ms
```

**输出**：`/root/vault/Research/{date} - {项目名} - QA 报告.md`

**质量门**：
- [ ] 0 critical / 0 high bug
- [ ] p99 < 200ms（或业务定义指标）
- [ ] 安全扫描通过

---

### 阶段 5：部署 / 发布

**输入**：通过 QA 的代码

**Harness 配置**：
```
工具：tencentcloud-lighthouse-skill / deploy-checklist
subagent A：灰度策略
subagent B：回滚方案
subagent C：监控配置
编排：Generate and Filter（多套部署方案 → 选最优）
/goal：灰度发布 + 监控就位 + 0 P0 故障 24h
```

**输出**：
- 线上 URL
- 监控 dashboard
- 应急预案

**质量门**：
- [ ] SLO 定义（错误率 / 延迟 / 可用性）
- [ ] 告警规则配置
- [ ] 回滚演练通过

**Checkpoint 3**：上线门控（何大人 20 min 批准发布）

---

### 阶段 6：运维 / 监控

**输入**：线上服务

**Harness 配置**：
```
工具：node-connect / tavily-search（安全公告）
cron：每天 3 次健康检查
subagent：异常检测
/goal：SLA 99.9% + MTTR < 30min
```

**输出**：
- 每日运维报告（微信推送）
- 月度可用性报告

**质量门**：
- [ ] SLA 达标
- [ ] 故障闭环 < 30min
- [ ] 知识库更新（每次故障沉淀 lesson）

---

### 阶段 7：复盘 / 知识沉淀

**输入**：阶段 1-6 全部产物

**Harness 配置**：
```
工具：context-recovery / copy-editing
subagent：经验提炼
agentic-stack：lesson 候选 → graduated
/goal：可复用 Skill + 知识库更新
```

**输出**：
- `/root/vault/Research/{项目名}/` 完整归档
- 新建/更新 Skill
- 更新 LESSONS.md

**质量门**：
- [ ] 下次同类项目可复用 ≥ 50%
- [ ] 经验沉淀到 agentic-stack
- [ ] 流程缺陷识别 + 下一轮改进

---

## 四、技术选型（基于联网搜索 2026 现状）

### 4.1 模型层

| 用途 | 推荐 | 理由 |
|---|---|---|
| 长任务规划 | Claude Opus 4.5 | 复杂推理强 |
| 快速代码补全 | Claude Sonnet / GPT-5.2 | 平衡速度与质量 |
| 多模型 PK | SiliconFlow | 2.3x 速度 / 32% 延迟降低 |
| 国内备选 | DeepSeek / 智谱 GLM | 成本可控 |

### 4.2 编排层

| 场景 | 工具 | 备注 |
|---|---|---|
| 单任务并行 | sessions_spawn | 阻塞委派 |
| 异步任务 | acp spawn | "稍后回你" |
| 动态工作流 | Claude Code Workflows | 6 种模式 |
| 企业级 | Paperclip | "公司操作系统" 70k stars |
| 国内 | Dify / Coze | 零代码 |

### 4.3 知识层

| 用途 | 工具 | 备注 |
|---|---|---|
| 长期记忆 | agentic-stack 4 层 | personal/working/semantic/episodic |
| 知识库 | vault + OKF 格式 | 已部分应用 |
| 跨天记忆 | context-recovery skill | 新建 |
| 上下文压缩 | OpenClaw 5 层流水线 | 内置 |

### 4.4 工具层

| 工具 | 用途 |
|---|---|
| Claude Code 6 命令 | /goal / /deep-research 等 |
| ppt-production-engine | PPT 自动生成 |
| webapp-testing | Web 应用测试 |
| superpowers-systematic-debugging | 系统性调试 |
| stock-research | 行情分析（已有）|
| context-recovery | 跨天记忆（新建）|

---

## 五、立即落地（1 周内可启动）

### 5.1 短期（1-3 天）

1. **建 r-d-workflow Skill** — 整合 7 阶段 SOP
2. **subagent 编排模板** — 基于 Fan Out / Tournament
3. **3-Checkpoint 流程卡** — 何时叫人、人看什么

### 5.2 中期（1-2 周）

4. **OKF 知识库完整化** — 给存量文章补 metadata
5. **建立经验沉淀机制** — 每次复盘自动写 LESSONS.md
6. **成本监控仪表盘** — subagent 跑多久花了多少 token

### 5.3 长期（1 月+）

7. **自我优化反馈环** — 每阶段产物回灌 skill
8. **Dynamic Workflow 自适应** — AI 现场写编排
9. **多项目并行跑** — 多个 R&D 流水线同时进行

---

## 六、风险与护栏

### 6.1 已知风险

| 风险 | 缓解 |
|---|---|
| AI 生成代码质量不稳 | Adversarial Verification + 单测覆盖率 |
| 上下文污染 | subagent 隔离 + context-recovery |
| Token 失控 | cost 监控 + Loop Until Done 设上限 |
| 模型幻觉 | 知识库 OKF 化 + 引用追溯 |
| 安全漏洞 | 安全扫描 + 灰度发布 |

### 6.2 红线

- 🚫 **金融场景不接券商 API**（模拟盘默认）
- 🚫 **生产环境不直接用 AI 写代码自动部署**
- 🚫 **不跳过 3 个 Checkpoint**
- 🚫 **不复盘就开下一轮**

---

## 七、成功度量

| 指标 | 目标 | 衡量方式 |
|---|---|---|
| 端到端项目周期 | 缩短 60% | 7 阶段总耗时 |
| 人类投入 | 减少 80% | 总人工小时 |
| 代码质量 | 0 critical | Bug 统计 |
| 知识复用率 | ≥ 50% | 同类项目复用比例 |
| 经验沉淀 | 100% 项目复盘 | LESSONS.md 月度增量 |

---

## 八、与其他方案对比

| 方案 | 我们的差异 |
|---|---|
| 传统 SDLC | 7 阶段全自动 + 3 Checkpoint |
| DevOps + AI Copilot | subagent 并行 + Dynamic Workflow |
| 纯 Vibe Coding | 标准化 7 阶段 + OKF 知识库 |
| Paperclip（公司级）| 个人/小团队可立即启动 |
| Claude Code Dynamic Workflows | 整合 6 模式 + 跨天记忆 |

---

## 九、附录：所有引用源

### 9.1 vault 内（13 篇）

- 2026-06-15 让 Claude Code 趁你睡觉就把活干完：使用6个核心命令
- 2026-06-15 Paperclip：开源「AI agent公司操作系统」
- 2026-06-15 别再让 Obsidian 笔记吃灰了
- 2026-06-15 Agent-MemoryForge 2.0
- 2026-06-15 Vercel Labs Zig
- 2026-06-16 Agent Harness 全景解析
- 2026-06-16 Claude Code 架构解析
- 2026-06-16 OpenClaw 24h 股票分析自由
- 2026-06-16 企业流程智能成熟度评估模型
- 2026-06-16 谷歌 OKF 新标准
- 2026-06-16 德勤 2026 趋势解读
- 2026-06-16 国内镜像站
- 2026-06-17 Dynamic Workflows（subagent 浪费上下文）

### 9.2 联网搜索（4 组，2026 最新）

- LTM: SDLC AI Radar 2026 — AI 是 SDLC 核心参与者
- Nitor Infotech: AI-Native SDLC Run Itself 2026
- mavon: 4 Patterns of Agentic SDLC Evolution
- arxiv 2604.26275: Agentic AI in SDLC 6 层参考架构
- Anthropic 2026 Agentic Coding Trends Report
- Mark Kashef: 6 Dynamic Workflows 模式
- Augment Code: Agentic SDLC 3 Checkpoints
- SegmentFault: AI Native 研发模式 /speckit.spec → /speckit.plan → /speckit.tasks
- IBM: 2026 年 AI 智能体指南
- 阿里云: AI 智能体标准化流程

### 9.3 自身体系

- MEMORY.md 长期记忆
- context-recovery skill（新建）
- agentic-stack 4 层记忆
- workspace/skills/ 67 个 skill
- stock-research cron 6 个（已验证 v5 全自动）

---

## 十、行动建议（致何大人）

**1. 立即（今天下午）**：
- 确认 7 阶段划分 ✓
- 确认 3 Checkpoint 位置 ✓
- 确认 Skill 复用现有（不新建）

**2. 明天**：
- 我先建 r-d-workflow Skill（SOP 模板）
- 跑 1 个真实小项目验证（如：context-recovery v2 升级）

**3. 本周内**：
- 跑完整 7 阶段 1 次（用既有项目 PPT 复刻 V2 做验证）
- 输出经验沉淀到 LESSONS.md

**4. 长期**：
- 沉淀成可推广的方案
- 对外讲解（公众号 / 演讲）

---

> **一句话总结**：把 13 篇文章 + 4 组搜索 + 现有 67 个 skill，整合成"7 阶段 + 3 Checkpoint + 6 编排模式"的 R&D 全流程方案，**用 OpenClaw / Claude Code 现有能力就能落地**。
