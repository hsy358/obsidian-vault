---
type: requirement-index
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
title: Yuanzhi OS竞品架构映射与 AI 重构解析 — 需求分析索引
description: Yuanzhi OS 是一个 AI 原生教学操作系统，通过三大空间（管理/专业/教师）和五大 AI 核心场景（PDF解析、长文裂变、文档摘要里程碑、多模态OCR...
tags:
- AI
- docs
---
# Yuanzhi OS竞品架构映射与 AI 重构解析 — 需求分析索引

> 本目录包含 Yuanzhi OS 项目的完整需求分析资产，基于 AI Native 需求分析技能（`ai-native-requirement-analysis`）生成。

---

## 📋 分析概览

**需求名称**：Yuanzhi OS — AI 原生教学操作系统
**分析状态**：Draft（第一版，17个待确认问题）
**分析日期**：2026-06-09
**分析方法**：Map-first, demand-driven（轻量地图优先 → 业务澄清 → 工程影响 → AC/切片）

---

## 🎯 核心定位

Yuanzhi OS 是一个 AI 原生教学操作系统，通过三大空间（管理/专业/教师）和五大 AI 核心场景（PDF解析、长文裂变、文档摘要里程碑、多模态OCR、课程知识图谱），全面替代传统 SDS 教学管理系统。

---

## 📁 文档索引

| 序号 | 文件 | 说明 | 状态 |
|---|---|---|---|
| 01 | `01-raw-requirement.md` | 原始需求原文（保留歧义） | ✅ |
| 02 | `02-clarification.md` | 业务需求澄清摘要 | ✅ |
| 03 | `03-engineering-impact.md` | 工程影响分析 | ✅ |
| 04 | `04-acceptance-criteria.md` | 验收标准（Given-When-Then） | ✅ |
| 05 | `05-open-questions.md` | 待确认问题追踪（17个） | ✅ |
| 06 | `06-implementation-slices.md` | 实现切片（13个） | ✅ |
| 07 | `07-user-scenarios.md` | 用户场景（10个） | ✅ |
| 08 | `08-use-cases.md` | 用例推导（14个主用例 + 10个隐含用例） | ✅ |
| 09 | `09-process-flows.md` | 流程图（Mermaid +状态机） | ✅ |
| 10 | `10-coverage-matrix.md` | 覆盖矩阵 | ✅ |
| 11 | `11-use-case-inference.md` | 隐含用例推导 | ✅ |
| 12 | `12-capability-flow-graph.md` | 能力流程图谱 | ✅ |
| — | `requirement-graph.json` | 机器可读图谱 | ✅ |
| — | `index.md` | 本文件 | ✅ |

---

## 📊 关键数字

| 维度 | 数量 |
|---|---|
| 用例（主） | 14 |
| 隐含用例 | 10 |
| 用户场景 | 10 |
| 验收标准 AC | 24 |
| 实现切片 | 13 |
| 待确认问题 | 17（P0: 7个，P1: 8个，P2: 2个） |
| 高风险节点 | 4（RISK-001/002/005/008） |
| 缺失能力 | 13 |
| 可复用能力 | 9 |

---

## 🔴 P0 待确认问题（阻塞优先级）

| Q-ID | 问题 | 影响范围 |
|---|---|---|
| Q003 | PDF 解析必须提取的指标字段清单 | AC-003, 核心数据模型 |
| Q004 | 不同院校培养方案模板兼容性策略 | PDF解析准确率 |
| Q006 | 长文裂变最大输入字数限制和分段策略 | 核心AI能力 |
| Q009 | GraphITI 引擎集成方式（REST API / SDK / 直连） | SLICE-04 |
| Q010 | 图数据库选型（FalkorDB vs Neo4j） | 存储层设计 |
| Q012 | 初审和终审是否可以由同一角色担任 | 权限矩阵 |
| Q014 | SDS 数据迁移粒度、方式、过渡期策略 | SLICE-13 |
| Q017 | AI 内容审核机制（实时过滤 vs 后置抽检） | AI输出合规 |

---

## 🏗️ 实现切片优先级

```
Phase 1（AI基础）: SLICE-01 → 02 → 03
Phase 2（图谱核心）: SLICE-04 → 05
Phase 3（业务流程）: SLICE-06 → 07
Phase 4（支撑系统）: SLICE-08 → 09 → 10 → 11
Phase 5（系统管理+迁移）: SLICE-12 →13
```

---

## 🌲 能力流程关键路径

1. **专业建设路径**：R03创建 → R04设计 → R04图谱构建 → R02初审 → R06终审 → 发布
2. **资源处理路径**：上传 → PDF解析/OCR → 指标提取 → 关联课程
3. **AI 任务路径**：发起任务 → AI处理 → 结果确认 → 使用/导出
4. **教案辅助路径**：教师发起 → AI对话 → 内容生成 → 插入编辑器

---

## 🔗 相关全局资产

- `docs/ai/PROJECT-MAP.md` — 轻量版项目地图
- `docs/ai/CAPABILITY-GRAPH.yaml` — 轻量版能力图谱
- `docs/ai/DECISIONS.md` — 决策日志
- `docs/ai/REQUIREMENT-DIFF-LEDGER.md` — 理解偏差追踪

---

*本文档为需求分析索引。详细分析内容见各子文档。*