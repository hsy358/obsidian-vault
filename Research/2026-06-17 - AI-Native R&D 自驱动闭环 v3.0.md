---
title: AI-Native R&D 自驱动闭环 v3.0（GAN 架构 + Loop Engineering + 长跑实战）
author: OpenClaw 小助
publish_date: '2026-06-17'
saved_date: '2026-06-17'
type: research-report
okf_metadata:
  schema: okf-v0.1-inspired
  version: 3.0
  supersedes:
  - 2026-06-17 AI-Native R&D 全流程方案 v1.0
  - 2026-06-17 AI-Native R&D 自驱动闭环 v2.0
  - 2026-06-17 AI-Native R&D 对照 YX Harness v2.1
  evolution: v1.0 7阶段 → v2.0 自驱动 → v2.1 8阶段+评分 → v3.0 GAN+Loop Engineering
  inputs:
  - v1.0/v2.0/v2.1 历史方案
  - 4 组新搜索结果（2026-06-17）
  - YX AI Delivery Harness dashboard（8 阶段命名来源）
status: implementable
description: 每次 subagent 输出后，强制 validator 跑一遍： - 输出中提到的文件存在吗？ - 提到的数字（如"覆盖率 85%"）能验证吗？
  - 跟 sp...
timestamp: '2026-06-17T00:00:00'
tags:
- AI
---
# AI-Native R&D 自驱动闭环 v3.0

> **关键发现**（来自 Anthropic 2026 最新研究）：
> ❌ **AI 自我评分是陷阱** — 当 AI 评估自己的工作时，**几乎总是批准**，哪怕结果很糟糕
> ❌ **SWE-Bench Pro** 显示 frontier 模型在长跑任务上只拿 **23%**（vs SWE-Bench Verified 80%）
> ✅ **真正有效的是 GAN 架构**：Generator（做事）+ Evaluator（评判）**分离**
> ✅ **3 角色**：**Planner**（规划）+ **Generator**（生成）+ **Evaluator**（评估）
> ✅ **Loop Engineering**：设计让 AI 自己 prompt 自己的 loop，不是人 prompt AI

---

## 一、v2.1 → v3.0 关键升级（5 个修正）

| 维度 | v2.1（错误做法）| v3.0（正确做法）| 来源 |
|---|---|---|---|
| **评分** | AI 自评 0-100 | **Adversarial Evaluator 单独评估** | Anthropic GAN |
| **架构** | 单 orchestrator | **3 loops：Analysis → Planning → Execution** | Compound Product |
| **任务定义** | tasks.json 简单列表 | **Sprint Contracts**（输入+输出+测试+验收）| Anthropic Agent SDK |
| **session 衔接** | progress.txt | **Structured Handoffs**（不只是日志）| Anthropic Harness |
| **失败处理** | Self-Heal 3 次升级 | **Anti-hallucination propagation 验证** | Augment Code |

---

## 二、v3.0 核心架构

### 2.1 3 Loop 架构（来自 Compound Product 模式）

```
┌──────────────────────────────────────────────────────────────┐
│ L0  人类扔需求（1 行 / 1 链接）                                │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ Loop 1: Analysis Loop（5-30 min）                             │
│   ├─ Explore Agent：自动调研 / 竞品 / 可行性                │
│   ├─ Propose Agent：生成 3 套方案（tournament）             │
│   └─ Output: explore.md + propose.md                         │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ Loop 2: Planning Loop（10-30 min）                            │
│   ├─ Planner Agent：拆 Sprint Contracts                      │
│   ├─ 每个 Contract = 输入 + 输出 + 测试 + 验收               │
│   └─ Output: sprint-contracts.md + tasks.json              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ Loop 3: Execution Loop（10+ 小时，self-driven）               │
│   ├─ 8 个 stage 顺序执行                                    │
│   ├─ 每 stage = Planner + Generator + Evaluator 三角色     │
│   ├─ Evaluator 失败 → Self-Heal Loop（3 次）                │
│   └─ 持续到所有 stage 完成 + 全部 Evaluator PASS             │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ L9  交付 + 知识回灌                                          │
│   ├─ Archive Agent：沉淀到 vault                             │
│   ├─ Skill Extractor：把成功经验转为 skill                   │
│   └─ OKF metadata 完整化                                    │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 3 角色 × 8 Stage（每 stage 内部）

| 角色 | 职责 | 工具 |
|---|---|---|
| **Planner** | 决定该 stage 下一步做什么 | ReAct 循环 |
| **Generator** | 执行（写代码/写文档/跑测试）| 文件/命令 |
| **Evaluator** | 独立评判（不同 prompt / 不同 model）| Adversarial |

**关键**：Evaluator 必须**用不同的 prompt 模板**或**不同的 model**，否则就是 self-eval 陷阱。

---

## 三、Sprint Contracts（替代 tasks.json 简单任务）

### 3.1 格式

```yaml
# sprint-contracts/feature-a.yaml
contract_id: feature-a
stage: apply
input:
  spec: "Implement user login with email/password"
  dependencies: ["feature-x"]
