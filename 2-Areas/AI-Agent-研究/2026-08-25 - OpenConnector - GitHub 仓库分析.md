---
type: github-repo-analysis
repo: oomol-lab/open-connector
url: https://github.com/oomol-lab/open-connector
homepage: https://oomol.com
snapshot_date: 2026-08-25
stars: 4800
forks: ~200（topics 显示活跃，但具体数待确认）
license: Apache-2.0（标准开源）
language: TypeScript + Hono + Cloudflare Workers
analyzed_date: 2026-08-25
tags: [ai-agent, tool-calling, connector-gateway, mcp, oauth, saas-integration, self-hosted, cloudflare-workers, apache-2.0, api-gateway, openconnector, agent-tools]
related:
  - oomol-lab/wanta（基于 OpenConnector + OpenCode 的桌面 Agent）
  - oomol-lab/connector-sdk（零依赖 TS 客户端）
  - oomol-lab/oo-cli（本地 agent 中继 CLI）
  - oomol-lab/dsh-oomol（DeepSeek Harness 集成）
source:
  url: https://github.com/oomol-lab/open-connector
  fetched: 2026-08-25T22:30+08:00
  by: 小助 via GitHub API + README + OOMOL 官方文档
---

# OpenConnector — AI Agent 的 SaaS 工具网关（GitHub 仓库分析）

> **一句话判断：** OpenConnector 不是 Agent 框架，而是位于 Agent 与外部 SaaS 之间的 **"工具调用层 + 凭据隔离层"**：通过 MCP / HTTP / SDK / CLI / OpenAPI 五种协议暴露 1000+ SaaS 的 10000+ Actions，让 Agent 调用外部应用时**永远不接触明文密钥**。"Connect Once, Use Everywhere"。

## 一、项目快照

