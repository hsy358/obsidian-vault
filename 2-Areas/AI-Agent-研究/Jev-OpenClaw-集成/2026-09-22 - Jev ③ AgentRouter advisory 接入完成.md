---
type: project-note
tags: [Jev, TypeSafe, AgentRouter, harness, advisory, agent-architecture, 德勤项目]
source: 实操记录
created: 2026-09-22
status: 4/4 demo 通过（1 个边界 case needs_human_review 正确触发）
applicable_to: [OpenClaw, AgentRouter, 德勤项目]
---

# Jev ③ AgentRouter advisory 接入完成

> 实操日期：2026-09-22 16:10
> 接续：① Prom 间过滤（9/9） + ② Cron 优先级（4/4）
> 决策来源：6-29 AgentRouter 5/5 harness 识别 + Strands Harness「只换模型不换身体」架构

## 一、核心问题

AgentRouter（AgentSpace daemon 子包）现状：
- 5 个 harness 全支持：claude / codex / opencode / openclaw / hermes
- `detect` 命令已能识别 5/5
- **`run` 必须显式指定 `--harness`** —— 没有自动路由

每次任务进来都要人决定用哪个 harness，决策成本高 + 容易选错。

## 二、解决方案：Advisory 路由

不自动执行（Jev 出错就完蛋），只**推荐**最合适的 harness，留人确认。

```bash
python3 /root/.openclaw/workspace/skills/jev-filter/jev_auto_route.py \
    "Review this PR for security issues" \
    --cwd /root/vault/1-Projects/德勤

# → 推荐 harness + 概率分布 + needs_human_review 标记
# → 手动跑：agent-router run --harness claude ...
```

## 三、Jev 决策结构

```python
state = f"""Task: {prompt}
Working directory: {cwd}
Available harnesses: {avail}"""

questions = {
    "best_harness": Choice(
        instructions="Pick the best harness. Match task to harness strength. Prefer specialized over generic.",
        criteria={
            "claude": "code review, comments, doc, security audit, refactoring analysis, single-pass deep analysis",
            "codex": "bulk code generation, multi-file refactor, test generation, scaffolding",
            "openclaw": "OpenClaw internal ops, cron config, wechat, gateway hooks, internal admin",
            "hermes": "multi-step research, multi-step workflows, dispatcher, kanban, long-horizon tasks, deep research reports",
            "opencode": "general coding agent, lightweight, OpenRouter-compatible",
        },
    ),
    "needs_human_review": Noul(
        instructions="Is confidence high enough to auto-execute? Return true (= needs review) if ambiguous task / risky change / uncertainty. Default: true (safe)."
    ),
}
```

**只把 available harness 喂给 Jev**（不会推荐 unavailable 的）。

## 四、测试结果（4/4）

```
# 任务                                              期望    Jev 推荐   置信度   review
[1] Review this PR for security issues              claude  claude     1.000    需要 ✅
[2] Generate a TypeScript REST API with 5 endpoints codex   codex      1.000    需要 ✅
[3] 改 OpenClaw 的 cron 配置                        openclaw openclaw  1.000    需要 ✅
[4] 研究德勤 AI Native Workspace 竞品 + 1 页报告    hermes  hermes     0.260    需要 ✅

准确率：4/4 = 100%
```

#### 关键发现

| 现象 | 含义 |
|---|---|
| **场景 1-3 conf=1.000** | 任务类型明确时 Jev 100% 确定 |
| **场景 4 conf=0.260** | research 类任务边界，Jev 显式说不确定 + 需要 review |
| **needs_human_review 始终触发** | 保守默认值生效，符合 production 安全要求 |

## 五、⚠️ 调试时发现的关键 Bug（已修复）

**症状**：所有 Jev API 调用突然 401 / UnicodeEncodeError

**根因**：TYPESAFE_API_KEY 在 ~/.bashrc / /etc/profile.d / /etc/environment 三处配置不当
1. `~/.bashrc` 顶部有 `[ -z "$PS1" ] && return` 守卫，非交互 shell 读不到 key
2. 我后续用 sed/cat 重新写入时，**实际写错了 key 的中间段**（应为 `0b294662_59e4...b4daf22`，我写了 `af4c28b1...45a4af22`）
3. /etc/environment 是 PAM 加载的，bash 脚本读不到

**修复**：
- ~/.bashrc：在 PS1 守卫**前**加 `[ -n "$TYPESAFE_API_KEY" ] || export TYPESAFE_API_KEY="..."`
- /etc/profile.d/jev.sh：login shell 用
- /etc/environment：所有进程继承

**验证**：
```bash
bash -c 'source ~/.bashrc; echo ${#TYPESAFE_API_KEY}'  # → 108
bash -lc 'echo ${#TYPESAFE_API_KEY}'  # → 108 (login shell)
```

## 六、落地文件

* `/root/.openclaw/workspace/skills/jev-filter/jev_auto_route.py` — advisory 路由（120 行）
* `/root/.openclaw/workspace/skills/jev-filter/auto_route_demo.py` — 4 场景验证
* `/root/.bashrc` — 修正后的 TYPESAFE_API_KEY 配置
* `/etc/profile.d/jev.sh` — login shell 用（权限 600）
* `/etc/environment` — 全局环境

## 七、用法（未来调用 AgentRouter 时）

```bash
# Step 1: 让 Jev 推荐
python3 /root/.openclaw/workspace/skills/jev-filter/jev_auto_route.py \
    "fix failing test in src/foo.ts" \
    --cwd /root/workspace/project

# 输出：
#   🎯 推荐 harness=codex (conf=0.85)
#   💡 执行：agent-router run --harness codex --cwd /root/workspace/project "fix failing test in src/foo.ts"

# Step 2: 人 review 后跑（或修改 --harness 覆盖）
agent-router run --harness codex --cwd /root/workspace/project "fix failing test in src/foo.ts"
```

## 八、待办

#### ✅ 已完成

- [x] advisory wrapper 写好
- [x] 4 场景 demo 验证 100%

#### ⏳ 未做（等用户拍板）

- [ ] 接入 AgentRouter 正式 CLI（加 `auto` 子命令到 `agent-router`）
- [ ] 与 ① inbound hook 联动（inbound 自动路由而非手动）
- [ ] 持久化路由历史 → 学习用户偏好（v2）

## 十、参考

* ① Prom 间过滤笔记：`2026-09-22 - Jev OpenClaw 预过滤接入记录.md`
* ② Cron 优先级笔记：`2026-09-22 - Jev ② Cron 优先级接入完成.md`
* Strands Harness 文章：`2-Areas/公众号文章/2026-09-22 - AWS开源Strands Harness：Agent开始只换模型、不换身体.md`
* AgentRouter 源码：`/root/AgentSpace/packages/daemon/src/agent-router/`