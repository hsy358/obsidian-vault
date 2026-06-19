# Self-Driving R&D · 独立可移植版 v4.1（深度优化）

> **版本定位**：v4.0 的深度优化版——修复方案 + 技术实现层面的关键问题
> **核心改进**：状态事务、Skill DAG、并发模型、错误恢复、可观测性、迁移路径
> **更新日期**：2026-06-19

---

## 零、v4.0 已知问题清单

| 类别 | v4.0 的问题 | v4.1 的改进 |
|------|-------------|-------------|
| **状态层** | YAML 单文件，并发写会冲突 | SQLite + YAML 双层：YAML 可读 + SQLite 事务 |
| **Skill 调度** | skill 串行调用，依赖关系不清晰 | **Skill DAG**：显式声明依赖，DAG 调度器并行执行 |
| **并发模型** | 单项目假设，多项目怎么办 | **多项目工作池** + 资源调度器（token budget + 并发上限）|
| **DecisionAgent** | "score >= 70" 太简化 | **5 层裁决规则**：环境/产物/质量/合规/成本 |
| **错误恢复** | 没提失败怎么办 | **5-mode self-correct**（沿用 v3.5）+ DLQ 模式 |
| **可观测性** | 没提 metrics/traces/logs | **三层观测**：metrics + traces + structured logs |
| **Skill 版本** | skill 没有版本管理 | Skill 注册表带 semver，强制版本检查 |
| **Skill Schema** | 输入输出松散 | **强类型 JSON Schema**，自动校验 |
| **前端** | 概念化，组件没拆 | **完整组件树 + 状态管理 + WebSocket 协议** |
| **迁移路径** | 没提从 v3.5 怎么迁 | **3 步迁移** + 适配层兼容旧 skill |
| **测试** | 完全没提 | **3 层测试**：unit + integration + e2e |
| **安全** | 一笔带过 | **3 层安全**：authn + authz + audit |

---

## 一、整体架构（v4.1）

```
┌──────────────────────────────────────────────────────────────┐
│  Frontend (React + Vite)                                      │
│  ├─ DashboardPage  ← 总览（所有项目）                          │
│  ├─ ProjectPage    ← 单项目（Pipeline + 4 面板）               │
│  ├─ SkillManager   ← Skill 注册表管理                         │
│  ├─ MetricsPage    ← 全局指标                                 │
│  └─ SettingsPage   ← 模型/通知/环境配置                       │
│  WebSocket 实时 + REST API                                     │
└──────────────────────────────────────────────────────────────┘
                              ↕
┌──────────────────────────────────────────────────────────────┐
│  Backend (Python 3.11+, FastAPI)                              │
│                                                                │
│  ┌───────────────── Application Layer ─────────────────────┐ │
│  │  ProjectService     # 多项目管理（CRUD）                  │ │
│  │  ExecutionService    # 阶段执行编排                       │ │
│  │  SkillService        # Skill 加载/注册/调用                │ │
│  │  NotificationService # 通知（飞书/微信/Slack）            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌───────────────── Domain Layer ─────────────────────────┐  │
│  │  LoopEngine         # GAMD 主循环（事件驱动）              │ │
│  │  StateMachine       # 9 状态机（YAML + SQLite）            │ │
│  │  SkillDAGScheduler  # Skill DAG 调度器（并行）            │ │
│  │  DecisionAgent      # 5 层裁决                            │ │
│  │  LLMInterface       # 模型适配                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌───────────────── Infrastructure Layer ──────────────────┐  │
│  │  DBManager          # SQLite（状态/审计/指标）             │ │
│  │  EventBus           # 事件总线（进程内 + 文件）            │ │
│  │  ConcurrencyManager # 资源池/信号量/token budget          │ │
│  │  Telemetry          # OpenTelemetry 集成                 │ │
│  │  Logger             # 结构化日志（JSON）                   │ │
│  └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
                              ↕
┌──────────────────────────────────────────────────────────────┐
│  External / Storage                                            │
│  ├─ projects/<name>/          ← 项目目录（每个项目独立）      │
│  │   ├─ .comet.yaml           ← 主状态（人类可读）             │
│  │   ├─ .state.db             ← SQLite（事务）                │
│  │   ├─ spec.md / tasks.json  ← 产物                          │
│  │   └─ artifacts/            ← 各阶段产物                    │
│  ├─ skills/<skill>/           ← Skill 目录                    │
│  ├─ lessons/                  ← 全局经验                       │
│  └─ vault.db                  ← 元数据/审计/指标              │
└──────────────────────────────────────────────────────────────┘
```