output:
  files:
    - src/auth/login.py
    - tests/test_login.py
  behavior: "User can log in with email+password, get JWT token"
tests:
  - "test_login_success"
  - "test_login_wrong_password"
  - "test_login_locked_account"
acceptance:
  - "All tests pass"
  - "Coverage ≥ 80%"
  - "No P0/P1 bugs"
  - "Lint clean"
estimated_tokens: 50000
estimated_minutes: 30
```

### 3.2 为什么 Sprint Contracts 重要

- **明确边界**（input/output）— Planner 不会跑偏
- **可测试**（tests）— Evaluator 有标准
- **可估算**（tokens/minutes）— Cost Guard 准确
- **可失败**（acceptance）— 失败有标准

---

## 四、Structured Handoffs（替代 progress.txt）

### 4.1 格式（每次 session 结束必写）

```markdown
# Handoff: session-{N} → session-{N+1}

## 完成的（Done）
- [feature-a] login implemented, 12 files, 800 lines
- [test] 23/25 pass, 2 known flakes

## 决策记录（Decisions）
- Used bcrypt over argon2 (reason: faster, library available)
- JWT TTL = 24h (reason: matches industry standard)

## 阻塞 / 已知问题（Blockers）
- [high] dep X install fails on Py 3.12, switched to 3.11
- [low] test_login_wrong_password flaky 1/100 runs

## 下一步（Next）
- [feature-b] implement signup (follows same pattern as login)
- [refactor] extract auth middleware (deprioritized)

## 约束 / 不要做（Constraints）
- Do NOT change JWT secret rotation logic (locked in security review)
- Do NOT add new dependencies without approval
- Spec is LOCKED — do not modify

## 关键文件路径
- src/auth/login.py:45 (main logic)
- tests/test_login.py (test entry)
- docs/security-review.md (locked)
```

### 4.2 vs progress.txt

| progress.txt（旧）| handoff.md（新）|
|---|---|
| 流水日志 | 结构化交接 |
| 跨 session 找 | **下次 session 第一个读** |
| 不强约束 | **明确"不要做"** |
| 没决策记录 | **决策可追溯** |

---

## 五、Anti-Hallucination 验证（multi-agent 关键）

### 5.1 问题（来自 Augment Code）

> "Hallucination propagation between agents, where one bad output becomes trusted input for every downstream agent in the pipeline. No mainstream framework validates message correctness between agents."

### 5.2 解决方案：Message Validator

```python
class MessageValidator:
    """验证 agent 之间的消息（防止幻觉传播）"""
    
    def validate(self, from_agent, to_agent, message):
        # 1. 格式校验
        if not self.check_format(message):
            return {"valid": False, "reason": "format_error"}
        
        # 2. 内容校验（关键）
        issues = []
        
        # 引用校验：消息中提到的文件路径必须存在
        for path in extract_paths(message):
            if not Path(path).exists():
                issues.append(f"path_not_found: {path}")
        
        # 数据校验：提到的数字必须可验证
        for claim in extract_claims(message):
            if not self.verify_claim(claim):
                issues.append(f"unverifiable_claim: {claim}")
        
        # 一致性：跟 spec.md / tasks.json 是否冲突
        if conflicts_with_spec(message):
            issues.append("conflicts_with_spec")
        
        if issues:
            return {"valid": False, "issues": issues, "action": "reject_and_redo"}
        return {"valid": True}
