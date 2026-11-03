---
title: DeepSeek Super-agent 设计分析与德勤借鉴点
date: 2026-11-03
type: research-note
tags: [AI-Agent, DeepSeek, Harness, Super-agent, 多智能体, 德勤项目, 架构参考]
sources:
  - https://mp.weixin.qq.com/s/zoS7GlReWPhfCjENGxXCdg （Harness 团队公众号《Exploring Super-agent Design》，2026-10-31，作者 Yujia Qiao）
  - https://github.com/deepseek-ai/dsh-superagent-prototype （MIT，研究原型）
  - https://www.deepseek.com/en/harness
related_notes:
  - 2026-10-28 - DeepSeek Harness + DS Bot - 架构分析与德勤项目借鉴点.md
  - 2026-06-29 - Hermes Agent v0.14 验证记录
---

# DeepSeek Super-agent：设计与借鉴

> 2026-10-31 DeepSeek Harness 团队发布《Exploring Super-agent Design: Towards a More Autonomous Agent System》（中文，公众号），
> 同日开源研究原型 `dsh-superagent-prototype`（MIT）。**官方明确定位："Research prototype for reference only, not an official DeepSeek product."**
> 部分文章内容在代码中尚未实现。

## 一、这是什么

一个**常驻（always-on）的自治智能体**：

- 从**群聊 + GitHub（可选飞书）**接需求
- 同时并行推进多个任务
- **只在人必须动作时才说话**
- 团队自用的实例：在没人 @ 它的情况下，从公开群里找出某个 bug 的根因并开了修复 PR

### 四条设计属性（原文口径）

| 属性 | 含义 |
|---|---|
| Continuous 持续 | 聊天里谈的计划，PR 评论里改的需求，它都能理解是同一件事 |
| Efficient 高效 | 不用等上一个指令结束就接下一个；多个复杂任务并行 |
| Proactive 主动 | 自己盯事件、推进值得推进的事，其余时候闭嘴 |
| Persistent 持久 | 待在团队真实工具里，坏了能自己恢复 |

### 出发点：瓶颈不在模型，在人

> 一个人通常只能盯住 **3–5 个**活跃的 agent session。
> 单个任务的上限由模型决定，**多个任务的上限由人的注意力决定**。

仓库一句话目标：**"take as little human attention as possible, and give as much value as possible."**

## 二、五块架构（可直接抄的部分）

| 部件 | 做什么 | 关键细节 |
|---|---|---|
| **两层：Router / Workers** | Router 只对人说话、派活；Worker 隔离并行干活 | **Router 可以根本没有 shell**，用轻量模型即可；Worker 才上最强模型 |
| **事件驱动而非 prompt 驱动** | 聊天消息、邮件、review 评论、CI 结果都是触发器 | **先代码过滤，模型只判断过滤后的**；Worker 订阅自己的 thread，**后续对话绕过 Router** |
| **人能忍受的回复** | 长任务立即返回，agent 一边干活一边继续对话 | 聊天回复上限 **100 字**；异步任务机制内置但默认关闭 |
| **计算 / 状态 / 机器分离** | 循环跑在云端，状态存数据库，小 daemon 在本地机器执行命令 | 兼容"开发者自己的电脑只是偶尔在线" |
| **Watchdog** | 独立 session + 定时器，核查每个 Worker 是否真在推进 | 维护者可用自然语言问"到底哪里卡住了" |

### Router 的关键设计（与常见"lead agent + subagents"不同）

> **Router 从不拆解任务、从不亲自干活。** 它只处理人，决定哪个 Worker 接哪个请求。
> 保持这层薄，是为了让单个 Router session 不成为瓶颈：思考期间到达的触发器先堆积，下次调用一起处理。

## 三、实测数据（DeepSeek 自测，官方称 preliminary）

合成负载：约 300 条群聊 + GitHub CI 消息，其中约 20 条真实需求，每种配置跑 5 轮。**编码被换成"只花时间"的工具，所以测的是调度与协同，不是代码质量。**

| 配置 | 结果 |
|---|---|
| Super-agent | 完成时间 p50 **12.4 分钟** / p95 **15.7 分钟** |
| 单 session + subagent 工具（中性 prompt） | **5 轮全部没委派**；p95 **29.5 分钟** |
| 单 session + 偏好委派的 prompt | 4/5 轮委派，但**仍慢于** Super-agent |
| Super-agent 但后续消息不走 Worker 直达 | 完成时间相同；Router 决策多 **~30%**；缓存 token 从 23.23M → **31.77M** |
| Router 负载 ~1 trigger/分钟 | 每次决策 **6.4 秒** 推理 |
| Router 负载 ~40 trigger/分钟 | 每次决策 **1.6 秒**，平均批量 2.8 |

