---
title: Spec-Kit —— 规格驱动开发的 AI 工程化利器
author: 架构茶话会（公众号二次解读）+ 小助实测校对
publish_date: '2026-07-15'
saved_date: '2026-07-15'
verified_date: '2026-07-15T14:00+08:00'
verified_version: github/spec-kit @ v0.12.15 (2026-07-14)
source: wechat-image
description: GitHub 开源 CLI 工具，把"先写 Spec 再写代码"做成 10 命令 SDD 流水线。本文含原图还原 + 实测校对（5 处事实错误已修正）+ 与 vault 里 Goal-Driven Execution / 12 条天条 / Harness 系列笔记的横向关联。
attachment: "[[attachments/2026-07-15 - Spec-Kit 信息图.jpg]]"
timestamp: '2026-07-15T13:29:00+08:00'
type: tech-article
tags:
- AI
- Agent
- Spec-Kit
- SDD
- 规格驱动
- 公众号
---

# Spec-Kit —— 规格驱动开发的 AI 工程化利器

> 来源：何大人 2026-07-15 微信发送的信息图（公众号「架构茶话会」解读，非 GitHub 官方发布）
> 实测校对：2026-07-15 14:00（github/spec-kit v0.12.15）
> 原图已存档：`attachments/2026-07-15 - Spec-Kit 信息图.jpg`

## 一、信息图原文还原（保留作存档）

### 主标题
**Spec-Kit** —— 规格驱动开发的 AI 工程化利器
GitHub 开源的 CLI 工具包，让 AI 按图纸施工，从"氛围编码"走向高质量交付
四大特征：规范先行 / AI 执行 / 质量可控 / 协作高效

### 1. 为什么需要 Spec-Kit？

AI 编程工具让写代码速度提升 **10 倍**，但带来"氛围编码"（Vibe Coding）问题：
- ❌ AI 生成代码看起来有模有样但实际不工作
- ❌ 没处理大文件 / 没限制格式（.exe 也能传）/ 没加载指示器
- ❌ 裁剪比例没强制 1:1 / 上传后没更新预览
- （图注：来回 10 轮对话，代码越来越乱）

Spec-Kit 的解法：**建筑事先画图纸，工人按图纸施工，监理按图纸验收**
先写清楚（规范 Spec）→ AI 按图纸施工（生成代码）→ 按标准验收（验收通过）

### 2. Spec-Kit 是什么？

GitHub 于 **2025 年 9 月** 开源的 CLI 工具包，与 Claude Code / GitHub Copilot / Cursor 集成，4 阶段工作流：
1. `/speckit.constitution` — 制定项目"宪法"（技术原则）
2. `/speckit.specify` — 编写结构化功能规格
3. `/speckit.plan` — 生成技术实现方案
4. `/speckit.tasks` — 拆解可执行的任务清单

### 3. 四阶段详解

**Stage 1：`/speckit.constitution`（技术原则 / 宪法）**
- 所有 API 遵循 RESTful 规范
- 前端必须使用 TypeScript
- 先写测试，再写实现（TDD）
- 性能：首屏 < 2 秒，支持 10k+
- 安全：所有输入必须校验
- **输出：** `.specify/memory/constitution.md`

**Stage 2：`/speckit.specify`（功能规格 / 需求）**
- 用户故事 1：上传头像 / 用户故事 2：裁剪头像
- 验收标准：JPG/PNG，≤5MB，裁剪比例 1:1
- **输出：** `specs/001-avatar-upload/spec.md`

**Stage 3：`/speckit.plan`（技术方案 / 设计）**
- 架构图 / API 设计 / 数据模型 / 技术选型 / 状态流 / 研究与决策依据
- **输出：** `specs/001-avatar-upload/{spec.md, plan.md, data-model.md, contracts/api-spec.json, research.md}`

