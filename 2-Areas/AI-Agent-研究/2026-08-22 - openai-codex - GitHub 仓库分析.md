---
type: github-repo-analysis
title: openai/codex - Codex Harness 全栈开源
repo_url: https://github.com/openai/codex
repo_owner: openai
repo_name: codex
license: Apache-2.0
primary_language: Rust
secondary_languages: TypeScript, Python, Starlark
stars: 111730
forks: 17174
open_issues: 13418
latest_release: rust-v0.149.0 (2026-08-20)
analyzed_date: 2026-08-22
tags: [agent-harness, code-execution, app-server, code-mode, mcp, rust, openai, executable-plugins, skill-protocol]
related_projects: [Hermes, OpenClaw, LangGraph, Paperclip]
status: stable
---

# openai/codex - Codex Harness 全栈开源

> 来源：何大人 2026-08-22 微信消息
> "项目地址是 github.com/openai/codex，这次开源的 Codex Harness 就在这个仓库里，采用 Apache-2.0 协议，包含 codex exec、Codex SDK 和 app-server 三个核心组件。"

## 一句话定位

OpenAI 把生产环境的 **Codex CLI + Codex Harness 整体开源**（不只是 CLI 工具）—— **111k stars、17k forks、13418 open_issues、Apache-2.0**，Rust monorepo + TypeScript/Python SDK + JSON-RPC 协议层 + 完整 Agent 执行栈。

---

## 1. 仓库基本面

| 字段 | 值 |
|---|---|
| 仓库 | https://github.com/openai/codex |
| 创建 | 2025-04-13 |
| 协议 | **Apache-2.0**（商业友好） |
| 主语言 | **Rust**（codex-rs monorepo） |
| Stars / Forks / Issues | **111,730 / 17,174 / 13,418** |
| 最新稳定 | rust-v0.149.0（2026-08-20） |
| 最新 alpha | rust-v0.150.0-alpha.6（2026-08-21）|
| 体积 | 566 MB（git size） |
| 默认分支 | main |
| 状态 | 活跃开发，每天 5-10 个 commit |

**对比参照**：
- 我们 vault 里之前最大的 Agent Harness 项目是 `Harness Handbook`（论文 + 项目），Codex 是**工业级生产代码**
- 跟 `codex` 同类的项目：LangGraph、Paperclip、Goose、Routa、Hermes Desktop、Harnss —— 但只有 Codex 是 OpenAI 自己生产环境用的

---

## 2. 三大核心组件（何大人说的）

### 2.1 codex exec —— CLI 执行引擎

实际仓库布局（比何大人说的更细）：

```
codex-rs/cli/src/                  ← CLI 外壳（171k main.rs + 17 个子命令模块）
├── main.rs              (171k!)   ← clap 命令路由器
├── app_cmd.rs                     ← app 子命令入口
├── debug_sandbox.rs     (40k)     ← 沙箱调试
├── doctor.rs            (151k!)   ← 诊断系统
├── exec_server_telemetry.rs        ← 执行服务遥测
├── login.rs             (20k)     ← ChatGPT/Auth 登录
├── marketplace_cmd.rs   (18k)     ← 插件市场
├── mcp_cmd.rs           (37k)     ← MCP 子命令
├── plugin_cmd.rs        (28k)     ← 插件管理
├── queue_cmd.rs         (1.8k)    ← 远程队列
├── remote_control_cmd.rs (27k)    ← 远程控制
├── migrate_rollouts.rs  (14k)     ← 会话迁移
└── ...

codex-rs/exec/src/                 ← 非交互式执行（lib.rs 78k）
├── cli.rs              (9.5k)     ← exec CLI
├── event_processor.rs  (1.5k)     ← 事件分发
├── exec_events.rs      (10k)      ← 事件类型
├── event_processor_with_human_output.rs (19k)
├── event_processor_with_jsonl_output.rs (26k)
├── lib.rs              (78k)      ← 执行核心
└── main.rs             (1.4k)

codex-rs/exec-server/              ← 远程执行服务
├── README.md            (12k)     ← **双模式 + Noise 加密 + 多路复用协议**
├── src/
└── tests/

codex-rs/execpolicy/               ← Starlark 策略引擎
├── README.md            (4.1k)
├── src/
├── examples/
└── tests/
```

