---
title: Agent Autoloop - GitHub 仓库分析
type: research-note
repo: https://github.com/KKKKhazix/agent-autoloop
stars: 2539
forks: 502
license: MIT
language: TypeScript
created: 2026-11-03
analyzed: 2026-11-05
tags: [agent, 自动化, 调度, 开源, 事件驱动, 插件化]
---

# Agent Autoloop - GitHub 仓库分析

> 一句话：让命令行 Agent（Claude Code / Codex / OpenClaw / Hermes…）在后台自己接活、自己跟到底；平时不打扰人，只有"删数据/重启服务/花钱/对外发消息"这类拿不准的事才推卡片要人拍板。

## 基本信息

| 项 | 值 |
|---|---|
| 仓库 | KKKKhazix/agent-autoloop |
| Star / Fork | 2539 / 502（2026-11-03 创建，2 天涨到这个量级，热度很高） |
| 许可 | MIT |
| 语言 | TypeScript |
| 内核规模 | 约 1651–1800 行，**零运行时依赖** |
| 安装 | `curl -fsSL .../install.sh \| sh`，需 Node 24 + Git + curl |
| 平台 | macOS / Linux（Windows 版作者说 11/7-8 做） |

## 核心定位

不是 Agent 框架，是**极轻量自动化中台（automation middleware）**：

- **事件 → 规则 → 派活 → 跑一轮 → 退出 → 需要时才问人** 的闭环
- 四个方向全部插件化、可替换：
  - 事件源：GitHub Webhook / GitLab Webhook / HTTP 接口 / cron 规则 / Issue 轮询
  - Agent：Claude Code / Codex / ACP / 通用命令（任意能"接收 prompt + 打印最后一条回复"的 CLI 都能接）
  - 通知通道：桌面通知（默认）/ 飞书 / 钉钉 / 企微 / Slack / Discord
  - 交付：CI/CD 流水线（打 `deliver` 标签 → 审代码 → 等 CI → 合并 → 等部署 → 核对线上版本）

## 四个内核机制（值得抄的设计）

1. **挂起零消耗**：等人拍板时**进程直接退出**，状态存数据库。你三天不回，Agent 进程一个不跑、Token 一分不花；一回答就接上原对话继续干。
2. **事件溯源**：所有状态由一条只追加日志算出，日志与索引同事务落盘，写完才应答。进程被 kill 也不丢已确认事实；数据格式变了直接从日志重建，不用写迁移脚本。
3. **指令数据分离**（防提示词注入）：外部文本（Issue 标题正文）只作为"资料文件"放进目录，**不拼进提示词**；提示词里只有校验过字符的类型、编号、链接。事件里带的 `cwd` / `agent` / `access` 字段**直接拒收**——用哪个 Agent、在哪干、什么权限，只由本机规则决定。
4. **跳数熔断**（类似网络包 TTL）：Agent 交回的事件会再派给 Agent，层数累加，人工提问和定时复查都不清零，Agent 自己改不了；>8 层只记录不再派活并发卡片告警。

## Agent 接入方式（对我们直接可用）

README 里直接点名了我们的栈：

| Agent | 接入命令 |
|---|---|
| OpenClaw | `openclaw agent exec {prompt}` |
| Hermes | `hermes chat -q {prompt}` |
| DeepSeek Harness | `dsh --profile headless {prompt}` |
| Cursor / CodeBuddy / pi | 见官方 CLI 文档 |

