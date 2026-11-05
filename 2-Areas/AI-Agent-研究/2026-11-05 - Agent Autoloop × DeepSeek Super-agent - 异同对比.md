---
title: Agent Autoloop × DeepSeek Super-agent - 异同对比与德勤借鉴
date: 2026-11-05
type: comparison-note
tags: [AI-Agent, 对比分析, Agent-Autoloop, DeepSeek-Super-agent, 德勤项目, 架构参考]
related_notes:
  - 2026-11-05 - Agent Autoloop - GitHub 仓库分析.md
  - 2026-11-03 - DeepSeek Super-agent - 设计分析与德勤借鉴点.md
  - 2026-10-28 - DeepSeek Harness + DS Bot - 架构分析与德勤项目借鉴点.md
---

# Agent Autoloop × DeepSeek Super-agent：异同对比

> 对比对象：
> - **A** = Agent Autoloop（KKKKhazix/agent-autoloop，MIT，2.5k★，2026-11-03 建，调度中台，1651 行零依赖）
> - **B** = DeepSeek Super-agent（dsh-superagent-prototype，MIT，官方定位"研究原型"，Router/Worker 双层自治底座）
>
> 前提不变（6-29 决策）：**Hermes v0.14 仍是德勤唯一框架**；两者都只借架构，不做产品二选一。

---

## 一、一句话区分

> **A 是"规则驱动的确定性管道"，B 是"模型驱动的自治调度器"。**

- A：`rules.json` 写死「什么事件 → 交给谁 → 在哪干 → 什么 prompt」，**调度是纯代码判断，几乎不烧模型 token 做决策**
- B：**Router 用模型判断**该派给谁（实测每次决策 1.6–6.4 秒推理，缓存 token 23M→32M），**调度本身消耗模型**

这决定了二者的一切差异。

---

## 二、相似处（设计哲学高度同源）

| # | 共同点 | A 的做法 | B 的做法 |
|---|---|---|---|
| 1 | **事件驱动，不是 prompt 驱动** | GitHub Webhook / cron / HTTP → 标准事件 → 内核 | 群聊消息 / PR 评论 / CI 结果 → Trigger → Eval |
| 2 | **人只在必须动作时被打扰** | `ask` 卡片：删数据/重启/花钱/对外发消息才问 | Router 只在人必须动作时说话，回复 ≤100 字 |
| 3 | **结构约束 > prompt 叮嘱** | 事件带 `cwd`/`agent`/`access` 直接拒收；跳数 >8 层停派 | Router **结构上就没有 shell**，拆不了也干不了 |
| 4 | **事件溯源 + 唯一写入点** | append-only 日志 + 索引同事务落盘 | Engine 是唯一写入者 + Outbox 是唯一 receipt 写入者 |
| 5 | **幂等** | 同事件排队时合并成一轮 | 同一 Trigger 接受两次只产生一个 Ticket |
| 6 | **挂起 = 释放** | 等你拍板时**进程直接退出**，等你回复再接原会话 | Worker 隔离，Router 常驻但不占 Worker 上下文 |
| 7 | **可复盘/可观测** | `why <轮次>` 一条命令查清来龙去脉；sim 崩溃 1000 次测试 | Web 面板只显示"需要人处理"；Watchdog 可被自然语言问诊 |
| 8 | **自托管 + 本机优先 + MIT** | 一台机器一条命令，无公网端口 | 云端循环 + 本地 daemon 执行 |
| 9 | **"少打扰"作为产品定位** | "平时不烦你，遇到拿不准的事才发卡片" | "take as little human attention as possible" |

> 这说明：**「把人的注意力当最稀缺资源」已经是 2026-11 行业共识**，A 和 B 是同一命题的两种工程答案。这条共识可以直接写进德勤项目的设计原则页。

---

## 三、根本区别

