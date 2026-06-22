---
type: requirement-ledger
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
title: REQUIREMENT-DIFF-LEDGER.md — 需求理解偏差追踪
tags:
- docs
---
# REQUIREMENT-DIFF-LEDGER.md — 需求理解偏差追踪

> 记录需求分析过程中发现的理解偏差、误解和修正。

---

## 偏差记录

| ID | 来源 | 原始理解 | 实际情况 | 修正日期 | 影响文档 |
|---|---|---|---|---|---|
| RDL-001 | 需求文档 | GraphITI 是图数据库 | GraphITI 是知识图谱构建**引擎**，底层使用 FalkorDB/Neo4j 存储 | 待确认 | CAPABILITY-GRAPH.yaml |
| RDL-002 | 需求文档 | "SDS教学管理系统"被全面替代 | 需求文档未明确是否存量 SDS 数据如何迁移 | 待确认 | 02-clarification.md |
| RDL-003 | 需求文档 |人才培养方案导入由 PlanImportParser 单独完成 | 与 PDF解析（ResourceExtractService）存在功能重叠，两者的边界需澄清 | 待确认 | 03-engineering-impact.md |

---

*初始版本：基于 Yuanzhi OS 需求文档创建。偏差项将在详细澄清后更新。*