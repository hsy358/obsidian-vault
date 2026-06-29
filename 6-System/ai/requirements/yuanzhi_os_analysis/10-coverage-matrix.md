---
type: requirement-doc
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
title: 10-coverage-matrix.md — Yuanzhi OS 覆盖矩阵
tags:
- AI
- RAG
- docs
---
# 10-coverage-matrix.md — Yuanzhi OS 覆盖矩阵

>需求资产覆盖情况：每个用例对应的角色、AI能力、文件、工程映射。

---

## 1. 用例 × 角色覆盖矩阵

| UC-ID | 校领导 R01 | 教务处管理员 R02 | 系部主任 R03 | 专业带头人 R04 | 一线教师 R05 | 评审专家 R06 | 系统管理员 R07 |
|---|---|---|---|---|---|---|---|
| UC-001 上传教学资源 | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| UC-002 PDF解析提取指标 |❌ | ⚙️ 自动 | ❌ | ⚙️ 自动 | ⚙️ 自动 |❌ | ❌ |
| UC-003 多模态OCR | ❌ | ⚙️ 自动 | ❌ | ⚙️ 自动 | ⚙️ 自动 | ❌ | ❌ |
| UC-004 发起长文裂变 | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| UC-005 生成摘要里程碑 | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| UC-006 构建知识图谱 | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| UC-007 评审图谱节点 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| UC-008 提交专业方案 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| UC-009 初审专业方案 | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| UC-010 终审专业方案 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| UC-011 查看数据看板 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| UC-012 AI辅助编写教案 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| UC-013 配置角色权限 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| UC-014 空间切换 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

> ✅ = 主要执行角色；⚙️ = 系统自动执行

---

## 2. 用例 × AI 能力覆盖矩阵

| UC-ID | PDF解析 | OCR | 长文裂变 | 文档摘要 | 知识图谱 | AI对话 |
|---|---|---|---|---|---|---|
| UC-001 上传资源 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| UC-002 PDF解析 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| UC-003 OCR | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| UC-004 长文裂变 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| UC-005 摘要里程碑 | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| UC-006知识图谱 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| UC-007 评审节点 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| UC-008 提交方案 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| UC-009 初审方案 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| UC-010 终审方案 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| UC-011 数据看板 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| UC-012 AI辅助教案 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| UC-013 权限配置 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| UC-014 空间切换 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## 3. 用例 × 工程模块映射

| UC-ID | 前端页面 | 前端组件 | 后端 Controller | 后端 Service | 数据模型 |
|---|---|---|---|---|---|
| UC-001 上传资源 | 资源上传页 [inferred] | GlobalDock.vue | ResourceController.java | ResourceExtractService.java | resource 表 |
| UC-002 PDF解析 |资源详情页 [inferred] | — | ResourceController.java | ResourceExtractService.java | resource_extracted 表 |
| UC-003 OCR | 资源详情页 [inferred] | — | ResourceController.java | ResourceExtractService.java | resource_text 表 |
| UC-004 长文裂变 | AISidebar.vue | — | [new] AiChatController | AiChatService.java | ai_mission 表 |
| UC-005 摘要里程碑 | 文档详情页 [inferred] | — | [new] AiChatController | AiChatService.java | document_summary, milestone 表 |
| UC-006 知识图谱 | KnowledgeGraphView.vue | TreeSelectWidget.vue | [new] KnowledgeGraphController | GraphitiService.java [inferred] | knowledge_node/edge 表 |
| UC-007 评审节点 | 评审列表页 [inferred] | — | [new] ReviewController | ReviewService.java | milestone_review_log 表 |
| UC-008 提交方案 | ProgramPlanView.vue | — | ProgramPlanController.java | PlanService.java | professional_project 表 |
| UC-009 初审方案 | 管理空间审核页 [inferred] | — | ReviewController.java | ReviewService.java | professional_project, review_log 表 |
| UC-010 终审方案 | 管理空间审核页 [inferred] | — | ReviewController.java | ReviewService.java | professional_project, review_log 表 |
| UC-011 数据看板 | HomeView.vue | — | DashboardController.java [inferred] | DashboardService.java | 统计聚合查询 |
| UC-012 AI辅助教案 | 教案编辑器 [inferred] | AISidebar.vue | AiChatController | AiChatService.java | ai_chat_history 表 |
| UC-013 权限配置 | 系统管理页 [inferred] | — | [new] AdminController | AuthService.java | role, permission, audit_log 表 |
| UC-014 空间切换 | 顶部导航 [inferred] | — | — | — | 路由 + store |

---

## 4. AI 场景 × 工程质量影响等级

| AI 场景 | 影响范围 | 风险等级 | 关键文件 |
|---|---|---|---|
| PDF解析提取指标 | 高（核心教学数据入口） | 🔴 High | ResourceExtractService.java, ResourceController.java |
| 长文裂变任务 | 高（核心 AI 能力） | 🔴 High | AiChatService.java（新增 splitMission） |
| 文档摘要里程碑 | 中（依赖裂变结果） | 🟡 Medium | AiChatService.java（新增 generateSummary） |
| 多模态 OCR | 中（影响资源数字化） | 🟡 Medium | ResourceExtractService.java（OCR 模块） |
| 课程知识图谱 | 高（图谱引擎集成） | 🔴 High | KnowledgeGraphView.vue, GraphitiService.java |

---

## 5. 覆盖缺口记录

| 缺口 ID | 缺口描述 | 来源证据 | 风险 |
|---|---|---|---|
| GAP-01 | 教案编辑器的具体实现未在已知模块中体现 | 需求提到但无文件引用 | 高：AI辅助教案功能无法精确评估工程量 |
| GAP-02 | 站内通知系统的实现未提及 | 需求隐含但无文件引用 | 中：影响任务完成通知、审核催办等 |
| GAP-03 | 审计日志模块未在已知文件中体现 | 需求提到但无文件引用 | 中：影响合规性要求 |
| GAP-04 | 人才培养方案导入（PlanImportParser）与 PDF解析的边界模糊 | 两个模块功能有重叠 | 中：可能导致重复开发或职责不清 |
| GAP-05 | 数据看板（DashboardController）的具体实现完全未知 | 需求提到但无文件引用 | 中：影响校领导核心体验 |

---

*覆盖矩阵基于已知模块推导。缺失模块详见03-engineering-impact.md。*