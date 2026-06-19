# Self-Driving R&D · 独立可移植版 v4.2（生态融合版）

> **版本定位**：在 v4.1 基础上吸收 **2026 年 6 月最新生态**（Paperclip / Conductor / Anthropic Harness / Routa / Harnss / Goose / Nika / GitHub multi-agent patterns）的核心设计
> **核心改进**：ACP/MCP 标准、Org Chart + Goal Ancestry、Heartbeat 调度、Action Schema、BYOA、Importable Templates
> **更新日期**：2026-06-19

---

## 零、调研清单（本次优化依据）

### Vault 已有资源
| 资源 | 关键贡献 |
|------|---------|
| YX AI Delivery Harness 截图 | 8 阶段 + 双栏 + Decision Agent + 人工 PASS |
| Comet 文章（OpenSpec+Superpowers）| `.comet.yaml` 状态机 + `guard.sh`/`handoff.sh`/`archive.sh` 脚本 |
| v3.5 架构设计 | 33 组件 / 8 阶段 / 5 层压缩 / 抗退化 / Self-Improvement |
| 2026-06-12 Routa Deep Research | 双后端（TS + Rust）/ Workspace-first / Kanban |
| 2026-06-12 Harnss Deep Research | Tauri 桌面 / ACP / 虚拟化列表 / Split View |
| 2026-06-12 Goose Deep Research | AAIF 标准 / 47.8k stars / MCP 70+ |
| 2026-06-15 Paperclip 文章 | 70k stars / BYOA / Heartbeat / Org Chart / Goal Ancestry |

### 网络新发现
| 资源 | 关键贡献 |
|------|---------|
| **Anthropic Harness Design** | 2-agent (initializer + coding) + progress.txt + init.sh + 干净 state |
| **Microsoft Conductor** | YAML 确定性路由（零 token 消耗）+ Jinja2 + 并行分组 + Web Dashboard |
| **GitHub Multi-Agent Patterns** | Typed Schema + Action Schema + MCP 是 table stakes |
| **Nika** | YAML + 5 semantic verbs + 多 provider 一行切换 |
| **Anthropic Structured-Prompt-Driven (SPDD)** | Prompt 是一等公民（git 控） |
| **awesome-harness-engineering** | 行业资源汇总（arXiv 论文 363+）|

---

## 一、v4.1 已知缺陷（v4.2 修复）

| 类别 | v4.1 的问题 | v4.2 改进 |
|------|------------|----------|
| **协议** | 没提 ACP/MCP | **全面支持 ACP（Agent Client Protocol）+ MCP（Model Context Protocol）** |
| **Agent 隔离** | Session 简单 | **每 agent 独立 session，无上下文串味**（Conductor 模式）|
| **Action 协议** | LLM 返回自由文本 | **Action Schema 强制约束**（GitHub 模式）|
| **Agent 角色** | 8 阶段是流水线 | **引入 Org Chart**：每个 agent 有角色 / 头衔 / 汇报线 / 预算 |
| **目标体系** | stage 之间无逻辑 | **Goal Ancestry 链**：Mission → Project → Agent → Task |
| **调度** | State-driven | **Heartbeat 队列**（DB-backed wakeup + 合并 + 预算检查）|
| **Memento 假设** | 默认 LLM 有记忆 | **显式 Memento Man 模式**：每次唤醒加载 heartbeat checklist |
| **Workflow 定义** | Python 内部 DSL | **YAML 优先**（Conductor 风格）+ Jinja2 路由 + 零 token |
| **Dry-run** | 无 | **workflow validate + dry-run**（Conductor 模式）|
| **安全限制** | 无 | **Max iteration + wall-clock timeout + dry-run** |
| **插件系统** | 三类 skill | **真正 plugin 架构**（Paperclip 风格：plugin 作为独立 npm/PyPI 包）|
| **模板共享** | 无 | **Importable Company Template**（下载一份 YAML 即得到一个完整公司）|
| **Para Memory** | 文件 | **分层文件记忆**（按 role 隔离） |
| **Skill 调用** | 串行/有依赖 | **静态 parallel_group + 动态 for_each + all/any 聚合** |
| **Skill 失效** | 5-mode self-correct | **+ skip + escalate 三档（soft / hard / human）** |
| **上下文控制** | 全量传递 | **3 模式：accumulate / last_only / explicit**（Conductor） |

---

## 二、整体架构（v4.2）

