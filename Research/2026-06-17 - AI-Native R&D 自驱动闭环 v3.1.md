---
title: "AI-Native R&D 自驱动闭环 v3.1（35min 规则 + Ralph Loop + HTN + 5-Layer Runtime + DeepWiki）"
author: "OpenClaw 小助"
publish_date: "2026-06-17"
saved_date: "2026-06-17"
type: research-report
okf_metadata:
  schema: okf-v0.1-inspired
  version: 3.1
  supersedes: 2026-06-17 AI-Native R&D 自驱动闭环 v3.0
  evolution: v3.0 → v3.1（增加 7 个深度研究产物）
status: implementable
---

# AI-Native R&D 自驱动闭环 v3.1

> **核心目标**：给你需求 → 充分理解 → 拆解任务 → 编码/测试/验证/修复/再验证 → 交付完整产品。AI 自驱动，10+ 小时，中间减少人工。
> **v3.1 vs v3.0**：在 v3.0 基础上加入 7 个深度研究产物（sub-35min 规则、Ralph Loop、HTN、DeepWiki、5-Layer Runtime、SpecKit、MCTS）

---

## 一、v3.0 → v3.1 关键升级（7 个新能力）

| 序号 | 新能力 | 来源 | 解决的问题 |
|---|---|---|---|
| 1 | **Sub-35min Session 规则** | Zylos Research 2026 | AI session > 35min 性能下降 |
| 2 | **Ralph Loop（1 行 bash）** | Huntley 2025 | 长跑 + fresh context + filesystem memory |
| 3 | **HTN Planning** | arxiv 2605.07707 (NeurIPS 2026) | 任务分解 + 减少 75% LLM 查询 |
| 4 | **Codebase Knowledge Graph** | Devin DeepWiki | Agent "不知道代码有什么" |
| 5 | **5-Layer Durable Runtime** | Orkes | 生产级 crash recovery |
| 6 | **SpecKit 3 阶段** | GitHub SpecKit | spec → plan → tasks 标准化 |
| 7 | **MCTS for Critical Decisions** | HPlan 2026 | 架构选型 / 库选择 |
| 8 | **Reflexion Memory** | Princeton/MIT 2023 | "为什么失败" 跨 session 记忆 |
| 9 | **Dead-Letter Queue** | Brightlume AI | 失败任务不删除，排队人工 |
| 10 | **Self-Correction 5 模式** | Micheal Lanham | 真自校正 vs 简单 retry |

---

## 二、Sub-35min Session 规则（最关键发现）

### 2.1 来源（Zylos Research 2026）

> **"Every AI agent experiences performance degradation after 35 minutes of human time spent on a task."**

> AI task duration doubling every 7 months：
> - 2026: 2-hour tasks autonomously
> - Late 2026: 8-hour workdays
> - 2028: full work weeks (40h)
> - 2029: work months (167h)

### 2.2 我们的应对

```python
# orchestrator.py 强制规则
MAX_SESSION_MINUTES = 30  # 留 5min buffer

def run_subagent(agent, task):
    start = time.time()
    
    # 监控 session 时长
    while not done:
        if (time.time() - start) / 60 > MAX_SESSION_MINUTES:
            log(f"⚠️ Session {agent} approaching 35min limit, forcing handoff")
            write_handoff()
            commit()
            return "HANDOFF_REQUIRED"
        
        # 继续 sub-agent 循环
        ...
```

### 2.3 Session 切分策略

```
总任务（如构建完整应用）= 10+ 小时
÷ sub-35min session
= 至少 18 个 session
= 每个 session 必须可独立续跑
= 必须有 Structured Handoff（v3.0 已建）
```

---

## 三、Ralph Loop（1 行 bash 实现）

### 3.1 来自 Huntley 2025

```bash
# 最简 Ralph Loop（核心）
while true; do
  cat PROMPT.md | claude-code --task "$(cat)"
done
```

**核心思想**：
- `while true` 持续跑
- 每次 fresh context
- Filesystem + git = memory
- "Persistence over precision, repetition over refinement"

### 3.2 LangChain Deep Agents 集成

