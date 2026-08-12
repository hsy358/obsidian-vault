---
title: "dashi-taskboard（Codex Taskboard）—— 本地优先的 Codex 任务面板"
date: 2026-08-12
source: web-search + web-fetch + 何大人微信发图
url: https://github.com/chuspeeism/dashi-taskboard
author: chuspeeism（社区作者，非 OpenAI 官方）
tags: [taskboard, codex, agent-orchestration, kanban, local-first, hermes-comparison]
status: research-note
type: ai-agent-research
---

# dashi-taskboard（Codex Taskboard）研究笔记

> **触发场景**：何大人 2026-08-13 00:30 通过微信发来一张介绍图（1200×2366 像素 JPG），介绍 "dashi-taskboard"——一个开源 Kanban 工具，专门解决 Codex 对话界面的"任务管理痛点"。
>
> 真实 GitHub repo: **https://github.com/chuspeeism/dashi-taskboard**

---

## ⚠️ 一个细节：图里叫 dashi-taskboard，但 README 自称 "Codex Taskboard"

图片描述写的是 "**dashi-taskboard**"（作者 chuspeeism 在 GitHub repo URL 用的命名），但 repo 内的 README 和官方文档自称 "**Codex Taskboard**"。两边名字混用，搜索时建议两个都试。

---

## 🎯 一句话本质

**Codex Taskboard = 本地优先（local-first）的 Kanban + Codex 集成层**，通过 CDP 注入官方 Codex/ChatGPT 客户端侧栏，把对话里的任务拆解成可视化的 4 列面板（Backlog / To-do / In Progress / Reviewing）。

---

## 🏗️ 架构（从 README 拆出）

### 三件套共用一套 HTTP API

| 组件 | 形态 | 作用 |
|---|---|---|
| **React UI** | 浏览器（127.0.0.1:47823）+ macOS App | 给"人"看的 4 列面板 |
| **taskctl CLI** | `npm run taskctl` 或 `npm link` 装全局 | 给脚本/Agent 用的命令 |
| **Codex Skill** | `skills/manage-taskboard` symlink 到 `~/.codex/skills/` | **教 Codex**自动管理任务 |

数据存 SQLite：`.data/taskboard.sqlite`（开发）或 `~/Library/Application Support/Codex Taskboard`（App）。

### Codex 集成（关键技术亮点）

| 能力 | 实现方式 |
|---|---|
| **侧栏注入** | CDP launcher + `--remote-debugging-port=9231` 起独立 Codex 窗口 → `npm run codex:inject --port 9231 --open` 注入 Taskboard 侧栏 |
| **任务→对话桥接** | 面板 "在对话中打开" → 选对应 Codex 项目 + 打开未发送 composer（含 e-taskboard 指令 + 实际 issue id） |
| **会话反向绑定** | `taskctl` 读 `CODEX_THREAD_ID`，把真实处理的会话写到 issue/comment 记录里 |
| **Git 分支/worktree 绑定** | 每个 issue 可绑一个 branch 或 worktree（从 Codex 项目 repo 扫描，自动） |
| **Codex Skill 工作流** | inspect → move to `in_progress` → optimistic version → verify → `in_review` → **用户显式确认才 done**（不自动） |

> **关键工程点**：CDP 默认无认证，同机进程可访问。launcher 只信任本地代码（README 自己警示）。
> **CSP 绕过**：Codex 26.715.52143 启用了 renderer CSP 阻断任意 HTTP iframe，所以 launcher 要 CDP CSP bypass + 重建 renderer + 等 OOPIF 真加载完。这是项目最硬核的工程坑。

### 网络与部署

- **默认监听** `0.0.0.0:47823`（LAN 可访问，**无认证** —— 信任网络下用，公开网络必须设 `127.0.0.1` + 加认证边界）
- **SSE 推送** + 断线全量刷新（避免漏掉断开期间改动）
- **Cloudflare 部署**支持：Worker Static Assets + D1 + R2（附件）+ HTTPS Basic Auth（适合 2 个信任协作者）

---

## ✅ 强项

1. **Skill 设计哲学正确**：不自动 done，**等用户显式确认** —— 拒绝 AI 单方面闭环，这是给"AI 自主程度"上保险栓
2. **本地优先**：SQLite + App 内嵌 Node 运行时，目标 Mac 不需要装 Node 也不需要装 Codex CLI（只需 ChatGPT.app）—— 部署门槛极低
3. **不 patch Codex**：不替换 fetch、不改私有 chunk、不编辑 Codex 数据文件 —— 抗 Codex 升级能力强
4. **三件套共用一套 API**：UI/CLI/Skill 不各自一套，避免不一致

## ⚠️ 局限（值得提的）

1. **macOS only**：CDP 注入 + Tauri App 都是 macOS 限定（README 提到需要 Xcode + Rust aarch64/x86_64 targets）
2. **依赖 Codex 客户端窗口**：必须在官方 ChatGPT.app 注入，本质是**寄生在 OpenAI 客户端**，OpenAI 一改 CDP 策略就可能挂
3. **LAN 模式无认证**：默认信任整网，公开网络必须自己加固
4. **Cloudflare 部署**走 HTTPS Basic Auth 共享密码 —— 不适合规模化团队（最多 2 人）
5. **不是真正的 Agent 任务调度器**：4 列 Kanban 是给人看的，**没有 claim/blocked/ready 这种 Agent 间调度状态**

