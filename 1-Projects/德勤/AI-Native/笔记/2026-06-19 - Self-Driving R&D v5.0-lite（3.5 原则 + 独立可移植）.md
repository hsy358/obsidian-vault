---
title: Self-Driving R&D · v5.0-lite（3.5 原则 + 独立可移植）
description: 要不要我直接开始写 workflow.yaml + 核心 6 个 Python 文件的代码？
type: note
---
# Self-Driving R&D · v5.0-lite（3.5 原则 + 独立可移植）

> **定位**：v3.5 的实战原则 + v4.x 的独立可移植架构 = **最小可落地版本**
> **核心原则**：**有原则地砍，只留 7 个核心能力 + 8 条 v3.5 原则**
> **目标**：1 人 2 周可上线，单项目 < 5 分钟人工介入，token < 100k
> **更新日期**：2026-06-19

---

## 一、设计哲学

**v3.5 是实战过的精华**——8 条原则经过 OpenClaw 跑过，**但绑定 OpenClaw**。
**v4.x 是独立架构**——完全脱离 OpenClaw，**但 v4.2 太复杂**。

**v5.0-lite 的解法**：
> **取 v3.5 的 8 条原则 + v4.x 的"独立 + YAML + 状态机"骨架**
> **砍掉所有 v4.2 的复杂特性，只留能跑通 R&D 主流程的最小集**

---

## 二、v3.5 八大原则（全部保留 + 落地）

| # | v3.5 原则 | Lite 中的落地 |
|---|----------|--------------|
| 1 | **Spec is Sacred** | `spec.md` LOCKED 文件，禁止修改 |
| 2 | **Adversarial > Self-Eval** | generator (M3) ≠ evaluator (DeepSeek/M2.7)，硬编码不同 |
| 3 | **State-Driven > Cron** | 状态变化触发动作，无 cron |
| 4 | **Sub-35min Sessions** | 30 分钟硬超时，超时写 handoff |
| 5 | **State = Files** | SQLite + YAML，git 友好 |
| 6 | **Handoff Contains "Don't"** | 每次 handoff 必含 `do:[]` + `don't:[]` |
| 7 | **Self-Improve, Not Self-Replace** | 改 prompt / 改 skill，不改引擎代码 |
| 8 | **Hard Gate for Trust** | 关键决策（spec 确认 / 验收）必须人批 |

---

## 三、Lite 保留的 7 个核心能力

| # | 能力 | 必要性 |
|---|------|--------|
| 1 | **YAML workflow** | 简单 + git 友好 |
| 2 | **状态机（SQLite + YAML）** | 防状态乱 |
| 3 | **5 层裁决** | 质量底线（简化版）|
| 4 | **3 上下文模式** | 节省 token |
| 5 | **3 档错误恢复** | 防止跑飞 |
| 6 | **模型无关** | 不绑定 LLM |
| 7 | **审计日志** | 事后可追 |

**砍掉的（v4.2 14 个特性）**：
- ❌ Org Chart（单 agent 够）
- ❌ Goal Ancestry（单项目用不到）
- ❌ Heartbeat 队列（直接调用）
- ❌ Memento Man（session 不跨天）
- ❌ ACP / MCP（内部用）
- ❌ Plugin 架构（skill 直接 import）
- ❌ Template（YAML 复用即可）
- ❌ Action Schema（关键 2-3 个即可）
- ❌ hash-chain 审计（普通日志）
- ❌ OpenTelemetry（暂不需要）
- ❌ 多 session 隔离
- ❌ 并行执行（先串行）
- ❌ review_loop（单次）
- ❌ 前端（CLI 先跑通）

---

## 四、整体架构（极简）