**Stage 4：`/speckit.tasks`（任务拆解 / 执行）**
- 拆解为可并行的任务清单，标注依赖关系（`[P]` = 可并行）
- **输出：** `specs/001-avatar-upload/tasks.md`

### 4. Spec-Kit vs 传统 AI 编程

| 环节 | Vibe Coding | Spec-Kit |
|---|---|---|
| 需求沟通 | 10 轮对话，碎片化 | 1 份 Spec，结构完整 |
| 技术方案 | AI 临时决定，可能前后矛盾 | Plan 文件统一决策，可 Review |
| 任务拆解 | AI 边做边拆，经常遗漏 | 一次性拆解，依赖清晰 |
| 代码质量 | "看起来对"，边界遗漏 | 验收标准前置，测试覆盖完整 |
| 维护成本 | 3 个月后看不懂 | Spec 即文档，新成员快速上手 |
| 回滚 | 改崩了不知道之前什么样 | Git 管 Spec 版本，随时回滚 |

**真实数据（图作者声称，来自 GitHub 内部测试）：**
- 首次通过率 40% → 85%（提升 112%）
- 调试时间减少 60%

### 5. 高级玩法
- **CI/CD 集成**：Spec 生成的契约可直接接入自动化测试（`speckit test --contract`）
- **多 Agent 协作**：API Mock Manager / Contract Test Runner / UI Component Tester / Resiliency Tester 通过 **MCP 协议**共享 Spec
- **渐进式 Spec**：v1.0 / v1.1 / v2.0 独立存储，可追溯可回滚

### 6. 快速开始（图作者给的命令）
```bash
npm install -g @letuscode/spec-kit   # ⚠️ 包名可疑，见下方"事实校对"
mkdir my-project && cd my-project
speckit init
# 然后在 Claude Code / Cursor 里依次跑 4 个 slash 命令
```

### 7. 谁适合用？
⭐⭐⭐ 个人 side project / ⭐⭐⭐⭐⭐ 初创 MVP / ⭐⭐⭐⭐⭐ 企业级 / ⭐⭐⭐⭐ 开源 / ⭐⭐ 算法研究（不适合）

---

## 二、⚠️ 事实校对（2026-07-15 14:00 实测校对结果）

> 实测源：`github/spec-kit` 仓库 README + `pyproject.toml` + `integrations/catalog.json` + `extensions/catalog.json` + `CHANGELOG.md`

| # | 图中说法 | 实测结果 | 严重度 |
|---|---|---|---|
| 1 | "GitHub 2025-09 开源 Spec-Kit" | ✅ 真实，仓库 `github/spec-kit` 存在 | OK |
| 2 | `npm install -g @letuscode/spec-kit` | ❌ **完全错**：spec-kit 是 **Python 项目**（`pyproject.toml` + `src/specify_cli/`），用 `uv tool install specify-cli` 安装；CLI 名是 **`specify` 不是 `speckit`**；`letuscode` 不是 GitHub 组织 | 🔴 高 |
| 3 | "GitHub 内部测试：首次通过率 40%→85%" | ⚠️ **官方 CHANGELOG / README 无此类数据**，未核实 | 中 |
| 4 | "通过 MCP 协议共享 Spec" | ⚠️ **官方 README 主推 `extensions + presets + project-local overrides` 4 层定制体系，没明说 MCP**；图作者解读 | 低 |
| 5 | 4 个 slash command | ⚠️ **少**：实际有 **10 个** —— 核心 7 个（`constitution / specify / plan / tasks / taskstoissues / implement / converge`）+ 可选 3 个（`clarify / analyze / checklist`） | 🟡 中 |
| 6 | `speckit init` | ⚠️ **错**：实际是 `specify init` + `--integration <agent>` 参数 | 🟡 中 |
| 7 | 信息图说"3 个月大还在快速迭代" | ❌ **错**：当前版本 **v0.12.15 = 2026-07-14 发布**（昨天），**v0.12.14 = 2026-07-13**；迭代节奏 = 每天 1-2 个 release；已是 **0.12.x 阶段的成熟产品 + 高速迭代** | 🟡 中 |

