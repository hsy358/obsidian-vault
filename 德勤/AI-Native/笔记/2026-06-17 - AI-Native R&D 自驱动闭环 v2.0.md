---
title: AI-Native R&D 自驱动闭环方案 v2.0（扔需求进去，AI 跑 10+ 小时自己闭环）
author: OpenClaw 小助
publish_date: '2026-06-17'
saved_date: '2026-06-17'
type: research-report
okf_metadata:
  schema: okf-v0.1-inspired
  version: 2.0
  supersedes: 2026-06-17 AI-Native R&D 全流程方案 v1.0
  evolution: v1.0 7 阶段人监督 → v2.0 AI 自驱动闭环
inputs:
- v1.0 方案（7 阶段 + 3 Checkpoint）
- Anthropic Effective harnesses for long-running agents
- Nx Self-Healing CI (Ralph Wiggum loops)
- Cursor long-running async agents
- Cursor building self-driving codebases
- 火山引擎 AI 研发框架（多任务并行）
status: implementable
description: 1. 确认方向 ✓（已说"扔需求进去跑 10+ 小时"） 2. 选第一个项目（建议：context-recovery v2 升级 或 PPT
  复刻 V2） 3....
timestamp: '2026-06-17T00:00:00'
tags:
- AI
- Agent
---
# AI-Native R&D 自驱动闭环方案 v2.0

> **核心目标**：扔一个需求进去，AI 跑 10+ 小时自己跑完需求 → 研发 → 测试 → 修复 → 验证 → 交付
> **人类角色**：从"驾驶"变成"乘客"——只看 3 个 Hard Gate

---

## 一、v1.0 → v2.0 关键转变

| 维度 | v1.0（7 阶段人监督）| v2.0（AI 自驱动） |
|---|---|---|
| **谁驱动流程** | 人（何大人 + 我）| **AI（Orchestrator Agent）** |
| **人类介入点** | 3 Checkpoint | **3 Hard Gate（更少）** |
| **运行时间** | 几小时-几天 | **10+ 小时不间断** |
| **上下文管理** | 单 session | **跨 session 持久化** |
| **失败处理** | 人判断 | **Self-Healing 自动修复** |
| **完成判断** | 人确认 | **Auto-Verification 自动通过** |
| **适合场景** | 中小项目 | **中大项目 / 紧急迭代** |

---

## 二、v2.0 核心架构（基于 Anthropic 长跑 agent 模型）

### 2.1 整体流程

```
┌─────────────────────────────────────────────────────┐
│ L0  人类扔需求（1 行字 / 1 个链接 / 1 段语音）        │
│      ↓                                               │
│ L1  Initializer Agent（一次性 5 min）               │
│      → 解析需求 → 写 SPEC → 设环境 → 初始 git       │
│      ↓                                               │
│ L2  Orchestrator Agent（10+ 小时 主循环）            │
│      → 跨 session 调度 → 维护 progress.txt          │
│      ↓                                               │
│ L3  Subagent Fleet（按需并行）                       │
│      ├─ Spec Agent（写规格）                         │
│      ├─ Architecture Agent（架构）                   │
│      ├─ Coding Agents（多模块并行）                  │
│      ├─ Test Agent（测试）                          │
│      ├─ Self-Heal Agent（自愈）                      │
│      └─ Verify Agent（验收）                        │
│      ↓                                               │
│ L4  Hard Gate Review（何大人 3 次介入）              │
│      ├─ Gate 1: SPEC 确认（10 min）                 │
│      ├─ Gate 2: 中期状态检查（5 min，可选）         │
│      └─ Gate 3: 最终交付验收（20 min）              │
│      ↓                                               │
│ L5  交付 → 知识回灌 → 下一轮                        │
└─────────────────────────────────────────────────────┘
```

### 2.2 跨 session 持久化（关键创新）

**Anthropic 模式**：每个 session 留 artifacts，下一个 session 接续。

