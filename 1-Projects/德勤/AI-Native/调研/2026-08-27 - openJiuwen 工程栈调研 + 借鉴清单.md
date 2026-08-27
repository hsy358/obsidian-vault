---
title: openJiuwen 工程栈调研 + 借鉴清单（2026-08-27）
date: 2026-08-27
type: research
purpose: 调研 openJiuwen（华为系开源 Agent 平台）全栈架构，提取可借鉴到德勤 MVP / Hermes / OpenClaw 执行器抽象层的具体技术点
related:
  - /root/vault/1-Projects/德勤/AI-Native/executor/abstract-interface.md
  - /root/vault/1-Projects/德勤/AI-Native/executor/langgraph-adapter.py
  - /root/vault/1-Projects/德勤/AI-Native/executor/tooling-stack-adapters.md
  - /root/vault/1-Projects/德勤/AI-Native/笔记/2026-06-29-开源研究部署笔记.md
---

# openJiuwen 工程栈调研 + 借鉴清单

## 0. 一句话定位

**openJiuwen（智问）** 是华为系开源的、生产级 AI Agent 平台，已在华为云 / 小艺智能体 / 鸿蒙智能体上落地金融 / 制造核心生产系统。它不是某个 Agent 框架，是**整个 Agent 平台底座**——这正好对应我们 6-29 定的"工程全景调研边界"。

> ⚠️ **研究边界（再次明确）**：本文**只回答**"openJiuwen 的具体技术 X 能否借鉴到 Hermes-based 德勤 MVP / OpenClaw 执行器抽象层"——**不**做"openJiuwen 替代 Hermes" 这种产品层面选型判断。

---

## 1. 全栈架构（一张图看懂）

```
┌─────────────────────────────────────────────────────────────┐
│  DeepAgents（开箱即用场景智能体）                                │
│  ├─ jiuwenswarm       多 Agent 协作框架 + 旗舰应用                  │
│  ├─ jiuwensymbiosis   具身智能体框架（embodiment-independent）    │
│  └─ deepsearch        知识增强深度搜索（GAIA / BrowseComp-Plus 榜首）│
├─────────────────────────────────────────────────────────────┤
│  SkillHub             Skill 托管 / 分发 / 版本管理 / 私有部署        │
├─────────────────────────────────────────────────────────────┤
│  Agent Studio         低/零代码可视化开发 + 工作流编排 + Prompt 调优  │
├─────────────────────────────────────────────────────────────┤
│  Agent Framework      【核心】编排 / 运行时 / LLM / 工具 / 检索 / 评测 │
│  ├─ agent-core         Python SDK                                      │
│  ├─ agent-core-java    Java SDK                                       │
│  ├─ agent-memory       【AutoGenetic 记忆系统】                        │
│  └─ agent-gateway      统一访问网关（开发中）                            │
├─────────────────────────────────────────────────────────────┤
│  Agent Distributed Runtime                                              │
│  └─ agent-runtime      服务化执行 + 多租户隔离 + 弹性扩缩 + K8s 部署   │
├─────────────────────────────────────────────────────────────┤
│  Agent System Service    AgentOS 基础服务                              │
│  ├─ 安全沙箱                                                       │
│  ├─ 统一持久化记忆存储                                                │
│  ├─ CLI / Agent 文件系统 / 跨 Agent 消息总线                          │
└─────────────────────────────────────────────────────────────┘
```

**关键洞察**：
- 它把"开发态 → 运行态 → 部署态 → 运维态"全生命周期都做了**模块化拆分**，每个仓库**可独立使用 / 独立演进**——这正好对应我们德勤 MVP 的"每个组件独立可部署"原则。
- 已商业化落地（华为云 / 小艺 / 鸿蒙）+ 榜单霸榜（GAIA / BrowseComp-Plus）= **生产可用度被验证过**——我们不是从零研究一个玩具项目。

---

## 2. 核心组件逐一拆解（**重点是能借鉴什么**）