```
┌────────────────────────────────────────────────────────┐
│  CLI / Web (可选)                                      │
│  - selfdriving run <project>                           │
│  - selfdriving status <project>                        │
│  - selfdriving gate <project> --approve/--reject       │
└────────────────────────────────────────────────────────┘
                         ↓
┌────────────────────────────────────────────────────────┐
│  Engine (Python ~1200 行)                              │
│                                                         │
│  ┌─ WorkflowRunner ────────────────────────────────┐  │
│  │  - 读 YAML workflow                              │  │
│  │  - 按 stage 顺序执行                              │  │
│  │  - 每个 stage 调一次 LLM                          │  │
│  └────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─ StateManager ──────────────────────────────────┐  │
│  │  - .comet.yaml (人类可读)                        │  │
│  │  - .state.db (SQLite，事务)                      │  │
│  │  - 状态机转换校验                                 │  │
│  └────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─ LLMInterface ──────────────────────────────────┐  │
│  │  - 适配 OpenAI / Anthropic / MiniMax / DeepSeek   │  │
│  │  - generator model ≠ evaluator model（v3.5 原则 2）│  │
│  │  - 3 上下文模式：accumulate / last_only / explicit │  │
│  └────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─ DecisionAgent ─────────────────────────────────┐  │
│  │  - 5 层裁决（简化版）                             │  │
│  │  - Hard Gate 触发人批                            │  │
│  └────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─ SelfCorrectEngine ─────────────────────────────┐  │
│  │  - 3 档：soft（自动）/ hard（自动升级）/ human   │  │
│  │  - Handoff 含 don't list（v3.5 原则 6）         │  │
│  └────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─ SkillExecutor ─────────────────────────────────┐  │
│  │  - 直接 Python import（不经过任何中间层）         │  │
│  │  - 5-10 个核心 skill 足够                        │  │
│  └────────────────────────────────────────────────┘  │
│                                                         │
│  Sub-35min Session Manager (v3.5 原则 4)               │
│  - 30 分钟硬超时                                       │
│  - 超时自动写 handoff，含 don't list                   │
└────────────────────────────────────────────────────────┘
                         ↓
┌────────────────────────────────────────────────────────┐
│  Storage (本地)                                         │
│  projects/<name>/                                       │
│  ├─ .comet.yaml      ← 状态 (YAML)                    │
│  ├─ .state.db        ← 状态 (SQLite)                  │
│  ├─ spec.md          ← 需求 (LOCKED)                  │
│  ├─ tasks.json       ← 任务                           │
│  ├─ artifacts/       ← 各 stage 产物                  │
│  └─ handoffs/        ← session 交接（含 don't list）  │
└────────────────────────────────────────────────────────┘
```

---

## 五、目录结构（极简）

```
selfdriving-lite/
├── README.md
├── pyproject.toml
├── config.yaml                 # 模型 + 通知配置
├── workflow.yaml               # 3 阶段 workflow（可扩 8）
├── selfdriving/
│   ├── __init__.py
│   ├── cli.py                  # CLI 入口（~100 行）
│   ├── engine.py               # WorkflowRunner（~250 行）
│   ├── state.py                # StateManager（~200 行）
│   ├── llm.py                  # LLMInterface（~150 行）
│   ├── decision.py             # DecisionAgent（~150 行）
│   ├── self_correct.py         # SelfCorrectEngine（~100 行）
│   ├── session.py              # Sub-35min session（~80 行）
│   └── handoff.py              # 含 don't list（~80 行）
├── skills/                     # 直接 import（不是注册表）
│   ├── web_search.py
│   ├── code_generator.py
│   ├── test_runner.py
│   ├── requirement_parser.py
│   └── README.md
├── projects/                   # 项目目录
│   └── example/
│       ├── .comet.yaml
│       ├── .state.db
│       ├── spec.md
│       ├── tasks.json
│       ├── artifacts/
│       └── handoffs/
└── tests/                      # 基础测试
    ├── test_engine.py
    ├── test_state.py
    └── test_decision.py
```

**核心代码量**：~1100 行（不含 skill）

---

