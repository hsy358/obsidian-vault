---
title: Birdview — 让 AI 编码 Agent 改代码前先画架构地图
type: project-note
tags: [birdview, ai-coding-agent, architecture-as-code, code-visualization, Qiuner]
url: https://github.com/Qiuner/birdview
site: https://qiuner.github.io/birdview/
fetched_date: 2026-09-22
status: archived
version: v0.3.1 (2026-09-22 release)
stars: 586 (10 天)
---

# Birdview — 让 AI 编码 Agent 改代码前先画架构地图

> **来源**：
> - GitHub: https://github.com/Qiuner/birdview
> - 项目站: https://qiuner.github.io/birdview/
> - 抓取日期：2026-09-22
> - 用户介绍：「Birdview 让 AI 编码 Agent 在改代码前先给项目画一张架构地图」

## 一、用户介绍要点（已与 AI 读）

1. **架构即代码**：每个模块有固定编号、归属文件和源码证据，关系可视化
2. **生成独立交互式 HTML 页面**：不用起服务，浏览器直接打开，支持多视图切换 + 改前改后对照
3. **可装成 Skill 默认自动介入，也能切到按需模式**：任务记录把"完成"和"检查通过"分开，避免 Agent 自说自话
4. **多 Agent 安装 + 自检**：v0.3.1 已支持

## 三、核心工作流

```
project source ──> architecture.json ─┐
                                      ├──> validate ──> render ──> standalone HTML
agent declarations ─> activity.jsonl ─┘
```

* **`architecture.json`** — 模块定义、职责、归属、证据、关系、视觉布局
* **`activity.jsonl`** — JSONL 把任务事件绑定到特定项目、地图版本、模块 ID
* **renderer** — 验证两个输入 → 生成视图
* **推荐工作流**：先 map → 再 expose 要动的模块 → 再带证据 edit

## 四、安装 & 使用

```bash
# 装到 codex 全局
npx skills add Qiuner/birdview --skill birdview --agent codex --global --copy --yes

# 装依赖 + 跑 doctor 自检
npm --prefix "$HOME/.agents/skills/birdview" ci
node "$HOME/.agents/skills/birdview/scripts/birdview.mjs" doctor

# 让 Agent 用 birdview（不编辑代码）
"Use Birdview to show this project's architecture; do not edit code."
```

* **依赖**：Node.js 18+ 和 npm
* **模式**：auto（默认）/ on-demand
* **doctor**：检查安装完整性，**不**检查 agent 激活状态

## 五、技术要点

* **MIT 开源**（vs jianying-headless 的非商用）
* **TypeScript** 实现
* **架构即代码**（architecture.json schema 验证）
* **改前改后对照**（双视图）
* **支持多 Agent 安装与自检**

## 六、与何大人的关联

### ⭐⭐⭐ **德勤项目强相关**

> **直接对接**：6-29 决策的「执行器抽象层 + 可插拔适配器」架构
> Birdview 是「Agent 改代码前先 map 架构」的现成模式

应用场景：
| 德勤项目场景 | Birdview 用法 |
|---|---|
| Agent MVP 改任何代码 | 先 map 架构 → 标本次动的模块 → 改 → 对照 |
| 德勤代码 review | 用 birdview render 出改前改后 diff 视图 |
| Agent 任务可追溯 | activity.jsonl 自动记录 |
| Skill 默认自动介入 | 德勤 Agent 可默认装 birdview Skill（auto 模式） |

### ⭐⭐ **OpenClaw 接入**

* OpenClaw 已有 skill 机制（per MEMORY.md）
* `~/.openclaw/workspace/skills/` 目录可装 birdview
* 但 birdview 是 Node.js（OpenClaw skill 是 Python 风格），可能需要 adapter

### ⭐ **Jev 体系直接受益**

* Birdview 跟 **Strands Harness**（我们今天归档过）同思路：架构即代码、可插拔
* **Jev + Birdview 组合**：
  - Birdview 做 architecture.json（结构化）
  - Jev 做 module 改动评分（"这次动这个模块风险多大？"）
  - Activity.jsonl 喂给 Jev 做 harness 推荐

## 七、同类项目（同赛道）

| 项目 | URL | 跟 Birdview 对比 |
|---|---|---|
| archify | github.com/topics/agent-architecture | 28k+ stars · 也是 architecture-as-code，但面向工程师 |
| shane9coy/Agent-Skill-Architecture-Guide | github.com/topics/agent-architecture | 跨 Claude Code/KiloCode/OpenClaw/OpenAI Codex 的参考 |
| BuilderIO/agent-native | gitnova trending | TypeScript · 单次定义 action，三处使用 |

## 八、v0.3.1 版本更新（今天 release）

* 用户提到 0.2.1 — **实际最新是 v0.3.1（2026-09-22 当天发布）**
* 增量更新未公开细节（需看 GitHub Releases）

## 十、待办

- [ ] 装一份到 OpenClaw `~/.openclaw/workspace/skills/birdview/` 试跑（如果兼容）
- [ ] 德勤 MVP demo 用 birdview 做 architecture.json（演示给德勤看"agent 改代码前先 map"）
- [ ] 写一份"如何在德勤项目用 birdview + Jev"的 1 页笔记