**注意**：CLI 的 `main.rs` 高达 171k 字节，是**完整平台**而不是普通 CLI。它包含 17 个子命令模块 + `desktop_app/` + `bin/` 子目录。

### 2.2 Codex SDK —— 双语言 SDK

```
sdk/
├── typescript/                       ← @openai/codex-sdk
│   ├── package.json (version 0.0.0-dev)
│   ├── tsup + jest
│   └── Node >= 18
└── python/                           ← openai-codex
    ├── pyproject.toml (version 0.0.0-dev)
    ├── uv_build >= 0.11.19
    ├── pydantic >= 2.12
    └── 依赖：openai-codex-cli-bin==0.147.0
```

**关键观察**：**Python SDK 直接依赖 `openai-codex-cli-bin`**（=预编译的 Rust CLI 二进制）—— 也就是说 **SDK 是 CLI 的薄包装**，不是独立实现。这是**务实架构**。

### 2.3 app-server —— JSON-RPC 协议层

```
codex-rs/app-server/                 ← 应用服务器核心
├── README.md            (178k!)    ← 完整协议规范
├── Cargo.toml           (4.7k)
└── src/

codex-rs/app-server-protocol/        ← 协议 schema
├── schema/                          ← JSON Schema 定义
├── scripts/
└── src/

codex-rs/app-server-client/          ← 客户端
codex-rs/app-server-daemon/          ← 守护进程
codex-rs/app-server-test-client/     ← 测试客户端
codex-rs/app-server-transport/       ← 传输层抽象
codex-rs/app-server-protocol-noop-macros/
```

**app-server 协议设计**（来自 178k README 摘录）：

| 项目 | 内容 |
|---|---|
| 协议 | **JSON-RPC 2.0**（去掉 `"jsonrpc":"2.0"` 头） |
| 传输 | **stdio / websocket / unix socket / off** 四种 |
| 三层抽象 | **Thread → Turn → Item**（嵌套会话模型） |
| 生命周期 | `initialize` → `initialized` → `thread/start` → `turn/start` → 事件流 → `turn/completed` |
| 事件 | `item/started`、`item/completed`、`item/agentMessage/delta`、`rawResponseItem/*` |
| 健康检查 | `GET /readyz`、`GET /healthz`（HTTP 探针）|
| Backpressure | 错误码 `-32001` + 客户端指数退避 |
| 持久化 | thread 可 archive / resume / fork / ephemeral |
| 隔离 | 每连接独立 handshake，重复 `initialize` 报 `"Already initialized"` |
| Schema 生成 | `codex app-server generate-ts` / `generate-json-schema` |
| MCP 扩展 | 客户端在 `initialize.capabilities.extensions` 声明 |

**为什么这是关键设计**：app-server 把 Agent 交互**协议化** —— IDE（VS Code/Cursor/Windsurf）、桌面 App、Web、SDK 全部走同一份 JSON-RPC 协议。**这是 OpenAI 的"前端/后端分离"**。

---

## 3. 完整 crate 地图（70+ 子 crate）

### 3.1 核心域（core 依赖图）

```
codex-core（核心领域逻辑，AGENTS.md 明确"resist adding code to codex-core"）
├── codex-agent-graph-store        ← Agent 图存储（多 Agent 协作基础设施）
├── codex-apply-patch              ← 结构化文件编辑协议（lib.rs 47k + invocation.rs 35k + streaming_parser.rs 34k）
├── codex-code-mode                ← Code Mode（grpc_session + remote_session 远程会话）
├── codex-context-fragments        ← 上下文片段（additional_context.rs + fragment.rs）
├── codex-extension-api            ← 扩展 API
├── codex-mcp                      ← MCP 集成
├── codex-config                   ← 配置系统
├── codex-exec-server              ← 执行服务
├── codex-execpolicy               ← 执行策略
├── codex-collaboration-mode-templates ← 协作模式（plan.md 等）
├── codex-connectors               ← 连接器
├── codex-diagnostics              ← 诊断
└── ...
```