---

## 🔄 同类项目横向对比（web_search 顺手发现的几个）

| 项目 | 定位 | 跟 dashi 区别 | Hermes 支持 |
|---|---|---|---|
| **dashi-taskboard** | Codex 侧栏注入的本地 Kanban | **人看**为主，CDP 寄生 | ❌ 无 |
| **[saltbo/agent-kanban](https://github.com/saltbo/agent-kanban)** | **Agent-first** 任务板，AI workforce mission control | Leader + Workers 架构，每 worker 独立 worktree，PR → merge 自动 complete | ✅ **明确列在 supported runtimes** |
| **[tcarac/taskboard](https://github.com/tcarac/taskboard)** | 本地 Kanban + MCP server（22 个工具） | 通用，**Go 单二进制** + SQLite + React UI + Tailwind v4 + dnd-kit | ❌ 无（通用） |
| **GoalBuddy（Codex /goal）** | `/goal` 命令内置的轻量 Kanban | **Codex 官方方向**，cards 带 objective + allowed files + verify commands + receipt | ❌ Codex only |
| **[changkun/wallfacer](https://github.com/changkun/wallfacer)** | 自主工程平台（spec-driven） | sandbox + 编排 + kanban，全自主 | ❌ 无（但支持 claude-code / codex） |
| **VS Code Agent Kanban** | VS Code 插件 + `.md` 任务格式 | `@kanban` 命令 + Git worktree + GitHub Copilot | ❌ 无（Copilot） |

---

## � 我的判断（不强挂钩德勤）

### 1. dashi-taskboard 适合的真正场景

- **个人开发者 + Codex 重度用户**：一个人用 Codex 跑多个并发 issue，需要"看见"任务进度 → dashi 是最轻量的解
- **不希望引入 OpenClaw / Hermes 这类重框架**：就想要个面板 + CLI，不想要 dispatcher 进程
- **不需要多 Agent 协调**：单 Codex 进程，单人

### 2. dashi 不适合的场景

- **多 Agent 协作**（Leader/Worker 分工） → 上 **saltbo/agent-kanban**
- **需要 Agent 间 claim/blocked/ready 状态机** → 这正是 Hermes dispatcher kanban 在做的（vault 已有 Hermes 研究笔记可查）
- **非 macOS** → tcarac/taskboard（Go 单二进制 + MCP）或 saltbo/agent-kanban（Web）

### 3. 跟 vault 已有内容的横向关联

- **MEMORY.md 已定决策**：Hermes Agent v0.14 是德勤项目 Agent 框架的唯一选择 → dashi 这种"寄生 Codex"的工具，跟 Hermes "原生 dispatcher" 思路**根本不同**，没有替代关系
- **vault/2-Areas/AI-Agent-研究/2026-06-12 - Hermes Desktop - Deep Research.md** 已经有 Hermes Kanban 深入研究 → 如果要看"任务编排"对比研究，可以把 dashi 当作"Codex 寄生派"的代表案例
- **vault/2-Areas/AI-Agent-研究/2026-07-30 - Harness Handbook** 提到 Harness 六大组件 → dashi 的 Skill 设计（inspire-in_progress-verify-in_review-用户确认）正好对应 Harness 的"verification + stop conditions"两个组件，是好的实例参考

---

## 🪖 推荐动作

按"先有 verifiable goal 再动手"原则：

1. **如果只想看个新鲜**：5 分钟翻完上面表格 + 看 GitHub README 截图，不必 clone
2. **如果你是 Codex 重度用户**：clone 下来 `npm install && npm start`，跑 1 个真实 issue 体验 Skill 工作流 —— **verifiable goal**：跑通 1 个任务从 backlog → in_progress → in_review → done（用户点确认）
3. **如果是研究 Agent 任务编排**：不要花时间在 dashi 上，**直接看 saltbo/agent-kanban**（它原生支持 Hermes，跟德勤项目的研究方向重合度更高 —— 但这是"借鉴点"研究，不是替代 Hermes）

---

## 📎 附件

- `2026-08-12_img_dashi-taskboard-intro.jpg`（何大人原始发图，1200×2366 像素，195KB）—— 介绍图，未单独 OCR（web_fetch README + web_search 已覆盖图内全部信息点）

## 🔗 来源

- GitHub: https://github.com/chuspeeism/dashi-taskboard
- 同类搜索：saltbo/agent-kanban, tcarac/taskboard, changkun/wallfacer, GoalBuddy (Codex /goal), VS Code Agent Kanban
- vault 关联：`2-Areas/AI-Agent-研究/2026-06-12 - Hermes Desktop - Deep Research.md`、`2-Areas/AI-Agent-研究/2026-07-30 - Harness Handbook - 论文核心要点 + 项目分析.md`