协议极简：**Agent 只需在最后一条回复里交代结果**。需要请示就在末尾附一段 ```agent-autoloop JSON 代码块，支持：
- `ask`（提问/选项卡片）
- `notice`（通知）
- `resolve`（关闭已解决卡片）
- `later`（预约复查，如"半小时后再醒来"）
- `events`（触发新事件）

JSON 写错 → 只让它在原会话里重写最后一段，不重做业务；重写也失败 → 保留原结论 + 通知人回执未生效。

## 现成场景模板

早报 / GitHub Issue 跟进 / 线上告警排查 / 用户反馈处理 / 网站巡检 / 飞书周报摘要 / PR 自动交付 / Claude 委托 Codex 处理网页 / 每周代码清理。

## 对德勤项目的可借鉴点（按 6-29 边界：只谈技术借鉴，不谈替代）

> 决策前提不变：**Hermes Agent v0.14 是德勤 Agent 框架的唯一选择**，本项目不替代 Hermes。

1. **"挂起零消耗"** ↔ 德勤 MVP 的人工介入（human-in-the-loop）：审批节点不能靠 Agent 进程常驻挂着等，那在政务/金融客户现场是成本 + 合规双重问题。事件溯源 + 挂起恢复是可直接抄的实现范式。
2. **指令数据分离** ↔ 金融/政务场景的提示词注入防护基线。事件字段白名单拒收（cwd/agent/access）+ 外部文本只落文件不进提示词，这两条几乎可以直接抄进我们的执行器抽象层。
3. **跳数熔断（TTL）** ↔ 多 Agent 编排时的循环保护。可作为我们编排层的默认策略：层数 > N 自动停止并告警。
4. **插件四方向抽象**（源 / Agent / 通道 / 交付）↔ 与我们已有的 **Capability Seam 三角色**（DSH 研究）思路一致，可交叉验证"可插拔执行器"是行业共识。
5. **插件化事件溯源日志 + `why <轮次>` 命令** ↔ 可观测性交付物：客户问"这一轮为什么这么跑"时能一条命令查清。德勤 MVP 演示里这是很好的加分项。
6. **通用命令 Agent 插件** ↔ 我们正在做的"每个 Agent 执行器都可插拔"的落地方案，可以拿它当反面参照（它只做 headless CLI 适配，不涉及 Agent 内部编排）。

## 风险 / 注意

- 项目**仅 2 天历史**，star 涨得极快但缺乏实战检验，作者自述"样例只在本地假飞书 CLI 上验证过，没在真实账号跑过完整业务"。
- 依赖 Node 24 + 本机已登录的 CLI Agent → 在交付给客户的服务器环境里，"已登录的 Agent"这一前提往往不成立（得改成 API Key 模式）。
- Windows 不支持（对我们 Linux 服务器无影响）。
- 它是**调度层**，不提供 Agent 编排/状态机/记忆——与 Hermes、LangGraph 是互补关系，不是竞争。

## 我们的动作建议

- 短期：可在本机装一个（Linux 匹配），接 OpenClaw 做**事件源 → 派活 → 卡片拍板**的闭环实测，验证"挂起零消耗"是否真省 Token。
- 中期：把"指令数据分离 + 跳数熔断"两条写进德勤 MVP 的执行器安全基线（可作为交付物的一部分）。
- 长期：观察 3 个月，看它是否长出"多 Agent 编排 + 记忆"，若长出来则与 Hermes 边界需重新评估（但产品路线决策优先级不变）。

## 快速入口

- 上手：`curl -fsSL https://raw.githubusercontent.com/KKKKhazix/agent-autoloop/main/install.sh | sh` → `agent-autoloop try`
- 文档：`docs/protocol.md`（通信协议）、`docs/plugins.md`（插件开发）、`skills/agent-autoloop/SKILL.md`（配置手册）、`SECURITY.md`（安全边界）
- 自测：`node sim/random.ts 24301 200000`（随机/崩溃/重复提交模拟）、`node sim/crash.ts 1000 12648430`（强杀 1000 次）、`npm run benchmark`

---

## 追加（2026-11-05 晚）：作者系列解读要点 + 源码交叉核验

何大人转来作者（Samuel）的系列解读稿，补充了 README 之外的细节。逐条与源码核对：