| 维度 | 信息 |
|---|---|
| 仓库 | [oomol-lab/open-connector](https://github.com/oomol-lab/open-connector) |
| 官方定位 | Open-source connector gateway for AI agents / alternative to Pipedream/Composio |
| Stars / Forks | 4.8k / ~200 |
| License | **Apache-2.0**（标准开源） |
| 技术栈 | TypeScript + Hono（web 框架）+ Cloudflare Workers 生态 |
| 存储 | SQLite（本地） / D1（CF） / PostgreSQL（自托管） |
| 数据 | D1 / R2（CF） / S3-compatible（自托管） |
| 提供能力 | **1,000+ Providers / 10,000+ Actions**（catalog 动态查询） |
| 部署形态 | 3 种：OOMOL Hosted / Cloudflare Workers / Self-hosted (Docker / Node.js / Fly.io) |
| 调用入口 | 5 种：SDK / CLI / MCP / HTTP / OpenAPI |
| 凭据支持 | API Key / OAuth2 / Custom / No-auth 四类 |
| 文档语言 | EN / 简中 / 繁中 / 日 / 韩 / 俄 / 法 七种 |

## 二、它解决的到底是什么问题

传统 AI Agent 调外部 SaaS 的痛点是**两头都不好做**：

**Agent 开发者视角：**
- 每个 SaaS（GitHub / Gmail / Notion / Slack ...）都要写一遍 OAuth 流程 + 胶水代码
- 写完一个换下一个，重复劳动
- 大量 prompt token 浪费在描述 API 细节上

**企业 IT / 安全视角：**
- Agent 直接持有用户 API Key / OAuth Token → 密钥泄漏即灾难
- 调用审计困难：谁、何时、调了哪个 API、传了什么数据
- 合规审计（GDPR / SOX / 等保）几乎不可能

OpenConnector 把这两头**同时解掉**：

```
传统模式：  Agent ──(明文密钥 + 胶水代码)──► SaaS
OpenConnector：Agent ──(MCP/HTTP/...)──► OpenConnector Gateway ──(统一 OAuth 池)──► SaaS
                                    ▲
                                    │ 密钥 / 审计 / 配额 / 脱敏
                                    └─ 全部在 Gateway 内
```

## 三、核心架构拆解

### 3.1 五种调用入口协议（设计哲学：多入口一等公民）

| 入口 | 用途 | 谁在用 |
|---|---|---|
| **SDK**（零依赖 TS） | 应用代码内嵌调用 | Wanta 桌面 Agent / 第三方应用 |
| **oo CLI** | 本地 agent 中继（终端内联） | Hermes / OpenCode / Codex 类 CLI Agent |
| **MCP**（`/mcp`） | MCP 协议 agent 直连 | Claude Desktop / MCP-capable agent host |
| **HTTP API** | 自定义服务调用 | 后端服务 / Webhook 回调 |
| **OpenAPI 3.1** | 自动生成 OpenAPI 文档 | 自定义客户端 / Swagger UI |

> **洞察**：五种入口共用同一套 catalog 和 schema。"一次集成，多处可用"——不是噱头，是架构级承诺。

### 3.2 声明式 Action Catalog（企业级必备）

```
每个 Action 都有：
  ├─ request/response schema      ← 类型安全
  ├─ required scopes              ← 权限最小化
  ├─ lazy-loaded executor source  ← 按需加载
  ├─ connection identity          ← 谁在调
  ├─ action allow/block policies  ← 谁能调什么
  ├─ temporary file transit       ← 文件传递
  └─ redacted run logs            ← 审计 + 脱敏
```

> **这才是企业级的关键**。OpenConnector 不只是"1000+ 集成"，它把每个 Action 当成**可声明、可审计、可策略化**的一等公民。这和德勤/平安场景里的"调用谁审计"问题直接对上。

### 3.3 三种部署形态（设计哲学：可插拔 Runtime）

| 形态 | 适用场景 | 存储栈 |
|---|---|---|
| **OOMOL Hosted** | 个人 / 小团队，零部署 | OOMOL 自管 |
| **Cloudflare Workers** | 边缘部署 / 全球低延迟 | D1 + R2 + Static Assets |
| **Self-hosted** | 企业私有化 / 合规要求 | SQLite/Postgres + S3 |
| **Fly.io** | 中等规模自托管 | 同上 |

> **设计者视野很广**：把**部署**和**能力**解耦——同一套 catalog 和 schema 在三种形态下完全一致。这对企业客户**极其友好**：先用 Hosted 试用，确认要私有化时迁移到 Self-hosted，代码零改动。

### 3.4 凭据管理四象限

```
            API Key
              │
   No-auth ──┼── OAuth2
              │
         Custom auth
```

每种凭据都通过 Gateway 代理转发，Agent 进程内**永远不见明文 token**。运行时还会做 **redacted run logs**——日志里的 token 自动打码。

## 四、与同类项目对比（生态定位）

| 项目 | 类型 | 定位差异 |
|---|---|---|
| **OpenConnector** | 自托管 + Hosted | 1000+ 集成 / 五协议 / 部署可插拔 |
| **Pipedream** | SaaS | 重 workflow 编排，但密钥托管在 Pipedream 云 |
| **Composio** | SaaS + 自托管 | 类似定位，但托管是主战场 |
| **MCP Server** | 单点 | 一个 server 一个服务，无统一 catalog |
| **n8n / Zapier** | workflow | 重流程编排，AI 是次要 |

> **OpenConnector 的差异点**：把"凭据隔离 + 1000+ catalog + 五协议 + 可插拔部署"四件事**同时**做透。不是竞品做的功能多，是它把"Agent 调用外部"这件事**当成基础设施**做。

## 五、OOMOL Lab 生态矩阵

OOMOL 不只是 OpenConnector，是一组协同的 Agent 基础设施：

| 仓库 | Stars | 用途 |
|---|---|---|
| **open-connector** | 4.8k | SaaS 工具网关（核心） |
| **wanta** | 67 | 基于 OpenCode + OpenConnector 的桌面 Agent |
| **connector-sdk** | 20 | 零依赖 TS 客户端 |
| **oo-cli** | 37 | 本地 agent 中继 |
| **dsh-oomol** | - | DeepSeek Harness 集成 |
| **pdf-craft** | - | AI PDF 抽取（姊妹项目） |
| **ovm-js** | 12 | Apple Virtualization 上的 OVM 管理 |

> **看 Wanta 的描述**："An open-source desktop AI agent foundation **powered by OpenCode and connected through OpenConnector**"——这就是 OpenConnector 的标杆用法：Agent 框架 + Connector 网关，二者通过 MCP 解耦。

## 六、和德勤 AI Native MVP 的关联

> **前提**：MEMORY.md 已明确——
> - Hermes Agent v0.14 是德勤 Agent 框架的唯一选择（2026-06-29）
> - 开源项目只作为**技术借鉴**，不替代 Hermes
> - 德勤项目需要**执行器抽象层 + 整套系统可单独部署**

### 6.1 强相关：踩中两个硬需求

德勤 AI Native 组织 Workspace 里，Agent 必然要调企业内外部系统（HR / 财务 / CRM / ERP / 审批 / 合规 / 知识库）。两个硬需求：

| 需求 | OpenConnector 怎么对应 |
|---|---|
| **企业合规：密钥不落 Agent** | 凭据四象限隔离 + redacted run logs |
| **100+ 企业内应用快速接入** | 1000+ SaaS catalog + 声明式 Action |

### 6.2 可借鉴的具体技术点

| # | OpenConnector 设计 | 德勤 MVP 可借鉴处 |
|---|---|---|
| 1 | **声明式 Action catalog**（schemas + scopes + policies） | 德勤每个企业应用的接入做成"声明式 Action"，而不是写死胶水代码 |
| 2 | **五种入口协议**（SDK / CLI / MCP / HTTP / OpenAPI） | Hermes / OpenClaw / Codex 各自走最合适的入口，但共用 catalog |
| 3 | **可插拔部署**（Hosted / Edge / Self-hosted） | 德勤客户既可以走 SaaS 试用，也可以私有化部署 |
| 4 | **"Connect Once, Use Everywhere"** | 企业 IT 视角的"统一集成层"——一次 OAuth，所有 Agent 可用 |
| 5 | **redacted run logs** | 合规审计的硬要求：日志里的 token / PII 必须脱敏 |
| 6 | **allow/block policies** | 企业场景下必须能按角色 / 部门控制"谁能调什么 Action" |
| 7 | **lazy-loaded executor** | 按需加载企业应用的执行器，避免一次性打包所有集成 |
| 8 | **Apache-2.0** | 完全商用友好，没有 source-available 限制（对比 Multica） |

### 6.3 组件定位建议

在德勤 AI Native MVP 的架构里，OpenConnector 模式可作为 **Tool Gateway（工具网关）** 组件，与 Hermes Agent 解耦：

```
┌─────────────────────────────────────────┐
│  Hermes Agent v0.14（执行器抽象层）        │
└──────────────────┬──────────────────────┘
                   │ MCP
                   ▼
┌─────────────────────────────────────────┐
│  德勤 Tool Gateway（借鉴 OpenConnector）    │
│  - 声明式 Action catalog                 │
│  - 凭据四象限隔离                        │
│  - 审计日志 + 策略控制                   │
└──────────────────┬──────────────────────┘
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
    HR/财务/CRM  ERP/审批     合规/知识库
   （企业内 100+ 应用）
```

### 6.4 不要做的事

- ❌ **不要试图替代 OpenConnector** —— MEMORY 边界：开源项目只做借鉴
- ❌ **不要把 OpenConnector 当成 Hermes 替代品** —— 它是 Hermes 的下游组件
- ❌ **不要照搬 1000+ SaaS catalog** —— 德勤场景是企业内应用，不是消费级 SaaS

## 七、和求职方向（德勤 / AI 工程师）的关联

### 7.1 德勤 AI Native MVP 简历论点

> 在德勤 AI Native 组织 Workspace 的设计中，借鉴 OpenConnector 的"声明式 Action catalog + 凭据隔离 + 多入口协议"模式，设计了企业级 **Tool Gateway** 组件，实现：
> - **100+ 企业内应用**统一接入（HR / 财务 / CRM / ERP / 审批）
> - Agent 调用外部时**永远不接触明文密钥**，满足等保 / GDPR 合规
> - 与 Hermes Agent 通过 MCP 解耦，可独立部署
> - **调用审计 100% 可追溯**，支持合规审查

### 7.2 AI 工程师岗位能力展示

OpenConnector 模式展示了：
1. **企业级 AI 合规设计**：密钥隔离、审计脱敏、策略控制
2. **架构抽象能力**：部署可插拔 + 多入口协议 + 声明式 catalog
3. **生态整合视野**：不重复造轮子，能识别"基础设施 vs 应用"的边界

## 八、风险与边界

| 风险 | 说明 |
|---|---|
| **生态规模小** | Stars 4.8k 比 Composio / Pipedream 小一个数量级，长期维护风险 |
| **企业级特性待验证** | SSO / RBAC / 多租户隔离等企业必备特性未在 README 详述 |
| **OOMOL 商业模式不明** | Hosted 服务是否长期免费 / 是否会与开源版分化需观察 |
| **MCP 协议成熟度** | MCP 仍在演进，OpenConnector 押注 MCP 是双刃剑 |
| **TypeScript-only** | 后端只 TS，企业若要 Java/Go 集成需额外工作 |

## 九、信息源

| 来源 | URL |
|---|---|
| GitHub README | https://github.com/oomol-lab/open-connector |
| GitHub API 元数据 | https://api.github.com/repos/oomol-lab/open-connector |
| 官方自托管文档 | https://oomol.com/en/docs/openconnector-self-hosting |
| 第三方深度介绍 | https://silenceper.com/en/article/2026-07-31-openconnector-ai-agent-saas-gateway |
| 配套项目 Wanta | https://github.com/oomol-lab/wanta |
| OOMOL Lab 组织 | https://github.com/oomol-lab |

---

> **总结**：OpenConnector 是当前**最像"AI 时代的 API 网关"**的开源项目——把"Agent 调外部 SaaS"这件事当成基础设施做，且把企业合规（密钥隔离 + 审计）作为一等公民。德勤 AI Native MVP 可借鉴其**声明式 catalog + 多协议入口 + 可插拔部署**三大设计，但不要试图替代 Hermes，而是作为 Hermes 的下游 Tool Gateway。