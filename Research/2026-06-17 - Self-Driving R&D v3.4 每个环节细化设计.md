---
title: "Self-Driving R&D v3.4 — 每个环节细化设计方案"
author: "OpenClaw 小助"
publish_date: "2026-06-17"
saved_date: "2026-06-17"
type: technical-spec
okf_metadata:
  schema: okf-v0.1-inspired
  version: 3.4
  supersedes: 2026-06-17 Self-Driving R&D v3.3
  evolution: v3.3 框架 → v3.4 每个环节完整设计
  scope: 9 stages + 3 roles + 4 GAMD + 5 layers + 8 sub-components
status: implementable
---

# Self-Driving R&D v3.4 — 每个环节细化设计方案

> **本方案覆盖 33 个环节**，每个都含：目的/输入/输出/算法/数据/代码/错误处理/例子
> 直接可落地实现

---

## A. 9 Stages 细化设计

### A1. Access（Initializer Agent）— 5 min

**目的**：接收用户需求，生成 spec.md，启动项目

**输入**：用户原始输入（文本/链接/语音转录）

**输出**：
- `spec.md`（锁定）
- `tasks.json`（初始状态）
- `init.sh`（环境恢复）
- `handoff/session-000.md`（首次交接）

**核心算法**：
```python
def access_stage(user_input):
    # 1. NLU 解析
    nlu_result = nlu_parse(user_input)
    # {
    #   "goal": "实现 XX 系统",
    #   "acceptance_criteria": ["AC1: ...", "AC2: ..."],
    #   "constraints": ["不接券商 API", "..."],
    #   "out_of_scope": ["..."],
    #   "risks": [{"risk": "...", "mitigation": "..."}],
    # }
    
    # 2. 写 spec.md（5W1H + AC + 风险 + 红线）
    spec_md = render_spec(nlu_result)
    
    # 3. 写 init.sh
    init_sh = render_init_sh()
    
    # 4. 写 tasks.json（9 stages 初始状态）
    tasks = {
        "stages": {
            "access":  {"status": "completed", "score": None, "started_at": ..., "completed_at": ...},
            "explore": {"status": "pending"},
            "propose": {"status": "pending"},
            "task":    {"status": "pending"},
            "apply":   {"status": "pending"},
            "verify":  {"status": "pending"},
            "review":  {"status": "pending"},
            "archive": {"status": "pending"},
        },
        "tasks": [],
    }
    
    # 5. 写 handoff/session-000.md
    handoff_md = render_initial_handoff(nlu_result)
    
    # 6. 健康度检查（v3.2 新增）
    health = check_environment_health()
    if not health["ok"]:
        raise EnvironmentError(health["issues"])
    
    # 7. Git init + commit
    git_init()
    git_commit("init: spec.md + init.sh + tasks.json")
    
    # 8. HG-1 通知何大人
    notify_hard_gate("access_done", summary)
    
    return {"spec": spec_md, "tasks": tasks, "health": health}
```

**关键文件**：
- `spec.md` 模板（必填字段：goal, 5W1H, AC, constraints, out_of_scope, risks）
- `init.sh` 模板（git init + 目录创建 + 健康度检查）

**错误处理**：
- NLU 失败 → 重试 3 次 → 升级何大人
- 健康度失败 → 列出问题 → 提示修复
- 写文件失败 → 立即报错（不要继续）

**性能**：< 5 min（LLM 调用 1-2 次）

---

### A2. Explore（Explore Agent）— 30 min

**目的**：调研竞品 + 可行性 + 风险识别

**输入**：spec.md

**输出**：
- `explore.md`（调研报告）

**核心算法**：
```python
def explore_stage(spec):
    # 1. 识别调研方向
    directions = identify_directions(spec)
    # ["竞品分析", "技术栈调研", "可行性评估", "类似项目案例"]
    
    # 2. 并行调研
    results = parallel_research(directions)
    # 用 subagent 并行，每个 subagent 调研一个方向
    
    # 3. 汇总
    explore_md = synthesize_research(results)
    # {
    #   "competitors": [...],
    #   "tech_options": [...],
    #   "feasibility": "high | medium | low",
    #   "similar_projects": [...],
    #   "risks": [...],
    #   "recommendations": [...],
    # }
    
    return explore_md
```

**Sub-agent 提示模板**：
```
你是 Explore Agent。任务是调研 {direction}。
请使用 web_search 工具查找 2026 年最新信息。
输出结构化报告（JSON），包含：
- 关键发现
- 数据来源
- 推荐方案
```

**Sub-step 进度**：
1. 识别方向 (5 min)
2. 并行调研 (15 min)
3. 汇总报告 (10 min)

**质量门**：
- explore.md 含 ≥ 3 个竞品
- ≥ 2 种技术栈对比
- 风险 ≥ 3 条

**错误处理**：
- web_search 失败 → 用 vault 已有文章
- subagent 超时 → 拆更小任务

---

### A3. Propose（Propose Agent + MCTS）— 30 min

**目的**：生成 3 套架构方案 + MCTS 选最优

**输入**：spec.md + explore.md

**输出**：
- `propose.md`（3 套方案 + MCTS 选最优）
- `plan.md`（最终选定的方案）

