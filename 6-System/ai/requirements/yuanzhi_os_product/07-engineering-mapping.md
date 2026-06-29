---
type: requirement-doc
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
title: 工程映射 / Engineering Mapping
description: 原始需求中提及了以下研发指引文件（作为工程线索）：
tags:
- AI
- docs
---
# 工程映射 / Engineering Mapping

**文档：** Yuanzhi OS 竞品架构映射与 AI 重构解析
**版本：** v1.0
**日期：** 2026-06-09
**Gate 状态：** ⚠️ BLOCKED

---

> ⚠️ **工程映射前置说明：** 本文档分析时未检测到代码仓库，无法进行实际工程影响分析。所有结论基于原始需求文档中提及的技术栈和研发指引（文件名引用）。相关内容标记为 `待工程确认`，实际工程映射需在代码仓库可用后重新分析。

---

## 1. 技术栈总览

| 层级 | 技术选型 | 来源 | 证据等级 |
|---|---|---|---|
| 前端框架 | Vue 3 + Tailwind CSS | 原始需求 1.3 | confirmed |
| 前端 UI 模式 | 类 Notion/OS 沉浸式多窗口交互 | 原始需求 1.3 | confirmed |
| 后端架构 | DDD 微服务（context/course, program, plan, graph） | 原始需求 1.3 | confirmed |
| 关系型存储 | PostgreSQL | 原始需求 1.3 | confirmed |
| 向量存储 | PgVector | 原始需求 1.3 | confirmed |
| 图数据库 | FalkorDB/Neo4j | 原始需求 1.3 | confirmed |
| AI 工作流 | 审批流中穿插 AI 节点 | 原始需求 1.3 | confirmed |
| 多模态 AI | Qwen-VL / GPT-4o | US-T03 研发指引 | confirmed |
| 知识图谱引擎 | GraphITI | US-T02 研发指引 | confirmed |

---

## 2. 限界上下文（DDD）

| 限界上下文 | 职责 | 核心业务对象 | 状态 |
|---|---|---|---|
| context/course | 教学相关 | CourseStandard, KnowledgeGraph | 计划中 |
| context/program | 专业相关 | ProgramPlan, OBEMatrix, MicroTaskCard | 计划中 |
| context/plan | 培养方案相关 | IndicatorTree, ReviewOpinion | 计划中 |
| context/graph | 图谱引擎 | KnowledgeGraph（GraphITI） | 计划中 |
| context/project | 项目管理 | Project, Milestone | 计划中 |
| context/portfolio | 教师档案袋 | TeacherPortfolio, AchievementRecord | 计划中 |
| context/workflow | 审批流 | FormConfig, WorkflowConfig | 计划中 |

> ⚠️ **assumed：** 限界上下文划分基于原始需求描述，待架构评审确认。

---

## 3. 研发指引文件映射

原始需求中提及了以下研发指引文件（作为工程线索）：