```python
# deepagents/examples/ralph_mode
from deepagents import RalphMode

ralph = RalphMode(
    agent=claude_code_agent,
    filesystem=project_fs,
    prompt="""你是 AI 软件工程师。
读取 /root/vault/Projects/{name}/spec.md
读取 /root/vault/Projects/{name}/progress.txt
读取 /root/vault/Projects/{name}/tasks.json
执行下一任务
写 handoff.md
git commit
如果所有任务完成，输出 'TASK_COMPLETE' 退出
否则继续
""",
    max_iterations=200,
    stop_on_text="TASK_COMPLETE",
)
ralph.run()
```

### 3.3 我们的集成

```python
# self-driving-rd/ralph_engine.py
class RalphEngine:
    """Ralph Loop 引擎（v3.1 核心）"""
    
    def __init__(self, project_root, agent="claude-code"):
        self.project = Path(project_root)
        self.agent = agent
        self.iteration = 0
        self.max_iter = 200
        self.max_minutes = 30  # sub-35min rule
        self.start = time.time()
    
    def run(self):
        log(f"🐹 Ralph Loop start: {self.project}")
        
        while self.iteration < self.max_iter:
            self.iteration += 1
            
            # 1. 读 prompt（带 Anti-Anxiety）
            prompt = self.read_prompt()
            
            # 2. 读 handoff（接续上 session）
            handoff = self.read_handoff()
            
            # 3. 跑一个 sub-35min session
            output = self.run_subagent(prompt, handoff)
            
            # 4. 检查完成
            if "TASK_COMPLETE" in output:
                log(f"✅ DONE after {self.iteration} iterations")
                return "OK"
            
            # 5. 检查超时
            elapsed_min = (time.time() - self.start) / 60
            if elapsed_min > self.max_minutes:
                log(f"⏱️ 30min reached, forcing handoff")
                self.force_handoff()
                # 重置 start（让下个 session 跑 30min）
                self.start = time.time()
                continue
            
            # 6. Sleep 避免 hot loop
            time.sleep(60)
        
        return "MAX_ITER_REACHED"
    
    def read_prompt(self):
        return f"""
你是 AI 软件工程师，负责项目 {self.project.name}。
这是多 session 项目的第 {self.iteration} 次迭代。
不要质疑之前 session 的决策，信任 /handoff/ 目录。

读取：
- spec.md（锁定）
- progress/progress.txt（跨 session 续跑）
- handoff/session-{self.iteration - 1}.md（上次交接）

执行下一任务：
- 改 tasks.json
- 写代码
- 跑测试
- 写 handoff.md
- git commit

如果所有任务完成，输出 'TASK_COMPLETE'
否则不要输出这个字符串，继续
"""
```

---

## 四、HTN Planning（NeurIPS 2026）

### 4.1 核心思想

> **Hierarchical Task Network (HTN)**：复合任务（compound）通过 methods 分解为基本任务（primitive）。

### 4.2 在 LLM Agent 中的应用

```python
class HTNPlanner:
    """HTN 风格任务分解器（v3.1）"""
    
    def __init__(self, llm):
        self.llm = llm
        self.method_library = self.load_methods()  # 领域知识
    
    def decompose(self, compound_task):
        """分解复合任务"""
        prompt = f"""
        复合任务: {compound_task}
        
        候选方法（从 method library）:
        {self.method_library.find_methods(compound_task)}
        
        任务: 选一个 method 把复合任务分解为子任务
        输出: list of subtasks
        """
        plan = self.llm.generate(prompt)
        return plan
    
    def refine_until_primitive(self, tasks):
        """递归分解直到全是 primitive"""
        primitive_tasks = []
        compound_tasks = [t for t in tasks if t.type == "compound"]
        
        for ct in compound_tasks:
            subtasks = self.decompose(ct)
            # 递归
            primitive_tasks.extend(self.refine_until_primitive(subtasks))
        
        primitive_tasks.extend([t for t in tasks if t.type == "primitive"])
        return primitive_tasks
```

### 4.3 减少 75% LLM 查询

- 简单任务：用 method library 直接展开（无 LLM）
- 复杂任务：HTN 一次分解（1 LLM call）
- vs 直接让 LLM 拆 100 个任务（100 calls）

---

## 五、Codebase Knowledge Graph（Devin DeepWiki 简化版）

### 5.1 轻量实现（不依赖向量数据库）