**结论**：架构（4 阶段）方向对，但**实现细节（包名、CLI 名、命令数、迭代速度、定制体系）跟图严重不符**。别照搬图。

### 真实安装（2026-07-15 校对版）

```bash
# 1. 先装 uv（Python 包管理器，spec-kit 官方推荐）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 装 specify-cli（注意：是 Python 包，不是 npm）
uv tool install specify-cli

# 3. 初始化项目（CLI 名是 specify，不是 speckit）
specify init my-project --integration copilot  # 或 claude / codex / gemini / cursor-agent / cline / amp 等 30+ agent
cd my-project

# 4. 在 AI agent 里跑 slash command（10 个，不是 4 个）
/speckit.constitution   # 核心：创建项目治理原则
/speckit.specify        # 核心：定义要构建什么
/speckit.clarify        # 可选：澄清未指定领域（plan 之前推荐）
/speckit.plan           # 核心：技术实现方案
/speckit.tasks          # 核心：生成任务清单
/speckit.analyze        # 可选：跨工件一致性分析（tasks 之后、implement 之前）
/speckit.checklist      # 可选：生成质量检查清单
/speckit.taskstoissues  # 核心：把任务转成 GitHub Issues
/speckit.implement      # 核心：执行所有任务，按 plan 构建 feature
/speckit.converge       # 核心：评估代码 vs spec/plan/tasks，追加剩余工作
```

---

## 三、与 vault 现有内容的横向关联

> 何大人 7-8 已明确：不硬挂德勤项目。本文就横向关联已有笔记，看是否补完我们的工程方法论。

### 关联 1：vs Goal-Driven Execution（MEMORY.md 7-9 从 Yuxi 借鉴的 4 条准则）

`/root/vault/2-Areas/AI-Agent-研究/2026-07-09 - Yuxi - Deep Research.md` 里我从 Yuxi 的 AGENTS.md 提取了 4 条核心准则：
1. Think Before Coding（先把任务转成最小验收标准）
2. Simplicity First（不写 speculative feature）
3. Surgical Changes（只改必须改的）
4. **Goal-Driven Execution**（verifiable goal + 失败标准比成功标准更重要）

**关系**：Yuxi 的 Goal-Driven Execution 是**纪律**（每次动手前问自己），Spec-Kit 是**工具**（把"先写 Spec"变成可执行的工作流）。**两者互补**：
- 纪律告诉你"为什么要先想清楚"
- 工具告诉你"怎么把'想清楚'沉淀为文件，AI 能读懂"

→ **建议**：把 Spec-Kit 当作 Goal-Driven Execution 的**机械化载体**。在 Hermes / Codex / Claude Code 里跑 10 个 slash 命令前，先自己按 Yuxi 准则过一遍 Goal。

### 关联 2：vs Vibe Coding 12 条天条（vault 5-28 笔记）

`/root/vault/2-Areas/公众号文章/2026-05-28 - Vibe Coding错误率从85%降到8%：我只做了12条天条.md` —— **同一问题的两种解法**：
- **天条款**（12 条规则）：用"行为边界"限制 AI 不要乱来（CLAUDE.md 里写死）
- **Spec-Kit 款**：用"前置规格"先定义清楚再让 AI 干活

→ **两者不冲突**：12 条天条可以放进 `.specify/memory/constitution.md`（Stage 1 输出），作为 Spec-Kit 流程的"宪法"输入。

→ **可立即试**：把 vault 5-28 那 12 条规则整理成 constitution 模板，跑一次 `/speckit.constitution` 看是否能结构化沉淀。

### 关联 3：vs Harness 设计（vault 5-24 笔记）

`/root/vault/2-Areas/公众号文章/2026-05-24 - 都是 AI Coding，为什么 Java 体验差了一个量级？五条方法论帮你构建自己的 Harness 环境.md` —— Harness 是 AI 编码的"操作系统"层，Spec-Kit 是 harness 里的 **spec 层**具体实现。

