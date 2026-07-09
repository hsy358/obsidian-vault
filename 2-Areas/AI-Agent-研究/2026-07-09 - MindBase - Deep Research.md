---
type: github-repo-analysis
repo: yanglongyun/mindbase（原 realuckyang/mindbase）
url: https://github.com/yanglongyun/mindbase
source_article: https://mp.weixin.qq.com/s/um4XCHXEETjrI8gAWS-OdQ
stars: 3
language: Vue + Cloudflare Workers
license: MIT
analyzed_date: 2026-07-09
analyzer: 小助（何大人 7-9 晚授权"自我提升"专项）
tags: [个人记忆中心, AI上下文同步, Cloudflare-Workers, D1-SQLite, MCP, OpenAPI, Anthropic-Skill, 开源, single-source-of-truth, agents-md]
purpose: 直接借鉴到我的"自我提升系统"+ v4 推荐跟踪流程
---

# MindBase — 开源的个人记忆中心

> 来源：深绘 微信公众号文章 + [yanglongyun/mindbase](https://github.com/yanglongyun/mindbase) · MIT · Vue · 3 stars · 2026-05-26 创建
> 这是何大人 7-9 晚发的第二个"自我提升素材"链接（与 Yuxi 形成系列：多租户 Agent + 个人记忆中心）

## 一、一句话定位

**MindBase = 你的个人数据库 + 你的 AI 助理们的共享上下文**——一份 SQLite（D1）数据，多个 AI 通过 OpenAPI / MCP / Skill 共享同一份事实。

## 二、对比 Yuxi（两篇文章一起看）

| 维度 | **Yuxi**（7-9 第一篇）| **MindBase**（7-9 第二篇）|
|---|---|---|
| 形态 | 多租户 Agent 平台 | 个人记忆中心 |
| 受众 | 企业客户 | 个人用户 |
| Stars | 6036 | 3 |
| 部署 | Docker Compose | Cloudflare Workers |
| 存储 | Postgres + Milvus + Neo4j + MinIO | D1 (SQLite) + R2 |
| Agent 引擎 | LangGraph v1 + DeepAgents | 内置 Agent Loop（OpenAI 兼容）|
| 上下文共享 | 知识库 + 知识图谱 | SQL 查询 + Contexts Pin |
| 互通方式 | LangGraph Multi-Agent | OpenAPI / MCP / Skill |
| 加新应用 | 修 schema + 加目录 | 修 schema + 加 4 个文件 + 加 registry |
| 元规则 | 完整 AGENTS.md（4 条准则 + Review + Workflow）| AGENTS.md 加应用契约 + 5 条原则 |

**关键洞察**：Yuxi 是"企业级 Agent Harness 模板"，MindBase 是"个人级 AI 上下文模板"——**我（小助）正好对应 MindBase 这一类**（何大人的个人 AI 助手）。

## 三、MindBase 的 4 大核心机制（重点学习）

### 机制 1：**contexts 表 = 系统级"置顶上下文"**

所有 AI 协作（内部 agent 的 system prompt + 外部协作的 `/api/ai/apps` 响应）都会**首先**读取 `contexts` 表的内容。

```js
// pin 接口（upsert, 同一 source_app+source_id 只存一条）
POST /api/contexts/pin
{ source_app: 'goals', source_id: '<id>', content: '2026年目标:...' }
```

**应用何时 pin**：
- 目标应用：当前 active 目标
- 项目应用：正在进行的项目简介
- 书单：正在读的书
- 健康：用户设定的健康目标

**直接借鉴到我的系统**：
- 我现在的 `MEMORY.md` 顶部「紧挨着的上下文」段 = **软版 pin**（context-recovery 每天注入）
- 但分散在 MEMORY.md 各处（v4 推荐策略 / Goal-Driven Execution / 每日持仓股票 / 何大人强偏好）
- **行动**：明天把这些"永驻信息"显式集中到 MEMORY.md 顶部，标注 `pin: true`

### 机制 2：**schema.sql 是单一事实源**

> "改 schema 删 DB 重建；命名改就所有地方一起改干净。开发阶段保持代码和意图同步，跳过兼容层。"

**直接借鉴到我的系统**：
- `recommendations.json` schema 不严格（之前 v3 推荐字段不统一）
- **行动**：v4 推荐时强制 schema 校验（必填 `operation_plan.stop_loss`、`板块`、`相关性`）

### 机制 3：**事件流（home_events）= 完成度语义的时间轴**

> "有'完成度语义'的关键动作（创建一笔账、读完一本书、目标 +1、达到里程碑）后，往 home_events 写一条 —— 直接 import { insertEvent } from '../home/repository.js'。事件失败时主操作继续完成（try/catch 吞掉）。"

**直接借鉴到我的系统**：
- 我现在每次只写 `daily_review[]` 数组，**没有"完成度事件流"**
- **行动**：v4 跟踪流程里加 `events[]` 字段（推荐发出 / 止损触发 / 大盘熔断 / 跟踪期满 都是事件），让 `recap_log.md` 可以按时间线渲染

### 机制 4：**AGENTS.md = 给 AI 加应用的契约**

> 加新应用就是：**后端 4 个文件 + 前端 1 个文件 + schema 1 段 + registry 1 行**

```
server/apps/<name>/
  manifest.js      ← 声明（应用名/图标/描述）
  repository.js    ← 数据访问
  service.js       ← 业务逻辑
  api.js           ← HTTP 路由
ui/apps/<name>/index.vue
schema.sql        ← 加表
server/apps/registry.js  ← 加 1 行 entry
```

**直接借鉴到我的系统**：
- 我加新 skill / 新 cron 时也是类似结构
- **行动**：未来加 cron 时套这个模板（payload / delivery / state）

## 四、MindBase 的 4 条原则（与 Yuxi AGENTS.md 对齐）

| MindBase 原则 | Yuxi 对应准则 | 借鉴 |
|---|---|---|
| **一致性**（前后端命名统一）| Surgical Changes（不改邻近代码）| ✅ 直接采用 |
| **直接迭代**（DDL 单一事实源，跳过兼容层）| Goal-Driven Execution | ✅ 直接采用 |
| **轻量工程**（按需求做事，留白处保持留白）| **Simplicity First** ⭐ | ✅ 完全对应 |
| **面向用户**（产品文案只面向用户）| —— | ✅ 启发：推荐报告要用户语言 |

**重点**：MindBase 的"轻量工程" = Yuxi 的 "Simplicity First"——**两套独立的项目，同一个核心原则**。这就是我应该坚守的元规则。

## 五、对我（小助）的 7 个具体行动（按优先级）

### P0（今晚可做）

1. **MEMORY.md 顶部"pin"段集中化**（明早做）：把"v4 推荐策略 / Goal-Driven Execution / 何大人强偏好"集中到 `## 🎯 Pinned Context` 段
2. **v4 推荐 schema 严格化**：强制字段 `operation_plan.stop_loss` / `板块` / `相关性`
3. **加 events 流**：`recommendations.json` 加 `events[]` 字段（推荐发出 / 止损触发 / 大盘熔断）

### P1（明天 7-10）

4. **凭证审计**：检查 OpenClaw 配置是否泄漏到 git
5. **明天 v4 推荐时按 schema 校验**，触发 schema 错误就拒绝推荐（强制硬规则）

### P2（本周）

6. **AGENTS.md 模板化**：未来加 cron / 加 skill 时套 MindBase 的"4 个文件 + 1 行 registry"模板
7. **recap_log.md 改成事件流时间线**：按事件渲染而不是按天

## 六、MindBase 启发我的"自我提升系统 v2"（草案）

> 这是脑洞，未实施。等何大人确认。

```
我的 MEMORY.md v2 结构：
├── 🎯 Pinned Context（永驻，每次会话自动加载）
│   ├── 何大人强偏好（称呼 / 风格 / 决策模式）
│   ├── 当前主线任务（v4 推荐 / 持仓分析 / 自我提升）
│   ├── Goal-Driven Execution 准则
│   └── v4 推荐硬约束（3 条）
├── 📚 昨日上下文（context-recovery 注入）
├── 📁 历史归档（按需读，不注入）
└── 🔧 配置（不进 git，gitignore 保护）
```

**核心转变**：从"全文 MEMORY.md 加载"到"Pinned Context + 按需加载"——类似 MindBase 的 `contexts` 表机制。

## 七、风险与权衡

| 借鉴点 | 风险 | 缓解 |
|---|---|---|
| Pin 集中化 | 改一次影响多个下游 | 改动前先备份 MEMORY.md |
| Schema 严格化 | 旧推荐数据可能不兼容 | v4 用新 schema，旧的 completed 不动 |
| 事件流 | 写入逻辑复杂度增加 | 失败 try/catch 吞掉（跟 MindBase 一致）|
| AGENTS.md 模板化 | 加新 skill 流程变长 | 用脚本自动生成 4 个文件 |

## 八、关键参考链接

- [MindBase GitHub](https://github.com/yanglongyun/mindbase)
- [微信公众号文章](https://mp.weixin.qq.com/s/um4XCHXEETjrI8gAWS-OdQ)
- [AGENTS.md 原始](https://github.com/yanglongyun/mindbase/blob/main/AGENTS.md)
- [MindBase 应用商店](https://mindbase.me)

## 九、今晚立即执行 + 明天 7-10 启动

✅ **已完成**：
- 文章本体归档 `公众号文章/2026-05-18 - MindBase 开源的个人记忆中心，同步你与 AI 的上下文.md`
- Deep Research 归档本文档
- v3 失败 + v4 策略已落到改进记录

⏳ **明天 7-10**：
- 9:00 盘前 v4 推荐（按 3 条硬约束 + 新 schema）
- 15:30 收盘跟踪（含 events 流 + 止损自动触发）
- 9:00 / 15:30 cron 修复（避开 API 过载）

⏳ **本周内**：
- MEMORY.md 顶部 pin 段集中化
- 凭证审计
- AGENTS.md 模板化（未来加 cron / skill 时套）
---

## 十、Schema.sql 深度解析（追加于 22:23，按"继续"指令）

> 继续按"先存放和分析"原则深入 MindBase 的 schema 设计——这是最具体可借鉴的部分。

### 10.1 整体结构（321 行）

```sql
-- ============================================================
-- 公共表(对应 system/ 下的基础设施)
-- ============================================================
CREATE TABLE conversations / messages / compactions
CREATE TABLE tokens         -- 外部 AI 接入授权
CREATE TABLE settings       -- 全局 KV
CREATE TABLE contexts       -- 系统级 pin 上下文 ⭐

-- ============================================================
-- 应用 (apps/*)
-- ============================================================
CREATE TABLE home_posts     -- 主页时间轴（用户+AI 共写）
CREATE TABLE home_events    -- 应用事件流 ⭐
CREATE TABLE todos_items    -- <name>_<entity> 命名约定
CREATE TABLE notes_notebooks / notes_pages
CREATE TABLE ledger_entries
CREATE TABLE projects_items
CREATE TABLE profile_blocks
CREATE TABLE llms_keys
CREATE TABLE prompts_items
CREATE TABLE apikeys_items
CREATE TABLE emails_addresses
CREATE TABLE domains_items
CREATE TABLE footprints_visits
```

### 10.2 5 条 schema 设计借鉴点（可直接套用我的 recommendations.json）

#### 借鉴 1：**表命名约定**（裸名 vs `<name>_*`）
- 公共表（基础设施）= **裸名**：`settings / tokens / contexts / conversations / messages`
- 应用表 = **`<name>_<entity>` 命名**：`todos_items / notes_notebooks / notes_pages / ledger_entries`

**套到我的系统**：
- `recommendations.json` 是单一文件不是数据库，但 schema 字段可以分层：
  - 公共字段（顶层）：`version / schema_notes / next_action_policy`
  - 条目字段：`entries[]`（每条 = 应用）
  - 每条内部结构：`<field>` 命名一致（如 `daily_review[] / events[] / stocks[]`）

#### 借鉴 2：**contexts 表设计**（直接对应我"系统级置顶上下文"）

```sql
CREATE TABLE contexts (
  id          TEXT PRIMARY KEY,
  content     TEXT NOT NULL DEFAULT '',
  source_app  TEXT NOT NULL DEFAULT '',  -- 哪个应用 pin 的
  source_id   TEXT,                       -- 源记录 id
  sort_order  INTEGER NOT NULL DEFAULT 0, -- 排序
  created_at  TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at  TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(source_app, source_id)           -- 同一应用同一记录只能 pin 一次
);
```

**套到我的 MEMORY.md v2**：
- 每个 Pinned Context 应该带 `source`（哪条规则 / 哪个决策产生的）
- 应该用 sort_order 控顺序（v4 策略 > Goal-Driven > 何大人强偏好）
- UNIQUE 约束防止重复

#### 借鉴 3：**home_events 表设计**（直接对应 v4 跟踪 events 流）

```sql
CREATE TABLE home_events (
  id          TEXT PRIMARY KEY,
  app         TEXT NOT NULL,                -- 'ledger' / 'books' / 'goals' ...
  action      TEXT NOT NULL,                -- 'created' / 'status_changed' / 'milestone' / 'completed'
  ref_id      TEXT,                          -- 源记录 id, 可空(已删除时仍保留事件)
  summary     TEXT NOT NULL,                 -- 一行人话, e.g. "记了一笔咖啡 ¥18"
  icon        TEXT,                          -- '💰', 渲染快
  created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
```

**v4 推荐 events 流应该长这样**：
```json
{
  "events": [
    {
      "ts": "2026-07-10T09:00:00",
      "app": "stock-rec",
      "action": "recommended",        // 推荐发出
      "ref_id": "2026-07-10-001",
      "summary": "v4 推荐 5 只：医药+消费+有色",
      "icon": "📋"
    },
    {
      "ts": "2026-07-12T15:30:00",
      "app": "stock-rec",
      "action": "stop_loss_hit",      // 止损触发
      "ref_id": "002475",
      "summary": "立讯精密触及止损 67.55 (-9.99%)",
      "icon": "🛑"
    },
    {
      "ts": "2026-07-15T15:30:00",
      "app": "stock-rec",
      "action": "tracking_completed", // 跟踪期满
      "ref_id": "2026-07-10-001",
      "summary": "跟踪 10 日完成，平均 +1.2%",
      "icon": "✅"
    }
  ]
}
```

**关键设计**：
- `ref_id` 可空（推荐被撤回/股票已退市也保留事件）
- `summary` 是一行人话（不写复杂 JSON）
- `icon` 预存（避免渲染时重新计算）

#### 借鉴 4：**初始数据写在 schema.sql 末尾**

```sql
INSERT INTO home_posts (id, author, content) VALUES
  ('welcome-1', 'system', '👋 欢迎使用 MindBase —— ...'),
  ('welcome-2', 'system', '💡 点击右上角打开应用中心 ...');
```

**借鉴到我的 recommendations.json**：
- 推荐条目初始化时应有"placeholder / template"
- 比如 `entry_template.v4` 字段，存储新推荐的默认结构

#### 借鉴 5：**注释即文档（schema 顶部 + 每张表上方都有）**

```sql
-- ============================================================
-- 公共表(对应 system/ 下的基础设施)
-- ============================================================

-- ---- chat:对话(会话 + 消息) ----
CREATE TABLE conversations ( ... );

-- ---- contexts:系统级上下文 —— 用户 / 各应用 pin 进来的内容,所有 AI 协作首先读取 ----
CREATE TABLE contexts ( ... );

-- ---- todos ----
-- 待办:单层清单。
CREATE TABLE todos_items ( ... );
```

**借鉴到 recommendations.json**：
- schema_notes 字段应该有完整的字段说明
- 借鉴到改进记录的 schema 部分

### 10.3 默认值设计哲学

MindBase 大量使用：
- `NOT NULL DEFAULT ''`（空字符串比 NULL 更好处理）
- `NOT NULL DEFAULT 0`（布尔/数字）
- `NOT NULL DEFAULT (datetime('now'))`（时间戳）
- TEXT 主键（不用自增 INT，便于跨表引用）

**借鉴**：
- v4 推荐字段默认值要明确（避免 None）
- 推荐条目 id 用 `YYYY-MM-DD-NNN`（TEXT 主键）而不是自增

### 10.4 索引设计

```sql
CREATE INDEX idx_contexts_sort ON contexts(sort_order ASC);
CREATE INDEX idx_home_events_created ON home_events(created_at DESC);
CREATE INDEX idx_apikeys_items_expire ON apikeys_items(expire_at);
CREATE INDEX idx_domains_items_expire ON domains_items(expire_date);
```

**特点**：所有索引紧跟对应 CREATE TABLE 后；命名 `<table>_<cols>` 清晰。

**借鉴**：v4 tracking_events 应该按 `created_at DESC` 索引（按时间线渲染）。

### 10.5 借鉴清单（不立刻动手，按"先存放和分析"暂缓）

| 借鉴点 | 状态 | 实施时点 |
|---|---|---|
| 表命名约定（裸名 + `<name>_*`）| 📋 已记录 | v4 推荐 schema 设计时 |
| contexts UNIQUE(source_app, source_id) | 📋 已记录 | MEMORY.md v2 设计时 |
| home_events schema 模板 | 📋 已记录 | v4 推荐 events 流设计时 |
| 初始数据写在 schema 末尾 | 📋 已记录 | v4 推荐 entry_template |
| 注释即文档 | 📋 已记录 | recommendations.json schema_notes |
| 默认值哲学 | 📋 已记录 | v4 推荐 schema 严格化时 |
| 索引设计 `<table>_<cols>` | 📋 已记录 | recap_log.md 改成事件流时 |