## 六、Workflow YAML（3 阶段默认，可扩 8）

```yaml
# workflow.yaml
workflow:
  name: lite-default
  version: "1.0.0"
  
  # v3.5 原则 4: Sub-35min
  safety:
    max_session_minutes: 30
    max_project_hours: 8
  
  # 默认 3 阶段，可扩到 8（注释掉就是 8 阶段完整版）
  stages:
    # === 必跑的 3 阶段 ===
    access:
      agent: pm
      description: "把需求写成 spec"
      skills: [requirement_parser]
      timeout_minutes: 5
      hard_gate: true  # v3.5 原则 8
      
      on_success: apply
      on_failure: failed
    
    apply:
      agent: engineer
      description: "写代码 + 写测试"
      skills: [code_generator, test_runner]
      timeout_minutes: 20
      context_mode: last_only  # v3.5 + Conductor
      
      on_success: verify
      on_failure: failed
    
    verify:
      agent: qa
      description: "跑测试 + 人工确认"
      skills: [test_runner]
      timeout_minutes: 5
      hard_gate: true  # v3.5 原则 8
      
      on_success: $end
      on_failure: apply  # 不通过就回 apply 改
    
    failed:
      agent: pm
      description: "失败处理"
      on_success: access  # 可重启

    # === 可选扩展阶段（默认注释，按需打开）===
    # explore:
    #   agent: researcher
    #   description: "技术调研"
    #   skills: [web_search]
    #   timeout_minutes: 10
    #   on_success: propose
    #
    # propose:
    #   agent: architect
    #   description: "出方案"
    #   timeout_minutes: 10
    #   on_success: task
    #
    # task:
    #   agent: pm
    #   description: "拆任务"
    #   timeout_minutes: 5
    #   on_success: apply
    #
    # review:
    #   agent: qa
    #   description: "AI 自评"
    #   timeout_minutes: 5
    #   on_success: archive
    #
    # archive:
    #   agent: pm
    #   description: "归档 + 写 lessons"
    #   timeout_minutes: 5
    #   on_success: $end
```

---

## 七、配置（极简）

```yaml
# config.yaml
# v3.5 原则 2: Adversarial - generator 和 evaluator 必须不同 model

models:
  generator:
    provider: minimax
    model: MiniMax-M3
    api_key: ${MINIMAX_API_KEY}
  
  # 评审用不同 model（强制约束）
  evaluator:
    provider: deepseek
    model: DeepSeek-R1
    api_key: ${DEEPSEEK_API_KEY}
  
  # 可选：用于简单任务
  fast:
    provider: minimax
    model: MiniMax-M2.7
    api_key: ${MINIMAX_API_KEY}

# 项目路径
projects_root: ./projects

# 通知（可选）
notification:
  feishu:
    webhook: ${FEISHU_WEBHOOK}
    on_events: [hard_gate, failed, completed]

# 限流
concurrency:
  max_concurrent: 3
  token_budget_per_project: 200000
```

---

## 八、核心代码（极简示例）

### 8.1 LLMInterface（v3.5 原则 2 落地）

```python
# selfdriving/llm.py
from openai import OpenAI
import os

class LLMInterface:
    """模型无关，generator 和 evaluator 用不同 model（v3.5 原则 2）"""
    
    def __init__(self, config: dict):
        self.clients = {}
        for name, cfg in config["models"].items():
            # 用 OpenAI 兼容协议（Anthropic / MiniMax / DeepSeek 都支持）
            base_url = self._base_url(cfg["provider"])
            self.clients[name] = OpenAI(
                base_url=base_url,
                api_key=os.environ[cfg["api_key"].strip("${}")]
            )
        # v3.5 原则 2: 强制 generator ≠ evaluator
        assert config["models"]["generator"]["model"] != config["models"]["evaluator"]["model"], \
            "v3.5 原则 2: generator and evaluator must use different models"
    
    def _base_url(self, provider):
        urls = {
            "openai": "https://api.openai.com/v1",
            "anthropic": "https://api.anthropic.com/v1",
            "minimax": "https://api.minimaxi.com/anthropic",
            "deepseek": "https://api.deepseek.com/v1",
        }
        return urls[provider]
    
    def chat(self, role: str, messages: list, **kwargs) -> str:
        """role: generator / evaluator / fast"""
        cfg = self.config["models"][role]
        client = self.clients[role]
        r = client.chat.completions.create(
            model=cfg["model"],
            messages=messages,
            **kwargs
        )
        return r.choices[0].message.content
```

