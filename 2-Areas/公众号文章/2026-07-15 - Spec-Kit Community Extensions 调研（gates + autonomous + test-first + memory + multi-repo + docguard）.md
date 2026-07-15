---
title: Spec-Kit Community Extensions 调研（6 个相关项目深挖）
author: 小助（实测调研）
publish_date: '2026-07-15'
saved_date: '2026-07-15'
verified_date: '2026-07-15T14:30+08:00'
verified_version: github/spec-kit @ v0.12.15 (2026-07-14)
source: github-repo-readme
description: 调研 4 个 extension（gates / docguard / multi-repo-sync / memory）+ 2 个 preset（test-first-governance / autonomous-run-governance），按"我们 vault / AgentSpace 可能用得上"程度排序。每个项目含安装命令、commands 列表、hooks 触发点、能力边界判断。
related:
- "[[2026-07-15 - Spec-Kit 规格驱动开发的 AI 工程化利器（架构茶话会）.md]]"
timestamp: '2026-07-15T14:30:00+08:00'
type: tech-article
tags:
- AI
- Agent
- Spec-Kit
- Extension
- Preset
- Quality-Gates
- TDD
- BDD
- 调研
---

# Spec-Kit Community Extensions 调研（6 个项目深挖）

> 调研对象：何大人指定的 4 个扩展（Quality Gates / DocGuard / Multi-Repo Sync / Spec Kit Memory）+ CHANGELOG 里提到的 2 个 preset（Test-First Governance / Autonomous Run Governance）
> 调研源：catalog.community.json（130+ extension）+ catalog.community.json 里的 presets 目录（25 preset）+ 各仓库 README 实读
> 目的：拿到每个的**安装命令 / commands 列表 / hooks 触发点 / 能力边界**，按相关度排序，等何大人决定要不要装

---

## 一、6 个项目速览表

| # | 项目 | 类型 | 版本 | 我们的相关度 | 主标签 |
|---|---|---|---|---|---|
| 1 | **Quality Gates (gates)** | extension | v0.1.0 | ⭐⭐⭐⭐⭐ | process / quality / hooks / ci / governance |
| 2 | **Autonomous Run Governance** | preset | v0.2.0 | ⭐⭐⭐⭐⭐ | autonomous / governance / evidence / permissions / retrospective |
| 3 | **Test-First Governance** | preset | v1.3.0 | ⭐⭐⭐⭐ | tdd / bdd / atdd / quality-gates / traceability |
| 4 | **Multi-Repo Branch Sync** | extension | v1.0.0 | ⭐⭐⭐⭐ | git / branching / multi-repo / submodules / workflow |
| 5 | **Spec Kit Memory** | extension | v0.3.0 | ⭐⭐⭐ | memory / recall / research / memsearch |
| 6 | **DocGuard — CDD Enforcement** | extension | v0.32.0 | ⭐⭐⭐ | documentation / validation / quality / cdd / traceability |

---

## 二、Tier 1：直接相关（4 个）

### 🔥 1. Quality Gates (gates) —— ⭐⭐⭐⭐⭐

> **核心定位**：**Spec Kit 是建议层（guide），gates 是强制层（enforce）**

| 维度 | 内容 |
|---|---|
| 仓库 | https://github.com/schwichtgit/spec-gates |
| 当前版本 | v0.1.0（2026-07-13 更新） |
| 兼容性 | spec-kit >= v0.12.4 |
| 提供 | 5 commands + 1 hooks |
| 安装命令 | `specify extension add --from <zip-url>` 或 `specify extension add --dev ./spec-gates` |

#### 三大边界（一个 policy，三个 verify）

```text
.specify/gates/policy.json
        |
        +----------------------+----------------------+
        |                      |                      |
  AGENT BOUNDARY         GIT BOUNDARY            CI BOUNDARY
  Claude Code hooks      pre-commit /            GitHub Actions
  PreToolUse: block      commit-msg:             Jenkins / GitLab CI
    protected files      block main commits,
  PostToolUse:           conventional commits,
    auto-format          no AI-isms
  Stop: refuse to end
    with failing checks
```

