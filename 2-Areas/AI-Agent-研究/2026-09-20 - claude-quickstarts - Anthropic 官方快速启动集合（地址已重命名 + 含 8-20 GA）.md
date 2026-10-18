# claude-quickstarts — Anthropic 官方快速启动集合调研

> **整理时间**：2026-09-20 23:02
> **信息来源**：何大人 23:02 微信视频口述 + 官方仓库（已跳转核实）+ Anthropic 2026-08-20 GA 公告
> **核实状态**：⚠️ **仓库地址已重命名** —— 何大人记的 `anthropic-quickstarts` 已迁移到 `claude-quickstarts`
> **PARA 类别**：2-Areas / AI-Agent-研究

---

## 0. 一句话定义

> Anthropic 官方维护的 **15+ 个可直接 fork + 部署的 Claude Agent 参考实现集合** —— 从"客服 / 金融分析 / 计算机操作 / 浏览器自动化"到"Managed Agents 全家桶（Slack / Linear / Sentry / CopilotKit / Road Trip Planner / Knowledge Wiki / MCP Server）"。
>
> 这是 **Anthropic 对"AI Agent 应该长什么样"的官方答案**——对德勤 MVP 有直接工程参考价值。

---

## 1. ⚠️ 仓库地址核实（重要纠正）

| 项目 | 值 |
|---|---|
| 何大人口述地址 | `github.com/anthropics/anthropic-quickstarts` |
| **实际仓库地址（2026-09 当前）** | **`github.com/anthropics/claude-quickstarts`** ⚠️ 已重命名 |
| Docker 包名（仍存在） | `ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-...` |
| License | **MIT** |
| 用途 | "A collection of projects designed to help developers quickly get started with building deployable applications using the Claude API" |

**事实**：访问 `github.com/anthropics/anthropic-quickstarts` 会**自动 301 重定向**到 `claude-quickstarts`。Docker 镜像还保留旧名字，但代码仓库已统一到 `claude-quickstarts`。

> **给何大人的反馈**：您视频里记的是老地址，现在 GitHub 已统一为 `claude-quickstarts`。

---

## 2. 完整 quickstart 清单（15+ 个，何大人只提到 3 个）

按类型分组：

### 2.1 经典业务场景（何大人提到的 3 个）

| Quickstart | 核心能力 | 备注 |
|---|---|---|
| **Customer Support Agent** | Claude 客服 Agent + 知识库访问 | 自然语言理解 + 生成 |
| **Financial Data Analyst** | Claude 金融数据分析 + 交互式可视化 | chat-driven 数据分析 |
| **Computer Use Demo** | Claude 控制桌面（点击 / 输入 / 截图） | 17 个 member tools，**`computer_toolset_20260801`** |

### 2.2 Computer Use 进阶（4 个）

| Quickstart | 核心能力 |
|---|---|
| **Computer Use Best Practices** | macOS 原生 computer-use 参考实现（VM 内运行）：显式 tool 定义 / 图像尺寸剪裁 / prompt caching / 服务端压缩 / 批量 tool 调用 / 沙箱 shell / 轨迹记录 |
| **Browser Use Demo** | 浏览器自动化：导航 / DOM 检查 / 内容提取 / 表单填写（基于 Playwright） |
| **Autonomous Coding** | Claude Agent SDK 的两阶段自主编码 agent（initializer + coding agent），多 session 通过 git 持久化进度，按 feature list 增量交付 |
| **Agents**（顶层目录） | 通用 agent 示例 |

### 2.3 Managed Agents 全家桶（9 个 ⭐ 重点）

这是 **Anthropic 的"Agent-as-a-Service"标准实现**——一个会话持久的 Claude Managed Agent + 各种前端/集成：