**最值得看的一条**：中性 prompt 下，模型选择"全都自己干"，并不断被新消息打断。改成"倾向委派"有帮助，但第 5 轮它自己判断活太小不值得派 → 长尾出现。
**Super-agent 的做法是把这个判断从 prompt 里拿走：Router 干脆没有能力干这活。**

## 四、原型现在实际能做什么（比文章窄得多）

- 针对**单个 GitHub 仓库**的主动式编码 agent，**飞书作为可选聊天源**
- 被允许的人提需求 → 开一个 work item → 在**自己的 agent session 和目录**里干 → 回原对话回复（可以是 PR）
- Web 面板**只显示"需要人处理"的条目**
- Setup 由 agent 带你做：读仓库 `SETUP.md`，**一次只问一个问题**
- 热度：发布一天约 **4300 star**（2026-11-01）

### 哲学文档（最值得引用的部分）

> "It acts only when asked, or when a written rule allows it."
> "It speaks only when a person must act or can use a result."
> 没人要求的工作 → 进入 **observe 模式**，只记录"它本来会做什么"。
> 给运维的话：**"Do not use it to produce volume."**

细则（来自 000-philosophy / 002-authorization）：

- **少概念**：只有领域概念（如 Source）及其实现（GitHub、Feishu）；业务需求要么变成某个概念的属性，要么变成 agent 遵守的 prompt，**不为它新增概念**
- **少设置**：默认能覆盖大多数团队时，默认值替代设置；团队用文字描述的行为 → 是 **prompt 文本，不是配置项**
- **一次只问一个具体问题**，用结构化形式，让问题真到人面前
- **按影响停手，不按努力停手**：本地改动做到"可评审"为止；需要设计决策时停下来问清楚
- **诚实汇报**：草稿就标未完成，失败就报失败，**绝不为"少问一句"而绕过限制**

## 五、领域模型（001-domain，最有工程价值的一份）

```
Source →(Trigger)→ Thread →(batch)→ Eval →(accept + Mandate)→ Ticket
                                        ↓(ignore/unavailable)→ recorded
Ticket ──(Assignment)──→ Executor（领域外）
Ticket ──(Channel)─────→ Source 回写
Trigger ──(Subscription fan-out)──→ 订阅该 Thread 的 Ticket（绕过 Eval，不给新授权）
```

核心概念与它们各自"守住"的规则：

| 概念 | 定义 | 守住什么规则 |
|---|---|---|
| **Source** | 事件流。kind=可复用实现，instance=一份配置 | 持有读取位置 + 自己的 bot 身份；**重启不能重放事件** |
| **Trigger** | 不可变事件，带 Source 自己的元数据（actor 等） | 属于一个或多个 Thread；**同一 Trigger 接受两次只产生一个 Ticket**（幂等） |
| **Thread** | 按时间排序的 Trigger 序列 | 同一时刻至多一个 Eval；持有 Subscription、运行中的 Eval、Decision 历史 |
| **Correlation** | Trigger 同时所属 Thread 之间的关系 | 只补上下文，**从不路由** |
| **Channel** | Thread 的写入侧（回帖地址） | 一个 Thread 可有多个 Channel；确认/回复/PR/已解决 review 都是写入 |
| **Policy** | 版本化的评估规则 + 各 Source 的部分（谁能发起、名单怎么同步、哪些 bot 可做候选） | **版本覆盖规则 + accept 模式 + Source 部分**；影响在跑 Ticket 的变更会通知其 Assignment，但**不撤销已发的 Mandate** |
| **Eval** | 对一批 Trigger 的判断，分两层：gate（准入）+ assessment（评估） | 输入=Trigger 批 + Thread 快照 + 该 Thread 上所有 Ticket（含已结束）+ 当前 Policy；输出=Decision；**自身不持状态** |
| **Mandate** | accept 授予的授权：Policy 版本、范围、强度、命中规则、发送者在该 Source 的身份 | **不可变**；范围变宽=新 Ticket；Ticket 结束不结束 Mandate，**只有人的 stop 才撤销**；恢复前需按当前 Policy 重新校验 |
| **Ticket** | 一份被授权的工作单元 | **只有 Eval 能创建**；自己定义状态，**不跟随 Executor 的状态** |
| **Assignment** | Ticket 与某个 Executor 实例的绑定 | 一个 Ticket 生命周期内可有多个；状态独立于 Ticket；**只有最终 report 能从 Executor 侧结束 Ticket** |
| **Subscription** | Ticket ↔ Thread 多对多 | 匹配到的 Trigger 扇出给所有存活订阅 Ticket，**不检查发送者**；人的消息走到 Ticket → 不走 Eval；**bot 和 CI 的消息不恢复已结束 Ticket** |

