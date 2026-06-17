---
title: "Self-Driving R&D v3.3 — Loop Engineering 自主改进闭环"
author: "OpenClaw 小助"
publish_date: "2026-06-17"
saved_date: "2026-06-17"
type: research-report
okf_metadata:
  schema: okf-v0.1-inspired
  version: 3.3
  supersedes: 2026-06-17 Self-Driving R&D v3.2
  evolution: v3.2 (Ralph Loop 基础上) → v3.3 (Loop Engineering 自主改进)
  key_insight: "真正的循环 = 自主改进闭环，不只是循环跑"
status: implementable
---

# Self-Driving R&D v3.3 — Loop Engineering 自主改进闭环

> **关键洞察**（来自 Loop Engineering 图片）：
> ❌ "Loop Engineering" ≠ Ralph Loop（"while true" 循环跑）
> ✅ **真正的 Loop = 自主改进闭环**（每次循环后**系统变聪明**）
> 核心："**不是简单定时任务，而是基于状态自主唤醒**"

---

## 一、v3.2 → v3.3 关键升级

| 维度 | v3.2（Ralph Loop）| **v3.3（Loop Engineering）** |
|---|---|---|
| 触发 | Cron 定时 | **状态驱动**（event-driven）|
| 单次循环 | 执行 + 验证 | **执行 + 度量 + 决策 + 学习** |
| 自改进 | ❌ 无 | **✅ 每次迭代后系统变聪明** |
| 长期效果 | 一直重复同样水平 | **越跑越强**（compound learning）|

**v3.2 的 Ralph Loop 是"循环跑"，v3.3 是"跑 + 学 + 改进"**。

---

## 二、Loop Engineering 4 阶段（v3.3 核心）

```
           ┌───── Goal (Target) ─────┐
           │                          │
           ↓                          │
     ┌── Action (Execution) ──┐         │
     │                         │         │
     │  生成代码                │         │
     │  跑测试                  │         │
     │  写文档                  │         │
     │                         │         │
     └────────────┬────────────┘         │
                  │                       │
                  ↓                       │
           ┌── Metrics (Measure) ──┐     │
           │                          │     │
           │  V&V 8 层              │     │
           │  Sub-step 进度         │     │
           │  Token/时间/成功率     │     │
           │  9 Critical Patterns    │     │
           │                         │     │
           └────────────┬────────────┘     │
                        │                  │
                        ↓                  │
           ┌── Decision (Strategy) ─┐    │
           │                          │    │
           │  Adversarial Eval       │    │
           │  MCTS（critical）       │    │
           │  Self-Correction 5 模式 │    │
           │  Reflexion Memory       │    │
           │                         │    │
           └────────────┬────────────┘    │
                        │                  │
                        ↓                  │
                  ↑─── 改进 ───┘
                  ↑
              学到了什么？
           写 reflexion.md / 更新 skill
           改 prompt / 更新 method library
```

### 2.1 Goal（目标）

**不是固定任务，是动态调整的目标**：
- 初始 Goal = spec.md acceptance criteria
- 每次循环后 Goal 可以细化（如 "实现 feature-a" 拆为 "实现 feature-a 登录 + 实现 feature-a 验证"）
- Goal 也可能**修正**（"原来想做 X，发现 Y 更合理"）

```python
class Goal:
    """动态目标"""
    def __init__(self, spec_path):
        self.original = parse_spec(spec_path)  # 原始目标
        self.current = self.original  # 当前目标
        self.history = []  # 目标变化历史
    
    def refine(self, sub_goal):
        """细化目标"""
        self.history.append(self.current)
        self.current = self.current + sub_goal
        return self.current
    
    def pivot(self, new_goal, reason):
        """重大调整"""
        self.history.append({"old": self.current, "new": new_goal, "reason": reason})
        self.current = new_goal
```

### 2.2 Action（行动）

**4 类行动**（不是单一执行）：
1. **执行**（生成代码、跑测试、写文档）
2. **修复**（Self-Correction 5 模式）
3. **探索**（Codebase KG query、Reflexion 搜索）
4. **决策**（MCTS 选架构、Adversarial 评估）

```python
class Action:
    TYPES = ["execute", "fix", "explore", "decide"]
    
    def execute(self, plan):
        return GeneratorAgent.run(plan)
    
    def fix(self, error, attempt=1):
        for mode in ["tool", "external", "iterative", "tree", "dead_letter"]:
            if self.try_fix(error, mode, attempt):
                return "OK"
        return "FAILED"
    
    def explore(self, query):
        return CodebaseKG.query(query)
    
    def decide(self, options, evaluator):
        return MCTSDecider(options, evaluator).decide()
```