| Quickstart | 集成场景 |
|---|---|
| **Managed Agents Chat SDK** | Vercel Chat SDK 前端 + 持久 session + token 流式 + tool 调用实时显示。**同一 handler 可接 Slack / Teams / Discord / Telegram / WhatsApp**（换 Chat SDK adapter 即可） |
| **Managed Agents CopilotKit** | CopilotKit 渲染 + AG-UI 协议 + token 流 + 事件 delta + 交互式 generative UI |
| **Managed Agents Knowledge Wiki** | M&A 数据室 wiki（基于 SEC EDGAR 公开文件）：并行 extract + resolve pass + steered consolidation + provenance + token 复用 |
| **Managed Agents Linear** | Linear Agent Platform 集成：webhook → session → 注释回复（OAuth actor=app） |
| **Managed Agents MCP Server (TypeScript)** | **9 个 tools** 把 Managed Agents Sessions API 暴露给 Claude Desktop / Claude Code / claude.ai；`wait_for_idle` 把事件流变 request/response；agent allowlist |
| **Managed Agents Road Trip Planner** | Next.js 直接基于 session（无 chat 框架、无 DB）：token 流 + 凭证注入 + 模型覆盖 + 多 agent 协调（draft → reviewer session thread） |
| **Managed Agents Sentry** | **cron 调度的无 host process agent**：环境变量凭证注入（egress proxy 替换 token） |
| **Managed Agents Slack** | Slack bot @mention → webhook → session → 回复（同 Linear 模式） |

---

## 3. 配套重大新闻：Anthropic 2026-08-20 GA（1 个月前）

| 模块 | 状态 | 关键变化 |
|---|---|---|
| **Computer Use** | GA | 从 preview 毕业，**每轮可发多个 tool calls**（不再 round-trip-by-action）。新版本 `computer_toolset_20260801`：`tools` 里 1 个 entry → 17 个 member tools（`screenshot` / `left_click` / `type` / `zoom` 等） |
| **Browser Tool** | GA | 浏览器自动化官方 tool（Browser Use Demo 升级） |
| **Skills API** | GA | **可复用 / 可版本化的 skills**——这是关键，从"demo 级 prompt"升级到"生产级可复用资产" |
| **Files API** | GA | 文件管理 |
| 数据保留 | 客户端 | 截图 / 鼠标 / 键盘 / 文件**全部存用户环境**，不存 Anthropic |

**Anthropic 官方数据**：computer use GA 后，**每任务 round trips 减少 20-40%**。

**含义**：从"实验性"→"生产可用"的标志——Anthropic 在为 Agent 标准化铺路。

---

## 4. 工程参考价值（对德勤 MVP）

按 MEMORY.md 7-8 准则：

### 4.1 🎯 强关联：可直接 fork 改写的 5 个

| Quickstart | 德勤 MVP 借鉴 |
|---|---|
| **Autonomous Coding** | ⚡ **直接借鉴** —— 德勤 MVP 的核心是 Agent 开发工作空间，这个就是 Anthropic 官方"两阶段 coding agent"参考实现 |
| **Managed Agents Chat SDK** | ⚡ **直接借鉴** —— 德勤客户交付需要**同一 Agent 后端接多个渠道**（Slack / Teams / 邮件 / 内部 IM），这是官方参考架构 |
| **Managed Agents MCP Server** | ⚡ **直接借鉴** —— 德勤 MVP 要让 **Hermes / OpenClaw / Codex / Claude Code 都能驱动**同一 Managed Agent（呼应 MEMORY.md 6-29 决策的"可插拔执行器"） |
| **Computer Use Best Practices** | ⚡ **直接借鉴** —— prompt caching / 服务端压缩 / 批量 tool 调用 / 沙箱 shell / 轨迹记录 = 5 个生产级最佳实践 |
| **Managed Agents Sentry** | 🔄 间接借鉴 —— cron 调度 + 无 host process + 凭证注入 = 德勤 MVP 给客户部署的"零运维 Agent"模式 |

### 4.2 ⚠️ 警示：Anthropic 已经在标准化 Agent

**事实判断**：**Anthropic 通过 claude-quickstarts + Skills API + Files API 已经把"AI Agent 应该长什么样"标准化了**。

**对德勤 MVP 的战略含义**（呼应 MEMORY.md 6-29 决策）：
- ✅ **应该**：在 Claude / Anthropic Managed Agents **之上**建德勤行业 know-how 层
- ❌ **不应该**：从零造 Agent 框架跟 Anthropic 竞争（必败，呼应今日 Jev vs Laya 的"闭源被开源撕碎"教训）
- ✅ **业务壁垒**：行业知识 / 客户数据 / 合规能力 > 自研 Agent 算法

### 4.3 跟今日其他内容的交叉