→ **战略视角**：Spec-Kit 不是替代 Claude Code / Cursor / OpenClaw，而是它们的"前置规范层"。跟 OpenClaw 的关系：**OpenClaw 是执行器，Spec-Kit 是规范源**，两者不冲突。

### 关联 4：vs AI-Native R&D 自驱动闭环 v2/v3

`/root/vault/1-Projects/德勤/AI-Native/笔记/2026-06-17 - AI-Native R&D 自驱动闭环 v{2,3}.0.md` —— 我之前设计的自驱动闭环是**项目级**（研究 → 决策 → 执行 → 复盘）；Spec-Kit 是**单功能级**（constitution → spec → plan → tasks）。颗粒度不同。

→ **嵌入点**：自驱动闭环里"决策"步骤，可以嵌入 Spec-Kit 的 `plan` 阶段产出作为决策依据。

---

## 四、能不能现在就装一个试试？

### 实操前提（必查 3 项）—— 已 2026-07-15 14:00 校对

```bash
# 1. 查 GitHub 官方仓库（已确认：github/spec-kit 存在，当前 v0.12.15）
# 2. 查 README 的 install 章节（已校对：是 uv tool install specify-cli）
# 3. 查 Claude Code 的 slash command 兼容性（已确认：spec-kit 集成 claude / codex / copilot / gemini / cursor / cline / amp 等 30+ agent）
```

### 最小验证（按 Yuxi Goal-Driven Execution 思路）

**verifiable goal**：能不能在 OpenClaw 里跑一次 10 命令工作流，产出完整的 `specs/001-hello-world/` 目录？
**成功标准**：4 个核心文件（constitution.md / spec.md / plan.md / tasks.md）全部生成 + 结构符合官方示例 + 任一 `--integration` 参数都能跑
**失败标准**：`specify init` 报错 / 任一 slash 命令不识别 / 输出文件残缺

→ **不在仓库写代码前不试**：跟 v4 策略"拒绝 speculative feature"同款纪律——先把官方文档读完，再决定要不要在我们的工具链里加这一层。

---

## 五、实测关键洞察（2026-07-15 14:00 校对后）

### 洞察 1：Spec-Kit 已经超越"4 阶段"——是 10 命令的完整 SDD 流水线

| 阶段 | 命令 | 关键能力 |
|---|---|---|
| **规范层** | `constitution / specify / clarify` | 治理原则 + 需求 + 澄清 |
| **设计层** | `plan / tasks / analyze / checklist` | 技术方案 + 任务拆解 + 一致性分析 + 质量清单 |
| **执行层** | `implement / converge` | AI 自动按 plan 写代码 + 自我评估 + 追加遗漏 |
| **协作层** | `taskstoissues` | 任务自动转 GitHub Issues |

→ **这不只是"先写 Spec 再写代码"，是规范→澄清→设计→分析→执行→评估的完整闭环**。

### 洞察 2：4 层定制体系（extensions + presets + bundles + project-local overrides）

按优先级（⬆ 高 → ⬇ 低）：
1. **Project-Local Overrides**（`.specify/templates/overrides/`）—— 单项目一次性调整
2. **Presets**（`.specify/presets/templates/`）—— 角色化定制
3. **Extensions**（`.specify/extensions/templates/`）—— 新能力
4. **Spec Kit Core**（`.specify/templates/`）—— 内置默认

→ **这是平台型产品的设计**，不是单功能 CLI。意味着：
- 团队可建"角色 preset"（前端 / 后端 / QA / Architect）
- 单仓库可加 extension（如 `agent-context` / `bug` / `git` / `selftest` / `template`）
- 现成 community extensions：`Multi-Repo Branch Sync` / `Quality Gates` / `Test-First Governance` / `Autonomous Run Governance` / `DocGuard` / `Spec Kit Memory`