```
项目目录/
├── .claude-progress.txt        # 主进度日志（每个 session 都写）
├── .claude-decisions.md        # 关键决策记录
├── .claude-blockers.md         # 阻塞问题清单
├── .claude-lessons.md          # 经验教训（即时沉淀）
├── .claude-scratch/            # 草稿区
├── init.sh                     # 初始化脚本（一键恢复环境）
├── spec.md                     # SPEC（创建时锁定）
├── plan.md                     # 计划
├── tasks.json                  # 任务状态
├── src/                        # 业务代码
├── tests/                      # 测试
├── docs/                       # 文档
└── .git/                       # 每个 session 一次 commit
```

### 2.3 主循环伪代码

```python
# Orchestrator Agent 主循环（10+ 小时）
while not all_tasks_done(tasks.json):
    # 1. 读取 progress（接续上 session）
    progress = read(".claude-progress.txt")
    
    # 2. 识别当前阶段
    current = parse_current_stage(progress)
    
    # 3. 派发 subagent
    if current == "spec":
        run_subagent("spec-agent", task=next_task)
    elif current == "arch":
        run_subagent("arch-agent", tournament=True)  # 锦标赛
    elif current == "code":
        run_subagents("code-agent", parallel=current_tasks)
    elif current == "test":
        run_subagent("test-agent", adversarial=True)  # 对抗
    elif current == "heal":  # Self-Healing
        run_subagent("heal-agent", ci_log=last_ci)
    elif current == "verify":
        run_subagent("verify-agent", acceptance=spec.md)
    
    # 4. 更新 progress
    append(".claude-progress.txt", new_entry)
    
    # 5. Git commit
    git_commit(amend=False, message=f"[{stage}] {summary}")
    
    # 6. 检查 hard gate
    if stage in ["spec_done", "mid_check", "deliver"]:
        request_human_review(urgency="normal")
        wait_human_decision(timeout=24h)
    
    # 7. Cost guard（防跑飞）
    if token_used > 5_000_000 or elapsed > 12h:
        request_human_intervention(urgency="high", reason="cost/time limit")
```

---

## 三、6 大核心 Agent 设计

### Agent 1：Initializer（初始化）

**职责**：跑一次，设置一切
**输入**：用户需求（1 行 / 1 链接）
**输出**：
- `spec.md`（清晰可验收的规格）
- `init.sh`（一键环境恢复）
- `tasks.json`（任务列表）
- 初始 git commit
- 第一个 SPEC 确认 hard gate

**关键 Skill**：
- `ai-native-requirement-analysis`
- `writing-plans`

---

### Agent 2：Spec Refiner（规格精炼）

**职责**：把模糊需求转成机器可读 SPEC
**输入**：初版 SPEC
**输出**：
- `spec.md`（含 5W1H / 验收标准 / 边界）
- 用户故事 + 验收测试
- 风险清单

**技巧**：用 `/speckit.spec` 模式（SegmentFault）

---

### Agent 3：Architecture（架构）

**职责**：选型 + 架构图 + 风险评估
**输入**：SPEC
**输出**：
- `docs/architecture.md`
- 选型对比表
- 风险评估 + 缓解

**编排**：Tournament（3 套架构方案 PK 选最优）

---

### Agent 4：Coding Fleet（编码舰队）

**职责**：写代码
**输入**：架构 + 当前 task
**输出**：
- `src/` 代码
- 单元测试
- 文档

**编排**：Fan Out（多模块并行）+ Loop Until Done
**质量门**：
- 单测覆盖率 ≥ 80%
- 0 critical bug
- 通过 self-review（Adversarial Verification）

---

### Agent 5：Self-Heal（自愈）

**职责**：CI 失败时自动修复
**触发**：CI 红 → 自动启动
**输入**：CI 日志 + 错误堆栈
**输出**：修复 PR + 重跑 CI

