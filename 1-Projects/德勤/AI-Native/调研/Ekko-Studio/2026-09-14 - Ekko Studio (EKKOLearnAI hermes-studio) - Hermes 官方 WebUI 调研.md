---
title: Ekko Studio (EKKOLearnAI/hermes-studio) - Hermes 官方 WebUI 调研
created: 2026-09-14
tags: [调研, AI-Native, Hermes, WebUI, Ekko-Studio, 多runtime适配, 可借鉴]
source: https://github.com/EKKOLearnAI/hermes-studio
author: EKKOLearnAI (ekko) — 11k stars, 1.3k forks, Forked from NousResearch/hermes-agent
license: MIT
status: 🟢 Very Active Development (v0.7.18, 2026-09-10)
related_projects: [Hermes-Agent-v0.14, 德勤-AI-Native-MVP, AgentSpace, Hermes-Slate-Desk]
related_docs: [2026-07-10 - Hermes Slate Desk - MeeJoy 社区 Hermes 桌面客户端.md]
---

# Ekko Studio (EKKOLearnAI/hermes-studio) - Hermes 官方 WebUI 调研

> **一句话定位**：Hermes Agent 的官方自托管 Web + 桌面客户端（前身叫 Hermes Studio / Hermes Web UI），是当前 Hermes 生态里**最完整的多 runtime 适配实现**——7 个 agent runtime 共用一套 UI + 配置 + 数据库。
>
> **来源**：何大人 2026-09-14 从某视频末尾获知地址（原拼写 `EKKoLearnAl` 是错的，正确为 `EKKOLearnAI`）。

## 0. 拼写差异（重要）

| 引用来源 | 拼写 | 状态 |
|:---------|:-----|:-----|
| 视频截图 / 何大人转引 | `EKKoLearnAl/hermes-studio` | ❌ 404 Not Found |
| 正确 GitHub URL | `EKKOLearnAI/hermes-studio` | ✅ 11.1k stars, 1.3k forks |

差异：第一个 `o` → 大写 `O`，最后 `Al` → 大写 `AI`。
未来引用统一用 **EKKOLearnAI**（注意大写 O + AI）。

## 1. 项目基础信息

| 字段 | 值 |
|:-----|:---|
| 项目名 | Ekko Studio（原 Hermes Studio / Hermes Web UI） |
| GitHub | https://github.com/EKKOLearnAI/hermes-studio |
| npm | `hermes-web-ui`（保留旧名） |
| 官网 | https://ekkostudio.xyz |
| 作者 | EKKOLearnAI（@ekko）|
| License | MIT |
| Stars / Forks | 11.1k / 1.3k |
| 当前版本 | v0.7.18（2026-09-10）|
| 趋势 | GitHub Trending #11（2026-07-17），TypeScript Repo #10（2026-04-17）|
| Forked from | NousResearch/hermes-agent |

> ⚠️ **命名变更**：项目原名 Hermes Studio / Hermes Web UI，现改名 Ekko Studio。但 **GitHub repo 名仍叫 hermes-studio**，npm 包名仍叫 hermes-web-ui——安装和 clone 命令继续用旧名。

## 2. 三大 agent family + 7 个 runtime 适配

| Agent Family | Runtime | Studio 拥有的能力 |
|:-------------|:--------|:------------------|
| **Hermes** | Hermes | Profiles / Providers / Models / Skills / Plugins / Memory / Jobs / Kanban / Channels / MCP / Terminal |
| **Ekko** | Ekko | Ekko 执行 + 审批 + 澄清 + Memory + MCP + provider runtime |
| **Coding** | Claude Code / Codex / Pi / Grok / OpenCode / DSH | Coding-agent 安装、配置、代理、sessions、进程执行 |

> 🎯 **这是关键**：Studio 把 7 个 runtime 装进同一个 UI，靠的是 **runtime adapter 层**——这跟德勤 MVP 的"执行器抽象层"目标**完全一致**。

## 3. Studio 自有 vs Hermes 自有（API 边界）

- **Studio-owned HTTP APIs** → `/api/studio/*`（聊天、群聊、workflow、文件、TTS/STT、媒体、设备、主题、日志、usage、auth、App 联通）
- **Hermes-owned control-plane APIs** → `/api/hermes/*`（profile / skill / plugin / memory / job / channel / MCP / terminal）
- **已发布移动 App** → 一套集中兼容层处理，不再双轨实现

→ 干净的两层架构：**Studio 做"workspace + UX"、Hermes 做"control plane"**。

## 4. 核心模块清单（30+ features）

### 4.1 Chat / Session
- 流式聊天（Socket.IO `/chat-run`）+ thinking 可视化 + tool trace + 文件预览
- 多 session 管理 + Studio 自建 SQLite（Hermes state.db 只读）
- 来源分组（Telegram/Discord/Slack 等）+ 当前 session 置顶 + Markdown 渲染 + 语法高亮 + 代码复制
- Profile 感知模型选择器 + 单 session token 用量徽章
- Ctrl+K session 搜索

### 4.2 Messaging Channels（10 平台）
| 平台 | 配置 |
|:-----|:-----|
| Telegram | bot token + mention control |
| Discord | bot token + mention + auto-thread + allowlist |
| Slack | bot token + mention |
| WhatsApp | enable + mention |
| Matrix | access token + homeserver |
| Feishu (Lark) | app ID/secret |
| DingTalk | client ID/secret |
| QQBot | app ID/secret |
| **WeChat** | QR code login |
| WeCom | bot ID/secret |