| 维度 | Agent Autoloop | DeepSeek Super-agent |
|---|---|---|
| **定位** | 自动化中台 / 调度层（Agent 外面套一层） | 自治 Agent 底座（本身就是 Agent 系统） |
| **授权模型** | ⚠️ **几乎没有**——`rules.json` 就是全部授权 | ✅ 完整：**Policy 版本化 + Mandate 不可变 + Admission 表三档**（explicit / inferred / not admitted） |
| **领域模型** | 轻：事件 / 轮次（带规则版本）/ 回复 | 重：Source·Trigger·Thread·Correlation·Channel·Policy·Eval·Mandate·Ticket·Assignment·Subscription |
| **"人"是什么** | 没有抽象，人只是"拍板的人" | **人只是 Trigger 的元数据**；跨 Source 身份映射是 prompt 文本 |
| **通道回写** | 插件化 webhook / 飞书卡片，通用但无 Thread 抽象 | Thread / Channel 一等公民，多通道回写 + 扇出 |
| **Agent 接入** | **通用 CLI**：Claude Code / Codex / ACP / OpenClaw / Hermes / Cursor…（只要能收 prompt 打印最后一句） | 自己的 **DSH Executor** + Worker session，Agent 内部由 DSH 提供 |
| **注入防护** | ✅ 强：外部文本只落文件不进提示词 + 字段白名单 | ⚠️ 弱：主要靠 Policy、prompt 文本、observe 模式 |
| **循环保护** | ✅ **跳数熔断 TTL**（>8 层停派，人工介入也不清零） | ❌ 无显式跳数熔断，只有 Watchdog **停滞检测**（事后） |
| **灰度/观察** | ❌ 无 | ✅ **observe 模式**：先记录"它本来会做什么"，人工核对后放开 |
| **决策成本** | 派活 p99 **1.82 ms**，几乎零 token | Router 决策 **1.6–6.4 s/次**，token 消耗显著 |
| **工程严谨度** | ✅ 极高：零运行时依赖、20 万步随机仿真、强杀 1000 次不丢事实、benchmark 达标线、随机种子可复现 | 一般：研究原型，官方明说"部分文章内容代码未实现" |
| **成熟度** | 2 天历史，2.5k★，作者自述样例"只在本地假飞书 CLI 验证过" | 官方发布 + 内部实例 + 消融实验数据 + 9 篇体系化文档（000–008） |
| **协作边界** | 单用户单机 | 团队级，多人多 channel |

### 一句话概括差异
- **A 强在"工程可靠性"**：可复现、可压测、可证明不丢事实、注入防护硬。
- **B 强在"治理与注意力经济"**：谁授权、授权范围、要不要做、怎么少打扰，全是明确抽象。
- **A 的短板正是 B 的长板**（授权/审计/领域建模）；**B 的短板正是 A 的长板**（工程严谨度/注入防护/熔断/成本）。

---

## 四、两者能否组合？—— 能，而且是互补的

```
┌──────────────────────────────────────────────┐
│ 治理层（B 借鉴）：Policy / Mandate / Ticket   │  ← 谁授权、范围可审计
├──────────────────────────────────────────────┤
│ 调度层（A 借鉴）：事件接入 / 派活 / 熔断 / 通知 │  ← 确定性的、可压测的
├──────────────────────────────────────────────┤
│ 执行层（已定）：Hermes v0.14 + 执行器抽象层    │  ← 每种 harness 都能接
└──────────────────────────────────────────────┘
```

- A 的插件位（源/Agent/通道/交付）恰好对应我们要做的**执行器抽象层适配器**
- B 的领域模型（Mandate/Policy）正是**金融/政务客户安全评审要的"可审计授权"**
- 两者都不提供 Agent 编排/状态机/记忆 → **都不与 Hermes 竞争**

---

## 五、对德勤项目的借鉴点（更新版）

### 从 A 补进已有清单（新增 3 条）
1. **指令数据分离**（外部文本只落文件、不拼提示词 + 事件字段白名单拒收）→ **P0**，可直接进德勤 MVP 安全基线，注解词注入面
2. **跳数熔断 TTL** → **P0**，编排层循环保护的默认参数（>8 层停派并告警）
3. **工程测试方法论**（随机仿真 20 万步 / 强杀 1000 次 / 种子可复现 / benchmark 达标线）→ **P1**，直接抄成**德勤交付的验收测试方案**：交付物不能"跑通一次就算数"，要能复现、能证明不丢事实

### 从 B 维持原判（不变）
- Router/Worker 分层且 Router 无执行权（P0）
- 事件先过滤后模型判断（P0）
- 注意力经济学作为设计原则（P0）
- Mandate 不可变 + Policy 版本化（P1，可审计）
- Watchdog 独立 session（P1）

### 需要升级的一条
- 原判"B 的领域模型是 P1"→ **应升 P0**：A 的 `rules.json` 授权模型在金融/政务**过不了安全评审**。德勤要用 **Policy 版本化 + Mandate 不可变**做授权底座，A 的轻量规则只能用于内部工具链，不能直接进客户环境。

### 明确不抄
- ❌ A 的"rules.json 即全部授权"（无审计、无版本、无准入分级）
- ❌ A 依赖"本机已登录的 CLI Agent"（客户服务器上不成立，须换 API Key 模式）
- ❌ A 的事件轮询/webhook 具体实现（用我们自己的 Source 抽象）

---

## 六、观察建议

- **A**：仅 2 天历史，star 涨势异常（2 天 2.5k），先观察 1–3 个月再看实战；本机可装（Linux 匹配）实测"挂起零消耗"是否真省 Token
- **B**：官方研究原型，DeepSeek 自己留了 4 个未解问题（Router session 规模上限、人机协作边界、Agent 间上下文边界、凭证不进模型上下文），**都在等社区方案**——这 4 条恰好是德勤项目要答的题，值得单独追

---

*资料来源：Agent Autoloop README（2026-11-05 抓取）、DeepSeek Super-agent 设计文章 + dsh-superagent-prototype docs/000–007、已有 vault 笔记两份。检索时间：2026-11-05。*
