---
type: requirement-index
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
---

# Yuanzhi OS 产品需求澄清与分析

**产品：** Yuanzhi OS（AI 原生教学操作系统）
**分析文档：** 竞品架构映射与 AI 重构解析
**版本：** v1.0
**日期：** 2026-06-09
**Gate 状态：** ⚠️ **BLOCKED**（4 个 P0 阻塞问题待澄清）
**分析模式：** Mode 0（需求完整性体检）+ Mode 0.5（需求澄清会话）

---

## 文档索引

### 核心资产

| 文档 | 说明 | Gate 前置状态 |
|---|---|---|
| **[00-requirement-completeness-audit.md](./00-requirement-completeness-audit.md)** | 需求完整性体检 · Ambiguity Gate | — |
| **[00A-clarification-session.md](./00A-clarification-session.md)** | 需求澄清会话 · Clarification Loop（第1轮） | BLOCKED |
| **[00B-clarification-summary.md](./00B-clarification-summary.md)** | 澄清结论摘要（等待回复） | 待澄清 |
| **[01-raw-requirement.md](./01-raw-requirement.md)** | 原始需求（保留原文，不消除歧义） | — |
| **[02-product-analysis.md](./02-product-analysis.md)** | 产品需求分析 | ⚠️ assumed |
| **[03-business-object-model.md](./03-business-object-model.md)** | 业务对象模型（字段/状态/权限） | ⚠️ assumed |
| **[04-use-cases-and-flows.md](./04-use-cases-and-flows.md)** | 用例与流程推演 | ⚠️ assumed |
| **[05-open-questions.md](./05-open-questions.md)** | 待确认问题跟踪 | pending |
| **[06-acceptance-criteria.md](./06-acceptance-criteria.md)** | 验收标准（Given-When-Then） | ⚠️ assumed |
| **[07-engineering-mapping.md](./07-engineering-mapping.md)** | 工程映射（无仓库，待工程确认） | 待工程确认 |

---

## 核心结论

### Gate 结论

> **⚠️ BLOCKED**
> 存在 **4 个 P0 阻塞问题**，不确认就继续会导致方向错误、权限越界、状态流转错误或数据结构返工。
> 必须先完成 Mode 0.5 澄清会话，再进入产品分析和工程映射。

**综合完整性评分：49/100**

### P0 阻塞问题（必须澄清）

| ID | 问题 | 来源 | 澄清对象 |
|---|---|---|---|
| **P0-001** | Data Copilot Text-to-SQL 权限模型 | UC-M01 | 产品经理/安全负责人 |
| **P0-002** | AI 任务裂变粒度与状态机 | UC-P02 | 产品经理/业务负责人 |
| **P0-003** | 表单拖拽配置器配置边界 | UC-M03 | 产品经理/技术负责人 |
| **P0-004** | 评审专家在专业空间的具体权限 | 第二章 | 产品经理/业务负责人 |

### P1 高风险问题（默认假设推进）

| ID | 问题 | 默认假设 | 风险 |
|---|---|---|---|
| P1-001 | PDF 指标提取映射规则与失败兜底 | 人工确认后写入；失败提示手动导入 | 低 |
| P1-002 | 教师档案袋积分计算规则 | 预置类型系数；首版仅展示累计 | 中 |
| P1-003 | AI 课标生成人机交接点 | AI 生成草稿→人工确认→正式 | 低 |
| P1-004 | GraphITI 图谱生成范围与触发 | 课程级手动触发，结果存 FalkorDB | 低 |
| P1-005 | OCR 字段覆盖与文件限制 | 固定字段集；单文件≤50MB；档案袋≤50文件 | 低 |
| P1-006 | AI 里程碑提炼触发时机 | 手动触发，用户确认后扣减预算 | 中 |
| P1-007 | 跨空间数据权限边界 | 系部主任仅看本专业数据 | 中 |

---

## 产品范围摘要