### 3.2 平台层

```
codex-app-server*（7 个 crate，完整协议栈）
codex-cloud-tasks*（云任务，4 个 crate）
codex-core-plugins（插件系统，60 个 .rs 文件）
├── marketplace_add / marketplace_upgrade / remote / startup_sync
├── agent_plugin_manifest.rs / discoverable.rs
├── artifact_operation.rs / app_mcp_routing.rs
└── command_migration.rs
codex-chatgpt（ChatGPT 集成）
codex-cloud-config
```

### 3.3 工具与基础设施

```
codex-async-utils / codex-ansi-escape
codex-bwrap（Linux 沙箱）
codex-aws-auth
codex-backend-client / codex-backend-openapi-models
codex-apply-patch / codex-mcp / codex-features / codex-history
codex-http-client / codex-api / codex-client
codex-home / codex-utils-cli / codex-utils-pty
codex-tools（工具集）
codex-tui（TUI 实现）
```

### 3.4 协议与构建

```
codex-app-server-protocol（独立 schema crate）
codex-app-server-protocol-noop-macros（过程宏）
codex-arg0（argv[0] 处理）
bazel/（Bazel 构建系统，不只 Cargo）
third_party/ / patches/
```

**关键观察**：
- 用 **Bazel + Cargo 双构建**（`MODULE.bazel` 1.5M，`MODULE.bazel.lock` 1.5M）
- `AGENTS.md` 明确写："If you change Rust dependencies, run `just bazel-lock-update`"
- `defs.bzl` 31k —— **自建 Bazel 规则**
- `justfile` 7.5k —— **just 任务系统**

---

## 4. Code Mode —— 新执行范式

```rust
codex-rs/code-mode/src/
├── grpc_session/                ← gRPC 会话
├── remote_session/              ← 远程会话
│   ├── lib.rs                   (356B)
│   ├── remote_session.rs        (20k)   ← 远程会话主逻辑
│   └── remote_session_tests.rs  (15k)
```

`app-server` README 提到：
> Pass `--code-mode-host URL` to connect this app-server process to a remote code-mode host instead of starting a local host. Use `ws://` or `wss://` for the WebSocket protocol, or a root `http://` or `https://` URL without a path or query for gRPC.

**Code Mode = Agent 直接执行代码的远程执行环境**，支持：
- gRPC transport（HTTP/2）
- WebSocket transport（WS/WSS）
- 出站连接独立于 `--listen`
- 共享于进程内所有线程

---

## 5. exec-server —— 远程执行的多路复用协议

来自 `codex-rs/exec-server/README.md`（12k 字节）：

### 5.1 两种模式

```bash
# 本地模式：WebSocket JSON-RPC
codex exec-server --listen ws://localhost:8080

# 远程模式：Noise 加密 WebSocket + 二进制 protobuf
codex exec-server \
  --remote https://remote.codex.example \
  --environment-id "$ENVIRONMENT_ID" \
  CODEX_API_KEY="$OPENAI_API_KEY"
```

### 5.2 Remote Relay Message Format

```
version
stream_id           ← UUIDv4，每会话独立
traceparent         ← W3C distributed tracing
tracestate          ← W3C vendor state
body                ← handshake | data | ack_frame | resume | reset | heartbeat
ack                 ← 最高连续对端 segment seq
ack_bits            ← 对端 seq 位图
seq                 ← segment 序列号
segment_index       ← 段索引（0-based）
segment_count       ← 段总数
payload             ← handshake bytes 或加密数据
next_seq            ← resume 专用
reason              ← reset 专用
```

**核心特性**：
- **多路复用**：UUIDv4 `stream_id` 隔离会话，每 stream 独立 `ConnectionProcessor`
- **可靠性**：segment-level seq + 滑动窗口（ack + ack_bits）
- **可恢复**：`resume` 帧支持断线续传
- **可观测**：W3C `traceparent` / `tracestate` 标准分布式追踪
- **加密**：Noise protocol + 二进制 protobuf relay frames