```
┌──────────────────────────────────────────────────────────────────────┐
│  Frontend (React + Vite)                                             │
│  ├─ DashboardPage    ← 多项目总览（Kanban）                          │
│  ├─ ProjectPage      ← 单项目 + PipelineTrack + 双栏面板            │
│  ├─ OrgChartPage     ← Agent 组织图（Paperclip 风格）               │
│  ├─ WorkflowEditor   ← YAML 可视化编辑 + DAG 预览                   │
│  ├─ PluginManager    ← 插件市场/已装/更新                           │
│  ├─ MemoryExplorer   ← Para 记忆浏览                                │
│  ├─ MetricsPage      ← OpenTelemetry 指标                          │
│  └─ SettingsPage     ← 模型/通知/预算/工作区                        │
│  WebSocket 实时 + REST + ACP-over-HTTP（agent 接入）                  │
└──────────────────────────────────────────────────────────────────────┘
                              ↕
┌──────────────────────────────────────────────────────────────────────┐
│  Backend (Python 3.11+ FastAPI)                                      │
│                                                                       │
│  ┌─────────────────── Orchestration Layer ───────────────────────┐  │
│  │  WorkflowEngine     ← YAML 解析 + Jinja2 路由（零 token）       │  │
│  │  HeartbeatScheduler  ← DB-backed wakeup 队列（带 coalescing）    │  │
│  │  GoalResolver        ← Mission → Project → Agent → Task 链解析  │  │
│  │  OrgChartManager     ← Agent 角色 / 汇报线 / 预算              │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌─────────────────── Agent Layer (BYOA) ─────────────────────────┐  │
│  │  ACPClient / ACPServer  ← 跨 agent 协议                          │  │
│  │  AgentRuntime           ← 内部 agent 执行容器                    │  │
│  │  ExternalAgentBridge    ← Claude Code / Codex / OpenClaw 接入  │  │
│  │  MementoLoader          ← Heartbeat checklist 注入             │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌─────────────────── Skill Layer ─────────────────────────────────┐  │
│  │  PluginLoader       ← 从 PyPI/npm 加载 plugin                    │  │
│  │  SkillDAGScheduler  ← 拓扑并行 + 3 模式上下文控制               │  │
│  │  MCPClient          ← MCP 工具调用（GitHub 模式）               │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌─────────────────── Decision Layer ──────────────────────────────┐  │
│  │  DecisionAgent      ← 5 层裁决（v4.1 沿用）                    │  │
│  │  ActionValidator    ← Action Schema 校验（GitHub 模式）          │  │
│  │  SelfCorrectEngine  ← 5-mode + 3 档（soft/hard/human）          │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌─────────────────── State & Storage ────────────────────────────┐  │
│  │  StateManager       ← YAML + SQLite（v4.1 沿用）                │  │
│  │  ParaMemory         ← 分层文件记忆（按 role 隔离）              │  │
│  │  WorkflowRegistry   ← YAML 模板仓库（可分享/版本化）            │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌─────────────────── Infrastructure ──────────────────────────────┐  │
│  │  LLMInterface       ← 多 provider 适配                          │  │
│  │  ConcurrencyManager ← Token budget + rate limit                  │  │
│  │  EventBus           ← Pub/Sub 事件                              │  │
│  │  Telemetry          ← OpenTelemetry                             │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
                              ↕
┌──────────────────────────────────────────────────────────────────────┐
│  External / Storage                                                    │
│  ├─ projects/<name>/           ← 项目目录                            │
│  ├─ .heartbeats/                ← Heartbeat 队列（SQLite）          │
│  ├─ .state.db                   ← 主状态库                           │
│  ├─ .comet.yaml                 ← 主状态（YAML）                     │
│  ├─ skills/                     ← 内置/脚本/API 三类                │
│  ├─ plugins/                    ← 第三方插件（PyPI/npm）            │
│  ├─ workflows/                  ← YAML workflow 库                   │
│  ├─ memory/<role>/              ← Para 记忆（按 agent 角色分）      │
│  └─ templates/companies/        ← Importable 公司模板              │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 三、核心架构改进

### 3.1 YAML 优先 Workflow（Conductor 模式）

**v4.1 的问题**：用 Python 内部 DSL 写 workflow，复杂且无法 git diff。

**v4.2 改进**：所有 workflow 用 YAML 声明，Jinja2 路由：

```yaml
# workflows/8-stage-pipeline.yaml
workflow:
  name: 8-stage-pipeline
  version: "1.0.0"
  description: Self-Driving R&D 主流程
  
  # 全局配置
  safety:
    max_iterations: 100
    wall_clock_timeout_minutes: 480  # 8 小时上限
    dry_run: false
  
  # 目标体系（Goal Ancestry）
  goal_ancestry:
    mission: "AI 驱动的自动化研发"
    project_goal: "{{ workflow.input.project_goal }}"
  
  # 输入输出
  input:
    spec_path: { type: string, required: true }
    tech_stack: { type: object }
  
  # Agent 组织图（Org Chart）
  org_chart:
    - role: ceo
      title: Project Manager
      reports_to: null
      budget: 5000
    - role: researcher
      title: Tech Researcher
      reports_to: ceo
      budget: 2000
    - role: architect
      title: Solution Architect
      reports_to: ceo
      budget: 3000
    - role: engineer
      title: Coding Agent
      reports_to: architect
      budget: 10000
    - role: qa
      title: Quality Assurance
      reports_to: architect
      budget: 2000
  
  # 8 阶段定义
  stages:
    access:
      agent: ceo
      depends_on: []
      timeout: 300
      skills: [requirement-parser, spec-validator]
      output: spec.md
      routes:
        - to: explore
          when: "{{ stages.access.output.score >= 70 }}"
        - to: failed
          when: "{{ stages.access.output.score < 70 }}"
    
    explore:
      agent: researcher
      depends_on: [access]
      timeout: 600
      # 静态并行组
      parallel:
        group: explore-search
        agents: [web-searcher, code-searcher, doc-reader]
        failure_mode: continue_on_error
      synthesizer:
        agent: researcher
        depends_on: [explore-search]
        output: explore.md
      routes:
        - to: propose
          when: "{{ stages.explore.output.score >= 70 }}"
        - to: access
          when: "{{ stages.explore.output.score < 70 }}"
    
    propose:
      agent: architect
      depends_on: [explore]
      timeout: 600
      skills: [proposal-writer, architecture-advisor]
      output: propose.md
      # 3 种上下文模式
      context_mode: last_only   # 只看 explore，不看 access
      routes:
        - to: task
    
    task:
      agent: architect
      depends_on: [propose]
      timeout: 300
      skills: [task-decomposer, dependency-analyzer]
      output: tasks.json
      routes:
        - to: apply
    
    apply:
      agent: engineer
      depends_on: [task]
      timeout: 3600
      parallel:
        group: apply-build
        agents: [code-generator, test-writer]
        failure_mode: fail_fast
      # engineer-to-QA review loop（Paperclip 模式）
      review_loop:
        until: "{{ stages.apply.score >= 80 }}"
        max_iterations: 5
        steps:
          - code-generator
          - self-correct
          - test-runner
          - score
      routes:
        - to: verify
    
    verify:
      agent: qa
      depends_on: [apply]
      timeout: 1200
      parallel:
        group: verify-checks
        agents: [test-runner, security-scanner, benchmark-runner]
        failure_mode: continue_on_error
      output: verify-report.json
      # 硬门禁
      hard_gate: true
      routes:
        - to: review
          when: "{{ stages.verify.output.passed == true }}"
        - to: apply
          when: "{{ stages.verify.output.passed == false }}"
    
    review:
      agent: ceo
      depends_on: [verify]
      timeout: 600
      skills: [review-writer, doc-generator]
      output: review.md
      hard_gate: true
      # 人工 gate
      human_gate:
        question: "是否通过评审？"
        options: [approve, reject, request_changes]
      routes:
        - to: archive
          when: "{{ human_gate.response == 'approve' }}"
        - to: apply
          when: "{{ human_gate.response == 'reject' }}"
        - to: verify
          when: "{{ human_gate.response == 'request_changes' }}"
    
    archive:
      agent: ceo
      depends_on: [review]
      timeout: 300
      skills: [archive-writer, lesson-extractor]
      output: lessons.md
      routes:
        - to: $end