### 2.1 agent-memory：AutoGenetic 记忆系统 ⭐⭐⭐

> 这是 openJiuwen 最值得借鉴的组件，没有之一。

**6 个核心能力**：

1. **分层记忆架构（L0–L3）**
   - L0 原始信息 → L1 摘要记忆 → L2 结构化记忆 → L3 用户画像
   - 每层独立持久化存储、信息密度递增
   - **自动提取**：UserProfile / SemanticMemory / EpisodicMemory / Variable / Summary
   - **支持自定义变量 + 禁用变量配置**

2. **Auto Dreaming（睡眠态记忆巩固）** ⭐
   - 三阶段睡眠范式（仿认知神经科学）：浅睡筛查 → REM 提取分类 → 深睡去重 / 冲突消解
   - 后台守护调度 + 忙时退避 + checkpoint 增量扫描
   - **Token 成本线性可控**

3. **MemoryTurbo 加速**
   - 会话**即时写缓存**（前端立即可读）
   - 记忆提取**异步后台跑**
   - 小模型按主题**合并会话** → 群组提取
   - 摊薄大模型调用成本

4. **Graph Memory（知识图谱）**
   - 多源写入：CONVERSATION / DOCUMENT / JSON
   - LLM 自动实体 / 关系抽取 + 合并去重
   - 图结构检索 + BFS 扩展 + Entity/Relationship/Episode 并行检索 + rerank 打分

5. **语义检索 + 冲突检测**
   - 统一跨类型向量语义检索
   - **MemUpdateChecker**：用 LLM 分析语义冲突，智能 ADD / DELETE
   - LLM 输出 UPDATE / DELETE 指令 → **语义校验后再执行**

6. **全栈存储后端**（5 大类可插拔）
   - KV：InMemoryKV / ShelveStore / DbBasedKV / Redis
   - Vector：ChromaDB / Milvus / Elasticsearch / GaussVector
   - Relational：SQLite / PostgreSQL / MySQL / GaussDB
   - Message：SqlMessageStore
   - Graph：Milvus GraphStore

7. **数据迁移框架**
   - KV / vector / SQL / message / index 的**版本化 schema 迁移**
   - 跨 BaseMemoryIndex 批量数据迁移
   - 操作注册表支持自定义扩展

8. **双维度解耦 Adapter 层** ⭐⭐⭐⭐⭐（**跟我们直接相关**）
   - **Plugin 维度**：hook-based 记忆注入，**已支持 OpenClaw / openJiuwen**
   - **Provider 维度**：统一 MemoryProvider 接口，支持 JiuwenMemory / Mem0
   - **N × M 自由组合**

9. **REST API + OpenClaw 插件**
   - FastAPI 提供完整 REST
   - **已发布 OpenClaw 官方插件**

---

### 2.2 agent-runtime：服务化运行时（5 维可借鉴）

**核心设计**：
- 统一方式部署不同 agent → 暴露为服务
- 多租户隔离（user_id / space_id）
- 多种部署策略：**subprocess（默认）/ docker / k8s**
- 全生命周期管理（deploy / inspect / delete / health check）

**目录结构**：
```
agent-runtime/
├── applications/   # 具体 agent 实现 + 低代码 agent / workflow IR 执行
├── cli/            # CLI 工具
├── docker/         # Docker 构建
├── foundation/     # DB / 端口 / 部署助手 / 日志
├── management/     # DeploymentManager + 部署策略执行器
├── server/         # FastAPI 管理服务（REST + 租户中间件 + 健康检查）
├── service/        # AgentApp / BaseApp 包装 FastAPI + 对话 API
└── scripts/        # 启动 / 构建脚本
```

**REST 端点**：
- `GET /health`
- `POST /api/v1/agents/deploy`
- `GET /api/v1/agents`
- `GET /api/v1/agents/{deployment_id}`
- `DELETE /api/v1/agents/{deployment_id}`