```python
# knowledge_graph.py
class CodebaseKG:
    """轻量代码库知识图谱"""
    
    def __init__(self, project_root):
        self.project = Path(project_root)
        self.kg_file = self.project / "knowledge_graph.json"
        self.kg = self.load()
    
    def index(self):
        """扫描代码库，建立索引"""
        # 每个模块/函数：
        node = {
            "path": "src/auth/login.py",
            "type": "module",
            "purpose": "用户登录逻辑（自描述）",
            "dependencies": ["src/db/users.py", "src/utils/jwt.py"],
            "dependents": ["src/api/auth_routes.py"],
            "tests": ["tests/test_login.py"],
            "recent_changes": [  # git log
                {"date": "2026-06-16", "msg": "implement login"},
            ],
            "key_functions": [
                {"name": "login", "args": ["email", "password"], "returns": "JWT"},
            ],
        }
        self.kg[node["path"]] = node
    
    def query(self, task):
        """Agent 查询相关模块"""
        prompt = f"""
        任务: {task}
        
        知识图谱（相关部分）:
        {self.find_relevant(task)}
        
        输出: 哪些模块需要改？哪些函数需要参考？
        """
        return self.llm.generate(prompt)
```

### 5.2 vs Devin DeepWiki

| Devin DeepWiki | 我们的轻量版 |
|---|---|
| 持续更新的交互式知识图谱 | ✅ JSON 文件 |
| 代码 + 元数据索引 | ✅ 文件路径 + 依赖 + 测试 |
| Devin Search 深度检索 | ✅ 简单 query |
| Kevin 32B 专用模型 | ❌ 用通用 LLM |
| 开源项目已用 | ❌ 我们自用 |

**够用就 OK**（不需要上重型 KG 库）

---

## 六、5-Layer Durable Runtime（Orkes 模式）

### 6.1 5 层架构

```
┌────────────────────────────────────────────────────────────┐
│ L5: Human-in-the-Loop                                       │
│   ├─ Hard Gate 通知（微信）                                │
│   ├─ 决策文件监听                                          │
│   └─ Dead-Letter Queue（3+ 失败任务）                     │
├────────────────────────────────────────────────────────────┤
│ L4: Observability                                           │
│   ├─ Trace 记录（每步 prompt+response+actions）           │
│   ├─ 指标收集（tokens / 时长 / 失败率）                  │
│   └─ Dashboard（简单文本报告）                           │
├────────────────────────────────────────────────────────────┤
│ L3: Orchestrator                                            │
│   ├─ Loop Engine（v3.1 Ralph Loop）                       │
│   ├─ HTN Planner                                           │
│   └─ Sub-agent 调度                                        │
├────────────────────────────────────────────────────────────┤
│ L2: State Store                                              │
│   ├─ progress.txt（主进度）                                │
│   ├─ handoff/session-N.md（每次 session 交接）             │
│   ├─ tasks.json（状态机）                                  │
│   ├─ dead_letter.json（失败队列）                          │
│   └─ 每次 sub-task 完成 → 写                              │
├────────────────────────────────────────────────────────────┤
│ L1: Agent Runtime                                            │
│   ├─ LLM 调度（Claude Code / Codex / OpenClaw agents）     │
│   ├─ Tool 调度（读写文件 / 跑命令 / git）                 │
│   └─ Sandbox per task（git branch 隔离）                  │
└────────────────────────────────────────────────────────────┘
```

### 6.2 每层失败模式

| 层 | 失败模式 | 应对 |
|---|---|---|
| L1 | LLM 超时 / 工具错误 | 重试 + 切换 model |
| L2 | 文件丢失 / git 损坏 | 多副本（git + local + vault）|
| L3 | Orchestrator 卡死 | Watchdog（cron 监控）|
| L4 | Trace 丢失 | 异步写 + 重试 |
| L5 | 决策超时 | 自动通过 + 记录 |

---

## 七、SpecKit 3 阶段对齐

### 7.1 GitHub SpecKit 流程

```
/speckit.spec   → 写规格
/speckit.plan   → 写计划
/speckit.tasks  → 拆任务
```

### 7.2 我们的对齐

```
spec.md    ↔ /speckit.spec
plan.md    ↔ /speckit.plan
tasks.json ↔ /speckit.tasks
```

### 7.3 价值

- GitHub/Microsoft 维护的标准
- 工具链兼容（spec-kit CLI）
- 团队协作通用