---

## 二、状态层（核心改进）

### 2.1 双层状态架构

**YAML 单层的问题**：
- 并发写会冲突（两个 stage 同时改）
- 没有事务（写到一半崩溃会损坏）
- 不支持复杂查询

**v4.1 双层设计**：
```
.comet.yaml  ← 人类可读（git 友好）
   │
   ├── 启动时：读 YAML → 导入 SQLite
   ├── 运行时：所有写走 SQLite（带事务 + 锁）
   └── 写回：关键事件 → 写回 YAML（commit hook）
```

### 2.2 SQLite Schema（核心表）

```sql
-- 项目表
CREATE TABLE projects (
    id           TEXT PRIMARY KEY,
    name         TEXT UNIQUE NOT NULL,
    status       TEXT NOT NULL,           -- active | paused | completed | failed
    current_stage TEXT NOT NULL,
    config       TEXT NOT NULL,           -- JSON
    created_at   TIMESTAMP,
    updated_at   TIMESTAMP
);

-- 阶段执行历史
CREATE TABLE stage_runs (
    id           TEXT PRIMARY KEY,
    project_id   TEXT NOT NULL,
    stage        TEXT NOT NULL,           -- access | explore | ... | archive
    status       TEXT NOT NULL,           -- pending | running | completed | failed
    score        INTEGER,                 -- 0-100
    skills_used  TEXT,                    -- JSON array
    artifacts    TEXT,                    -- JSON
    started_at   TIMESTAMP,
    ended_at     TIMESTAMP,
    error        TEXT,                    -- 失败原因
    retry_count  INTEGER DEFAULT 0,
    parent_run_id TEXT,                   -- 失败重试的父 run
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- 状态机转换日志
CREATE TABLE state_transitions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id   TEXT NOT NULL,
    from_stage   TEXT,
    to_stage     TEXT NOT NULL,
    from_status  TEXT,
    to_status    TEXT NOT NULL,
    actor        TEXT NOT NULL,           -- system | DecisionAgent | human
    reason       TEXT,
    ts           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Skill 调用记录
CREATE TABLE skill_invocations (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id   TEXT NOT NULL,
    stage_run_id TEXT NOT NULL,
    skill_name   TEXT NOT NULL,
    skill_version TEXT NOT NULL,
    input        TEXT,                    -- JSON
    output       TEXT,                    -- JSON
    status       TEXT NOT NULL,           -- success | failed | timeout
    duration_ms  INTEGER,
    tokens_used  INTEGER,
    error        TEXT,
    ts           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Gate 决策
CREATE TABLE gate_decisions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id   TEXT NOT NULL,
    stage_run_id TEXT NOT NULL,
    decision     TEXT NOT NULL,           -- PASS | PASS_WITH_WARNING | BLOCK | MANUAL_PASS
    score        INTEGER,
    rules_passed TEXT,                    -- JSON array
    rules_failed TEXT,
    reason       TEXT,
    actor        TEXT NOT NULL,           -- DecisionAgent | human
    ts           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 事件总线（用于跨进程通信）
CREATE TABLE events (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id   TEXT,
    type         TEXT NOT NULL,           -- state_change | skill_invoked | gate_decided | error
    payload      TEXT NOT NULL,           -- JSON
    ts           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    consumed     BOOLEAN DEFAULT 0
);

-- 审计日志（操作追溯）
CREATE TABLE audit_log (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    actor        TEXT NOT NULL,
    action       TEXT NOT NULL,
    target       TEXT,
    details      TEXT,
    ts           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2.3 状态机（修正）

v4.0 把阶段当成"8 个独立 stage"，但真实 R&D 中：
- 阶段可以**跳过**（小项目不需要探索）
- 阶段可以**重复**（验证不通过要回到 apply 修复）
- 阶段可以**并行**（提案 + 任务可以同时）

**v4.1 状态机**：

```python
# 状态转换规则（不是固定 8 段流程，而是可灵活跳转）
STAGE_GRAPH = {
    "access":  ["explore", "propose"],     # 接入后可以直接提案
    "explore": ["propose", "access"],      # 探索不通过要回到接入
    "propose": ["task", "explore"],        # 提案不通过要回到探索
    "task":    ["apply", "propose"],       # 任务确认不通过要回到提案
    "apply":   ["verify", "task"],         # 应用失败要回到任务
    "verify":  ["review", "apply", "failed"],  # 验证失败回到 apply
    "review":  ["archive", "verify", "failed"],  # 评审不通过回到 verify
    "archive": ["completed"],
    "failed":  ["access", "explore", "apply", "verify"],  # 失败可从任意技术阶段重启
    "completed": []                        # 终态
}
```

### 2.4 锁与并发

```python
class StateManager:
    def __init__(self, project_id):
        self.project_id = project_id
        self._lock_file = f".locks/{project_id}.lock"
    
    @contextmanager
    def exclusive_lock(self, timeout=30):
        """文件锁：避免两个 stage 并发写同一项目"""
        # 跨进程互斥（用 fcntl.flock）
        # ...
    
    def transition(self, from_stage, to_stage, actor, reason):
        """状态转换（带事务）"""
        with self.exclusive_lock():
            with self.db.transaction():
                # 1. 验证转换合法
                assert to_stage in STAGE_GRAPH[from_stage]
                # 2. 写 state_transitions 表
                self.db.insert("state_transitions", ...)
                # 3. 更新 projects.current_stage
                self.db.update("projects", ...)
                # 4. 触发事件
                self.event_bus.emit("state_change", ...)
                # 5. 写回 .comet.yaml（commit hook）
                self._sync_yaml()