| 作者口径 | 源码核验 | 结论 |
|---|---|---|
| 「内核只做四件事：收事件、按规则分活、把活派给 Agent、把每一步记下来，其余什么都不干」 | `kernel/` 共 8 个模块：`decide`(决策) / `rules`(规则形态) / `cron` / `due`(到期) / `query` / `evolve`(事实日志) / `store` / `state` / `card-page` | ✅ 属实 |
| 「内核自己也绝对不往外连，需要联网的都放插件里」 | `kernel/*.ts` 的 import 汇总**只有** `node:crypto`、`node:sqlite` + 自身模块，**零 http client、零 fetch** | ✅ 属实，且比"零 LLM 调用"更强：**内核零出站网络** |
| 「内核里绝不允许写死具体产品名字（Claude/Codex/Hermes 都不关心）」 | `kernel/rules.ts` 里 `Agent` 是 `{name, worker, use, access, command?, model?}` 抽象；具体 Agent 全在 `plugins/{claude,codex,acp,command}/` | ✅ 属实，**厂商中立** |
| 「同一件事短时间内连续来好几条消息会合成一轮，不一窝蜂去改同一个东西」 | `kernel/decide.ts:157-167 enqueue()`：同 `rule` + 同 `lane` 的排队 run **被复用**，事件累加进同一 run 的 `run_events`；`lane = rule.parallel ? subject : ""`（无 parallel 时整条 rule 一条 lane，有则按 subject 分线）；`groupLimit` 再限并发 | ✅ 属实，是**真合并**（复用同一 run），不只是排队限流 |
| 「是否需要审批、能执行什么操作一律以本机 rules.json 为准，能防一些 Prompt 注入」 | `protocol/rules.ts` 校验事件字段白名单（`cwd`/`agent`/`access` 拒收），外部文本只落文件不进提示词；`ASK_FIRST` 清单：删数据/停服/花钱/对外发消息/改产品方向/新建轮换密钥/改权限 | ✅ 属实 |
| 「跳数熔断：Agent 每叫醒下一个 Agent 就加一层，超过 8 层自动停下来并发卡片」 | `kernel/decide.ts:34 MAX_HOPS = 8`；人工提问与定时复查都不清零 | ✅ 属实 |
| 「轮询脚本没新东西就直接退出，不叫醒大模型，不花 token」 | `examples/watch-github-issues.sh` 属**事件源侧**，在模型之外 | ✅ 属实 |

### 作者的框架叙事（可复用到我们自己的对外表达）

> 事件 → 派活 → 执行 → 交付 → **批奏折**（拿不准就找人拍板）

其中"**批奏折**"这个中文隐喻很好：**决策权上移到人，但只在需要决策时**。可作为德勤项目对客户讲"人在环"的设计话术。

### 对德勤的三条新增借鉴

1. **内核零出站网络**（P0）→ 我们的执行器/调度层应坚持"核心不出网、联网能力全在适配层"。这条与"每个组件独立可部署"要求天然契合，也方便金融/政务做网络分区审查。
2. **厂商中立的内核抽象**（P0）→ 内核只认 `{name, use, access, command?}`，不认 Claude/Codex/Hermes。这正是德勤"每种 harness 都能接"的最小可行形态，可直接写进执行器抽象层的接口定义。
3. **事件合并（复用同一 run + lane 分线）**（P1）→ 我们的编排层也需要"同一对象上的连续事件合并成一轮"，否则会出现多个 Agent 同时改同一交付物。作者的说法在这点上是准确的，README 没写清。

---

## 追加（2026-11-05 上午）：rules.json 到底是谁写的？——三层时序厘清

何大人追问："规则和派活是不是上一步模型分析规划后写到规则里的？"

**答：方向对了一半。要分三层看。**

### 第 1 层 · 设计期（一次性/按需）——**确实是模型规划的**

关键证据：作者把整个中台的**操作手册本身写成了给 AI 读的 SKILL.md**（`skills/agent-autoloop/SKILL.md`）：

- frontmatter description：「配置 Agent 自动化中台：加规则、接新的事件插件、接新的 Agent、接新的通道…用户说"有事的时候让 Agent 自己处理"…时用」
- 正文直接以**祈使句指挥 AI**：「用户想接自动化时先从例子改，不要从零写」「每条规则回答五个问题：什么事件（when），交给谁（to），在哪（cwd），照什么做（skill、prompt），要不要告诉用户（tell）」
- README 也说「可以把安装说明丢给你的 Agent，让它替你装好」

**所以官方推荐用法就是：人提需求 → Claude Code / Codex 读 SKILL.md + `examples/recipes/` 模板 → 生成 rules.json + 处理手册(Skill) + 插件代码 → 人审 → 落地。**
"规则是模型分析规划后写下来的" —— 在**这一层完全成立**。