---

## 6. execpolicy —— Starlark 策略引擎

来自 `codex-rs/execpolicy/README.md`：

### 6.1 策略语法（Starlark）

```starlark
prefix_rule(
    pattern = ["cmd", ["alt1", "alt2"]],   # 有序 tokens；list 表示 alternatives
    decision = "prompt",                   # allow | prompt | forbidden
    justification = "explain why",
    match = [["cmd", "alt1"]],             # 必匹配示例（自带单元测试）
    not_match = [["cmd", "oops"]],         # 必不匹配示例
)

host_executable(
    name = "git",
    paths = ["/opt/homebrew/bin/git", "/usr/bin/git"],
)
```

### 6.2 决策严格度

```
forbidden > prompt > allow   # 严格度排序
```

### 6.3 关键特性

- **Starlark 语法**（来自 Bazel 生态）
- **`match` / `not_match` = 自带单元测试**（load-time 验证）
- **CLI 子命令**：`codex execpolicy check --rules file rules...`
- **`--resolve-host-executables`**：basename 回退开关
- **`justification` 可选**：human-readable rationale（在 approval prompt 中显示）
- **多文件合并**：多次 `--rules` 按顺序合并评估

### 6.4 与 LangGraph 等的对比

| 项目 | 策略语言 | 决策模型 |
|---|---|---|
| Codex execpolicy | **Starlark**（Bazel 生态） | allow / prompt / forbidden |
| LangGraph | Python 装饰器 | checkpointer + interrupt |
| Hermes | （未明确） | （未明确） |
| Paperclip | （未明确） | （未明确） |

**Starlark 选择很聪明**：data-only（无副作用）、可沙箱执行、可单元测试。

---

## 7. Plan Mode（来自 `collaboration-mode-templates/templates/plan.md`）

**3 阶段对话式 Plan Mode**：

1. **Plan Mode 严格性**："Plan Mode is not changed by user intent, tone, or imperative language"
2. **`update_plan` 工具 vs Plan Mode 严格分离**："If you try to use `update_plan` in Plan mode, it will return an error"
3. **Plan 必须 decision complete**："It must be **decision complete**, where the implementer does not need to make any decisions."
4. **mutation / non-mutation 严格区分**：
   - Allowed：reading, searching, static analysis, dry-run, tests
   - Not allowed：editing, writing, applying patches, migrations, codegen, side-effectful commands

**跟 OpenClaw 的 `update_plan` 工具完全一致** —— 工具是工具，模式是模式，不能混用。

---

## 8. Codex 自带的 Skills 与 Environment

```
.codex/                              ← Codex 自带的开发配置
├── environments/
│   └── environment.toml             ← 沙箱环境配置（301B）
└── skills/                          ← Codex 自带的 Skills
    ├── babysit-pr/
    ├── code-review/
    ├── code-review-breaking-changes/
    ├── code-review-change-size/
    ├── code-review-context/
    ├── code-review-testing/
    ├── codex-pr-body/
    ├── path-types/
    ├── remote-tests/
    ├── test-tui/
    └── update-v8-version/
```

**跟我们 vault 的对比**：MEMORY.md 提"Claude/Codex/Codebuddy 通过软链接共享 skills" —— 现在 Codex 自己**原生支持 skills 目录**（`.codex/skills/`），跟我们的软链架构是同源理念。

**Codex 自带的 11 个 skill 全是开发流程**：PR 监护、6 维代码评审、TUI 测试、V8 版本升级。

---

## 9. 工程规范（来自 `AGENTS.md`，22k 字节）

### 9.1 Rust 工程风格

- **`#[async_trait]` 和 `#[allow(async_fn_in_trait)]` 双禁**
  - 优先用 native RPITIT trait methods with explicit `Send` bounds
  - 推荐：`fn foo(&self, ...) -> impl std::future::Future<Output = T> + Send;`
