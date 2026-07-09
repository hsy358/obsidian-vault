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