**跟我们 AgentRouter 的对照**：

| 维度 | openJiuwen agent-runtime | 我们的 AgentRouter |
|---|---|---|
| **核心定位** | "服务化部署 + 多租户隔离 + 多策略执行" | "执行器统一识别 + 路由分发" |
| **部署维度** | 跨进程 / 容器 / K8s | 单机本地优先 |
| **租户隔离** | ✅ 原生 | ❌ 未实现 |
| **多策略** | subprocess + docker + k8s | 子进程 + 注入 nvm 修复（特定） |
| **可借鉴** | **统一部署抽象 + 策略选择模式** | Adapter 边界 + 识别协议 |

---

### 2.3 agent-core：Python SDK 核心

**两种预置 Agent**：
- **ReActAgent**：Reasoning + Action 范式，循环执行 → 工具调用 → 观察
- **WorkflowAgent**：工作流自动跳转

**核心能力**：
- **多工作流跳转**（单 session 内自由切换 + checkpoint 断点续传）⭐
- 异步并行图执行 + 组件并发 + 流式处理
- **Prompt 自优化** + **Prompt 自动生成** + **全链路可观测**
- 高性能 runtime（async IO + streaming）
- Agent 状态保存 + 中断恢复

**示例代码骨架**（已读过源码）：
```python
from openjiuwen.core.workflow import Start, End, LLMComponent, LLMCompConfig
from openjiuwen.core.runner.runner import Runner
from openjiuwen.core.single_agent.legacy import WorkflowAgentConfig
from openjiuwen.core.application.workflow_agent import WorkflowAgent

# 1. 注册 workflow → Runner.resource_mgr
# 2. 创建 WorkflowAgent + add_workflows([flow])
# 3. await Runner.run_agent(workflow_agent, {"query": ...})
```

**风格观察**：
- **Runner.resource_mgr.add_workflow** 是注册中心模式 → 跟我们 Adapter 注册中心异曲同工
- **WorkflowCard（id + name + version + input_params）** 是工作流元数据
- **LLMComponent + input_schema** 显式建模参数流 → 比 Hermes dispatcher 的隐式 query string 严谨

---

### 2.4 其他组件

| 组件 | 关键能力 | 借鉴度 |
|---|---|---|
| **jiuwenswarm** | 多 Agent 协作框架 + Skill 自演进 | ⭐⭐（长周期任务可参考）|
| **jiuwensymbiosis** | 具身智能体框架（embodiment-independent） | ⭐（跟我们 MVP 无关） |
| **deepsearch** | 知识增强深度搜索 + 片段级引用 + 溯源推理 | ⭐⭐（德勤 RAG 可借鉴片段溯源）|
| **skillhub** | Skill 托管分发 + 版本管理 + 私有部署 | ⭐⭐⭐（跟我们 Skills 系统同构）|
| **agent-studio** | 低代码 + 工作流编排 + 资源管理 | ⭐（不直接借鉴） |
| **agent-gateway** | 通道管理 + 消息处理 + 定时任务 + 心跳 | ⭐⭐⭐（**跟我们 AgentRouter 直接对位**）|
| **agent-protocol** | MCP / A2A 协议的 C++ SDK | ⭐（我们用 Python 已适配） |

---

## 3. 跟我们 vault 里现有资产的对照