**模式**：Nx Ralph Wiggum 循环（直到 CI 绿）
**退出条件**：
- ✅ CI 绿 → 提交 + 继续
- ⚠️ 3 次失败 → 升级到 Hard Gate
- 💰 成本超限 → 升级到 Hard Gate

---

### Agent 6：Verify（验收）

**职责**：跑 spec.md 里的验收标准
**输入**：完成代码 + spec.md
**输出**：
- 验收报告
- 演示视频（如适用）
- 部署链接

**触发**：所有 task done

---

## 四、3 个 Hard Gate 设计

### Hard Gate 1：SPEC 确认（项目启动时）

**触发**：Initializer Agent 完成 SPEC 后
**何大人看**：
- 需求理解对不对（5 min 看）
- 验收标准合理不合理（5 min 看）
- 风险接受不接受（5 min 决策）

**通过**：进入 10+ 小时主循环
**拒绝**：回到 Initializer 重写

---

### Hard Gate 2：中期检查（可省略）

**触发**：50% 任务完成时（默认关闭）
**何大人看**：
- 进度是否符合预期
- 是否需要调整方向
- 成本是否超预算

**通过**：继续
**拒绝**：调整 / 暂停 / 终止

---

### Hard Gate 3：最终交付（项目完成时）

**触发**：Verify Agent 报告全绿
**何大人看**：
- 验收测试结果
- 演示 / 截图
- 文档完整性

**通过**：交付 + 知识回灌
**拒绝**：打回 Self-Heal

---

## 五、Self-Healing 自愈机制（核心创新）

### 5.1 失败分类与处理

| 失败类型 | 例子 | 处理方式 |
|---|---|---|
| **编译错误** | 语法错 / 类型错 | Coding Agent 自修 |
| **单测失败** | 边界条件 | Coding Agent 自修 |
| **集成测试失败** | 模块接口错 | Architecture Agent 重新对齐 |
| **CI 配置错** | pipeline 挂 | Self-Heal Agent 修 |
| **依赖装不上** | 网络 / 版本 | Self-Heal Agent 重试 / 换源 |
| **API 限流** | 第三方拒绝 | 自动 backoff + 重试 |
| **3 次失败** | 持续跑挂 | **升级到 Hard Gate** |
| **成本超限** | token 爆 | **升级到 Hard Gate** |

### 5.2 自愈循环（Nx Ralph Wiggum 模式）

```python
def self_heal_loop(max_attempts=3):
    attempt = 0
    while attempt < max_attempts:
        # 1. 跑 CI
        result = run_ci()
        if result.success:
            return "OK"
        
        # 2. 分析失败
        failure = analyze(result.log)
        
        # 3. 派 Heal Agent
        fix = run_subagent("heal-agent", failure=failure)
        if not fix:
            attempt += 1
            continue
        
        # 4. 应用修复
        apply_fix(fix)
        
        # 5. 重跑 CI
        attempt += 1
    
    return "ESCALATE"  # 升级到何大人
```

### 5.3 失败回滚

- 每次修复前 `git commit` 留 checkpoint
- 3 次失败自动 `git revert` 回到上次成功状态
- 把"修复无果"状态写入 `.claude-blockers.md`

---

## 六、成本与安全护栏

### 6.1 成本护栏

| 维度 | 限制 | 触发动作 |
|---|---|---|
| **单次 session** | < 1h 或 < 500K tokens | 超限 → 自动 commit + 退出 |
| **单次项目** | < 12h 或 < 5M tokens | 超限 → Hard Gate |
| **每小时** | < $5 | 超限 → 暂停 + 通知 |
| **API 调用** | < 100/min | 超限 → backoff |

### 6.2 安全护栏

- 🚫 **金融场景不接券商 API**（永久红线）
- 🚫 **生产环境不直接部署**（必须 Hard Gate 3 通过）
- 🚫 **不删除 vault 历史文件**（OKF 知识不可丢）
- 🚫 **不覆盖 MEMORY.md 顶部**（context-recovery 必备）
- 🚫 **不发非预期的微信消息**（不主动打扰）