### 第 2 层 · 运行期（每次事件）——**派活不经过模型**

- 规则固化在 `rules.json`，内核只认文件：`kernel/decide.ts:513 HANDLERS.rules` 由 host 文件监听推入，**没有任何输入类型允许 Agent 回写规则**
- 事件匹配纯代码：`kernel/rules.ts:29-33` `when` 只有 `{cron}` 与 `{source, types[]}` 两种形态，命中即派活
- 每轮执行时模型确实在跑，但**它不决定"派给谁"**——那是规则写死的

### 第 3 层 · 执行内自规划——**模型有有限的自作主张权**

`events`（再派活）/ `later`（复查）/ `ask`（拍板），受规则 `emits` 声明与 8 层跳数熔断约束。

### 时序图

```
[设计期]  人提需求 ──► AI 读 SKILL.md + 模板 ──► rules.json + Skill + 插件 ──► 人审
                                        （产物固化，可版本审计）
[运行期]  事件 ──► 内核纯代码匹配 ──► 派活（规则写死）──► 模型执行 ──┬─► 自作主张（events/later/ask）
                                                                    └─► 完成/交付
```

### 对德勤的两条新结论

1. **配置手册要写成"给 AI 读的"**（P0）：Autoloop 把整套配置说明做成 SKILL.md 分发给 Agent，让实施期由 Agent 帮客户生成规则与手册——**交付实施成本大幅下降**。我们的交付物应配套一份同样形态的 SKILL.md/配置指南，而不是只有 PDF 文档。
2. **AI 生成的规则必须带"首投灰度"**（P0）：AI 生成的 rules.json 可能埋雷（权限过宽、cwd 指错、askFirst 漏配、prompt 写歪）。Autoloop 自身的防线是「规则校验 + 版本审计 + 写错旧规则继续跑 + 报错卡片」；**缺的是"未经人审的规则首次上线"这道闸**——正好用 Super-agent 的 **observe 模式**补：AI 新写的规则第一次上线先只记录不执行，人核对后再放开。
   → 两项目互补关系落地：**Autoloop 的确定性派活 + AI 辅助生成配置，配 Super-agent 的 observe 灰度**，是一套相当完整的落地组合。

---

## 追加（2026-11-05 上午）：怎么用？启动入口与需求入口在哪

### A. Agent Autoloop

**装什么**
```bash
# 官方安装（装程序 + 启用登录后常驻服务）
curl -fsSL https://raw.githubusercontent.com/KKKKhazix/agent-autoloop/main/install.sh | sh
# 或：把 INSTALL.md 丢给 Claude Code / Codex，让它代装（作者推荐）
# 本地源码安装：sh install.sh --agent codex   （--agent claude / --command 'hermes chat -q {prompt}'）
```
- 程序：`~/.agent-autoloop/app`；配置：`~/.agent-autoloop/rules.json` + `config.json` + 密钥
- 前置：Node ≥24、Git、curl、**一个已登录的命令行 Agent**；目录权限 0700

**启动（三种）**
| 方式 | 命令 | 说明 |
|---|---|---|
| 常驻服务（默认） | 安装脚本自动装 systemd/launchd 服务 | 装完即在后台跑 |
| 前台跑 | `agent-autoloop up` | 调试/临时用 |
| 服务管理 | `agent-autoloop service install / start / stop` | |
| 自检 | `agent-autoloop status` / `doctor` / `try` | `try` 会真花额度跑一遍问答 |

**需求入口 = 事件，不是对话**（关键点）
| 入口 | 怎么接 |
|---|---|
| 定时 | rules.json 的 `when: {cron: "0 9 * * *"}` |
| GitHub / GitLab | Webhook 插件（内置） |
| 任意系统 | `agent-autoloop key new source <名字>` → 对方 `POST /v1/events` |
| 推不动的系统 | 轮询脚本 + `use: "command"` 的 Agent + `emits`（没新东西直接退出，**不花 token**） |
| 外部应用里的定时任务 | `agent-autoloop tell <编号> --task <任务名>` |
| **人要拍板** | 中台推卡片 → `agent-autoloop answer <卡片> <序号>` / `resolve` / `stop` |