### 三大空间

| 空间 | 核心功能 | 关键角色 |
|---|---|---|
| 🏢 **管理空间** | 全局数据大盘、评价考核中枢、底层配置底座 | 校领导、教务处管理员、系统管理员 |
| 🎯 **专业空间** | 人培方案研制、建设规划裂变、项目看板管理 | 系部主任、专业带头人、评审专家 |
| 👩‍🏫 **教师空间** | 四宫格工作台、课程标准研制、教师档案袋 | 一线教师 |

### 核心技术

- **DDD 微服务**：context/course, program, plan, graph, project, portfolio, workflow
- **多模态存储**：PostgreSQL + PgVector + FalkorDB/Neo4j
- **AI 引擎**：大模型 + GraphITI 知识图谱 + Qwen-VL/GPT-4o OCR
- **前端**：Vue 3 + Tailwind CSS，类 Notion/OS 沉浸式多窗口

---

## 关键默认假设

> 所有 assumed 内容在澄清后需更新为 confirmed。

| ASSUM | 内容 | 错误影响 |
|---|---|---|
| ASSUM-001 | Text-to-SQL 首版仅预置模板 | 若需自由 SQL，需新增安全机制 |
| ASSUM-002 | AI 任务裂变按语义段落 | 若粒度不同，Schema 需重设 |
| ASSUM-003 | 表单设计器首版轻量配置 | 若需完整 BPMN，工期翻倍 |
| ASSUM-004 | 评审专家只读+评审意见 | 若需驳回，需新增状态和字段 |
| ASSUM-005 | AI 指标提取失败兜底为手动导入 | 无兜底时 AI 失败会导致流程卡死 |
| ASSUM-006 | 积分首版仅展示累计 | 若需兑换，需新增账户和事务 |
| ASSUM-007 | AI 课标生成需人工确认后转正式 | 无交接点会导致数据质量风险 |
| ASSUM-008 | GraphITI 图谱课程级手动触发 | 若需全校图谱，需新增合并策略 |
| ASSUM-009 | OCR 支持固定字段集 | 若需更多字段，需扩展 Prompt |
| ASSUM-010 | AI 里程碑手动触发用户确认后扣减 | 自动触发若无标准，会产生误判 |
| ASSUM-011 | 系部主任仅看本专业数据 | 跨专业对比场景受限 |

---

## 建议下一步

1. **🔴 立即：** 产品经理/业务负责人回复 `00A-clarification-session.md` 中的 4 个 P0 问题
2. **🟡 澄清后：** 执行 Clarification Apply，回写所有资产，更新 Gate 结论
3. **🟡 澄清后：** 接入代码仓库，执行 `07-engineering-mapping.md` 完整工程影响分析
4. **🟢 确认后：** 进入 `08-implementation-slices.md` 实现切片规划（面向 Claude Code/Codex）
5. **🟢 确认后：** 生成 `09-test-plan.md` 测试计划

---

## 质量门状态

- [ ] 业务目标清楚 → ⚠️ 有总目标但未量化
- [ ] 角色权限清楚 → ⚠️ 7 个角色已识别但权限细则缺失
- [ ] 业务对象清楚 → ❌ 核心对象仅有名称，字段/状态/生命周期全缺失
- [ ] 主/分支/异常流程清楚 → ⚠️ 主流程有，分支/异常全缺失
- [ ] 关键动作的前置/后置/状态变化清楚 → ❌ 全缺失
- [ ] 数据校验/重复提交/并发/失败/回滚/通知/审计清楚 → ❌ 全缺失
- [ ] 可验证的 Given-When-Then AC → ❌ AC 完全缺失（58 条中 51 条基于假设）
- [ ] P0/P1/P2 问题列出并提供默认假设 → ✅ 已完成
- [ ] Gate 结论 → ✅ BLOCKED
- [ ] Clarification Apply → ⏳ 等待回复
