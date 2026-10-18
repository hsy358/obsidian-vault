---
type: project-note
tags: [Jev, TypeSafe, heartbeat, OpenClaw, agent-architecture, 德勤项目]
source: 实操记录
created: 2026-09-22
status: 5/5 demo 通过
applicable_to: [OpenClaw, HEARTBEAT]
---

# Jev ④ Heartbeat 智能化接入完成

> 实操日期：2026-09-22 16:15
> 接续：① Prom 间过滤（9/9） + ② Cron 优先级（4/4） + ③ AgentRouter advisory（4/4）
> HEARTBEAT.md 之前完全为空，现已改造为 Jev pre-filter 驱动

## 一、核心问题

HEARTBEAT.md 之前只有占位注释（"keep empty to skip heartbeat"）。
心跳要么完全跳过（空文件）要么每次都触发完整 LLM 检查（不智能）。

实际需求：
- 大多数心跳 = 没事干 → 浪费 LLM token
- 真有事（API 出错、cron 失败、user 长时间不活跃）→ 应该立刻通知

## 二、解决方案：Jev Pre-Filter

心跳时先跑 `jev_heartbeat.py`，根据 6 类信号让 Jev 决定是否 act：

| 信号 | 来源 | 用途 |
|---|---|---|
| `vault_commits_24h` | git log | 高活跃度提示 |
| `api_error_recent` | vault-sync.log 含 2056 | Token Plan 见底 |
| `cron_recent_fail` | vault-sync.log 含 fatal | cron 异常 |
| `user_recent_active_min` | sessions.json mtime | 用户最近活跃 |
| `is_quiet_hour` / `is_business_hour` | 当前小时 | 23-08 静默 |
| `vault_uncommitted` | git status --porcelain | 未提交改动 |

Jev Noul 决策 → 输出 `{action: "act" | "quiet", checks: [...]}`。

## 三、测试结果（5/5）

```
# 场景                                              期望   Jev noul  实际
[1] 工作日下午，vault 活跃                          act    0.790     act    ✅
[2] 凌晨 3 点，一切正常                            quiet  0.100     quiet  ✅
[3] API 见底（今日踩的坑）                          act    0.910     act    ✅
[4] 傍晚，vault 安静，正常下班                      quiet  0.340     quiet  ✅
[5] 深夜 API 出错 + cron 失败 + vault 未提交        act    0.900     act    ✅

准确率：5/5 = 100%
```

## 四、实际心跳测试（2026-09-22 16:10 跑）

```json
{
  "action": "act",
  "reasons": ["jev_noul=0.790"],
  "signals": {
    "vault_commits_24h": 10,
    "api_error_recent": false,
    "cron_recent_fail": false,
    "user_recent_active_min": 1.8,
    "hour_local": 16,
    "is_quiet_hour": false,
    "is_business_hour": true,
    "vault_uncommitted": false
  },
  "checks": ["review_vault_recent_changes"]
}
```

→ Jev 准确判断：**act 但仅 review**，不刷屏。

## 五、调试时发现的小 bug

**症状**：user_recent_active_min 显示 960 min（实际才 1.8 min）

**根因**：`__pycache__` 没清，跑了上次 wrong 的逻辑
- 第一次改 `user_recent_active_min` 用 MEMORY.md mtime（不活跃时被误判为 sleep）
- 第二次改成 sessions.json mtime，但 pycache 还在用旧 .pyc
- **`rm -rf __pycache__` 后正确**

**教训**：开发期 wrapper 时加个 `# pyright: strict` 或者改完强制 clear cache。

## 六、落地文件

| 文件 | 用途 |
|---|---|
| `/root/.openclaw/workspace/skills/jev-filter/jev_heartbeat.py` | 主体 wrapper（170 行） |
| `/root/.openclaw/workspace/skills/jev-filter/heartbeat_demo.py` | 5 场景 demo |
| `/root/.openclaw/workspace/HEARTBEAT.md` | **之前为空，现改造为 Jev 驱动** |
| `/root/vault/2-Areas/AI-Agent-研究/Jev-OpenClaw-集成/2026-09-22 - Jev ④ Heartbeat 智能化接入完成.md` | 本笔记 |

## 七、HEARTBEAT.md 改造前后对比

| | 改造前 | 改造后 |
|---|---|---|
| 状态 | 空文件（注释说 keep empty to skip） | 有决策规则 + Jev pre-filter 指引 |
| 触发模式 | 全跳 / 全跑 | Jev 按信号智能判断 |
| Token 消耗 | 多数浪费 | 只 act 时耗 token |
| 输出长度 | （n/a） | quiet=0 / act=精简 |

## 八、待办

#### ✅ 已完成

- [x] wrapper 写好
- [x] 5 场景 demo
- [x] 实际心跳测试通过
- [x] HEARTBEAT.md 改造

#### ⏳ 未做

- [ ] 接到 OpenClaw 实际 heartbeat 钩子（hook 配置在 OpenClaw config）
- [ ] 监控：act rate / quiet rate / 漏报率

## 九、参考

* ① Prom 间过滤笔记：`2026-09-22 - Jev OpenClaw 预过滤接入记录.md`
* ② Cron 优先级：`2026-09-22 - Jev ② Cron 优先级接入完成.md`
* ③ AgentRouter advisory：`2026-09-22 - Jev ③ AgentRouter advisory 接入完成.md`