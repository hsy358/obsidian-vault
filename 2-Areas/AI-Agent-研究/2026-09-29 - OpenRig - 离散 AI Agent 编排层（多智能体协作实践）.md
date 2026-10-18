---
title: "OpenRig：将离散 AI Agent 编织为持久化协作系统的多智能体编排实践"
source_url: https://mp.weixin.qq.com/s/MVALnklEO5a_xrN1jV7cEw
author: 秦睦迪（公众号「秦先生在广东」，前腾讯高级开发工程师，15 年+全栈）
published_date: 2026-09
captured_date: 2026-09-29
type: research-report
tags: [multi-agent, orchestration, ai-coding, claude-code, codex, tmux, npm-tool, openrig]
related:
  - /root/vault/2-Areas/AI-Agent-研究/2026-08-17 - loopany 开源项目调研.md
  - /root/vault/2-Areas/AI-Agent-研究/2026-08-22 - openai-codex - GitHub 仓库分析.md
  - /root/vault/2-Areas/AI-Agent-研究/2026-07-25 - Multica - GitHub 仓库分析.md
---

# OpenRig — 多智能体编排层（秦睦迪 文章解读）

> **TL;DR**：OpenRig 不是更强的单个 Agent，而是 **编排层（Orchestration Layer）** —— 通过 tmux 持久化 + YAML 声明式拓扑 + MCP 自治集成，把 Claude Code / Codex 等离散工具整合为可协调、可快照、可恢复的协作团队。解决多 Agent 场景最大的痛点：**状态碎片化**。

---

## 1. 核心定位：从终端堆栈到持久化团队

> 当 AI 编程助手从单一终端窗口演变为多 Agent 并行工作时，传统的"开新终端"方式迅速显露出局限。

OpenRig 作为"集线器"管理多 Agent 团队：
- **tmux 持久化**：跨 Agent 协调 + 上下文共享
- **统一健康状态 + 日志聚合**：混乱的终端 → 有序的系统化流程
- **不替代单个 Agent**（如 Claude Code / Codex），而是编排它们

---

## 2. 技术栈 & 部署约束（源码核对版本）

| 项 | 详情（核对至 GitHub main / npm @openrig/cli@0.6.0）|
|---|---|
| 包名 | `@openrig/cli`（**不是 `openrig`**）|
| 当前版本 | **0.6.0**（npm @ 2026-09-28；文章说 0.5.9 已过时）|
| 运行时 | **Node.js 22 或 24**（0.6.0 源码 `engines.node >=22`；**Node 20 已不再支持**；26+ 未测）|
| 依赖 | tmux + SQLite + better-sqlite3 + hono + zod + commander + @modelcontextprotocol/sdk |
| 平台 | **macOS / Linux 原生**；**Windows 不支持，WSL2 未充分验证**|
| 安装 | `npm install -g @openrig/cli`（或 `bun install -g @openrig/cli`）|
| 仓库 | https://github.com/mvschwarz/openrig（Apache-2.0）|
| 官网 | https://openrig.dev |

---

## 3. 声明式配置（YAML = RigSpec）

```
Pods（代理组）/ Seats（席位）/ Edges（通信边）
```

**核心命令**：
- `rig up`：一键启动整个团队
- `rig down --snapshot`：保存当前状态快照
- `rig up <name>`：从快照恢复
- `rig send <role>`：向特定角色派任务
- `rig setup --dry-run`：预览 setup 计划（**强建议**）

**预设拓扑**：
1. `two-seat starter (first-project)` — 双 Agent 入门
2. `conveyor` — 4 席位流水线（模拟 CI/CD）
3. `product-team` — 含 QA / 设计 / 审查的多席位团队

---

## 4. 工作流与 MCP 自治

- **主控 Agent** 自动分配任务 → 执行 → 协调审查 → 形成闭环
- **TUI**：实时可视化团队拓扑、健康状态、日志
- **MCP 集成**：Agent 自主调用 `rig_up` / `rig_send` 管理拓扑 → **Agent 自治 + 人工监控**

---

## 5. ⚠️ 安全红线：实际写入清单（源码核对）

> 关键：**0.4.8.2 之后 OpenRig 已不再写 `~/.claude/settings.json`**（即不再写全局 permission allowlist）。但仍会写下面这些文件。

### setup 阶段（`rig setup`，`--dry-run` 可预览）

| 路径 | 范围 | 写入内容 | 备份必要 |
|---|---|---|---|
| `~/.tmux.conf` | global | append `# OpenRig managed block`（`set -g mouse on`、`history-limit 50000`），用 marker 包裹，可幂等替换 | ✅ |
| `~/.config/cmux/settings.json`（macOS only）| global | cmux socket control → `automation` 模式 | ✅（仅 macOS）|

### Daemon 启动阶段（**自动、无预览**）

