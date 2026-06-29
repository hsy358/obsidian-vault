---
type: requirement-doc
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
title: 01-raw-requirement.md — Yuanzhi OS 竞品架构映射与 AI 重构解析
description: Yuanzhi OS 是一个 AI 原生教学操作系统，目标是全面替代传统 SDS教学管理系统。
tags:
- AI
- docs
---
# 01-raw-requirement.md — Yuanzhi OS 竞品架构映射与 AI 重构解析

> **原始需求原文**，保留歧义，不做改写。

---

## 文档来源

- **文档标题**：Yuanzhi OS 竞品架构映射与 AI 重构解析
- **类型**：需求概述 / 架构规划文档
- **获取方式**：用户直接提供

---

## 原始需求文本

### 一、项目背景与目标

Yuanzhi OS 是一个 AI 原生教学操作系统，目标是**全面替代传统 SDS教学管理系统**。

核心定位：
- AI 原生：从底层架构到交互界面深度融合 AI 能力
- 教学操作系统：覆盖专业建设、人才培养方案管理、一线教学全流程
- 全面替代 SDS：继承并超越现有 SDS 系统的所有功能

### 二、三大空间

Yuanzhi OS 面向三类用户群体，划分为三大空间：

| 空间 | 面向角色 | 核心职能 |
|---|---|---|
| **管理空间** | 校领导、教务处管理员 |校级管控、资源配置、数据决策 |
| **专业空间** | 系部主任、专业带头人 | 专业建设、课程体系设计、知识图谱构建 |
| **教师空间** | 一线教师、评审专家 | 一线教学、教案编写、AI 辅助教学、方案评审 |

### 三、技术架构

**前端**：
- Vue 3 + Tailwind CSS
- 已知组件/页面：HomeView.vue、AiChatService.java、ResourceExtractService.java、TreeSelectWidget.vue、ProgramPlanView.vue、PlanImportParser.java、GlobalDock.vue、AISidebar.vue、KnowledgeGraphView.vue、ResourceController.java

**后端**：
- DDD 微服务架构
- 核心服务：AI 对话服务、资源提取服务、培养方案解析服务

**存储层**：
- PostgreSQL：主业务数据
- PgVector：向量嵌入存储（语义检索）
- FalkorDB / Neo4j：知识图谱存储

**知识图谱引擎**：
- GraphITI：课程知识图谱构建与查询引擎

### 四、AI 核心场景

| 场景 | 说明 |
|---|---|
| **PDF 解析提取指标** | 从 PDF 教学文档（培养方案、教学大纲）中自动提取结构化指标（课程名、学时、学分、考核方式等） |
| **长文裂变任务** | 将长文档（如整本教材、整套培养方案）拆解为可执行的子任务列表 |
| **文档摘要里程碑** | 对长文档自动生成摘要，并识别关键里程碑节点 |
| **多模态 OCR** | 对扫描件、图片型 PDF 进行文字识别，提取教学资源内容 |
| **课程知识图谱** | 基于课程内容构建知识网络，支持知识点关联分析、检索与教学路径推荐 |

### 五、角色矩阵

| 角色 | 归属空间 | 典型操作 |
|---|---|---|
| 校领导 | 管理空间 | 查看数据看板、专业建设总览 |
| 教务处管理员 | 管理空间 | 专业建设审批、资源配置、用户管理 |
| 系部主任 | 专业空间 | 专业规划、方案审核 |
| 专业带头人 | 专业空间 | 课程体系设计、知识图谱构建 |
| 一线教师 | 教师空间 | 教案编写、课件生成、AI 辅助教学 |
| 评审专家 | 教师空间 | 方案评审、反馈 |
| 系统管理员 | （全局） | 系统配置、权限管理 |

### 六、已知的代码模块引用

**前端（Vue 3）**：
- `HomeView.vue`：首页，三大空间入口
- `ProgramPlanView.vue`：人才培养方案视图
- `KnowledgeGraphView.vue`：知识图谱可视化
- `TreeSelectWidget.vue`：树形选择组件
- `GlobalDock.vue`：全局 AI 能力停靠栏
- `AISidebar.vue`：AI 侧边栏对话界面

**后端（Java DDD）**：
- `ResourceController.java`：资源管理 Controller
- `AiChatService.java`：AI 对话服务
- `ResourceExtractService.java`：资源提取服务（PDF/OCR）
- `PlanImportParser.java`：培养方案导入解析

---

## 原始需求中未明确的事项

以下内容在原始需求中**未明确**，需在澄清阶段识别：

1. SDS 系统存量数据如何迁移？
2. 三大空间的具体菜单结构与路由？
3. PDF 解析支持的模板格式列表？
4. 长文裂变的粒度控制策略？
5. 知识图谱节点的评审流程？
6. AI 生成结果的置信度阈值与人工确认机制？
7. 多角色权限的具体矩阵（哪些角色能看到/操作什么）？
8. 各 AI 场景的性能指标要求（SLA）？
9. 外部 AI 大模型的调用方式（直连/中转/私有化部署）？
10. GraphITI 与 FalkorDB/Neo4j 的具体集成方式？

---

*本文件为原始需求，保留原文歧义，不做改写。澄清与分析见02-clarification.md 及后续文档。*