---
title: JevAgentHarness 分析 —— 决策模型与 LLM 共享控制权（论文 + 开源实现）
date: 2026-11-05
type: research-note
subject: arXiv:2610.21412 / github.com/JevAgentHarness/JevAgentHarness
authors: Kunlun Zhu, Tao Feng, Xu Han, Heng Wang, Ling Yang, Xiangru Tang, Jiaxuan You, Heng Ji (UIUC / Princeton / Google)
tags: [决策模型, 模型路由, 成本治理, 开源Agent, 阈值拟合, 德勤项目]
related_notes:
  - 2026-11-05 - Agent Autoloop - GitHub 仓库分析.md
  - 2026-11-05 - 德勤 Agent 平台借鉴清单 v1（Autoloop×Super-agent×DSH）.md
  - 2026-11-05 - 德勤 Agent 调度内核原型 v0.1 - 实现与验收.md
  - ../../2-Areas/AI-Agent-研究/Jev-OpenClaw-集成/（2026-09-22 四个接入点）
---

# JevAgentHarness 分析（2026-11-05）

> **一句话**：把"这一步该用便宜模型还是强模型"的判断，从 LLM 手里交给一个**小决策模型**，
> 通过**本地 OpenAI 兼容代理**接入，**harness 一行不改**；省 28–64% 成本、4–43% 时间，成功率与纯强模型持平（误差 3 点内）。

## 0. 何大人转述的核实结果：✅ 全部属实，且论文里还有几条更重要的**负面结论**

| 转述 | 核实 | 备注 |
|---|---|---|
| 74 个 Terminal-Bench 2.0 任务 | ✅ | 每 harness 74 题、各跑 1 次 |
| 成本降 28–64% | ✅ | 取决于快模型与强模型的价差（见 §3.3） |
| 耗时缩短 4–43% | ✅ | |
| 成功率与纯强模型持平（误差 3 点内） | ✅ | 但**统计功效弱**：74 题、1 次跑，95% CI 很宽 |
| 小模型判断"廉价 vs 强模型" | ⚠️ 表述需修正 | 论文实际做的是**多选决策委托**（决策模型给每个选项打分），"路由"只是其中一种模式 |
| 无需改动原 harness | ✅ | 靠本地代理 + 模型名 `jah-auto` |

**论文里三条更该知道的**：

1. **孤立问答最强的决策模型，放进 agent 里只解出 69.5% 的任务。**
2. **不设拟合阈值直接委托工具选择，成功率掉 19.0 个点。**
3. 论文自己在 agent 循环里，**只有"工具选择 / 参数选择"两处 cascade + 拟合阈值**同时做到省成本且不掉成功率；
   其它 yes/no 类决策点（停止判断、反思触发）**并没有省下成本**。

## 1. 机制拆解

### 1.1 代理位置（不改 harness 的关键）

```
Harness (Codex / pi / DSH / mini-swe-agent / Terminus-2 / 任何 OpenAI 兼容客户端)
   │  base_url = http://127.0.0.1:8787/v1 ，api_key = "jah"（dummy）
   ▼
JevAgentHarness 代理
   ├─ 决策模型：读 agent 当前状态 → 回答"下一步 routine 还是 hard" → p(hard)
   ├─ 路由：p(hard) ≥ τ → strong tier；否则 → fast tier
   └─ 上游：strong tier / fast tier（可分属不同 provider）
```
模型名：`jah-auto`（路由）/ `jah-strong`（全强）/ `jah-fast`（全快）—— 同一任务跑两种名字即可做 A/B。

### 1.2 三条硬规则（安全与质量的地基）

1. **第一步永远走强模型**（读任务、做规划）
2. **"任务是否完成"的判断永远走强模型**（快模型想收尾时，强模型重做该步）
3. **任何错误都回退强模型**：决策模型超时/报错 → 强模型；快模型调用失败 → 强模型。
   → **agent 永远不会因为路由器而停摆**

### 1.3 八个决策点 × 五种模式

| 决策点 | 模式 | 含义 |
|---|---|---|
| `routing` | cascade(默认) / guard / shadow / off | 这一步写强模型还是快模型 |
| `tool_select` | cascade / assist / guard / shadow | 强制选工具 / 给 LLM 候选shortlist / 强模型复核 |
| `stop` | strong(默认) / guard / trigger / shadow | 结束判断 |
| `reflection` | trigger / always / shadow | 卡住时把该步升级到强模型 |
| `action` | guard / shadow | **危险命令二次把关**（`rm -rf`、`git push --force`、`DROP TABLE`、部署…） |