### 2.3 Metrics（度量）— v3.3 重点新增

**不是单一"pass/fail"，是 7 维度量**：

```python
class MetricsCollector:
    """7 维度量采集"""
    
    def collect(self, project):
        return {
            # 1. 完成度
            "completion": self._calc_completion(project),  # 0-1
            
            # 2. 质量
            "quality": {
                "lint_score": self._lint_check(project),  # 0-100
                "test_coverage": self._coverage(project),  # 0-1
                "complexity_avg": self._avg_complexity(project),  # 越低越好
                "tech_debt_hours": self._tech_debt(project),  # 估算
            },
            
            # 3. 性能
            "performance": {
                "session_time_avg": self._avg_session_time(project),  # 分钟
                "tokens_per_task": self._avg_tokens(project),
                "cost_per_task": self._avg_cost(project),
            },
            
            # 4. 成功率
            "success_rate": {
                "tasks_completed": self._completed_count(project),
                "tasks_failed": self._failed_count(project),
                "self_heal_success": self._heal_success_rate(project),
            },
            
            # 5. 9 Critical Patterns 检测
            "failure_patterns": self._detect_patterns(project),
            
            # 6. Learning（关键）
            "learning": {
                "reflexion_count": self._reflexion_count(project),
                "skill_extracted": self._skill_count(project),
                "method_updated": self._method_count(project),
                "prompt_evolved": self._prompt_version(project),
            },
            
            # 7. 资源
            "resources": {
                "total_cost": self._total_cost(project),
                "remaining_budget": self._remaining(project),
                "time_elapsed": self._elapsed(project),
            },
        }
```

### 2.4 Decision（决策）

**3 层决策**：
1. **战术层**：下一步做什么（Planner Agent）
2. **战略层**：什么时候升级 Hard Gate（Decision Agent）
3. **进化层**：prompt / method / skill 怎么改（Self-Improvement Engine）

```python
class DecisionEngine:
    """3 层决策"""
    
    def decide_tactical(self, state):
        """战术：下一步行动"""
        return PlannerAgent.next_action(state)
    
    def decide_strategic(self, metrics):
        """战略：是否升级"""
        if metrics["quality"]["test_coverage"] < 0.5:
            return "STOP_AND_UPGRADE"
        if metrics["completion"] > 0.9 and metrics["success_rate"]["self_heal_success"] > 0.7:
            return "NEARLY_DONE"
        return "CONTINUE"
    
    def decide_evolutionary(self, history):
        """进化：系统怎么改"""
        # 这是 v3.3 核心新增
        return SelfImprovementEngine.evolve(history)
```

---

## 三、Self-Improvement Engine（v3.3 核心新增）

**3 类自改进**：
1. **Skill Library 自增**（成功经验 → 可复用 skill）
2. **Method Library 自更新**（失败模式 → method 改进）
3. **Prompt Evolution**（每次跑自动改 Planner/Generator prompt）

### 3.1 Skill Library 自动提取

