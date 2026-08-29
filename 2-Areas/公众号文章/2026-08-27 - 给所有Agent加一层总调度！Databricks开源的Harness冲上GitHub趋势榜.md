---
title: "给所有Agent加一层总调度！Databricks开源的Harness冲上GitHub趋势榜"
author: "智猩猩AI"
publish_date: "2026-08-27 18:58:51"
saved_date: "2026-08-29"
source: "wechat"
url: "https://mp.weixin.qq.com/s/YOu4RBebv-f3cqxQJGAvsg"
type: article
tags: [Omnigent, Databricks, Agent编排层, meta-harness, 可插拔执行器, Hermes, Claude-Code, Codex, 跨厂商Agent, 德勤-MVP, AI-Native]
---

# 给所有Agent加一层总调度！Databricks开源的Harness冲上GitHub趋势榜

> 来源：智猩猩AI 编辑：金水
> 项目：[omnigent-ai/omnigent](https://github.com/omnigent-ai/omnigent) （9.3k star, GitHub Trending）
> 版本：v0.11.0（2026-08-26 发布）

## 核心命题

AI 编程 Agent 井喷（Claude Code / Codex / Cursor / OpenCode / Hermes / Pi），但**每个都像不同品牌的遥控器，凑不到一块**。

**Databricks Omnigent 的答案**：别再逐个适配 Agent，**建一个覆盖所有 Agent 的"元编排层"（meta-harness）** ——在 Claude Code、Codex、Cursor、OpenCode、Hermes、Pi 之上套一层统一调度，换 harness 不用重写代码，组合多个 Agent 不用从零搭框架，策略与沙箱统一下发。

## 凭什么统一所有 Agent

支持的 harness（v0.11.0）：
- **Claude Code** / **Codex** / **Cursor** / **OpenCode** / **Hermes** / **Pi** / 自研 Agent
- 想换底层引擎？**改 YAML 里一个字段就行** —— Skill/MCP/插件从具体厂商抽离到统一层

### 1. Agent 互相协作、互相挑刺 ⭐ 核心亮点

Omnigent 不是单雇一个 Agent，而是**同时拉起多个 Agent 互相当质量关卡**。

**Polly 示例**（技术主管型）：
1. 理解需求 → 拆任务
2. 把子任务分给多个写代码的子 Agent（Claude Code / Codex / Pi）
3. **每个 Agent 在独立 git worktree 里干活**——互不干扰
4. 把每个 Agent 产出的 diff 路由给**不同厂商**的审查者（例：Codex 写 → Claude 审）
5. diff 摆在你面前 → 你拍板 merge

**Debby 示例**（双头脑暴）：
- 你抛问题 → 同时丢给 Claude 和 GPT
- 答案并排摆出来
- `/debate` 两个模型你来我往辩几轮 → 收一个结论

### 2. 跨设备同步与实时协作

- 同一 session：终端起头 → 浏览器继续 → 手机收尾
- **服务端持有会话状态，客户端只是视图**——团队围观 / 评论 / 接手变成可能

### 3. 策略治理与云沙箱（最后落到可控）

- **三层 Policy 叠加**（server / 单 Agent / 单会话），越细规则优先级越高
- 内置：审批危险操作、限制调用次数、**硬性花费封顶**（`max_cost_usd: 5.00`）
- 配合 Modal / E2B / K8s 云沙箱：Agent 跑在远端一次性环境，本机不必一直在线

## 怎么上手

```bash
# 安装
curl -fsSL https://raw.githubusercontent.com/omnigent-ai/omnigent/main/scripts/install_oss.sh | sh
# 安装后得到 omnigent 和 omni 两个一模一样的命令

# 启动
omnigent claude                # 跑 Claude Code，session 可分享团队
omnigent codex                 # 跑 Codex
omnigent run examples/polly/   # 直接跑 polly
```

### YAML 声明 Agent

```yaml
name: my_agent
prompt: You are a helpful data analyst.
executor:
  harness: claude-sdk     # 也能换成 codex、cursor、pi...
tools:
  word_count:
    type: function
    callable: mypackage.mymodule.word_count
  researcher:
    type: agent
    prompt: Search for relevant information and summarize it.
    tools:
      word_count: inherit
```

### 现成示例

| 示例 | 玩法 |
|---|---|
| `examples/polly/` | 技术主管型：规划 → 并行子 Agent 写 → 别家 Agent 审查 |
| `examples/debby/` | 双头脑暴（Claude + GPT 答案并排互怼） |
| `examples/deep-research/` | 联网做带出处的研究报告 |

## 项目立场（原作者总结）

> "AI Agent 正从'单兵作战'走向'兵团作战'，编排层 / 调度层会是接下来开源圈最值得盯的方向之一。"
>
> **冷水**：还在 alpha，生产环境别贸然上；harness 适配矩阵还在补齐。
>
> **方向很清晰**：你的 Agent 不该被某个厂商的遥控器绑架——这一层，正在被开源填上。

---

## 🧠 小助分析（与德勤 MVP 强相关）

### 🎯 直接命中的决策点

**6-29 何大人决策**："Hermes / OpenClaw / Codex / Claude Code 等都是可插拔 Agent 执行器——德勤项目需要设计**执行器抽象层**，每种都能接"。

**Omnigent 就是这个抽象层的开源实现**——对应位置：**德勤 MVP 的执行器抽象层（Executor Abstraction Layer）**。

### 三个可借鉴点

1. **Harness YAML 配置即一切**
   - 改 `executor.harness: claude-sdk` 为 `codex` / `cursor` / `pi`，整个工作流不动
   - **德勤 MVP 抽象层接口应该返回 / 写入同样的 YAML 结构**——不要每个执行器写不同的 config

2. **Polly 模式 = 德勤"AI 主管"原型的开源参照**
   - 规划 → 多 Agent 并行 in git worktree → **异厂商审查** → diff 拍板
   - 德勤项目里"Mentor Agent / AI Lead" 角色，正好对应 polly
   - **直接抄 examples/polly/ 的 git worktree 隔离方案**——这是关键的工程正确性保障

3. **三层 Policy + 硬花费上限**
   - `max_cost_usd: 5.00` 这种硬约束写法 → 直接进德勤 MVP 的 cost guard
   - **云沙箱（Modal / E2B / K8s）思想**：德勤交付时客户机环境隔离问题，一次性 remote sandbox 比让客户机常驻稳

### ⚠️ 风险点

- **alpha 阶段**：生产别用，但**作为德勤"执行器抽象层"参考实现完全够用**
- **适配矩阵不完整**：少数厂商 native 模式还得等——Omnigent 已经支持的 6 个 harness，德勤可全接
- **Databricks 主导**：商业公司驱动，未来可能有商业化压力（vs. 纯社区版本）

### 📌 一句话结论

> **Omnigent 是德勤 MVP"可插拔 Agent 执行器 + 多厂商协作 + 策略治理"的开源验证版**——可以直接 fork `examples/polly/` 作为 MVP 第一版 demo 的骨架，节省 1-2 周实现时间。

### 行动建议（建议优先级排序）

| # | 行动 | 预期收益 |
|---|---|---|
| 1 | 克隆 [omnigent-ai/omnigent](https://github.com/omnigent-ai/omnigent) 本地跑通 `examples/polly/` | 验证多 Agent 协作可行性（半天） |
| 2 | 对比 `Omnigent harness 接口` vs `Hermes dispatcher 接口`，合并 / 互译 | 减少德勤抽象层重复设计（2-3 天） |
| 3 | 把 `max_cost_usd` 等 Policy 模型抽出来，套上德勤成本守卫 | 立刻可用（1 天） |
| 4 | 只调研不动手 | ✗ 错过 0.14 → 0.15 的窗口期 |
