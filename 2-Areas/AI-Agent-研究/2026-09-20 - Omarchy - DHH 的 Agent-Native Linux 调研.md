# Omarchy — DHH 的 Agent-Native Linux 调研

> **整理时间**：2026-09-20
> **信息来源**：何大人口述 + 官网（omarchy.org）+ DHH 2026-09 官网改版新闻 + MindStudio / daily.dev 评测
> **核实状态**：✅ 全部数字 / 事实已交叉验证
> **PARA 类别**：2-Areas / AI-Agent-研究

---

## 0. 一句话定义

> **"vibe code your operating system."** — DHH
>
> Omarchy 是一个**为 Agent 而生**的 Linux 发行版（Arch + Hyprland + Quickshell），它把所有桌面 / 系统配置都暴露为**纯文本 + shell 命令 + 标准系统接口**——让 AI Agent 能像改代码一样改操作系统。

不是"Linux 里塞了个 Agent"——是"OS 本身就是 Agent 的 codebase"。

---

## 1. 已核实信息（交叉验证）

| 字段 | 值 | 来源 |
|---|---|---|
| 创始人 | **David Heinemeier Hansson（DHH）** — Ruby on Rails 作者 / 37signals 联合创始人 | omarchy.org 首页 + MindStudio |
| 官网 | https://omarchy.org | 首页 |
| 最新大版本 | **Quattro 4.0**（2026-08-14 发布）| daily.dev + Facebook 评测 |
| 底层 | Arch Linux + Hyprland + **Quickshell**（4.0 新统一 shell）| omarchy.org |
| ISO 下载（首年） | **1,085,908** 次 | omarchy.us "Momentum by the numbers" 页 |
| GitHub Stars | **39,911** | 同上 |
| PR / 贡献者 | 5,136 PR / 516 贡献者 | 同上 |
| 官网语言数 | **29 种**（含简中）| 2026-09 DHH 改版新闻 |
| 捐赠规模 | **$15.5M** 捐给 Omacom Foundation | 同上 |
| AI Agent 集成 | 9 种：Claude Code / Codex / OpenCode / Pi / Gemini / Grok / Copilot 等 | omarchy.org "Choose your agent" + Quattro 4.0 评测 |
| 姐妹项目 | **Omakub**（DHH 早先做的 Ubuntu + GNOME 版本，2024 发布） | MindStudio |
| 安装耗时 | 最快机器 35 秒，多数电脑 < 2 分钟 | omarchy.org |

⚠️ **何大人 9-20 信息准确度**：3 个核心数字（110万 / 4万 / 29种语言）全部命中，无误差。

---

## 2. 核心设计哲学 — Omarchy Doctrine

**10 条原则**（omarchy.org/doctrine）的浓缩版：

1. **Oma = omakase**（主厨发办）：替用户选好工具 + 调好细节，而不是丢 1000 个配置项
2. **可塑（malleable）**：默认装好即用，但**任何层都能改**
3. **OS 即 codebase**：配置全是纯文本 + shell 命令 + 标准接口 → Agent 可读可改可验证
4. **Unite the nerds, welcome the agents**：团结极客 + 接纳 Agent
5. ...（其他 6 条未单独抓取，Doctrine 页里有完整版）

**关键金句**：
- *"When you can vibe code whatever app comes to your mind, you should be able to vibe code your operating system."*
- *"There's not this two-tier system where Apple or Windows make the real thing and you try to hack your little thing."*
- 投资人味的话：*"when you've just raised ~$2m in tokens, why the hell not?"*（DHH 自嘲用 200 万美元 tokens 做 29 种语言翻译）

---

## 3. Quattro 4.0 四大新能力（重点）

### 3.1 统一桌面 Shell（Quickshell）

**之前**：waybar（顶栏）+ Walker（启动器）+ Mako（通知）+ hyprlock（锁屏）+ hypridle + swaybg + polkit-gnome + SwayOSD —— **8 个进程碎片化**

**4.0 之后**：**一个 Quickshell 长驻进程 + 插件化主题** —— **Waybar / Walker / Mako / hyprlock / swaybg / polkit-gnome 全部被替换**

**意义**：桌面变成一个**可脚本化、可编程、可被 Agent 整体操控**的统一体——之前 Agent 想"调通知透明度"要改 4 个配置文件，现在改 1 处。

### 3.2 默认 Agent 选型器（First Boot Picker）

首次启动 → 让用户从 9 种 Agent 里选默认（Claude Code / Codex / OpenCode / Pi / Gemini / Grok / Copilot / ...）→ 登录 → 全系统都交给它。

**意义**：把"用什么 Agent"从**用户的技术选型决定**降级成**产品 Onboarding 流程**——Agent 是 OS 的一等公民，不是外部工具。

### 3.3 Crash Watcher + diagnose-crash skill

进程崩溃 → systemd-coredump 抓 dump → 弹通知 → 点一下 → **默认 Agent 自动接管**：
- 读 crash dump
- 诊断根因
- 帮你写 bug report

**意义**：从"被动报错"到"Agent 主动治愈"。

### 3.4 Model-Usage Widget

状态栏放一个 widget，**跨多 Agent 跟踪每周额度**（Claude Code / Codex / Pi / Oh My Pi / OpenCode）

**意义**：用户不必为每个 Agent 单独登录控制台看额度——OS 层做汇总。

---

## 4. 可借鉴的方法论（与现有项目触点）

### 4.1 🎯 强关联：德勤 AI Native MVP

按 MEMORY.md "产品路线"：Hermes Agent v0.14 是德勤项目唯一 Agent 框架；Omarchy **不是替代 Hermes**，但有 3 个具体技术可借鉴：