**Parity property**：agent 通过的 → git 也通过 → CI 也通过。`tests/test-parity.sh` 强制这条不变量。**第四个边界（服务端 branch protection）通过 `/speckit.gates.ci github --protect` 启用**。

#### 三个"反失效"机制（**这是最有价值的部分**）

> "Enforcement that can silently stop enforcing is worse than none — you still believe you are covered."

1. **Attestations**：每次 `verify.sh` 在 `.specify/gates/attestations.jsonl` 追加 1 条记录（含 policy SHA-256 + per-gate resolved binary + version + lockfile pin + 结果 + 时长）。**只留证据不留内容**。
2. **Canaries**：`canary.sh` 在 sandbox 故意注入已知违规（prettier-dirty 文件 / SC2086 script / `rm -rf /` 工具调用 / `.env` 编辑 / AWS-key 字符串），要求真 gate 拒收。**CI 每次跑 canary** —— canary 红了意味着 gate 坏了，不是 dirty tree。
3. **Parity drift**：每次 run 比对每个工具的 resolved version vs lockfile pin。drift = 失败。`attestation.parity = error | warning | off`。

#### acceptance criteria 变可执行

```markdown
- [x] T042 Ship the exporter

  ```accept
  # verifies: SC-003
  bash tests/test-exporter.sh
  ```
```

` ```accept ` fence 包住的 shell 脚本 = 该 task 的验收标准 = gate 真的会跑（exit 0 = 通过）。

#### 跟我 vault 已有内容的关联

| 已有 | 关联 |
|---|---|
| **Yuxi Goal-Driven Execution**（MEMORY.md 7-9） | 同款思路的工具化："verifiable goal + 失败标准比成功标准更重要" |
| **v4 推荐策略 3 条硬约束**（strategy_improvements.md） | 同款风控思维：每条规则都要立刻能验证 |
| **Vault 5-28 12 条天条** | 同类问题（防 Vibe Coding 失控）的不同解法 —— 12 条天条是"行为边界"，Quality Gates 是"强制层" |

**判断**：**这是 6 个项目里跟我们最相关的**。如果只能装一个，**先装这个**。

---

### 🔥 2. Autonomous Run Governance —— ⭐⭐⭐⭐⭐

> **核心定位**：**完整自主交付流程的治理**（不是"如何写 spec"，而是"如何让 autonomous agent 跑 SDD 而不出事"）

| 维度 | 内容 |
|---|---|
| 仓库 | https://github.com/hindermath/spec-kit-preset-autonomous-run-governance |
| 当前版本 | v0.2.0（2026-07-14 更新，**昨天发布**） |
| 兼容性 | spec-kit >= v0.8.3 |
| 提供 | 12 templates + 2 commands + 2 scripts |
| 推荐优先级 | **70**（高于 Test-First Governance 的 5） |
| 安装命令 | `specify preset add --from <zip-url> --priority 70` 或 `--dev` |

#### 5 个核心命令

| 命令 | 用途 |
|---|---|
| `speckit.autonomous` | 端到端 autonomous 交付 |
| `speckit.autonomous-status` | 只读运行状态查询 |
| `speckit.autonomous-stop` | 安全边界暂停（cooperative checkpoint） |
| `speckit.autonomous-resume` | 显式恢复（pause 或中断后） |
| `speckit.autonomous-retrospective` | 分类学习 |

#### 三大授权级别（**这是核心安全机制**）

```text
LocalImplementation  = 安全默认（无需授权）
PublishPR           = 必须显式当前授权
MergeAndSync        = 必须显式当前授权
```

**关键不变量**：
- **Never infer provider bypass** from autonomy / repo access / prior run
- **stop command is cooperative**（在下一个安全 agent/command 边界 checkpoint，**不**声称原子终止任意外部进程）
- **PausedByUser requires resume**（显式暂停 ≠ 自动恢复）
- **Unexpected interruption requires revalidation**：drift / operation / governance / authority

#### Gate evidence（机器可校验）

```bash
bash .specify/presets/autonomous-run-governance/scripts/validate-autonomous-gate-evidence.sh \
  --requirements specs/NNN-feature/autonomous-gate-requirements.json \
  --evidence /tmp/provider-gate-evidence.json \
  --head "$(git rev-parse HEAD)"
