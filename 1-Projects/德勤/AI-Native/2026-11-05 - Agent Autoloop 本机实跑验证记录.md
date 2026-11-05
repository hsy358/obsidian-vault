---
title: Agent Autoloop 本机实跑验证记录
date: 2026-11-05
type: verification-note
subject: Agent Autoloop（KKKKhazix/agent-autoloop）
host: VM-0-10-ubuntu / Linux / Node v24.22.1（nvm）
result: 全闭环跑通 ✅
tags: [Agent-Autoloop, 实跑验证, 事件溯源, 挂起零消耗, 注入防护, 成本治理]
related_notes:
  - 2026-11-05 - Agent Autoloop - GitHub 仓库分析.md
  - 2026-11-05 - Agent Autoloop × DeepSeek Super-agent - 异同对比.md
---

# Agent Autoloop 本机实跑验证记录（2026-11-05）

> 目的：不看 README 吹，实跑验证「事件 → 派活 → 干活 → 卡片拍板 → 接原会话续跑 → 完成」闭环与**审计链**。

## 0. 环境

| 项 | 值 |
|---|---|
| 系统 | Linux（VM-0-10-ubuntu），systemd degraded |
| Node | 默认 v22.22.2 → **需切 v24.22.1**（nvm 已装；安装脚本强制要求 ≥24） |
| 被派活的 Agent | **OpenClaw**（`openclaw agent --session-id autoloop-trial -m {prompt}`），command 模式 |
| 安装方式 | 本地源码快照 git init 后 `AGENT_AUTOLOOP_REPO=... sh install.sh --command '...' --no-service --port 3350` |
| 落盘位置 | `~/.agent-autoloop/`（app / config.json / rules.json / hub.db / master.key / worker/runs），目录权限 0700 |

**踩坑**：① Node 22 会被安装脚本直接拒掉；② `git clone` 本地 tarball 会失败（无 .git），需先 `git init` 成仓库；③ 容器里 systemd degraded，用 `--no-service` + 手动 `agent-autoloop up` 更稳。

## 1. 跑通的三轮

### 第 1 轮 —— **回执 JSON 非法，容错路径被真实触发** 🧪

Agent 输出结论「问了一个问题」，并附 `ask` 回执，但 JSON 非法：
原因是 `about` 字段里嵌了**未转义的英文双引号**（`如"蓝色"`）。

中台行为（**完全符合设计**）：
1. **不重做已完成的业务** —— 这一轮按第一行结论直接结束
2. 推一张卡片：「『试一下』的回执读不懂 ……（不是合法的 JSON：Expected ',' or '}' …）」
3. 原文留在 `~/.agent-autoloop/worker/runs/1-1/stdout-1.log`，留 14 天
4. `agent-autoloop answer 1` 即可结案

> **教训（对德勤直接相关）**：即使 Agent 很守规矩，也可能产出非法 JSON——只要它想在 JSON 字符串里写中文引号。
> 我们的回执协议必须：**① 明确禁止字段内出现英文双引号；② 提供更宽容的格式（如 key-value 或 YAML 片段）；③ 解析失败必须"保结论 + 通知人"，绝不重做业务。**

### 第 2 轮 —— 正常 ask 卡片 ✅

修正 prompt（去掉 `about` 字段 + 明确"字符串里不要出现英文双引号"）后：

```
【等你决定】#2 试跑：选一个颜色
  1. 蓝色
  2. 绿色
回答：agent-autoloop answer 2 <序号>
```

**挂起零消耗实测**：此时 `agent-autoloop status` 显示 **「在跑 0 · 排队 0 · 等你 1」**——
即**没有任何 Agent 进程存活**、没有 token 消耗，中台只是在等。等待期是纯状态，不是进程。

### 第 3 轮 —— **回答后接同一会话续跑并完成** ✅

```
$ agent-autoloop answer 2 1
收到，Agent 接着干。
在跑 1 · 排队 0 · 今天做完 2 · 等你 0
...
#3 试一下 做完了：你选了蓝色，试跑通过
```

### 审计链（`agent-autoloop why 3`）

```
第 3 轮 · 试一下
11-05 11:15:32  规则版本 #26
11-05 11:18:46  触发事件：来源 local · 类型 card.answered · 对象 无
11-05 11:18:46  本人回答「试跑：选一个颜色」：蓝色
11-05 11:18:46  vm-0-10-ubuntu 领取（Agent）
11-05 11:20:43  结束：你选了蓝色，试跑通过
```

> **一条命令查清某轮为什么这么跑** —— 这是可以直接进德勤演示的可观测性交付物。

## 2. 关键发现（对德勤最有价值的四条）

| # | 发现 | 对德勤的含义 |
|---|---|---|
| 1 | **挂起零消耗是真的**：ask 之后进程数为 0，状态在库里 | 人工审批节点可以放在任何执行器上，不用为"等审批"常驻一个 Agent 进程 |
| 2 | **续跑是"同会话"**：`--session-id` 固定 → OpenClaw 接着原会话继续，不是重开 | 对应我们"换执行器/重试不重做"的 Assignment 语义 |
| 3 | **command 模式不报 Token/费用**：`plugins/command/agent.ts` 的 `read()` 只返回 text，**不返回 usage，也不给会话链接、不支持内核级 resume**（resume 靠 CLI 自己带 session id） | ⚠️ **成本治理硬约束**：要精确 token/费用统计，必须写 **agent 插件**（如 Codex/ACP 插件那样能解析 usage），不能用 command 模式 |
| 4 | **OpenClaw 嵌套调用会掉到 embedded fallback**（gateway scope upgrade pending approval → gateway closed 1008 → embedded） | 我们的执行器在无 gateway 授权时会退化为本地内嵌运行——**部署时要把 gateway scope 授权纳入清单** |

## 3. 运维备忘（本机）

```bash
export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; nvm use 24   # 必须 Node 24
agent-autoloop up          # 前台启动中台（当前在跑，pid 见 ~/.agent-autoloop/up.pid）
agent-autoloop status      # 全局状态 + 轮数统计
agent-autoloop why <轮次>  # 审计链
agent-autoloop answer <卡片> [序号]   # 回答 / 结案
agent-autoloop check       # 校验 rules.json
agent-autoloop stop <轮次> / uninstall  # 停止
```

- 中台数据目录：`~/.agent-autoloop/`（0700）；备份需同时保留 `hub.db` 与 `master.key`（后者 0600，坏了中台拒绝启动）
- 当前实例**仍在后台运行**（端口 127.0.0.1:3350），需要收尾时 `agent-autoloop stop` + `uninstall --yes`（保留规则与数据）

## 4. 结论

**Agent Autoloop 的内核机制经实跑验证成立**：确定性派活、事件溯源、挂起零消耗、同会话续跑、非法回执容错，五项全部属实且行为符合设计。

**它不能替代的**：授权治理（Policy/Mandate）、多任务并行编排、Token 成本统计（command 模式）、停滞检测。
→ 再次印证：**目标形态 = Autoloop 的内核纪律 + Super-agent 的治理层**，二者互补而非替代。

---

*验证时间：2026-11-05 11:07–11:21（Asia/Shanghai）。证据留存：`~/.agent-autoloop/worker/runs/{1-1,2-1,3-1}/`、`hub.db` 事实日志。*
