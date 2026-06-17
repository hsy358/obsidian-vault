---
title: "YX AI Delivery Harness 对照分析 + Self-Driving R&D 方案 v2.1"
author: "OpenClaw 小助"
publish_date: "2026-06-17"
saved_date: "2026-06-17"
type: research-report
okf_metadata:
  schema: okf-v0.1-inspired
  version: 2.1
  supersedes: 2026-06-17 AI-Native R&D 自驱动闭环 v2.0
  input_image: yx-ai-delivery-harness-dashboard.jpg
status: implementable
---

# YX AI Delivery Harness 对照分析 + v2.1 升级

> **背景**：何大人分享了 YX AI Delivery Harness 的 dashboard 截图（已存档）
> **目的**：把这套已落地的 8 阶段命名 + 评分 + 门禁机制吸收进我们的方案

---

## 一、YX Harness 的 8 阶段（来自截图）

| # | 中文 | 英文 | 截图状态 | 得分 |
|---|---|---|---|---|
| 1 | 接入 | Access / Ingestion | ✅ 已完成 | 92 |
| 2 | 探索 | Explore / Discovery | ✅ 已完成 | 88 |
| 3 | 提案 | Propose / Proposal | ✅ 已完成 | 85 |
| 4 | 任务 | Task / Assignment | ✅ 已完成 | 82 |
| 5 | 应用 | Apply / Deployment | ✅ 已完成 | - |
| 6 | 验证 | Verify / Validation | 🔵 **执行中** | - |
| 7 | 评审 | Review | ⚪ 待处理 | - |
| 8 | 归档 | Archive | ⚪ 待处理 | - |

**核心特征**（截图观察）：
- 每阶段有 AI 自评得分（92/88/85/82）
- 进度轨道可视化
- 4 个状态色：✅绿（完成）/ 🔵蓝（执行）/ 🔴红（失败）/ ⚪灰（待处理）
- 过程面板双栏：左 = Agent 工作台 / 右 = 决策 Agent
- 门禁（Gate）机制 + 人工 PASS 按钮
- 实时指标：过程日志 / Claude 调用 / Agent 研判 / 思考轮次

---

## 二、命名对照：我的 v2.0 → YX Harness v2.1

| v2.0（7 阶段）| v2.1（8 阶段对齐 YX）| 改进点 |
|---|---|---|
| 需求 / 立项 | **接入**（Access）| 简化（只做"接进来"）|
| - | **探索**（Explore）| 新增（AI 自动调研/可行性）|
| 架构 / 设计 | **提案**（Propose）| 改"提案"更准确（包含方案）|
| - | **任务**（Task）| 新增（任务分解步骤）|
| 编码 + 部署 | **应用**（Apply）| 合并（编码即应用）|
| 测试 / QA | **验证**（Verify）| 改"验证"（不只测试）|
| - | **评审**（Review）| 新增（AI 自评 + 人工评审）|
| 复盘 / 沉淀 | **归档**（Archive）| 改"归档"（含沉淀）|

**改进逻辑**：
- 拆"任务"从"提案"出来（先提案，再拆任务）← 更符合 V 模型
- 拆"评审"从"验证"出来（先 AI 验，再人评）← Hard Gate 显式化
- 拆"探索"从"接入"出来（先接进来，再探索）← 与 Nx 阶段一致

---

## 三、关键技术吸收

### 3.1 阶段自评得分（新增）

**每阶段 AI 自动打分 0-100**，存到 `tasks.json.stages.{stage}.score`：

```json
{
  "stages": {
    "access":  {"status": "completed", "score": 92, "completed_at": "..."},
    "explore": {"status": "completed", "score": 88, "completed_at": "..."},
    "propose": {"status": "completed", "score": 85, "completed_at": "..."},
    "task":    {"status": "completed", "score": 82, "completed_at": "..."}
  }
}
```

**评分规则**（每个 stage 不同）：