```

---

## 三、Skill DAG 调度器（核心改进）

### 3.1 v4.0 的问题

v4.0 让 skill 串行调用，但实际：
- 多个 skill 之间可能有**依赖关系**（skill B 要等 skill A 的输出）
- 多个 skill 之间可能**无依赖**（可以并行）
- skill 可能**失败重试**或**降级**

### 3.2 Skill DAG 设计

```yaml
# skills/_registry.yaml 完整版（含 DAG）
version: "4.1"
skills:
  # ── 内置 Skill ──
  requirement-parser:
    type: builtin
    module: skills.requirement_parser
    version: "1.2.0"
    description: "解析自然语言需求 → spec.md"
    input_schema: ./requirement-parser/schema.json
    output_schema: ./requirement-parser/output_schema.json
    stages: [access]
    depends_on: []
    timeout_seconds: 60
    retry: {max: 2, backoff: exponential}
    critical: true            # 失败 = 阶段失败

  spec-validator:
    type: builtin
    module: skills.spec_validator
    version: "1.0.0"
    description: "验证 spec 完整性（验收标准/风险）"
    input_schema: ./spec-validator/schema.json
    output_schema: ./spec-validator/output_schema.json
    stages: [access]
    depends_on: [requirement-parser]    # 依赖上一个
    timeout_seconds: 30
    critical: true

  # ── 探索阶段 ──
  web-search:
    type: script
    entry: skills/web-search/run.sh
    version: "2.1.0"
    description: "网页搜索"
    input_schema: ./web-search/schema.json
    output_schema: ./web-search/output_schema.json
    stages: [explore]
    depends_on: []
    timeout_seconds: 120
    parallel_group: explore-search    # 同组内可并行
    critical: false

  code-search:
    type: script
    entry: skills/code-search/run.sh
    version: "1.0.0"
    description: "代码库搜索"
    input_schema: ./code-search/schema.json
    output_schema: ./code-search/output_schema.json
    stages: [explore]
    depends_on: []
    timeout_seconds: 60
    parallel_group: explore-search
    critical: false

  explore-synthesizer:
    type: builtin
    module: skills.explore_synthesizer
    version: "1.0.0"
    description: "汇总探索结果"
    input_schema: ./explore-synthesizer/schema.json
    output_schema: ./explore-synthesizer/output_schema.json
    stages: [explore]
    depends_on: [web-search, code-search]   # 等两个搜索都完成
    timeout_seconds: 90
    critical: true

  # ── 应用阶段 ──
  code-generator:
    type: builtin
    module: skills.code_generator
    version: "3.0.0"
    description: "根据 spec 生成代码"
    input_schema: ./code-generator/schema.json
    output_schema: ./code-generator/output_schema.json
    stages: [apply]
    depends_on: []
    timeout_seconds: 300
    critical: true

  test-writer:
    type: builtin
    module: skills.test_writer
    version: "2.0.0"
    description: "生成测试"
    input_schema: ./test-writer/schema.json
    output_schema: ./test-writer/output_schema.json
    stages: [apply]
    depends_on: [code-generator]    # 依赖代码先生成
    timeout_seconds: 300
    parallel_group: apply-tests
    critical: true

  linter:
    type: script
    entry: skills/linter/run.sh
    version: "1.0.0"
    description: "代码 lint"
    input_schema: ./linter/schema.json
    output_schema: ./linter/output_schema.json
    stages: [apply]
    depends_on: [code-generator]
    timeout_seconds: 60
    parallel_group: apply-tests
    critical: false

  # ── 验证阶段 ──
  test-runner:
    type: script
    entry: skills/test-runner/run.sh
    version: "1.5.0"
    description: "运行测试套件"
    input_schema: ./test-runner/schema.json
    output_schema: ./test-runner/output_schema.json
    stages: [verify]
    depends_on: []      # 依赖 apply 产物（目录级）
    timeout_seconds: 600
    critical: true

  security-scanner:
    type: script
    entry: skills/security-scanner/run.sh
    version: "1.0.0"
    description: "安全扫描"
    input_schema: ./security-scanner/schema.json
    output_schema: ./security-scanner/output_schema.json
    stages: [verify]
    depends_on: []
    timeout_seconds: 300
    parallel_group: verify-checks
    critical: true

  benchmark-runner:
    type: script
    entry: skills/benchmark-runner/run.sh
    version: "1.0.0"
    description: "性能基准"
    input_schema: ./benchmark-runner/schema.json
    output_schema: ./benchmark-runner/output_schema.json
    stages: [verify]
    depends_on: []
    timeout_seconds: 600
    parallel_group: verify-checks
    critical: false
