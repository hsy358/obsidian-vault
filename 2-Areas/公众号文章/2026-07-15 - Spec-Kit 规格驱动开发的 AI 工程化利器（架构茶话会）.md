---
title: Spec-Kit —— 规格驱动开发的 AI 工程化利器
author: 架构茶话会（公众号二次解读）
publish_date: '2026-07-15'
saved_date: '2026-07-15'
source: wechat-image
description: GitHub 2025-09 开源的 CLI 工具，把"先写 Spec 再写代码"做成 4 阶段标准工作流（constitution / specify / plan / tasks）。本文同时给出事实校对、与 vault 里 Goal-Driven Execution / 12 条天条 / Harness 系列笔记的横向关联。
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

## 二、⚠️ 事实校对（图里这几处有疑问）

| 图中说法 | 校对结果 | 处理建议 |
|---|---|---|
| "GitHub 2025-09 开源 Spec-Kit" | ✅ 真实，仓库 `github/spec-kit` 存在 | 可信 |
| `npm install -g @letuscode/spec-kit` | ❌ **可疑** —— `letuscode` 不是 GitHub 组织 | 不要照装，先到 `github.com/github/spec-kit` 看 README |
| "首次通过率 40% → 85%" / "调试时间减少 60%" | ⚠️ **未核实** —— GitHub 官方博客未公开此类数据 | 引用前需找官方来源 |
| "通过 MCP 协议共享 Spec" | ⚠️ **图作者解读** —— GitHub 官方文档没有明说 MCP 用法 | 仅供参考 |
| `/speckit.constitution` 等 4 个命令 | ✅ 与 GitHub 官方 spec-kit 文档对齐 | 可信 |

**结论**：架构（4 阶段工作流）可信；安装命令 / 数据 / MCP 细节需自行 verify。

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

→ **建议**：把 Spec-Kit 当作 Goal-Driven Execution 的**机械化载体**。在 Hermes / Codex / Claude Code 里跑 4 个 slash 命令前，先自己按 Yuxi 准则过一遍 Goal。

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

### 实操前提（必查 3 项）

```bash
# 1. 查 GitHub 官方仓库（不是 npm 包）
gh repo view github/spec-kit 2>&1 | head -20

# 2. 查 README 的 install 章节（不是公众号二次解读）
curl -sL https://raw.githubusercontent.com/github/spec-kit/main/README.md | head -100

# 3. 查 Claude Code 的 slash command 兼容性
# /speckit.* 是 Claude Code 原生命令，还是要靠插件？
```

### 最小验证（按 Yuxi Goal-Driven Execution 思路）

**verifiable goal**：能不能在 OpenClaw 里跑一次 4 阶段工作流，产出完整的 `specs/001-hello-world/` 目录？
**成功标准**：4 个文件（constitution.md / spec.md / plan.md / tasks.md）全部生成 + 文件结构符合图里示例
**失败标准**：跑 `speckit init` 报错 / 任一 slash 命令不被识别 / 输出文件残缺

→ **不在仓库写代码前不试**：跟 v4 策略"拒绝 speculative feature"同款纪律——先把官方文档读完，再决定要不要在我们的工具链里加这一层。

---

## 五、给我的判断

| 维度 | 判断 |
|---|---|
| **理念价值** | ⭐⭐⭐⭐⭐ —— "先写 Spec 再写代码"是 AI 编程失控的正解 |
| **工具成熟度** | ⭐⭐⭐ —— 9 月开源，3 个月仍在快速迭代，文档可能滞后 |
| **跟现有工具关系** | 互补（OpenClaw 是执行器、Spec-Kit 是规范源） |
| **ROI** | 看项目规模 —— 简单 side project 用 12 条天条就够；MVP / 企业级才值得上 Spec-Kit |
| **风险** | 公众号解读多有事实错误（npm 包名 / 数据 / MCP 细节），**别照搬** |

**最终建议**：先读官方 README + 在 1-2 个小仓库里实测 4 阶段工作流，**不要直接照搬公众号的安装命令**。如果实测可用，可以把 12 条天条整理成 constitution 模板（嵌入 `.specify/memory/constitution.md`）。

---

## 六、待办（可选）

- [ ] 读 `github/spec-kit` 官方 README，校对 install 命令（必做）
- [ ] 选 1 个 side project 跑一次 4 阶段，产出 specs 目录（验证可行性）
- [ ] 把 vault 5-28 的 12 条天条整理成 constitution 模板（如果走 Spec-Kit 路线）
- [ ] 关注 `github/spec-kit` 的 release notes（3 个月内可能大改 API）