```

**关键设计点**（融合 Conductor 优势）：
- **零 token 路由**（Jinja2 表达式求值决定流向）
- **静态并行组**（parallel_group + failure_mode）
- **3 种上下文模式**（accumulate/last_only/explicit）
- **review_loop 循环结构**（until + max_iterations）
- **human_gate 节点**（web UI 显示，CEO 决策）
- **safety 限制**（max_iterations + wall_clock）

### 3.2 Heartbeat 调度（Paperclip 模式）

**v4.1 用 cron + 状态驱动**。**v4.2 升级为 Heartbeat 队列**：

```python
# HeartbeatScheduler（DB-backed wakeup queue）
class HeartbeatScheduler:
    """
    替代 v4.1 的 cron + state-driven。
    来源：Paperclip 的 Heartbeats & Routines + Anthropic 的 Memento Man 模式。
    """

    def __init__(self, db: DB):
        self.queue = WakeupQueue(db)  # SQLite-backed

    def schedule(self, agent_role: str, trigger: Trigger, payload: dict):
        """
        调度一次唤醒
        trigger: cron | interval | event | dependency
        """
        item = WakeupItem(
            id=uuid4(),
            agent_role=agent_role,
            trigger=trigger,
            payload=payload,
            scheduled_at=trigger.next_time(),
            status="pending",
            retry_count=0,
            coalesce_key=f"{agent_role}:{trigger.name}"  # 同 key 合并
        )
        self.queue.enqueue(item)

    def tick(self):
        """每次 tick 处理 pending wakeups"""
        items = self.queue.pop_due(batch_size=10)

        # Coalescing：同 agent_role + 同一 minute 内的多个 wakeup 合并
        items = self._coalesce(items)

        for item in items:
            self._wake_agent(item)

    def _wake_agent(self, item: WakeupItem):
        """
        关键：Memento Man 模式
        每次唤醒 = 全新 session，必须从文件/记忆里恢复上下文
        """
        # 1. 加载 ParaMemory（分层文件记忆）
        memory = ParaMemory.load(agent_role=item.agent_role)

        # 2. 加载 Heartbeat Checklist（agent 的"我今天要做什么"）
        checklist = HeartbeatChecklist.load(agent_role=item.agent_role)

        # 3. 加载当前项目状态
        project_state = self._load_project_state(item)

        # 4. 启动新 session（隔离上下文）
        session = AgentSession.start(
            role=item.agent_role,
            memory=memory,
            checklist=checklist,
            project_state=project_state,
            trigger=item.trigger,
        )

        # 5. Agent 跑完后写回 ParaMemory
        session.on_complete(lambda result: memory.save(result))