| 研发指引文件 | 用途 | 相关用例 | 建议动作 |
|---|---|---|---|
| `HomeView.vue` + Echarts | 全局数据大盘前端 | UC-M01 | 复用现有组件，扩展 Text-to-SQL 可视化 |
| `AiChatService.java` | AI 聊天服务 | UC-M01 | 复用，新增 Text-to-SQL 模板匹配逻辑 |
| `TreeSelectWidget.vue` | 指标树前端 | UC-M02 | 复用或扩展 |
| `ResourceExtractService.java` | PDF 解析服务 | UC-M02 | 复用，新增 LLM Prompt 调优 |
| `admin_side_web/src/compoents/formRender` | 表单画布 | UC-M03 | 复用，新增拖拽排序和必填配置 |
| `ProgramPlanView.vue` | 人培方案编辑器 | UC-P01 | 新增或扩展 |
| `CoPoMatrix` 实体 | OBE 矩阵 | UC-P01 | 新增，支撑度字段需扩展 |
| `PlanImportParser.java` | 规划文档解析 | UC-P02 | 复用或扩展 AI 裂变功能 |
| `ProgramTasksView.vue` | 任务卡片视图 | UC-P02 | 新增微任务卡片组件 |
| `ProgramProjectsView.vue` | 项目看板 | UC-P03 | 复用，引入拖拽库 |
| `GlobalDock.vue` | 四宫格工作台 | UC-T01 | 复用或扩展 |
| `AISidebar.vue` | AI 侧边栏 | UC-T01 | 新增或扩展 |
| `graph_service/main.py` | GraphITI 服务 | UC-T02 | 复用，新增课程级图谱生成 |
| `GraphApplicationService.java` | 图谱应用服务 | UC-T02 | 复用 |
| `KnowledgeGraphView.vue` | 图谱渲染 | UC-T02 | 新增或扩展 |
| `FileCard.vue` | 文件卡片 | UC-T03 | 复用，新增多文件拖拽 |
| `ResourceController.java` AI 分析接口 | 多模态 OCR | UC-T03 | 复用，新增 Qwen-VL/GPT-4o 集成 |

> ⚠️ **assumed：** 以上文件路径基于原始需求描述，未实际检测代码仓库存在性。待仓库可用后逐一验证。

---

## 4. 影响分析表（待工程确认）

| 需求点 | 现有能力 | 证据等级 | 缺口 | 风险 | 建议实现入口 |
|---|---|---|---|---|---|
| Text-to-SQL 预置模板 | `AiChatService.java` 存在 AI 聊天能力 | inferred | 无 SQL 模板匹配逻辑；无权限网关 | 高（数据泄露风险） | 新增 `SqlTemplateService` 和权限网关 |
| PDF 指标提取 | `ResourceExtractService.java` 存在 PDF 解析 | inferred | LLM Prompt 调优；三级指标树映射逻辑 | 中 | 扩展 `ResourceExtractService`，新增 Prompt 管理 |
| 表单拖拽设计器 | `formRender` 组件存在 | inferred | 缺少字段排序和必填配置持久化；缺少 BPMN 引擎 | 高（工期风险） | 轻量方案：扩展 formRender；完整 BPMN 需二期 |
| AI 任务裂变 | `PlanImportParser.java` 存在文档解析 | inferred | 缺少语义段落裂变逻辑和任务卡片生成 | 高（粒度不明确） | 等 P0-002 澄清后实现 |
| OBE 矩阵 | `CoPoMatrix` 实体存在 | inferred | 缺少可视化组件和支撑度计算 | 中 | 新增 `OBEMatrixView.vue` |
| 项目 Kanban 看板 | `ProgramProjectsView.vue` 存在项目视图 | inferred | 缺少拖拽库和 AI 里程碑提炼 | 中 | 引入拖拽库（dnd-kit 或 vue-draggable） |
| AI 课标生成 | `GraphApplicationService.java` 存在图谱服务 | inferred | 缺少课标生成 Prompt 和人培矩阵拉取逻辑 | 中 | 等 P1-003 澄清后实现 |
| GraphITI 图谱 | `graph_service/main.py` 存在 | inferred | 缺少课程级触发和 FalkorDB 写入 | 中 | 扩展图谱服务 |
| 多模态 OCR | `ResourceController.java` AI 接口存在 | inferred | 缺少 Qwen-VL/GPT-4o 集成和积分计算 | 中 | 等 P1-002/P1-005 澄清后实现 |
| 评审专家权限 | 无相关代码 | missing | 缺少评审意见写入和只读权限拦截 | 高（权限漏洞） | 等 P0-004 澄清后实现 |

---

## 5. 多模态存储架构

```
PostgreSQL (关系型)
├── 用户/角色/权限
├── 人培方案/课程标准/项目
├── 指标树/微任务卡片
└── 积分账户

PgVector (向量)
├── 文档嵌入（PDF 解析后文本向量化）
├── 语义搜索（知识图谱实体相似度）
└── AI 生成内容向量化

FalkorDB/Neo4j (图数据库)
├── 知识图谱实体关系
├── OBE 矩阵支撑关系
└── 课程知识网络
```