五种整合模式：**Cascade**（决策模型先答，置信够就用）· **Replace**（决策模型说了算）· **Assist**（给 LLM 候选）· **Guard**（复核 LLM 的选择）· **Trigger**（决定某步要不要跑）。

### 1.4 阈值规则（论文公式）

$$c(s) \ge q_L - \frac{\Delta C}{V}$$

`c(s)`=决策置信度，`q_L`=LLM 做对该选择的正确率，`ΔC`=省下的一次 LLM 调用成本，`V`=一次错误选择的代价。
→ **决策模型可以比 LLM 差一点，只要省下的钱盖得住多犯的错。**

## 2. 开源实现盘点（MIT 代码，24 个源文件 ≈ 175KB）

```
src/jevagentharness/
  server.py    38KB  代理主逻辑（OpenAI Chat + Responses 两种方言）
  points.py    30KB  八个决策点 × 模式的全部实现
  router.py    10KB  分档路由
  fit.py       11KB  ★ 阈值拟合（最值得抄）
  decision.py  9.7KB 决策后端：jev(openrouter/typesafe/local) + rules + none
  config.py   10.5KB  配置模型
  prices.py    4KB   价格表（用于成本核算）
  report.py    3.8KB jah report
docs/  configuration.md / harnesses.md / modes.md
bench/ Terminal-Bench 2.0 评测、协议、结果
research/ 论文全部实验代码（含 AgentDecision-4B 训练）
```

### 2.1 ★ `fit.py` 的阈值拟合算法（可直接抄的工程方法）

```
fit_point(records, point, target=0.95, min_count=30, z=1.645):
  1. 取带标签记录（fit_ok、无 error、有 label、非单工具场景）
  2. 遍历所有候选阈值 t：
       子集 = {score ≥ t}
       n_accepted = |子集|，coverage = |子集|/|全部|，agreement = 子集内与 LLM 一致的比例
       lower = Wilson 得分下界(k/n, z=1.645)   ← 单侧 95% 置信下界
  3. 取第一个满足 **n_accepted ≥ 30 且 lower ≥ 0.95** 的 t（再取整到 0.01）
  4. 输出配置片段
```
> 📌 **这就是我们手写阈值（0.5 / 0.6 / 0.75）与论文方法的本质差距**：
> 手写阈值 = 拍脑袋；拟合阈值 = **"样本量 ≥30 且一致率下界 ≥95% 才允许委托"**，否则一律不委托。

### 2.2 `rules` 决策后端：**零模型、零 key、零依赖**

判据只有三条（`decision.py::RulesBackend`）：
- 连续两次相同动作 → `repeated_action`，p(hard)=0.9
- 最近输出命中错误正则（取尾部 6000 字符）→ `error_signal`，p(hard)=0.9
- 都没命中 → p(hard)=0.1
- 危险命令命中预过滤 → `action_risk`，p(risky)=0.9

并且**明确拒绝**回答 `next_tool` / `task_done` / `already_done` / `fast_step_ok` —— 需要模型的决策点，**宁可退回 LLM-only 行为**。

### 2.3 运维抓手

| 命令 | 作用 |
|---|---|
| `jah serve --preset shadow` | **所有决策点只记录不改行为**（= 我们内核的 observe 灰度） |
| `jah fit <logs>` | 在自身轨迹日志上拟合阈值并打印配置片段 |
| `jah report <logs>` | 每个模型名：会话数、步数、强模型占比、每会话 $ 与 LLM 秒数 |
| `curl localhost:8787/stats` | 实时花费、分档占比、会话数 |
| `budget_usd` | 超过预算拒绝新会话（成本闸门） |

日志：`steps.jsonl`（每步的档位/原因/p(hard)/token/成本/延迟）、`decisions.jsonl`（决策点、模式、概率、它做了什么、LLM 自己选了什么 —— `jah fit` 读它）、`states.jsonl`（决策模型看到的完整状态，**opt-in**，用于训自己的决策模型）。
**安全声明**：prompt / 输出 / header / key **从不落日志**；代理默认只绑 `127.0.0.1`；**真实 key 只在代理环境里，harness 只拿到 dummy key** → key 不进 agent 沙箱。

## 3. 实验结果（务必连同限制一起看）

### 3.1 主结果（Terminal-Bench 2.0，74 题，Jev `jev-1.13`，τ=0.75）