```

**对比 v4.1 的 cron**：

| 维度 | v4.1（cron）| v4.2（heartbeat）|
|------|-------------|------------------|
| 调度 | 定时 | 定时+事件+依赖+合并 |
| 上下文 | 每次 reload state | 显式 Memento Man 注入 checklist |
| 合并 | 无 | 同 agent 同 minute 自动合并 |
| 失败处理 | retry | retry + dead-letter + 升级 |
| 适配多 agent | 各 cron 独立 | 统一队列 + role-based |

### 3.3 BYOA（Bring Your Own Agent）

**v4.1 只支持内部 agent**。**v4.2 全面支持外部 agent 接入**：

```python
# ACP（Agent Client Protocol）— 行业新兴标准
# 已被 Harnss / Goose / Routa / Paperclip 广泛采用

class AgentAdapter(Protocol):
    """所有 agent 适配器实现这个接口"""
    role: str
    name: str
    version: str

    async def invoke(self, prompt: str, context: dict) -> AgentResult: ...
    async def heartbeat(self) -> HeartbeatStatus: ...
    async def cancel(self, run_id: str) -> None: ...

# 内置 agent（直接 import）
class ClaudeCodeAdapter:
    role = "engineer"
    name = "claude-code"
    # 调用 Claude Code CLI / Anthropic API

class OpenAICodexAdapter:
    role = "engineer"
    name = "codex"
    # 调用 Codex CLI / OpenAI API

# 外部 agent（通过 ACP-over-HTTP）
class ExternalACPAdapter:
    """任意支持 ACP 协议的 agent"""
    role = "engineer"
    def __init__(self, endpoint: str):
        self.endpoint = endpoint  # e.g. http://claude-code-box:8080
    
    async def invoke(self, prompt, context):
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{self.endpoint}/v1/invoke", json={...})
            return AgentResult.from_json(r.json())

# OpenClaw 兼容适配器（保留向下的兼容性）
class OpenClawAdapter:
    """通过 sessions_spawn 调用 OpenClaw"""
    role = "engineer"
    async def invoke(self, prompt, context):
        return await openclaw_sessions_spawn(task=prompt, context=context)
```

**配置方式**：
```yaml
# config.yaml
agents:
  ceo:
    adapter: builtin_pm  # 内置
    model: minimax/MiniMax-M3
  
  researcher:
    adapter: builtin_researcher
    model: deepseek/DeepSeek-R1
  
  engineer:
    adapter: external_acp  # 外部 ACP
    endpoint: http://claude-code-box:8080
    model: anthropic/claude-sonnet-4.5
    fallback: builtin_codex  # 失败时回退
  
  qa:
    adapter: builtin_qa
    model: minimax/MiniMax-M2.7