### 洞察 3：跟现有 AI 工具的关系——互补，不是替代

Spec-Kit 是**规范源 + 工作流驱动**：
- 它不写代码
- 它产出 spec / plan / tasks 文档，让 AI agent 读
- 它跟 30+ AI coding agents 集成（Claude Code / Codex / Cursor / Copilot / Gemini CLI / Cline / Amp 等）
- 在 agent 里通过 `/speckit.*` slash command 触发

→ **跟 OpenClaw 的关系**：OpenClaw 是执行器，Spec-Kit 是规范源。两者可以**串联**（Spec-Kit 产出 spec → OpenClaw 执行实现）。

### 洞察 4：官方明确瞄准"企业级约束"场景

README "Experimental Goals" 里明确写：
- ✅ **Enterprise constraints**: mission-critical application development, organizational constraints (cloud providers, tech stacks, engineering practices), enterprise design systems, compliance requirements
- ✅ **Technology independence**: 跨语言/框架通用
- ✅ **User-centric development**: from vibe-coding to AI-native development
- ✅ **Creative & iterative processes**: parallel implementation exploration, upgrade and modernization tasks

→ **直接瞄准德勤级咨询/企业落地场景**。但**不强行关联德勤项目**，按何大人 7-8 明确。

### 洞察 5：迭代速度惊人——每天 1-2 个 release

- **v0.12.15 = 2026-07-14 发布**（昨天）
- **v0.12.14 = 2026-07-13**
- 每天 1-2 个 release

→ **这意味着**：仓库里看到的任何实现细节，**3 个月后可能大变**。vault 里写 spec-kit 相关笔记时必须**标注日期 + 版本号**（本笔记已标注 `verified_version: github/spec-kit @ v0.12.15`）。

---

## 六、给我的判断（校对后修订）

| 维度 | 信息图判断 | 实测判断 | 修订 |
|---|---|---|---|
| **理念价值** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ —— "specifications become executable" | 同 |
| **工具成熟度** | ⭐⭐⭐（3 个月大） | ⭐⭐⭐⭐⭐（0.12.x，每天 1-2 release，企业级已瞄准） | ⬆ 升 2 档 |
| **命令完整度** | 4 个 | **10 个**（7 核心 + 3 可选） | ⬆ 大幅升级 |
| **安装方式** | npm（错） | uv / pipx（Python） | 修订 |
| **定制能力** | MCP（未核实） | **4 层定制体系**（extensions/presets/bundles/overrides） | 更具体 |
| **跟现有工具关系** | 互补 | **互补 + 可串联**（spec-kit 产出 → OpenClaw 执行） | 更明确 |
| **风险** | 公众号解读多错误 | **架构对、细节错** —— 别照搬命令 / 数据 / MCP | 提示升级 |

**最终建议**（按 Yuxi Goal-Driven Execution）：
- ✅ **可立即试**：装 `specify-cli` + 在 1 个小仓库（如我的 `agent-tools` skill）跑 `constitution / specify / plan / tasks` 4 命令
- ✅ **可立即复用**：把 vault 5-28 的 12 条天条整理成 `.specify/memory/constitution.md` 模板
- ⚠️ **不建议**：直接拿信息图当 SOP 在生产用——细节错太多

---

## 七、待办（已实测校对，下一步可选）

- [x] 读 `github/spec-kit` 官方 README，校对 install 命令（2026-07-15 14:00 完成）✅
- [ ] 装 specify-cli（`uv tool install specify-cli`），版本固定到 `v0.12.15` 避免 daily 升级影响
- [ ] 选 1 个 side project 跑一次完整 10 命令流程（最小验证"4 阶段 → 10 阶段"扩展示范）
- [ ] 把 vault 5-28 的 12 条天条整理成 constitution 模板
- [ ] 看 community extensions 里有没有可借鉴的（Quality Gates / Test-First Governance 直接相关）
