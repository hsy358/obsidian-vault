---
title: "Multica — Managed Agents Platform（zhangsensen Notion 链接还原）"
author: "zhangsensen（Notion 作者） + 二次源整合"
publish_date: "2026-08-29"
saved_date: "2026-08-29"
source: "notion-reconstructed"
original_url: "https://app.notion.com/p/zhangsensen/Multica-Managed-Agents-Agent-Task-3c146975666d81be805ed2eda329ef52?source=copy_link"
sources:
  - "https://www.multica.ai/docs/agents"
  - "https://dev.to/truongpx396/multica-deep-dive-how-to-build-a-managed-agents-platform-54l2"
  - "https://www.arunbaby.com/ai-agents/0089-multica-agents-as-teammates"
  - "https://www.multica.ai"
type: research-note
tags: [Multica, Managed-Agents, Agent-Task-Board, Backend-Interface, 可插拔执行器, OpenClaw, Hermes, Claude-Code, Codex, Go-Backend, Postgres, WebSocket, 德勤-MVP, AI-Native, Notion-链接]
status: reconstructed
reconstruction_note: "原文是 zhangsensen 的 Notion SPA（无法直接 fetch），本笔记整合 Multica 官方文档 + dev.to 深度解读 + arunbaby 第三方分析的等效内容。"
---

# Multica — Managed Agents Platform

> **注意**：何大人发的 Notion 链接是 zhangsensen 的 Notion SPA，无法直接 fetch（返回空 HTML）。zhangsensen 是 Multica 团队成员。**等效内容**已通过官方文档 + dev.to deep dive 还原。下方所有事实均出自二次源。

> 📌 **本文与 Omnigent 的对位关系**：见末尾"🎯 与 Omnigent 对比"章节。两者同档但定位不同。

## 一句话定位

**Multica**：开源的多 Agent 管理平台（Apache 2.0，~5.5k stars，2079 commits），把 AI 编程 Agent 视为团队成员——assign tasks、track progress、compound skills，从单一仪表盘管理。

> "Multica 不是 agent framework（不写 agent loop），是 management platform（管理已有 agent CLIs）。"
> "CrewAI / LangGraph 是连线工具（how agents talk），Multica 是任务板（how I run agents like a team）。"

## 三个核心变化（同步 → 异步团队协作）

| 变化 | 含义 |
|---|---|
| **Task lifecycle 显式状态机** | enqueue → claim → start → complete/fail；blocker 主动上报，不"silent spin" |
| **Skill compounding（能力复利）** | Agent 解决问题后沉淀为 reusable skill，下次同任务直接复用——单次 Agent 永远从零起 |
| **Agent persistent identity** | Agent 有 profile / 工作量 / 历史 / 成功率，像人类 teammate 一样在 board 上 |

## 架构全景（Three Artifacts from Same Monorepo）

```
┌──────────────────┐
│ Browser / Desktop│
│ (Next.js / EL)   │
└────────┬─────────┘
         │ HTTPS + WS
┌────────▼─────────────────┐
│ Server (Go: Chi + WS)   │ ← source of truth
│ Postgres + (opt) Redis  │
└────────┬────────┬────────┘
         │ WS push │ HTTPS poll (3s)
         │ wakeup  │
┌────────▼────────▼────────┐
│ Daemon on user's laptop │ ← runs the agents
│ (same Go binary, cobra) │
└────────┬────────────────┘
         │ exec.Command
   ┌─────┼─────┬───────┬──────────┐
   ▼     ▼     ▼       ▼          ▼
 claude codex cursor gemini opencode ... (11 backends)
```

| Artifact | Built from | Runs where |
|---|---|---|
| Server binary | `server/cmd/server` | 你的基础设施（Docker/VPS/k8s）|
| multica CLI + daemon | `server/cmd/multica` | 用户笔记本（Homebrew/install.sh）|
| Web app | `apps/web` (Next.js) + `apps/desktop` (Electron) | 浏览器/Mac/Win/Linux |

## 关键抽象 ⭐ Agent Backend Interface（与德勤 MVP 强相关）

> "Multica 最重要的单一决策：不要自己写 agent loop，只写 control plane，把工作派给已存在的 agent CLI。"