**明确拒绝的概念**（很值得学）：
- ❌ Principal / Membership 作为实体，或跨 Source 映射身份 —— **人只是 Trigger 的元数据**；允许名单是 Policy 的 Source 部分；跨 Source 身份映射是 prompt 文本
- ❌ Eval 自己调度延迟 Trigger —— 需要等待的条件就是**另一个普通 Source**，Eval 不反向依赖 Source
- ❌ "追加到 Ticket" 这种 Decision —— 追加就是 Subscription 扇出，不需要 Eval
- ❌ 每 Thread 至多一个存活 Ticket —— 一个 Thread 可以承载多件独立的工作

### 授权强度三档

| 强度 | 情形 |
|---|---|
| **explicit** | 名单上的人 @ 了 agent；或对已有 Ticket 的 Thread 追问；准入表某格设为 explicit request |
| **inferred** | 不在名单的人对有 Ticket 的 Thread 追问（除非其格是 explicit）；准入表设为 inferred candidate；名单内 bot 的消息 |
| **not admitted** | 其他 bot 的消息、准入表忽略的、以及 accept 模式为 `off` 时的全部 inferred |

**Admission 表**（每个 Source 一张，行=接收范围，列=3 档）：
- Feishu：每个配置的群 / 其他群里的 @ / 私聊
- GitHub：新 Issue、新 PR、评论、默认分支 CI
- 每格默认：在名单但不@ → inferred；不在名单但@ → ignore；不在名单也不@ → ignore
- **CI 结果没有发送者**，所以它那行只提供最后一格

## 六、实现架构（007-architecture，TypeScript + DSH Bundle）

```
Source plugins ──SourceContext──┐
Session tools ──────────────────┼→ Engine ─→ Store / Policy / SourceRegistry
HTTP management routes ─────────┘        ├→ MasterAssessor（decide）
                                         ├→ DshExecutor
                                         └→ Outbox（唯一 receipt 写入者）
```

- **Runtime 是组合根，不含领域规则**；构造失败会关 Store + 释放锁
- **Engine 是 Trigger/Thread/Decision/Ticket/Assignment 的唯一写入者**；**所有方法同步**，每条命令在**一个事务**里改聚合；端口在事务内入队外部工作，**adapter 在提交后执行**
- Engine 五个内部件：**Intake / Evals / Tickets / Assignments / Replies**，依赖单向流动
- **Outbox**：`send` 在一个事务里保存消息 receipt + 入队 `reply` effect；effect handler 才真正通过 `SourceRegistry.send` 发出；Source 关闭时消息等待，对话消失则丢弃
- **Notices**：把领域事件和 worker 活动转成主 session 消息；`reportRelay` **问题立即转发，普通进度留在自己的 Ticket 上**；落在 turn 期间的中继在下一步一起投递
- **Passes**：每 2 秒一轮（或命令触发），先处理到期 effect，再 `Engine.evaluateDue` —— Source 的 Trigger 由此进入 Engine
- Engine 按角色暴露**只读 Pick**：`EngineForSources / ForMainSession / ForPeople / ForSettings / ForExecutor`

## 七、DeepSeek 自己留的四个未解问题

1. 如何突破单个 Router session 的规模上限
2. session 从屏幕上消失后，人该怎么和 agent 协作
3. **不同 agent 实例之间的上下文边界怎么划、彼此怎么通信**
4. **安全**：云端循环被攻破 → 所有连上来的机器都危险；**凭证需要一种"能被使用但从不进入模型上下文"的方式**

## 八、给德勤项目的借鉴点（按优先级）

> 前提不变（2026-06-29 决策）：**Hermes Agent v0.14 仍是德勤 Agent 框架的唯一选择**，Super-agent 只借架构范式，不做产品二选一。

### P0 —— 直接可抄（成本低、收益高）

1. **Router / Worker 分层，且 Router 无执行权**
   抄点：**Router 只做人机接口与派单，不拆解任务、不执行**。用"**结构上做不到**"代替"prompt 里叮嘱它别做"。
   收益：消除"模型自己判断活太小不委派"的长尾（DeepSeek 实测 p95 29.5 → 15.7 分钟）。
   德勤落点：**执行器抽象层之上加一层轻量 Dispatcher**，Dispatcher 只认路由不认工具。

2. **事件驱动 + 先代码过滤、后模型判断**
   抄点：**过滤器跑在模型之前**，模型只判过滤后的少量事件；**Worker 订阅自己的 Thread，后续对话直接到 Worker，绕过 Router**。
   收益：Router 决策成本实测从 6.4s → 1.6s/次，缓存 token 省 23%；这是"多租户/多项目"的成本关键。
   德勤落点：政务/金融客户里**信噪比极高的事件流**（告警、工单、CI）必须先过滤。