| 阶段 | 评分维度 |
|---|---|
| access | 输入清晰度 / 验收标准 / 风险覆盖 |
| explore | 调研覆盖度 / 竞品对比 / 可行性 |
| propose | 方案数量 / 选型理由 / 风险缓解 |
| task | 任务颗粒度 / 依赖清晰 / 可并行度 |
| apply | 单测覆盖 / 编译通过 / lint |
| verify | 集成测试 / 性能 / 安全 |
| review | AI 自评 / 文档完整 / 演示 |
| archive | lessons 沉淀 / vault 更新 / 复用度 |

**门禁阈值**：阶段得分 < 70 → 自动 Self-Heal → 仍 < 70 → 升级 Hard Gate

### 3.2 决策 Agent（独立概念）

**YX Harness 把"环境检查"独立成 Decision Agent**。这是个聪明设计：

```python
class DecisionAgent:
    """独立的决策者，不参与执行，只做判断"""
    def check_environment(self):
        """环境检查：python/node/git/依赖"""
        return {"python": "ok", "deps": "ok", ...}
    
    def check_quality(self, artifacts):
        """质量门禁：代码/测试/文档"""
        return {"passes": 0, "blocks": 0, "warnings": 0}
    
    def decide_gate(self, stage, score):
        """门禁决策"""
        if score >= 80: return "PASS"
        if score >= 70: return "PASS_WITH_WARNING"
        return "BLOCK"
```

**vs 我的 v2.0 决策分散在 subagent 里** → YX Harness 把"判断"和"执行"分离，**更清晰**。

### 3.3 双栏过程面板

YX Harness 底部双栏结构：

```
┌──────────────────────────┬──────────────────────────┐
│  验证门禁                │  决策 Agent              │
│  ├─ 过程日志: 3         │  ├─ 环境检查             │
│  ├─ Claude 调用: 1     │  ├─ 检查项               │
│  ├─ Agent 研判: 0     │  ├─ 裁决摘要             │
│  └─ 思考轮次: 0        │  └─ PASS/BLOCK 决策      │
│  [临时 Agent 工作台]     │  [人工 PASS 按钮]        │
└──────────────────────────┴──────────────────────────┘
```

**v2.0 升级**：我们的 orchestrator 应该输出**双栏视图**到 vault（不只是文字报告）。

### 3.4 ReAct 编排（工作台状态）

截图显示工作台状态 "**ReAct 编排中**" — 这就是 Anthropic 提的 **Reasoning + Acting 循环**：

```python
# ReAct 模式 subagent
while not done:
    # 1. Reason（思考下一步）
    thought = llm("基于当前状态，下一步应该...")
    # 2. Act（执行动作）
    result = execute(thought.action)
    # 3. Observe（观察结果）
    state.update(result)
```

**v2.0 升级**：每个 subagent 内部应该是 ReAct 循环，不是一次性 LLM 调用。

---

## 四、升级后的 8 阶段协议（v2.1）

### 4.1 `tasks.json` v2.1 Schema

```json
{
  "project": "my-tool",
  "version": "2.1",
  "created": "2026-06-17T14:00:00",
  "current_stage": "verify",
  "stages": {
    "access":  {"status": "completed", "score": 92, "agent": "initializer", "completed_at": "..."},
    "explore": {"status": "completed", "score": 88, "agent": "explore-agent"},
    "propose": {"status": "completed", "score": 85, "agent": "propose-agent"},
    "task":    {"status": "completed", "score": 82, "agent": "task-agent"},
    "apply":   {"status": "completed", "score": 0,   "agent": "apply-agent"},
    "verify":  {"status": "in_progress", "score": 0, "agent": "verify-agent", "started_at": "..."},
    "review":  {"status": "pending"},
    "archive": {"status": "pending"}
  },
  "metrics": {
    "process_logs": 3,
    "claude_calls": 1,
    "agent_judgments": 0,
    "think_rounds": 0,
    "gate_decisions": {"pass": 0, "block": 0, "warn": 0}
  },
  "tasks": [...],
  "hard_gates": ["spec_done_approved"]
}
```

### 4.2 8 阶段 Agent 协议