### 8.2 StateManager（v3.5 原则 5 落地）

```python
# selfdriving/state.py
import sqlite3
import yaml
from pathlib import Path

class StateManager:
    """v3.5 原则 5: State = Files（SQLite + YAML 双层）"""
    
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.yaml_path = project_dir / ".comet.yaml"
        self.db_path = project_dir / ".state.db"
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS state_transitions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_stage TEXT, to_stage TEXT,
                    actor TEXT, reason TEXT,
                    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS stage_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stage TEXT, status TEXT, score INTEGER,
                    started_at TIMESTAMP, ended_at TIMESTAMP,
                    error TEXT, retry_count INTEGER DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS handoffs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT, stage TEXT,
                    do_list TEXT, dont_list TEXT,  -- v3.5 原则 6
                    context TEXT,
                    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
    
    def get_state(self) -> dict:
        return yaml.safe_load(self.yaml_path.read_text())
    
    def transition(self, from_stage: str, to_stage: str, actor: str, reason: str):
        """带状态机校验的转换"""
        # 校验合法转换（v3.5 状态机）
        if not self._is_valid_transition(from_stage, to_stage):
            raise ValueError(f"Invalid transition: {from_stage} -> {to_stage}")
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO state_transitions (from_stage, to_stage, actor, reason) VALUES (?,?,?,?)",
                (from_stage, to_stage, actor, reason)
            )
        
        # 同步到 YAML
        state = self.get_state()
        state["current_stage"] = to_stage
        state["previous_stage"] = from_stage
        self.yaml_path.write_text(yaml.safe_dump(state, allow_unicode=True))
    
    def _is_valid_transition(self, from_stage: str, to_stage: str) -> bool:
        """简单状态机（可跳转版本）"""
        VALID = {
            "access":  ["apply", "failed", "$end"],
            "apply":   ["verify", "apply", "failed"],  # verify 不通过可回 apply
            "verify":  ["$end", "apply", "failed"],
            "failed":  ["access", "$end"],
            "$end":    [],
        }
        return to_stage in VALID.get(from_stage, [])
```

### 8.3 WorkflowRunner（核心 250 行）