- **`format!` 参数必须 inline**（`"text {var}"` 而非 `"text " + var`）
- **`if` 必须 collapse**（`collapsible_if` lint）
- **`match` 必须 exhaustive**，避免 wildcard arms
- **bool/Option 参数避免** —— 用 enum/named method/newtype（避免 `foo(false)` 这种 hard-to-read 调用）
- **argument comment lint**：`/*param_name*/` 注释前置 opaque literal（`None`、bool、数字）
- **module < 500 LoC**，文件超过 800 LoC 必须拆模块

### 9.2 模型上下文不变量

```
1. No history rewrite - 上下文必须增量构建
2. Avoid frequent changes to context that cause cache misses
3. No unbounded items - 每项必须有有界大小和硬上限
4. No items larger than 10K tokens
5. Highlight new individual items that can cross >1k tokens as P0
6. All injected fragments must be defined as structs in `core/context` 
   and implement ContextualUserFragment trait
```

### 9.3 破坏性变更检查清单

```
- app-server APIs
- raw response item events (rawResponseItem/*)
- CLI parameters
- configuration loading
- resuming sessions from existing rollouts
```

### 9.4 PR 大小限制

```
- 总变更 < 800 行
- 复杂逻辑变更 < 500 行
- 必须拆成可 review 的阶段
```

### 9.5 测试规范

- **集成测试 > 单元测试**（在 `core/suite` 用 `test_codex`）
- Agent 逻辑变更**必须有集成测试**
- 测试模块放独立文件 `xxx_tests.rs`，用 `#[path = "..."]` 引用
- **Snapshot 测试用 insta**（特别 TUI 输出）
- **UI 变更必须更新 snapshot**

### 9.6 模块组织

- **新增概念先想清楚放在哪个 crate**（不直接塞 `codex-core`）
- **`codex-core` 是反模式**：AGENTS.md 明确"resist adding code to codex-core"
- **tracing 用 `#[tracing::instrument]`**（不用 `.instrument()` 附加 span）
- **避免一次性小辅助方法**（只被引用一次就别拆）

### 9.7 Bazel 集成

```
If you change Rust dependencies (Cargo.toml or Cargo.lock), 
run `just bazel-lock-update` from the repo root to refresh 
MODULE.bazel.lock, and include that lockfile update in the same change.
```

---

## 10. 架构总览图

```
┌─────────────────────────────────────────────────────────────────┐
│                          用户界面层                              │
├─────────────────────────────────────────────────────────────────┤
│  CLI (171k)            Desktop App         IDE Extensions       │
│  • 17 subcommands      • chatgpt.com       • VS Code            │
│  • debug_sandbox       • TUI (ratatui)     • Cursor             │
│  • doctor              • marketplace       • Windsurf           │
│  • plugin/mcp                                  │                │
│  • queue/remote_control                         │                │
└──────────────────────────┬──────────────────────────────────────┘
                           │ JSON-RPC 2.0 (stdio/ws/unix)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              app-server 协议层（7 个 crate）                       │
│  app-server-protocol  →  app-server  →  app-server-daemon       │
│  app-server-client    →  app-server-test-client                 │
│  app-server-transport →  app-server-protocol-noop-macros         │
│                                                                  │
│  Thread → Turn → Item 三层抽象                                   │
│  initialize / thread/start / turn/start / item/* 事件            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   codex-core 核心域                              │
│  agent-graph-store │ apply-patch │ code-mode │ context-fragments │
│  mcp │ config │ exec-server │ execpolicy │ collaboration-mode   │
│  connectors │ diagnostics │ extension-api │ core-plugins        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌─────────┐  ┌──────────┐  ┌──────────┐
        │ exec    │  │ exec-    │  │ cloud-   │
        │ (CLI)   │  │ server   │  │ tasks    │
        │ 78k lib │  │ (远程)   │  │ (云任务) │
        └─────────┘  └──────────┘  └──────────┘
                           │
                           ▼
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌─────────┐  ┌──────────┐  ┌──────────┐
        │ 沙箱    │  │ 追踪     │  │ 凭据     │
        │ bwrap/  │  │ tracing  │  │ aws-auth │
        │ sandbox │  │ W3C      │  │ OAuth    │
        └─────────┘  └──────────┘  └──────────┘
```