```

### 3.3 DAG 调度器实现

```python
class SkillDAGScheduler:
    """拓扑排序 + 并行执行"""

    def __init__(self, registry: dict):
        self.registry = registry

    def execute(self, stage: str, context: dict) -> dict:
        """执行某 stage 的所有 skill"""
        # 1. 收集该 stage 的所有 skill
        skills = self._skills_for_stage(stage)
        if not skills:
            return {}

        # 2. 构建 DAG
        dag = self._build_dag(skills)

        # 3. 按拓扑层级并行执行
        results = {}
        for layer in self._topological_layers(dag):
            # 同一层内的 skill 并行执行
            with ThreadPoolExecutor(max_workers=len(layer)) as pool:
                futures = {
                    pool.submit(self._run_skill, skill, context, results): skill
                    for skill in layer
                }
                for future in as_completed(futures):
                    skill = futures[future]
                    result = future.result()
                    results[skill.name] = result

                    # 关键 skill 失败 → 立即停止
                    if skill.critical and not result.success:
                        self._handle_critical_failure(skill, result)
                        raise SkillCriticalError(skill.name, result.error)

        return results

    def _topological_layers(self, dag) -> list[list[Skill]]:
        """Kahn 算法分层：每层内的节点可并行"""
        in_degree = {n: 0 for n in dag.nodes}
        for n in dag.nodes:
            for dep in dag.predecessors(n):
                in_degree[n] += 1

        layers = []
        current = [n for n, d in in_degree.items() if d == 0]

        while current:
            layers.append(current)
            next_layer = []
            for n in current:
                for succ in dag.successors(n):
                    in_degree[succ] -= 1
                    if in_degree[succ] == 0:
                        next_layer.append(succ)
            current = next_layer

        return layers

    def _run_skill(self, skill, context, prev_results) -> SkillResult:
        """执行单个 skill（带重试 + 超时 + 监控）"""
        for attempt in range(skill.retry.max + 1):
            try:
                start = time.time()
                result = self._invoke(skill, context, prev_results)
                result.duration_ms = (time.time() - start) * 1000

                if result.success:
                    return result
                elif attempt < skill.retry.max:
                    wait = skill.retry.backoff(attempt)
                    time.sleep(wait)
                    continue
                else:
                    return result

            except TimeoutError:
                if attempt < skill.retry.max:
                    continue
                return SkillResult(success=False, error="timeout")