```python
# skill_extractor_v33.py
"""
每次循环成功后，提取可复用 skill
"""
import re
from pathlib import Path
import json
import subprocess

class SkillExtractorV33:
    def __init__(self, project_root):
        self.project = Path(project_root)
        self.skill_lib = Path("/root/.openclaw/workspace/skills")
    
    def run_after_session(self, session_id):
        """每次 session 结束调用"""
        handoff = self.project / f"handoff/session-{session_id:03d}.md"
        if not handoff.exists():
            return
        
        # 1. 判断这次 session 成功了吗
        if not self._is_success(handoff):
            self._record_failure(handoff)
            return
        
        # 2. 提取 pattern
        pattern = self._extract_pattern(handoff)
        if not pattern:
            return
        
        # 3. 检查是否已存在
        existing = self._find_similar_skill(pattern)
        if existing:
            self._update_existing(existing, pattern)
        else:
            self._create_new_skill(pattern)
    
    def _is_success(self, handoff):
        """判断 session 是否成功（V&V 通过）"""
        text = handoff.read_text()
        return "全部通过" in text or "all_pass" in text
    
    def _extract_pattern(self, handoff):
        """提取成功 pattern"""
        text = handoff.read_text()
        # 提取关键决策 + 关键代码模式
        decisions = re.findall(r"决策[:：]\s*(.+?)(?:\n|$)", text)
        if not decisions:
            return None
        return {
            "decisions": decisions,
            "summary": text[:500],
            "files_changed": self._git_diff_files(),
        }
    
    def _find_similar_skill(self, pattern):
        """找已有相似 skill（用 embedding 或关键词）"""
        # 简化：基于关键词
        keywords = self._extract_keywords(pattern)
        for skill_dir in self.skill_lib.iterdir():
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                content = skill_md.read_text()
                if any(kw in content for kw in keywords):
                    return skill_dir
        return None
    
    def _create_new_skill(self, pattern):
        """创建新 skill"""
        # 自动命名
        name = self._suggest_name(pattern)
        skill_dir = self.skill_lib / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成 SKILL.md
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(f"""---
name: {name}
description: "Auto-extracted from {self.project.name} session"
---

# {name}

Auto-extracted from successful session.

## Pattern
{chr(10).join(pattern['decisions'])}

## When to use
- Similar context
- Similar decision pattern
""")
        # 记录
        log(f"✨ New skill extracted: {name}")
    
    def _update_existing(self, skill_dir, pattern):
        """更新已有 skill（加新例）"""
        skill_md = skill_dir / "SKILL.md"
        content = skill_md.read_text()
        content += f"\n\n## New example\n{pattern['summary']}\n"
        skill_md.write_text(content)
```

### 3.2 Method Library 自更新

```python
# method_library.py
"""
失败模式 → method 库更新
"""
class MethodLibrary:
    """失败 method 集合"""
    
    def __init__(self):
        self.path = Path("/root/.openclaw/workspace/skills/methods.json")
        self.methods = self._load()
    
    def record_failure(self, task, error, method_used):
        """记录失败"""
        # 找最相似的 method
        closest = self._find_closest_method(method_used)
        
        if not closest:
            # 新 method
            self._add_method(method_used, failures=1)
        else:
            # 更新失败率
            closest["failures"] = closest.get("failures", 0) + 1
            closest["last_error"] = str(error)
            self._save()
    
    def record_success(self, method_used):
        """记录成功"""
        closest = self._find_closest_method(method_used)
        if closest:
            closest["successes"] = closest.get("successes", 0) + 1
            self._save()
    
    def rank_methods(self, context):
        """给当前 context 排名 methods"""
        candidates = self._find_candidates(context)
        # 按成功率排序
        for c in candidates:
            total = c.get("successes", 0) + c.get("failures", 0)
            if total > 0:
                c["success_rate"] = c.get("successes", 0) / total
            else:
                c["success_rate"] = 0.5  # 默认
        return sorted(candidates, key=lambda c: -c["success_rate"])
    
    def evolve_method(self, method, new_strategy):
        """method 进化（基于成功 pattern）"""
        method["strategy"] = new_strategy
        method["evolved_at"] = datetime.now().isoformat()
        self._save()
```

### 3.3 Prompt Evolution（最核心）

```python
# prompt_evolution.py
"""
Planner/Generator/Evaluator 的 prompt 随时间进化
"""
import json
import re
from pathlib import Path
from datetime import datetime

class PromptEvolution:
    """v3.3 核心：系统自己改自己的 prompt"""
    
    def __init__(self, prompts_dir):
        self.dir = Path(prompts_dir)
        self.prompts = self._load_all()
    
    def evolve_after_session(self, agent_name, success, feedback):
        """每次 session 结束后，evolve prompt"""
        if not success:
            return  # 只在成功时 evolve
        
        prompt = self.prompts[agent_name]
        current_version = prompt["version"]
        
        # 1. 提取哪些 instruction 起了作用
        effective_instructions = self._analyze_what_worked(feedback)
        
        # 2. 强化这些 instruction
        new_prompt_text = self._strengthen(prompt["text"], effective_instructions)
        
        # 3. 加新的 heuristic
        new_heuristic = self._extract_heuristic(feedback)
        if new_heuristic:
            new_prompt_text = self._add_heuristic(new_prompt_text, new_heuristic)
        
        # 4. 写新版本
        new_version = current_version + 1
        new_path = self.dir / f"{agent_name}.v{new_version}.md"
        new_path.write_text(new_prompt_text)
        
        # 5. 更新 index
        self.prompts[agent_name] = {
            "current": new_path,
            "version": new_version,
            "text": new_prompt_text,
            "evolved_at": datetime.now().isoformat(),
        }
        self._save_index()
    
    def _analyze_what_worked(self, feedback):
        """从 feedback 找出有效的 instruction"""
        # 简单实现：找所有被引用的 instruction
        return re.findall(r"## (.+?)\n", feedback)
    
    def _extract_heuristic(self, feedback):
        """提取新启发"""
        # 找 reflection 中的 "I learned that..." 模式
        match = re.search(r"I learned that (.+?)(?:\.|$)", feedback)
        return match.group(1) if match else None
    
    def _strengthen(self, prompt, instructions):
        """强化 prompt"""
        # 简单：把 instructions 加到 prompt 顶部
        addition = f"\n## Proven Instructions (learned from {len(instructions)} sessions)\n"
        for inst in instructions:
            addition += f"- {inst}\n"
        return addition + "\n" + prompt
    
    def _add_heuristic(self, prompt, heuristic):
        """加新启发"""
        return prompt + f"\n\n## New Heuristic\n- {heuristic}\n"
```