---

## 11. 跟 MEMORY.md 中"Agent 执行器"的对应关系

> MEMORY.md §工程全景调研边界（2026-06-29 何大人明确）：
> **"Hermes / OpenClaw / Codex / Claude Code 等都是可插拔 Agent 执行器 —— 德勤项目需要设计执行器抽象层，每种都能接"**

| 维度 | Codex | Hermes | OpenClaw | Claude Code | LangGraph |
|---|---|---|---|---|---|
| 语言 | Rust | (查) | (查) | (查) | Python |
| 协议层 | **JSON-RPC 2.0** | (查) | (查) | (查) | Python API |
| 执行策略 | **Starlark** | (查) | (查) | (查) | 装饰器 |
| 文件编辑 | **apply-patch 单独 crate** | (查) | (查) | (查) | (查) |
| 多 Agent 协作 | **agent-graph-store** | (查) | (查) | (查) | Graph |
| 沙箱 | **bwrap + sandbox** | (查) | (查) | (查) | 无 |
| Plan 模式 | **3 阶段对话 + mutation 隔离** | (查) | (查) | (查) | (查) |
| Skills | **`.codex/skills/` 原生** | (查) | (查) | (查) | 无 |
| 远程执行 | **Noise + 多路复用** | (查) | (查) | (查) | 无 |
| MCP | **内置 codex-mcp crate** | (查) | (查) | (查) | Adapter |
| 插件市场 | **marketplace_cmd** | (查) | (查) | (查) | 无 |
| Cloud Tasks | **独立 4 crate** | (查) | (查) | (查) | 无 |

---

## 12. 借鉴点索引（给德勤 MVP）

按 MEMORY.md §开源研究边界：**不**问 "Codex 替代 Hermes 吗"，**只**问 "Codex 的什么技术可借鉴到 Hermes-based 德勤 MVP"。

### 12.1 协议层（强借鉴）⭐⭐⭐

**app-server JSON-RPC 协议** → 德勤 MVP 的"执行器抽象层"
- 4 种 transport（stdio/ws/unix/off）—— 德勤 MVP 至少需要 stdio + ws
- Thread → Turn → Item 三层抽象 —— 德勤 MVP 也需要这个模型
- Backpressure -32001 + 指数退避 —— 客户端必须实现
- `codex app-server generate-ts` / `generate-json-schema` —— **一站式生成多语言 SDK** 是黄金范式
- `/readyz` + `/healthz` 健康检查 —— 德勤 MVP 必须有

### 12.2 多路复用协议（强借鉴）⭐⭐⭐

**exec-server Noise + protobuf + 多 stream + ack/ack_bits**
- 德勤 MVP 多 Agent 并行执行时，**UUIDv4 stream_id + ConnectionProcessor** 几乎是必须
- W3C `traceparent` 标准化追踪 —— 德勤 MVP 直接用 OpenTelemetry SDK
- `resume` 帧支持断线恢复 —— 德勤 MVP 长期任务必备

### 12.3 执行策略（强借鉴）⭐⭐

**Starlark-based execpolicy** → 德勤 MVP 的工具调用权限系统
- `prefix_rule + decision + justification + match + not_match` —— **策略自带单元测试**这点很先进
- `host_executable` 约束可执行路径 —— 德勤 MVP 多租户隔离需要
- `codex execpolicy check` CLI 子命令 —— 德勤 MVP 可作为独立工具

### 12.4 文件编辑协议（强借鉴）⭐⭐

**apply-patch 独立 crate**（lib.rs 47k + invocation.rs 35k + streaming_parser.rs 34k）
- 结构化 patch（Heredoc 格式）—— 不是 freeform text edit
- **streaming_parser** —— 大 patch 流式解析
- standalone_executable —— 可作为独立工具复用
- 德勤 MVP Agent 改文件应该用这种结构化协议

### 12.5 Plan Mode（借鉴理念）⭐⭐