```

### 3.4 Skill Schema（强类型）

```json
// skills/code-generator/schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CodeGeneratorInput",
  "type": "object",
  "required": ["spec_path", "tech_stack", "output_dir"],
  "properties": {
    "spec_path": {
      "type": "string",
      "description": "spec.md 的绝对路径"
    },
    "tech_stack": {
      "type": "object",
      "properties": {
        "language": {"enum": ["python", "typescript", "go", "rust"]},
        "framework": {"type": "string"},
        "dependencies": {"type": "array", "items": {"type": "string"}}
      }
    },
    "output_dir": {
      "type": "string",
      "description": "代码输出目录"
    }
  }
}
```

---

## 四、DecisionAgent（5 层裁决）

### 4.1 v4.0 的问题

只看了 score >= 70，太简化。真实的 R&D 阶段有**多种失败维度**。

### 4.2 5 层裁决规则

```python
class DecisionAgent:
    """5 层规则，每层独立评估"""

    def decide_gate(self, project, stage_run) -> GateDecision:
        results = []

        # Layer 1: 环境检查（这个 stage 能跑起来吗？）
        env = self._check_environment(stage_run.skills_used)
        results.append(("environment", env))

        # Layer 2: 产物检查（必需产物都生成了吗？）
        artifacts = self._check_artifacts(stage_run.stage, stage_run.artifacts)
        results.append(("artifacts", artifacts))

        # Layer 3: 质量检查（产物质量是否合格？）
        quality = self._check_quality(stage_run.stage, stage_run.artifacts)
        results.append(("quality", quality))

        # Layer 4: 合规检查（是否符合 spec/标准/安全？）
        compliance = self._check_compliance(stage_run.stage, stage_run.artifacts)
        results.append(("compliance", compliance))

        # Layer 5: 成本检查（token 预算是否超支？）
        cost = self._check_cost(project, stage_run)
        results.append(("cost", cost))

        # 汇总：所有 layer 都要过
        failed = [name for name, r in results if not r.passed]
        score = sum(r.score for _, r in results) / len(results)

        if not failed:
            decision = "PASS"
        elif all(name in ["cost"] for name in failed):
            decision = "PASS_WITH_WARNING"  # 成本超可接受
        else:
            decision = "BLOCK"

        return GateDecision(
            decision=decision,
            score=int(score),
            rules_passed=[name for name, r in results if r.passed],
            rules_failed=failed,
            reason=self._format_reason(results)
        )

    def _check_environment(self, skills) -> RuleResult:
        """环境检查：每个 skill 跑前都验证了 python/node/git/依赖"""
        # 调每个 skill 的 pre_check 钩子
        # ...

    def _check_artifacts(self, stage, artifacts) -> RuleResult:
        """产物检查：每个 stage 有必填产物（如 apply → src/, tests/）"""
        required = {
            "access": ["spec.md"],
            "explore": ["explore.md"],
            "propose": ["propose.md"],
            "task": ["tasks.json"],
            "apply": ["src/", "tests/"],
            "verify": ["verify-report.json"],
            "review": ["review.md"],
            "archive": ["lessons.md"]
        }
        missing = [a for a in required.get(stage, []) if a not in artifacts]
        return RuleResult(
            passed=len(missing) == 0,
            score=100 if not missing else max(0, 100 - len(missing) * 25),
            details=f"Missing: {missing}" if missing else "All artifacts present"
        )

    def _check_quality(self, stage, artifacts) -> RuleResult:
        """质量检查：阶段相关质量指标"""
        checks = {
            "apply": self._check_code_quality,         # lint/format/coverage
            "verify": self._check_test_coverage,       # coverage/perf/security
            "review": self._check_doc_completeness,
        }
        check_fn = checks.get(stage, lambda a: RuleResult(passed=True, score=100))
        return check_fn(artifacts)

    def _check_compliance(self, stage, artifacts) -> RuleResult:
        """合规检查：是否遵守 spec/公司标准/安全规范"""
        # ...

    def _check_cost(self, project, stage_run) -> RuleResult:
        """成本检查：单项目 token 预算"""
        # ...