```

### 3.4 Org Chart + Goal Ancestry（Paperclip 模式）

```python
# GoalResolver
class GoalResolver:
    """解析 Mission → Project → Agent → Task 链"""

    def resolve(self, project_id: str) -> GoalChain:
        # 1. Mission（来自 config）
        mission = self.config.mission  # "AI 驱动的自动化研发"

        # 2. Project Goal（来自 project metadata）
        project_goal = self.db.get_project(project_id).goal

        # 3. Agent Goal（来自 agent 角色 + 当前任务）
        agent_goal = self._resolve_agent_goal(project_id)

        # 4. Task Goal（具体任务）
        task_goal = self._resolve_task_goal(project_id)

        return GoalChain(
            mission=mission,
            project=project_goal,
            agent=agent_goal,
            task=task_goal
        )

# 每个 agent 启动时自动注入 SKILL.md 上下文
def inject_goal_context(agent_session, project_id):
    chain = GoalResolver().resolve(project_id)
    agent_session.add_context(f"""
    # Why Am I Doing This?

    ## Mission (Company)
    {chain.mission}

    ## Project Goal
    {chain.project}

    ## My Goal (as {agent_session.role})
    {chain.agent}

    ## Current Task
    {chain.task}

    Remember: every action you take should serve the mission.
    """)
```

### 3.5 Memento Man 模式（Paperclip 模式）

**核心假设**：每次 LLM session 启动时，模型就像电影《记忆碎片》的主人公——**能力全开但零记忆**。所以每次唤醒必须加载：

```yaml
# agents/engineer/heartbeat.md
# Heartbeat Checklist for Engineer role
---
role: engineer
last_updated: 2026-06-19
---

# Engineer Heartbeat Checklist

## 身份
- 你是 Engineer Agent
- 上级：Architect
- 同事：QA, Researcher
- 预算：10000 tokens / 项目

## 启动必做（每次 session 都要做）
1. 读 `memory/engineer/identity.md` → 知道"我是谁"
2. 读 `memory/engineer/skills.md` → 知道"我会什么"
3. 读 `memory/engineer/mistakes.md` → 知道"我以前犯过什么错"
4. 读 `projects/<current>/tasks.json` → 知道"今天要做什么"
5. 读 `projects/<current>/spec.md` → 知道"做什么"
6. 读 `projects/<current>/.comet.yaml` → 知道"现在到哪一步"

## 工作流程
1. 选一个 task
2. 看 spec 里的对应需求
3. 写代码 + 写测试
4. 跑 linter + test
5. 提交 + 写 handoff
6. 通知 Architect

## 不要做
- 不要修改 spec.md（spec 是 sacred）
- 不要跳过测试
- 不要在没看任务的情况下乱写代码
- 不要忘了写 handoff

## 失败模式
- 如果测试失败：重试 1 次 → 切到小范围重试 → 通知 Architect
- 如果超出预算：暂停 + 通知
- 如果遇到 spec 矛盾：立即停 + 通知

## 完成后
1. 更新 `memory/engineer/skills.md`（学到了什么）
2. 如果有 mistake，更新 `memory/engineer/mistakes.md`
3. 写 handoff
```

**ParaMemory 分层**（按 role 隔离）：
```
memory/
├── ceo/
│   ├── identity.md          # 角色定义
│   ├── skills.md            # 当前能力清单
│   ├── mistakes.md          # 失败教训
│   └── decisions.md         # 重大决策记录
├── engineer/
│   ├── identity.md
│   ├── skills.md
│   ├── mistakes.md
│   └── patterns.md          # 编码模式
├── researcher/
├── architect/
└── qa/
```

### 3.6 Action Schema（GitHub Multi-Agent 模式）

**v4.1 的问题**：LLM 返回自由文本，下游难以处理。

**v4.2 改进**：每个 agent 的输出必须匹配 Action Schema：

```python
# schemas/actions.py
from pydantic import BaseModel
from typing import Literal, Union, List

# Engineer Agent 的合法 actions
class WriteCode(BaseModel):
    type: Literal["write_code"]
    files: List[FileChange]
    tests: List[FileChange]
    notes: str

class RunTests(BaseModel):
    type: Literal["run_tests"]
    command: str
    expected: str

class RequestReview(BaseModel):
    type: Literal["request_review"]
    summary: str
    artifacts: List[str]

class EscalateToArchitect(BaseModel):
    type: Literal["escalate_to_architect"]
    reason: str
    context: dict

class HandoffFailed(BaseModel):
    type: Literal["handoff_failed"]
    error: str
    attempted: int

EngineerAction = Union[WriteCode, RunTests, RequestReview, EscalateToArchitect, HandoffFailed]

# 在 agent 输出后强制校验
class ActionValidator:
    def validate(self, agent_role: str, raw_output: str) -> Action:
        parsed = LLM.structured_output(raw_output, schema=get_schema(agent_role))
        # 校验失败 → 重试或升级
        if not parsed:
            raise ActionSchemaViolation(...)
        return parsed
