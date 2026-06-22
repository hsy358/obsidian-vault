---
type: requirement-doc
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
title: 03-engineering-impact.md — Yuanzhi OS 工程影响分析
description: Yuanzhi OS 是一个 AI 原生教学操作系统，通过 Vue 3 + Tailwind CSS 前端和 DDD 微服务后端构建，覆盖三大空间（管理/专业/...
tags:
- AI
- docs
---
# 03-engineering-impact.md — Yuanzhi OS 工程影响分析

> 分析 AI 核心场景对现有工程的影响，包括匹配到的模块、可复用能力、缺失能力、冲突点和推荐实现入口。

---

## 1. 需求摘要

Yuanzhi OS 是一个 AI 原生教学操作系统，通过 Vue 3 + Tailwind CSS 前端和 DDD 微服务后端构建，覆盖三大空间（管理/专业/教师）和七类角色。AI 核心场景包括 PDF 解析、长文裂变、文档摘要里程碑、多模态 OCR、课程知识图谱五大能力。

---

## 2. 现有上下文检查

**已检查文件**：
- PROJECT-MAP.md（轻量版，基于需求文档推断）
- CAPABILITY-GRAPH.yaml（轻量版）
- 需求文档中列出的已知模块清单

**证据等级说明**：
- `[verified]`：已读代码确认
- `[inferred]`：基于路径/命名推断，未完整确认
- `[planned]`：只存在于文档/路线图/需求文本
- `[missing]`：搜索未发现

---

## 3. 匹配到的现有模块

### 3.1 前端模块

| 模块 | 证据等级 | 匹配场景 | 说明 |
|---|---|---|---|
| `HomeView.vue` | [planned] | 首页/数据看板 | 需求提到但未读取源码，三大空间入口需确认 |
| `ProgramPlanView.vue` | [planned] | 培养方案编辑/提交 | 需求提到但未读取源码 |
| `KnowledgeGraphView.vue` | [planned] | 知识图谱可视化 | 需求提到但未读取源码 |
| `TreeSelectWidget.vue` | [planned] | 课程/章节多级选择 | 需求提到但未读取源码 |
| `GlobalDock.vue` | [planned] | 全局 AI 入口 | 需求提到但未读取源码 |
| `AISidebar.vue` | [planned] | AI 对话/任务面板 | 需求提到但未读取源码 |

### 3.2 后端模块

| 模块 | 证据等级 | 匹配场景 | 说明 |
|---|---|---|---|
| `ResourceController.java` | [planned] | 资源上传/解析接口 | 需求提到但未读取源码 |
| `AiChatService.java` | [planned] | AI 对话/裂变/摘要 | 需求提到但未读取源码，splitMission/generateSummary 方法待确认 |
| `ResourceExtractService.java` | [planned] | PDF解析/OCR | 需求提到但未读取源码，OCR 模块是否独立待确认 |
| `PlanImportParser.java` | [planned] | 培养方案导入 | 需求提到但未读取源码，与 PDF 解析边界模糊 |

### 3.3 存储层

|组件 | 证据等级 | 说明 |
|---|---|---|
| PostgreSQL | [planned] | 主业务数据库，schema 未知 |
| PgVector | [planned] | 向量存储，集成方式未知 |
| FalkorDB/Neo4j | [planned] | 图数据库，选型未确定 |
| GraphITI Engine | [planned] | 知识图谱引擎，API 接口未知 |

---

## 4. 可复用能力