| 阶段 | Agent 名称 | 输入 | 输出 | 评分 |
|---|---|---|---|---|
| 接入 (Access) | initializer-agent | 用户需求 | spec.md | 验收标准 + 风险 |
| 探索 (Explore) | explore-agent | spec.md | explore.md（调研/可行性）| 覆盖度 + 竞品 |
| 提案 (Propose) | propose-agent | spec + explore | propose.md（方案）| 数量 + 选型 |
| 任务 (Task) | task-agent | propose.md | tasks.json（细粒度任务）| 颗粒度 + 依赖 |
| 应用 (Apply) | apply-agent | tasks.json | src/ + tests/ | 覆盖 + 编译 |
| 验证 (Verify) | verify-agent | src/ | verify.md | 集成 + 性能 |
| 评审 (Review) | review-agent | verify.md | review.md（AI 自评）| 自评 + 文档 |
| 归档 (Archive) | archive-agent | review.md | lessons.md + vault 更新 | 沉淀 + 复用 |

### 4.3 3 个 Hard Gate 位置（重新设计）

| Gate | 触发 | 决策内容 | 超时行为 |
|---|---|---|---|
| **HG-1** | 接入阶段完成 | SPEC 确认 | 自动通过（继续）|
| **HG-2** | 任务阶段完成 | 任务拆解确认 | 自动通过 |
| **HG-3** | 验证阶段完成 | 最终验收 | **不通过则不交付** |

### 4.4 评分机制（新增）

```python
def score_stage(stage, artifacts):
    """每个 stage 完成后 AI 自评"""
    prompt = f"""
    你刚完成 stage: {stage}
    artifacts: {artifacts}
    
    按以下维度评分 (0-100):
    - 完整性 (30%)
    - 准确性 (30%)
    - 可执行性 (20%)
    - 文档/可读性 (20%)
    
    输出: {{"score": 85, "issues": [...], "improvements": [...]}}
    """
    return llm(prompt)
```

---

## 五、技术架构升级（v2.1）

### 5.1 新增组件

| 组件 | 用途 | 实现 |
|---|---|---|
| **Decision Agent** | 独立门禁决策 | 独立 subagent |
| **Stage Scorer** | 每阶段 AI 自评 | LLM 调用 |
| **ReAct Loop** | subagent 内部循环 | 改造现有 |
| **Metrics Collector** | 过程指标 | orchestrator 集成 |
| **Gate Watcher** | Hard Gate 监听 | 微信回复解析 |

### 5.2 保留的 v2.0 能力

- ✅ Initializer + Coding Agent 双层（Anthropic 模式）
- ✅ progress.txt 跨 session 续跑
- ✅ Self-Heal Loop（CI 失败自动修）
- ✅ Cost Guard
- ✅ 3 Hard Gate

### 5.3 v2.1 新增的 orchestrator 改造

```python
# 新版主循环关键改动
def run_stage_v21(stage, agent_type, task):
    # 1. 派 subagent
    rc, out, err = spawn(agent_type, task)
    if rc != 0: return False
    
    # 2. AI 自评（新增）
    score = score_stage(stage, artifacts=out)
    log(f"Stage {stage} score: {score['score']}")
    
    # 3. Decision Agent 门禁（新增）
    gate_decision = decision_agent.check(stage, score, artifacts)
    log(f"Gate decision: {gate_decision}")
    
    # 4. 记录 metrics（新增）
    metrics.add(stage, claude_calls=1, judgments=1)
    
    # 5. 写 tasks.json
    tasks["stages"][stage].update({
        "status": "completed",
        "score": score["score"],
        "gate_decision": gate_decision
    })
    write_tasks(tasks)
    
    # 6. Hard Gate 检查
    if stage in HARD_GATE_STAGES:
        hard_gate_notify(stage, summary)
    
    return True
```

---

## 六、与 YX Harness 的差异（我们做轻量版）