---

## 八、MCTS for Critical Decisions

### 8.1 何时用 MCTS

- 架构选型（多个方案）
- 库选择
- API 设计
- 性能 vs 可维护性 取舍

### 8.2 简单实现

```python
def mcts_decide(options, evaluator, iterations=5):
    """Monte Carlo Tree Search for critical decisions"""
    best = options[0]
    best_score = -1
    
    for opt in options:
        score = 0
        # Rollout: 模拟此选项的执行结果
        for _ in range(iterations):
            sim_result = simulate(opt, evaluator)
            score += sim_result
        
        if score > best_score:
            best = opt
            best_score = score
    
    return best

# 用法
architectures = [arch_a, arch_b, arch_c]
chosen = mcts_decide(
    architectures,
    evaluator=lambda arch: simulate_5_years(arch),
    iterations=3
)
```

### 8.3 vs Tournament 模式

| Tournament（v3.0）| MCTS（v3.1）|
|---|---|
| 3 方案直接对比 | N 方案 + 模拟推演 |
| 一次性评判 | 多次 rollout 评估 |
| 适合架构 | 适合复杂决策 |
| 简单 | 需要模拟器 |

---

## 九、Reflexion Memory（自我反思存储）

### 9.1 来自 Princeton/MIT 2023

> Verbal self-reflection stored in persistent memory

### 9.2 实现

```python
class ReflexionMemory:
    """失败 → 反思 → 记忆（v3.1 新增）"""
    
    def __init__(self, project_root):
        self.path = Path(project_root) / "reflexion.md"
    
    def add(self, task, error, reflection):
        """每次失败写一条反思"""
        with self.path.open("a") as f:
            f.write(f"""
## {datetime.now()} - {task}

### Error
{error}

### Reflection
{reflection}

### Avoid Next Time
{reflection.avoidance}

""")
    
    def search(self, current_task):
        """失败前先搜相关反思"""
        if not self.path.exists():
            return ""
        return llm_search(self.path.read_text(), current_task)
```

### 9.3 完整自校正循环

```
sub-agent 失败
  ↓
error 进 Dead-Letter Queue
  ↓
Reflexion Agent 分析（"为什么失败"）
  ↓
写 reflexion.md（persistent memory）
  ↓
下次同类任务 → 先搜反思 → 避免重复
```

---

## 十、Self-Correction 5 模式（Lanham 框架）

### 10.1 5 种真正的自校正（vs 简单 retry）

| 模式 | 说明 | 我们的实现 |
|---|---|---|
| **1. Self-Critique** | LLM 评自己输出 | ❌ Anthropic 警告此为陷阱 |
| **2. External Critique** | 独立 LLM 评 | ✅ Adversarial Evaluator（v3.0）|
| **3. Tool-based Verification** | 用工具验证（编译/测试）| ✅ CI / pytest |
| **4. Iterative Refinement** | 多次迭代改进 | ✅ Ralph Loop |
| **5. Tree Search** | 多种路径搜索 | ✅ MCTS（v3.1）|

### 10.2 我们的 Self-Heal 升级

```python
# v3.1 自校正（5 模式组合）
def self_correct(task, output):
    # 1. Tool-based: 跑测试
    test_pass = run_tests()
    if not test_pass: return "FIX_TESTS"
    
    # 2. External: Adversarial Evaluator
    eval_pass = adversarial_eval(output)
    if not eval_pass: return "REVISE_OUTPUT"
    
    # 3. Iterative: Ralph Loop 重试（最多 3 次）
    for attempt in range(3):
        output = refine(output, eval_pass.feedback)
        if all_checks_pass(output): return "OK"
    
    # 4. Tree Search: 换思路
    alt_output = try_alternative(task)
    if check(alt_output): return "OK"
    
    # 5. Dead-Letter: 排队人工
    return "DEAD_LETTER"
```

---

## 十一、Dead-Letter Queue（失败任务管理）

### 11.1 设计