### 3.4 Self-Improvement 主循环

```python
# self_improvement_engine.py
"""
每次 session 结束 → 跑 Self-Improvement Engine
"""
class SelfImprovementEngine:
    def __init__(self, project_root):
        self.project = Path(project_root)
        self.skill_extractor = SkillExtractorV33(project_root)
        self.method_lib = MethodLibrary()
        self.prompt_evo = PromptEvolution("/root/.openclaw/workspace/prompts")
    
    def run_after_session(self, session_id, success, feedback):
        """每次 session 后跑"""
        # 1. 提取 skill
        self.skill_extractor.run_after_session(session_id)
        
        # 2. 更新 method library
        if success:
            self.method_lib.record_success(method_used=feedback.get("method"))
        else:
            self.method_lib.record_failure(
                task=feedback.get("task"),
                error=feedback.get("error"),
                method_used=feedback.get("method"),
            )
        
        # 3. Evolve prompts
        for agent_name in ["planner", "generator", "evaluator"]:
            self.prompt_evo.evolve_after_session(agent_name, success, feedback)
        
        # 4. 写自改进日志
        self._log_evolution(session_id, success, feedback)
    
    def _log_evolution(self, session_id, success, feedback):
        log_path = self.project / "self_evolution.log"
        with log_path.open("a") as f:
            f.write(f"\n[{datetime.now()}] session-{session_id}: success={success}\n")
            f.write(f"  decisions: {feedback.get('decisions', [])}\n")
            f.write(f"  next_improvement: {feedback.get('next', '')}\n")
```

---

## 四、State-Driven Scheduler（v3.3 核心新增）

**不是定时跑，是基于状态触发**：

```python
# state_scheduler.py
"""
状态驱动的调度器（不是 cron）
"""
import time
from enum import Enum

class State(Enum):
    IDLE = "idle"
    INITIALIZING = "initializing"
    RUNNING = "running"
    BLOCKED = "blocked"  # 需人介入
    PAUSED = "paused"
    COMPLETE = "complete"
    IMPROVING = "improving"  # 自改进中

class StateDrivenScheduler:
    """基于状态触发，不是定时"""
    
    def __init__(self, project):
        self.project = project
        self.state = State.IDLE
        self.last_state_change = time.time()
        self.state_history = []
    
    def observe(self):
        """观察状态（不是定时）"""
        new_state = self._detect_state()
        if new_state != self.state:
            self._transition(new_state)
    
    def _detect_state(self):
        """检测当前应该是什么状态"""
        if self._is_complete():
            return State.COMPLETE
        if self._is_blocked():
            return State.BLOCKED
        if self._has_pending_work():
            return State.RUNNING
        if self._is_improving():
            return State.IMPROVING
        return State.IDLE
    
    def _transition(self, new_state):
        """状态转换"""
        old = self.state
        self.state = new_state
        self.last_state_change = time.time()
        self.state_history.append({
            "from": old,
            "to": new_state,
            "ts": self.last_state_change,
        })
        
        # 触发对应动作
        if new_state == State.RUNNING:
            self._spawn_session()
        elif new_state == State.BLOCKED:
            self._notify_human()
        elif new_state == State.COMPLETE:
            self._notify_delivery()
        elif new_state == State.IMPROVING:
            self._run_improvement()
    
    def _is_complete(self):
        return all(t.get("status") == "done" for t in self._tasks())
    
    def _is_blocked(self):
        # 有 3+ 失败任务在 dead-letter
        dlq = self._dlq()
        return any(item["attempts"] >= 3 for item in dlq.get("queue", []))
    
    def _has_pending_work(self):
        return any(t.get("status") != "done" for t in self._tasks())
    
    def _is_improving(self):
        # 自改进有 pending
        return self._evolution_pending()
    
    def run(self):
        """主循环：持续观察状态"""
        while self.state != State.COMPLETE:
            self.observe()
            time.sleep(60)  # 每分钟观察一次
```

