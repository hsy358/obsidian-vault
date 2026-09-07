---
type: research-report
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: openclaw-2026-09-07
title: cangjie-skill — GitHub 仓库研究
description: 1. Project Overview 2. Why Now / Why Hot 3. Core Methodology 4. Architecture 5. Direct Connections to Deloitte MVP 6. Borrowable vs Forced 7. Action Plan
tags:
- AI
- Agent
- Skill
- Knowledge-Distillation
- OpenClaw
- Claude-Code
- DeepSeek-Harness
- Methodology
- Capability-Bundle
- RIA-TV++
- Meta-Skill
source:
  url: https://github.com/kangarooking/cangjie-skill
  fetched: 2026-09-07T07:58+08:00
  by: 小助 via GitHub API (gh CLI 坏, 改用 curl + token)
---

# cangjie-skill — GitHub 仓库研究

**Date:** 2026-09-07
**Prepared for:** 何大人 · Internal Research
**Sources:** https://github.com/kangarooking/cangjie-skill · 中文/日文/英文 README · SKILL.md · CHANGELOG · GitHub API

---

## 1. Project Overview

**cangjie-skill**（仓颉之技）是一个 **meta-skill**——把书、长视频字幕、播客文字稿、课程、访谈、长文等高价值长内容，**蒸馏** 成可被 AI Agent 调用的原子化 skill 工具包。

| 维度 | 信息 |
|---|---|
| **GitHub** | https://github.com/kangarooking/cangjie-skill |
| **作者** | kangarooking（个人开发者） |
| **最新版本** | v2.5.0（2026-08-30） |
| **首发** | 2026-04-16 |
| **语言** | Python（核心），schemas 用 JSON Schema，官网用 Astro |
| **许可证** | MIT |
| **Stars** | **9,579**（4.5 个月，数据飞快） |
| **Forks** | 776 |
| **Size** | 73 MB（repo 整体，包含多本书的产物） |
| **官方网站** | https://cangjie-skill.com/ |
| **兼容执行器** | **OpenClaw**（badge 直接挂 OpenClaw） / Claude Code / DeepSeek Harness（独立 .tgz 插件） |

### 核心一句话

> **「读完、看完、听完之后，带走一套能调用的方法论。」**
> **不是摘要压缩，是结构化复用。**

---

## 2. Why Now / Why Hot

9579 stars / 4.5 个月 / 单人开发——验证了三个趋势叠加：