```

- 真实 git head 校验（不能伪造 evidence）
- requirements 定义 command 和可选 runner/platform tokens
- **绿色 tooling job 不能 satisfy runtime gate**（即使名字含 platform）

#### 跟我 vault 已有内容的关联

| 已有 | 关联 |
|---|---|
| **Hermes Agent 上手指南**（vault 5-11） | 同款问题：autonomous agent 跑 SDD 时如何安全治理 |
| **AgentSpace 部署 + AgentRouter**（2026-07-02 commit） | 同款需求：多 harness 的统一执行层 + 治理 |
| **OPENCLAW 安全关注**（MEMORY.md v0.14 验证段） | 这个 preset 的"never infer provider bypass"原则跟 OpenClaw 的 safety policy 直接对位 |

**判断**：**跟 Hermes / AgentSpace / OpenClaw 的 autonomous 治理完全对位**。如果要走 autonomous agent 路线，**必装**。

---

### 🔥 3. Test-First Governance —— ⭐⭐⭐⭐

> **核心定位**：把 **TDD + BDD + ATDD + traceability + risk-based quality gates** 注入到所有 SDD 阶段

| 维度 | 内容 |
|---|---|
| 仓库 | https://github.com/ka-zo/spec-kit-preset-test-first-governance |
| 当前版本 | v1.3.0（2026-07-13 更新） |
| 兼容性 | spec-kit >= v0.12.11 |
| 提供 | 10 templates + 8 commands |
| 推荐优先级 | **5**（**必须最高** —— 其他 preset 不能超过它） |
| 安装命令 | `specify preset add test-first-governance --priority 5` 或 `--from <zip>` |

#### 4 类强制测试

| 类型 | 强制范围 |
|---|---|
| **TDD** | 生产逻辑（happy path / boundary / edge case / contract / expected error） |
| **BDD** | 用户可见行为 + 业务规则 + 备选流 + 可观察错误 |
| **ATDD** | 利益相关方验收边界 |
| **Risk-based quality gates** | 覆盖 / linting / formatting / 静态分析 / 安全 / runtime smoke / 可追溯性 |

#### 推荐工作流（这是强化后的全流程）

```text
/speckit.constitution → /speckit.specify → /speckit.clarify → /speckit.plan
→ /speckit.checklist → /speckit.tasks → /speckit.analyze
→ /speckit.implement → /speckit.converge
```

**强化**：constitution / specify / plan / checklist / tasks / analyze / implement / converge
**不修改**：clarify（可选但推荐）

#### 生成的工件（specs/<feature>/ 下）

- `test-traceability.md`（需求-测试追溯）
- `defect-log.md`（缺陷追踪）
- `test-summary.md`（feature 级别测试摘要）

#### 报告默认路径

```text
rolling 模式（无 release ID） → reports/test-summary.md
release 模式（有 release ID） → reports/releases/<release-id>/test-summary.md
```

#### 跟我 vault 已有内容的关联

| 已有 | 关联 |
|---|---|
| **v4 推荐策略 -8% 止损硬规则** | 同款风控思维：硬规则 + 立刻可验证 |
| **MEMORY.md "🎯 Goal-Driven Execution"** 准则 2：Simplicity First | Test-First Governance 的 coverage-complete 原则有点相反 —— 它要求**不只最小**（"TDD inventories are coverage-complete rather than merely minimal"） |

**判断**：跟 v4 策略硬规则同款，**但 Yuxi 的 Simplicity First 准则说"不写 speculative feature"**，这里跟它有轻微张力。**按项目决定**：MVP 装它压质量；side project 用 12 条天条够。

---

### 🔥 4. Multi-Repo Branch Sync —— ⭐⭐⭐⭐

> **核心定位**：在 plan/tasks 阶段**自动创建子仓库的同名 feature branch**（git submodule / nested repo）

| 维度 | 内容 |
|---|---|
| 仓库 | https://github.com/fyloss/spec-kit-multi-repo-sync |
| 当前版本 | v1.0.0（2026-07-13 更新） |
| 兼容性 | spec-kit >= v0.2.0 |
| 提供 | 3 commands + 2 hooks |
| 安装命令 | `specify extension add --from <zip-url>` 或 `specify extension add --dev ./spec-kit-multi-repo-sync` |

#### 关键设计：**hooks 不是 replace**

| | Preset (command override) | This extension (hooks) |
|---|---|---|
| 触碰 core `plan`/`tasks` | ✅ Yes（替换） | ❌ No |
| 活过 `specify self upgrade` | ❌ 每次手动 merge | ✅ Yes，自动 |
| 继承 core 改进 | ❌ Lost | ✅ Yes |
| 命名空间 | ❌ No（污染 core） | ✅ Yes（`speckit.multi-repo-sync.*`） |

→ 这是 **README 里作者主动跟 preset 版本做的对比**（社区 preset `sakitA/spec-kit-preset-multi-repo-branching`）。**这个 extension 的方案更优雅**。

#### 工作流

```text
1. 跑原生流程：/speckit.specify → /speckit.plan → /speckit.tasks
   → core 在 root 仓库创建 feature branch