### 6.3 中断恢复

- 每完成一个 subagent 任务 → 立即 commit
- 每完成一个 stage → 写 progress.txt + commit
- 任何中断（断电 / API 限流 / 超时）→ 下次从 progress.txt 接续

---

## 七、立即可落地的最小可行方案（MVP）

### 7.1 1 周内可启动

| Day | 工作 | 产出 |
|---|---|---|
| 1 | 建 `self-driving-rd` Skill（SOP）| SKILL.md + 模板 |
| 1 | 建 Orchestrator Agent 雏形 | 跨 session 调度 |
| 2 | 写 `.claude-progress.txt` 协议 | 进度文件格式 |
| 2 | 写 `init.sh` 模板 | 一键环境恢复 |
| 3 | 配 Self-Heal Loop | 失败重试机制 |
| 3 | 配 3 个 Hard Gate 通知 | 微信 push |
| 4 | 配 Cost Guard | 限额 + 报警 |
| 5-7 | 跑 1 个真实项目验证 | 端到端闭环 |

### 7.2 MVP 项目选择

**建议第一个项目**：
- ✅ 范围明确（小功能，不是巨型系统）
- ✅ 验收清晰（可以写测试）
- ✅ 不接金融（避开红线）
- ✅ 跑过类似（降低风险）

**候选**：
- PPT 复刻 V2（已做过 V1）
- context-recovery v2 升级
- 新建一个工具类 Skill

### 7.3 验证指标

| 指标 | 目标 |
|---|---|
| 端到端耗时 | < 8h |
| 人类介入 | ≤ 2 次（启动 + 验收）|
| Self-Heal 成功率 | ≥ 80% |
| Token 消耗 | < 3M |
| 最终验收 | 一次通过 |

---

## 八、长期演进（3-6 个月）

### 8.1 v3.0：自进化

- 每完成项目自动总结 → 更新 Skill
- 失败案例入 LESSONS.md
- 流程自我优化（用强化学习调参）

### 8.2 v4.0：多项目并行

- 一个何大人 → 多个自驱动项目并行
- 资源调度器（多 Orchestrator 协调）
- 跨项目知识共享

### 8.3 v5.0：完全自治

- 何大人只看 Hard Gate 1（SPEC）
- 中间 2 个 Gate 也自动化（基于历史偏好学习）
- 真正实现"扔需求进去" → "早上看结果"

---

## 九、所需工具与能力清单

### 9.1 已有 ✓

- OpenClaw cron（定时触发）
- OpenClaw sessions_spawn（subagent 派发）
- sessions_yield（长跑 session）
- context-recovery skill（跨 session 记忆）
- 67 个现有 skills
- akshare / web_search / message 等工具

### 9.2 需要新建

| 工具 | 用途 | 工作量 |
|---|---|---|
| `self-driving-rd` Skill | SOP 模板 | 1 天 |
| Orchestrator Agent 模板 | 跨 session 调度 | 1 天 |
| `init.sh` 模板 | 环境恢复 | 0.5 天 |
| Self-Heal Loop 脚本 | 自动修复 | 1 天 |
| Cost Guard 监控 | 限额 + 报警 | 0.5 天 |
| 3-Hard-Gate 通知 | 微信 push | 0.5 天 |

### 9.3 需要验证

- [ ] 跨 session progress.txt 协议稳定性
- [ ] Self-Heal 修复成功率
- [ ] Cost Guard 准确性
- [ ] Hard Gate 触发合理性

---

## 十、成功度量

| 指标 | v1.0 | v2.0 目标 |
|---|---|---|
| 单项目总耗时 | 3-7 天 | **< 8h** |
| 人类介入 | 3 次 Checkpoint | **≤ 2 次 Hard Gate** |
| Self-Heal 成功率 | 0%（无）| **≥ 80%** |
| Token 效率 | 1x | **0.6x**（subagent 隔离）|
| 项目成功率 | ~70% | **≥ 90%** |
| 月项目数 | 2-3 个 | **8-10 个** |