```python
# selfdriving/engine.py
import yaml
from pathlib import Path
from datetime import datetime, timedelta
import time

class WorkflowRunner:
    """v3.5 原则 4: Sub-35min sessions"""
    
    def __init__(self, project_dir: Path, llm, state, decision, self_correct, handoff_mgr):
        self.project_dir = project_dir
        self.llm = llm
        self.state = state
        self.decision = decision
        self.self_correct = self_correct
        self.handoff_mgr = handoff_mgr
        self.workflow = yaml.safe_load(Path("workflow.yaml").read_text())
        self.session_start = None
    
    def run(self, stage: str = None):
        """主循环"""
        stage = stage or self.state.get_state()["current_stage"]
        
        while stage != "$end":
            stage_cfg = self.workflow["stages"][stage]
            
            # v3.5 原则 4: Sub-35min
            self.session_start = datetime.now()
            
            try:
                # 1. 执行 stage
                result = self._run_stage(stage, stage_cfg)
                
                # 2. 5 层裁决
                decision = self.decision.evaluate(stage, result)
                
                # 3. Hard Gate
                if stage_cfg.get("hard_gate"):
                    self._notify_human(stage, decision)
                    if not self._wait_human_decision(stage):
                        # 人拒绝 → 进 failed
                        self.state.transition(stage, "failed", "human", "manual reject")
                        stage = "failed"
                        continue
                
                # 4. 转换到下一阶段
                next_stage = self._decide_next(stage, decision, stage_cfg)
                self.state.transition(stage, next_stage, "system", f"score={decision.score}")
                stage = next_stage
                
            except TimeoutError:
                # v3.5 原则 4 + 6: 写 handoff 含 don't list
                self.handoff_mgr.write(stage, self.session_start, error="timeout")
                print(f"[HANDOFF] {stage} 超时，已写入 handoff/。请下次 session 续跑。")
                return  # 优雅退出
    
    def _run_stage(self, stage, cfg):
        """执行单个 stage"""
        print(f"[STAGE] {stage} 开始")
        
        # 加载 spec（v3.5 原则 1: Spec is Sacred）
        spec = (self.project_dir / "spec.md").read_text()
        
        # 加载历史 context（3 模式）
        context_mode = cfg.get("context_mode", "last_only")
        context = self._load_context(stage, context_mode)
        
        # 调 LLM
        messages = self._build_prompt(stage, cfg, spec, context)
        
        # 评审用 evaluator model（v3.5 原则 2）
        role = "evaluator" if stage == "verify" else "generator"
        result = self.llm.chat(role, messages)
        
        # 写产物
        self._write_artifact(stage, result)
        
        return result
    
    def _decide_next(self, current, decision, cfg):
        """决定下一阶段"""
        if decision.passed:
            return cfg.get("on_success", "$end")
        return cfg.get("on_failure", "failed")
    
    def _check_session_timeout(self):
        """v3.5 原则 4: 30 分钟硬超时"""
        elapsed = (datetime.now() - self.session_start).total_seconds()
        if elapsed > 30 * 60:
            raise TimeoutError(f"Session > 30min ({elapsed}s)")
```

### 8.4 SelfCorrectEngine（3 档）

```python
# selfdriving/self_correct.py
class SelfCorrectEngine:
    """3 档错误恢复"""
    
    async def recover(self, error, stage, context) -> str:
        # Soft：自动恢复（不破坏流程）
        if self._is_transient(error):
            return await self._retry_with_backoff(stage, context)
        
        if self._is_schema_issue(error):
            return await self._regenerate(stage, context, error.feedback)
        
        # Hard：自动升级（重试代价高）
        if self._is_quality_issue(error):
            return await self._switch_approach(stage, context)
        
        if self._is_resource_exhausted(error):
            return await self._switch_model(stage, context)
        
        # Human：升级到人
        return await self._escalate_to_human(stage, error)
```

### 8.5 Handoff（含 don't list - v3.5 原则 6）

```python
# selfdriving/handoff.py
class HandoffManager:
    """v3.5 原则 6: Handoff Contains Don't"""
    
    def write(self, stage: str, session_start, error: str = None):
        handoff = {
            "stage": stage,
            "session_start": session_start.isoformat(),
            "do": [
                f"继续 {stage} 阶段",
                "参考上一次 artifact",
                "如果超时已经发生，不要重新跑全流程",
            ],
            "dont": [  # v3.5 原则 6 强制
                "不要修改 spec.md（LOCKED）",
                "不要跳过 verify 阶段",
                "不要在不同 stage 间随意跳转（除非状态机允许）",
                "不要重复执行已经成功的 stage",
            ],
            "context": self._collect_context(),
            "error": error,
        }
        
        # 写到文件
        handoff_path = self.project_dir / "handoffs" / f"session-{session_start.strftime('%Y%m%d-%H%M%S')}.yaml"
        handoff_path.parent.mkdir(parents=True, exist_ok=True)
        handoff_path.write_text(yaml.safe_dump(handoff, allow_unicode=True))
        
        # 记录到 SQLite
        with sqlite3.connect(self.state.db_path) as conn:
            conn.execute(
                "INSERT INTO handoffs (session_id, stage, do_list, dont_list, context) VALUES (?,?,?,?,?)",
                (..., stage, json.dumps(handoff["do"]), json.dumps(handoff["dont"]), json.dumps(handoff["context"]))
            )
```