**3 阶段对话式 Plan + mutation 严格隔离 + decision complete**
- 德勤 MVP 的 plan 模式可以参照
- "Plan Mode vs update_plan 工具严格分离" —— 跟 OpenClaw `update_plan` 工具理念一致

### 12.6 Skills 原生支持（借鉴）⭐

**`.codex/skills/` 原生目录** —— 跟我们 vault 的 skill 软链架构同源
- MEMORY.md 提"Codex 通过软链共享 skills"—— 现在 Codex 自带原生支持
- 德勤 MVP 可以用 `.codex/skills/` 风格作为 Skill 发现机制

### 12.7 MCP 内置（借鉴）⭐

**codex-mcp 是 core 一等公民**（不是 adapter）
- 德勤 MVP 的 MCP 集成可参考这种"内置而非外挂"设计

### 12.8 插件市场（借鉴）⭐

**marketplace_cmd + core-plugins 60 文件**
- 插件元数据（agent_plugin_manifest.rs）+ discoverable 机制
- 远程 marketplace + 本地 marketplace + Git marketplace
- 德勤 MVP 可作为后续扩展

### 12.9 Agent 协作（借鉴）⭐⭐

**agent-graph-store** —— 多 Agent 图存储
- MEMORY.md §工程全景调研边界 提到"组织控制"
- 德勤 MVP 多 Agent 协作可参考此架构

### 12.10 Code Mode（新范式，观望）⭐

**grpc_session + remote_session** —— Agent 直接执行代码
- 这是 OpenAI 的新方向，**还在早期**
- 德勤 MVP 可以先观察，不急着实现

### 12.11 Cloud Tasks（观望）⭐

**cloud-tasks 独立 4 crate** —— 云端异步任务
- 跟德勤 MVP 的"长期任务调度"需求相关
- 但当前不急，先专注本地执行

---

## 13. 不借鉴的（明确）

按 MEMORY.md §开源研究边界 + 2026-07-09 §Yuxi §Simplicity First：
- ❌ **不引入 Bazel**：德勤 MVP 用 Cargo + pnpm 已经够，**Bazel 是过度工程**（学习成本、构建时间、维护负担）
- ❌ **不引入 Starlark**：Python 装饰器已经够用，**Starlark 数据栈是无必要的复杂度**
- ❌ **不抄 marketplace 完整插件系统**：v3 教训（写 5 条风控规则没一条执行），德勤 MVP 先 core 跑通
- ❌ **不抄 Cloud Tasks**：当前需求不匹配
- ❌ **不照搬 Plan Mode 3 阶段对话**：交互范式取决于终端用户

---

## 14. 待验证 / 未确认

| 项 | 状态 | 验证方式 |
|---|---|---|
| Codex 是否真的"开源 Harness"（vs 只开源 CLI） | ✅ 已确认 —— 整个 monorepo 70+ crate 都开源 |
| app-server 协议稳定性 | ⚠️ `experimental` 标签多 | 跟踪 release notes |
| exec-server 是否能在生产用 | ⚠️ WebSocket transport 标 "experimental / unsupported" | 跟踪稳定性 |
| execpolicy 是否 production-ready | ⚠️ README 写 "still in preview. The API may have breaking changes" | 等稳定 |
| SDK 0.0.0-dev | ⚠️ 版本未发布 | 等 1.0 |
| apply-patch 是否兼容 OpenAI Function Calling schema | ❓ 未验证 | 后续查 |
| Code Mode 完整规范 | ❓ README 178k 未读完 | 后续读 |
| agent-graph-store 数据模型 | ❓ 未读源码 | 后续读 |
| MCP extensions 协议 | ❓ 未读 | 后续读 |

---

## 15. 行动建议

按 MEMORY.md §Goal-Driven Execution（"先有 verifiable goal 再动手"）：

1. **本机升级 codex**：`codex 0.128.0` → `0.149.0`（有 21 个版本差距）—— verify: `codex --version`
2. **深读 3 个核心文档**：
   - `codex-rs/app-server/README.md`（178k）
   - `codex-rs/exec-server/README.md`（12k）
   - `codex-rs/execpolicy/README.md`（4.1k）