| 能力 ID | 能力名称 | 所在模块 | 复用场景 | 复用方式 |
|---|---|---|---|---|
| CAP-001 | `resource.upload` | `ResourceController.java` | 资源上传通用能力 | 直接复用 |
| CAP-002 | `resource.pdf-extract` | `ResourceExtractService.java` | PDF 解析提取 | 扩展字段提取规则 |
| CAP-003 | `resource.ocr` | `ResourceExtractService.java` | OCR 识别 | OCR 模块复用 |
| CAP-004 | `ai.chat` | `AiChatService.java` | AI 对话基础能力 | 扩展裂变/摘要方法 |
| CAP-005 | `kg.frontend` | `KnowledgeGraphView.vue` | 图谱可视化 | 扩展节点编辑功能 |
| CAP-006 | `ui.tree-select` | `TreeSelectWidget.vue` | 树形选择 | 复用至课程选择 |
| CAP-007 | `ui.global-dock` | `GlobalDock.vue` | 全局停靠栏 | 扩展 AI 能力入口 |
| CAP-008 | `ui.ai-sidebar` | `AISidebar.vue` | AI 侧边栏 | 扩展任务类型 |
| CAP-009 | `page.home` | `HomeView.vue` | 角色首页 | 扩展数据看板 |

---

## 5. 缺失能力

| 能力 ID | 能力名称 | 优先级 | 影响范围 | 阻塞场景 |
|---|---|---|---|---|
| MISS-001 | `ai.doc-split` 方法 | P0 | `AiChatService.java` | 长文裂变无法实现 |
| MISS-002 | `ai.summary` 方法 | P0 | `AiChatService.java` | 摘要里程碑无法实现 |
| MISS-003 | `mission.tracking` 面板 | P1 | 前端新增组件 | 用户无法追踪任务状态 |
| MISS-004 | `milestone.review` 流程 | P0 | 新增 ReviewService | AI 里程碑无法评审发布 |
| MISS-005 | `audit.logging` | P1 | 后端新增模块 | 合规审计要求不满足 |
| MISS-006 | `notification.system` | P1 | 前端+后端 | 任务完成/催办无法通知 |
| MISS-007 | `kg.conflict-detection` | P1 | `GraphitiService.java` | 图谱覆盖/追加策略无法执行 |
| MISS-008 | `ai.content-moderation` | P1 | `AiChatService.java` | AI 输出合规风险 |
| MISS-009 | `plan.version-history` | P2 | `ProgramPlanView.vue` + 后端 | 方案历史版本无法查看 |
| MISS-010 | `resource.versioning` | P2 | `ResourceController.java` | 资源多版本无法管理 |
| MISS-011 | `data.migration` (SDS) | P0 | 新增迁移模块 | 存量 SDS 数据无法迁移 |
| MISS-012 | `space.session-isolation` | P1 | 前端 store | 空间切换时状态管理 |
| MISS-013 | `common.batch-operation` | P2 | ReviewController | 批量评审无法支持 |

---

## 6. 可能受影响文件

### 6.1 直接受影响文件（高风险）

| 文件 | 影响类型 | 影响原因 | 变更描述 |
|---|---|---|---|
| `ResourceController.java` | 修改 | 新增资源解析触发器接口 | 增加解析状态查询和回调接口 |
| `ResourceExtractService.java` | 修改 | PDF解析和 OCR 能力扩展 | 增加裂变任务输入处理、指标提取规则 |
| `AiChatService.java` | 修改 | 新增长文裂变和摘要方法 | 增加 splitMission()、generateSummary()、evaluateMission() 等方法 |
| `KnowledgeGraphView.vue` | 修改 | 图谱节点编辑功能扩展 | 增加节点增删改、关系编辑功能 |
| `GlobalDock.vue` | 修改 | 全局 AI 入口扩展 | 增加新的 AI 能力入口（长文裂变、摘要） |
| `AISidebar.vue` | 修改 | AI 任务类型扩展 | 增加任务状态追踪面板、取消/重试功能 |

### 6.2 间接受影响文件（中风险）

| 文件 | 影响类型 | 影响原因 |
|---|---|---|
| `PlanImportParser.java` | 需澄清 | 与 PDF 解析功能边界模糊，可能需要整合或明确分工 |
| `HomeView.vue` |扩展 | 数据看板增加 AI 使用统计、专业建设进度等指标 |
| `TreeSelectWidget.vue` | 扩展 | 增加知识图谱节点选择的专业范围筛选 |
| `ProgramPlanView.vue` | 扩展 | 增加 AI 摘要展示、里程碑节点展示 |