---

## 十一、风险与护栏（升级版）

| 风险 | 概率 | 缓解 |
|---|---|---|
| 成本失控 | 中 | Cost Guard 硬限 |
| 失败循环 | 中 | 3 次升级 Hard Gate |
| 安全违规 | 低 | 红线 + 永久护栏 |
| 知识丢失 | 低 | OKF + vault + Git |
| 方向偏离 | 中 | Hard Gate 2 校准 |
| 中断无法恢复 | 低 | progress.txt + init.sh |
| 模型幻觉 | 中 | Adversarial Verification |

---

## 十二、与其他方案对比（v2.0 视角）

| 方案 | 我们差异 |
|---|---|
| v1.0（7 阶段人监督）| **人类介入从 3 → 2 次** |
| Claude Code Dynamic Workflows | 加了**跨 session 持久化** + **Self-Heal** |
| Nx Self-Healing CI | 从 CI 自愈扩展到**全流程自愈** |
| Paperclip（公司级）| **个人级**，可立即跑 |
| Cursor Async Agents | 加了**OKF 知识回灌** |

---

## 十三、行动建议（致何大人）

### 今天（30 min 决策）

1. **确认方向** ✓（已说"扔需求进去跑 10+ 小时"）
2. **选第一个项目**（建议：context-recovery v2 升级 或 PPT 复刻 V2）
3. **确认 3 Hard Gate 位置** ✓
4. **确认红线** ✓

### 明天（1 天搭建）

5. 建 `self-driving-rd` Skill（SOP 模板）
6. 写 Orchestrator Agent 雏形
7. 跑第 1 个 session 验证

### 本周（5 天闭环）

8. 跑完第 1 个端到端项目
9. 总结经验 → 更新 SOP
10. 写自驱动 R&D 实操手册（公开分享）

---

## 十四、关键引用

### 14.1 联网搜索（2026 最新）

- **Anthropic**: Effective harnesses for long-running agents
  - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
  - 核心：Initializer + Coding Agent + claude-progress.txt
- **Cursor**: Building Towards Self-Driving Codebases
  - Aman Sanger (Cursor CTO) at NVIDIA GTC, 2026-04-12
  - 核心：async agents as colleagues
- **Nx**: Autonomous AI Agent Workflows
  - https://nx.dev/blog/autonomous-ai-workflows-with-nx
  - 核心：Self-Healing CI + Ralph Wiggum loops
- **Anthropic 2026 Agentic Coding Trends Report**
  - Trend 3: Long-running agents build complete systems
- **Augment Code**: Agentic SDLC
  - 3 Checkpoints pattern

### 14.2 vault 内（升级引用）

- v1.0 方案（已存在）
- 13 篇文章（同 v1.0）
- context-recovery skill（新建，已存在）

### 14.3 已有能力

- OpenClaw 5 层上下文压缩
- agentic-stack 4 层记忆
- sessions_spawn 异步派发
- sessions_yield 长跑机制

---

> **一句话总结 v2.0**：
> 把 v1.0 的"7 阶段人监督"升级为"AI 自驱动闭环"——扔需求进去，AI 跑 10+ 小时自完成需求 → 研发 → 测试 → 自愈 → 验证。何大人只看 3 个 Hard Gate（启动 SPEC 确认 / 中期检查 / 最终验收），中间全部由 AI + Self-Heal 接力。

---

> **下一步**：
> 1. 选第一个项目（建议 PPT 复刻 V2 或 context-recovery v2）
> 2. 我建 `self-driving-rd` Skill（半天）
> 3. 写 Orchestrator Agent 雏形（半天）
> 4. 跑第 1 个 session 验证