| 维度 | YX Harness | 我们的 v2.1 |
|---|---|---|
| **形式** | Web Dashboard | 文本 + cron + 微信 |
| **可视化** | 完整 UI（轨道/进度/双栏）| 简化为 progress.txt + 微信 |
| **评分** | AI 自评 0-100 | AI 自评 0-100（一致）|
| **门禁** | 决策 Agent + 人工 PASS | 微信通知 + 文件决策 |
| **部署** | 需 Web 服务 | OpenClaw cron + skill 即可 |
| **成本** | 需要部署 web 服务 | 复用现有 OpenClaw |
| **落地** | 1-2 周 | 1-2 天 |

**关键差异**：YX Harness 是产品形态（带 UI），我们是**工程形态**（带 skill + cron）。功能等价，但形态不同。

---

## 七、立即落地（v2.1）

### 7.1 1-2 天可启动

| 步骤 | 工作量 | 产出 |
|---|---|---|
| 改 orchestrator.py → 8 阶段 | 2h | 8 阶段主循环 |
| 加 stage_scorer.py | 1h | AI 自评 |
| 加 decision_agent.py | 1h | 门禁决策 |
| 加 metrics_collector | 0.5h | 指标 |
| 更新 SKILL.md | 0.5h | 8 阶段协议 |
| 跑第 1 个真实项目 | 1 天 | 端到端验证 |

### 7.2 第 1 个项目建议

**推荐**：把 v2.0 → v2.1 的升级**作为第一个项目**，让 AI 自己跑 8 阶段升级 orchestrator，验证完整流程。

**这样形成元循环**：
- 跑 v2.1 → 完成 v2.1 升级（meta）
- AI 升级自己 → 跑 v2.2
- 持续自我进化

---

## 八、给何大人的判断

### 8.1 关键洞察

1. **YX Harness 的 8 阶段命名比我们更精准** → 直接吸收
2. **每阶段 AI 自评得分** → 我们之前没做，是 YX 的强项 → 加上
3. **Decision Agent 独立** → 借鉴（解耦判断与执行）
4. **ReAct 编排** → subagent 内部应该 ReAct，不是单次 LLM

### 8.2 v2.0 vs v2.1

| 项 | v2.0 | v2.1 |
|---|---|---|
| 阶段数 | 7 | **8**（吸收 YX）|
| 评分 | 无 | **每阶段 0-100** |
| 决策 | 分散 | **独立 Decision Agent** |
| subagent | 一次性 | **ReAct 循环** |
| 落地 | 5 天 | **2 天**（改造而非新建）|

### 8.3 关键问题

> **"YX Harness 是不是我要竞争的产品？"**

不是 — 它是**已落地的产品形态**，我们的 **self-driving-rd skill 是工程实现**。两者**互补**：
- YX Harness：适合大团队（带 UI 协作）
- 我们的 v2.1：适合个人/小团队（轻量自动化）

可以**互相借鉴** — YX 的 8 阶段命名 + 评分机制 + Decision Agent → 我们 v2.1 全部吸收。

---

## 九、行动建议

### 今天（30 min 决策）

1. **确认升级 v2.1**（8 阶段 + 评分 + Decision Agent）✓
2. **选第一个项目**：v2.0 → v2.1 升级（让 AI 升级自己）
3. **选后端**：
   - 方案 A：纯 OpenClaw skill + cron（轻量）
   - 方案 B：搭简易 Web UI 模拟 YX Harness（重）

### 明天（1-2 天搭建）

4. 改 orchestrator.py → 8 阶段
5. 加 stage_scorer.py + decision_agent.py
6. 跑 v2.0→v2.1 升级项目（meta 验证）

### 长期

7. v3.0：自进化（每完成项目自动总结 → 改 skill）
8. v4.0：多项目并行

---

## 十、引用

- **图片**：`yx-ai-delivery-harness-dashboard.jpg`（已存档）
- **v2.0 方案**（基础）
- **13 篇 vault 公众号文章**（基础）
- **联网搜索 4 组**（Anthropic / Nx / Cursor 等）

---

> **一句话总结 v2.1**：
> 吸收 YX Harness 已落地的 8 阶段命名 + 阶段评分 + Decision Agent 独立 + ReAct subagent，把 v2.0 的 7 阶段升级为更精准的 8 阶段闭环。2 天可落地。