```go
// server/pkg/agent/agent.go
type Backend interface {
    Execute(ctx context.Context, prompt string, opts ExecOptions) (*Session, error)
}

type ExecOptions struct {
    Cwd                         string
    Model                       string
    SystemPrompt                string
    MaxTurns                    int
    Timeout                     time.Duration
    SemanticInactivityTimeout   time.Duration // kill if no semantic event in N
    ResumeSessionID             string
    CustomArgs                  []string
    McpConfig                   json.RawMessage
}

type Session struct {
    Messages <-chan Message  // streamed; closes when agent exits
    Result   <-chan Result   // exactly one Result, then closes
}
```

### Factory — 一个新 Agent = 一个新文件

```go
func New(name string, cfg Config) (Backend, error) {
    switch name {
    case "claude":   return newClaude(cfg)
    case "codex":    return newCodex(cfg)
    case "cursor":   return newCursor(cfg)
    case "gemini":   return newGemini(cfg)
    case "copilot":  return newCopilot(cfg)
    case "opencode": return newOpenCode(cfg)
    case "openclaw": return newOpenClaw(cfg)  // ✓
    case "hermes":   return newHermes(cfg)    // ✓
    case "pi":       return newPi(cfg)
    case "kimi":     return newKimi(cfg)
    case "kiro":     return newKiro(cfg)
    }
    return nil, fmt.Errorf("unknown backend %q", name)
}
```

**11 个 backend**，每个约 17–33 KB——加新 agent ≈ 加一个文件。零协议修改、零 DB 迁移、零 UI 改动。

### 标准实现 Pattern（Claude Code ~17 KB）

```go
cmd := exec.CommandContext(ctx, c.path, args...)
cmd.Dir = opts.Cwd
cmd.Env = mergedEnv
stdout, _ := cmd.StdoutPipe()
stdin, _ := cmd.StdinPipe()
stderrTail := newStderrTail(64 * 1024) // bounded ring buffer
cmd.Stderr = stderrTail

cmd.Start()
io.WriteString(stdin, prompt)
stdin.Close()

scanner := bufio.NewScanner(stdout)
scanner.Buffer(make([]byte, 0, 1024*1024), 10*1024*1024) // 10 MB lines

for scanner.Scan() {
    var msg claudeSDKMessage
    if json.Unmarshal(scanner.Bytes(), &msg); err != nil { continue }
    switch msg.Type {
    case "assistant": handleAssistant(msg)  // text/thinking/tool-use; tally tokens
    case "user":      handleUser(msg)       // tool-result
    case "system":    trySend(MessageStatus{...})
    case "result":    finalOutput, finalStatus, finalSessionID = ...
    case "log":       trySend(MessageLog{...})
    }
}
```

**关键招式**：
- `--output-format stream-json`（NDJSON over stdout）流式
- **stderrTail bounded 64KB ring buffer**——没有它，原生 CLI 崩溃只显示"exit status 3"，无诊断
- 自动 approve 所有 tool-use control requests（人工审批已下沉到 issue/comment 层）

### Per-Backend Quirks（值得抄的差异处理）

| Backend | 特殊处理 |
|---|---|
| `claude.go` | `--output-format stream-json` + auto-approve |
| `codex.go` (33 KB) | spawn codex app-server；**per-task CODEX_HOME**（避免 skills 污染系统级）|
| `hermes.go` / `kimi.go` / `kiro.go` | **说 ACP 协议**（Agent Client Protocol） |
| `cursor.go` | Windows 平台差异处理 |
| `openclaw.go` | **不读 workdir 里的 AGENTS.md** → system prompt 全部 inline 传 |
| `models.go` (27 KB) | 静态模型目录 + `ListModels()`，daemon heartbeat 拉取供 UI model picker |
| `version.go` | `DetectVersion(ctx, path)` + `CheckMinVersion(name, version)`——防止 daemon 注册版本过低的 runtime |

## 本地 Daemon 架构（核心循环）

`server/internal/daemon/daemon.go` (~53 KB)

### 启动流程