```

### 3.7 MCP 集成（GitHub 模式）

```python
# MCPClient
class MCPClient:
    """通过 Model Context Protocol 调用外部工具"""

    def __init__(self, mcp_servers: list):
        self.servers = {s.name: s for s in mcp_servers}
    
    async def call_tool(self, server: str, tool: str, args: dict) -> dict:
        # MCP 协议保证 input/output schema 一致
        ...

# config.yaml
mcp_servers:
  - name: github
    command: npx @modelcontextprotocol/server-github
    env: { GITHUB_TOKEN: ${GITHUB_TOKEN} }
  - name: filesystem
    command: npx @modelcontextprotocol/server-filesystem
    args: ["/root/projects"]
  - name: web-search
    command: npx @modelcontextprotocol/server-brave-search
    env: { BRAVE_API_KEY: ${BRAVE_API_KEY} }
```

### 3.8 Plugin 架构（Paperclip 模式）

**v4.1 的三类 skill**（builtin/script/api）升级为真正的 **plugin 架构**：

```
plugins/
├── official/
│   ├── github-integration/    # PyPI: selfdriving-plugin-github
│   ├── slack-notifier/        # PyPI: selfdriving-plugin-slack
│   ├── jira-sync/             # PyPI: selfdriving-plugin-jira
│   └── feishu-notifier/       # PyPI: selfdriving-plugin-feishu
└── community/
    ├── notion-sync/           # PyPI: selfdriving-plugin-notion
    └── ...
```

**plugin 协议**（标准接口）：
```python
# plugins/<name>/plugin.py
from selfdriving.plugin import Plugin, hook

class MyPlugin(Plugin):
    name = "github-integration"
    version = "1.2.0"
    
    # 钩子：在某些事件时触发
    @hook("stage.before_access")
    async def on_access_start(self, context):
        ...
    
    @hook("stage.after_verify")
    async def on_verify_done(self, context):
        ...
    
    # 注册 skill
    def skills(self):
        return [GitHubCommitSkill, GitHubPRSkill]
    
    # 注册 action schema
    def actions(self):
        return [CreatePR, MergePR]
```

**安装方式**：
```bash
# 类似 npm/PyPI
pip install selfdriving-plugin-github
selfdriving plugin enable github-integration
```

### 3.9 Importable Company Template（Paperclip 模式）

```yaml
# templates/saas-startup-company.yaml
# 完整的"AI 公司"模板，下载即用
template:
  name: SaaS Startup Company
  description: 完整的 SaaS 创业公司 AI 团队
  author: dotta
  version: "1.0.0"
  stars: 5400

org_chart:
  - role: ceo
    title: CEO
    adapter: builtin_pm
  - role: cto
    title: CTO
    adapter: builtin_architect
  - role: backend-engineer
    reports_to: cto
    adapter: external_acp
    endpoint: http://claude-code-box:8080
  - role: frontend-engineer
    reports_to: cto
    adapter: external_acp
    endpoint: http://codex-box:8081
  - role: qa
    reports_to: cto
    adapter: builtin_qa
  - role: marketer
    reports_to: ceo
    adapter: builtin_writer
  - role: customer-success
    reports_to: ceo
    adapter: builtin_support

workflows:
  - build-new-feature
  - fix-bug
  - customer-onboarding
  - weekly-report

skills:
  - stripe-integration
  - email-sender
  - analytics-tracker
  - legal-doc-generator
```

**使用**：
```bash
# 导入模板
selfdriving template import saas-startup-company

# 启动一个具体的"公司"
selfdriving start my-startup --template saas-startup-company

# 这会创建：
# - 6 个 agent 的 org chart
# - 4 个 workflow
# - 4 个 skill
# - ParaMemory 模板
# 全部就绪，可以立刻使用
```

---

## 四、状态层（v4.2 强化）

### 4.1 多文件状态布局

```
projects/<project>/
├── .comet.yaml              # 主状态（YAML，人类可读）
├── .state.db                # 主状态库（SQLite，事务）
├── .heartbeat/              # Heartbeat 队列（SQLite）
│   └── wakeup.db
├── spec.md                  # 需求规格
├── tasks.json               # 任务分解
├── artifacts/               # 各阶段产物
│   ├── access/
│   ├── explore/
│   ├── propose/
│   ├── task/
│   ├── apply/
│   ├── verify/
│   ├── review/
│   └── archive/
├── reviews/                 # 评审记录
├── lessons/                 # 本项目 lessons
│   └── lessons.md
└── handoffs/                # 跨 session 交接
    ├── session-001.md
    ├── session-002.md
    └── ...