```python
class DeadLetterQueue:
    """失败任务不删除，排队等人工 review"""
    
    def __init__(self, project_root):
        self.path = Path(project_root) / "dead_letter.json"
        self.queue = self.load()
    
    def add(self, task, error, attempts):
        self.queue.append({
            "task": task,
            "error": error,
            "attempts": attempts,
            "added_at": datetime.now().isoformat(),
            "status": "pending_review",
        })
        self.save()
        wechat_send(f"⚠️ Dead-Letter: {task['name']} (3 failed)")
    
    def review(self, task_id, decision):
        """人工决策"""
        # approve: 接受当前不完美结果
        # retry: 重试 with 不同参数
        # skip: 跳过此任务
        # escalate: 升级到何大人
        ...
```

### 11.2 关键原则

- **不删除失败任务**（保留 trace）
- **不静默重试**（3 次就升级）
- **不阻塞主流程**（dead-letter 不影响其他任务）
- **可分析模式**（3 个同类失败 → 提取 pattern → 更新 method library）

---

## 十二、V&V Layer（Verification & Validation）

### 12.1 来自 arxiv 2508.17343

> "AI goes far beyond instructions given by a prompt"
> "Deciphering and clarification of developer intent" is the key difficulty
> "AI-based V&V of AI-generated code" is emerging

### 12.2 V&V 层次

```
V&V Layer (v3.1 新增，独立于 Adversarial Evaluator)
├─ L1: 编译检查（syntax / type）
├─ L2: 单元测试（pytest）
├─ L3: 集成测试（API / DB）
├─ L4: 端到端测试（Playwright）
├─ L5: 性能测试（locust）
├─ L6: 安全扫描（bandit / semgrep）
├─ L7: 验收测试（vs spec.md acceptance criteria）
└─ L8: 用户场景测试（"作为 X，我想要 Y" → 实际跑）
```

### 12.3 验收测试（关键，来自用户原话"完全符合需求"）

```python
def acceptance_test(spec, product):
    """验证产品是否完全符合需求"""
    
    # 从 spec.md 提取 acceptance criteria
    criteria = parse_acceptance(spec)  # list of testable conditions
    
    results = []
    for c in criteria:
        # 自动生成测试
        test = generate_test(c)
        # 跑测试
        passed = run_test(test)
        results.append({
            "criterion": c.text,
            "passed": passed,
            "evidence": test.output,
        })
    
    # 输出验收报告
    return {
        "total": len(results),
        "passed": sum(1 for r in results if r["passed"]),
        "failed": [r for r in results if not r["passed"]],
        "ready_for_delivery": all(r["passed"] for r in results),
    }
```

---

## 十三、完整端到端流程（v3.1 终极版）

### 13.1 9 阶段流程（基于 8 阶段 + V&V）

```
L0  需求扔入（1 行 / 1 链接 / 1 段语音）
     ↓
L1  接入 (Access) — Initializer Agent 5min
     ├─ NLU 解析需求
     ├─ 写 spec.md（acceptance criteria）
     └─ HG-1 通知何大人
     ↓
L2  探索 (Explore) — 30min
     ├─ Explore Agent: 调研 / 竞品 / 可行性
     └─ 输出 explore.md
     ↓
L3  提案 (Propose) — 30min
     ├─ Propose Agent: 3 套方案
     ├─ MCTS 选最优
     └─ 输出 propose.md
     ↓
L4  任务 (Task) — 30min
     ├─ HTN Planner: 拆 Sprint Contracts
     └─ 输出 tasks.json + sprint-contracts/*.yaml
     ↓
L5  应用 (Apply) — 10+ 小时（多 session）
     ├─ Ralph Loop (sub-35min per session)
     ├─ 每个 session = Planner/Generator/Evaluator
     ├─ Self-Heal (5-mode self-correction)
     └─ Codebase KG 持续更新
     ↓
L6  验证 (Verify) — 1-2 小时
     ├─ V&V 8 层（编译/单测/集成/E2E/性能/安全/验收/场景）
     └─ 输出 verify.md
     ↓
L7  评审 (Review) — 30min
     ├─ Adversarial Evaluation
     └─ HG-2/3 通知
     ↓
L8  归档 (Archive) — 30min
     ├─ Skill Extractor: 自动生成可复用 skill
     ├─ Reflexion Memory: 写反思
     ├─ OKF metadata 完整化
     └─ Dead-Letter Queue 处理
     ↓
L9  交付
```

### 13.2 单 session 内部（sub-35min）