---

## 九、5 层裁决（简化版）

```python
# selfdriving/decision.py
class DecisionAgent:
    """5 层裁决（v3.5 沿用 + 简化）"""
    
    def evaluate(self, stage: str, result) -> Decision:
        scores = {}
        
        # Layer 1: 环境（简单检查：spec 存在、产物写盘）
        scores["env"] = self._check_env(stage)
        
        # Layer 2: 产物（必需产物存在）
        scores["artifacts"] = self._check_artifacts(stage)
        
        # Layer 3: 质量（针对 stage 不同的质量检查）
        scores["quality"] = self._check_quality(stage, result)
        
        # Layer 4: 合规（v3.5 原则 1: spec 守恒）
        scores["compliance"] = self._check_compliance(stage, result)
        
        # Layer 5: 成本（token 不超预算）
        scores["cost"] = self._check_cost(stage)
        
        total = sum(scores.values()) / len(scores)
        passed = total >= 70 and all(s >= 50 for s in scores.values())
        
        return Decision(
            passed=passed,
            score=int(total),
            layers=scores,
            reason=self._format_reason(scores)
        )
    
    def _check_artifacts(self, stage):
        required = {
            "access": ["spec.md"],
            "apply": ["artifacts/apply/code", "artifacts/apply/tests"],
            "verify": ["artifacts/verify/test_report"],
        }
        missing = [a for a in required.get(stage, []) 
                   if not (self.project_dir / a).exists()]
        return 100 if not missing else max(0, 100 - len(missing) * 30)
```

---

## 十、Self-Improvement（v3.5 原则 7）

```python
# Lite 改 prompt，不改引擎
# 每次 stage 完成后，self_correct 把成功/失败模式记下来
# 下次跑时，自动调整 prompt

class SelfImprover:
    def record_outcome(self, stage, success, prompt, error=None):
        outcome = {
            "stage": stage,
            "success": success,
            "prompt_hash": hash(prompt),
            "error": error,
            "ts": datetime.now(),
        }
        # 写到 lessons/learned_patterns.json
        ...
    
    def improve_prompt(self, stage, base_prompt):
        """根据历史 success/fail 模式调整 prompt"""
        patterns = self._load_patterns(stage)
        # 简单的：加上成功 case + 失败 case 的反例
        return f"{base_prompt}\n\n## Learned from past runs:\n{patterns}"
```

---

## 十一、CLI 入口

```python
# selfdriving/cli.py
import click

@click.group()
def cli():
    """Self-Driving R&D Lite"""
    pass

@cli.command()
@click.argument("project")
def run(project):
    """跑一个项目"""
    from .engine import WorkflowRunner
    from .state import StateManager
    from .llm import LLMInterface
    from .decision import DecisionAgent
    from .self_correct import SelfCorrectEngine
    from .handoff import HandoffManager
    
    config = yaml.safe_load(open("config.yaml"))
    project_dir = Path(config["projects_root"]) / project
    
    llm = LLMInterface(config)
    state = StateManager(project_dir)
    decision = DecisionAgent(project_dir)
    self_correct = SelfCorrectEngine()
    handoff_mgr = HandoffManager(project_dir, state)
    
    runner = WorkflowRunner(project_dir, llm, state, decision, self_correct, handoff_mgr)
    runner.run()

@cli.command()
@click.argument("project")
def status(project):
    """查看项目状态"""
    state = StateManager(...)
    print(state.get_state())

@cli.command()
@click.argument("project")
@click.option("--approve/--reject", required=True)
def gate(project, approve):
    """处理 Hard Gate"""
    # 写决策到 .comet.yaml
    ...

if __name__ == "__main__":
    cli()
```