```

### 4.3 Hard Gate vs Soft Gate

```python
HARD_GATES = {
    "access":  {"after": True,  "notify": ["feishu", "wechat"]},   # 接入后必须人确认
    "verify":  {"after": True,  "notify": ["feishu", "wechat"]},   # 验证后必须人确认
    "archive": {"after": True,  "notify": ["feishu"]},             # 归档后通知（可自动）
}

SOFT_GATES = {
    # 其他阶段：自动通过，失败才通知
}
```

---

## 五、并发与资源管理

### 5.1 多项目并发

```python
class ConcurrencyManager:
    """全局资源池"""

    def __init__(self, config):
        # 全局并发上限（API 限流）
        self.global_concurrency = config.max_concurrent  # 默认 4
        # Token 预算（按模型分组）
        self.token_budget = {
            "minimax/MiniMax-M3": TokenBucket(capacity=1_000_000, refill_rate=100_000),
            "minimax/MiniMax-M2.7": TokenBucket(capacity=2_000_000, refill_rate=200_000),
            "deepseek/DeepSeek-R1": TokenBucket(capacity=500_000, refill_rate=50_000),
        }
        # API 速率限制
        self.rate_limiter = {
            model: AsyncRateLimiter(rpm=60)  # 每分钟 60 次
            for model in self.token_budget
        }
        # 信号量：全局并发
        self.semaphore = asyncio.Semaphore(self.global_concurrency)

    async def acquire(self, model: str, estimated_tokens: int) -> ContextManager:
        """获取执行许可（带 token 预算检查）"""
        async def _acquire():
            await self.semaphore.acquire()
            await self.rate_limiter[model].acquire()
            if not self.token_budget[model].try_consume(estimated_tokens):
                raise BudgetExhaustedError(model)
        return _acquire
```

### 5.2 Sub-35min Session（沿用 v3.5 原则）

```python
SESSION_TIMEOUT = 30 * 60  # 30 分钟硬上限

class SessionManager:
    """长任务自动拆分"""

    async def run_with_timeout(self, task):
        try:
            return await asyncio.wait_for(
                self._execute(task),
                timeout=SESSION_TIMEOUT
            )
        except asyncio.TimeoutError:
            # 超时：写 handoff，下个 session 续跑
            handoff = self._write_handoff(task)
            return SessionResult(
                status="handoff",
                handoff_path=handoff.path,
                message=f"Session timeout, handoff at {handoff.path}"
            )
```

---

## 六、可观测性（OpenTelemetry 集成）

### 6.1 三层观测

```python
# 配置 OpenTelemetry
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp import OTLPSpanExporter

# 1. Traces（链路追踪）
tracer = trace.get_tracer("self-driving-rd")

# 2. Metrics（指标）
meter = metrics.get_meter("self-driving-rd")
stage_duration = meter.create_histogram("stage.duration.ms")
gate_decisions = meter.create_counter("gate.decisions")
token_usage = meter.create_counter("llm.tokens.used")

# 3. Logs（结构化日志）
import structlog
logger = structlog.get_logger()

# 在 stage 执行时
with tracer.start_as_current_span("stage.run") as span:
    span.set_attribute("project.id", project.id)
    span.set_attribute("stage", stage.name)
    span.set_attribute("score", stage_run.score)

    stage_duration.record(duration_ms, {"stage": stage.name})
    token_usage.add(tokens, {"model": model, "stage": stage.name})
```

### 6.2 关键指标

```
# 业务指标
- project.success_rate          # 项目成功率
- stage.avg_duration            # 阶段平均耗时
- stage.score.distribution      # 阶段得分分布
- gate.decision.distribution    # 门禁决策分布
- skill.invocation.success_rate # Skill 成功率
- llm.tokens.used.per_stage     # 每阶段 token 用量