**vs Cron**：
- Cron: 每 5 min 跑一次（无论是否需要）
- State: 状态变化才触发（更省 token、更精准）

---

## 五、Multi-Dimensional Metrics Dashboard

```python
# metrics_dashboard.py
"""
7 维度量可视化（v3.3）
"""
import streamlit as st
import json
from pathlib import Path
from datetime import datetime

def render_metrics_dashboard(project_root):
    project = Path(project_root)
    st.title("📊 Loop Engineering 7 维度量")
    
    metrics = MetricsCollector().collect(project)
    
    # 1. 完成度
    st.metric("完成度", f"{metrics['completion']*100:.1f}%",
              delta=f"{(metrics['completion']-0.5)*100:.1f}%" if metrics['completion'] > 0.5 else None)
    
    # 2. 质量（4 子项）
    st.subheader("质量")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Lint", f"{metrics['quality']['lint_score']:.0f}/100")
    with col2:
        st.metric("测试覆盖率", f"{metrics['quality']['test_coverage']*100:.0f}%")
    with col3:
        st.metric("平均复杂度", f"{metrics['quality']['complexity_avg']:.1f}")
    with col4:
        st.metric("技术债", f"{metrics['quality']['tech_debt_hours']:.0f}h")
    
    # 3. 性能
    st.subheader("性能")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("平均 session 时间", f"{metrics['performance']['session_time_avg']:.1f}min")
    with col2:
        st.metric("平均 token/task", f"{metrics['performance']['tokens_per_task']:.0f}")
    with col3:
        st.metric("平均 cost/task", f"${metrics['performance']['cost_per_task']:.2f}")
    
    # 4. 成功率
    st.subheader("成功率")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tasks 完成", metrics['success_rate']['tasks_completed'])
    with col2:
        st.metric("Tasks 失败", metrics['success_rate']['tasks_failed'])
    with col3:
        st.metric("Self-Heal 成功率", f"{metrics['success_rate']['self_heal_success']*100:.0f}%")
    
    # 5. 9 Critical Patterns
    st.subheader("9 Critical Failure Patterns")
    for pattern, detected in metrics['failure_patterns'].items():
        icon = "🚨" if detected else "✅"
        st.text(f"{icon} {pattern}")
    
    # 6. 自改进（v3.3 核心）
    st.subheader("🧠 自改进进度")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Reflexion 数量", metrics['learning']['reflexion_count'])
    with col2:
        st.metric("Skill 提取", metrics['learning']['skill_extracted'])
    with col3:
        st.metric("Method 更新", metrics['learning']['method_updated'])
    with col4:
        st.metric("Prompt 版本", f"v{metrics['learning']['prompt_evolved']}")
    
    # 7. 资源
    st.subheader("资源")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("总成本", f"${metrics['resources']['total_cost']:.2f}")
    with col2:
        st.metric("剩余预算", f"${metrics['resources']['remaining_budget']:.2f}")
    with col3:
        st.metric("已运行", f"{metrics['resources']['time_elapsed']:.1f}h")
```

---

## 六、完整 Loop Engineering 实现