| Omarchy 做法 | 德勤 MVP 借鉴点 |
|---|---|
| **Onboarding 时选默认 Agent**（9 选 1） | `1-Projects/德勤/AI-Native/executor/` 抽象层应该做"用户首次登录选执行器" UX——**让 Agent 选型变成 onboarding 流程，而不是配置文件** |
| **Quickshell 统一 8 个碎片进程** | 德勤的可插拔执行器抽象层 **不要做"X 替代 Y"的二选一**，而要像 Quickshell 那样"8 个组件统一抽象 + 插件化"——每个 Agent 框架（Hermes / OpenClaw / Codex / Claude Code / OpenCode）都是**可插拔执行器 adapter** |
| **diagnose-crash skill**（Agent 自愈） | 德勤 MVP 的"工作空间自愈"应该学这套：**监控 + 检测异常 + 自动调度 Agent 处理** —— 而不是只靠用户点按钮 |

**架构启示**（呼应 MEMORY.md "工程全景调研边界"）：**Hermes / OpenClaw / Codex / Claude Code / OpenCode 都应被视为可插拔 Agent 执行器** —— 这正是 Omarchy 把碎片化桌面统一到 Quickshell 的同款思维。

### 4.2 中等相关：Wish-Y / 个人 Workspace

Omarchy 的"vibe code your OS"哲学 = Wish-Y 的"vibe code your workspace"——两者都是"让 Agent 跟用户一起改造使用环境"。具体做法：

- **Skills-as-config**：Omarchy 把"做 app / plugin / theme"打包成 skill 给 Agent → Wish-Y 也可以把"配 Notion 模板 / 建日历 / 整理 vault"打包成 skill
- **环境即代码**：Wish-Y 的工作流应该**全可被 Agent 读写**——而不是藏在 GUI 后面

### 4.3 通用借鉴：Agent 框架选型方法论

Omarchy **没有自研 Agent 框架**——直接集成 9 个现成的（Claude/Codex/OpenCode/Pi...）。这印证了 MEMORY.md 7-9 决策：

> **不造轮子，复用现成 Agent 框架 + 在 OS 层做整合层**

德勤 MVP 应该把 80% 工程量放在"整合层"（adapter + 路由 + 可观测），20% 在"自研执行逻辑"——Omarchy 用 Quickshell 整合了 8 个碎片，**这种"整合层工程师"**正是德勤 AI Native MVP 需要的核心能力。

---

## 5. 不太相关的部分（不挂钩）

- **Wayland / Hyprland / 桌面主题美学** —— 跟 AI Agent 无关，纯审美
- **2 分钟装机速度** —— 是 DX 优化，不是 AI Native 核心
- **Omakub / Ubuntu 兄弟版** —— 同思路 Arch 版本，不必分别研究
- **"$2m tokens 做 29 语言翻译"** —— DHH 自嘲梗，工程意义不大

---

## 6. 风险与质疑（来自社区）

Reddit / r/hyprland 评价：

- ✅ 正面：很多人用 Mac 的公司同事开始考虑 Linux
- ⚠️ 负面：**bloat 跟 Windows 差不多**；installer 不让用户逐项选包
- ⚠️ 负面：Arch 滚动更新 + AI 自动化 = 出问题更复杂（"vibe code your OS"翻车时无人兜底）

**对德勤 MVP 的启示**：**别把 Agent 自动化推到"无人兜底"层**——重要操作必须有"diff 预览 + 一键回滚"——Omarchy 的脚本化可改 ≠ 不可逆。

---

## 7. 信息源

| 来源 | URL |
|---|---|
| 官网首页 | https://omarchy.org |
| 官网 momentum 数据页 | https://omarchy.us |
| DHH 29 语言改版新闻 | https://omarchy.org/news/2026/09/omarchy-org-redesign-launches-with-29-languages |
| MindStudio 评测 | https://www.mindstudio.ai/blog/what-is-omarchy-linux |
| daily.dev Quattro 4.0 解读 | https://daily.dev/posts/omarchy-4-0-adds-ai-agent-tooling-and-a-better-screenshot-annotator-uqdsjkgpr |
| DHH 采访（Linux 是不是完美 OS） | https://www.youtube.com/watch?v=_CuibYl_Fh0 |
| Reddit 评测（含批评） | https://www.reddit.com/r/hyprland/comments/1mo8rlw/omarchy_review_the_good_the_bad_and_the_hell_no |

---

## 8. 个人备忘

- **DHH 公开承认** AI 还不如"大多数初级程序员"，但他"mostly codes by hand"的同时，把 Omarchy 做成 Agent-Native OS——这种**"我自己不一定全用，但我要把工具做出来"的工程哲学**值得学
- **Omarchy 跟 LangGraph / Paperclip / OpenSquilla / Multica 是完全不同物种**：那些是"Agent 框架"，Omarchy 是"Agent 的运行环境"——层次更高一级
- 如果德勤面试被问"你怎么理解 AI Native"——**Omarchy 是当下最好的对标案例**：不要回答"我们做了个 Agent"，而要回答"**我们把整个工作空间做成 Agent 可读可改可验证的 codebase**"

---

## 9. 下一步行动（建议）

1. ⚠️ **本调研不立即触发德勤 MVP 改动** —— 仅作为"执行器抽象层 / Agent Onboarding UX"两个点的**方法论参考**
2. 📅 **等 Hermes v0.14 dispatcher 跑稳**（参考 MEMORY.md "Hermes 实际验证"）后，再回头看 Quattro 4.0 的"统一 Shell"模式能不能借鉴到 Hermes-based 德勤 MVP
3. 🔍 **不深挖**：Omakub（Ubuntu 版本）、Hyprland 配置语法、Quickshell 插件机制 —— 优先级低
