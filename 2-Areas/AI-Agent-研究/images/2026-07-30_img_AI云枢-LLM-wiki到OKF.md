---
title: 从 LLM-wiki 到 OKF —— 知识框架架构图
type: document-metadata
file_type: img
file_path: 2026-07-30_img_AI云枢-LLM-wiki到OKF.jpg
source: 微信图片（何大人 2026-07-30 16:30 微信发送；原始公众号：「AI云枢」）
uploaded_date: 2026-07-30
description: |
  信息图（2154×1197 像素，144 KB）。横向布局，三段式架构：

  【左侧 — 各团队的知识库（各写各的）】三种"上游"格式示例：
  1. **Team Wiki**（蓝色 / Markdown 风格）
     ```yaml
     ---
     title: 订单表
     source: bigquery.sales.orders
     tags: [sales, table]
     ---
     ```
  2. **AGENTS.md**（绿色 / YAML frontmatter）
     ```yaml
     ---
     name: 订单表
     description: 订单明细表
     ref: /docs/data/orders.md
     ---
     ```
  3. **Metadata Repo**（黄色 / YAML 实体文件）
     ```yaml
     ---
     entity: table
     title: orders
     location: bq://sales.orders
     labels: {domain: sales}
     ---
     ```

  【中间 — OKF 桥】
  标题：「统一的开放格式」
  中心图标：吊桥（连接左 + 右）
  OKF 核心特点：
  - ✓ 每个文件是一个概念（Concept）
  - ✓ 文件路径即唯一 ID
  - ✓ YAML Frontmatter + Markdown 正文

  【右侧 — 多种消费者（互通复用）】两类下游：
  1. **Agent**（蓝色机器人图标）：
     - 读取知识
     - 检索关联
     - 辅助决策
  2. **Visualizer**（绿色图谱图标）：
     - 关系图谱
     - 结构浏览
     - 影响分析

  【署名】公众号 · AI云枢

image_dimensions: 2154x1197
size_bytes: 144656
classification: image
tags: [OKF, LLM-wiki, 知识框架, 知识库, 格式标准化, Agent, Visualizer, AI云枢, 信息图, 待归档]
status: archived
archive_date: 2026-07-30
archive_path: /root/vault/2-Areas/AI-Agent-研究/images/
archived_from: 0-Inbox
---

# 从 LLM-wiki 到 OKF —— 信息图结构化解析

> **一句话判断**：这张图把"LLM-wiki 时代的知识碎片化"问题，**用一座桥的结构画出来**——左侧是各团队**各写各的**3 种格式（Wiki / AGENTS.md / Metadata Repo），中间是 **OKF 桥（统一的开放格式）**，右侧是 2 类**互通复用**的消费者（Agent / Visualizer）。核心论点：**统一格式是上下游解耦的前提**。

## 一、图谱定位

| 维度 | 信息 |
|---|---|
| 类型 | 公众号信息图（横向布局，三段式架构） |
| 来源 | 公众号「AI云枢」 |
| 尺寸 | 2154×1197（横向 banner 比例） |
| 大小 | 144 KB |
| 核心元素 | 左侧 3 个"上游格式" + 中间 OKF 桥 + 右侧 2 类"下游消费者" |
| 视觉隐喻 | 中间用**吊桥**（suspension bridge）连接两侧——OKF 就是桥 |

> 图中三段用**虚线箭头**连接（说明不是强耦合，是适配关系）。桥的中央写着"OKF"+"统一的开放格式"。

## 二、三段式结构详解

### 2.1 左侧：各团队的知识库（各写各的）

| 来源 | 格式 | 关键字段 | 典型代表 |
|---|---|---|---|
| **Team Wiki** | Markdown + frontmatter | `title` / `source` / `tags` | Notion / Confluence / 本地 Wiki |
| **AGENTS.md** | YAML frontmatter | `name` / `description` / `ref` | Claude Code / OpenClaw 的 agent skill 定义 |
| **Metadata Repo** | YAML 实体文件 | `entity` / `title` / `location` / `labels` | DataHub / Amundsen / 数据资产目录 |

**作者判断**：这 3 种格式在企业内部**并存但互不兼容**——同一份"订单表"知识，可能在 3 个系统里写 3 遍。

### 2.2 中间：OKF 桥 —— 核心特点

| # | 特点 | 含义 |
|---|---|---|
| 1 | **每个文件是一个概念（Concept）** | 一个 .md = 一个独立语义单元，不是混合大杂烩 |
| 2 | **文件路径即唯一 ID** | `/1-Projects/德勤/README.md` 就是这个项目的唯一标识，不需要 UUID |
| 3 | **YAML Frontmatter + Markdown 正文** | 机器读 frontmatter，人类读正文；不需要数据库 |

**OKF = Open Knowledge Format**（Google Cloud 推出，何大人 6-22 已研究）。

### 2.3 右侧：多种消费者（互通复用）

| 消费者 | 能力 | 对应实现 |
|---|---|---|
| **Agent** | 读取知识 / 检索关联 / 辅助决策 | OpenClaw / Claude / Codex / Hermes |
| **Visualizer** | 关系图谱 / 结构浏览 / 影响分析 | Datacore / Obsidian Graph |

**关键判断**：因为 OKF 是纯文本 + frontmatter，**不需要数据库**，所以 Agent 和 Visualizer 都**直接读文件系统**——上游格式变化只要能转 OKF，下游就**零成本兼容**。