1. **绑定 health port** :19514，`/health` 端点 → 防止双 daemon 冲突
2. `resolveAuth()` — 从 `~/.multica/config.json` 加载 token
3. `syncWorkspacesFromAPI` — 对每个 workspace：
   - `exec.LookPath` 探测每个 agent CLI
   - 跑 `agent.DetectVersion` + `CheckMinVersion`
   - `POST /api/daemon/register` 上报 `{name, type, version, status}`
   - 缓存返回的 `runtimeIDs`
4. 启动 5 个后台 goroutine：
   - `workspaceSyncLoop` (30s)
   - `taskWakeupLoop` — 打开 daemon WS，监听即时唤醒
   - `heartbeatLoop` (15s) — `POST /api/daemon/heartbeat`（响应可 piggyback：`PendingUpdate` / `PendingModelList` / `PendingLocalSkills` / `PendingLocalSkillImport`）
   - `gcLoop` — 清理 `~/multica_workspaces/` 已完成 issue
   - `serveHealth` — 本地 `/health` JSON

### Poll Loop ⭐（daemon 心脏）

```go
sem := make(chan struct{}, cfg.MaxConcurrentTasks) // default 20

for {
    runtimeIDs := d.allRuntimeIDs()
    for i := 0; i < len(runtimeIDs); i++ {
        sem <- struct{}{}  // acquire slot (blocks if full)
        rid := runtimeIDs[(pollOffset+i)%len(runtimeIDs)]  // round-robin
        task, _ := d.client.ClaimTask(ctx, rid)
        if task != nil {
            wg.Add(1); d.activeTasks.Add(1)
            go func(t Task) {
                defer wg.Done()
                defer d.activeTasks.Add(-1)
                defer func(){ <-sem }()  // release slot
                d.handleTask(ctx, t)
            }(*task)
            break  // claimed; sleep before next round
        } else {
            <-sem  // nothing claimed; release slot
        }
    }
    sleepWithContextOrWakeup(ctx, cfg.PollInterval, taskWakeups)
}
```

**默认参数**：`PollInterval=3s`、`MaxConcurrentTasks=20`、`AgentTimeout=2h`

## 每 Task 隔离 + 原生 Config 注入

**Per-Task Workdir**：`~/multica_workspaces/{ws}/{task}/workdir/` — 每个 task 一个独立目录，**互不干扰**。

**Meta-Skill**：每个 provider 注入对应的"原生 config"：

| Provider | 注入什么 |
|---|---|
| Claude Code | `CLAUDE.md` |
| Codex | `AGENTS.md`（codex 也认）|
| 其他 | 各家 native 文件 |

**Skill Files in Native Skill Directories**：把团队的 skills（markdown bundles）也写到对应 provider 的 skill 目录里。

## Skill Compounding（能力复利系统）⭐

> "Agent 解决一个问题（数据库迁移 pattern、test scaffold）后，**该方案变成全 team reusable skill**。能力随时间复利，不再每次从零起。"

### 三件事保证复利落地

1. **Lockfile reproducible installs** — skill 版本锁
2. **Prompt vs Skill 拆分**：instructions 是 prompt（每次跑），knowledge 是 skill（沉淀复用）
3. **Per-Agent Customization** — agent 在 skills 上叠加私有 layer

## Resumable Sessions（关键工程）

- **Mid-Flight Session Pinning**：任务进行中，pin 住 session ID
- **Resume on Next Claim**：下次 claim 时带 `ResumeSessionID` → 续上原 session
- **Resume Fallback**：session 已失效时从 scratch 启动
- **GC**：清理已完成 task 的 workdir（保留 N 天）

## 服务端数据模型（Postgres 17 + pgvector）

**4 张核心表**：

```
agent           — 身份 / 配置
agent_task_queue — 任务队列
runtime         — daemon 注册的 runtime
task            — 单次 run 的过程 + 结果
```

**Server endpoints**：`claim task` / `start` / `messages (batch)` / `usage` / `complete` / `fail` / `status`

**分层**：`Handler → Service → Repo`（sqlc 生成）

**Polymorphic Actors**：agent / runtime / task 共享一套 actor 抽象

**WebSocket 双子系统**：
- 用户面 WS（前端订阅 dashboard）
- Daemon 面 WS（push wakeup）