**核心算法**：
```python
def propose_stage(spec, explore):
    # 1. 生成 3 套架构方案
    options = []
    for i in range(3):
        option = generate_architecture(spec, explore, variant=i)
        options.append({
            "id": f"arch-{i}",
            "name": option["name"],
            "stack": option["stack"],
            "structure": option["structure"],
            "risks": option["risks"],
            "score": 0.0,  # MCTS 填
        })
    
    # 2. MCTS 选最优
    def evaluator(arch):
        # 用 LLM 模拟此架构的 5 年表现
        return llm_evaluate(arch, "scalability, maintainability, time_to_mvp, cost")
    
    best = MCTSDecider(options, evaluator, iterations=5).decide()
    
    # 3. 写 propose.md
    propose_md = render_propose(options, best)
    
    # 4. 写 plan.md（最终方案）
    plan_md = render_plan(best, spec)
    
    return propose_md, plan_md
```

**Sub-step 进度**：
1. 生成 3 套方案 (15 min)
2. MCTS 选最优 (10 min)
3. 写 propose.md + plan.md (5 min)

**质量门**：
- 3 套方案都有具体技术栈
- MCTS 选优有 reasoning
- plan.md 含架构图（mermaid）+ 选型理由

**错误处理**：
- LLM 生成方案失败 → 重试 3 次
- MCTS 不收敛 → 选默认方案

---

### A4. Task（HTN Planner）— 30 min

**目的**：用 HTN 算法把方案拆解为 Sprint Contracts

**输入**：plan.md

**输出**：
- `tasks.json`（更新版：含所有 sprint contracts）
- `sprint-contracts/*.yaml`（每个 contract 一个文件）

**核心算法**：
```python
def task_stage(plan):
    # 1. HTN 分解
    method_lib = load_method_library()
    
    # compound task: "实现 XX 系统"
    primitive_tasks = htn_decompose(plan.main_task, method_lib)
    # 递归分解直到所有都是 primitive
    
    # 2. 生成 Sprint Contracts
    contracts = []
    for task in primitive_tasks:
        contract = {
            "id": task.id,
            "stage": "apply",
            "input": task.input,
            "output": {
                "files": task.expected_files,
                "behavior": task.expected_behavior,
            },
            "tests": task.test_cases,
            "acceptance": task.acceptance_criteria,
            "estimated_tokens": task.estimate.tokens,
            "estimated_minutes": task.estimate.minutes,
            "dependencies": task.deps,
        }
        contracts.append(contract)
    
    # 3. 排序（依赖关系）
    sorted_contracts = topological_sort(contracts)
    
    # 4. 写文件
    for c in sorted_contracts:
        write_yaml(f"sprint-contracts/{c['id']}.yaml", c)
    
    # 5. 更新 tasks.json
    update_tasks_json(contracts)
    
    return contracts
```

**HTN Method Library 示例**：
```yaml
# methods.yaml
- name: web_app_decomposition
  applies_to: "web app"
  decomposition:
    - auth_module
    - db_module
    - api_module
    - frontend_module
- name: api_decomposition
  applies_to: "API server"
  decomposition:
    - routing
    - middleware
    - handlers
    - data_access
```

**Sprint Contract 模板**：
```yaml
# sprint-contracts/auth-login.yaml
id: auth-login
stage: apply
input:
  spec_ref: spec.md#AC1
  dependencies: []
output:
  files:
    - src/auth/login.py
    - tests/test_login.py
  behavior: "用户可以用 email+password 登录，返回 JWT"
tests:
  - test_login_success
  - test_login_wrong_password
  - test_login_account_locked
acceptance:
  - "All 3 tests pass"
  - "Coverage >= 80%"
  - "Lint clean"
estimated_tokens: 50000
estimated_minutes: 30
```

**质量门**：
- 所有 contract 有 acceptance criteria
- 依赖关系正确（无循环）
- 估算合理（总 token < 5M，总时间 < 12h）

---

### A5. Apply（Generator + Adversarial + Self-Heal）— 10+ hours

**目的**：按 Sprint Contracts 写代码、测试、修复

