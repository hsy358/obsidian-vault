---
title: "SpacetimeDB：数据库即服务器的全栈后端框架"
author: "Clockwork Labs"
publish_date: ""
saved_date: "2026-07-29"
source: "github"
url: "https://github.com/clockworklabs/SpacetimeDB"
repository: "clockworklabs/SpacetimeDB"
license: "BSL 1.1（数年后转换为带 linking exception 的 AGPL v3.0）"
tags:
  - SpacetimeDB
  - database
  - backend
  - realtime
  - full-stack
  - AI-infrastructure
---

# SpacetimeDB：数据库即服务器的全栈后端框架

> 保存时间：2026-07-29 14:28（Asia/Shanghai）  
> 原始项目：[clockworklabs/SpacetimeDB](https://github.com/clockworklabs/SpacetimeDB)  
> 项目主页：[spacetimedb.com](https://spacetimedb.com)  
> 本文包含项目快照、技术分析与完整 README 原文。

## 项目快照（2026-07-29）

- 核心定位：**relational database that is also a server（数据库即服务器）**
- 主要语言：Rust
- GitHub：约 **24.8k Stars / 1.0k Forks**
- 最新稳定版本：**v2.7.0-hotfix3**（Release v2.7.0，2026-07-22）
- 服务端模块语言：Rust、C#、TypeScript、C++
- 客户端 SDK：TypeScript（React / Next.js / Vue / Svelte / Angular / Node.js 等）、Rust、C# / Unity、C++ / Unreal
- 部署：Maincloud 托管或 `spacetime start` / Docker 自托管
- 许可证：BSL 1.1；若干年后转换为带 linking exception 的 AGPL v3.0

## 一句话判断

SpacetimeDB 不是把“前端也塞进数据库”，而是把传统后端的 **关系数据库、业务逻辑服务器、实时状态同步、类型安全客户端绑定与部署单元** 收敛到一个运行时里。它更准确的说法是：**数据库原生的应用服务器 / 实时后端平台**。

## 核心架构

```text
Web / App / Unity / Unreal 客户端
            │
            │ 类型安全 SDK：调用 Reducer + 订阅表/查询
            ▼
┌─────────────────────────────────────────────┐
│                SpacetimeDB                  │
│  Tables       → 数据与索引                  │
│  Reducers     → 事务型写逻辑 / API           │
│  Views        → 只读计算查询                 │
│  Procedures   → 可执行外部 HTTP 调用         │
│  Identity     → 身份、权限与授权              │
│  Subscriptions→ 增量推送 + 客户端本地缓存同步  │
│  Commit Log   → 持久化、崩溃恢复              │
└─────────────────────────────────────────────┘
```

其关键变化不是“少写几层代码”，而是把后端边界从：

```text
Client → API Server → Cache / MQ → Database
```

压缩成：

```text
Client → SpacetimeDB Module
```

## 为什么适合 AI 时代

1. **Agent 生成全栈应用时，系统边界更少**  
   Schema、事务逻辑、权限和客户端绑定在同一模型内，减少 ORM、DTO、REST/GraphQL、缓存一致性和实时推送等胶水代码，AI Coding 更容易端到端保持一致。

2. **天然适合实时、协作型 Agent 产品**  
   多 Agent 状态、任务队列、执行事件、人机协同面板、审批状态等都可通过表 + Reducer + Subscription 实时同步，不必再手工拼 WebSocket 与缓存失效策略。

3. **强类型接口更利于 Agent 修改代码**  
   从服务端 Schema 生成客户端绑定，能够把很多跨端不一致问题前置为编译错误，降低 AI 改一端忘另一端的概率。

4. **单体部署降低原型和小团队运维成本**  
   对 MVP、游戏、实时仪表盘和内部工具，单二进制 / 单运行时的确能显著减少容器、Kubernetes、消息队列和独立缓存的复杂度。

但要注意：它本身**不是大模型框架、向量数据库、Agent 编排器或长期记忆系统**。它更适合作为 AI 应用的**事务状态层 + 实时同步层 + 业务逻辑运行时**。

## 最适合的场景

- 多人在线游戏、Unity / Unreal 实时后端
- 协同编辑、聊天、白板、实时看板
- 多 Agent 任务状态与事件流同步
- Human-in-the-loop 审批台、Agent Control Plane
- AI 原型、内部工具、小团队产品
- 需要强事务一致性且客户端必须实时感知变化的应用

## 不宜直接押注的场景

- 依赖 PostgreSQL / MySQL 大量既有扩展、ORM 和 DBA 工具链
- 超大规模冷数据、OLAP、数据湖或复杂 BI 工作负载
- 需要多数据库异构集成、复杂消息中间件与成熟微服务治理的系统
- 对数据库高可用、备份恢复、跨地域容灾、审计认证有严苛要求但尚未完成 PoC 的企业核心系统
- 团队无法接受 BSL 商业条款或未来 AGPL 转换机制的场景

## 与相邻产品的差异

| 方案 | 核心模型 | SpacetimeDB 的差异 |
|---|---|---|
| 传统 Spring / Node + PostgreSQL | API 服务与数据库分离 | SpacetimeDB 把事务业务逻辑直接运行在数据库模块内 |
| Firebase / Supabase | BaaS：数据库 + Auth + 实时能力 | SpacetimeDB 更强调“数据库就是应用服务器”和自定义编译模块 |
| Convex | 响应式数据库 + 服务端函数 | 理念最接近；SpacetimeDB 更偏底层、自托管、Rust/C#/C++ 与游戏性能 |
| Redis / WebSocket | 缓存或实时通道 | SpacetimeDB 同时承担权威事务状态、持久化与实时同步 |
| Temporal / LangGraph | 工作流 / Agent 编排 | SpacetimeDB 不负责工作流语义，但可作为其一致性状态与实时事件底座 |

## 关键风险与验证清单

1. **许可证**：BSL 1.1 不是传统意义上的宽松开源许可证，商业部署前需逐条审查 Additional Use Grant 与变更日期。
2. **单运行时耦合**：省掉中间层的同时，也把数据模型、业务逻辑和平台运行时绑定得更紧；迁移成本可能高于 PostgreSQL。
3. **生态成熟度**：约 24.8k Stars 说明关注度高，不等同于企业级运维生态成熟。
4. **性能边界**：官方强调内存状态 + 磁盘 commit log，应使用真实数据量验证内存占用、恢复时间、订阅扇出和热点写事务。
5. **运维能力**：重点验证备份恢复、升级迁移、滚动发布、监控告警、TLS、HA、跨地域和容量扩展。
6. **安全模型**：客户端直连不等于无安全边界；所有写操作与私有数据访问必须由 Reducer、表权限和身份声明严格控制。

## 建议的最小 PoC

选择一个“多 Agent 任务看板”而非企业核心系统：

- 表：`agents`、`tasks`、`task_events`、`approvals`
- Reducer：创建任务、抢占任务、更新状态、提交审批
- 客户端：React 实时看板
- 验收：两个 Agent 并发抢同一任务只允许一个成功；状态变化 1 秒内推送到 UI；进程重启后数据和事件可恢复
- 对照组：用 Supabase 或 PostgreSQL + WebSocket 实现同一功能，对比代码量、延迟、部署复杂度和迁移难度

## 小助结论

**值得研究，适合做“小而硬”的 PoC，但暂不建议未经验证直接作为企业通用底座。**

它真正有价值的地方不是“又一个数据库”，而是把后端复杂度做了结构性压缩：数据、事务逻辑、实时同步和客户端类型绑定由同一系统维护。对 AI Coding 来说，这种更少边界、更强约束的架构确实更友好；但对企业生产环境，许可证、平台绑定、运维成熟度和生态兼容性仍需单独过关。

---

# README 原文（完整快照）

> 来源：`master/README.md`，保存于 2026-07-29。相对图片路径需回到原仓库查看。

<p align="center">
    <a href="https://spacetimedb.com#gh-dark-mode-only" target="_blank">
	<img width="320" src="./images/dark/logo.svg" alt="SpacetimeDB Logo">
    </a>
    <a href="https://spacetimedb.com#gh-light-mode-only" target="_blank">
	<img width="320" src="./images/light/logo.svg" alt="SpacetimeDB Logo">
    </a>
</p>
<p align="center">
    <a href="https://spacetimedb.com#gh-dark-mode-only" target="_blank">
        <img width="250" src="./images/dark/logo-text.svg" alt="SpacetimeDB">
    </a>
    <a href="https://spacetimedb.com#gh-light-mode-only" target="_blank">
        <img width="250" src="./images/light/logo-text.svg" alt="SpacetimeDB">
    </a>
    <h3 align="center">
        Development at the speed of light.
    </h3>
</p>
<p align="center">
    <a href="https://github.com/clockworklabs/spacetimedb"><img src="https://img.shields.io/github/v/release/clockworklabs/spacetimedb?color=%23ff00a0&include_prereleases&label=version&sort=semver&style=flat-square"></a>
    &nbsp;
    <a href="https://github.com/clockworklabs/spacetimedb"><img src="https://img.shields.io/badge/built_with-Rust-dca282.svg?style=flat-square"></a>
    &nbsp;
	<a href="https://github.com/clockworklabs/spacetimedb/actions"><img src="https://img.shields.io/github/actions/workflow/status/clockworklabs/spacetimedb/ci.yml?style=flat-square&branch=master"></a>
    &nbsp;
    <a href="https://status.spacetimedb.com"><img src="https://img.shields.io/uptimerobot/ratio/7/m784409192-e472ca350bb615372ededed7?label=cloud%20uptime&style=flat-square"></a>
    &nbsp;
    <a href="https://hub.docker.com/r/clockworklabs/spacetimedb"><img src="https://img.shields.io/docker/pulls/clockworklabs/spacetimedb?style=flat-square"></a>
    &nbsp;
    <a href="https://github.com/clockworklabs/spacetimedb/blob/master/LICENSE.txt"><img src="https://img.shields.io/badge/license-BSL_1.1-00bfff.svg?style=flat-square"></a>
</p>
<p align="center">
    <a href="https://crates.io/crates/spacetimedb"><img src="https://img.shields.io/crates/d/spacetimedb?color=e45928&label=Rust%20Crate&style=flat-square"></a>
    &nbsp;
    <a href="https://www.nuget.org/packages/SpacetimeDB.Runtime"><img src="https://img.shields.io/nuget/dt/spacetimedb.runtime?color=0b6cff&label=NuGet%20Package&style=flat-square"></a>
    &nbsp;
    <a href="https://www.npmjs.com/package/spacetimedb"><img src="https://img.shields.io/npm/dm/spacetimedb?color=cb0000&label=npm&style=flat-square"></a>
</p>
<p align="center">
    <a href="https://discord.gg/spacetimedb"><img src="https://img.shields.io/discord/1037340874172014652?label=discord&style=flat-square&color=5a66f6"></a>
    &nbsp;
    <a href="https://twitter.com/spacetime_db"><img src="https://img.shields.io/badge/twitter-Follow_us-1d9bf0.svg?style=flat-square"></a>
    &nbsp;
    <a href="https://clockworklabs.io/join"><img src="https://img.shields.io/badge/careers-Join_us-86f7b7.svg?style=flat-square"></a>
    &nbsp;
    <a href="https://www.linkedin.com/company/clockworklabs/"><img src="https://img.shields.io/badge/linkedin-Connect_with_us-0a66c2.svg?style=flat-square"></a>
</p>

<p align="center">
    <a href="https://discord.gg/spacetimedb"><img height="25" src="./images/social/discord.svg" alt="Discord"></a>
    &nbsp;
    <a href="https://twitter.com/spacetime_db"><img height="25" src="./images/social/twitter.svg" alt="Twitter"></a>
    &nbsp;
    <a href="https://github.com/clockworklabs/spacetimedb"><img height="25" src="./images/social/github.svg" alt="GitHub"></a>
    &nbsp;
    <a href="https://twitch.tv/SpacetimeDB"><img height="25" src="./images/social/twitch.svg" alt="Twitch"></a>
    &nbsp;
    <a href="https://youtube.com/@SpacetimeDB"><img height="25" src="./images/social/youtube.svg" alt="YouTube"></a>
    &nbsp;
    <a href="https://www.linkedin.com/company/clockwork-labs/"><img height="25" src="./images/social/linkedin.svg" alt="LinkedIn"></a>
    &nbsp;
    <a href="https://stackoverflow.com/questions/tagged/spacetimedb"><img height="25" src="./images/social/stackoverflow.svg" alt="StackOverflow"></a>
</p>

<br>

## What is SpacetimeDB?

SpacetimeDB is a relational database that is also a server. You upload your application logic directly into the database, and clients connect to it without any server in between.

Write your schema and business logic as a **module** in [Rust](https://spacetimedb.com/docs/quickstarts/rust), [C#](https://spacetimedb.com/docs/quickstarts/c-sharp), [TypeScript](https://spacetimedb.com/docs/quickstarts/typescript), or [C++](https://spacetimedb.com/docs/quickstarts/c-plus-plus). SpacetimeDB compiles it, runs it inside the database, and automatically synchronizes state to connected clients in real-time.

Instead of deploying a web or game server that sits in between your clients and your database, your clients connect directly to the database and execute your application logic in your module. You can write all of your permission and authorization logic right inside your module just as you would in a normal server.

This means that you can write your entire application in a single language and deploy it as a single binary. No more separate webserver, no more containers, no more Kubernetes, no more VMs, no more DevOps, no more caching later. Zero infrastructure to manage.

<figure>
    <img src="./images/basic-architecture-diagram.png" alt="SpacetimeDB Architecture" style="width:100%">
    <figcaption align="center">
        <p align="center"><b>SpacetimeDB application architecture</b><br /><sup><sub>(elements in white are provided by SpacetimeDB)</sub></sup></p>
    </figcaption>
</figure>

SpacetimeDB is optimized for maximum speed and minimum latency. SpacetimeDB provides all the ACID guarantees of a traditional RDBMS, with all the speed of an optimized web server. All application state is held in memory for fast access, while a commit log on disk provides durability and crash recovery. The entire backend of our MMORPG [BitCraft Online](https://bitcraftonline.com) runs as a single SpacetimeDB module: chat, items, terrain, player positions, everything, synchronized to thousands of players in real-time.

## Quick Start

### 1. Install

```bash
# macOS / Linux
curl -sSf https://install.spacetimedb.com | sh

# Windows (PowerShell)
iwr https://windows.spacetimedb.com -useb | iex
```

### 2. Log in

```bash
spacetime login
```

This opens a browser to authenticate with GitHub. Your identity is linked to your account so you can publish databases.

### 3. Start developing

```bash
spacetime dev --template chat-react-ts
```

That is it. This creates a project from a template, publishes it to [Maincloud](https://spacetimedb.com/docs/how-to/deploy/maincloud), and watches for file changes, automatically rebuilding and republishing on save. See [pricing](https://spacetimedb.com/pricing) for details.

## How It Works

SpacetimeDB modules define **tables** (your data) and **reducers** (your logic). Clients connect, call reducers, and subscribe to tables. When data changes, SpacetimeDB pushes updates to subscribed clients automatically.

```rust
// Define a table
#[spacetimedb::table(accessor = messages, public)]
pub struct Message {
    #[primary_key]
    #[auto_inc]
    id: u64,
    sender: Identity,
    text: String,
}

// Define a reducer (your API endpoint)
#[spacetimedb::reducer]
pub fn send_message(ctx: &ReducerContext, text: String) {
    ctx.db.messages().insert(Message {
        id: 0,
        sender: ctx.sender,
        text,
    });
}
```

On the client side, subscribe and get live updates:

```typescript
const [messages] = useTable(tables.message);
// messages updates automatically when the server state changes.
// No polling. No refetching.
```

## Language Support

### Server Modules

Write your database logic in any of these languages:

| Language | Quickstart |
|----------|-----------|
| **Rust** | [Get started](https://spacetimedb.com/docs/quickstarts/rust) |
| **C#** | [Get started](https://spacetimedb.com/docs/quickstarts/c-sharp) |
| **TypeScript** | [Get started](https://spacetimedb.com/docs/quickstarts/typescript) |
| **C++** | [Get started](https://spacetimedb.com/docs/quickstarts/c-plus-plus) |

### Client SDKs

Connect from any of these platforms:

| SDK | Quickstart |
|-----|-----------|
| **TypeScript** (React, Next.js, Vue, Svelte, Angular, Node.js, Bun, Deno) | [Get started](https://spacetimedb.com/docs/quickstarts/react) |
| **Rust** | [Get started](https://spacetimedb.com/docs/quickstarts/rust) |
| **C#** (standalone and Unity) | [Get started](https://spacetimedb.com/docs/quickstarts/c-sharp) |
| **C++** (Unreal Engine) | [Get started](https://spacetimedb.com/docs/quickstarts/c-plus-plus) |

## Running with Docker

```bash
docker run --rm --pull always -p 3000:3000 clockworklabs/spacetime start
```

## Building from Source

If you need features from `master` that have not been released yet:

```bash
# Prerequisites: Rust toolchain with wasm32-unknown-unknown target
curl https://sh.rustup.rs -sSf | sh

git clone https://github.com/clockworklabs/SpacetimeDB
cd SpacetimeDB
cargo build --locked --release -p spacetimedb-standalone -p spacetimedb-update -p spacetimedb-cli
```

Then install the binaries:

<details>
<summary>macOS / Linux</summary>

```bash
mkdir -p ~/.local/bin
STDB_VERSION="$(./target/release/spacetimedb-cli --version | sed -n 's/.*spacetimedb tool version \([0-9.]*\);.*/\1/p')"
mkdir -p ~/.local/share/spacetime/bin/$STDB_VERSION

cp target/release/spacetimedb-update ~/.local/bin/spacetime
cp target/release/spacetimedb-cli ~/.local/share/spacetime/bin/$STDB_VERSION
cp target/release/spacetimedb-standalone ~/.local/share/spacetime/bin/$STDB_VERSION

# Add to your shell config if not already present:
export PATH="$HOME/.local/bin:$PATH"

# Set the active version:
spacetime version use $STDB_VERSION
```
</details>

<details>
<summary>Windows (PowerShell)</summary>

```powershell
$stdbDir = "$HOME\AppData\Local\SpacetimeDB"
$stdbVersion = & ".\target\release\spacetimedb-cli" --version |
    Select-String -Pattern 'spacetimedb tool version ([0-9.]+);' |
    ForEach-Object { $_.Matches.Groups[1].Value }
New-Item -ItemType Directory -Path "$stdbDir\bin\$stdbVersion" -Force | Out-Null

Copy-Item "target\release\spacetimedb-update.exe" "$stdbDir\spacetime.exe"
Copy-Item "target\release\spacetimedb-cli.exe" "$stdbDir\bin\$stdbVersion\"
Copy-Item "target\release\spacetimedb-standalone.exe" "$stdbDir\bin\$stdbVersion\"

# Add to your system PATH: %USERPROFILE%\AppData\Local\SpacetimeDB
# Then in a new shell:
spacetime version use $stdbVersion
```
</details>

Verify with `spacetime --version`.

## Documentation

Full documentation is available at **[spacetimedb.com/docs](https://spacetimedb.com/docs)**, including:

- [Quickstart guides](https://spacetimedb.com/docs) for every supported language and framework
- [Core concepts](https://spacetimedb.com/docs/core-concepts): tables, reducers, subscriptions, authentication
- [Tutorials](https://spacetimedb.com/docs/tutorials/chat-app): chat app, Unity multiplayer, Unreal Engine multiplayer
- [Deployment guide](https://spacetimedb.com/docs/how-to/deploy/maincloud): publishing to Maincloud
- [CLI reference](https://spacetimedb.com/docs/reference/cli-reference)
- [SQL reference](https://spacetimedb.com/docs/reference/sql-reference)

## License

SpacetimeDB is licensed under the [Business Source License 1.1 (BSL)](LICENSE.txt). It converts to the AGPL v3.0 with a linking exception after a few years. The linking exception means you are **not** required to open-source your own code if you use SpacetimeDB. You only need to contribute back changes to SpacetimeDB itself.

**Why did we choose this license?**
We chose to license SpacetimeDB under the MariaDB Business Source License for 4 years because we can't compete with AWS while also building our products for them.

We chose GPLv3 with linking exception as the open source license because we want contributions merged back into mainline (just like Linux), but we don't want to make anyone else open source their own code (i.e. linking exception). 