# 系统指标
- api.rate_limit.remaining      # API 限流余量
- db.connection.pool.size       # DB 连接池
- concurrent.projects.active    # 活跃项目数
- dlq.size                      # Dead Letter Queue 长度
```

---

## 七、错误恢复（5-Mode Self-Correct）

```python
class SelfCorrectEngine:
    """5 种修复模式，按级尝试"""

    async def recover(self, stage_run, error) -> RecoveryResult:
        for mode in [
            self._mode1_retry,         # 简单重试（网络错误）
            self._mode2_reformulate,   # 重新构造 prompt
            self._mode3_switch_model,  # 切换模型
            self._mode4_skip_skill,    # 跳过非关键 skill
            self._mode5_handoff_human, # 升级到人工
        ]:
            result = await mode(stage_run, error)
            if result.success:
                # 记录成功模式（自学习）
                self.method_library.add_success(
                    stage=stage_run.stage,
                    error=type(error).__name__,
                    mode=mode.__name__
                )
                return result

        # 全部失败：写 DLQ
        self.dlq.add(stage_run, error)
        # 触发 Hard Gate
        await self.notification_service.hard_gate_notify(stage_run, error)
        return RecoveryResult(success=False, handoff=True)
```

---

## 八、迁移路径（v3.5 → v4.1）

### 8.1 三步迁移

```bash
# Step 1: 安装 v4.1
git clone https://github.com/xxx/self-driving-rd.git
cd self-driving-rd && pip install -e .

# Step 2: 从 OpenClaw workspace 导出 skill
selfdriving migrate import-skills \
  --from /root/.openclaw/workspace/skills \
  --to ./skills

# Step 3: 把现有 v3.5 项目接入 v4.1
selfdriving migrate import-project \
  --project my-tool \
  --from /root/vault/Research \
  --to ./projects/my-tool
```

### 8.2 兼容层

```python
# v4.1 可以**读** v3.5 的项目结构（.comet.yaml 风格）
# 通过 v3 适配器转换：

class V3Adapter:
    """把 v3.5 的项目状态转成 v4.1 的状态"""

    def import_project(self, v3_project_path):
        # 读 v3.5 的 spec.md, tasks.json, handoff/
        # 写到 v4.1 的 SQLite + YAML
        # 状态机从 v3 的"9 stage 强制流程"转成 v4.1 的"可灵活跳转"
        ...
```

---

## 九、测试策略

### 9.1 三层测试

```
tests/
├── unit/                          # 单元测试
│   ├── test_state_machine.py      # 状态转换合法性
│   ├── test_skill_dag.py         # DAG 调度
│   ├── test_decision_agent.py    # 5 层裁决
│   └── test_skill_router.py
│
├── integration/                   # 集成测试
│   ├── test_full_pipeline.py     # 跑完整 8 阶段（小项目）
│   ├── test_skill_failure.py     # skill 失败的恢复
│   ├── test_concurrent_projects.py # 多项目并发
│   └── test_state_persistence.py # 状态持久化
│
└── e2e/                          # 端到端
    ├── test_real_project.py      # 真实项目跑通
    └── test_observability.py     # 可观测性