```

### 5.3 关键检查点

每次 subagent 输出后，**强制 validator 跑一遍**：
- 输出中提到的文件存在吗？
- 提到的数字（如"覆盖率 85%"）能验证吗？
- 跟 spec.md 冲突吗？
- 有 hallucinated import / API 吗？

---

## 六、Loop Engineering 核心模式

### 6.1 核心思想（来自 Loop Engineering 2026）

> "Stop prompting your coding agent, and start designing the loop that prompts it for you."

**关键转变**：
- ❌ 人 → prompt → AI → 等待 → 人 → 再 prompt
- ✅ 人 → 设 loop → AI 自己 prompt 自己 → 跑到完成

### 6.2 Loop Engine 实现

```python
class LoopEngine:
    """自我驱动的循环引擎"""
    
    def run(self, project, max_iterations=100):
        for i in range(max_iterations):
            state = self.read_state(project)
            
            # 1. 完成检查
            if self.is_done(state):
                log(f"Iteration {i}: DONE")
                break
            
            # 2. 超限检查
            if self.cost_guard.exceeded():
                log(f"Iteration {i}: COST/TIME EXCEEDED")
                request_human_intervention()
                break
            
            # 3. Planner 决定下一步
            plan = self.planner.next_action(state)
            log(f"Iteration {i}: PLAN = {plan}")
            
            # 4. Generator 执行
            result = self.generator.execute(plan)
            
            # 5. Validator 检查（防 hallucination）
            validation = self.validator.validate(result)
            if not validation["valid"]:
                log(f"Iteration {i}: VALIDATION FAILED: {validation['issues']}")
                continue  # 不写入 progress，下次重做
            
            # 6. Evaluator 评估（独立）
            evaluation = self.evaluator.evaluate(result)
            log(f"Iteration {i}: EVAL = {evaluation}")
            
            # 7. 写 Structured Handoff
            self.write_handoff(state, plan, result, evaluation)
            
            # 8. Git commit
            git_commit(f"iter-{i}: {plan.summary}")
            
            # 9. Sleep（避免 hot loop）
            time.sleep(60)