| 路径 | 范围 | 写入内容 |
|---|---|---|
| `~/.openrig/`（`OPENRIG_HOME`）| global | instance state：SQLite DB + managed plugin resources |
| `~/.claude/skills/` | global | seeds `openrig-skills` discovery skill（subject to existing version ownership）|
| `~/.agents/skills/` | global | 同上 |

### Rig / Seat Launch 阶段（**自动、无预览**）

**Claude Code**：
- `~/.claude.json` → **workspace trust + onboarding completion**
- `<workspace>/.claude/settings.local.json` → context collector `statusLine` + activity hooks + `permissions.defaultMode=acceptEdits`
- `<workspace>/.mcp.json` → Exa/Context7 MCP entries
- `<workspace>/.openrig/` → helper scripts

**Codex**（`runtime.codex.hooks_enabled` 默认开启）：
- `~/.codex/config.toml` → 启用 hooks + OpenRig activity relay commands + pre-written trust hashes
- `<workspace>` → seat startup 添加 `trust_level = "trusted"`
- Codex cache → recognized update notice 跳过记录

### Hook 内容

- activity relays POST 到本地 daemon 的 `/api/activity/hooks`，payload 含 event type/subtype、seat/runtime identity、timestamp、native session identity
- **不含 prompt 文本和 tool arguments**（README line 103）
- Claude collector 写 context/token usage、session/transcript-path metadata、rate-limit data 到 `state/context-usage` 和 `state/provider-usage`

### 关键警告（README line 136-142）

> Managed hook blocks target OpenRig's entries and retain unrelated hooks, **but trust entries, selected resource keys and Claude's existing status-line command can be replaced**. Some writers recover unreadable settings as empty objects; **this is not a complete preservation or rollback guarantee**. Back up relevant files before first use. **Daemon/bootstrap writes are automatic and do not each have an interactive preview; `rig setup --dry-run` does not preview every later startup effect.**

### 回滚方法（**官方未提供独立 uninstall 脚本**）

1. `npm uninstall -g @openrig/cli` → 移除 CLI 和 npm-postinstall（Node ABI check）
2. `tmux kill-server` → 关闭所有 managed tmux session
3. 手动清理：
   - 删除 `~/.openrig/`（`OPENRIG_HOME` 默认值）
   - 从 `~/.tmux.conf` 移除 `# OpenRig managed block ... # End` 区段
   - 从 `~/.claude.json` 移除 OpenRig 写入的 trust 段和 onboarding completion（**无备份则不可逆**）
   - 从 `~/.codex/config.toml` 移除 OpenRig hook 和 trust entries
   - 删除 `~/.claude/skills/openrig-skills` / `~/.agents/skills/openrig-skills`
   - 删除工作区里的 `.openrig/`、`.claude/settings.local.json` 里的 OpenRig 段、`.mcp.json` 里的 Exa/Context7
4. 重启 Claude Code / Codex 让它们重新加载自己的 config

**这就是为什么「备份 → dry-run → setup」的标准流程至关重要。**

---

## 6. 版本迁移

0.5.9 中 context 库路径 + 遥测存储位置有重大变更。
官方提供 `openrig-upgrade` skill（Agent 操作脚本），分三阶段：准备 → 验证 → 最终化，**支持回滚**。

---

## 7. 待深挖（作者自留问题）

1. **上下文同步与冲突解决**：Claude / Codex 跨模型同步；多 Agent 同时改同一代码库的仲裁机制
2. **容错与重试**：子 Agent 失败/超时时 Owner 的具体策略（指数退避？人工介入？）
3. **效率量化**：相比单 Agent，复杂项目的实际提升 vs 通信开销边际递减
4. **扩展性**：team 规模扩大时通信开销是否瓶颈？是否支持异步解耦？

---

## 我的判断（何大人备注）

**值得试的亮点**
- tmux 持久化 + 快照 = 长任务可中断/可恢复
- 声明式 YAML = 复杂团队可版本化、可复现
- TUI > N 个终端切换

**需要警惕的红线**
- ⚠️ `setup` 会**自动改写** `~/.claude.json` 和 `~/.codex/config.toml`，**先备份再跑**
- Windows / WSL2 不支持（当前服务器是 Linux OK）
- 跨模型冲突仲裁文中没给答案

**跟当前场景契合度**
- 个人单 Agent 跑活儿 → 收益有限
- 想搭"Claude Code + Codex 评审 + 自定义 DevOps Agent"的多 Agent 流水线 → OpenRig 比手撸 tmux 脚本划算

---

## 下一步行动（2026-09-29 待办）

- [x] 深挖 GitHub/npm 源码，列出 `rig setup` 实际写入的具体字段、hook 内容、回滚方法（**已完成**）
- [ ] 备份 `~/.claude.json` 和 `~/.codex/config.toml`
- [ ] 跑 `rig setup --dry-run` 看计划，给何大人拍板
- [ ] 试装后做最小实验（rig + claude code 跑个具体任务）

---

**捕获**：2026-09-29 by Hermes Agent
**原文**：https://mp.weixin.qq.com/s/MVALnklEO5a_xrN1jV7cEw