→ 凭证统一写到 `~/.hermes/.env`，channel 行为写到 `~/.hermes/config.yaml`。

### 4.3 Workflow（Vue Flow 可视化）
- 节点：Hermes / Ekko / Claude Code / Codex / Pi / Grok / OpenCode / DSH
- 边：directed edges + structured conditions + success/failure routes + loops + approval gates
- Import/export 工作流定义 + profile-aware workspaces
- Run budgets / deadlines / stop/rerun + 持久化执行历史 + frozen snapshots + 节点对话回放

### 4.4 Cron / Kanban
- Cron CRUD + 暂停/恢复 + 立即执行 + 表达式预设
- Profile-aware Kanban 板（plan + 追踪 agent work）

### 4.5 Usage Analytics
- Token 用量拆分（input/output）+ 估算成本 + cache hit rate + 模型分布 + 30 天趋势

### 4.6 Provider 管理
- 自动从 `~/.hermes/auth.json` 凭证池发现模型
- `/v1/models` 拉取每个 provider 可用模型
- Provider CRUD（preset + custom OpenAI-compatible）

## 5. 技术栈

| 层 | 技术 |
|:---|:-----|
| 桌面 | Tauri（或 Electron 二选一）|
| 前端 | Vue / Vue Flow（workflow canvas）|
| 实时通信 | Socket.IO |
| 数据存储 | SQLite（Studio 自建）+ Hermes state.db（只读）|
| 部署 | 桌面应用（macOS/Windows/Linux）+ npm CLI + Docker |

## 6. 对德勤 MVP 的可借鉴点（重点 ⭐）

### 6.1 「Runtime Adapter 层」的真实范本 ⭐⭐⭐
- 7 个 runtime 共用同一 UI——这是德勤 MVP "执行器抽象层" 的目标
- 借鉴点：
  - 适配器边界：每个 runtime 一个 adapter，对外暴露一致接口（start chat / send message / stream / cancel / get session list）
  - Studio-owned vs Runtime-owned 的 API 分层（`/api/studio/*` vs `/api/hermes/*`）→ 德勤 MVP 可以沿用这个思路

### 6.2 微信 / 飞书 / 钉钉 channel 适配
- Ekko Studio 已经实现了 WeChat QR login + Feishu app ID/secret + DingTalk client ID/secret
- **关键问题**：开源实现的成熟度如何？是否有反限制措施？需要 review 代码再决定借鉴方式
- 德勤 MVP 客户多半是大企业 + 国央企 → 飞书 + 钉钉 + 企微是刚需

### 6.3 视觉化工作流（Vue Flow）
- 节点 + 边 + 条件路由 + 审批门 → 适合"业务流编排"场景
- 德勤 MVP 如果面向业务用户（不仅是开发者），这个 UX 很关键
- 比 LangGraph 的 StateGraph 更友好（拖拽 vs 写代码）

### 6.4 Token 用量 + 成本分析
- Studio 直接做了 usage dashboard，对德勤 MVP 的"成本可控"卖点很有说服力

### 6.5 不要借鉴的点
- 桌面客户端（Tauri/Electron）→ 德勤 MVP 应该是纯 Web，桌面应用是另一个工程量
- Studio 自建 SQLite session 库 → 何大人 MVP 阶段不需要，直接用 Hermes state.db 即可

## 7. 与已有调研的关系

| 项目 | 对比 | 互补关系 |
|:-----|:-----|:---------|
| **Hermes Slate Desk** (MeeJoy) | 极简桌面客户端，做减法 | Ekko Studio 是 Hermes 官方"全家桶"，MeeJoy 是第三方极简版 |
| **LangGraph adapter** (vault/executor/) | StateGraph 编程范式 | Ekko Studio 是可视化范式，两者互补 |
| **OpenJiuwen 工程栈** | 国内同类平台 | Ekko Studio 是开源国际版，OpenJiuwen 是国内商业版 |

## 8. 待办（follow-up）

- [ ] clone 代码 → `/tmp/ekko-studio/`，本地跑通 desktop app
- [ ] 重点 review `packages/runtime-adapters/` → 看 7 个 runtime adapter 的接口设计
- [ ] review 微信 / 飞书 / 钉钉 channel 实现 → 评估成熟度 + 反限制
- [ ] 跟德勤 MVP 的 `executor/abstract-interface.md` 对照 → 看哪些字段能直接借鉴
- [ ] 调研 Ekko 自己的 agent runtime（跟 Hermes 啥关系）→ 可能影响德勤 MVP 的执行器选型

## 9. 引用

- GitHub: https://github.com/EKKOLearnAI/hermes-studio
- Releases: https://github.com/EKKOLearnAI/hermes-studio/releases
- Issues: https://github.com/EKKOLearnAI/hermes-studio/issues
- npm: https://www.npmjs.com/package/hermes-web-ui
- 官网: https://ekkostudio.xyz
- 趋势: https://trendshift.io/repositories/27306

---
**归档原因**：何大人 2026-09-14 23:29 转引某视频末尾的 GitHub 地址，因拼写错误 404，搜索后找到正确项目。强挂钩德勤 MVP（执行器抽象层 + 微信/飞书/钉钉 channel + 视觉化工作流），故存档到 `1-Projects/德勤/AI-Native/调研/Ekko-Studio/`。