```

### 6.3 Anti-Context-Anxiety 提示

每次 session 开始时，**明确告诉 AI**：
```
"你正在执行 X 项目的 Y 阶段。
之前 N 个 session 已经做完了 ABC。
不要质疑之前的决策（除非有明确证据）。
这是多 session 项目，信任 progress/handoff.md。
你的工作 = 增量推进，不是重新评估整个项目。"
```

---

## 七、9 Critical Failure Patterns（来自 DAPLab Columbia）

我们要在 self-heal loop 里**主动检测**这 9 个：

| # | Failure Pattern | 检测方法 |
|---|---|---|
| 1 | User/Agent 描述错位 | 写代码后回看 spec 对比 |
| 2 | 局部修复合不上整体 | 集成测试 |
| 3 | 边界条件未处理 | 边界测试 |
| 4 | 状态管理错误 | 状态机测试 |
| 5 | 异步竞争 | 并发测试 |
| 6 | 错误处理缺失 | 异常路径测试 |
| 7 | 安全漏洞 | 安全扫描 |
| 8 | 性能退化 | 性能基线 |
| 9 | 可维护性差 | Lint / 类型检查 |

**每个 stage 完成后，Evaluator 必须**对照**这 9 项**。

---

## 八、Trace as Primary Debugging

### 8.1 完整 Trace 格式

```json
{
  "session_id": "003",
  "timestamp": "2026-06-17T16:00:00",
  "stage": "apply",
  "trace": [
    {
      "actor": "planner",
      "action": "decide_next",
      "input": "current_state: {tasks: 5, done: 1}",
      "output": "next: implement feature-a",
      "tokens": 1200,
      "duration_ms": 8500
    },
    {
      "actor": "generator",
      "action": "write_code",
      "input": "contract: feature-a",
      "output": "files: [src/auth/login.py, tests/test_login.py]",
      "tokens": 8500,
      "duration_ms": 45000
    },
    {
      "actor": "validator",
      "action": "validate",
      "input": "files: [...]",
      "output": "{valid: true, issues: []}",
      "tokens": 300,
      "duration_ms": 2000
    },
    {
      "actor": "evaluator",
      "action": "evaluate",
      "input": "code: ..., contract: feature-a",
      "output": "{score: 0.85, issues: ['lint warning: line 23'], pass: true}",
      "tokens": 1500,
      "duration_ms": 10000
    }
  ],
  "total_tokens": 11500,
  "total_duration_ms": 65500,
  "result": "ok"
}
```

### 8.2 何时用 trace 调试

- ❌ 失败时重跑（浪费时间）
- ✅ **读 trace 找根因** → 改 generator 的 prompt → 重跑

---

## 九、Skill Library（成功经验自动沉淀）

### 9.1 模式（来自 SICA）

> "Successful skills are stored in a **skill library** and reused in future tasks, effectively acting as persistent self-improvement"

### 9.2 实现

每次 stage 完成后，Archive Agent 不仅写 lessons，还**生成可复用 skill**：

```bash
# archive-agent 自动执行
# 1. 提取这次成功的 pattern
# 2. 写成 skill
mkdir -p /root/.openclaw/workspace/skills/{extracted-skill-name}
# 3. 写 SKILL.md
# 4. 加到 skill list
```

### 9.3 skill 触发规则

**Orchestrator 检查**：
- 每个 stage 前 → 查 skill library → 有匹配的 skill 就用
- 优先用 library skill 跑（已验证），不优先用 LLM 重新做

---

## 十、v3.0 vs v2.1 对比

| 维度 | v2.1 | v3.0 |
|---|---|---|
| **整体架构** | 8 阶段单 loop | **3 loops（Analysis/Planning/Execution）** |
| **每 stage 角色** | 1 个 subagent | **3 角色（Planner/Generator/Evaluator）** |
| **评分** | AI self-score 0-100 | **Adversarial Evaluator（独立 prompt）** |
| **任务定义** | tasks.json 简单列表 | **Sprint Contracts（带测试+验收）** |
| **session 衔接** | progress.txt | **Structured Handoffs（明确"不要做"）** |
| **失败防护** | Self-Heal 3 次 | **Self-Heal + Anti-hallucination Validator** |
| **调试** | 凭直觉 | **Trace 优先（每步都有记录）** |
| **经验沉淀** | lessons.md | **Skill Library（自动生成可复用 skill）** |
| **任务粒度** | Stage 级别 | **Sprint Contract 级别（更小）** |

---

## 十一、所需工具与能力清单

### 11.1 已有 ✓

- OpenClaw sessions_spawn / sessions_yield
- OpenClaw cron
- OpenClaw message
- context-recovery skill
- 67 个现有 skills
- akshare / web_search / message 等工具

### 11.2 需要新建

| 工具 | 用途 | 工作量 |
|---|---|---|
| `self-driving-rd-v3` Skill | 3 loops + 3 roles | 1 天 |
| `orchestrator_v3.py` | Loop Engine | 1.5 天 |
| `message_validator.py` | Anti-hallucination | 0.5 天 |
| `evaluator.py` | Adversarial Evaluation | 0.5 天 |
| `trace_logger.py` | 完整 trace 记录 | 0.5 天 |
| `sprint_contract.py` | Contract 模板 | 0.5 天 |
| `handoff_writer.py` | Structured Handoff | 0.5 天 |
| `skill_extractor.py` | 自动生成 skill | 1 天 |
| **合计** | | **~6 天** |

### 11.3 验证

- [ ] 3 loops 跑通（每 loop < 30 min）
- [ ] 3 角色（Planner/Generator/Evaluator）跑通
- [ ] Adversarial Evaluator 真的能抓 bug
- [ ] Message Validator 拦截 hallucination
- [ ] Structured Handoff 跨 session 续跑成功
- [ ] Trace 调试有效
- [ ] Skill Library 自动沉淀

---

## 十二、立即可落地的最小可行方案（MVP）

### 12.1 1 周可启动

| Day | 工作 | 产出 |
|---|---|---|
| 1 | 写 `orchestrator_v3.py`（Loop Engine）| 主循环跑通 |
| 2 | 写 3 个 role agent templates | Planner/Generator/Evaluator |
| 3 | 写 `message_validator.py` | Anti-hallucination |
| 4 | 写 `sprint_contract.py` + `handoff_writer.py` | 任务结构 + 衔接 |
| 5 | 写 `evaluator.py` | Adversarial Evaluation |
| 6 | 改造 `self-driving-rd` Skill | 整合 v3 |
| 7 | 跑第 1 个真实项目 | 端到端验证 |

### 12.2 第 1 个项目建议

**v2.1 → v3.0 升级项目**：
- 让 AI 自己用 3 loops + 3 roles 升级 orchestrator
- **Meta 验证**：AI 升级 AI
- 证明 v3.0 的 self-improvement 能力

### 12.3 验证指标

| 指标 | 目标 |
|---|---|
| 端到端耗时 | < 8h |
| Evaluator 抓 bug 率 | ≥ 80% |
| Validator 拦截 hallucination | ≥ 90% |
| Session 续跑成功率 | 100% |
| 失败升级 Hard Gate 率 | < 20% |

---

## 十三、长期演进

### 13.1 v3.5：自优化 Feedback Loop

- 每完成项目 → 提取 patterns → 自动优化下次 loop 参数
- 例如：如果 80% 失败在"探索"阶段 → 自动加更多 explore subagent

### 13.2 v4.0：跨项目 Skill Transfer

- Skill Library 跨项目共享
- "Vibe Coding" skill（来自 vault 文章）作为跨项目通用

### 13.3 v5.0：完全自治

- Hard Gate 1 也自动化（基于历史偏好）
- 何大人只看最终交付

---

## 十四、关键引用

### 14.1 联网搜索（2026 最新）

- **Anthropic**: Effective harnesses for long-running agents（2025-11）
  - Initializer + Coding Agent + claude-progress.txt
  - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- **Anthropic**: Harness design for long-running application development
  - **3-agent 架构：Planner + Generator + Evaluator**
  - https://www.anthropic.com/engineering/harness-design-long-running-apps
- **Anthropic Workshop**: Build Agents That Run for Hours
  - **Self-evaluation is a trap**（核心警示）
  - Adversarial evaluator agents work better
  - Structured handoffs > context compaction
- **Anthropic Opus 4.5/4.6**: Long-running agent SDK
  - Generator-Evaluator contract
  - Rubrics for subjective output
  - Traces as primary debugging
- **DAPLab Columbia**: 9 Critical Failure Patterns
  - https://daplab.cs.columbia.edu/general/2026/01/08/9-critical-failure-patterns-of-coding-agents.html
- **Augment Code**: Multi-Agent AI Systems Failure Modes
  - **Hallucination propagation** 关键问题
- **SWE-Bench Pro**: Long-Horizon Software Engineering
  - Frontier models only 23% (vs SWE-Bench 80%)
  - https://openreview.net/forum?id=9R2iUHhVfr
- **Loop Engineering 2026**: Designing the loop that prompts itself
  - https://tosea.ai/blog/loop-engineering-ai-agents-complete-guide-2026
- **Compound Product** (snarktank): Analysis → Planning → Execution loops
  - https://github.com/snarktank/compound-product
- **Karpathy autoresearch** (March 2026): 630-line Python self-improving
- **Reflexion** (Princeton/MIT 2023): Verbal self-reflection in memory
- **SICA**: Skill library pattern

### 14.2 历史引用

- v1.0 / v2.0 / v2.1（已存在）
- 13 篇 vault 公众号文章
- YX AI Delivery Harness dashboard

---

## 十五、致何大人的判断

### 15.1 v3.0 相比 v2.1 的本质变化

| 维度 | v2.1 | v3.0 |
|---|---|---|
| 核心思想 | "AI 跑 8 阶段" | "**3 loops 跑 + 3 角色相互制衡**" |
| 评分 | AI 自己评 0-100 | **独立 Evaluator 评判（GAN 式）** |
| 任务 | tasks.json 列表 | **Sprint Contracts（带测试）** |
| 衔接 | progress.txt 日志 | **Structured Handoff（明确边界）** |
| 失败 | Self-Heal 3 次 | **Self-Heal + Message Validator** |
| 沉淀 | lessons.md | **Skill Library（自动生成 skill）** |
| 调试 | 凭直觉 | **Trace 优先** |
| 来源 | YX Harness 启发 | **Anthropic 2026 最新 + Compound Product + Karpathy** |

### 15.2 关键洞察

1. **AI 自评不可信** — Anthropic 反复强调：AI 评 AI 几乎总批准
2. **长跑任务比想象难 3-4 倍** — SWE-Bench Pro 23% vs SWE-Bench 80%
3. **Loop > Prompt** — 设计让 AI 自己 prompt 自己的 loop
4. **3 角色 > 1 角色** — Planner/Generator/Evaluator 制衡
5. **Sprint Contract > Task** — 明确边界 + 测试 + 验收
6. **Handoff > Progress** — 不只是日志，明确"不要做"
7. **Skill Library > Lessons** — 沉淀成可复用 skill

### 15.3 实施建议

**今天（30 min 决策）**：
1. 确认 v3.0 升级方向 ✓
2. 选第一个项目（v2.1 → v3.0 升级）
3. 确认 6 天时间表

**明天（6 天搭建）**：
4. 写 orchestrator_v3.py（Loop Engine）
5. 写 3 role templates
6. 写 validator + evaluator + handoff
7. 跑第 1 个项目验证

**长期（1 月+）**：
8. v3.5：自优化 feedback
9. v4.0：跨项目 skill transfer
10. v5.0：完全自治

---

> **一句话总结 v3.0**：
> 抛弃 AI 自我评分（陷阱），改用 **GAN 式 Adversarial Evaluation**；抛弃单 loop，改用 **3 loops × 3 roles**；抛弃简单 tasks，改用 **Sprint Contracts**；抛弃 progress.txt，改用 **Structured Handoffs**；抛弃 lessons，改用 **Skill Library**。6 天可落地。