---

## 十二、实施计划（**2 周上线**）

### Week 1：核心骨架
- **Day 1-2**：写 `state.py`（200 行）+ `llm.py`（150 行）
- **Day 3**：`engine.py` 主体（250 行）
- **Day 4**：`decision.py`（150 行）+ `self_correct.py`（100 行）
- **Day 5**：`session.py`（80 行）+ `handoff.py`（80 行）+ `cli.py`（100 行）

### Week 2：Skills + 测试
- **Day 6-7**：写 5 个核心 skill（web_search / code_generator / test_runner / requirement_parser / doc_writer）
- **Day 8-9**：跑 1-2 个真实小项目
- **Day 10**：写 README + 文档

**总计：~1100 行核心代码 + 5 个 skill + 真实项目验证**

---

## 十三、验证标准

**MVP 上线标准**（2 周后必须达到）：

| 标准 | 目标值 | 验证方式 |
|------|--------|---------|
| 单项目 token 消耗 | < 100k | 跑 1 个 demo |
| 单项目运行时间 | < 30 分钟 | 跑 1 个 demo |
| 人工介入次数 | < 5 次/项目 | 跑 1 个 demo |
| 配置时间 | < 5 分钟/项目 | 写一个新项目 |
| 跨 session 续跑 | 能（handoff 含 don't）| 故意超时一次 |
| 不同 model 评审 | 强制（v3.5 原则 2）| 单元测试 |
| 状态机非法转换 | 拒绝 | 单元测试 |

---

## 十四、与 v3.5 / v4.2 的关系

```
v3.5（实战）                  v5.0-lite（本版本）
OpenClaw 依赖           →      独立可移植
9 stage 矩阵           →      3 阶段默认（可扩 8）
33 组件                →      7 核心
5-mode self-correct    →      3 档（soft/hard/human）
sessions_spawn 调度    →      直接 Python 调用
8 条架构原则           →      8 条原则 100% 落地 ✅

v4.2（设计蓝图）
30+ 概念              →      7 核心 ✅
YAML + Jinja2         →      YAML + 简单 Python 路由
Org Chart / Heartbeat  →      砍掉
MCP / ACP             →      砍掉
Plugin / Template     →      砍掉
```

**v5.0-lite = v3.5 原则 + v4.x 独立骨架 + 7 核心 = 真正可落地**

---

## 十五、未来演进路径

```
v5.0-lite (2 周)        v5.1-standard (3 月)        v5.2-pro (6-12 月)
- 3 阶段                 - 8 阶段                      - 完整 8 阶段
- 1 agent                - 2-3 agent                   - 多 agent + Org Chart
- CLI                    - CLI + 简单 Web              - 完整 Web Dashboard
- 无并行                 - 基础并行                    - 完整 DAG
- SQLite 状态            - SQLite + 备份               - 分布式存储
- 5 层裁决               - 完整 5 层                   - 含 ML 自学习裁决
                          - Heartbeat (简单)            - 完整 Heartbeat 队列
                          - ParaMemory (基础)           - 完整 Memento Man
                                                         - ACP / MCP / Plugin
                                                         - Importable Templates
```

**每一步都必须先在真实项目跑过**，不靠设计。

---

## 十六、最终结论

**v5.0-lite 是 v3.5 的"独立 + 简化"重制版**：
- 8 条 v3.5 原则 100% 落地
- 完全脱离 OpenClaw
- 7 个核心能力
- ~1100 行 Python
- 1 人 2 周可上线
- 真实项目验证

**这就是我们接下来要做的"产品"**——不是 v4.2（设计蓝图），不是 v3.5（OpenClaw 绑定），是 **v5.0-lite**。

要不要我直接开始写 `workflow.yaml` + 核心 6 个 Python 文件的代码？