2. on after_plan  hook:  speckit.multi-repo-sync.analyze
   → 发现被影响的 sub-repo / submodule
   → 在 plan.md 写 "Affected Repositories" table
3. on after_tasks hook:  speckit.multi-repo-sync.sync
   → 读 table → 在每个 affected repo 创建同名分支
   → default: 切到新分支（best-effort，dirty tree 时只创建不切换）
   → set switch: false 改为 create-only
   → submodule 用 `git submodule update --init` 初始化
```

#### 跟我 vault 已有内容的关联

| 已有 | 关联 |
|---|---|
| **AgentSpace**（2026-07-02 部署在 `/root/AgentSpace`） | 我们的本地自托管多仓布局可能直接适用 |
| **德勤 AI-Native MVP**（vault 1-Projects/德勤/AI-Native/） | 多仓 monorepo 场景可能直接受益 —— 但按何大人 7-8 明确**不硬挂德勤** |

**判断**：**hooks 方案比 preset replace 方案优雅**，但**我们目前没有多仓 monorepo 项目急需**。**按需装**，不立即试。

---

## 三、Tier 2：可选相关（2 个）

### ⭐ 5. Spec Kit Memory —— ⭐⭐⭐

> **核心定位**：在 SDD 阶段之前**回忆之前的 spec / decision**（不是写，是 recall）

| 维度 | 内容 |
|---|---|
| 仓库 | https://github.com/zaytsevand/spec-kit-memory |
| 当前版本 | v0.3.0（2026-07-10 更新） |
| 兼容性 | spec-kit >= v0.2.0 |
| 提供 | 2 commands + 3 hooks |
| 工具依赖 | 可选 `memsearch`（不强制） |
| 安装命令 | **必须 `--dev`**（catalog install 还没配置）：`specify extension add --dev /path/to/spec-kit-memory` |

#### 3 个 hooks 触发点

| Hook | Command | Mode | 做什么 |
|---|---|---|---|
| `before_specify` | `speckit.memory.recall` | **read-only** | **Primary** —— 写 spec 前浮现 prior art |
| `before_plan` | `speckit.memory.recall` | read-only | plan 的 Phase 0 research 之前回忆 |
| `after_plan` | `speckit.memory.list-related-specs` | **writes research.md** | 写 `## Related specs (from memory)` 段 |