```python
# loop_engineering.py
"""
真正的 Loop Engineering 引擎
v3.3 核心
"""
import time
import json
from pathlib import Path
from datetime import datetime
from enum import Enum

class LoopState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    IMPROVING = "improving"
    COMPLETE = "complete"
    BLOCKED = "blocked"

class LoopEngineer:
    """Goal → Action → Metrics → Decision 4 阶段闭环"""
    
    def __init__(self, project_root):
        self.project = Path(project_root)
        self.state = LoopState.IDLE
        self.iteration = 0
        self.metrics_history = []
        self.skill_extractor = SkillExtractorV33(project_root)
        self.method_lib = MethodLibrary()
        self.prompt_evo = PromptEvolution("/root/.openclaw/workspace/prompts")
        self.scheduler = StateDrivenScheduler(project_root)
    
    def run(self):
        """主循环：自主改进闭环"""
        log(f"🔄 Loop Engineering start: {self.project}")
        
        while self.state != LoopState.COMPLETE:
            self.iteration += 1
            log(f"--- Iteration {self.iteration} ---")
            
            # 1. Goal：确定本轮目标
            goal = self._get_goal()
            log(f"Goal: {goal}")
            
            # 2. Action：执行
            action_result = self._take_action(goal)
            log(f"Action result: {action_result['status']}")
            
            # 3. Metrics：度量
            metrics = self._measure(action_result)
            self.metrics_history.append(metrics)
            log(f"Metrics: completion={metrics['completion']:.2f}, quality={metrics['quality']['test_coverage']:.2f}")
            
            # 4. Decision：决策
            decision = self._decide(metrics)
            log(f"Decision: {decision['action']}")
            
            # 5. Self-Improvement（v3.3 新增）
            self._improve(goal, action_result, metrics, decision)
            
            # 6. 更新 state
            self.state = self._update_state(decision)
            
            # 7. Sleep
            time.sleep(60)
        
        log(f"🎉 Loop complete after {self.iteration} iterations")
    
    def _get_goal(self):
        """从 spec.md + 当前状态找下一目标"""
        state = read_state(self.project)
        tasks = state["tasks"]["tasks"]
        pending = [t for t in tasks if t.get("status") != "done"]
        if not pending:
            return {"type": "complete", "description": "no more tasks"}
        return {"type": "task", "task": pending[0], "description": pending[0].get("name")}
    
    def _take_action(self, goal):
        """执行：4 类行动之一"""
        if goal["type"] == "complete":
            return {"status": "complete", "action": "none"}
        task = goal["task"]
        
        # 1. 执行
        if task.get("type") == "execute":
            return GeneratorAgent.run(task)
        # 2. 修复
        elif task.get("type") == "fix":
            return SelfHealAgent.run(task, max_attempts=3)
        # 3. 探索
        elif task.get("type") == "explore":
            return CodebaseKG.query(task["query"])
        # 4. 决策
        elif task.get("type") == "decide":
            return MCTSDecider.decide(task["options"])
        else:
            return {"status": "unknown_task_type", "action": "fail"}
    
    def _measure(self, action_result):
        """度量：7 维"""
        return MetricsCollector().collect(self.project)
    
    def _decide(self, metrics):
        """决策：3 层"""
        decision = {"action": "continue"}
        
        # 战略层
        if metrics["quality"]["test_coverage"] < 0.5:
            decision["action"] = "STOP_AND_UPGRADE"
            decision["reason"] = "low_coverage"
        elif metrics["completion"] > 0.9 and metrics["success_rate"]["self_heal_success"] > 0.7:
            decision["action"] = "FINALIZE"
            decision["reason"] = "near_complete"
        elif metrics["failure_patterns"].get("F10_self_eval_trap"):
            decision["action"] = "STOP_AND_UPGRADE"
            decision["reason"] = "self_eval_trap_detected"
        
        return decision
    
    def _improve(self, goal, action_result, metrics, decision):
        """自改进（v3.3 核心）"""
        # 1. Skill Library 自增
        if action_result.get("status") == "ok":
            self.skill_extractor.run_after_session(self.iteration)
        
        # 2. Method Library 更新
        if action_result.get("status") == "ok":
            self.method_lib.record_success(method_used=goal.get("method"))
        else:
            self.method_lib.record_failure(
                task=goal.get("task", {}),
                error=action_result.get("error"),
                method_used=goal.get("method"),
            )
        
        # 3. Prompt Evolution
        for agent_name in ["planner", "generator", "evaluator"]:
            self.prompt_evo.evolve_after_session(
                agent_name,
                success=action_result.get("status") == "ok",
                feedback=action_result,
            )
        
        # 4. 写自改进日志
        self._log_improvement(goal, action_result, metrics, decision)
    
    def _update_state(self, decision):
        if decision["action"] in ["FINALIZE"]:
            return LoopState.COMPLETE
        elif decision["action"] in ["STOP_AND_UPGRADE"]:
            return LoopState.BLOCKED
        else:
            return LoopState.RUNNING
    
    def _log_improvement(self, goal, action, metrics, decision):
        log_path = self.project / "self_evolution.log"
        with log_path.open("a") as f:
            f.write(f"\n[{datetime.now()}] iter-{self.iteration}\n")
            f.write(f"  Goal: {goal.get('description')}\n")
            f.write(f"  Action: {action.get('status')}\n")
            f.write(f"  Metrics: completion={metrics['completion']:.2f}\n")
            f.write(f"  Decision: {decision['action']}\n")
            f.write(f"  Improvement: prompt evolved, method updated\n")
```