| openJiuwen 组件 | 我们 vault 现有 | 差距 / 借鉴动作 |
|---|---|---|
| **agent-memory (AutoGenetic)** | Datacore + Memory_search + 日报 | **🔴 缺 L0-L3 分层 + Auto Dreaming + 冲突检测** |
| **agent-memory (OpenClaw 插件)** | Hermes kanban + AgentSpace 1455 | **🟢 已有官方支持，可直接 pip install** |
| **agent-runtime (服务化部署)** | AgentRouter（5 harness 识别）+ Hermes dispatcher | **🟡 缺多租户 + 多部署策略** |
| **agent-core (多 workflow 切换 + checkpoint)** | langgraph-adapter（StateGraph demo） | **🟢 框架层已有，需补"断点续传 + 多 workflow 跳转"实现** |
| **agent-core (Prompt 自优化 + 全链路可观测)** | Hermes + langgraph-adapter（demo 阶段） | **🔴 Prompt 自优化缺；可观测有基础但不全** |
| **jiuwenswarm (多 Agent + Skill 自演进)** | OpenClaw subagent + sessions_spawn | **🟡 Skill 自演进缺（当前 Skill 静态）** |
| **deepsearch (片段级引用 + 溯源)** | vault 里 RAG 笔记 | **🟢 模式可借鉴** |
| **skillhub (Skill 托管分发)** | workspace/skills/ + Git 同步 | **🟡 缺版本管理 + 私有部署市场** |
| **agent-gateway (通道 + 消息 + 心跳)** | AgentRouter + sessions_list | **🟢 已基本覆盖** |

**总览**：
- 🟢 已有或基本覆盖：3 项
- 🟡 有基础需补：4 项
- 🔴 缺：2 项（**Agent 记忆系统** + **Prompt 自优化**）

---

## 4. 借鉴清单（**按德勤 MVP 优先级排序**）

### P0：**agent-memory 集成**（直接受益） ⭐⭐⭐⭐⭐

**为什么是 P0**：
- agent-memory 已经发布官方 **OpenClaw plugin**（hook-based 记忆注入）→ **零适配成本**
- AutoGenetic 思路（L0-L3 + Auto Dreaming + 冲突检测）正好补我们 vault 的**唯一短板**
- 已有 Mem0 等接口规范 → **可插拔**

**可借鉴的技术点 → 写 adapter 给 Hermes**：
1. **OpenClaw plugin** 直接装：`pip install openjiuwen-memory[openclaw]`
2. **L0-L3 分层 + 双维度 Adapter** 模式 → 给 Hermes 加 `MemoryProvider` 接口
3. **MemoryTurbo 加速**（会话即时写缓存 + 异步提取）→ 解决 kanban dispatcher 写日志卡顿
4. **MemUpdateChecker** 冲突检测 → 解决 LangGraph-adapter 笔记里提到的"日志里能看到失败但 Agent 不认怂"问题
5. **Auto Dreaming 后台守护** → 写一份 SOP + 脚本实现凌晨定期巩固记忆

**行动项**：
- [ ] 读 `openJiuwen-ai/agent-memory` 完整 README.md（zh）
- [ ] 试装 `pip install openjiuwen` + 配置 OpenClaw plugin
- [ ] 写 `executor/openjiuwen-memory-adapter.py` 参考实现

### P1：**agent-runtime 多部署策略** ⭐⭐⭐⭐

**为什么是 P1**：
- AgentRouter 已有 5 harness 识别 → 但**没有"部署策略"抽象层**
- 多租户 + K8s 部署是德勤企业级演示的加分项
- subprocess / docker / k8s 策略模式 → 给 Hermes "**部署即服务**"能力

**可借鉴**：
1. **Strategy 模式**（subprocess / docker / k8s）→ 给 Hermes Dispatcher 加 `--strategy` 参数
2. **DeploymentManager** 注册中心 → 跟 AgentRouter 协同
3. **REST 端点设计**（/deploy /list /delete /health）→ 给 AgentSpace 加 API
4. **租户上下文注入**（user_id / space_id）→ 给 demo 加多用户场景

**行动项**：
- [ ] 写 `executor/deploy-strategy-adapter.py`（Strategy 模式抽象）
- [ ] 给 AgentSpace 加 `/api/v1/agents/deploy` 端点
- [ ] 加 docker 部署 demo（演示用）

### P2：**agent-core 多 Workflow + checkpoint** ⭐⭐⭐

**为什么是 P2**：
- LangGraph StateGraph demo 已能跑，但**单 workflow**
- 德勤 MVP 需要"切换场景"（如客服场景切到代码审查）→ **多 workflow 切换是刚需**
- checkpoint 断点续传 → 长任务可靠性