→ **recall 是只读的**（回忆 + 总结，不写 spec/plan/code），**唯一写入动作是给 research.md 加 Related specs 段**（idempotent，可重跑）。

#### 配置（memory-config.yml）

```yaml
memory_tools:
  - command: "memsearch:memory-recall"
    description: "Semantic recall over past sessions, specs and decisions"
stages:
  default: true
  before_specify: true
  before_plan: true
settings:
  read_only: true
  fail_open: true   # 找不到/失败也不阻塞 SDD 阶段
  max_findings: 8
```

#### 关键设计：**fail_open + read_only**

- **找不到 memory 不阻塞**（SDD 流程继续）
- **recall 永远不写**（保证实验安全）
- **memory tools 是 list**（不是硬编码某个 tool），可插拔

#### 跟我 vault 已有内容的关联

| 已有 | 关联 |
|---|---|
| **vault PARA + Datacore**（2026-06-29 AI 3.0 装） | 同款目标：把 vault 当 memory backend，让 SDD 阶段能 recall 历史 |
| **MEMORY.md + memory/YYYY-MM-DD.md** 每日笔记 | vault 本来就是项目历史库 —— 但目前没自动 recall 集成 |

**判断**：**理念跟我们 vault 的"项目历史"目标完全对位**，但**需要 memsearch 工具**（或自己造一个 vault 索引）。**不在 spec-kit 体系内实现会重复造轮子**，先看 `memsearch` 是不是能用。

---

### ⭐ 6. DocGuard — CDD Enforcement —— ⭐⭐⭐

> **核心定位**：**Canonical-Driven Development** —— 文档是真相来源，AI 写文档，DocGuard 验证

| 维度 | 内容 |
|---|---|
| 仓库 | https://github.com/raccioly/docguard |
| 当前版本 | v0.32.0（2026-07-13 更新，迭代活跃） |
| 兼容性 | spec-kit >= v0.1.0 |
| 提供 | 6 commands + 3 hooks |
| 发行版 | **4 种**：Node.js core (npm `docguard-cli`) + Python wrapper (PyPI) + GitHub Action + Spec Kit Extension (ZIP) |
| 30 秒试用 | `npx docguard-cli demo`（不需要装） |

#### 三大功能（架构图）

```text
CLI Entry (docguard.mjs) → Commands (18)
                                 |
                +----------------+----------------+----------------+
                |                |                |                |
             guard           generate          score          diagnose
                |
                +--> Validators (27) + Scanners (4) + Scoring (8 类) + Output (Terminal / JSON / Badge)
```

#### 核心能力

- **27 validators**（文档-代码一致性检查）
- **4 scanners**（routes / schemas / doc-tools / speckit）
- **8 类加权评分**（按类别权重算质量分）
- **SARIF 输出**（IDE 集成）
- **MCP server**（agent 集成）

#### 跟我 vault 已有内容的关联

| 已有 | 关联 |
|---|---|
| **vault PARA + OKF frontmatter**（2026-06-29） | vault 里已经在用 frontmatter 做文档结构化 —— DocGuard 的 validators 可能能套 |
| **MEMORY.md Yuxi Goal-Driven Execution** 准则 1：Think Before Coding | DocGuard 的"docs first"跟它同款 |

**判断**：**v0.32.0 已经迭代到很成熟**（PyPI + npm + GH Action + Spec Kit Extension 全发行版），但**不是 SDD 工作流直接依赖**，可作为**质量保证侧**独立装。

---

## 四、汇总判断（按"我们 vault / AgentSpace 可能用得上"排序）