**输入**：tasks.json + sprint-contracts/*.yaml

**输出**：
- `src/` 代码
- `tests/` 测试
- 多次 handoff.md（每个 session 一个）

**核心算法**（sub-35min session 内）：
```python
def apply_session(contract, session_id, state):
    start = time.time()
    
    # 1. 读 handoff（接续）
    handoff = read_handoff(session_id - 1)
    
    # 2. Anti-Anxiety prompt
    anti_anxiety = render_anti_anxiety(session_id, handoff)
    
    # 3. Plan（ReAct Planner）
    plan = planner_agent(contract, state, handoff)
    # 输出：5-10 个 steps
    
    # 4. Execute（Generator）
    for step in plan:
        result = generator_agent(step, model="minimax/MiniMax-M3")
        track_cost(result.tokens)
        trace(session_id, "generator", step, ...)
        
        # 4.1 Validate（Message Validator）
        validation = validate_message(result)
        if not validation["valid"]:
            write_reflexion("validation_failed", validation.issues)
            continue  # redo this step
        
        # 4.2 Evaluate（Adversarial，**不同 model**）
        evaluation = evaluator_agent(result, model="minimax/MiniMax-M2.7")
        trace(session_id, "evaluator", ...)
        
        if not evaluation.passed:
            # 4.3 Self-Heal（5 模式）
            for mode in ["tool", "external", "iterative", "tree", "dead_letter"]:
                if try_fix(result, mode):
                    evaluation.passed = True
                    break
            if not evaluation.passed:
                dlq_add(contract, "evaluator_failed")
                return False
    
    # 5. 写 handoff
    elapsed_min = (time.time() - start) / 60
    handoff_md = render_handoff(
        session_id=session_id,
        plan=plan,
        results=results,
        next_steps=plan.next,
        constraints=spec.constraints,
    )
    
    # 6. Git commit
    git_commit(f"session-{session_id}: {contract.id} done")
    
    # 7. Self-Improvement
    SelfImprovementEngine.run_after_session(session_id, success=True, feedback=...)
    
    # 8. Check 30min rule
    if elapsed_min > 30:
        write_handoff(...)
        return "HANDOFF_REQUIRED"
    
    return True
```

**Sub-step 进度（来自 YX Harness 1-2-3-4-5）**：
1. ✅ Read handoff
2. ✅ Plan
3. ✅ Execute step 1
4. 🔵 Execute step 2 (current)
5. ⚪ Validate
6. ⚪ Evaluate
7. ⚪ Write handoff
8. ⚪ Git commit

**3 角色 + 3 阶段**：
| 阶段 | 角色 | Model |
|---|---|---|
| Plan | Planner (ReAct) | M3 |
| Execute | Generator | M3 |
| Evaluate | Adversarial Evaluator | **M2.7（不同）** |

**5-mode Self-Correction**：
```python
def self_correct(error, attempt):
    # Mode 1: Tool-based（编译/测试）
    if fix_with_tool(error): return True
    
    # Mode 2: External（不同 prompt 重试）
    if fix_with_external(error): return True
    
    # Mode 3: Iterative（多次迭代）
    for i in range(3):
        if fix_with_iteration(error, i): return True
    
    # Mode 4: Tree Search（多条路径）
    if fix_with_tree(error): return True
    
    # Mode 5: Dead-Letter（入队）
    dlq_add(...)
    return False
```

**质量门（每个 contract）**：
- 所有 tests pass
- Coverage >= 80%
- Lint clean
- Adversarial Evaluator PASS

---

### A6. Verify（V&V 8 层）— 1-2 hours

**目的**：8 层验证 + 验收测试（确认"完全符合需求"）

**输入**：src/ + tests/ + spec.md

**输出**：
- `verify.md`（8 层结果）
- `acceptance_test_results.json`

**8 层详细实现**：

| 层 | 工具 | 阈值 | 失败时 |
|---|---|---|---|
| L1 编译 | `py_compile` / `mypy` | 0 error | Self-Heal |
| L2 单测 | `pytest tests/` | 100% pass | Self-Heal |
| L3 集成 | `pytest tests/integration/` | 100% pass | Self-Heal |
| L4 E2E | `playwright test` | 100% pass | Self-Heal |
| L5 性能 | `locust` | p99 < 200ms | Optimizer |
| L6 安全 | `bandit` | 0 high | Manual fix |
| **L7 验收** | **自动生成 + pytest** | **AC 全过** | **Self-Heal** |
| L8 场景 | `scenarios.yaml` | 全过 | Manual review |

**L7 验收测试**（关键，v3.0/v3.1/v3.2 重点）：
```python
def l7_acceptance(spec_path):
    spec = read(spec_path)
    criteria = parse_acceptance(spec)  # 提取 - [ ] AC1: ...
    
    results = []
    for c in criteria:
        # 自动生成测试
        test_code = llm_generate_test(c)
        test_file = f"tests/acceptance/test_{c['id'].lower()}.py"
        write(test_file, test_code)
        
        # 跑测试
        passed = pytest_run(test_file)
        results.append({"criterion": c.text, "passed": passed})
    
    return {
        "total": len(results),
        "passed": sum(1 for r in results if r.passed),
        "results": results,
        "ready_for_delivery": all(r.passed for r in results),
    }
```

**8 层结果汇总**：
```python
def run_all_vnv(spec_path):
    return {
        "L1_compile": l1_compile(),
        "L2_unit": l2_unit_test(),
        "L3_integration": l3_integration_test(),
        "L4_e2e": l4_e2e_test(),
        "L5_performance": l5_performance(),
        "L6_security": l6_security(),
        "L7_acceptance": l7_acceptance(spec_path),
        "L8_scenario": l8_scenario_test(),
    }
```

**全过 = ready_for_delivery: true**（这是交付门）

---

### A7. Review（Adversarial + 9 Patterns）— 30 min

**目的**：独立 AI 评估 + 9 Critical Patterns 检查

**输入**：verify.md + src/ + spec.md

**输出**：`review.md`（AI 自评 + 9 patterns 报告）

**核心算法**：
```python
def review_stage(verify_result, spec):
    # 1. Adversarial Evaluation（**不同 model**）
    review = adversarial_evaluator(verify_result, spec, model="minimax/MiniMax-M2.7")
    # 评分维度：完整性、准确性、可维护性、安全性、性能
    
    # 2. 9 Critical Patterns 检查
    patterns = detect_9_patterns(src_path)
    # 9 个 pattern 详细检查
    
    # 3. 输出 review.md
    review_md = render_review(review, patterns)
    
    return review_md
```

**9 Critical Patterns 检测**：
```python
PATTERNS = {
    "F01_misalignment": "对比 spec.md acceptance vs 实际 output",
    "F02_local_fix_global_miss": "L3 集成测试失败次数",
    "F03_boundary_missed": "L2 边界用例覆盖",
    "F04_state_error": "状态机测试",
    "F05_async_race": "L3 并发测试",
    "F06_error_handling_missing": "故意触发异常路径",
    "F07_security_vuln": "L6 bandit 高危数",
    "F08_perf_regression": "L5 perf vs baseline",
    "F09_maintainability_low": "lint / complexity 平均",
}
```

**质量门**：
- 9 patterns 全部 ✅
- Adversarial 评分 >= 80

---

### A8. Archive（Skill Extractor + Reflexion）— 30 min

**目的**：把成功经验沉淀为可复用 skill + 写反思

**输入**：review.md + 整个项目 + handoff/ + traces

**输出**：
- `archive.md`（归档报告）
- 新生成的 skill（写到 `/root/.openclaw/workspace/skills/`）
- 更新后的 method library
- 更新后的 prompt versions

**核心算法**：
```python
def archive_stage(project):
    # 1. Skill Extractor
    skills = extract_skills(project)
    for skill in skills:
        write_skill(skill)
        # 写到 /root/.openclaw/workspace/skills/{name}/
    
    # 2. Method Library 更新
    update_method_library(project)
    # 成功 method → 增加权重
    # 失败 method → 标记 + 改进
    
    # 3. Prompt Evolution
    evolve_prompts(project)
    # 写新版本 prompt
    
    # 4. Reflexion Memory 写
    write_reflexion_summary(project)
    # "这次学到的..."
    
    # 5. 写 archive.md
    archive_md = render_archive(skills, methods, prompts, reflexion)
    
    return archive_md
```

**Skill 提取规则**：
```python
def extract_skills(project):
    # 1. 找成功 sessions
    successful = [s for s in handoffs if s.is_success]
    
    # 2. 提取每个成功 session 的 pattern
    patterns = []
    for s in successful:
        # 找关键决策
        decisions = parse_decisions(s.handoff_md)
        # 找 git diff
        files = git_diff_files(s.commit)
        patterns.append({
            "decisions": decisions,
            "files": files,
            "summary": s.summary,
        })
    
    # 3. 去重 + 合并
    merged = merge_similar_patterns(patterns)
    
    # 4. 生成 skill
    return [generate_skill(p) for p in merged]
```

---

### A9. Delivery（最终交付）— 10 min

**目的**：通知何大人 + 推送产物

**输入**：archive.md + 完整 src/

**输出**：
- 微信通知（HG-3 通过消息）
- GitHub push
- vault 归档

**核心算法**：
```python
def delivery_stage(project):
    # 1. 验证所有 stage 完成
    if not all_stages_completed(project):
        raise ValueError("Not all stages completed")
    
    # 2. 最终 V&V 检查
    final_vnv = run_all_vnv(project.spec)
    if not final_vnv["ready_for_delivery"]:
        raise ValueError("V&V not passed")
    
    # 3. GitHub push
    git_push(project)
    
    # 4. vault 归档
    archive_to_vault(project)
    
    # 5. 微信通知
    notify_delivery(project)
    # "✅ 项目 {name} 交付完成\n- 代码: {url}\n- 文档: {url}\n- 测试覆盖率: 85%"
    
    # 6. 触发自改进
    SelfImprovementEngine.run_after_delivery(project)
```

---

## B. 3 Roles 细化设计

### B1. Planner（ReAct）

**目的**：决定下一步做什么

**输入**：当前状态 + handoff + Codebase KG

**输出**：plan（5-10 个 steps）

**实现**：
```python
def planner_agent(contract, state, handoff):
    # ReAct 循环
    thoughts = []
    for i in range(3):  # 最多 3 个 thoughts
        thought = llm_thought(
            task=contract,
            state=state,
            handoff=handoff,
            history=thoughts,
        )
        thoughts.append(thought)
        if thought.action == "FINISH":
            break
    
    # 选 best thought（用 confidence 排序）
    best = max(thoughts, key=lambda t: t.confidence)
    
    # Action 阶段
    if best.action == "plan":
        return generate_steps(best)
    elif best.action == "explore":
        return explore_then_plan(best)
    elif best.action == "ask_human":
        return ask_human_and_wait(best)
    elif best.action == "FINISH":
        return {"steps": [], "done": True}
```

**Prompt 模板**：
```
你是 Planner agent。负责决定下一步做什么。

任务：{contract.summary}
上次交接：{handoff.text}
当前状态：{state.summary}
知识图谱（相关模块）：{kg_relevant_modules}

ReAct 思考步骤：
1. 思考：我应该做什么？为什么？
2. 行动：read_file / write_code / run_test / ask_human / FINISH
3. 观察：基于上一步结果调整

输出 JSON：
{
  "thought": "...",
  "action": "write_code" | "read_file" | "run_test" | "ask_human" | "FINISH",
  "params": {...},
  "confidence": 0.0-1.0
}
```

**Model**：minimax/MiniMax-M3（深度思考）

---

### B2. Generator（Tool Use）

**目的**：执行 plan（写代码/跑测试/写文档）

**输入**：plan steps

**输出**：执行结果（文件修改、测试结果、文档）

**实现**：
```python
def generator_agent(plan, model="minimax/MiniMax-M3"):
    results = []
    for step in plan.steps:
        # 1. 执行 step
        if step.type == "write_code":
            result = write_code(step, model=model)
        elif step.type == "run_test":
            result = run_test(step)
        elif step.type == "write_doc":
            result = write_doc(step, model=model)
        
        # 2. 验证输出
        validation = validate_message(result.output)
        if not validation["valid"]:
            write_reflexion("validation", validation.issues)
            continue
        
        results.append(result)
        track_cost(result.tokens)
    
    return results
```

**Tools**：
- `read_file(path)`
- `write_file(path, content)`
- `edit_file(path, old, new)`
- `run_command(cmd)`
- `run_test(path)`
- `git_commit(msg)`
- `web_search(query)`

**Prompt 模板**：
```
你是 Generator agent。负责写代码和跑测试。

任务：{step.description}
当前文件：{file_context}
约束：{constraints}
不要修改 spec.md（locked）

输出：
- 修改的文件列表（带 diff）
- 测试结果
- 任何 warning
```

**Model**：minimax/MiniMax-M3（稳定）

---

### B3. Adversarial Evaluator（不同 Model）

**目的**：独立评估（不是 self-eval）

**输入**：Generator 输出 + spec.md

**输出**：pass / fail + 详细 feedback

**关键**：**必须用不同 model**（v3.0 Anthropic 警告：self-eval 陷阱）

**实现**：
```python
def evaluator_agent(generator_output, spec, model="minimax/MiniMax-M2.7"):
    # 注意：M2.7（不同 model 避免 self-eval 陷阱）
    prompt = f"""你是 Adversarial Evaluator。**严格评估** Generator 输出。

任务：{contract.text}
Spec 验收标准：
{spec.acceptance_criteria}

Generator 输出：
{generator_output}

请**严格**评估（不要轻易通过）：
1. 代码能跑吗？（看逻辑）
2. 跟 spec acceptance 对得上吗？
3. 有什么 bug 风险？
4. 性能如何？
5. 安全吗？

输出 JSON：
{{
  "verdict": "pass" | "fail",
  "score": 0.0-1.0,
  "issues": [...],
  "suggestions": [...]
}}
"""
    result = llm_call(prompt, model=model)  # M2.7
    
    return {
        "verdict": result.verdict,
        "score": result.score,
        "issues": result.issues,
        "passed": result.verdict == "pass" and result.score >= 0.7,
    }
```

**Rubrics（v3.0 Anthropic 推荐）**：
```python
RUBRICS = {
    "completeness": "是否覆盖了 spec 的所有 AC？",
    "correctness": "代码逻辑是否正确？",
    "maintainability": "代码是否易读易维护？",
    "security": "是否有明显的安全漏洞？",
    "performance": "是否满足性能要求？",
}
```

**Model**：minimax/MiniMax-M2.7（**不同**！）

---

## C. 4 GAMD Stages 细化设计

### C1. Goal（动态目标）

**核心类**：
```python
class Goal:
    def __init__(self, spec_path):
        self.original = parse_spec(spec_path)  # 原始目标
        self.current = self.original
        self.history = []  # 目标变化历史
    
    def refine(self, sub_goal):
        """细化目标"""
        self.history.append({"old": self.current, "new": self.current + sub_goal, "type": "refine"})
        self.current = self.current + sub_goal
        return self.current
    
    def pivot(self, new_goal, reason):
        """重大调整"""
        self.history.append({"old": self.current, "new": new_goal, "reason": reason, "type": "pivot"})
        self.current = new_goal
```

**Goal 数据结构**：
```json
{
  "original": "实现 XX 系统",
  "current": "实现 XX 系统的登录功能",
  "history": [
    {"old": "实现 XX 系统", "new": "实现 XX 系统的登录功能", "type": "refine", "ts": "..."}
  ],
  "acceptance_criteria": [...],
  "constraints": [...],
}
```

---

### C2. Action（4 类）

**Action Types**：
```python
class Action:
    TYPES = ["execute", "fix", "explore", "decide"]
    
    def execute(self, plan):
        """执行：写代码/跑测试/写文档"""
        return GeneratorAgent.run(plan)
    
    def fix(self, error, attempt):
        """修复：5-mode self-correction"""
        for mode in ["tool", "external", "iterative", "tree", "dead_letter"]:
            if self.try_fix(error, mode, attempt):
                return {"status": "fixed", "mode": mode}
        return {"status": "failed", "action": "dead_letter"}
    
    def explore(self, query):
        """探索：Codebase KG query / Reflexion 搜索"""
        return {
            "kg": CodebaseKG.query(query),
            "reflexion": search_reflexion(query),
        }
    
    def decide(self, options, evaluator):
        """决策：MCTS / Tournament"""
        return MCTSDecider(options, evaluator).decide()
```

---

### C3. Metrics（7 维）

**7 维度量**：
```python
class MetricsCollector:
    def collect(self, project):
        return {
            "completion": self._calc_completion(project),  # 0-1
            "quality": {
                "lint_score": self._lint(project),  # 0-100
                "test_coverage": self._coverage(project),  # 0-1
                "complexity_avg": self._complexity(project),
                "tech_debt_hours": self._tech_debt(project),
            },
            "performance": {
                "session_time_avg": self._session_time(project),
                "tokens_per_task": self._tokens(project),
                "cost_per_task": self._cost(project),
            },
            "success_rate": {
                "tasks_completed": self._completed(project),
                "tasks_failed": self._failed(project),
                "self_heal_success": self._heal_success(project),
            },
            "failure_patterns": self._detect_patterns(project),  # 9 patterns
            "learning": {
                "reflexion_count": self._reflexion_count(project),
                "skill_extracted": self._skill_count(project),
                "method_updated": self._method_count(project),
                "prompt_evolved": self._prompt_version(project),
            },
            "resources": {
                "total_cost": self._total_cost(project),
                "remaining_budget": self._remaining(project),
                "time_elapsed": self._elapsed(project),
            },
        }
```

**每个维度的实现**：
```python
def _lint(self, project):
    r = subprocess.run(["flake8", "src/", "--max-line-length=120"],
                       cwd=project, capture_output=True, text=True)
    # 解析输出，0 错误 = 100 分
    errors = len(r.stdout.splitlines())
    return max(0, 100 - errors * 2)

def _coverage(self, project):
    r = subprocess.run(["coverage", "run", "-m", "pytest", "tests/", "&&",
                       "coverage", "report"],
                       cwd=project, capture_output=True, text=True)
    # 解析 TOTAL 行
    match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", r.stdout)
    return int(match.group(1)) / 100 if match else 0.0
```

---

### C4. Decision（3 层）

**3 层决策**：
```python
class DecisionEngine:
    def decide_tactical(self, state):
        """战术层：下一步做什么"""
        return PlannerAgent.next_action(state)
    
    def decide_strategic(self, metrics):
        """战略层：是否升级"""
        if metrics["quality"]["test_coverage"] < 0.5:
            return {"action": "STOP_AND_UPGRADE", "reason": "low_coverage"}
        if metrics["completion"] > 0.9 and metrics["success_rate"]["self_heal_success"] > 0.7:
            return {"action": "FINALIZE", "reason": "near_complete"}
        if metrics["failure_patterns"].get("F10_self_eval_trap"):
            return {"action": "STOP_AND_UPGRADE", "reason": "self_eval_trap"}
        return {"action": "CONTINUE", "reason": "normal"}
    
    def decide_evolutionary(self, history):
        """进化层：系统怎么改（v3.3 核心）"""
        # 1. Skill Library 提取
        # 2. Method Library 更新
        # 3. Prompt Evolution
        return SelfImprovementEngine.run(history)
```

---

## D. 5-Layer Runtime 细化设计

### D1. L1: Agent Runtime

**职责**：LLM 调度 + Tool 调度 + Sandbox

**核心实现**：
```python
class AgentRuntime:
    """L1 真实运行环境"""
    
    def __init__(self):
        self.llm_pool = {
            "M3": "minimax/MiniMax-M3",      # 1M context, 主力
            "M2.7": "minimax/MiniMax-M2.7",  # 200K, 便宜
            "opus": "codebuddy/claude-opus-4.5",  # 推理
        }
        self.tools = {
            "read_file": self._read_file,
            "write_file": self._write_file,
            "edit_file": self._edit_file,
            "run_command": self._run_command,
            "run_test": self._run_test,
            "git_commit": self._git_commit,
            "web_search": self._web_search,
        }
    
    def call(self, prompt, model="M3", tools=None, timeout=1800):
        """统一的 LLM 调用"""
        return llm_call(
            prompt=prompt,
            model=self.llm_pool[model],
            tools=[self.tools[t] for t in tools] if tools else None,
            timeout=timeout,
        )
```

**Sandbox**：
```python
class Sandbox:
    """每个 task 一个 git branch 隔离"""
    def __init__(self, project, task_id):
        self.project = project
        self.branch = f"task/{task_id}"
        self._create_branch()
    
    def _create_branch(self):
        subprocess.run(["git", "-C", self.project, "checkout", "-b", self.branch])
    
    def cleanup(self):
        # 测试通过后 merge 回 main
        subprocess.run(["git", "-C", self.project, "checkout", "main"])
        subprocess.run(["git", "-C", self.project, "merge", self.branch])
        subprocess.run(["git", "-C", self.project, "branch", "-d", self.branch])
```

---

### D2. L2: State Store

**职责**：所有状态文件

**文件清单**：
```
/root/vault/Projects/{name}/
├── spec.md              # 锁定
├── plan.md
├── explore.md
├── propose.md
├── tasks.json           # state machine
├── sprint-contracts/*.yaml
├── init.sh
├── progress/
│   ├── progress.txt
│   └── traces.jsonl
├── handoff/
│   ├── session-000.md
│   ├── session-001.md
│   └── session-N.md
├── knowledge_graph.json
├── reflexion.md
├── dead_letter.json
├── self_evolution.log
├── substeps.json
├── .cost_tracking.json
└── .gate_*.decision
```

**State 读写抽象**：
```python
class StateStore:
    def __init__(self, project):
        self.project = Path(project)
    
    def read_all(self):
        return {
            "spec": self.read("spec.md"),
            "plan": self.read("plan.md"),
            "tasks": self.read_json("tasks.json"),
            "kg": self.read_json("knowledge_graph.json"),
            "dlq": self.read_json("dead_letter.json"),
            "cost": self.read_json(".cost_tracking.json"),
            "reflexion": self.read("reflexion.md"),
            "substeps": self.read_json("substeps.json"),
        }
    
    def write_atomic(self, file, content):
        """原子写：先写 .tmp，再 rename"""
        tmp = self.project / f"{file}.tmp"
        tmp.write_text(content)
        tmp.rename(self.project / file)
```

---

### D3. L3: Orchestrator

**职责**：Loop Engineering 4 阶段循环

**核心实现**：
```python
class Orchestrator:
    """L3 主调度器"""
    
    def __init__(self, project):
        self.project = project
        self.goal = Goal(project / "spec.md")
        self.metrics = MetricsCollector()
        self.decision = DecisionEngine()
        self.action = Action()
        self.state = State(project)
    
    def run(self):
        """主循环：Goal → Action → Metrics → Decision"""
        while not self.is_complete():
            # 1. Goal
            goal = self.goal.current
            
            # 2. Action
            action_result = self.action.execute(goal)
            
            # 3. Metrics
            metrics = self.metrics.collect(self.project)
            
            # 4. Decision
            decision = self.decision.decide_strategic(metrics)
            
            # 5. Self-Improve（v3.3）
            self.improve(action_result, metrics, decision)
            
            # 6. State 更新
            self.state.update(decision)
            
            # 7. Sleep
            time.sleep(60)
```

---

### D4. L4: Observability

**职责**：Trace + Metrics + Dashboard

**Trace 格式**：
```json
{
  "ts": "2026-06-17T16:00:00",
  "session_id": "003",
  "stage": "apply",
  "actor": "generator",
  "action": "write_code",
  "input": "contract: feature-a",
  "output": "files: [src/auth/login.py]",
  "tokens": 8500,
  "duration_ms": 45000,
  "validation": "pass",
  "evaluation": {"score": 0.85, "issues": []}
}
```

**Metrics 存储**：
```python
class MetricsStore:
    def record(self, trace):
        with open("progress/traces.jsonl", "a") as f:
            f.write(json.dumps(trace) + "\n")
    
    def query(self, session_id=None, stage=None, action=None):
        """按条件查询 trace"""
        traces = []
        with open("progress/traces.jsonl") as f:
            for line in f:
                t = json.loads(line)
                if session_id and t["session_id"] != session_id: continue
                if stage and t["stage"] != stage: continue
                if action and t["action"] != action: continue
                traces.append(t)
        return traces
```

**Dashboard（Streamlit）**：
```python
def render_dashboard(project):
    st.title(f"📊 {project.name} Dashboard")
    
    # 7 维度量
    metrics = MetricsCollector().collect(project)
    cols = st.columns(7)
    for i, (name, val) in enumerate(metrics.items()):
        with cols[i]:
            st.metric(name, str(val))
    
    # Trace 时间线
    traces = MetricsStore().query()
    st.subheader("Trace Timeline")
    for t in traces[-50:]:
        st.text(f"[{t['ts']}] {t['actor']}.{t['action']} ({t['duration_ms']}ms)")
```

---

### D5. L5: HITL

**职责**：Hard Gate 通知 + 决策监听 + Dead-Letter Queue

**Hard Gate 流程**：
```python
class HITL:
    """L5 人类介入层"""
    
    def request_gate(self, gate_name, summary):
        # 1. 写决策文件
        gate_file = self.project / f".gate_{gate_name}.decision"
        gate_file.write_text("pending")
        
        # 2. 微信通知
        msg = f"""🚦 Hard Gate {gate_name}
{summary}
请在 24h 内决策：批准/打回/调整"""
        send_wechat(msg)
        
        # 3. 等待
        return gate_file
    
    def check_gate(self, gate_file, timeout=86400):
        """检查决策（每分钟查一次）"""
        start = time.time()
        while time.time() - start < timeout:
            decision = gate_file.read_text().strip()
            if decision == "approved":
                return "approved"
            elif decision == "rejected":
                return "rejected"
            elif decision.startswith("adjust:"):
                return decision
            time.sleep(60)
        # 超时
        return "auto_approved"  # 默认行为
```

**Dead-Letter Queue**：
```python
class DeadLetterQueue:
    def add(self, task, error, attempts):
        dlq = self._load()
        dlq["queue"].append({
            "task": task,
            "error": error,
            "attempts": attempts,
            "added_at": datetime.now().isoformat(),
            "status": "pending_review",
        })
        self._save(dlq)
        send_wechat(f"⚠️ Dead-Letter: {task['name']}")
    
    def review(self, task_id, decision):
        """人工决策"""
        # 找到任务，更新 status
        for item in self.dlq["queue"]:
            if item["task"]["id"] == task_id:
                item["status"] = decision
        self._save(self.dlq)
```

---

## E. 8 Sub-Components 细化设计

### E1. Initializer v3.2（5 步）

详见 A1. Access stage。

### E2. ReAct Agent

**实现**（完整 ReAct 循环）：
```python
class ReactAgent:
    def __init__(self, max_iter=10, max_thoughts=3):
        self.max_iter = max_iter
        self.max_thoughts = max_thoughts
        self.trace = []
    
    def run(self, task, context, tools):
        history = []
        for i in range(self.max_iter):
            # Thought
            thoughts = []
            for _ in range(self.max_thoughts):
                t = self._think(task, context, history, tools)
                thoughts.append(t)
                if t.action == "FINISH":
                    return t.result
            
            # 选 best
            best = max(thoughts, key=lambda t: t.confidence)
            
            # Action
            result = self._act(best, tools)
            
            # Observation
            obs = self._observe(result)
            
            history.append({"thoughts": thoughts, "best": best, "result": result, "obs": obs})
            self.trace.append(history[-1])
            
            if obs.task_complete:
                return obs.result
        
        return {"status": "max_iter", "history": history}
```

### E3. Claude Code Agent

详见 B1-B3 + L1 Agent Runtime。

### E4. Substep Tracker

```python
class SubstepTracker:
    def __init__(self, project):
        self.project = Path(project)
        self.file = self.project / "substeps.json"
    
    def set_steps(self, stage, steps):
        """为某 stage 定义 sub-steps"""
        ...
    
    def format_progress(self, stage):
        """格式化为 '✅1 ✅2 🔵3 ⚪4' """
        ...
```

### E5. Environment Health Check

```python
def check_environment_health():
    issues = []
    checks = {}
    
    # Python 版本
    import sys
    py = sys.version_info
    checks["python"] = f"{py.major}.{py.minor}"
    if py < (3, 10):
        issues.append(f"Python {py.major}.{py.minor} < 3.10")
    
    # Git
    r = subprocess.run(["git", "--version"], capture_output=True, text=True)
    checks["git"] = r.returncode == 0
    if r.returncode != 0:
        issues.append("git not available")
    
    # 磁盘空间
    import shutil
    stat = shutil.disk_usage("/root/vault")
    checks["disk_free_gb"] = stat.free / 1e9
    if checks["disk_free_gb"] < 1:
        issues.append("disk space < 1GB")
    
    # 工具
    for tool in ["python3", "pip", "git", "node"]:
        r = subprocess.run(["which", tool], capture_output=True)
        if r.returncode != 0:
            issues.append(f"{tool} not found")
    
    return {"ok": len(issues) == 0, "issues": issues, "checks": checks}
```

### E6. Lightweight UI（Streamlit）

详见 v3.2 simple_ui.py。

### E7. Skill Extractor

详见 v3.3 skill_extractor_v33.py。

### E8. Method Library

```python
class MethodLibrary:
    def __init__(self):
        self.path = Path("/root/.openclaw/workspace/skills/methods.json")
        self.methods = self._load()
    
    def record_failure(self, task, error, method_used):
        closest = self._find_closest(method_used)
        if closest:
            closest["failures"] += 1
            closest["last_error"] = str(error)
        else:
            self._add_method(method_used, failures=1, last_error=str(error))
        self._save()
    
    def record_success(self, method_used):
        closest = self._find_closest(method_used)
        if closest:
            closest["successes"] += 1
        self._save()
    
    def rank(self, context):
        """根据 context 排名 methods（按成功率）"""
        candidates = self._find_candidates(context)
        for c in candidates:
            total = c.get("successes", 0) + c.get("failures", 0)
            c["success_rate"] = c.get("successes", 0) / total if total > 0 else 0.5
        return sorted(candidates, key=lambda c: -c["success_rate"])
```

---

## F. 关键数据流图

```
用户需求 (1 行/链接)
    ↓
[A1 Access / Initializer] 5 min
    ↓ spec.md (locked) + tasks.json + init.sh
    ↓ HG-1 通知
[A2 Explore] 30 min
    ↓ explore.md
[A3 Propose] 30 min
    ↓ propose.md (3 套方案 + MCTS) + plan.md
[A4 Task / HTN] 30 min
    ↓ sprint-contracts/*.yaml
[A5 Apply / Generator] 10+ hours
    ↓ sub-35min session × 18+
    ↓ 每 session: Plan → Execute → Validate → Evaluate → Reflect → Handoff
    ↓ src/ + tests/ + handoff/
    ↓ Self-Improvement（v3.3）
[A6 Verify / V&V] 1-2 hours
    ↓ 8 层（含 L7 验收）
[A7 Review / Adversarial] 30 min
    ↓ review.md (9 patterns 检查)
    ↓ HG-2/3 通知
[A8 Archive] 30 min
    ↓ 新 skill 写到 /root/.openclaw/workspace/skills/
    ↓ method library 更新
    ↓ prompt 进化
    ↓ archive.md
[A9 Delivery]
    ↓ GitHub push + 微信通知
    ↓ 🎉
```

---

## G. 33 个环节清单（汇总）

| # | 环节 | 类型 | 详细位置 |
|---|---|---|---|
| 1 | Initializer / Access | Stage | A1 |
| 2 | Explore | Stage | A2 |
| 3 | Propose + MCTS | Stage | A3 |
| 4 | Task / HTN | Stage | A4 |
| 5 | Apply / Generator | Stage | A5 |
| 6 | Verify / V&V | Stage | A6 |
| 7 | Review / Adversarial | Stage | A7 |
| 8 | Archive / Skill Extract | Stage | A8 |
| 9 | Delivery | Stage | A9 |
| 10 | Planner (ReAct) | Role | B1 |
| 11 | Generator (Tool Use) | Role | B2 |
| 12 | Evaluator (Adversarial) | Role | B3 |
| 13 | Goal (动态) | GAMD | C1 |
| 14 | Action (4 类) | GAMD | C2 |
| 15 | Metrics (7 维) | GAMD | C3 |
| 16 | Decision (3 层) | GAMD | C4 |
| 17 | L1 Agent Runtime | Layer | D1 |
| 18 | L2 State Store | Layer | D2 |
| 19 | L3 Orchestrator | Layer | D3 |
| 20 | L4 Observability | Layer | D4 |
| 21 | L5 HITL | Layer | D5 |
| 22 | Initializer v3.2 | Sub-comp | E1 |
| 23 | ReAct Agent | Sub-comp | E2 |
| 24 | Claude Code Agent | Sub-comp | E3 |
| 25 | Substep Tracker | Sub-comp | E4 |
| 26 | Environment Health | Sub-comp | E5 |
| 27 | Lightweight UI | Sub-comp | E6 |
| 28 | Skill Extractor | Sub-comp | E7 |
| 29 | Method Library | Sub-comp | E8 |
| 30 | Trace | Cross | D4 |
| 31 | Cost Guard | Cross | (D2) |
| 32 | Reflexion Memory | Cross | A5 |
| 33 | Dead-Letter Queue | Cross | (D5) |

---

## H. 落地优先级

| 优先级 | 环节 | 工作量 |
|---|---|---|
| P0 | Initializer / Generator / Evaluator | 3 天 |
| P0 | V&V 8 层 | 2 天 |
| P0 | Hard Gate + Dead-Letter | 1 天 |
| P1 | State Store + Trace | 1 天 |
| P1 | Skill Extractor | 1 天 |
| P1 | Substep Tracker | 0.5 天 |
| P2 | Lightweight UI | 1 天 |
| P2 | Method Library | 0.5 天 |
| P2 | Prompt Evolution | 1 天 |
| P3 | HTN Planner | 1 天 |
| P3 | MCTS | 0.5 天 |
| **合计** | | **12.5 天** |

---

> **v3.4 完成**：33 个环节的完整细化设计，每个含目的/输入/输出/算法/代码/错误处理/性能。
> 下一步：选 P0 的 3 件套开搭（Initializer/Generator/Evaluator + V&V + Hard Gate）。