**可借鉴**：
1. **WorkflowCard** 元数据模式（id + name + version + input_params）→ 给 Hermes 加 Workflow 注册表
2. **多 workflow 切换 + checkpoint 续传** → 写 adapter 给 LangGraph StateGraph
3. **Prompt 自优化 + 全链路可观测** → **借鉴但不一定抄，自己实现更轻量**

**行动项**：
- [ ] 升级 `langgraph-adapter.py`：加 WorkflowCard 注册 + 多 workflow 跳转
- [ ] 写 `executor/multi-workflow-adapter.py`（参考 openJiuwen 的实现）

### P3：**skillhub Skill 版本管理** ⭐⭐

**为什么是 P3**：
- 我们 Skills 是文件系统 + Git 同步 → **没有版本管理 + 分发市场**
- 德勤 MVP 演示时可作为"私有 Skill 仓库"卖点

**可借鉴**：
1. **Skill 元数据标准**（name + version + description + dependencies）
2. **Skill Hub REST**（publish / search / download / private）
3. **私有部署** → 演示可加

**行动项**：
- [ ] 给 `workspace/skills/*/SKILL.md` 加 version + dependencies 字段
- [ ] 写 `vault/SKILL-INDEX.md` 索引（已有类似，按 skillhub 风格升级）

---

## 5. **不该借鉴的**（明确边界）

| 维度 | 我们的取舍 |
|---|---|
| **"openJiuwen 替代 Hermes"** | ❌ **绝不讨论**——这是 6-29 已定的产品路线 |
| **完整 SDK 集成** | ❌ 重——我们只要可借鉴的设计模式 |
| **企业级 K8s + 多租户全套** | ❌ MVP 阶段过重——**做"可插拔接口"就好** |
| **Auto Dreaming 完整实现** | 🟡 太重——只取"定期巩固"的思路，写个轻量 cron |
| **C++ agent-protocol** | ❌ 我们用 Python 已适配 MCP |
| **deepsearch 完整迁移** | ❌ 跟我们研究主题无关 |

---

## 6. 优先级 + 时间表

| 周次 | 任务 | 产出 |
|---|---|---|
| **本周** | pip install openjiuwen + 试装 OpenClaw plugin | 安装验证报告 |
| **本周+1** | 读 agent-memory 完整代码 + 写 `openjiuwen-memory-adapter.py` | adapter 草图 |
| **本周+2** | 升级 LangGraph-adapter + 多 workflow + checkpoint | executor v2 |
| **下周** | Strategy 部署抽象 + AgentSpace 加 deploy API | AgentRouter v2 |

---

## 7. 关键提醒

1. **不抄框架、只学设计模式**——把 openJiuwen 当"参考实现目录"用
2. **每个借鉴都要落 adapter / 脚本**——光写笔记不算交付
3. **强调"独立可部署"**——这是 6-29 既定原则，openJiuwen 本身就是这个思路
4. **借鉴深度要节制**——MVP 阶段重在跑通 + 演示价值，不要陷入企业级全套

---

## 8. 参考链接

- [openJiuwen GitHub Org](https://github.com/openJiuwen-ai)
- [agent-core README](https://github.com/openJiuwen-ai/agent-core)
- [agent-core-java](https://github.com/openJiuwen-ai/agent-core-java)
- [agent-memory README](https://github.com/openJiuwen-ai/agent-memory)
- [agent-runtime README](https://github.com/openJiuwen-ai/agent-runtime)
- [jiuwenswarm](https://github.com/openJiuwen-ai/jiuwenswarm)
- [deepsearch](https://github.com/openJiuwen-ai/deepsearch)
- [skillhub](https://github.com/openJiuwen-ai/skillhub)
- [36氪 - DeepAgent 与 DeepSearch 双双霸榜](https://m.36kr.com/p/3679871003832198)