```

### 9.2 关键测试用例

- **状态机非法转换被拒绝**（不能从 verify 直接跳到 archive）
- **Skill 失败后能恢复**（test-runner 超时 → 切到小范围重跑）
- **DecisionAgent 5 层都失败时进入 DLQ**
- **多项目并发 token 预算正确**
- **`.comet.yaml` 损坏能从 SQLite 恢复**

---

## 十、前端架构（v4.1 详细版）

### 10.1 组件树

```
src/
├── App.tsx
├── router.tsx
├── pages/
│   ├── DashboardPage.tsx           # 总览：所有项目
│   ├── ProjectPage.tsx             # 单项目详情
│   ├── SkillManagerPage.tsx        # Skill 管理
│   ├── MetricsPage.tsx             # 指标
│   └── SettingsPage.tsx
├── components/
│   ├── pipeline/
│   │   ├── PipelineTrack.tsx       # 8 阶段进度条
│   │   ├── StageNode.tsx           # 单个阶段
│   │   └── PipelineLegend.tsx
│   ├── process/
│   │   ├── ProcessPanel.tsx        # 过程日志面板
│   │   ├── LogStream.tsx           # 实时日志流（WebSocket）
│   │   └── MetricCard.tsx
│   ├── decision/
│   │   ├── DecisionPanel.tsx       # 决策面板
│   │   ├── EnvironmentCheck.tsx    # 环境检查
│   │   ├── ChecklistItems.tsx
│   │   └── ManualPassButton.tsx    # 人工 PASS
│   ├── agent/
│   │   ├── AgentWorkbench.tsx      # ReAct 状态
│   │   └── ReActTrace.tsx
│   └── common/
│       ├── Layout.tsx
│       ├── Sidebar.tsx
│       └── Header.tsx
├── state/
│   ├── projectStore.ts             # Zustand
│   ├── pipelineStore.ts
│   └── notificationStore.ts
├── services/
│   ├── api.ts                      # REST 客户端
│   └── websocket.ts                # WebSocket 客户端
└── types/
    └── api.ts                      # TypeScript 类型（与后端同步生成）
```

### 10.2 WebSocket 协议

```typescript
// 前端订阅
ws.send(JSON.stringify({
  action: "subscribe",
  channel: "project.${projectId}",
}))

// 后端推送
ws.send(JSON.stringify({
  type: "stage.status_changed",
  project_id: "...",
  stage: "verify",
  status: "completed",
  score: 88,
  timestamp: "2026-06-19T..."
}))

ws.send(JSON.stringify({
  type: "skill.invocation.completed",
  skill: "test-runner",
  status: "failed",
  error: "timeout"
}))
```

---

## 十一、安全模型

### 11.1 3 层安全

```yaml
# security/auth.yaml
authn:                              # 身份认证
  method: jwt
  secret: ${JWT_SECRET}
  expires_in: 86400

authz:                              # 权限控制
  roles:
    - name: admin
      permissions: ["*"]
    - name: developer
      permissions: ["project.read", "project.run", "skill.read"]
    - name: viewer
      permissions: ["project.read", "metrics.read"]

audit:                              # 审计
  enabled: true
  log_path: ./logs/audit.log
  retention_days: 90
  redact_fields: [api_key, password, token]
```

### 11.2 API Key 安全管理

```python
# config.yaml 里的敏感字段全部从环境变量读
# 启动时校验必需 key 存在

def load_config():
    config = yaml.safe_load(open("config.yaml"))
    for model_name, model_cfg in config["models"].items():
        # api_key 必须是 ${ENV_VAR} 格式
        if not model_cfg["api_key"].startswith("${"):
            raise ConfigError("api_key must be env var, not literal")
    return config
```

---

## 十二、改进对比总结

| 维度 | v4.0 | v4.1 | 提升 |
|------|------|------|------|
| 状态层 | YAML 单文件 | **YAML + SQLite 双层，事务支持** | 并发安全 |
| Skill 调度 | 串行调用 | **DAG + 拓扑并行** | 性能 |
| Skill 类型 | 松散 | **JSON Schema 强类型** | 可靠性 |
| 决策 | 单一分数 | **5 层规则（环境/产物/质量/合规/成本）** | 准确度 |
| 错误恢复 | 无 | **5-mode self-correct** | 韧性 |
| 状态机 | 固定 8 段 | **可灵活跳转** | 真实场景 |
| 资源管理 | 单项目 | **多项目 + token budget + 限流** | 可扩展 |
| 可观测性 | 无 | **OpenTelemetry 3 层** | 可维护 |
| 测试 | 无 | **unit + integration + e2e** | 质量 |
| 前端 | 概念 | **完整组件树 + WebSocket** | 可落地 |
| 安全 | 无 | **JWT + RBAC + audit** | 企业可用 |
| 迁移 | 无路径 | **3 步迁移 + 兼容层** | 可演进 |
| 部署 | 概念 | **docker-compose + env vars** | 一键起 |

**v4.1 才是真正可落地的版本**。