---

## 6. API 接口建议（待工程确认）

| 接口 | 方法 | 用途 | 输入 | 输出 |
|---|---|---|---|---|
| `/api/v1/indicator-tree/parse-pdf` | POST | PDF 指标提取 | multipart PDF | 三级指标树 JSON |
| `/api/v1/task-cards/split` | POST | AI 任务裂变 | document ID / file | 微任务卡片列表 |
| `/api/v1/course-standard/generate` | POST | AI 课标生成 | course_id, knowledge_points | 课标草稿 JSON |
| `/api/v1/knowledge-graph/generate` | POST | GraphITI 图谱生成 | course_standard_id | 图谱生成任务 ID |
| `/api/v1/achievement/ocr` | POST | 多模态 OCR | multipart file | 抽取字段列表 + 置信度 |
| `/api/v1/project/milestone/extract` | POST | AI 里程碑提炼 | project_id, document | 里程碑列表 + 预算影响 |
| `/api/v1/sql-template/query` | POST | Text-to-SQL 模板查询 | natural_language_query | 数据图表 JSON |

> ⚠️ **assumed：** API 接口基于推理，待架构评审和代码仓库确认后调整。

---

## 7. 数据库 Schema 建议（核心表）

> ⚠️ **assumed：** 以下 Schema 基于业务对象模型推断，待工程确认。

```sql
-- 指标树
CREATE TABLE indicator_tree (
  id UUID PRIMARY KEY,
  indicator_name VARCHAR(200) NOT NULL,
  level VARCHAR(10) NOT NULL CHECK (level IN ('L1','L2','L3')),
  parent_id UUID REFERENCES indicator_tree(id),
  weight DECIMAL(3,2) NOT NULL CHECK (weight >= 0 AND weight <= 1),
  source_pdf VARCHAR(500),
  status VARCHAR(20) DEFAULT '待提取',
  created_by UUID NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 微任务卡片
CREATE TABLE micro_task_card (
  id UUID PRIMARY KEY,
  task_description TEXT NOT NULL,
  source_paragraph TEXT,
  source_document_id UUID,
  assignee_id UUID,
  due_date DATE,
  status VARCHAR(20) DEFAULT '待领取',
  created_by UUID NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP
);

-- 成果记录
CREATE TABLE achievement_record (
  id UUID PRIMARY KEY,
  teacher_portfolio_id UUID NOT NULL,
  achievement_type VARCHAR(20) NOT NULL,
  title VARCHAR(500) NOT NULL,
  author VARCHAR(200),
  journal_name VARCHAR(200),
  published_year INTEGER,
  doi VARCHAR(200),
  integral INTEGER DEFAULT 0,
  confidence_score DECIMAL(3,2),
  status VARCHAR(20) DEFAULT '待提取',
  source_file_url VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 积分账户
CREATE TABLE integral_account (
  id UUID PRIMARY KEY,
  teacher_id UUID NOT NULL UNIQUE,
  total_integral INTEGER DEFAULT 0,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 评审意见
CREATE TABLE review_opinion (
  id UUID PRIMARY KEY,
  review_object_id UUID NOT NULL,
  review_object_type VARCHAR(50) NOT NULL,
  opinion_content TEXT NOT NULL,
  reviewer_id UUID NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 8. 下一阶段建议

1. **✅ 优先：** 接入代码仓库，执行完整工程影响分析
2. **✅ 优先：** 澄清 P0 问题后更新 `07-engineering-mapping.md`
3. **⚠️ 待定：** GraphITI 引擎集成方式需与 AI 团队确认
4. **⚠️ 待定：** Text-to-SQL 权限网关设计需安全评审
5. **⚠️ 待定：** BPMN 引擎选型（Camunda/Flowable/自研）待技术评审
