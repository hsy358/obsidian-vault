---
type: github-repo-analysis
repo: xerrors/Yuxi
url: https://github.com/xerrors/Yuxi
stars: 6036
forks: 876
license: MIT
language: Python (FastAPI) + Vue 3
analyzed_date: 2026-07-09
analyzer: 小助（何大人 7-9 晚授权"自己做主 + 自我提升"专项）
tags: [agent-harness, knowledge-base, rag, knowledge-graph, langgraph, lightrag, mcp, fastapi, vue, milvus, neo4j, deepagents, multi-tenant, agents-md]
purpose: 借鉴到股票推荐 / 持仓分析 / 自我提升框架
---

# Yuxi（语析）— 多租户 Agent Harness + 企业知识库

> 来源：[xerrors/Yuxi](https://github.com/xerrors/Yuxi) · **6036 stars** · MIT · 最新 push 2026-07-09
> 在线文档：https://xerrors.github.io/Yuxi/
> 作者：江南大学软件工程博士生 wenjie.zhang@stu.jiangnan.edu.cn（求职中，研究方向 AI Agent / 知识图谱 / 大模型应用）
> 注：这是 7-9 何大人给 @HSY 自我的"提升素材"

## 一、一句话定位

**Yuxi 是 LangGraph v1 + LightRAG + FastAPI + Vue 3 的多租户 Agent Harness 平台**——
- 用户可在类 ChatGPT 界面与"挂载了 Skills + MCP + 子智能体 + 沙盒工具"的智能体对话
- 每个智能体的回答带 **引用来源 + 知识图谱推理 + 可交付产物**
- 管理员配置知识库 / 模型 / 权限；用户用对话触发 RAG 检索 + 图谱推理

## 二、技术栈一览

| 层 | 技术 |
|---|---|
| 前端 | Vue 3 · Vite · Pinia |
| 后端 | FastAPI · **LangGraph v1** · ARQ（异步 worker）|
| 存储 | PostgreSQL · Redis · MinIO · **Milvus** · **Neo4j** |
| 文档解析 | **MinerU** · PaddleX · RapidOCR · DeepSeek OCR |
| Agent 框架 | 直接引入 **DeepAgents**（langchain-ai）|
| 部署 | Docker Compose（含 sandbox-provisioner 沙盒服务）|

## 三、架构代码地图（ARCHITECTURE.md 的精髓）

Yuxi 的 `ARCHITECTURE.md` 是一份**只描述稳定系统边界**的文档（参考 matklad 的建议），核心不变量：

1. **HTTP 路由层保持薄**：路由层只做请求解析 + 认证 + 响应装配，领域逻辑都在 `yuxi.services`
2. **持久化查询集中在 `yuxi.repositories`**：路由不能绕过 repository 直接操作模型
3. **前端 API 集中在 `web/src/apis`**：组件不散落拼后端 URL
4. **Agent 能力 = Context + Middleware + Toolkits + Backends 组合**：知识库通过工具访问，不硬编码进单页面
5. **LITE_MODE 必须可用**：跳过知识库 / 图谱 / 评估重依赖
6. **沙盒虚拟路径边界（`SANDBOX_VIRTUAL_PATH_PREFIX`）**：用户路径与宿主机路径严格分离

**后端代码地图**：
```
backend/
├── server/                  ← FastAPI 应用入口（薄路由层）
│   ├── main.py
│   ├── routers/             ← HTTP 路由边界
│   ├── utils/               ← 生命周期/认证/日志
│   └── worker_main.py       ← worker 入口
└── package/yuxi/            ← 业务包（核心）
    ├── agents/              ← LangGraph 智能体
    │   ├── BaseAgent
    │   ├── buildin/         ← 内置智能体
    │   ├── middlewares/     ← 把知识库/Skills/MCP/附件挂到运行时
    │   ├── toolkits/        ← 工具注册 + 内置工具
    │   └── backends/        ← 沙盒 / Skills 外部执行后端
    ├── services/            ← 用例层（跨模块流程入口）
    ├── repositories/        ← SQLAlchemy 查询
    ├── storage/             ← postgres / minio
    ├── knowledge/           ← 知识库 + 图谱领域
    │   ├── KnowledgeBaseManager
    │   ├── implementations/ ← Milvus / Dify
    │   ├── graphs/          ← 知识图谱适配
    │   └── chunking/        ← 文档分块
    ├── knowledge/parser/    ← MinerU/PaddleX/OCR 边界
    ├── models/              ← chat/embedding/rerank 适配
    └── config/              ← 应用配置 + 内置模型信息
```

**一次典型智能体对话链路**：
```
AgentView (Vue)
  → web/src/apis
  → /api/chat (server/routers/chat_router.py)
  → yuxi.services.chat_service / agent_run_service
  → 读 conversation + agent config + tools + skills + knowledge
  → 后台 run 队列（ARQ worker）
  → LangGraph 智能体执行
  → 运行事件写 Redis，最终状态写 Postgres，文件落 MinIO / 沙盒
  → SSE/轮询 → 前端消费事件流 → 渲染消息 / 工具 / 引用 / 产物
```

## 四、🎯 AGENTS.md — 这才是给我"自我提升"最关键的素材

> **重点**：Yuxi 的 `AGENTS.md` 是目前我见过的**最简洁最可执行的 Agent 自我约束规则**——4 条开发准则直接命中 v3 推荐 -16.79% 失败的根因。

### 准则 1：Think Before Coding
> **Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- Restate the request as the smallest acceptance criteria（先把验收标准说清楚）
- State your assumptions explicitly（明确假设）
- If multiple interpretations exist, present them - don't pick silently（多个解读就摆出来，不要闷头选一个）
- If a simpler approach exists, say so（更简单的方案就直说）

**→ 借鉴到我**：每天推荐前，**先把"我会按什么规则推荐"用 5 行写出来**，不要闷头拉数据。

### 准则 2：Simplicity First
> **Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked（不做超出需求的功能）
- No abstractions for single-use code（单用例不抽抽象）
- No "flexibility" / "configurability" that wasn't requested（不要没必要的灵活度）
- If you write 200 lines and it could be 50, rewrite it

**→ 借鉴到我**：v3 推荐时我加了 4 条"如果大盘跌 1% 减仓 30%"的规则但没执行——这就是"speculative feature"。**v4 推荐规则要最少，最多 3 条硬约束**。

### 准则 3：Surgical Changes
> **Touch only what you must. Clean up only your own mess.**

- Don't "improve" adjacent code（不"顺便"改邻近代码）
- Don't refactor things that aren't broken（不重构没坏的代码）
- Match existing style（匹配现有风格）
- The test: Every changed line should trace directly to the user's request（每行改动都能追溯到用户需求）

**→ 借鉴到我**：每次复盘**只针对"今天亏的那一笔"分析 + 改进**，不要顺便改整套策略。

### 准则 4：Goal-Driven Execution ⭐
> **Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

**→ 借鉴到我**（这条最关键）：v3 推荐跟踪失败的核心就是**没有 verifiable goal**——
- ❌ "推荐 5 只 AI 产业链股" → 没有 verify 机制（涨跌没有 if-then 触发）
- ✅ v4 应该是："每天推荐 5 只 → 每日 15:30 复盘盈亏 → 跌 -10% 自动写失败反思"（**每个步骤都有 verify**）

### Review 准则（4 步）

1. **先确认主路径和关键场景能跑**（如果不清楚，要求先验证）
2. **审查当前方案是不是上下文最优解**（更简洁方案存在时不要直接重写，先说取舍）
3. **检查过度设计 / 过度防御 / 过度嵌套**（识别"为不存在的需求加代码"）
4. **认真评估测试价值**（"给出靶子后评估靶子"的低价值测试建议清掉）

### 调试工作流（核心原则）

1. **Docker Compose 优先**：开发跑在容器里，本地热重载，不假设本地裸跑
2. **改完必须测试**：单测 / 集成 / e2e 按风险等级选
3. **绝不放过度的防御/回退机制**（"用 fallback 掩盖设计缺陷"是反模式）

### 其他治理规范（值得借鉴）

- **需求沟通规范**：需求不明确时主动挖细节，对齐验收标准，需求/改动较大时在 `docs/vibe/` 建日期文档
- **变更清单**：每次改完更新 `docs/develop-guides/changelog.md`
- **Conventional Commits 规范**：中文提交信息，标题简洁，描述改动 + 原因

## 五、与 OpenClaw / 自我提升系统的具体借鉴点

### 借鉴 1：把 "Goal-Driven Execution" 写进我的工作规则

立即在 `MEMORY.md` 加一节：

```markdown
## 🎯 Goal-Driven Execution（2026-07-09 从 Yuxi AGENTS.md 借鉴）

做任何任务前：
1. 把任务转成"verifiable goal"——必须能验证完成 / 失败
2. 多步骤任务先列 plan（step → verify）
3. 复杂任务先写最小验收标准（5 行内能说清的）
4. **失败标准也要写**（什么情况下算"我错了"，比"什么情况下算"我对了"更重要）
```

### 借鉴 2：v4 推荐策略改写（用 Simplicity First）

❌ **v3 的反思改进措施**（6-26 写过但没执行）：
- 行业分散度硬约束（单板块最多 2 只）
- 大盘熔断（上证 -1% 减仓 30%、-2% 减仓 50%）
- 跌破 MA20 全部清仓
- 止损位动态调整
- 强制配 1-2 只非相关性标的

→ 5 条规则太多且复杂 → 失败根因（**speculative feature**）

✅ **v4 推荐策略**（最少硬约束，最多 3 条）：
1. **5 只覆盖 ≥3 个板块**（相关性硬约束 → 唯一降低组合方差的硬规则）
2. **每只预设止损位 = 基线 × 0.92**（-8% 自动减仓 → 写在推荐理由里）
3. **大盘风险日（上证 -1.5%）→ 整组标记暂停，不加仓**（唯一大盘风控）

→ 3 条规则，每条都简单到能立刻验证

### 借鉴 3：用 ARCHITECTURE.md 风格重写 `MEMORY.md`

Yuxi 的 ARCHITECTURE.md 只描述"稳定的系统边界"，不写易变细节。
我的 `MEMORY.md` 现在有 33k 字符——**其中很多是历史事件**（应该下沉到 `memory/YYYY-MM-DD.md`）。
**行动**：把"昨日上下文"段保留（context-recovery 用），把"易变的项目状态"下沉到具体项目 README。

### 借鉴 4：建立"需求沟通规范"文档

Yuxi 要求"需求/改动较大时在 `docs/vibe/` 建日期文档"——这对德勤 / 元知项目特别合适。
**行动**：今晚在 `1-Projects/股票-A股/vibe/` 建第一份需求文档 `2026-07-09 - v4 推荐策略 + 自我提升系统设计.md`

### 借鉴 5：用 Review 准则反推 v3 失败

| Yuxi Review 步骤 | v3 推荐检查 |
|---|---|
| 主路径能跑吗？ | ❌ 跟踪流程 cron 中断 6-29~7-4，5/10 没复盘 |
| 是不是上下文最优解？ | ❌ 5 只里 4 只电子/通信，组合方差太大 |
| 有没有过度设计/防御？ | ❌ 写了 5 条风控规则没一条执行（pure speculative） |
| 测试有没有价值？ | ❌ 没有"什么情况下算推荐失败"的成功标准 |

## 六、Yuxi 与德勤项目的可能交集（不强挂钩，仅记录）

> 何大人 7-8 明确："不要每个链接都和德勤挂钩"。仅记录可能的引用点，不预设结论。

- **可插拔 Agent Harness 思路**：Yuxi 的 LangGraph v1 + DeepAgents + Skills + MCP 组合，正是何大人 6-29 提出的"执行器抽象层 + 每种都能接"的方向
- **多租户架构**：Yuxi 的多租户 / 权限 / 工作台模式，可参考到"德勤咨询 AI 平台"的多客户场景
- **但**：Yuxi 不直接替代 Hermes（决策已定），仅作为"成熟 Agent Harness 工程实践"参考

## 七、关键参考链接

- [Yuxi GitHub](https://github.com/xerrors/Yuxi)
- [Yuxi 在线文档](https://xerrors.github.io/Yuxi/)
- [AGENTS.md 原始文件](https://github.com/xerrors/Yuxi/blob/main/AGENTS.md)
- [ARCHITECTURE.md 原始文件](https://github.com/xerrors/Yuxi/blob/main/ARCHITECTURE.md)
- 致谢项目：[LightRAG](https://github.com/HKUDS/LightRAG) / [DeepAgents](https://github.com/langchain-ai/deepagents) / [DeerFlow](https://github.com/bytedance/deer-flow) / [RAGflow](https://github.com/infiniflow/ragflow) / [LangGraph](https://github.com/langchain-ai/langgraph) / [QwenPaw](https://github.com/agentscope-ai/QwenPaw)

## 八、今晚要立即采取的行动（与 7-9 早上的指令挂钩）

1. **归档本文档**（已完成）→ Git 同步
2. **写"v4 推荐策略"** 到 `1-Projects/股票-A股/改进记录/strategy_improvements.md`
3. **写"自我提升框架"** 到 `MEMORY.md` 新增段
4. **修 cron**：把 agentTurn 调模型的 cron 改成纯 Python 脚本（避开 MiniMax API 过载）
5. **明天 7-10 启动 v4 推荐**（按 3 条硬约束：3 板块分散 + -8% 止损 + 大盘 -1.5% 暂停加仓）
6. **每天 9:00 持仓 K 线日报** + **15:30 推荐复盘** 持续跑，自己做主止损/止盈判断