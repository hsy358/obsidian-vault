---
title: "OpenWork — Claude Cowork 的开源替代（基于 OpenCode）"
source: github
url: https://github.com/different-ai/openwork
saved_date: 2026-10-28
tags: ["GitHub-分析", "Agent-Platform", "OpenCode", "MCP", "团队协作", "Electron"]
description: "24,289 star，桌面端 Agent 工作台（macOS/Windows/Linux），基于 OpenCode，支持任意模型 + Skill/MCP 团队共享 + 企业控制面自托管"
---

# OpenWork — GitHub 仓库分析

**仓库**: [github.com/different-ai/openwork](https://github.com/different-ai/openwork)
**Star**: 24,289 ⭐ | **语言**: TypeScript 为主（36MB TS + 3.6MB JS）| **默认分支**: `dev`
**创建**: 2026-01-14 | **最近推送**: 2026-10-28（非常活跃）
**官网**: https://openworklabs.com | **文档**: openworklabs.com/docs
**最新版本**: v0.18.63（2026-10-26）
**License**: 目录分割式（见下）

> 一句话：**Claude Cowork 的免费开源替代**——一个桌面应用，AI Agent 在你自己的文件上干实事。底座是 [OpenCode](https://opencode.ai)，模型任意（50+ provider / 自己的 API key / 本地 Ollama），团队可共享 Skill 和 MCP Server。

## 定位

不是 CLI，是**桌面 App**（Electron），macOS / Windows / Linux 全平台。文件留在本地，云可选。

对标产品：Anthropic 的 **Claude Cowork**（以及 Codex 的团队化形态）。

## 核心设计：三条腿

### 1. OpenWork MCP — 从任意 Agent 里用 OpenWork

一个远程 MCP Server，把你分配的 Skill、插件、MCP 连接、Google Workspace、Microsoft 365 能力带进 Claude Code / Codex / Cursor / OpenCode 等任意客户端。

暴露 **4 个工具**：
- `search_capabilities` — 找能用什么
- `execute_capability` — 执行
- `list_skills` / `get_skill` — 列出并读某个 SKILL.md

接入方式（都是一行）：
```bash
codex mcp add openwork --url https://api.openworklabs.com/mcp/agent
claude mcp add --transport http openwork https://api.openworklabs.com/mcp/agent
```
```json
{ "mcp": { "openwork": { "type": "remote", "enabled": true, "url": "https://api.openworklabs.com/mcp/agent", "oauth": {} } } }
```

**关键洞察**：桌面 App 不是必选项——你可以完全不装 App，只在已有 Agent 里挂这个 MCP。能力层（Skill/MCP/连接）跟 UI 解耦。

### 2. OpenWork Den — 企业控制面

- 规模化推理供给 + 管控各团队能用哪些模型 provider
- 邀请成员、建团队、管权限
- 桌面策略、限制本地模型访问、锁定组织允许的 App 版本
- 通过 marketplace 发布 Skill/插件，分配到组织/团队/个人
- 导入 Agent Plugin 或 Anthropic 兼容插件
- **可自托管**在自有基础设施上

### 3. openwork-server — 文件系统后端 API

独立于桌面 App 的服务层，`npm install -g openwork-server` 即可跑。

```bash
openwork-server --workspace /path/to/workspace --approval auto
openwork-server web --open     # 同源提供 UI + API，自管 OpenCode engine
```

- 默认绑 `127.0.0.1`，approval `auto`，workspace = 当前目录
- 首次运行会下载**该版本测试过的确切 OpenCode 版本**到 `~/.openwork/openwork-server/engines/`，之后复用；也可 `OPENWORK_OPENCODE_BIN` 指向自己的 OpenCode
- `web` 模式默认无 CORS 头，且只接受发给 localhost / IP / `--host` 的请求
- 跨机访问建议：server 留在 127.0.0.1，前面挂 TLS 代理（README 举例 `tailscale serve --bg --https=8787`）

## 工程上值得看的两处

### A. 桌面任务恢复（Task Recovery）

`resumeInterruptedTasks` 只在「桌面内嵌自有 engine 的 server」时启用。设计相当严谨：

- `desktop_task_recovery` 表存最多 **1000 条**任务身份：workspace 路径、原 engine、最后观测到的用户轮次、恢复阶段。**不存 prompt、transcript、凭证**
- 退出/更新时：engine teardown 前做最终 checkpoint，**2 个任务快照在途、10 秒预算**
- 重启后：每 2 秒检查 2 个快照，**每 2 秒最多准入 1 个续跑**，最多 2 个恢复任务同时活跃
- 排除项：已完成 / 已归档 / 手动停止 / 被审批或提问阻塞 / 活跃的委派工作；**新的手动操作会让旧的恢复意图失效**
- 安全默认：workspace 缺失、目录变更、策略不可用、快照未验证 → **一律不授权发送**
- V1 要求原始用户轮次和模型都在最近 100 条消息快照里；V2 用会话原生模型
- 续跑时要求 agent **先检查已完成的效果**，而不是重跑原始 prompt
- 准入是**持久化声明式**的：丢失的 ack 绝不盲目重试；崩溃恢复需要「观测到仍在运行的任务 + 仍匹配的未完成轮次」，无法解释的中断保持停止状态
- 文档明确承认：这套机制防的是**重复准入**，**不是**外部工具的 exactly-once 执行

**这套「先声明后发送 + 幂等准入 + 不确定就停下问人」的语义，是多 Agent 编排里最容易做错的地方。**

### B. MCP App 启动所有权（Launch Lease）

MCP App 的启动用**租约（lease）**管理：

- `POST /workspace/:id/mcp-apps/resolve` 返回不透明的 `app.launchId`
- `POST /workspace/:id/mcp-apps/call` **必须**带 launchId + 同 sessionId + 同 engine，服务端把租约绑到自己的实例、workspace、会话、原始 native 启动工具、resource URI 和私有配置指纹
- 派发前重新校验：原工具 App 可见性、resource 绑定与可用性、原工具与请求工具的策略、当前会话归属/归档状态、配置
- 租约进程内有效，**30 分钟过期**，每 server 上限 256 个（先淘汰最老）
- 兼容策略刻意 **fail-closed**：老客户端不带租约调用 → `missing_launch_context`；租约过期 → `stale_launch_context`
- 私有指纹包含：有效配置（含 headers）、相关 MCP 条目的 workspace/global 运行时代次、私有 Connect 授权代次、本地托管网关连接/凭证/注册修订号
- 明确列出**检测不到**的情况：文件配置按观测值比较（改完又改回看不出来）、provider 侧账号变更若不改变宿主可见凭证和配置也检测不到

## 目录结构

| 路径 | 内容 |
|---|---|
| `apps/app` | React UI |
| `apps/desktop` | Electron 壳 |
| `apps/server` | `openwork-server`（MIT） |
| `packages/` | 30 个共享核心包（MIT）——含 opencode-plugin、sandbox、daytona 沙箱、freestyle、computer-use、browser-tabs、email、calendar、documents、workbook、presentation、review、remote-sessions、world、sdk、features（marketplace）… |
| `ee/` | OpenWork Den 控制面 + MCP 网关 + 推理（EE License） |
| `evals/` | 可执行测试规格（`evals/specs/**/*.test.ts` + `.e2e.test.ts`） |
| `worlds/` | 声明式 dev/test 环境定义（`pnpm world`） |
| `.opencode/skills/` | 30 个仓库 agent skill |

`packages/` 里有一批有意思的：`sandbox` / `sandbox-daytona` / `sandbox-freestyle`（沙箱后端）、`computer-use` / `headless-threads` / `browser-tabs`（浏览器与桌面操作）、`openwork-ui-mcp` / `mcp-apps`、`free-auto`、`codemode`、`automations`、`headless-threads`。

## 许可证（重要）

目录分割式，类似 GitLab：

- **`ee/` 之外全部 MIT** — 桌面 App 和核心平台完全开源
- **`ee/` 目录（OpenWork Den）= OpenWork EE License**（source-available）
  - 生产使用需有效订阅
  - **≤5 人组织免费**
  - **任意规模 30 天评估免费**
  - 开发测试永远免费
  - **每个 `ee/` 版本发布满 2 年后自动转为 MIT**
- 采用该许可之前的版本仍是原许可（FSL-1.1-MIT）

对德勤交付的意义：核心是 MIT，可自由商用；企业控制面 ≤5 人免费，这基本覆盖 MVP 阶段。

## 本地开发

前置：**Node 24**（`.nvmrc` 锁定 24.22.1+，运行时会拒绝 25+ 和更老的 24）、**pnpm 11**（`corepack enable`，禁用 npm/yarn）。

```bash
git clone https://github.com/different-ai/openwork.git
cd openwork && corepack enable && pnpm install && pnpm dev
```

测试全部走 `evals/specs/**/*.test.ts`（app-driving 的用 `.e2e.test.ts`）：
```bash
pnpm --dir evals install --frozen-lockfile
pnpm evals:pr specs/<name>.test.ts
pnpm evals:e2e <name> --local
```

多 worktree 并行：`pnpm dev:worktree`（自动派生独立 profile、自动挑空闲 CDP/Vite 端口）。

无 Electron 的 headless web 模式：`pnpm world up dev-app-web --detach`（单实例、只绑 loopback、owner-only manifest 0600、强制 owner bearer 不进 Vite bundle）。

CI：`.github/workflows/` 下有 actionlint、shellcheck、merge-gate、Daytona mac-mini 等，另用 **Sentry Warden** 做 agent 级静态检查（`warden:check`，runtime pi）。

## 安装包体积（要留意）

v0.18.63 每个平台安装包 **250–355 MB**（内嵌 OpenCode engine + Electron）：
- mac-arm64 dmg 342 MB / mac-x64 dmg 354 MB
- linux-x64 AppImage 316 MB
- win-x64 exe 261 MB

三个变体：`openwork` / `openwork-cloud` / `openwork-enterprise`。

## 我的判断

**强项**：
1. **能力层与 UI 解耦**——MCP 4 工具的抽象很干净：搜索能力、执行、列 Skill、读 Skill。这套「capability discovery」接口设计，比堆一堆裸 MCP server 强得多
2. **恢复与幂等语义做得非常严谨**——尤其 "先声明后发送"、"不确定就停下"、"重复准入 ≠ exactly-once" 这几句自我约束，是真跑过生产才写得出来的
3. **fail-closed 兼容策略**——老客户端不带租约直接拒，而不是默默放行
4. MIT 核心 + EE 两年转 MIT，license 设计干净

**风险/成本**：
1. **体量大**（300MB+，且内嵌 engine），CI/网络/磁盘都是成本
2. **商业化色彩浓**——EE 订阅、marketplace、诊断遥测、Daytona 沙箱商务化打包，核心与商业版边界要盯着
3. **迭代极快**（v0.18.63，2026-01 才建仓）→ API 不稳定，AGENTS.md 强调 PR 必须带 evals 证据，说明质量门禁在补
4. 有遥测/诊断包（`ee/packages/telemetry`、`den-diagnostics`），部署前要审

**对德勤项目的可借鉴点**：
1. **Capability 抽象**：把「Skill / 插件 / MCP / SaaS 连接」统一成 capability，用 `search_capabilities` + `execute_capability` 暴露——这跟我们执行器抽象层的方向一致，但 OpenWork 的**能力发现**做得更完整。我们可以直接借这个 API 形状
2. **租约式启动所有权**（launchId + 指纹 + 30 分钟过期 + 256 上限）：MCP App / Tool 调用的授权模型，非常适合用来约束「Agent 能调什么、调的是哪次上下文」
3. **恢复准入语义**（幂等声明、快照验证、不确定就停）：可以直接抄进 Hermes/OpenClaw 执行器 adapter 的失败恢复规范
4. **目录分割许可证** 的商业化设计参考

**结论**：这是目前开源界最接近「Claude Cowork 替代品」的成熟项目，24k star 不到一年做到这个体量，值得持续跟踪。对何大人而言最有价值的可能不是直接用（300MB + 商业边界），而是**它的能力抽象层和租约/恢复语义**这两块设计。
