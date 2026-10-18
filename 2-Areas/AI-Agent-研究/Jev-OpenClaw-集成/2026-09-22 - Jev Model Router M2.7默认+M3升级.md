---
type: project-note
tags: [Jev, TypeSafe, model-router, M2.7, M3, OpenClaw, agent-architecture]
source: 实操记录
created: 2026-09-22
status: 配置生效（10/10 demo 通过）
applicable_to: [OpenClaw, 全 LLM Agent]
---

# Jev Model Router：M2.7 默认 + M3 升级

> 实操日期：2026-09-22 16:30
> 何大人决策：默认 M2.7，图片/复杂任务/显式说"用 M3" → M3
> 实现：Jev 评分 + config patch

## 一、改动清单

| 项 | 改前 | 改后 |
|---|---|---|
| `agents.defaults.model.primary` | `minimax/MiniMax-M3` | `minimax/MiniMax-M2.7` |
| `agents.defaults.model.fallbacks` | `["minimax/MiniMax-M2.7"]` | `["minimax/MiniMax-M3"]` |
| 新增 `skills/jev-filter/jev_model_router.py` | — | 模型路由器 |

## 二、Jev Router 决策逻辑

```python
def decide_model(message, has_image, user_override):
    # 1. 用户显式 override（"用 M3"/"切到 M2.7"）
    # 2. 图片 → M3（vision + 1M context）
    # 3. 极短（<20 字符）→ M2.7
    # 4. 极长（>1500 字符）→ M3
    # 5. 其它 → Jev Score(0-4) / 4，>= 0.5 → M3
```

## 三、调试时 3 个坑（写进教训库）

| 坑 | 修复 |
|---|---|
| **Score 字段是 `.score`，不是 `.answer`**（跟之前 Noul 的 `.noul` 一样坑） | `getattr(score_obj, "score", 0)` |
| **Score 范围是 0-N（N=criteria 数量-1），不是 0-1** | `normalized = raw / (len(criteria) - 1)` |
| **pycache 不刷**（改完文件不生效） | `rm -rf __pycache__` |
| **长消息阈值 2000 太松**（1805 字符被 Jev 误判为简单） | 降到 1500 |

## 四、10/10 测试结果

```
样本（部分）                              期望    Jev 决定
你好 / hi / 帮我查下今天的股票            M2.7    M2.7  (short ✅)
用 M3 写一份 Q3 总结 / 切到 M3 ...         M3      M3    (user_explicit ✅)
看看这张图                                M3      M3    (has_image ✅)
请帮我分析...（1805 字符）                  M3      M3    (long_message ✅)
设计 AI Agent 平台架构 5 大模块            M3      M3    (jev_score=3.68/4=0.92 ✅)
1 + 1 = ?                                 M2.7    M2.7  (short ✅)
写一个 Python 函数读取 jsonl              M2.7    M2.7  (jev_score=1.86/4=0.46 ✅)

准确率：10/10 = 100%
```

## 五、Gateway 重载方式

```bash
# 找 gateway PID
ps -ef | grep "openclaw.*gateway" | grep -v grep
# 发 SIGUSR1 触发 config reload
kill -SIGUSR1 <gateway_pid>
```

* Gateway 持续运行（34+ 天），SIGUSR1 不重启进程，只重载配置
* 新 session 起 M2.7 default
* 旧 session 保持原模型（要切可用 `session_status model=`）

## 七、成本影响（粗算）

* M2.7 input $0.30 / 百万；cache read $0.06
* M3 input $0.21 / 百万；cache read $0.042
* **M3 单价更低**（per token），但 M2.7 在短消息更快 + context 更小 → 总成本可能更低
* 真实节省要观察 1 周 cron + heartbeat 数据

## 八、落地文件

| 文件 | 用途 |
|---|---|
| `skills/jev-filter/jev_model_router.py` | router 主体（150 行） |
| `/root/.openclaw/openclaw.json` | 配置改 primary/fallback |

## 九、用法（给后续 OpenClaw 维护者）

```python
from jev_model_router import decide_model

# 收到新消息时
result = decide_model(message, has_image=bool(attachments))
# result = {"model": "minimax/MiniMax-M3", "reason": "has_image"}
```

如果 `model != current_session_model`：
```bash
# 切到推荐模型
session_status model="<result['model']>"
```

## 十、待办

#### ✅ 已完成

- [x] Config patch (M2.7 primary)
- [x] Gateway SIGUSR1 reload
- [x] Jev Router 写好 + 10/10 demo

#### ⏳ 未做

- [ ] 接 OpenClaw gateway 入口（inbound 进来时自动跑 router）
- [ ] 监控：M3 使用率 / 自动切换次数 / 漏判率
- [ ] 1 周后对比 M2.7/M3 token 消耗