3. **本地跑通 Plan Mode**：用 `codex` 进入 Plan 模式，验证 mutation 隔离
4. **本地跑通 exec-server**：用 Noise 模式启动一个远程会话
5. **写借鉴技术文档**到 `/root/vault/1-Projects/德勤/AI-Native/executor/`
   - `2026-08-22 - Codex-app-server-协议借鉴.md`
   - `2026-08-22 - Codex-exec-server-多路复用借鉴.md`
   - `2026-08-22 - Codex-execpolicy-策略借鉴.md`
6. **把 apply-patch 协议抄一份**作为 Hermes 的标准文件编辑协议（verify: 跟现有 Hermes 行为兼容）

---

## 16. 仓库统计摘要

```
总代码量：codex-rs/ ~ 70+ crate，~200+ .rs 文件
总文档量：app-server README 178k，AGENTS.md 22k
总 stars：111,730（远超 Harness Handbook 等同类）
总 commits：每天 5-10 个 commit（高度活跃）
release 节奏：alpha 每 1-2 天，稳定版每 1-2 周
发布渠道：rust-vX.Y.Z-alpha.N → rust-vX.Y.Z
构建系统：Bazel + Cargo 双系统（justfile 任务协调）
CI：jjust argument-comment-lint + rustfmt + clippy + insta snapshot
测试：集成测试在 core/suite，单元测试在 xxx_tests.rs
```

---

## 17. 关联项目

- **同仓库**：
  - `codex-rs/`（Rust monorepo，主代码）
  - `sdk/typescript/`（@openai/codex-sdk）
  - `sdk/python/`（openai-codex）
  - `codex-cli/`（CLI wrapper）
- **vault 同类研究**：
  - `2026-06-12 - Goose - Deep Research.md`
  - `2026-06-12 - Harnss - Deep Research.md`
  - `2026-06-12 - Hermes Desktop - Deep Research.md`
  - `2026-06-12 - Routa - Deep Research.md`
  - `2026-06-12 - muselab GitHub 仓库分析.md`
  - `2026-07-30 - Harness Handbook - 论文核心要点 + 项目分析.md`
  - `2026-07-30 - OpenCodeReview - 阿里开源 AI 代码审查工具（混合架构）.md`
  - `2026-08-05 - TencentDB Agent Memory - GitHub 仓库分析.md`
  - `2026-08-14 - LifeOS - GitHub 仓库分析.md`
  - `2026-08-17 - loopany 开源项目调研.md`
  - `2026-08-18 - PlanWeave - GitHub 仓库分析.md`
  - `2026-08-04 - Heron：AI Agent 时代的内核级嗅探器.md`
- **vault PARA 位置**：`2-Areas/AI-Agent-研究/`（PARA 类别 Areas）
- **MEMORY.md 引用**：
  - §工程全景调研边界（"Hermes / OpenClaw / Codex / Claude Code 都是可插拔 Agent 执行器"）
  - §开源研究边界（"只问具体技术能否借鉴"）
  - §Hermes Agent v0.14 实际验证（2026-06-29）

---

## 18. 一句话总结（给何大人看）

> **OpenAI 把 Codex Harness 全栈开源了**（不只是 CLI）。**核心是 app-server JSON-RPC 协议 + Rust monorepo + 双 SDK + Starlark 策略引擎 + Noise 多路复用远程会话**。**111k stars、Apache-2.0、每天 5-10 commit**。对德勤 MVP 的可借鉴点：app-server 协议（⭐⭐⭐）、exec-server 多路复用（⭐⭐⭐）、execpolicy 策略（⭐⭐）、apply-patch 结构化文件编辑（⭐⭐）、agent-graph-store 多 Agent 协作（⭐⭐）。**不抄**：Bazel、Starlark、marketplace、Cloud Tasks。**优先级**：本机 codex 升级 + 深读 3 个核心文档 + 写借鉴笔记到 `/root/vault/1-Projects/德勤/AI-Native/executor/`。

---

_分析者：小助 | 何大人 2026-08-22 微信消息触发_
_分析时间：2026-08-22 14:28 GMT+8_