```

### 4.2 状态机（兼容 v4.1 的灵活跳转）

```python
# STAGE_GRAPH 沿用 v4.1
STAGE_GRAPH = {
    "access":  ["explore", "propose", "failed"],
    "explore": ["propose", "access", "failed"],
    "propose": ["task", "explore", "failed"],
    "task":    ["apply", "propose", "failed"],
    "apply":   ["verify", "task", "failed"],
    "verify":  ["review", "apply", "failed"],
    "review":  ["archive", "verify", "failed"],
    "archive": ["completed"],
    "failed":  ["access", "explore", "apply", "verify"],
    "completed": []
}
```

### 4.3 状态机现在用 YAML 声明（Conductor 风格）

```yaml
# .comet.yaml
project: my-tool
version: 4.2
created: 2026-06-19
workflow: 8-stage-pipeline  # 引用 workflow 模板

current_stage: verify
previous_stage: apply

goal_ancestry:
  mission: "AI 驱动的自动化研发"
  project: "构建开源 Self-Driving R&D 平台"

agents_active:
  - role: engineer
    session_id: eng-005
    last_heartbeat: 2026-06-19T15:00:00
  - role: qa
    session_id: qa-002
    last_heartbeat: 2026-06-19T15:05:00

stage_history:
  access:  {status: completed, score: 92, skills_used: [requirement-parser, spec-validator], ended_at: ...}
  explore: {status: completed, score: 88, skills_used: [web-search, code-search, explore-synthesizer], ended_at: ...}
  propose: {status: completed, score: 85, skills_used: [proposal-writer], ended_at: ...}
  task:    {status: completed, score: 82, skills_used: [task-decomposer], ended_at: ...}
  apply:   {status: completed, score: 0, skills_used: [code-generator, test-writer, linter], ended_at: ...}
  verify:  {status: in_progress, skills_used: [test-runner, security-scanner], started_at: ...}

# 兼容字段
skills_registry_version: "4.2"
```

---

## 五、错误恢复（v4.2 三档）

```python
class SelfCorrectEngine:
    """v4.1 5-mode → v4.2 三档"""

    async def recover(self, error, context) -> RecoveryAction:
        # 1. Soft Recovery（不破坏流程）
        if error.is_transient:
            return await self._retry_with_backoff(context)
        if error.is_schema_violation:
            return await self._regenerate_with_schema_feedback(context)
        
        # 2. Hard Recovery（需要升级机制）
        if error.is_quality_issue:
            return await self._invoke_self_correction_loop(context)
        if error.is_resource_exhausted:
            return await self._switch_model_or_skill(context)
        if error.is_dependency_failed:
            return await self._retry_with_alternative_path(context)
        
        # 3. Human Escalation（升级到人）
        if error.is_unrecoverable:
            return await self._escalate_to_human(context)
```

---

## 六、可观测性

**v4.1 的 OpenTelemetry 沿用 + Paperclip 的不可变审计日志**：

```python
# 不可变审计日志（Paperclip 模式）
# 一旦写入不可修改、不可删除
class AuditLog:
    def __init__(self, db: DB):
        # SQLite 的 append-only table
        # + 每次写入生成 hash chain
        ...
    
    def write(self, actor: str, action: str, target: str, details: dict):
        prev_hash = self._last_hash()
        entry = {
            "actor": actor,
            "action": action,
            "target": target,
            "details": details,
            "ts": now(),
            "prev_hash": prev_hash,
        }
        entry["hash"] = sha256(json.dumps(entry))
        # append only, no UPDATE, no DELETE
        self.db.insert("audit_log", entry)