### 6.3 新增文件需求

| 新文件 | 类型 | 说明 |
|---|---|---|
| `MissionTrackingPanel.vue` | 前端组件 | AI 任务状态追踪面板 |
| `MilestoneReviewPanel.vue` | 前端组件 | 里程碑评审面板 |
| `AiChatController.java` | 后端 Controller | AI 对话/裂变/摘要接口封装 |
| `ReviewController.java` | 后端 Controller | 评审接口 |
| `ReviewService.java` | 后端 Service | 评审业务逻辑 |
| `GraphitiService.java` | 后端 Service | GraphITI 引擎集成 |
| `NotificationService.java` | 后端 Service | 站内通知服务 |
| `AuditLogService.java` | 后端 Service | 审计日志服务 |
| `ContentModerationService.java` | 后端 Service | AI 内容合规审查 |

---

## 7. 行为变化

### 7.1 ResourceExtractService.java 行为变化

**当前行为**（推断）：
- 接收文件流，提取 PDF 文本，返回结构化字段

**新行为**：
- 增加长文裂变任务输入处理（超长文本分段）
- 增加 OCR 模块调用（图片型 PDF）
- 增加指标置信度返回（用于判断是否需人工确认）

**兼容性**：
- 现有 PDF 解析接口需保持向后兼容（参数不变）
- 新增可选参数 `options: { enableOcr: boolean, confidenceThreshold: number }`

### 7.2 AiChatService.java 行为变化

**当前行为**（推断）：
- 基础 AI 对话，多轮对话上下文管理

**新行为**：
- 增加 `splitMission(text)` 方法：长文裂变
- 增加 `generateSummary(docId)` 方法：文档摘要里程碑
- 增加 `evaluateMission(missionId)` 方法：AI 任务评估
- 任务状态管理（pending/running/completed/failed/confirmed）

**兼容性**：
- 现有对话接口 `/api/ai/chat` 需保持向后兼容

### 7.3 KnowledgeGraphView.vue 行为变化

**当前行为**（推断）：
- 只读展示知识图谱节点和关系

**新行为**：
- 支持节点增删改
- 支持关系编辑
- 支持图谱构建进度展示
- 支持评审状态展示

**兼容性**：
- 现有只读视图需在功能开关控制下兼容（feature flag）

### 7.4 GlobalDock.vue / AISidebar.vue 行为变化

**当前行为**（推断）：
- 固定的 AI 入口和对话面板

**新行为**：
- AISidebar 新增任务类型选择（对话/裂变/摘要/图谱）
- AISidebar 新增任务追踪面板（显示进行中/已完成任务）
- GlobalDock 新增长文裂变和摘要快捷入口

**兼容性**：
- 现有 AI 入口保持兼容，新增入口以增量方式添加

---

## 8. 集成风险

| 风险 ID | 风险描述 | 风险等级 | 影响范围 | 缓解策略 |
|---|---|---|---|---|
| RISK-001 | GraphITI引擎集成方式未知（REST API / SDK / 直连） | 🔴 High | GraphitiService.java | Q009: 明确集成方式 |
| RISK-002 | 图数据库选型未确定（FalkorDB vs Neo4j） | 🔴 High | 存储层 | Q010: 确认选型 |
| RISK-003 | PlanImportParser 与 ResourceExtractService 功能重叠 | 🟡 Medium | 后端服务职责划分 | Q004: 明确边界 |
| RISK-004 | AI 大模型私有化部署方式未确定 | 🟡 Medium | AiChatService.java | 明确调用方式（网关/直连） |
| RISK-005 | SDS 数据迁移策略缺失 | 🔴 High | 数据层 | Q014: 明确迁移策略 |
| RISK-006 | AI 响应时延影响用户体验 | 🟡 Medium | 前端 UI | 增加 loading 状态和超时处理 |
| RISK-007 | 知识图谱节点评审流程缺失 | 🟡 Medium |评审功能 | MISS-004: 新增 ReviewService |
| RISK-008 | 内容合规审查机制缺失 | 🟡 Medium | AI 输出 | Q017: 明确审核机制 |

