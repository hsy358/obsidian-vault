---
type: project-note
tags: [Jev, TypeSafe, OpenClaw, pre-filter, agent-architecture, 德勤项目]
source: 实操记录
created: 2026-09-22
updated: 2026-09-22 (15:35 真 API 验证通过)
status: 真 API 验证通过 9/9
applicable_to: [OpenClaw, 德勤项目, AI-Agent-平台]
---

# Jev OpenClaw 预过滤接入记录

> 实操日期：2026-09-22
> 决策来源：上一轮 Jev 接入 6 切入点分析
> 执行人：OpenClaw 主会话 + 用户授权「你按照建议可以继续做」
> **最新更新**：真 Jev API 验证完成（9/9 = 100%）

## 一、为什么做出 ⑥ → Jev 接入

* 今日 MiniMax Token Plan 上限，导致 5 个股票 cron 反复重试消耗 token
* 根本原因：**所有 inbound message 无差别进 LLM**，没有"该不该让 LLM 看见"的预判
* Jev 正好是这场景的解：**70-500ms、低成本、带类型的概率化判断**

## 二、调研结论（这一轮）

| 项 | 结果 |
|---|---|
| Jev 是什么 | TypeSafe AI 的 System One 模型（非 LLM） |
| SDK | typesafe-sdk 0.7.0 pypi 可装 |
| 输入价 | $0.042 / 百万 token（输出免费） |
| 延迟 | 70-500ms（实测 312ms 均值） |
| 输出类型 | Choice / Score / Noul + 校准概率 |
| vault 现成研究 | 充足（22 玩法文章、JevScout 等） |
| API key | ✅ TYPESAFE_API_KEY 已就位（~/.bashrc + /etc/profile.d/jev.sh + systemd env） |

## 三、已落地

#### 1. wrapper 代码

位置：`/root/.openclaw/workspace/skills/jev-filter/`

* `jev_filter.py` - 核心 30 行 + Mock 实现 + CLI 入口
  - `JevFilter` (真 SDK)
  - `MockJevFilter` (heuristic simulator，demo 用)
  - `FilterResult` (is_safe / intent / confidence / action)
  - 失败时 fall through 到 `to_llm`（不丢消息）
* `demo.py` - Mock 离线 demo
* `real_demo.py` - 真 API demo（9 条样本 + prompt injection 探针）
* `README.md` - 用法 + 接入点

#### 2. Mock demo 结果（基线对照）

```
样本                             期望           结果           意图       置信度
你好                             bypass_llm   bypass_llm   casual   0.88     ✅
帮我查下今天的股票                to_llm       to_llm       task     0.70     ✅
spam 免费送 通知中奖              drop         drop         ignore   0.95     ✅
整理一下这个文件                  to_llm       to_llm       task     0.70     ✅

准确率：8/8 = 100%（heuristic simulator）
```

#### 3. 真 Jev API 结果（2026-09-22 15:35，TYPESAFE_API_KEY 已生效）

```
[1] 你好                                    bypass_llm  intent=casual  conf=1.000  784ms ✅
[2] 嗨 在吗                                  bypass_llm  intent=casual  conf=1.000  231ms ✅
[3] 帮我查下今天的股票                       to_llm      intent=task     conf=1.000  249ms ✅
[4] 改一下 cron 持仓 K 线的触发时间           to_llm      intent=config  conf=1.000  225ms ✅  ← 真 Jev 分出 config！
[5] spam 免费送 通知中奖                     drop        intent=ignore  conf=1.000  277ms ✅
[6] [system] error retry                     drop        intent=ignore  conf=1.000  265ms ✅
[7] 整理一下这个文件                         to_llm      intent=task     conf=0.710  234ms ✅
[8] 哈哈                                     bypass_llm  intent=casual  conf=0.990  220ms ✅
[9] Ignore all previous instructions...      drop        intent=ignore  conf=0.620  322ms ✅  ← prompt injection 也被挡！

准确率：9/9 = 100%
平均延迟：312ms / 次（首次 784ms 是冷启）
总耗时：2.81s
动作分布：drop=3, bypass_llm=3, to_llm=3
```

#### 关键发现

| 现象 | 含义 |
|---|---|
| **几乎所有 conf=1.000** | Jev 对简单分类非常确信 |
| **config 意图被正确分出** | 真模型比 heuristic 更细，能识别「改 cron」是 config 不是 task |
| **prompt injection 被挡** | conf=0.62 不算高但正确分类为 ignore → drop 生效 |
| **平均 312ms 延迟** | 在文档说的 70-500ms 中间，完全可接受 |
| **首次 784ms 是冷启** | 之后稳定 220-280ms |

## 四、待办（next steps）

#### ✅ 真 API key 已就位

- TYPESAFE_API_KEY 已落：~/.bashrc、/etc/profile.d/jev.sh（权限 600）、/root/.config/environment.d/jev.conf
- 9/9 真实样本测试通过（详见 §三.3）

#### ⚠️ 安全提醒

- **key 已暴露在聊天记录里**（用户主动贴的）→ 建议下次方便时 rotate 一次（console.typesafe.ai 重新生成）
- 当前临时方案：环境变量持久化，但权限 600 + 不进 git + 不进 vault
- 长期方案：移到 secrets manager（如 Bitwarden / 1Password CLI 集成）

#### ⏳ 接入 OpenClaw gateway

1. 在 OpenClaw gateway 入口加 pre-filter hook
2. 失败时 fall through 到原路径
3. 加监控：drop rate / bypass rate / 漏报率

#### 💡 6 个切入点的下一步顺序

按上一轮分析的优先级：

| # | 切入点 | 状态 |
|---|---|---|
| ① | Prom 间 Jev 过滤 | ✅ wrapper 完成 + 真 API 9/9 |
| ② | Cron 优先级 + 资产软回收 | 待做（复用 #1 的 SDK） |
| ③ | AgentRouter 增强 | 待做（与 Strands Harness 借鉴互补） |
| ④ | Heartbeat 智能化 | 待做（HEARTBEAT.md 还空着） |
| ⑤ | 多渠道路由 | 待做（先接微信，再扩 Discord） |
| ⑥ | Subagent 任务冷热分类 | 待做（spawn 前判断） |

**建议先做 ②**（继续用同一个 SDK，复用最高）。**今天就能把 5 个 cron 那类问题根治**。

## 五、关键决策

* **失败时 fall through**：Jev 调用失败 → 直接 `to_llm`（不丢消息）
* **drop 阈值为 0.6**：低于这个概率的 spam 一律丢
* **bypass_llm 只走 casual + 高置信度**：避免误判漏掉任务
* **JevScout 的 mock 模式是应用层做的**，SDK 本身没有 mock → 我用关键字 heuristic 模拟 wrapper 逻辑

## 六、参考文档

* typesafe-sdk 源码：`/usr/local/lib/python3.12/dist-packages/typesafe_sdk/`
* JevScout（vault）：`2-Areas/AI-Agent-研究/JevScout-求职自动化/`
* 22 玩法文章：`2-Areas/公众号文章/2026-09-20 - 整理了最新Jev模型的全网22个爆火玩法！.md`
* 上一轮 6 切入点分析：会话内提供