```

---

## 七、与 v4.1 的核心差异总表

| 维度 | v4.1 | v4.2 | 来源 |
|------|------|------|------|
| Workflow 定义 | Python DSL | **YAML + Jinja2 路由**（零 token）| Conductor |
| Agent 接入 | 仅内部 | **BYOA（ACP + 外部 HTTP）** | Paperclip/Conductor |
| 协议 | 无 | **ACP + MCP** | Harnss/Goose/GitHub |
| 调度 | cron + state | **Heartbeat 队列**（DB + 合并） | Paperclip |
| Agent 模型 | "8 阶段是流水线" | **Org Chart + 角色/汇报线** | Paperclip |
| 目标体系 | 阶段名 | **Goal Ancestry 链** | Paperclip |
| Memory | 单一 | **Memento Man + 分层 Para** | Paperclip/Anthropic |
| 上下文 | 全量 | **3 模式（accumulate/last_only/explicit）** | Conductor |
| Action 输出 | 自由文本 | **Action Schema 强约束** | GitHub |
| 错误恢复 | 5-mode | **3 档（soft/hard/human）** | 实践简化 |
| 并行 | 静态 DAG | **parallel_group + 动态 for_each** | Conductor |
| 循环 | 单次 stage | **review_loop until+max_iter** | Conductor |
| 插件 | 三类 skill | **Plugin 架构（PyPI/npm 标准）** | Paperclip |
| 模板 | 无 | **Importable Company Templates** | Paperclip |
| 安全 | JWT/RBAC | **+ max_iter + wall_clock + dry-run** | Conductor |
| 审计 | 普通日志 | **不可变 hash-chain 审计** | Paperclip |
| 启动模式 | LLM 有记忆 | **Memento Man：每次注入 checklist** | Anthropic/Paperclip |
| Skills 复用 | skill registry | **+ workflow_registry + plugin 双层** | Conductor |
| Session 隔离 | 单 session | **每 agent 独立 session，无串味** | Conductor |

---

## 八、实施优先级（更新）

| 优先级 | 模块 | 工作量 | v4.2 新增要点 |
|--------|------|--------|--------------|
| **P0** | YAML Workflow Engine | 5-7 天 | Jinja2 路由 + 3 上下文模式 + review_loop |
| **P0** | HeartbeatScheduler | 3 天 | DB-backed 队列 + coalescing |
| **P0** | ACP Adapter | 3 天 | 内部 + 外部 agent 接入 |
| **P0** | LLMInterface | 2 天 | 沿用 v4.1 |
| **P0** | StateManager | 2 天 | 沿用 v4.1 |
| **P1** | MementoLoader + ParaMemory | 3 天 | Heartbeat checklist + 分层记忆 |
| **P1** | Org Chart + GoalAncestry | 2 天 | 角色/汇报线/预算 |
| **P1** | ActionValidator | 2 天 | 强类型 action 约束 |
| **P1** | 8 个 Stage Agent | 5 天 | 沿用 v4.1 + 用 YAML 编排 |
| **P2** | MCPClient | 3 天 | MCP 工具调用 |
| **P2** | PluginLoader | 3 天 | PyPI 风格 plugin |
| **P2** | React 前端 | 7 天 | Org Chart + DAG 编辑器 |
| **P2** | Company Template 机制 | 3 天 | Importable YAML |
| **P3** | SelfCorrectEngine 三档 | 3 天 | soft/hard/human |
| **P3** | Self-Improvement | 5 天 | 沿用 v3.5 思路 |

**预计总工期**：约 6-8 周（1 人）或 3-4 周（3 人团队）

---

## 九、与 2026 年主流生态对标

| 特性 | 本方案 v4.2 | Paperclip (70k⭐) | Conductor (MSFT) | Goose (47.8k⭐) | Routa (16k⭐) | Harnss |
|------|-------------|-------------------|------------------|-----------------|---------------|--------|
| YAML workflow | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| 确定性路由 | ✅ | ❌ | ✅ | ❌ | 部分 | ❌ |
| BYOA | ✅ | ✅ | 部分 | ❌ | ✅ | ✅ |
| ACP 支持 | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| MCP 支持 | ✅ | ❌ | 部分 | ✅ | ✅ | ✅ |
| Org Chart | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Goal Ancestry | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Heartbeat | ✅ | ✅ | ❌ | ❌ | 部分 | ❌ |
| Memento Man | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Plugin | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Importable Template | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Action Schema | ✅ | 部分 | 部分 | ❌ | 部分 | ❌ |
| 8 阶段 pipeline | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 模型无关 | ✅ | ✅ | 部分 | ❌ | ✅ | 部分 |
| 单二进制部署 | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Star 数量 | - | 70k | 6k+ | 47.8k | 16k | 小 |

**v4.2 几乎覆盖了所有主流生态的核心特性**，并在 **8 阶段 pipeline + 模型无关 + 模型适配层** 上有独到优势。

---

## 十、最终定位

> **v4.2 = Conductor 的 YAML 路由 + Paperclip 的 Org Chart/Heartbeat/Memento Man + Anthropic 的 2-Agent Harness + GitHub 的 Action Schema + YX 的 8 阶段 + 我们自创的 Skill DAG + 模型无关**
> 
> **是当前所有主流 AI R&D 编排系统优点的集大成者**，并具备：
> - **8 阶段结构化 pipeline**（vs 通用框架）
> - **模型无关**（vs Claude Code/Codex 锁死）
> - **状态机可灵活跳转**（vs 死板流程）
> - **真正的 Plugin 架构**（vs 简单 skill 注册表）
> - **Importable Templates**（vs 一次性配置）
