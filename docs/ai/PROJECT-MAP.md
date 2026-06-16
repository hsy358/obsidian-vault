---
type: project-map
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
---

# PROJECT-MAP.md — Yuanzhi OS

> 轻量版项目地图，基于 Yuanzhi OS 需求文档中提到的模块构建。
> 来源：[需求文档] Yuanzhi OS 竞品架构映射与 AI 重构解析
> 状态：lightweight（第一轮，不追求全量覆盖）

---

## 1. 技术栈概览

| 层级 | 技术选型 |
|---|---|
| 前端框架 | Vue 3 + Tailwind CSS |
| 后端架构 | DDD 微服务（Domain-Driven Design） |
| 主数据库 | PostgreSQL |
| 向量存储 | PgVector |
| 图数据库 | FalkorDB / Neo4j |
| 知识图谱引擎 | GraphITI |
| AI 能力 | PDF解析、长文裂变、文档摘要、多模态 OCR、课程知识图谱 |

---

## 2. 目录结构（推断）

```
yuanzhi-os/
├── src/
│   ├── views/                    # 页面视图
│   │   ├── HomeView.vue          # 首页
│   │   ├── ProgramPlanView.vue   # 人才培养方案视图
│   │   └── KnowledgeGraphView.vue # 知识图谱视图
│   ├── components/ # 公共组件
│   │   ├── TreeSelectWidget.vue # 树形选择组件
│   │   ├── GlobalDock.vue        # 全局停靠栏
│   │   └── AISidebar.vue         # AI 侧边栏
│   ├── api/                      # API客户端
│   │   └── resource.ts # Resource API
│   ├── services/                # 前端服务层
│   │   └── ai/ # AI 相关服务
│   └── store/                    # 状态管理（Pinia/Vuex）
├── server/ # 后端 DDD 微服务
│   ├── controller/               # 控制器层
│   │   └── ResourceController.java
│   ├── service/                 # 业务服务层
│   │   ├── AiChatService.java
│   │   └── ResourceExtractService.java
│   ├── domain/                   # 领域层
│   ├── infrastructure/           # 基础设施层
│   └── repository/              # 仓储层
├── plan-parser/                   # 人才培养方案解析模块
│   └── PlanImportParser.java
└── tests/                        # 测试
```

---

## 3. 主要模块映射

### 3.1 前端模块（Vue 3 + Tailwind CSS）

| 模块 | 类型 | 说明 |
|---|---|---|
| `HomeView.vue` | page | 首页视图 |
| `ProgramPlanView.vue` | page | 人才培养方案视图 |
| `KnowledgeGraphView.vue` | page | 知识图谱视图 |
| `TreeSelectWidget.vue` | component | 树形选择组件（通用） |
| `GlobalDock.vue` | component | 全局停靠栏（AI 能力入口） |
| `AISidebar.vue` | component | AI 侧边栏（对话/任务面板） |

### 3.2 后端模块（Java DDD 微服务）

| 模块 | 类型 | 说明 |
|---|---|---|
| `ResourceController.java` | controller | 资源管理接口 |
| `AiChatService.java` | service | AI 对话服务 |
| `ResourceExtractService.java` | service | 资源提取服务（PDF/OCR） |
| `PlanImportParser.java` | service | 人才培养方案导入解析 |

### 3.3 AI 核心场景相关模块

| 场景 | 涉及模块 | 说明 |
|---|---|---|
| PDF 解析提取指标 | `ResourceExtractService.java`, `ResourceController.java` | 从教学文档提取结构化指标 |
| 长文裂变任务 | `AiChatService.java` | 将长文档拆解为子任务 |
| 文档摘要里程碑 | `AiChatService.java` | 自动生成文档摘要与里程碑节点 |
| 多模态 OCR | `ResourceExtractService.java` | 扫描件/图片文字识别 |
| 课程知识图谱 | `KnowledgeGraphView.vue`, GraphITI | 构建课程知识网络 |

---

## 4. 三大空间与路由映射

### 管理空间（校级管控）

- 校领导：数据看板、专业建设总览
- 教务处管理员：专业建设管理、资源配置

### 专业空间（专业建设）

- 系部主任：专业规划、方案审核
- 专业带头人：课程体系设计、知识图谱构建

### 教师空间（一线教学）

- 一线教师：教案编写、课件生成、AI 辅助教学
- 评审专家：方案评审、反馈

---

## 5. 外部依赖

| 依赖 | 类型 | 说明 |
|---|---|---|
| PostgreSQL | database | 主业务数据库 |
| PgVector | vector-db | 向量嵌入存储（知识图谱检索） |
| FalkorDB / Neo4j | graph-db | 知识图谱存储 |
| GraphITI | engine | 知识图谱构建引擎 |
| AI 大模型 | external | PDF解析、长文理解、OCR 等 AI 能力 |

---

## 6. 数据模型（推断）

| 实体/对象 | 说明 |
|---|---|
| `ProgramPlan` | 人才培养方案 |
| `Course` | 课程 |
| `Resource` | 教学资源（文档/课件） |
| `KnowledgeNode` | 知识图谱节点 |
| `KnowledgeEdge` | 知识图谱边 |
| `AIMission` | AI 任务（如裂变任务、摘要任务） |
| `User` | 用户（多角色） |
| `Role` | 角色（校领导/教务/系部/教师/专家/管理员） |

---

## 7. API 接口（推断）

| 接口 | 方法 | 说明 |
|---|---|---|
| `/api/resource/upload` | POST | 上传教学资源 |
| `/api/resource/extract` | POST | 解析资源（PDF/OCR） |
| `/api/ai/chat` | POST | AI 对话 |
| `/api/ai/mission/split` | POST | 长文裂变 |
| `/api/ai/summary` | POST | 文档摘要 |
| `/api/knowledge/graph` | GET/POST | 知识图谱查询/构建 |
| `/api/program/plan/import` | POST | 人才培养方案导入 |
| `/api/program/plan/list` | GET | 方案列表 |

---

## 8. 状态管理（推断）

| Store | 说明 |
|---|---|
| `useUserStore` | 当前用户信息与角色 |
| `useResourceStore` | 教学资源管理 |
| `useAiMissionStore` | AI 任务状态管理 |
| `useKnowledgeGraphStore` | 知识图谱数据 |

---

*本地图为轻量版，完整分析见 `requirements/yuanzhi_os_analysis/`*