**单节点 vs 多节点**：Redis stream fanout 可选（多节点用）

## Autopilot（自动化触发）

- **Cron schedule** —— 定时跑
- **Webhook trigger** —— 外部事件触发
- **Manual** —— 手动跑
- 都是无人工 assign 的 agent run 路径

## 🎯 与 Omnigent 对比（同档但定位不同）

| 维度 | **Omnigent** (Databricks) | **Multica** |
|---|---|---|
| 定位 | **Meta-harness 编排层**（在 Agent 之上套调度）| **Managed Agents Platform**（把 Agent 当 teammate）|
| 主导方 | Databricks（商业公司） | zhangsensen 团队（纯开源） |
| 形态 | 单一 Python 包 + CLI | 三 artifact（Server + Daemon + Web）|
| 核心抽象 | Harness YAML 配置 | Go `Backend` interface |
| 适配 harness | 6 个：Claude Code / Codex / Cursor / OpenCode / Hermes / Pi | **11 个**：Claude Code / Codex / Cursor / Gemini / Copilot / OpenCode / OpenClaw / Hermes / Pi / Kimi / Kiro |
| 跨设备 | ✅（同一 session 终端↔浏览器↔手机）| ✅（dashboard 实时同步）|
| Task Board | ❌（无 board 概念）| ✅ **Linear-shape 任务板**（agent 与人类共视图）|
| Skill 库 | ❌ | ✅ **Skill compounding** |
| 策略治理 | ✅ 三层 Policy + 硬花费上限 | ✅ Access / Concurrency limits |
| 云沙箱 | ✅ Modal / E2B / K8s | ⚠️ 本机 daemon + 自托管 |
| 自托管 | ⚠️ 单机 install | ✅ **Docker Compose 一行命令** |
| 协议 | 自有 | **ACP 协议**（Hermes/Kimi/Kiro 都用）|
| 状态 | alpha (v0.11.0, 9.3k stars) | 早期生产 (5.5k stars, 2079 commits) |
| **对德勤 MVP 启示** | **执行器抽象层设计参考** | **任务生命周期 + 团队协作 + Skill 库参考** |

### **结论**：两者互补，不是二选一

- **Omnigent** 解决「Agent 之上套调度」→ 对位**德勤执行器抽象层**（让 Hermes/Codex/Claude 互换）
- **Multica** 解决「Agent 当 teammate 跑」→ 对位**德勤 Workspace / 项目管理**层（assign task、track、skill 库）

德勤 MVP **同时参考两者**：抽象层用 Omnigent 思路，任务板 + Skill 库用 Multica 思路。

## 与德勤 MVP 强相关借鉴点

按 6-29 何大人决策："Hermes / OpenClaw / Codex / Claude Code 等都是可插拔 Agent 执行器——德勤项目需要设计**执行器抽象层** + **整套系统可单独部署**"。

### 直接可抄的工程范式

| # | Multica 做法 | 德勤 MVP 借鉴 |
|---|---|---|
| 1 | **Backend interface 单一抽象** + **Factory 模式** 11 个 backend | **德勤抽象层 = Backend interface**；德勤适配器 = Hermes/Codex/Claude/OpenClaw 各一个 .go / .py 文件 |
| 2 | **每个 backend 一个 17–33 KB 文件**（exec.Command + JSON 解析） | **避免重写 agent loop**——派给现有 CLI，别自己写 |
| 3 | **Per-Task Workdir 隔离** | **德勤任务执行也用独立 workdir**，避免污染主仓库 |
| 4 | **stderrTail bounded 64KB ring buffer** | **德勤监控也得抄**——CLI 崩溃只显示"exit 3" |
| 5 | **Per-Backend Quirks 表**（CODEX_HOME 隔离、openclaw 不读 AGENTS.md）| **德勤每个适配器都建 Quirks wiki**——避免踩同样的坑 |
| 6 | **5 个后台 goroutine daemon**（workspace / wakeup / heartbeat / gc / health）| **德勤 daemon 同款 5 loop 拆分** |
| 7 | **Poll Loop signal semaphore + round-robin** | **德勤任务派发同款**，避免单 runtime 饿死 |
| 8 | **Skill Compounding 沉淀复利** | **德勤项目最有价值的差异化能力**——客户场景里沉淀的 SOP 都要进 skill 库 |
| 9 | **Linear-shape 任务板**（agent 与人类共视图）| **德勤 Workspace MVP 直接抄**——客户买了多 agent 后能看见每只 agent 在干啥 |
| 10 | **Resumable Sessions + pin session ID** | **德勤长任务必备**——中断续跑从原 session 继续 |
| 11 | **ACP 协议（Hermes/Kimi/Kiro 用）**| **德勤**要**支持 ACP**——Hermes 已是执行器之一，必须接 ACP |
| 12 | **Apache 2.0 + Docker Compose 一行自托管** | **德勤交付形态**——客户私有部署必须 ≤5 分钟启动 |