3. **注意力经济学作为设计原则（这是最有"咨询味"的一条）**
   抄点：每条消息/通知/面板元素/文档段落都要**能自证其价值 > 它消耗的注意力**，否则删掉。
   配套：聊天回复 **≤100 字**；**面板只显示"需要人处理"的**，健康状态不占空间；一次只问一个具体问题。
   德勤落点：可以直接搬进**客户交付验收标准**和**Agent 输出的 UI/IM 交付规范**。

4. **按影响停手，不按努力停手**
   抄点：本地改动做到"可评审"为止；需要业务决策就停下来问，**且一次只问一个结构化问题**。
   德勤落点：**金融/政务场景里"该问"比"做完"更重要**，这是交付边界管理的现成话术。

### P1 —— 需要改造后抄

5. **Ticket / Mandate / Policy / Assignment 四件套领域模型**
   - **Mandate 不可变 + 版本化 Policy**：工作被授权的范围和依据要**可审计、可回溯**（谁在什么规则版本下批准了什么范围）→ 金融/政务客户安全评审的硬需求
   - **Ticket 自己定状态，不跟随 Executor 状态** → 执行器可替换（Hermes / OpenClaw / Codex 都能当 Executor）而不影响工作语义
   - **Assignment 一个 Ticket 生命周期内可有多个** → 天然支持"换执行器/重试/迁移"，正好对上德勤"每种 harness 都能接"的要求
   - **拒绝"Principal/Membership 实体"、拒绝跨 Source 映射身份** → **人只是事件元数据**，授权名单按 Source 分开维护 —— 这个反直觉的决定省掉了一整个权限模型

6. **幂等 + 唯一写入点**
   抄点：**同一 Trigger 接受两次只产生一个 Ticket**；**Engine 是唯一写入者**，全部同步 + 单事务；**Outbox 是唯一 receipt 写入者**，事务内入队、提交后执行。
   德勤落点：可执行器抽象层的**参考实现骨架**照抄（单事务 + Outbox + 端口/adapter 分层）。

7. **Watchdog 独立 session**
   抄点：**不靠 Executor 自己报告进度**，另起一个定时 session 检查每个 Worker 是否真在推进，且**维护者能用自然语言问它哪里卡住**。
   德勤落点：长周期交付项目（德勤项目本来就是）的**停滞检测 + 一键诊断**。

8. **Observe 模式（先只记录，后放行）**
   抄点：未经规则允许的主动行为先进 observe，只记录"它本来会做什么"，人工核对后再放开。
   德勤落点：**客户环境上线前的灰度策略**，直接写进交付方案。

### P2 —— 值得抄的思想，不值得抄实现

9. **"不为主体"**：主体是事件元数据，跨源身份映射是 prompt 文本 —— 极简授权模型
10. **文档按序编号、每篇只建立在前面的概念上**（000→008）—— **德勤交付文档/技术方案模板可直接套用这个"渐进式概念引入"结构**
11. **"不要用它来制造产量"** —— 作为交付方对客户的**责任话术**：Agent 批量产 PR / 群发消息，亏的是团队注意力

### 明确不抄

- ❌ **飞书 / GitHub 双通道的具体实现**（德勤客户渠道不同，但 **Source 抽象**该抄）
- ❌ **TypeScript + DSH Bundle 的技术栈**（德勤在 Hermes v0.14 之上）
- ❌ **Router session 规模上限问题**（DeepSeek 自己也没解，等社区方案）

## 九、与已有笔记的关系

| 笔记 | 关系 |
|---|---|
| `2026-10-28 - DeepSeek Harness + DS Bot` | 本文是它的**续篇**：DSH 讲"可插拔执行器"（Capability Seam 三角色），Super-agent 讲"**如何组织一屋子的执行器**"。两者合起来正好覆盖德勤执行器抽象层 |
| `2026-06-29 - Hermes Agent v0.14` | 决策不变：Hermes 仍是唯一框架，Super-agent 只借架构 |
| Hermes 社区致谢 | DS Bot 曾致谢 Hermes Agent + Hermes Bot Mode → 社区共识仍在，可作汇报佐证 |

## 十、一句话结论

**Super-agent 的真正贡献不是"更强的 agent"，而是"把人的注意力当成最稀缺的资源来设计系统"** ——
Router 无执行权（结构消除判断失误）、事件先过滤后判断（成本可控）、回复 ≤100 字 + 面板只留"需要人"（噪音最小化）、
Mandate 不可变 + Policy 版本化（可审计）、Engine 唯一写入点 + Outbox（可换执行器）。
对德勤而言，**这套东西的价值在"交付治理与成本治理"**，正好是 Agent 平台项目从 demo 走向企业落地的分水岭。

---

*资料来源：DeepSeek Harness 团队公众号（2026-10-31，Yujia Qiao）、dsh-superagent-prototype 仓库 README + docs/000~007、CellCog 分析、MarkTechPost、ThePandaily。检索时间：2026-11-03。*