| Harness | 成功率（纯强 → 路由） | Δ（95% CI） | 每题成本 | 每题耗时 | 留在强模型的步数占比 |
|---|---|---|---|---|---|
| mini-swe-agent | 66.2% → 63.5% | −2.7 [−14.9, +8.1] | $0.91 → $0.33（**−64%**） | 13.7 → 7.9 min（**−43%**） | 45% |
| pi | 52.7% → 56.8% | +4.1 [−6.8, +14.9] | $0.62 → $0.42（−31%） | 11.3 → 10.8 min（−4%） | 55% |
| DeepSeek Harness | 66.2% → 66.2% | +0.0 [−8.1, +8.1] | $0.94 → $0.68（−28%） | 13.4 → 11.4 min（−15%） | 50% |
| Terminus-2 ¹ | 27.0% → 41.9% | +14.9 | $0.11 → $0.14（**+27%**） | 22.6 → 16.1 min（−29%） | 44% |

¹ **这一行不成立**：Terminus-2 走纯 JSON 对话，53/74 基线任务超时，空回复让基线"看起来更便宜" → 官方标注 **inconclusive**。

**作者自己的判读**：成功率列要读作"**没有可检出的损失**"，不是"变好了"。CI 很宽。

### 3.2 什么没work（开发集 15 题，仅供选型）

| 模式 | 实测 |
|---|---|
| tool_select cascade | 编码场景只有 1–4 个工具，**没有可靠可执行的阈值**（p≥0.99 时覆盖仅 7.9% 步、96% 一致） |
| stop guard | p(done)≥0.9 在 **0/60** 次快模型收尾上命中 → 不可用 |
| routing guard | 比 cascade 更贵 |
| action guard | **0/8 触发**，最高 p(risky)=0.02 → 编码场景几乎不触发 |
| reflection trigger | 唯一看起来有益的（3 个样本都领先），但样本太少不能下结论 |

其它事实：6533 次决策调用只失败 1 次（OpenRouter 499）；决策调用成本仅占总成本 **0.7%–3.6%**；17 次 agent 超时算失败。

### 3.3 省多少，取决于两件事（最实用的一条）

1. **价差**：Gemini 3.8 Flash 只比 Argon 便宜 ~2.7× → 只省 7–13%；**Flash-Lite 便宜 4–7× → 省 28–64%**
2. **留在强模型的步数**：每次跑都有约一半的步被判为 hard 留在强模型，账单仍由强模型主导

> 📌 **对我们的直接含义**：MiniMax M3 → M2.7 的价差不大（且 M2.7 更弱），
> **照搬这套路由大概率只能省个位数到十几个点**，除非我们能拿到 4–7 倍价差的档位。
> 先量价差，再决定要不要做。

## 4. 模型与数据（HuggingFace `JevAgentHarness`）

| 名称 | 内容 | 许可 |
|---|---|---|
| AgentDecision-4B | Qwen3-4B 上的 LoRA，训于 agent 状态 + 公开工具使用数据 | **CC BY-NC 4.0（非商用）** |
| AgentDecision-4B-v1 | 注册 Stage-2 测试前冻结的检查点（SFT+GRPO） | CC BY-NC 4.0 |
| AgentDecision-0.8B | 同配方，底座 StartLux-Decision-0.8B | CC BY-NC 4.0 |
| AgentDecisionBench | 基准数据集 | CC BY 4.0 |
| AgentDecision-train | 训练数据（agent 状态 + Jev 软标签） | CC BY-NC 4.0 |
| coding-agent-decisions | 代理在 Terminal-Bench 2.0 上的逐步决策日志 | CC BY-NC 4.0 |

⚠️ **官方警告（README 原文）**：这些模型**训于 DecisionGym 的客服状态，不是编码 agent**；
用之前必须 `--preset shadow` + `jah fit` 拟合阈值。

## 5. 与我们已有 Jev 集成（2026-09-22）的差距

我们本地 `skills/jev-filter/` 已有四个接入点：① 入站预过滤 ② Cron 优先级 ③ AgentRouter advisory ④ Heartbeat 智能化（+ Model Router）。

| 维度 | 我们现在的做法 | 论文方法论 | 差距 |
|---|---|---|---|
| 阈值 | **手写** 0.5 / 0.6 / 0.75 | 自身轨迹拟合 + Wilson 下界 ≥95% + 样本 ≥30 | ⚠️ **最大差距** |
| 决策模型 | 云端 Jev（`jev-1.13`，需 `TYPESAFE_API_KEY`；**无 key 时 fail-quiet**） | Jev / 自托管 / **rules(零 key)** / AgentDecision-4B | 可零 key 落地 |
| 作用范围 | 只是"要不要 act / 路由建议" | 八决策点 × 五模式，可控可 shadow | 我们只做了 1–2 个点 |
| 失败回退 | fail-quiet（不做事） | 全部回退强模型 | 方向一致 |
| 审计 | 缺决策溯源 | steps.jsonl + decisions.jsonl（可接内核 facts） | 可补 |