### 不直接抄的（差异点）

| Multica 选择 | 德勤考量 |
|---|---|
| Go 后端 + Chi + sqlc | 德勤客户有 Java/Python 技术栈——**接口层用 Python（更普及）** + 实现层多语言 |
| Next.js 前端 | 德勤 MVP 前端看客户偏好——可能 Vue/React 都行 |
| Postgres 17 + pgvector | 德勤**多半用客户已有数据库**——抽象层不绑 DB |
| 工作量定义在 daemon 上 | 德勤**直接走云端控制面**——少一层 daemon |
| 每 backend 一个 stdlib JSON 解析 | 德勤可考虑**统一 NDJSON 适配**（像 Omnigent 那样）|

### 🚨 一个真实 bug（dev.to 提的）值得警惕

> "**Strict UUID Parsing**（a real bug in disguise）"
> — Multica 早期版本用严格 UUID v4 校验，所有 32-hex Notion 短码都过不去，后改成宽松格式

**德勤教训**：URL / 引用里的 ID 格式**别假设严格 UUID**——容错优先。

## 行动建议（与德勤 MVP）

按收益排序：

| # | 行动 | 预期收益 |
|---|---|---|
| 1 | **克隆 [multica-ai/multica](https://github.com/multica-ai/multica)** 本地跑通 `docker compose -f docker-compose.selfhost.yml up` | 5 分钟验证平台形态 |
| 2 | **对比 `Backend interface` vs `Omnigent harness YAML`** → 写德勤抽象层 spec | 1-2 周抽象层设计压缩到 2-3 天 |
| 3 | **抄 Skill Compounding 设计** + **Lockfile 锁版本** | 德勤最有差异化能力的部分 |
| 4 | **直接采用 Linear-shape 任务板**作为德勤 Workspace MVP | 节省 2-3 周前端 |
| 5 | **只调研不动手** | ✗ 错过 0.14 → 0.15 的窗口期 |

## 数据 / 引用来源

- 📖 Multica Agents 官方文档：https://www.multica.ai/docs/agents
- 📖 dev.to 深度解读（22k stars 双语言 monorepo 解构）：https://dev.to/truongpx396/multica-deep-dive-how-to-build-a-managed-agents-platform-54l2
- 📖 arunbaby 第三方分析（含 Faros AI / Cognition AI 数据点）：https://www.arunbaby.com/ai-agents/0089-multica-agents-as-teammates
- 📖 Multica 主页：https://www.multica.ai
- 🔗 Notion 原链接（无法直接 fetch）：https://app.notion.com/p/zhangsensen/Multica-Managed-Agents-Agent-Task-3c146975666d81be805ed2eda329ef52?source=copy_link

---

## 🔗 横向关联

- **Omnigent（同期 8-27 公众号文章）**：Meta-harness 编排层，与 Multica 互补
- **Hermes Agent v0.14**（德勤 MVP 唯一执行器）：Multica 已支持 Hermes backend
- **AgentSpace 部署**（/root/AgentSpace）：本地自托管，已验证 AgentRouter ↔ OpenClaw 链路
- **德勤项目 README**：`/root/vault/1-Projects/德勤/README.md`
- **执行器抽象层决策**（6-29）：MEMORY.md "开源研究边界 / 工程全景调研边界" 章节