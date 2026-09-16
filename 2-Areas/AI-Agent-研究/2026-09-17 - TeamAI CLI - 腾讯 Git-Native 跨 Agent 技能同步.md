---
title: "TeamAI CLI — 腾讯开源的 Git-Native 跨 AI Agent 技能同步工具"
author: "Tencent + 二次源整合"
publish_date: "2026-09-09"
saved_date: "2026-09-17"
source: "github-repo-analysis"
original_url: "https://github.com/Tencent/teamai-cli"
official_site: "https://teamai.ai"
sources:
  - "https://github.com/Tencent/teamai-cli"
  - "https://www.npmjs.com/package/teamai-cli"
  - "https://genztech.blog/p/teamai-cli-setup-guide"
  - "https://pyshine.com/TeamAI-Make-Every-Team-AI-Native"
  - "https://agentconn.com/agents/teamai-cli"
type: research-note
tags: [TeamAI, Tencent, OpenClaw, Hermes, Claude-Code, Codex, Cursor, CodeBuddy, Git-Native, Skill-Sync, Cross-Agent, Friction-Based-Learning, MCP, 德勤-MVP-强关联, Team-Execution, Team-Context, Team-Improvement]
status: complete
note: "何大人给的链接是 github.com/teamai-team/teamai（404 错误），正确地址是 Tencent/teamai-cli。已通过 web_search 找到真身。"
license: MIT
stars: "2.9k（一天内 +563，曾登 GitHub trending）"
---

# TeamAI CLI — 腾讯开源的 Git-Native 跨 AI Agent 技能同步工具

> 📌 **核心定位**：腾讯开源的 CLI（MIT，~2.9k stars，一天 +563），把团队级的 skills、rules、MCP、hooks、knowledge 通过 git 仓库**自动同步到每个团队成员的本地 AI 工具**——Claude Code、Codex、Cursor、CodeBuddy、OpenCode、OpenClaw、Hermes、Qoder、Kiro、ZCode 全都支持。

> 🎯 **对德勤 MVP 的关联**：**极强关联**——OpenClaw 和 Hermes 都在官方支持矩阵里。**这不是另一个 Agent 框架，是 Agent 间的 skill sync 工具**——和咱们德勤 MVP 要解决的"多客户统一 AI 工作流"问题高度重合。

> ⚠️ **链接勘误**：何大人给的链接 `github.com/teamai-team/teamai` 返回 404，正确地址是 **`github.com/Tencent/teamai-cli`**。

## 一句话定位

**TeamAI CLI**：腾讯开源的"AI Native 团队协作"工具，通过 **git repo 作为 single source of truth**，把团队的 skills/rules/MCP/hooks/agents 自动分发到每个团队成员本地的各种 AI Agent 里。所有改动走"push → MR 评审 → pull"流程，**零手动同步**。

> 官方标语：**"One Team. One Harness. Every Agent."**

## 🏗️ 三大 Layer（架构全景）