1. **"把同事蒸馏成 AI" 的潮流**：[nuwa-skill](https://github.com/alchaincyf/nuwa-skill)（蒸馏人，如马斯克 skill）+ [darwin-skill](https://github.com/alchaincyf/darwin-skill)（skill 自动进化）已经出圈。
2. **cangjie-skill 补上"蒸馏内容"维度**：把"人系统性表达过的内容"（书/视频/播客）也蒸馏成 skill。
3. **执行器平台化**：cangjie-skill 同时跑 OpenClaw / Claude Code / DeepSeek Harness——证明"可插拔执行器 + skill 协议"已成行业共识。

**22 个已蒸馏 skill 仓库**（README 列表）证明输出可复制：
- 投资类：buffett-letters-skill（20）/ poor-charlies-almanack-skill（12）/ duan-yongping-skill（15）
- 文案类：viral-copywriting-skill（14）/ copywriters-handbook-skill（12）/ contagious-skill（15）/ influence-skill（12）
- 思维类：first-principles-skill（10）/ cognitive-dividend-skill（15）/ 1000-true-fans-skill（13）
- 国学类：huangdi-neijing-skill（22）/ mao-selected-works-skill（25）/ sunzi-bingfa-skill（8）/ zhouyi-skill（8）
- AI 类：system-prompt-skills（15，165 个 AI 产品 system prompt）/ ai-for-everyone-skill（25）
- X 增长：X-growth-skills（15）

---

## 3. Core Methodology — RIA-TV++（v2.5）

**命名拆解**：
- **RIA** = 赵周《这样读书就够了》的便签拆书法（Reading / Interpretation / Appropriation）
- **TV** = Triple Verification（三重验证）
- **++** = Agent 扩展：E（Execution 可执行步骤）+ B（Boundary 边界）

**七阶段流水线**：

```
阶段 0   Adler 整书理解           → BOOK_OVERVIEW.md（结构/解释/批判/应用四步）
阶段 1   5 个 Agent 并行提取      → 候选方法论单元池
                                  （framework / principle / case / counter-example / glossary）
阶段 1.5 三重验证（知识验证）     → 证据检验 + 用户轻确认
阶段 1.6 独立 Skill 晋级门        → 五判据 + 预算约束（产品化验证）
阶段 2   RIA++ 构造能力卡         → .cangjie/capabilities/cards/<slug>.md (R/I/A1/A2/E/B)
阶段 3   Zettelkasten 链接        → verified.yaml 的 also_read + GLOSSARY.md
阶段 4   压力测试 (darwin 兼容)   → 评测用例 + 诱饵题 + 跨 skill 混淆测试
阶段 5   编译与交付              → cangjie.py compile（single/pack）+ DIGEST.md + 安装包
```

**v2.5 关键变化**（ADR-002，2026-08-30）：阶段 2-4 改为产出 **Capability Bundle**（`verified.yaml` + `cards/*.md`），`single` 和 `pack` 都从同一份 Bundle 编译——保证同一组 `capability_id` 稳定引用。

---

## 4. Architecture

### 4.1 三层产物结构

```
books/<book-slug>/
├── PIPELINE_STATE.md          ← 断点续跑
├── BOOK_OVERVIEW.md           ← 阶段 0
├── verified.md                ← 阶段 1.5 通过的单元
├── GLOSSARY.md                ← 阶段 3 共享术语
├── DIGEST.md                  ← 阶段 5 面向读者精华长文
├── candidates/                ← 阶段 1 原始池
├── rejected/                  ← 阶段 1.5 淘汰 + 原因
└── .cangjie/                  ← v2.5 侧车层（编译事实源 + 运行记录）
    ├── capabilities/          ← verified.yaml + cards/<slug>.md
    ├── runs/<run-id>/         ← 每次编译决策报告
    └── snapshots/             ← 发布前快照（rollback）
```

### 4.2 两种输出模式

| 模式 | 产出 | 适用场景 |
|---|---|---|
| **`single`** | 1 个路由入口 + 能力卡 | 学习/查阅该书 |
| **`pack`** | 1 个来源路由入口 + 少量晋级独立 Skill | 接入日常工作流、跨书组合 |

`select_output_strategy.py` 实现 single-first-v1 auto 决策（不确定时优先 single）。

### 4.3 统一 CLI `scripts/cangjie.py`

v2.5 把 9 个工具收敛成一条命令：
- `doctor`（诊断） / `migrate-legacy`（迁移） / `compile`（编译）
- `replan-output`（输出重规划） / `update`（增量更新） / `repair`（修复）
- `rollback`（回滚） / `eval`（评测） / `benchmark`（基准测试）

**生产级设计**：per-run workdir + 写锁 + staging 校验 + 本地手改检测（三选一保护）+ 原子发布 + 快照回滚。

### 4.4 演进机制

- **内容寻址预处理**（SourceDocument + 结构化 chunk + 确定性缓存）
- **源文档 diff**（chunk 级 → change-set）
- **影响分析**（dependency graph + impact analysis）
- **事务性补丁**（apply_skill_patch.py + 自动回滚）
- **Schema 化契约**（capability / capability-bundle / output-decision / source-manifest / change-set / dependency-graph / eval-suite / failure-case / contracts/source-document / contracts/chunk）

### 4.5 评测工具链

- `run_trigger_evals.py`（固定种子切分 / 盲测任务包 / 判分）
- `run_output_evals.py`（匿名三变体 / 机械断言）
- `benchmark.py`（A 类静态指标 + 过程代理指标聚合）
- 50 条任务集（task-set-v2） + Naval 试点 Bundle 回填

---

## 5. Direct Connections to 何大人's Current Work

> **校准原则（何大人 7-8 明确）**：不强挂钩，只列真有借鉴价值的连接。

### 5.1 🔥 直接可用：把 14 年平安经验蒸馏成 Skill Pack（求职叙事核心）

**论据**：
- cangjie-skill 已经证明："经验 → 多个可调用 SKILL.md + INDEX + DIGEST" 是**可标准化复用的产品形态**。
- 何大人在平安 14 年（金融科技 + 政务数字化 + 智慧城市）方法论密度足够支撑 15-20 个 skill。
- **这正是德勤 AI Native MVP 最硬的论据**——"我不是空谈 AI Native，我把自己的 14 年方法论做成了可调用的 Skill Pack"。

**操作**：
1. 先用 cangjie-skill 蒸馏 1 本自己的"方法论书"（如《平安云交付手册》/《平安 Agent 平台实战》）做 demo
2. 用 demo 直接去德勤面试——"我把自己的 14 年做成了 12 个可调用 skill"

### 5.2 🔥 直接可用：德勤项目"执行器抽象层"已有现成参考实现

**论据**：
- cangjie-skill 的 badge 直接挂 **OpenClaw + Claude Code + DeepSeek Harness** 三个执行器。
- 也就是说，"一个 skill 同时跑在三个执行器"已经被 cangjie-skill 验证可行。
- 何大人 6-29 明确："Hermes / OpenClaw / Codex / Claude Code 等都是可插拔 Agent 执行器"——这正是 cangjie-skill 的架构选择。

**借鉴**：
- 学习 cangjie-skill 的"适配器分层"实现（`dist/` 目录 + `.cangjie/runs/` 决策报告）
- 德勤项目的"执行器抽象层"可以参考同一思路——但**不替换** Hermes（何大人 5-11 / 6-29 已决策 Hermes 是德勤唯一选择）

### 5.3 直接可用：vault PARA 顶层 + 公众号文章 + 笔记可批量蒸馏

**论据**：
- vault 里 342 文件 / 54 篇公众号文章 / 119 个项目文件——**全是 cangjie-skill 的潜在源材料**。
- 蒸馏后能产出"何大人版 skill pack"（`hesiyan-平安-交付-skill` / `hesiyan-德勤-方法论-skill`）。

**操作**：
- 不需要一次蒸馏所有——按 `1-Projects/求职-德勤/` 优先级，只蒸馏德勤面试会聊的领域
- 推荐先试 1 本（如《平安 Agent 平台交付实战》or 何大人自己的某份方法论总结）验证流程

### 5.4 借鉴：7 阶段流水线可借鉴到 Hermes 德勤 MVP

**借鉴点**：
- **Adler 整书理解**（阶段 0）= 任何 AI 任务先做全局理解再拆解 → Hermes 任务接单后第一动作可借鉴
- **三重验证**（阶段 1.5）= Agent 输出后的自我校验机制
- **晋级门**（阶段 1.6）= 哪些方法论值得独立路由，哪些只做能力卡
- **能力卡 RIA++** = Agent 知识表示的统一 schema

**不借鉴**：
- Zettelkasten 链接图——对 MVP 太重
- content-addressed 预处理——对 MVP 太重
- 评测盲测机制——v0 阶段不要做

### 5.5 借鉴：Capability Bundle 作为"输出事实源"

**借鉴点**：
- 德勤 MVP 可以借鉴 **"先有 Bundle，再编译产物"** 思路——任何 Agent 任务先产出"能力卡 + 元数据"，再编译成具体 skill / API / UI。
- 这与"OKF 格式层 + KDD 流程层 + 成熟度评估层"（vault 里 2026-06-16 那份方案）天然契合。

### 5.6 不建议：作为德勤项目的"产品级依赖"

**反对**：
- cangjie-skill 是 meta-skill（蒸馏工具），不是 Agent 框架
- 引入会增加一层依赖，对 MVP 不划算
- 用法应该是**直接装在 OpenClaw 里当工具用**（蒸馏何大人自己的内容），而不是嵌进德勤项目的运行时

---

## 6. Action Plan（按 SIMPLE-FIRST，3 条硬约束）

### 🔴 立即（今天/明天）

**A1. 在 OpenClaw 里装 cangjie-skill，用自己的方法论试一次**
- 验证 skill 真实可用性（不是看 README 吹的）
- 蒸馏对象：何大人自己写过的一份方法论总结（避免无米之炊）
- 验收标准：1 本"书" → 1 个 `pack/` 目录 + 至少 3 个可调用的 SKILL.md

**A2. 同步看 SKILL.md 全文 + methodology/00-overview.md**
- 理解 RIA-TV++ 的 7 阶段细节（这次只看总览，下周再深入）
- 时间预算：30 分钟

### 🟡 1 周内

**B1. 蒸馏 1 份德勤面试用 demo**
- 蒸馏对象候选：①《平安 Agent 平台交付实战》② 何大人自己的某份方法论总结
- 目标：能截图给德勤面试官看 "我把自己 14 年做成了 N 个 skill"

**B2. 给德勤项目借鉴"执行器抽象"思路**
- 在 `/root/vault/1-Projects/德勤/AI-Native/executor/` 里加一份对比笔记
- 标题建议：`2026-09-XX - cangjie-skill 执行器适配 vs Hermes - 借鉴 vs 替代.md`
- **不写** "cangjie-skill 替代 Hermes"——只写"cangjie-skill 在 3 个执行器上跑通的能力"可借鉴

### 🟢 月度

**C1. 评估蒸馏更多书的 ROI**
- 看是否值得把 vault 54 篇公众号文章批量蒸馏成"何大人方法论 skill pack"
- 决策依据：1 本书投入多少时间 → 产出多少 skill → 实际调用频率

---

## 7. References

- **GitHub:** https://github.com/kangarooking/cangjie-skill
- **官网:** https://cangjie-skill.com/
- **v2.5.0 Release:** https://github.com/kangarooking/cangjie-skill/releases/tag/v2.5.0
- **DeepSeek Harness 插件:** https://github.com/kangarooking/cangjie-skill/releases/download/v2.5.0/dsh-cangjie-skill-2.5.0.tgz
- **兄弟项目 nuwa-skill:** https://github.com/alchaincyf/nuwa-skill（蒸馏人）
- **兄弟项目 darwin-skill:** https://github.com/alchaincyf/darwin-skill（skill 演化）
- **依赖 skill video-downloader:** https://github.com/kangarooking/kangarooking-skills/tree/main/video-downloader

### 已蒸馏 skill pack 列表（22 个，按主题分组）

| 主题 | Pack | Skills |
|---|---|---|
| 投资 | buffett-letters-skill | 20 |
| 投资 | poor-charlies-almanack-skill | 12 |
| 投资 | duan-yongping-skill | 15 |
| 文案 | viral-copywriting-skill | 14 |
| 文案 | copywriters-handbook-skill | 12 |
| 文案 | contagious-skill | 15 |
| 文案 | influence-skill | 12 |
| 思维 | first-principles-skill | 10 |
| 思维 | cognitive-dividend-skill | 15 |
| 增长 | 1000-true-fans-skill | 13 |
| 增长 | X-growth-skills | 15 |
| 国学 | huangdi-neijing-skill | 22 |
| 国学 | mao-selected-works-skill | 25 |
| 兵法 | sunzi-bingfa-skill | 8 |
| 易学 | zhouyi-skill | 8 |
| 人物 | sunyuchen-skill | 1（7 capabilities）|
| AI | system-prompt-skills | 15 |
| AI | ai-for-everyone-skill | 25 |
| 视频 | loop-engineering-skill | 8 |
| 综合 | no-rules-rules-skill | 10 |
| 媒体 | qbdx-hub/wo-yu-di-tan-skill | 6 |
| 媒体 | qbdx-hub/mingchao-those-things-skill | 7 |
| 数学 | qbdx-hub/high-math-vol1-ch1-skill | 8 |
