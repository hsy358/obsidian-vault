---
type: github-repo-analysis
repo: block/buzz
url: https://github.com/block/buzz
homepage: https://github.com/block/buzz
snapshot_commit: 5e2e132a4ba0f5268d3689f6068dd61adb3d0168
stars: 11232
forks: 877
open_issues: 562
latest_release: v0.4.26 (Buzz Desktop)
license: Apache-2.0
language: Rust + TypeScript + Dart
analyzed_date: 2026-07-25
tags: [nostr, relay, workspace, human-agent, event-log, chat, git, identity, schnorr, rust, axum, postgres, redis, blossom, agent, code-review, workflow, jack-dorsey, block]
source:
  url: https://github.com/block/buzz
  fetched: 2026-07-25T23:27+08:00
  by: 小助 via GitHub API + README + 外部报道
---

# Block / Buzz — Hive-Mind 协作平台（GitHub 仓库分析）

> **一句话判断**：Buzz 是 Block / Jack Dorsey 推出的开源 **人类 + AI Agent 协作工作区**，底层是一个自托管的 **Nostr 中继（relay）**——所有消息、评论、git 事件、工作流步骤都用同一类签名事件表示，agent 用独立的密钥对获得"成员身份"而非"工具权限"。

## 一、项目快照

| 维度 | 信息 |
|---|---|
| 仓库 | [block/buzz](https://github.com/block/buzz) |
| 维护方 | Block, Inc.（Jack Dorsey 的金融科技公司） |
| 创建时间 | 2026-03-06 |
| 本次快照 | 2026-07-25，main `5e2e132a` |
| Stars / Forks | 11,232 / 877 |
| Open Issues | 562 |
| 最新版本 | `Buzz Desktop v0.4.26`，2026-07-25 |
| 主语言 | Rust（约 12.9 MB）+ TypeScript（约 9.5 MB）+ Dart（移动端，约 1.7 MB） |
| 许可证 | **Apache 2.0**（真·开源） |
| 桌面端 | Tauri + React |
| 移动端 | Flutter（iOS + Android，正在接入） |
| 服务端 | Rust 工作区，Axum WS + REST，Postgres + Redis + S3/MinIO |

> 数字来自 2026-07-25 GitHub API。Buzz 由 Jack Dorsey 公开宣布于 2026-07-21，仓库原本在年初就开放，发布前已在 Block 内部使用数月。来源：[Yahoo Tech](https://tech.yahoo.com/ai/meta-ai/articles/jack-dorseys-block-launches-buzz-110343370.html)、[Crypto Briefing](https://cryptobriefing.com/block-launches-buzz-nostr-workspace)。

## 二、它在解决什么问题

现代团队在不同工具里来回跳：

- 聊天在 Slack / Teams
- 代码在 GitHub / GitLab
- CI 结果在另一处
- Bot 用 webhook 粘合
- 搜索又是一个独立系统

Buzz 把这些都映射到同一个事件流：

- 一条消息是一种事件
- 一次代码审阅是一种事件
- 一条 CI 结果是一种事件
- 一次工作流步骤也是一种事件

agent 用自己的 Nostr 密钥对在同一个中继上签名发帖，**权限粒度不是 flag，而是身份**——同一个频道、同一种搜索索引、同一个审计链。人在里面叫同事，agent 也在里面叫同事，只是持有不同的 keypair。

## 三、核心能力

### 3.1 同一事件总线

```text
channel 消息 · DM · 表情反应
   └──┐
git patch · repo announcement · CI status (NIP-34)
   └──┐
workflow 触发 · 审批 · 审计 (hash-chain)
   └──┐
media · canvas · voice huddle
```

所有事件用同一类身份（公钥 + Schnorr 签名）和同一类过滤器（NIP-01 filters）暴露给客户端。

### 3.2 Community = URL

- 自托管默认一个 relay 对应一个 community；
- 托管方可以在共享 Postgres / Redis / MinIO 的同时用域名或子域名切租户；
- 用户视角的"工作区"就是 URL，租户边界对用户透明。

### 3.3 Agent 是成员不是 Bot

`buzz-cli` 是为 LLM 工具调用设计的 JSON-in / JSON-out CLI。`buzz-acp` 是 ACP 适配层，让 Goose / Codex / Claude Code 等执行器直接接进 relay。agent 在频道里发帖、提交 patch、参与审阅、跑工作流，和人类成员一样的操作面，**但携带自己的身份和审计链**。

### 3.4 Git 事件化

按 NIP-34 把 patch、repo 公告、状态写进事件流。代码评审和合并决定都落在同一个 channel 里——channel 就是"这段代码为什么存在"的记录。

### 3.5 可声明的工作流

YAML 定义触发与步骤：消息 / 表情反应 / schedule / webhook。当前 4 类触发，审批门控在接入中。

### 3.6 媒体与协作面

- 视频可加 frame-anchored comments；
- 共享白板；
- voice huddle（生命周期事件在接入中）。

## 四、技术架构

```text
┌───────────────────────────────────────────────────────────┐
│ Clients                                                  │
│ Desktop (Tauri)  · Mobile (Flutter)  · buzz-cli          │
│ Goose / Codex / Claude Code via buzz-acp                │
└────────────────────────────┬──────────────────────────────┘
                             │ WS + REST
                ┌────────────▼─────────────┐
                │       buzz-relay        │
                │ NIP-01 · NIP-42 · REST  │
                │ hash-chain audit log    │
                └─┬──────────────┬────────┬┘
                  │              │        │
            ┌─────▼─────┐  ┌─────▼────┐  ┌▼────────┐
            │ Postgres  │  │  Redis   │  │ S3/MinIO│
            │ events +  │  │ pub/sub  │  │ Blossom │
            │ FTS search│  └──────────┘  └─────────┘
            └───────────┘
```

### Crate 速览

| 区域 | 组件 |
|---|---|
| 核心协议 | `buzz-core`（零 IO 类型 + NIP-01 + Schnorr 校验） · `buzz-relay`（Axum WS + REST）|
| 服务 | `buzz-db` · `buzz-auth` · `buzz-pubsub` · `buzz-search` · `buzz-audit`（hash-chain 日志）|
| Agent 面 | `buzz-cli` · `buzz-acp` · `buzz-agent` · `buzz-dev-mcp`（shell + 文件编辑）· `buzz-workflow` · `buzz-persona` |
| Git | `git-sign-nostr` · `git-credential-nostr` · `buzz-pair-relay` / `buzz-pairing-cli` |
| 共享 / 工具 | `buzz-sdk` · `buzz-media` · `buzz-admin` · `buzz-test-client` |

> 多租户模式下，`community` 边界贯穿 DB 行、缓存键、搜索文档、工作流状态、媒体元数据、git 指针和审计链——共享基础设施只是实现细节。

## 五、关键工程取舍

### Rust 工作区

> "a suspicious number of Rust crates"

- 大部分逻辑留在服务端 relay，单一真源；
- agent 在客户端用 buzz-acp / buzz-cli 接入，不需要把模型运行拖进 server；
- 桌面是 Tauri（Rust 壳 + React 前端），和后端共享类型与事件模型。

### Nostr 当协议层

- 现成的身份（公钥）、签名（Schnorr）、过滤器（NIP-01）模型；
- 复用 NIP-34（git）、NIP-42（认证）、NIP-98（HTTP 鉴权）；
- 复用 Blossom（NIP-类似协议）做媒体存储；
- 自然适合"多 relay / 自托管 / 跨组织"场景。

### 审计用 hash-chain

`buzz-audit` 不是普通 append-only 表，而是 hash-chain——可以验证事件未被篡改。对企业合规是个重要差异化点。

## 六、与现有 AgentSpace / Multica 的关系

| 维度 | Buzz | AgentSpace（HKUDS）| Multica |
|---|---|---|---|
| 协议底座 | Nostr relay + 事件总线 | Postgres + AgentRouter | Go + WebSocket + Postgres |
| Agent 身份 | Nostr 密钥对 | Workspace member + Harness 标识 | Profile + Runtime |
| 工作区形态 | 多 channel + DM + voice | Workspace + 治理面板 | Issue 看板 + Squad |
| 部署 | 自托管 relay / 托管 | 自托管 / Platform | Cloud / Docker |
| 许可证 | Apache 2.0 | Apache 2.0 | 修改版 Apache 2.0（商业限制）|
| 客户端 | Desktop + 移动端（Flutter）| Web + CLI | Web + Desktop + iOS |

### 我的判断

- 三者都属于 "Agent Control Plane" 范畴，**互相不是替代关系，是不同范式**：
  - **Buzz**：把工作区协议化（事件总线 + 身份 + 审计），适合需要"可移植 + 自托管 + 可验证审计"的团队
  - **AgentSpace**：把 Agent 当作"数字员工"管理，强调组织治理
  - **Multica**：把 Agent 当作"团队同事"管理，强调 Issue 流程 + Squad
- **最适合借鉴的 Buzz 部分不是界面，而是协议层抽象**：
  - 事件总线（NIP-01 过滤器 + Schnorr 签名）
  - hash-chain 审计
  - identity-scoped permission（不是 flag）
  - agent 在同一工作面拥有和人类相同的操作面

## 七、最值得借鉴的 5 点

### P1：事件即一切

把 channel 消息、DM、表情、git patch、CI 状态、工作流步骤都建模为同一类事件。**好处**：检索、审计、回放都是同一套基础设施；agent 不需要"切频道"就能看到全部上下文。

### P2：identity-scoped 权限

不再"人类用户 vs agent 权限位"，而是"在某个 channel / community 里拥有同一种身份"。**好处**：撤销、转让、委托就是改 key 关系；审计链路也按身份走。

### P3：hash-chain 审计

`buzz-audit` 用 hash-chain 让审计不再是"我们相信数据库没被改"，而是"任何篡改都可以验证出来"。对金融、政府、医疗客户友好。

### P4：agent 拥有完整操作面

agent 不是 webhook 或 cron job；它能开 channel、起 canvas、跑工作流、加入 huddle。**好处**：agent 真正成为"在工作面里有身份的成员"，而不是外部脚本。

### P5：relay = community = URL

URL 是工作区入口，自带边界。**好处**：多租户隔离不靠业务层堆叠，而是协议层就规定好。

## 八、不建议现在直接做的事

- 不因 Jack Dorsey 名头就启动部署——开源版是开发预览，不是 GA；
- 不依赖 Block 托管服务做生产依赖；
- 不在没读完 `VISION.md` / `ARCHITECTURE.md` / `SECURITY.md` 前直接跑 `just setup`；
- 不把现有 AgentSpace 切到 Nostr——两套范式的迁移成本远超收益；
- 不要因为 Rust 工作区看起来"高大上"就急着复制；
- 不在没有 VPN / TLS / 鉴权 hardening 前暴露 `ws://localhost:3000`；
- 移动端标注"being wired up"，短期不要押注。

## 九、最小验收标准（如果未来做 POC）

POC 之前先明确：**不是要把 Buzz 部署成德勤 MVP 的替代品，而是看哪些组件值得拆解借鉴。**

1. `just setup` + `just dev` 跑通桌面端连本地 relay；
2. 用 `buzz-cli` 配 `BUZZ_PRIVATE_KEY` 发一条消息，验证签名落地；
3. 跑 `crates/buzz-acp` 接 Codex 或 Goose 验证 agent 能在 channel 发消息；
4. 跑一条 YAML 工作流，触发 → 步骤 → 完成都成为审计事件；
5. 拉一条 git patch 事件，验证 NIP-34 落库；
6. 关掉 relay 后用 Postgres 验证 hash-chain；
7. 用 `buzz-pair-relay` 验证两个 relay 之间的跨 community 配对行为。

**失败标准**：桌面端 hot-reload 反复失败、agent 消息无法签名、hash-chain 验证出错、git 事件无法回放、YAML 工作流在 schedule 触发下重复跑空——任一项发生都停止深入。

## 十、对 vault 中现有决策的影响

- 现有 AgentSpace 路线**不受影响**——Buzz 是不同协议范式的项目，不是替代品；
- 不修改"Hermes 是既定 Agent 框架"的边界；
- 真正可能借用的是 **hash-chain 审计**和**事件总线抽象**，作为"借鉴点"列入 v6.x R&D 方案的调研子项；
- 来源仍然是 MEMORY.md 中"产品线决策顺序"+"开源研究边界"：

> 不要做产品层面的"二选一"决策。研究包 A / B / C 的产出应该是借鉴 + adapter 代码，而不是替换。  
> 来源：`MEMORY.md#L73-L107`

## 十一、最终结论

### 结论卡

- **值不值得研究**：值得，优先级中-高。
- **值不值得立即部署**：暂不建议，先做隔离 POC。
- **值不值得替换 AgentSpace**：不值得（不同范式）。
- **最有借鉴价值**：事件总线、identity-scoped 权限、hash-chain 审计、agent 完整操作面、relay = community 协议边界。
- **最大风险**：项目年轻（2026-Q1 才立项）、移动端 / 审批门控尚未完成、内部版与开源版边界（README 提到"I work at Block, don't use the OSS release"）。

> 真正值得学的不是 Buzz 本身怎么搭，而是它"用 Nostr 协议把工作区压缩成事件流"的范式。这种范式很可能会渗透到未来所有 Agent 协作产品的设计中。

## 十二、参考来源

- GitHub：https://github.com/block/buzz
- README：https://github.com/block/buzz/blob/main/README.md
- 架构：https://github.com/block/buzz/blob/main/ARCHITECTURE.md
- Agent 视角：https://github.com/block/buzz/blob/main/VISION_AGENT.md
- 发布说明：https://github.com/block/buzz/releases
- 媒体：[Yahoo Tech](https://tech.yahoo.com/ai/meta-ai/articles/jack-dorseys-block-launches-buzz-110343370.html) · [Crypto Briefing](https://cryptobriefing.com/block-launches-buzz-nostr-workspace) · [KuCoin News](https://www.kucoin.com/news/flash/block-launches-buzz-a-nostr-based-alternative-to-slack-and-github) · [Trendshift](https://trendshift.io/repositories/61760)