| 优先级 | 项目 | 类别 | 何时装 |
|---|---|---|---|
| 🟢 P0 立即考虑 | **Quality Gates** | extension | 任何用 spec-kit 的项目（**最有价值**） |
| 🟢 P0 立即考虑 | **Autonomous Run Governance** | preset | 任何走 autonomous agent 的项目 |
| 🟡 P1 按项目 | **Test-First Governance** | preset | MVP / 企业级项目（side project 不需要） |
| 🟡 P1 按项目 | **Multi-Repo Branch Sync** | extension | 有 multi-repo / submodule 的项目 |
| ⚪ P2 可选 | **Spec Kit Memory** | extension | 想把 vault 当 memory backend 时 |
| ⚪ P2 可选 | **DocGuard** | extension | 想做文档-代码一致性强制时 |

---

## 五、跟我 vault 已有内容的横向对位（不硬挂德勤项目）

> 何大人 7-8 已明确：不硬挂德勤项目。本文做横向关联，按各项目独立判断。

| vault 已有 | 相关 extension / preset | 同款思维 |
|---|---|---|
| **MEMORY.md Goal-Driven Execution 4 条准则**（7-9 Yuxi 借鉴） | Quality Gates | "verifiable goal + 失败标准 + attestation" 工具化 |
| **vault 5-28 Vibe Coding 12 条天条** | Test-First Governance + Quality Gates | "行为边界 + 强制层" 双保险 |
| **vault 5-24 Harness 设计 5 条方法论** | 所有 extension/preset | harness 是 OS 层，extensions 是 OS 之上的应用 |
| **vault 5-11 Hermes Agent 上手指南** | Autonomous Run Governance | autonomous agent 安全治理 |
| **AgentSpace 部署 + AgentRouter**（2026-07-02 commit） | Autonomous Run Governance | 多 harness 统一治理层 |
| **MEMORY.md OPENCLAW 安全关注**（v0.14 验证段） | Autonomous Run Governance | "never infer provider bypass" 原则同款 |
| **v4 推荐策略 3 条硬约束** | Test-First Governance | 硬规则 + 立刻可验证 |
| **vault PARA + Datacore**（2026-06-29 装） | Spec Kit Memory | 把 vault 当 memory backend |
| **OKF frontmatter**（2026-06-29 PARA 同步） | DocGuard | 文档-代码一致性强制 |

---

## 六、待办（等何大人决策）

### 选项 A：先装 Quality Gates（推荐起点）
- 装 `specify` CLI + Quality Gates extension
- 选 1 个 side project 跑一遍 SDD + gates，验证 parity property 真有效
- **verifiable goal**：能在 pre-commit hook 里看到 canary 红了
- **失败标准**：gates 装上但 parity test fail / canary 不触发

### 选项 B：先调研 memsearch（再考虑 Spec Kit Memory）
- memsearch 是 Spec Kit Memory extension 推荐的 memory backend
- 我们的 vault + Datacore 可能能替代 memsearch（需要造 adapter）
- **verifiable goal**：能不能用 `memsearch:memory-recall` 调 vault 的 Datacore 索引
- **失败标准**：memsearch 文档不存在 / 不能接外部数据源

### 选项 C：先不动
- 信息已经存档 + 分析完成，6 个项目的能力清单齐了
- 等真有项目要用 spec-kit 时再选

---

## 七、笔记元信息

- **调研时间**：2026-07-15 14:00 - 14:30
- **数据源**：
  - `github/spec-kit` 仓库（v0.12.15 / 2026-07-14）
  - `extensions/catalog.community.json`（130+ extension）
  - `presets/catalog.community.json`（25 preset）
  - 6 个项目 README 实读（gates / docguard / multi-repo-sync / memory / test-first-governance / autonomous-run-governance）
- **关联笔记**：`2026-07-15 - Spec-Kit 规格驱动开发的 AI 工程化利器（架构茶话会）.md`
- **下一步决策**：等何大人选 A / B / C