```
Session Start (Fresh Context)
  ↓
读 spec.md / handoff / progress
  ↓
Anti-Anxiety Prompt: "信任之前的决策"
  ↓
Codebase KG query
  ↓
Plan (ReAct)
  ↓
Execute (Generator)
  ↓
Tool-based Verify (编译/测试)
  ↓
Adversarial Evaluate (独立 prompt)
  ↓
MCTS（critical decisions）
  ↓
Reflexion Reflect
  ↓
Write Handoff
  ↓
Git Commit
  ↓
Session End (≤ 30min)
```

---

## 十四、所需工具与能力清单（v3.1）

### 14.1 已有 ✓

- OpenClaw sessions_spawn / sessions_yield
- OpenClaw cron
- OpenClaw message
- context-recovery skill
- 67 个现有 skills
- akshare / web_search / message 等工具

### 14.2 需要新建

| 工具 | 用途 | 工作量 |
|---|---|---|
| `self-driving-rd-v3.1` Skill | 升级 SKILL.md | 0.5 天 |
| `ralph_engine.py` | Ralph Loop 引擎 | 1 天 |
| `htn_planner.py` | HTN 任务分解 | 1 天 |
| `codebase_kg.py` | 轻量知识图谱 | 1 天 |
| `vnv_layer.py` | 8 层 V&V | 1.5 天 |
| `reflexion_memory.py` | 反思存储 | 0.5 天 |
| `dead_letter.py` | 失败队列 | 0.5 天 |
| `acceptance_test.py` | 验收测试生成器 | 1 天 |
| `mcts_decide.py` | 关键决策 | 0.5 天 |
| `5_layer_runtime.py` | 生产级 runtime | 1 天 |
| **合计** | | **~8.5 天** |

### 14.3 验证

- [ ] Ralph Loop 能 sub-35min 持续跑
- [ ] HTN Planner 减少 75% LLM 调用
- [ ] Codebase KG 减少 50% "不知道有什么" 问题
- [ ] 5-Layer Runtime 任何层失败可恢复
- [ ] Reflexion Memory 跨 session 有效
- [ ] V&V 8 层全过 = 交付
- [ ] Dead-Letter Queue 不阻塞
- [ ] MCTS 选出的架构 > 随机

---

## 十五、立即落地的最小可行方案

### 15.1 第 1 周（先做基础）

| Day | 工作 | 产出 |
|---|---|---|
| 1 | 写 `ralph_engine.py` | 1-line bash + 简单 Python 包装 |
| 2 | 写 `reflexion_memory.py` | 失败 → 反思 → 写文件 |
| 3 | 写 `codebase_kg.py` | 扫描 + JSON 索引 |
| 4 | 写 `dead_letter.py` | 失败任务队列 |
| 5 | 改造 `orchestrator.py` v3.0 → v3.1 | sub-35min 强制 |

### 15.2 第 2 周（再上深度）

| Day | 工作 | 产出 |
|---|---|---|
| 6-7 | 写 `htn_planner.py` | LLM-生成启发式 |
| 8-9 | 写 `vnv_layer.py` | 8 层 V&V |
| 10 | 写 `mcts_decide.py` + `acceptance_test.py` | 决策 + 验收 |

### 15.3 第 3 周（端到端验证）

| Day | 工作 | 产出 |
|---|---|---|
| 11-12 | 跑 v3.0 → v3.1 升级（meta）| AI 升级自己 |
| 13-14 | 跑完整端到端（小项目）| 验证全流程 |
| 15 | 写 v3.1 总结 + 知识沉淀 | LESSONS.md |

---

## 十六、关键引用

### 16.1 2026 联网搜索（深度版）

- **Devin / Cognition** (Cognition Labs)
  - DeepWiki: continuously-updated knowledge graph
  - **Kevin 32B**: open-source 8B model, 91% on CUDA kernel gen
  - Multi-turn RL for narrow domains
- **Zylos Research** (2026-01)
  - **35-minute degradation** (KEY)
  - Task duration doubling every 7 months
  - 2026: 2h tasks, 2028: 40h weeks, 2029: 167h months
- **Huntley Ralph Loop** (2025-05, 持续到 2026)
  - "Ralph is a bash loop"
  - Fresh context + filesystem memory
- **arxiv 2605.07707 (NeurIPS 2026)**
  - **HTN Planning with LLM-Generated Heuristics**
  - Reduces LLM queries by 75%