## 三、跟何大人现状的强对照（这是核心价值）

### 3.1 三段全映射

| 图中位置 | 何大人 vault 对应 | 状态 |
|---|---|---|
| **左侧 Team Wiki 风格** | `2-Areas/公众号文章/` + `2-Areas/AI-Agent-研究/`（OKF frontmatter 笔记） | ✅ 已有 |
| **左侧 AGENTS.md 风格** | OpenClaw skill 定义 + `/root/.openclaw/workspace/skills/` | ✅ 已有 |
| **左侧 Metadata Repo 风格** | Datacore 索引（基于 Dataview） | ✅ 已有 |
| **中间 OKF 桥** | vault 所有 `.md` 的 frontmatter + tags 体系 | ✅ 部分实现 |
| **右侧 Agent** | AgentSpace 5 harness（OpenClaw / Claude / Codex / Hermes） | ✅ 已有 |
| **右侧 Visualizer** | Datacore 插件（关系图谱 / 结构浏览 / 影响分析） | ✅ 已有 |

**结论**：何大人的 vault **已经是"左→OKF→右"的完整实例**——只是没有显式化（没有一个 README 声明这套架构）。

### 3.2 三段之间缺失的"适配器"

| 缺失环节 | 问题 | 建议 |
|---|---|---|
| **左侧 → 中间** | 公众号文章、skill 定义、Datacore 索引三种格式**已经都在用 OKF frontmatter**，但**没强制 schema** | 建一个 OKF schema 规范（哪些字段必填、哪些可选） |
| **中间 → 右侧** | Agent 能读 .md（OpenClaw filesystem tools），但 Visualizer（Datacore）**只能从结构化 frontmatter 推关系**，无法自动从正文提取 | 给 Datacore 加 NLP 实体提取（成本高，暂缓） |
| **右侧 → 左侧的反馈** | Agent 改 vault 后**没有 resync** 链路——Harness Handbook 的思路正好填这个 | 参考 Harness Handbook 的 resync 流水线 |

## 四、可能的延伸应用

### 4.1 自身 vault（直接相关）

按图作者建议的"统一开放格式"思路，何大人可以：

1. **建一份 OKF schema 文档**：`/root/vault/6-System/standards/OKF-schema-何大人版.md`
   - 强制字段：`title` / `tags` / `created_date` / `source`
   - 可选字段：`author` / `description` / `related`
   - 不强制但建议：`status` / `archive_date`
2. **写一篇「vault 是如何演化成 OKF 闭环的」对外讲稿**：可直接挂到德勤面试 / 求职博客

### 4.2 德勤项目（间接挂钩，按 6-29 决策）

德勤 MVP 的核心架构难题就是"**多种格式 → 统一消费**"：

| 内部来源 | 格式 | 德勤 MVP 需要统一到 |
|---|---|---|
| 业务文档 | Word / PDF / Markdown | OKF |
| 数据库 schema | DDL / DataHub metadata | OKF |
| Agent skill 定义 | AGENTS.md | OKF |
| 业务规则 | Decision table | OKF |

**借鉴点**：用 OKF 桥做"格式适配层"，让上层 Agent / Visualizer 都从 OKF 读，不需要为每种格式写 adapter。

### 4.3 求职差异化（按 6-30 决策）

德勤面试若问"你怎么设计企业知识中台"：

1. 直接画这张三段式图（左侧 3 种上游 + 中间 OKF 桥 + 右侧 2 类消费者）
2. 关键论述点：**格式适配 vs 统一 schema**——选 OKF 是因为它**纯文本 + 不需要数据库**，迁移成本最低
3. 引用 Google Cloud OKF v0.1 规范 + 何大人 vault 实际落地案例

→ 体现"**系统抽象 + 工程取舍**"思维，不是某个技术点的深度。

## 五、立即可做

1. ✅ **本次已完成**：图归档 + sidecar + 结构化解析
2. ⏳ **可选**：写一份 `/root/vault/6-System/standards/OKF-schema-何大人版.md`，明确 vault 的 OKF 字段规范（让左→中转换有标准）
3. ⏳ **可选**：在 `/root/vault/2-Areas/AI-Agent-研究/` 下加一份 `2026-07-30 - 知识框架三段式（OKF 桥）+ 何大人 vault 现状映射.md`，把上面 3.1 / 3.2 表格展开
4. ⏳ **可选**：跟之前那张 SaaS 知识库图对比，整理成一份"**企业知识库完整架构**"对外讲稿（含 OKF 桥层 + 4 层架构图）

## 六、引用与可能延伸

- **OKF 规范来源**：Google Cloud OKF v0.1（何大人 6-22 已研究，存档于 `2-Areas/AI-Agent-研究/2026-06-22 - Google Cloud OKF Open Knowledge Format.md`）
- **OKF 与 vault 差异 audit**：`2-Areas/AI-Agent-研究/2026-06-22 - OKF 与 vault 差异 audit 表.md`
- **同主题前一张图**（今天归档）：SaaS 企业知识库技术全景（始图号）—— 4 层架构（生产端 → 治理 + 检索 → LLM Wiki 派生视图 → 用户体验）
- **Harness Handbook resync**：今天归档的另一篇研究——**代码改了之后如何滚动知识**，正好对应右侧消费者 → 左侧的反馈