---

## 9. 与现有实现的冲突

| 冲突 ID | 冲突描述 | 涉及文件 | 冲突类型 | 解决方案 |
|---|---|---|---|---|
| CONFLICT-001 | PlanImportParser（培养方案导入）与 ResourceExtractService（PDF解析）职责重叠 | `PlanImportParser.java` vs `ResourceExtractService.java` | 功能重叠 | 明确边界：PlanImportParser 处理 Excel/Word，ResourceExtractService 处理 PDF/图片 |
| CONFLICT-002 | 知识图谱节点状态机（`ai_generated → published`）与现有专业方案状态机存在关联 | `KnowledgeNode` vs `ProfessionalProject` | 状态联动 | 定义状态联动规则：图谱节点发布不影响方案状态，但方案发布需图谱节点已发布 |
| CONFLICT-003 | 空间切换时 store 状态是否清空未定义 | 前端 store | 设计冲突 | Q013: 确认空间切换策略 |
| CONFLICT-004 | AI 任务异步处理与现有同步 API 设计冲突 | `AiChatService.java` | 接口设计 | 新增 `/api/ai/mission/*` 异步接口组，与现有 `/api/ai/chat` 共存 |

---

## 10. 工程驱动的澄清问题

| Q-ID | 问题 | 影响范围 | 澄清对象 |
|---|---|---|---|
| Q009 | GraphITI 引擎集成方式（REST API / SDK / 直连）？ | GraphitiService.java 设计 | 技术负责人 |
| Q010 | 图数据库选型（FalkorDB vs Neo4j）？ | 存储层设计 | 技术负责人 |
| Q014 | SDS 数据迁移粒度、方式、过渡期策略？ | 数据层迁移设计 | 产品经理 |
| Q017 | AI 内容审核机制（实时过滤/后置抽检）？ | AiChatService.java | 产品经理/合规 |

---

## 11. 推荐实现入口

| 区域 | 入口文件 | 证据 | 操作 |
|---|---|---|---|
| 前端 -资源上传 | `GlobalDock.vue` | [planned] | 扩展上传入口，增加解析状态展示 |
| 前端 - AI 侧边栏 | `AISidebar.vue` | [planned] | 新增任务类型和追踪面板 |
| 前端 - 图谱可视化 | `KnowledgeGraphView.vue` | [planned] | 扩展节点编辑功能 |
| 后端 - 资源解析 | `ResourceController.java` | [planned] | 新增解析状态回调接口 |
| 后端 - AI 服务 | `AiChatService.java` | [planned] | 新增 splitMission / generateSummary 方法 |
| 后端 - 图谱引擎 | `GraphitiService.java` | [missing] | 新建文件封装 GraphITI API |
| 后端 - 评审服务 | `ReviewService.java` | [missing] | 新建文件实现评审逻辑 |
| 后端 - 通知服务 | `NotificationService.java` | [missing] | 新建文件实现通知发送 |
| 后端 - 审计日志 | `AuditLogService.java` | [missing] | 新建文件实现审计日志 |

---

## 12. 假设

- 当前工程使用 Vue 3 + Tailwind CSS，路由使用 Vue Router，状态管理使用 Pinia（推断）
- 后端采用 Spring Boot DDD 架构，Controller → Service → Repository 分层（推断）
- GraphITI 引擎提供 HTTP REST API 封装
- AI 大模型通过内部网关调用（私有化部署）
-存储层 PostgreSQL 和 PgVector 共用同一数据库实例
- 站内消息通过 WebSocket 或轮询实现实时通知

---

*工程影响分析完成。AC 和实现切片详见04-acceptance-criteria.md 和06-implementation-slices.md。*