- **GPT-HTN-Planner** (GitHub)
  - LLM + HTN 实战项目
- **Orkes Beyond Sandboxes** (2026-06-12)
  - **5-Layer Durable Runtime** for production
- **Brightlume AI** (2026)
  - Long-Running AI Agents patterns
  - **Dead-Letter Queue**
- **Anthropic Long-Running Claude**
  - CLAUDE.md as living plan
  - CHANGELOG.md as lab notes
  - **Ralph loop** integration
- **O'Reilly Long-Running Agents**
  - Comprehensive 2026 review
  - Cursor Composer 2 + cloud agents
  - Google Gemini Enterprise Agent Platform (SLAs)
- **arxiv 2508.17343** (SE community)
  - "**Deciphering developer intent**" is key
  - **AI-based V&V** emerging
- **Leonardo Gonzalez: Frontier Code Intelligence**
  - Public DeepWiki
  - Codemaps vs DeepWiki
- **Micheal Lanham**: Self-Correcting Agents
  - 5 Architecture Patterns
  - Real correction vs expensive retry
- **Decoding AI: Ralph Loops**
  - 1 writer + 1 reviewer loop
  - Skill auto-update from signals
- **Wopee.io AI Testing Agents 2026**
  - Self-healing of broken selectors
  - Visual regression smart filtering
- **QA Wolf: 3-Agent Architecture**
  - Mapping agent
  - Generation agent
  - Maintenance agent

### 16.2 历史引用

- v1.0 / v2.0 / v2.1 / v3.0
- 13 篇 vault 公众号文章
- YX AI Delivery Harness dashboard

---

## 十七、致何大人的判断（v3.1 视角）

### 17.1 关键洞察

1. **35-min 是硬限制**（不是建议）— 超过就降级
2. **Ralph Loop 是 1 行 bash** — 简单但有效
3. **HTN 减少 75% LLM 调用** — 成本友好
4. **Codebase KG 是必要** — 没它 agent "不知道有什么"
5. **5-Layer Runtime 是生产级** — 不是 demo 级
6. **V&V 8 层是"完全符合需求"的保证** — 验收测试层
7. **Reflexion + Dead-Letter** — 失败可学

### 17.2 v3.1 相比之前的本质变化

| 维度 | v3.0 | **v3.1** |
|---|---|---|
| Session 时长 | 无限制 | **sub-35min 强制** |
| 主循环 | 单 loop | **Ralph Loop**（fresh context）|
| 任务分解 | 简单列表 | **HTN Planning** |
| 代码理解 | 无 | **Codebase KG** |
| 生产级 | 单进程 | **5-Layer Runtime** |
| 验证深度 | 编译+测试 | **V&V 8 层** |
| 失败处理 | Self-Heal | **Reflexion + Dead-Letter** |
| 决策方式 | Tournament | **MCTS** |

### 17.3 给用户的回应

**Q: 给需求后 AI 怎么完全自驱动？**
A: 9 阶段流水线 + 30+ sub-35min session + Ralph Loop + 5-Layer Runtime + V&V 8 层 + 验收测试

**Q: 怎么保证"完全符合需求"？**
A: V&V Layer L7 = 验收测试，对照 spec.md 每条 acceptance criteria

**Q: 怎么"自己跑很久"？**
A: Ralph Loop 持续跑，sub-35min session 自动交接，5-Layer Runtime 抗 crash

**Q: 怎么"减少人工参与"？**
A: 3 Hard Gate（启动 SPEC 确认 / 中期 / 最终），中间全部 AI 自动

---

## 十八、v3.1 后的演进

### 18.1 v3.5：自优化

- 每完成项目自动总结 → 提取 skill
- Skill Library 跨项目共享
- 失败 patterns 自动更新 method library

### 18.2 v4.0：多项目并行

- 多项目同时跑
- 资源调度器
- 跨项目知识共享

### 18.3 v5.0：完全自治

- HG-1 也自动化（基于历史偏好学习）
- 何大人只看最终交付

---

> **一句话总结 v3.1**：
> v3.0 基础上加入 **sub-35min session 规则 + Ralph Loop + HTN Planning + Codebase KG + 5-Layer Runtime + V&V 8 层 + Reflexion + Dead-Letter + MCTS**。每个能力都有 2026 最新研究背书。8.5 天可落地。