**skill 的角色**：**可选**。`skills/agent-autoloop/SKILL.md` 是给 AI 读的"安装+配置手册"——装的时候让 Claude Code/Codex 读它来装、写规则、写 Skill；**装完运行时不依赖 skill**。

> 一句话：**不是"在 Codex 里跟它聊天"**。中台是常驻服务，事件进 → 内核按 rules.json 派活 → Codex 在自己的会话里干活 → 结果/卡片回来。你跟中台之间只有卡片交互。

### B. DeepSeek Super-agent（dsh-superagent-prototype）

**装什么**：它是 **DSH 的 bundle 插件**（Cordis patch），不是独立程序 → 必须先有 DeepSeek Harness。
前置：Node 22.19+/24、pnpm、git、tmux、python3、**GitHub CLI**、DSH、模型 provider；还要**专用 GitHub 账号**（agent account，agent 的所有发言都在这个名下）。

**安装**：官方也是"让 AI 带你装"——
> 「Read SETUP.md in this repository and set up dsh-superagent with me.」

SETUP.md 要求 AI **一次只问一个问题**，共 9 问：来源（GitHub only / +飞书）→ 仓库 → agent 账号 → 飞书群 → GitHub 允许名单 → 飞书允许人 → checkout 目录 → commit 身份 → **是否自动合并**（默认否）。
默认项：`profile superagent`（DSH web profile 的副本，独立端口 **3082**）、状态目录 `~/.dsh/state/superagent`、分支前缀 `agent/`、**accept mode = observe**（先记录不动手）、每小时自检修复。

**启动**：`dsh superagent --from-default-profile`（首次）或改 `cordis.patch.yml`；`scripts/dsh-superagent status` 退出码 0 = 正常。

**需求入口 = 聊天 / PR 评论里 @它**（跟 Autoloop 最大的不同）
- GitHub：在 issue 上评论 `@<agent登录名> <需求>` → **约 1 分钟内**面板出现一个 Ticket
- 飞书：@机器人 或私聊
- **Web 面板**：端口 3082，侧边栏 **Superagent** 条目，**只显示"需要人处理"的**
- 设置通过 Management API 保存：`github` source → `feishu` source → `policy`（允许名单）→ `executor` → prompts（含 commit 身份与自动合并要求）

**给人交底的三条规矩**（000-philosophy）：从窄的范围开始、往少噪音调、agent 说的话自己负责。

### C. 两者并排看「入口」

| | Agent Autoloop | DeepSeek Super-agent |
|---|---|---|
| 装的东西 | 独立程序 + 已登录 CLI Agent | DSH + bundle + 专用 GitHub 账号(+飞书) |
| 常驻进程 | 中台 hub 服务（+ worker） | DSH profile 进程（tmux）|
| **人怎么提需求** | **不聊天**：发事件（cron/webhook/HTTP/轮询） | **聊天**：issue 评论 @它 / 飞书 @它 |
| 人怎么收到回应 | 桌面通知/飞书卡片 → `answer` | 面板（只看需人处理）+ 原对话里回 + PR |
| skill 是否必需 | 可选（AI 读的安装配置手册） | 必需（SETUP.md 就是给 AI 的安装剧本）|
| 上手成本 | **低**（一条 curl） | **高**（DSH + 账号 + 名单 + 飞书）|
| 最小验证 | `agent-autoloop try` | `dsh-superagent status` + 在 issue 上 @ 它 |

### D. 对我们的现实结论

- **我们的服务器上想最快验证 → 选 Autoloop**（Linux 匹配，一条 curl，可接 `openclaw agent exec {prompt}`）
- **Super-agent 起步重**：DSH + 专用 GitHub 账号 + 允许名单 + 飞书机器人，我们目前没有这些前置
- **注意 OpenClaw 已覆盖的部分**：常驻 + 多频道 + 直接聊天入口 = Super-agent 的"人机入口"；Autoloop 补的是 **事件→规则→派活→审计** 这一段确定性中台。二者不冲突