| 今日内容 | 与 claude-quickstarts 关联 |
|---|---|
| **Omarchy（DHH Agent-Native Linux）** | Computer Use Demo + Best Practices = "Agent 操作整台电脑"的**官方参考实现**——Omarchy 是"系统层让 Agent 可读可改"，claude-quickstarts 是"官方怎么做 Computer Use Agent" |
| **Jev vs Laya（朋友圈截图）** | ⚠️ **反面教材**：3 年闭门造 Agent 框架被 3 天开源撕碎 → 德勤 MVP **不能走 Jev 老路**（自研核心算法）→ 必须走 **"整合层 + 行业 know-how"** 路线 |
| **SAM 3.1（微信公众号文章）** | 弱关联：SAM 是"专门模型分工"代表；Managed Agents 系列里的 **Road Trip Planner** 也演示了 "**multi-agent 协调（draft → reviewer session thread）**" = 同款分工范式 |

---

## 5. 部署细节（快速参考）

每个子目录都有独立 README + setup 步骤。通用流程：

```bash
# 1. Clone
git clone https://github.com/anthropics/claude-quickstarts.git
cd claude-quickstarts/<subdir>

# 2. 装依赖（每个子目录不同，README 列出）
# pip / npm / pnpm

# 3. 设 API key
export ANTHROPIC_API_KEY="sk-ant-..."

# 4. Run
# python app.py / npm run dev / etc.
```

**Docker 路径**（Computer Use Demo 有官方镜像）：
```bash
docker pull ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest
```

> ⚠️ **小坑**：Docker 镜像名保留旧名 `anthropic-quickstarts`，但代码仓库已统一为 `claude-quickstarts`——文档查找时两个名字都要认。

---

## 6. 信息源

| 来源 | URL |
|---|---|
| 官方仓库（**当前地址**） | https://github.com/anthropics/claude-quickstarts |
| 旧地址（自动 301） | https://github.com/anthropics/anthropic-quickstarts |
| Computer Use 官方文档 | https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool |
| GA 发布新闻（2026-08-20） | https://aiinsiders.net/article/anthropic-ships-computer-use-browser-tool-skills-api-to-ga |
| Docker 镜像（保留旧名） | https://github.com/anthropics/anthropic-quickstarts/pkgs/container/anthropic-quickstarts |

---

## 7. 个人备忘

- **"Fast Start File"** 这个名字我搜不到准确出处——可能是视频里给的口语化名字，**Anthropic 官方叫 "Claude Quickstarts"** 或 "Claude FastStart Guide" 之类的。**建议何大人下次视频里可以提"claude-quickstarts 仓库"**，避免和"Anthropic 官方其他文件"混淆
- **Anthropic 的策略很清晰**：把 Agent 标准化（computer use / browser tool / Skills API / Files API全 GA + 15+ quickstart）—— 任何"自研 Agent 框架"在这个生态下都难有壁垒
- **德勤 MVP 的"反脆弱设计"**：把工程量 80% 放在"行业 know-how / 合规 / 客户数据整合"，20% 放在"差异化 Agent 编排"——绝不要在"自研 Agent 框架"上花 80% 精力
- **直接借鉴清单**（下次德勤 MVP 进入实施阶段）：Autonomous Coding + Managed Agents Chat SDK + Managed Agents MCP Server + Computer Use Best Practices + Managed Agents Sentry
- **今日 git push 失败根因**（已修复）：`.git/config` 里 `[url "...insteadOf = https://github.com/"]` 段写的是**旧失效 token**（2026-08-04 确认失效的那个），强制重写所有 GitHub URL 用旧 token。修复方式：把该段 token 替换成当前真 token（`github_pat_11A7KZNRA0vavQDrmVzhAz_...`）。修复后 push / fetch 都恢复正常，cron `vault-sync.sh` 也能跑了

---

## 8. 下一步行动（建议）

1. ⚠️ **本调研不立即触发德勤 MVP 改动**——仅作为"工程参考清单"留档
2. 📅 **等德勤 MVP 进入"执行器抽象层"实施阶段**——回头看 Autonomous Coding + Managed Agents MCP Server 是否可以直接 fork
3. 🔍 **不深挖**：每个具体 quickstart 的源码——优先级低，等要用时再读
4. 📌 **建议何大人把今日三个内容串成一份"AI Agent 当下形态速览"**：Omarchy（OS 层）+ claude-quickstarts（应用层）+ Jev vs Laya（生态层反思）= 一个完整的"AI Agent 工程全景图"