**结论**：我们 2026-09 的判断方向是对的（Jev 型决策模型适合做分流），但**实现还停在"论文批评的早期形态"**：
手写阈值 + 单点 advisory + 依赖云 key。

## 6. 对德勤项目的落地建议（分层）

### ✅ 可以直接抄（方法论 > 代码）
1. **阈值拟合纪律**：委托准入 = 样本 ≥30 **且** 一致率 Wilson 下界 ≥95%（`fit.py` 算法）
2. **`shadow` 先行**：任何决策点先只记录不改行为 —— 与我们内核的 observe 灰度同构，可直接对齐
3. **失败回退强模型**：路由器永远不能让 agent 停摆
4. **rules 决策后端**（重复动作 / 错误信号 / 危险模式）—— 零 key、零依赖，**且完全符合我们"内核确定性、零出站"的原则**
5. **key 不进沙箱**：代理持真 key，agent 侧只拿 dummy key → 这正是 Super-agent 遗留四问里"**凭证如何能被使用但永不进入模型上下文**"的现成答案
6. **预算闸门** `budget_usd` + 决策溯源日志

### ⚠️ 需要改造后用
- **双档路由**：我们没有 4–7 倍价差的档位；建议先在 Hermes 前做 **M3(strong) / M2.7(fast)** 的 shadow 采集，量出价差与"留在强模型的步数占比"再决定是否上线
- **Anthropic 兼容缺口**：jah 的 upstream 只支持 gemini / openai(chat) / openai_responses，**没有 Anthropic Messages API**；而 Hermes 走 Anthropic 兼容端点（MiniMax）→ **要么给 jah 加 anthropic upstream，要么我们自写一个 Anthropic 兼容双档代理**
- **决策溯源接入内核**：把 `steps.jsonl` / `decisions.jsonl` 的关键字段（档位、p(hard)、τ、是否回退）写入我们内核的 `facts` 表 → 满足德勤审计要求

### ❌ 不能直接用
- **AgentDecision-4B / 0.8B 权重：CC BY-NC 4.0 非商用** → **德勤是商业交付，不能直接用在客户生产环境**
- 官方也警告它们训于客服状态、编码任务未验证
- 论文的 Terminal-Bench 数字不能直接当我们的预期（不同模型、不同价差、统计功效弱）

## 7. 风险清单

| 风险 | 说明 | 缓解 |
|---|---|---|
| 成功率隐性下降 | 孤立问答强 ≠ agent 内可用；无拟合阈值直接委托掉 19 点 | Wilson 下界 ≥95% + 样本≥30 + shadow 先行 |
| 决策模型自身开销 | 每步多一次决策调用（0.15s、$0.0001/状态） | 实测仅占总成本 0.7–3.6%，可接受 |
| 快模型能力不足 | 快档在"卡住/收尾"上错率高 | 完成判断与失败步强制回强模型 |
| 价差不够 | 我们的 M3/M2.7 价差小 → 收益有限 | 先量价差再投入 |
| 许可 | 决策模型权重 NC 非商用 | 商业交付用 rules 后端或自训（数据可用部分需再核许可） |
| 审计断链 | 决策发生在模型层，不在我们内核视野内 | 决策日志 → 内核 facts 表 |

## 8. 建议的下一步（低成本、高信息量）

1. **不部署 jah，先取两类数据**：用 Hermes 跑一批德勤真实任务，记录每步的"是否困难"（可先用 rules 后端的三条判据 + 人工标注 100 步）→ 得出我们自己的"强模型步数占比"与"价差"
2. **把 Wilson 阈值拟合写进内核的规则校验**：`rules.py` 里对任何"决策委托"类规则要求附样本量与下界证据
3. **决策溯源字段进内核 facts**：`decision_point / tier / p / tau / fell_back`
4. 若上述三项结论为正，再考虑：给 jah 加 Anthropic upstream，或自写 Hermes 前置双档代理（我们已有 DSH/MiniMax 生态经验）

---

*核查方式：arXiv API + HTML 全文（§1–2）、仓库 README/modes 文档、`fit.py` 与 `decision.py` 源码、开发集与测试集结果文件。*
*注：本机到 github.com:443 不通，仓库文件经 raw.githubusercontent + Contents API 逐份获取。*