```
┌─────────────────────────────────────────────────────────┐
│                       TeamAI CLI                          │
├─────────────────────────────────────────────────────────┤
│                                                            │
│  Layer 1: Team Execution（已是生产状态）                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │  init / pull / push                                │  │
│  │  skills + rules + agents + hooks + MCP + env       │  │
│  │  → 团队配置自动分发到本地 Agent                     │  │
│  └───────────────────────────────────────────────────┘  │
│                                                            │
│  Layer 2: Team Context（beta）                             │
│  ┌───────────────────────────────────────────────────┐  │
│  │  recall + learnings + codebase graph + teamwiki    │  │
│  │  → 团队知识自动检索，跨 Agent 共享                  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                            │
│  Layer 3: Team Improvement（beta）                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  friction-based share-learnings + sessions + digest │  │
│  │  → 团队从每次执行中持续学习                          │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 🎯 核心设计哲学（值得借鉴）

### 1. **Git 作 Single Source of Truth**

不是中央服务器，不是 SaaS——**就是一个普通 git repo**（GitHub / GitLab / GitCode / CNB / TGit / 自建 Git 都行）。

```
Team AI Native Repo (git)
├── skills/                ← 团队级技能库
│   └── <name>/SKILL.md
├── rules/                 ← 团队级规则
├── agents/                ← 团队级 agent 配置
│   ├── <name>.yaml
│   └── <namespace>/<name>.yaml
├── hooks/hooks.yaml       ← SessionStart/Stop 等
├── mcp/mcp.yaml           ← 团队 MCP 服务器
├── env/                   ← 共享环境变量（**不放 secrets**）
├── culture.md             ← 团队文化（注入 CLAUDE.md/AGENTS.md）
├── claudemd/*.md          ← 注入 Claude Code 的指令
├── docs/                  ← 项目基础文档
└── teamwiki/              ← (beta) 从代码库自动生成的知识图谱
```

**push → MR 评审 → pull 流程**：
```text
1. 团队成员 teamai push   → 创建 branch + MR
2. Reviewer 评审          → approve + merge
3. 其他成员 SessionStart  → 自动触发 teamai pull
                          → 同步到本地 AI 工具
```

> 💡 **这就是 OpenClaw vault 架构**——**vault 就是 teamai 风格的 git 仓库**！

### 2. **Friction-Based Learning（极优雅）**

**核心洞察**：**"不痛不痒的 session 不学，只学真正踩坑的 session"**。

**触发学习的 friction 信号**（打分制）：
- 你**打断**了 AI（interrupted）
- 你**纠正**了 AI（corrected）
- 你**否决**了某个 tool call（denied tool call）
- AI 自己**重试失败工具** N 次（retried failing tools）
- ❌ **不**触发：长但平稳的 session（很多 tool call 但无 friction）

**触发时的提示**（Stop hook）：
```text
[teamai] This session may contain a problem worth documenting: 
you interrupted the AI twice, the AI retried failing tools 8 times.

Task: Fix duplicate project-level Hook injection

Consider running /teamai-share-learnings to summarize what you learned 
and share it with your team.
```

**每次 session 最多提示一次**（避免打扰）——可关闭但默认开。

> 💡 **这就是 OpenClaw "记忆触发器"可以借鉴的机制**——我每次打断 AI 都该被记录为"学习时刻"。

### 3. **teamai-recall 子 Agent 做知识检索（beta）**

- 默认关闭，**需团队明确启用**（`sharing.recall.enabled: true`）
- 启用后：`teamai pull` 自动部署 `teamai-recall` 子 agent 到每个 AI 工具的 `agents/` 目录
- **AI 在每次任务前调用 recall 子 agent**
  - 关键词提取
  - 跑相关性 precheck（不相关直接跳过）
  - 搜索（BM25 + 图增强）
  - 返回结构化摘要
- **每次会话最多触发一次**（控制开销）

**手动调用**：
```bash
teamai recall "port conflict"
# 输出：
[1/2] MR review caught a port-conflict bug ★1 [user]
Author: member-a | Score: 18.5 | Tags: troubleshooting, networking

[2/2] Deployment configuration best practices [project]
Author: member-b | Score: 12.0 | Tags: deploy, config
```

### 4. **teamai codebase 自动提取知识图谱（核心创新）**

```bash
teamai import --from-repo https://github.com/org/repo
teamai codebase --extract /path/to/repo
teamai codebase --deep-enrich --project my-service
teamai codebase --reconcile --output /path/to/repo
teamai codebase --lint
```

**双轨提取**：
- **AST 轨**（TypeScript/JavaScript/Python/Go）：**WASM tree-sitter**，纯 JS 依赖、无需原生 toolchain
- **启发式轨**（所有语言，包括 Java/Rust）：regex-based

> 💡 **WASM tree-sitter 这点很聪明**——客户端零依赖、跨平台一致。

**edges 类型**：
- `DEPENDS_ON`（import/require 关系）
- `REFERENCES`（call sites）
- `IMPLEMENTS`（TS implements clauses）

**重排序增强**：recall 时给 codebase 命中页加权

## 🧩 官方支持矩阵（重要）

**11 个 AI Agent 全部支持**：Claude Code ✓ Codex ✓ Cursor ✓ CodeBuddy ✓ WorkBuddy ✓ OpenCode ✓ **OpenClaw ✓** **Hermes ✓** DeepSeek Harness ✓ Qoder ✓ Kiro ✓ ZCode ✓

**关键观察**：
- ✅ **OpenClaw 完整支持**（skills/rules/docs/env/agents/hooks/mcp 全部）
- ✅ **Hermes 部分支持**（skills/docs/env/agents/hooks）
- ✅ **跨 Git provider**（GitHub/GitLab/GitCode/CNB/TGit/私有 Git）

| Agent | Execution | Context | Improvement |
|-------|-----------|---------|-------------|
| Claude Code | ✓✓✓✓✓✓✓✓✓✓✓✓✓ | 全部 | 全部 |
| Codex | ✓✓✓✓✓✓✓✓✓✓✓✓✓ | 全部 | 全部 |
| Cursor | ✓✓✓✓✓✓✓✓✓✓✓✓✓ | 全部 | 全部 |
| CodeBuddy | ✓✓✓✓✓✓✓✓✓✓✓✓✓ | 全部 | 全部 |
| OpenCode | ✓✓✓✓✓✓✓✓✓✓ | — | — |
| **OpenClaw** | ✓✓✓✓ | — | ✓✓✓ |
| **Hermes** | ✓✓✓✓ | — | ✓✓✓ |
| DeepSeek Harness | ✓✓ | — | ✓✓✓ |

> 💡 **OpenClaw 在 TeamAI 官方支持矩阵里**——**说明 OpenClaw 已经是 AI 编程 Agent 的"事实标准"之一**。这是个好消息。

## 🎯 核心命令清单

| 命令 | 用途 |
|------|------|
| `teamai init <repo>` | 初始化（OAuth 登录、关联 repo、注册成员、注入 hooks）|
| `teamai pull` | 拉取团队资源，注入本地 AI 工具 |
| `teamai push` | 推送本地资源，创建 MR |
| `teamai status` | 显示本地 vs 团队 repo 差异 |
| `teamai recall <query>` | 搜索团队知识库 |
| `teamai recall enable/disable/status` | 切换 recall 状态 |
| `teamai contribute` | 分享 session 经验到团队 repo |
| `teamai session save` | 记录隐私脱敏的 session 摘要 |
| `teamai digest` | 生成周报（7 天成功率、prompt、活跃时间、成本、cache、纠正趋势）|
| `teamai dashboard` | Web 仪表盘（实时 session + 7 天对比）|
| `teamai projects` | 绑定工作目录到项目 |
| `teamai roles` | 管理角色 → namespace 映射 |
| `teamai tags` | 标签订阅 |
| `teamai source` | 订阅其他团队 repo |
| `teamai doctor` | 配置诊断 |

## 🎯 对德勤 MVP 的可借鉴点（核心价值）

> **极强关联**：TeamAI 解决的"团队 AI 工作流统一"问题，**就是德勤 MVP 的核心场景之一**——给每个客户的团队提供一致的 AI 工作流，但允许每个员工用不同 AI 工具（Claude Code / Codex / Cursor / OpenClaw）。

### 借鉴点 1：**Friction-Based Learning 机制** ⭐⭐⭐

**TeamAI 的核心创新**：**不是所有 session 都学，只学有摩擦的 session**。

**对应德勤 MVP**：
- ❌ 现在：所有 session 都记录，无差别（信息洪水）
- ✅ 改进：**借鉴 friction scoring**——只记录"打断/纠正/否决/重试"的 session
- ✅ **直接抄这个打分逻辑**（已验证有效）

**实现路径**：
- 在 Agent Router 层加 friction detector
- Session End hook 评分
- 超过阈值才触发"学习时刻"提示
- 用户确认后自动 generate learning doc → 入 team repo

### 借鉴点 2：**Git 作 SSO（Single Source of Truth）**

**TeamAI 的设计**：**git repo = team AI 知识的唯一来源**。

**对应德勤 MVP**：
- ✅ **和 vault 的设计哲学完全一致**——vault 本身就是 git repo
- ✅ 客户私有 vault 就能当 team repo
- ✅ 团队成员 pull vault → 自动同步到本地 Agent
- ✅ **零基础设施**（不用建服务器）

### 借鉴点 3：**culture.md 注入 AGENTS.md**

**TeamAI 的设计**：在 repo 根放 `culture.md`，自动注入到每个 Agent 的 `CLAUDE.md` / `AGENTS.md`。

**对应德勤 MVP**：
- ✅ 客户的"工作文化/价值观/团队约定"可以直接进 culture.md
- ✅ 自动同步到每个员工本地 Agent
- ✅ **不需要每个 Agent 单独配置**（OpenClaw 用户尤其受益）

### 借鉴点 4：**teamai-recall 子 Agent 做知识检索**

**TeamAI 的设计**：recall 是一个独立子 Agent，在任务前自动调用。

**对应德勤 MVP**：
- ✅ 借鉴这个"先 recall 再行动"的模式
- ✅ **但实现方式要简化**——直接复用 Hermes 的 RAG 能力（已有）
- ✅ 关键词 precheck 减少无效检索（参考 TeamAI 的 `recall --check`）

### 借鉴点 5：**teamai codebase 知识图谱提取**

**TeamAI 的设计**：用 WASM tree-sitter 从代码库自动提取 imports/calls/implements。

**对应德勤 MVP**：
- ✅ **这是"项目记忆"的关键基础设施**——客户代码库的自动索引
- ✅ WASM tree-sitter 客户端零依赖的做法可学
- ✅ 双轨（AST + 启发式）保证覆盖率

### 借鉴点 6：**跨 Agent Harness 抽象**

**TeamAI 的设计**：**同一份 skill 在 11 种 Agent 里通用**。

**对应德勤 MVP**：
- ✅ **德勤客户可能用不同 Agent**（有的 Claude Code，有的 Cursor，有的 OpenClaw）
- ✅ 借鉴 TeamAI 的抽象层，**让 skill 跨 Agent 适配**
- ✅ **这就是可插拔执行器抽象层的另一种实现**——不是协议层抽象，而是**文件格式适配层**

### 借鉴点 7：**Project × Role 维度**

**TeamAI 的设计**：
- `teamai projects` 把工作目录绑定到项目
- `teamai roles` 定义角色 → namespace 映射
- 每个员工只拉取**自己角色相关的 skill**

**对应德勤 MVP**：
- ✅ **多租户/多角色**天然契合这个模型
- ✅ 律师只能看律师的 skill，财务只能看财务的 skill
- ✅ **客户数据隔离**——learnings/<project-id>/ 是项目私有的

### 借鉴点 8：**Weekly Digest 自动总结**

**TeamAI 的设计**：`teamai digest` 自动生成周报（成功率、prompt、活跃时间、成本、cache、纠正趋势）。

**对应德勤 MVP**：
- ✅ **每周给客户经理发"AI 使用情况周报"**——这个差异化服务
- ✅ 指标直接抄 TeamAI 的（已验证）
- ✅ 加上**项目维度**（哪个项目的 AI 用得最多）

## 🚫 注意事项（不夸大 TeamAI）

1. **不解决 Agent 本身问题**——TeamAI 不写 Agent，只同步配置
2. **依赖团队纪律**——必须有人 push 才有内容
3. **MR 流程可能拖慢**——push 要 review，但小团队可以省
4. **Codebase 提取对 monorepo 友好，对单文件项目价值有限**
5. **Recall 子 Agent 是 beta**——效果待验证
6. **依赖 OAuth + Git 平台**——不能完全离线

## 📦 部署与集成

**安装**：
```bash
npm install -g teamai-cli
```

**初始化**：
```bash
# Project-scope（默认）
cd /path/to/my-project
teamai init https://github.com/yourorg/yourrepo

# User-scope（资源装到 ~/)
teamai init https://github.com/yourorg/yourrepo --scope user
```

**模板**：[teamai-hub](https://github.com/teamai-hub) org 提供预装 skills/rules 的 fork 模板

## 🔗 资源

| 资源 | 链接 |
|------|------|
| **GitHub** | https://github.com/Tencent/teamai-cli |
| **官网** | https://teamai.ai |
| **NPM** | https://www.npmjs.com/package/teamai-cli |
| **文档** | docs/usage-guide.md |
| **中文 README** | README.zh-CN.md |
| **TrendShift 趋势** | https://trendshift.io/repositories/123184 |
| **License** | MIT |

## 相关/对比项目

| 项目 | 对比 |
|------|------|
| **Multica** | 同档管理平台，但 Multica 是"agent team 任务板"，TeamAI 是"team skill 同步"——**互补不冲突** |
| **Hermes** | Agent 本身，TeamAI 在它之上做 skill sync |
| **OpenClaw** | Agent 本身，TeamAI 在它之上做 skill sync |
| **LangChain Hub / PromptHub** | 中心化 prompt 库，TeamAI 是去中心化（git repo）|

## 引用（暂未发论文）

```text
@software{teamai-cli-2026,
  title={TeamAI CLI: Make Every Team AI Native},
  author={Tencent},
  year={2026},
  url={https://github.com/Tencent/teamai-cli},
  license={MIT}
}
```

---

## 🧠 我的最终判断

**TeamAI CLI 是 2026 年最值得借鉴的"团队 AI Native"基础设施**——它把"如何让一个团队的所有成员都按统一工作流用 AI"这个**企业落地核心难题**给出了**Git-native 的工程答案**：

> **"git repo = team AI 知识源 → push/MR/pull 流程 → 自动注入每个 Agent"**

**核心差异化**：
1. **Friction-based learning**（不学没摩擦的 session）
2. **WASM tree-sitter**（客户端零依赖的知识提取）
3. **Git 作 SSO**（零基础设施）
4. **11 个 Agent 适配**（OpenClaw 和 Hermes 都在内）

**对德勤 MVP 的 8 大借鉴点**（详见上面），其中最重要的 3 个：

1. ⭐⭐⭐ **Friction-Based Learning 机制**——**直接抄打分逻辑**
2. ⭐⭐ **Git 作 SSO**——和 vault 设计哲学 100% 一致
3. ⭐⭐ **teamai-recall 子 Agent 模式**——简化后用 Hermes 的 RAG 实现

**和咱们 6-29 决策的"执行器抽象层"不冲突，反而互补**——TeamAI 解决**配置/知识**跨 Agent 同步，咱们要解决**运行时执行**跨 Agent 抽象。**两个一起用就是完整的"AI Native 团队平台"**。

**信号价值**：**OpenClaw 已经在 TeamAI 官方支持矩阵**——这等于腾讯给 OpenClaw 背书（虽然腾讯自己也有 WorkBuddy）。**咱们 OpenClaw 的选择是对的**。