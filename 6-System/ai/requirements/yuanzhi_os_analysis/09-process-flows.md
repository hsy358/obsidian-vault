---
type: requirement-doc
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
title: 09-process-flows.md — Yuanzhi OS 流程图
tags:
- AI
- docs
---
# 09-process-flows.md — Yuanzhi OS 流程图

>核心业务流程的 Mermaid 流程图与文字描述。

---

## 1. 专业建设完整流程

```mermaid
flowchart TD
    subgraph 创建阶段
        A1[系部主任创建专业规划] --> A2[专业带头人设计课程体系]
        A2 --> A3[专业带头人构建知识图谱]
    end

    subgraph 审核阶段
        A3 --> A4{提交审核}
        A4 -->|通过| B1[教务处管理员初审]
        B1 -->|通过| B2[评审专家终审]
        B1 -->|驳回| A2
        B2 -->|通过| B3[专业发布]
        B2 -->|驳回| A2
    end

    subgraph 教学阶段
        B3 --> C1[一线教师使用 AI 辅助教学]
        C1 --> C2[AI 生成教案/课件]
        C2 --> C3[校领导查看数据看板]
    end
```

**说明**：专业建设从创建到发布的完整流程，包含初审/终审驳回回路。

---

## 2. 资源上传与 AI 解析流程

```mermaid
flowchart TD
    A[用户上传教学资源] --> B{文件格式检测}
    B -->|PDF文本型| C[PDF 解析]
    B -->|图片型PDF| D[OCR 识别]
    B -->|JPG/PNG| D
    D --> E{OCR 成功?}
    E -->|否| F[提示识别失败]
    E -->|是| G[文本内容提取]
    C --> H{解析成功?}
    H -->|否| I[标记需人工补录]
    H -->|是| J[提取结构化指标]
    G --> J
    J --> K[用户确认指标]
    K --> L{确认通过?}
    L -->|是| M[保存至数据库]
    L -->|否| N[手动修正后保存]
    M --> O[关联课程/专业]
    N --> O
```

---

## 3. 长文裂变任务流程

```mermaid
flowchart TD
    A[用户发起长文裂变] --> B{字数检测}
    B -->|< 5000字| C[直接调用 AI裂变]
    B -->|≥ 5000字| D[自动分段]
    D --> E[逐段调用 AI 裂变]
    C --> F[合并子任务结果]
    E --> F
    F --> G{低置信度任务?}
    G -->|是| H[高亮标记需确认]
    G -->|否| I[直接展示结果]
    H --> I
    I --> J[用户编辑确认]
    J --> K[保存子任务列表]
    K --> L[分配给相关教师]
```

---

## 4. 知识图谱构建与评审流程

```mermaid
flowchart TD
    A[专业带头人选择课程] --> B[调用 GraphITI 引擎]
    B --> C[生成课程节点和关系边]
    C --> D[前端可视化展示]
    D --> E[专业带头人编辑图谱]
    E --> F[提交评审]
    F --> G{AI 置信度 ≥ 0.95?}
    G -->|是| H[自动通过无需评审]
    G -->|否| I[通知评审专家审核]
    H --> J[节点发布上线]
    I --> J
    J --> K[节点写入 FalkorDB/Neo4j]
    K --> L[向量嵌入写入 PgVector]
```

---

## 5. 人才培养方案审核流程

```mermaid
flowchart TD
    A[系部主任编辑培养方案] --> B{表单校验}
    B -->|不通过| A2[显示缺失字段]
    B -->|通过| C[提交审核]
    C --> D[专业状态: submitted]
    D --> E[教务处管理员初审]
    E --> F{初审结果}
    F -->|通过| G[专业状态: first-reviewed]
    F -->|驳回| H[状态回退: drafting + 驳回理由]
    G --> I[评审专家终审]
    I --> J{终审结果}
    J -->|通过| K[专业状态: published]
    J -->|驳回| H
    K --> L[通知相关人员]
```

---

## 6. AI 辅助教案编写流程

```mermaid
flowchart TD
    A[教师在教案编辑器点击 AI 辅助] --> B[AISidebar 打开]
    B --> C[教师输入问题或选择模板]
    C --> D[AiChatService 处理请求]
    D --> E{AI 响应成功?}
    E -->|否| F[显示错误提示]
    E -->|是| G[返回 AI 生成内容]
    G --> H[教师预览内容]
    H --> I{插入编辑器?}
    I -->|是| J[内容插入编辑器]
    I -->|否| K[继续对话]
    J --> L[对话历史保存]
    K --> B
```

---

## 7. 空间切换流程

```mermaid
flowchart TD
    A[用户在空间切换器选择目标空间] --> B{有未保存内容?}
    B -->|是| C[提示切换将丢失未保存内容]
    C --> D{用户确认?}
    D -->|取消| E[保持当前空间]
    D -->|确认| F[清空未保存内容]
    B -->|否| F
    F --> G{目标空间有权限?}
    G -->|否| H[提示无权限]
    G -->|是| I[路由跳转目标空间]
    I --> J[更新 store 状态]
    J --> K[加载目标空间首页]
```

---

## 8. 核心状态机

### 8.1 专业方案状态机

```mermaid
stateDiagram-v2
    [*] --> drafting: 创建
    drafting --> submitted: 提交审核
    submitted --> first-reviewed: 初审通过
    submitted --> drafting: 初审驳回
    first-reviewed --> final-reviewed: 终审通过
    first-reviewed --> drafting: 终审驳回
    final-reviewed --> published: 发布
    published --> drafting: 重新编辑（需重新审核）
    published --> archived: 归档
    archived --> [*]
```

### 8.2 AI 任务状态机

```mermaid
stateDiagram-v2
    [*] --> pending: 创建任务
    pending --> running: AI 开始处理
    running --> completed: 成功完成
    running --> failed: 处理失败
    completed --> confirmed: 人工确认
    completed --> [*]
    failed --> pending: 重试
    confirmed --> [*]
```

### 8.3 知识图谱节点状态机

```mermaid
stateDiagram-v2
    [*] --> ai_generated: AI 生成
    ai_generated --> under_review: 提交评审
    ai_generated --> published: 置信度≥0.95自动通过
    under_review --> published: 评审通过
    under_review --> rejected: 评审驳回
    published --> ai_generated: 重新编辑
    rejected --> ai_generated: 修订后重新提交
```

---

*流程图基于08-use-cases.md的用例推导。覆盖矩阵见10-coverage-matrix.md。*