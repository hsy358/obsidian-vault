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