---

## 七、v3.3 完整能力矩阵

| 能力 | v3.0 | v3.1 | v3.2 | **v3.3** |
|---|---|---|---|---|
| 基础 8 阶段 | ✅ | ✅ | ✅ | ✅ |
| 3 角色 | ✅ | ✅ | ✅ | ✅ |
| Sub-35min | ❌ | ✅ | ✅ | ✅ |
| Ralph Loop | ❌ | ✅ | ✅ | ⚠️ 升级为 GAMD |
| HTN | ❌ | ✅ | ✅ | ✅ |
| Codebase KG | ❌ | ✅ | ✅ | ✅ |
| 5-Layer Runtime | ❌ | ✅ | ✅ | ✅ |
| V&V 8 层 | ⚠️ | ✅ | ✅ | ✅ |
| **Goal-Action-Metrics-Decision 显性化** | ❌ | ❌ | ❌ | ✅ |
| **State-Driven Scheduler** | ❌ | ❌ | ❌ | ✅ |
| **7-Dimensional Metrics** | ❌ | ❌ | ⚠️ 基础 | ✅ |
| **Self-Improvement Engine** | ❌ | ❌ | ❌ | ✅ |
| **Skill Library 自增** | ❌ | ❌ | ⚠️ 计划 | ✅ |
| **Method Library 自更新** | ❌ | ❌ | ⚠️ 计划 | ✅ |
| **Prompt Evolution** | ❌ | ❌ | ❌ | ✅ |
| Claude Code 集成 | ❌ | ❌ | ✅ | ✅ |
| ReAct Agent | ❌ | ❌ | ✅ | ✅ |
| 环境健康度 | ❌ | ❌ | ✅ | ✅ |
| Sub-step 进度 | ❌ | ❌ | ✅ | ✅ |
| Lightweight UI | ❌ | ❌ | ✅ | ✅ |

---

## 八、给何大人的回答

**Q: Loop Engineering 跟 Ralph Loop 区别是？**
A: 
- **Ralph Loop**: `while true; do run; done`（重复跑）
- **Loop Engineering**: 每次循环后**系统学到了新东西**（跑 + 学 + 改进）

**Q: 为什么这个区别重要？**
A: 10+ 小时跑下来，Ralph Loop 一直同样水平；Loop Engineering 越跑越强。

**Q: 具体怎么"越跑越强"？**
A: 3 类自改进：
1. **Skill Library 自增**（成功经验 → 可复用 skill）
2. **Method Library 自更新**（失败模式 → method 改进）
3. **Prompt Evolution**（每次跑改 Planner/Generator 的 prompt）

**Q: v3.3 整体改进核心？**
A: v3.3 把"循环跑"升级为"循环 + 自改进"。

---

## 九、立即落地清单（v3.3）

| 周 | 工作 | 产出 |
|---|---|---|
| W1 | Ralph Loop + reflexion + kg + dlq | 基础 4 件 |
| W2 | htn_planner + vnv_layer | 深度 2 件 |
| W3 | mcts + acceptance + UI | 决策 + 验收 + UI |
| W4 | Claude Code + ReAct + 健康度 | v3.2 新 3 件 |
| W5 | **Self-Improvement Engine + State Scheduler** | **v3.3 新 2 件** |
| W6 | 端到端测试 | 跑通完整 |

**总工作量**：~12 天（v3.2 是 10 天，v3.3 加 2 天）

---

## 十、引用

- **图片**：`loop-engineering-closed-loop.jpg`（已存档）
- **@AI有点聊**：AI新范式：循环工程（2026）
- v3.0 / v3.1 / v3.2（已存在）
- 上一轮搜索的"Loop Engineering 2026"文章（Tosea AI）
- YX Harness 二次分析（v3.2 基础）

---

> **v3.3 核心转变**：从"循环跑"升级为"循环 + 自改进"。
> 12 天可落地。10+ 小时跑下来，系统**会真的变聪明**。
