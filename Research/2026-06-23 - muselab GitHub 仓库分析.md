---
type: github-repo-analysis
repo: hesorchen/muselab
url: https://github.com/hesorchen/muselab
stars: 26
license: MIT
language: Python (backend) + Vanilla HTML/Alpine.js (frontend)
analyzed_date: 2026-06-23
tags: [claude-agent-sdk, ai-assistant, self-hosted, pwa, personal-knowledge-base, harness, deepseek, minimax, muse]
---

# muselab — 自托管 AI 个人工作台（GitHub 仓库分析）

> 来源：[hesorchen/muselab](https://github.com/hesorchen/muselab) · 26 stars · MIT · v1.1.0
> 作者：hesorchen（hesorchen@gmail.com）
> 与 OpenClaw 的设计哲学高度对齐，是**目前最值得对标的同类项目**

## 一、项目定位（一句话）

**muselab 是你的"档案 + Muse（真正懂你的 AI）"**——基于 Claude Agent SDK 的自托管 AI 个人工作台。

- 自托管 / 无 npm / 无打包 / 无构建步骤（**这条非常戳**）
- 一行命令安装：`curl -fsSL ... | bash`
- 浏览器打开 `http://localhost:8765`，粘贴 token 登录
- 8 家模型一键切换：Claude / DeepSeek / GLM / **MiniMax** / Kimi / Qwen / MiMo / ERNIE

## 二、与 OpenClaw 的对比

| 维度 | **muselab** | **OpenClaw** |
|---|---|---|
| 形态 | Web 应用（FastAPI + Alpine.js）| Agent Harness（CLI + 技能系统）|
| 受众 | 终端用户开箱即用 | 开发者 / 高级用户底座 |
| Agent 引擎 | Claude Agent SDK（直接依赖）| 独立实现（ReAct + 工具调度）|
| 模型 | 8 家厂商可切换 | 多 provider 抽象 |
| 用户档案 | 一个目录（`MUSELAB_ROOT`）+ 根 `CLAUDE.md` 自动加载 | MEMORY.md + memory/ + context-recovery 三层 |
| 技能 | 11 个内置 skill + 自动发现 `~/.claude/skills/` | 67+ skill 跨端统一存储 |
| 移动端 | **PWA 同步会话** | 主要桌面端 |
| 定时任务 | ✅（asyncio cron loop）| ✅（cron 任务）|
| Web Push | ✅（VAPID 签名）| ❌ |
| 文档规模 | 40k LOC（前后端）| 工具 67 + skills 多 |
| Constitution 治理 | ✅（RFC 2119 风格 12 原则 + 架构不变量）| ❌（散落在 MEMORY.md）|
| 双根设计 | ✅ repo + archive 永久分离 | ❌（混合）|
| 文档完备度 | **极高**（50+ 文档 / 中英双语）| 中等 |

## 三、muselab 的六大设计原则（Constitution P1–P6）

> 摘自 `constitution.md`——muselab 用 **RFC 2119 风格** 的宪法来治理项目，是 OpenClaw 缺失的工程化实践。

### P1 — 可读胜于巧妙，小胜于功能全
> muselab is intentionally small so the whole codebase stays human-readable.

### P2 — Clone-and-run：永远不要构建步骤
- 前端**没有** bundler / transpiler / npm install
- Alpine.js v3 + 现代浏览器原生支持
- 第三方库都 vendor 在 `frontend/vendor/`（带许可证登记）

### P3 — SDK over raw API
> 永不用 Messages API 直连，必须走 **Claude Agent SDK**（与 Claude Code 同一引擎）。
> 统一获得 MCP / Skills / Subagents / plan mode / CLAUDE.md 自动加载。

### P4 — 归档属于用户，代码仓库永不碰它
**两个根永久分离**：
- `repo`（muselab/）= 代码 + 每实例状态
- `archive`（MUSELAB_ROOT）= 用户的私人文件（独立备份，互不干扰）

### P5 — 整文件即输入单位
**不用 RAG 切块**——按需 Read / Grep / Edit 完整读文件，零语义损耗。
对比 AnythingLLM 的 RAG 路线：muselab 明确选择"全文件直接读取"。

### P6 — 个人信息在发布物中是"放射性的"
开源仓库，**禁止真实个人数据**出现在代码/文档/提交/测试/示例中。
测试必须用临时归档目录跑。

## 四、架构不变量（A1–A6）

| ID | 不变量 | 启发 |
|---|---|---|
| A1 | 两个根永久分离 | OpenClaw 应该明确 `~/.openclaw/workspace` vs 用户数据 |
| A2 | 分层 backend，一模块一 router | 我们的 `backend/*.py` 可以学 |
| A3 | **每会话 env 隔离 + 隔离的 CLAUDE_CONFIG_DIR** | 关键安全点：阻止第三方模型走 Pro OAuth 计费 |
| A4 | 客户端池键 = `(session_id, model, effort)`，LRU 3 | 池键设计很聪明 |
| A5 | **一个会话锁一个模型** | 跨厂商 thinking-block 签名不互通 |
| A6 | MCP 默认零、按属性 gate | 默认安全 |

## 五、核心技术细节（值得借鉴）

### 1. 会话锁定单模型（A5）
```python
# session 第一次真实 turn 时 pin model
session.model = request.model
# 后续 turn 必须复用这个 model
# 跨厂商 thinking 签名不互通，混用会 400
```

### 2. Per-request env 注入（A3）
```python
ANTHROPIC_BASE_URL = vendor_endpoint  # DeepSeek / GLM / MiniMax
ANTHROPIC_API_KEY = vendor_key
CLAUDE_CONFIG_DIR = isolated_dir  # 关键！阻止 CLI 走 Pro OAuth
```
**这是 muselab 集成 8 家模型的核心技巧**——和 OpenClaw 的多 provider 抽象可对照。

### 3. SDK 客户端池（A4）
- 键 `(session_id, model, effort)`，LRU 容量 3
- 每个 assistant 消息**自带 model 字段**，刷新后徽章仍正确
- MCP spawning 与池容量有交互——改池键是架构变更

### 4. SSE Turn Loop（`/api/chat/stream`）
- 浏览器用 EventSource（无法设 header）→ token 走 `?token=`
- `TurnBroadcast` 保证浏览器断连不杀掉回复——重连时 replay 缓冲
- Web Push 在长时间任务完成后通知，**标签页关闭也能收到**

### 5. 安全日志
```python
# backend/main.py — TokenFilter
# 修复了一个真实 bug：之前 scrub 整条 msg 后把 args=() 清空，
# 导致 uvicorn AccessFormatter 5-tuple unpack 失败 → journald 报错
# 正确做法：只替换 args[2] 里的 token，保留 5-tuple 形状
```

### 6. 11 个内置 Skill
| Skill | 触发 | 用途 |
|---|---|---|
| web-search | 问时效事实 | 多源 + 日期引用 |
| markdown-formatter | 清理 MD | 标题/列表/全角标点统一 |
| mermaid-helper | 画图 | 选类型 + 校验语法 |
| code-reviewer | 代码审查 | bug→安全→性能→可维护性 |
| citation-formatter | 学术引用 | APA/IEEE/GB/T 7714/BibTeX |
| task-decomposer | 模糊目标 | DoD + 估时 + 临界路径 |
| summary-distiller | 长文摘要 | TL;DR / 关键点 / 行动项 |
| **pptx** | 生成 PPT | python-pptx |
| csv-analyzer | CSV 分析 | pandas + 条件图表 |
| translate | 中英互译 | 三段式：直译→识别→润色 |
| meeting-notes | 会议纪要 | 决议/行动项/待办 |

### 7. Skills 发现机制
```python
ClaudeAgentOptions(
    setting_sources=["user", "project", "local"],
    cwd=str(ROOT),  # archive 根
    skills="all"
)
```
- `user` → `~/.claude/`（与 Claude Code CLI 共享）
- `project` → 当前 cwd（即 archive）
- `local` → cwd 内的 `.claude/`

**这个发现顺序对我们设计 skill 加载策略有借鉴**。

## 六、依赖管理哲学（pyproject.toml）

muselab 在依赖版本上限上**有意写得保守**，注释非常说明问题：

```toml
# Upper bound is a DELIBERATE guard, not pessimism:
# muselab is an adapter over the SDK and hand-maintains assumptions
# the SDK doesn't expose as a programmatic contract — the harness-tool
# denylist and the CLI JSONL transcript format.
# An unbounded `>=` lets any minor bump silently expose a new tool or
# break JSONL parsing with zero signal. <0.3 makes SDK upgrades explicit.
"claude-agent-sdk>=0.2.106,<0.3",
```

**翻译**：muselab 是 SDK 之上的适配器，对 SDK 的内部行为有手维护的假设（denylist / JSONL 格式），所以必须 pin 上限，让升级成为显式动作。

**这条哲学 OpenClaw 应该学**——很多 SDK 我们也吃版本。

## 七、可借鉴 OpenClaw 的 7 个点

| # | 借鉴点 | OpenClaw 现状 | 行动建议 |
|---|---|---|---|
| 1 | **Constitution 治理** | 散落在 MEMORY.md | 写 `HARNESS_CONSTITUTION.md`，RFC 2119 风格 |
| 2 | **P2: Clone-and-run / 无构建** | 部分（前端无）| backend 安装脚本再简化 |
| 3 | **P5: 整文件输入，不 RAG** | 已经遵循 | 文档化（写进 Constitution）|
| 4 | **A1: 双根分离** | 混合（workspace 既装代码又装 vault 引用）| 明确 `~/.openclaw/` vs vault |
| 5 | **A3+A5: 会话级 env 隔离 + 锁模型** | 多 provider 但未严格隔离 | 加 session → model 锁定 |
| 6 | **Web Push 通知** | ❌ | 长任务（cron / 分析）完成后推送 |
| 7 | **移动 PWA** | ❌ | 跟 muselab 一样做 PWA 镜像 |

## 八、可观察的 4 个细节（小心机）

1. **`_TokenFilter`** —— 日志过滤 token，但保留 uvicorn AccessFormatter 的 5-tuple args 形状（修复了一个真实的 journald bug）
2. **`_BG_TASKS: set`** —— 强引用长生命周期后台任务，避免事件循环 GC 掉
3. **`_ASSET_VERSION_CANDIDATES`** —— 多个文件 hash 出一个资产版本号，强制客户端刷新
4. **Clio 的"Stacked horizontal bars (scroll layers)"图标** —— 九位缪斯每位一个几何图形，简洁且能区分

## 九、参考链接

- 主页：https://github.com/hesorchen/muselab
- 中文 README：https://github.com/hesorchen/muselab/blob/main/README_zh.md
- Constitution：https://github.com/hesorchen/muselab/blob/main/constitution.md
- Architecture：https://github.com/hesorchen/muselab/blob/main/docs/architecture.md
- Comparison：https://github.com/hesorchen/muselab/blob/main/docs/comparison.md
- Promo 页：https://hesorchen.github.io/muselab/promo/
- DeepWiki：https://deepwiki.com/hesorchen/muselab

## 十、Meta 学习

- **同类项目命名学**：muselab（小写）= muse + lab；Muse 来自希腊神话；OpenClaw = Open + Claw（小助的爪子）
- **作者 hesorchen 是个人开发者**，但产出了 Constitution / 双根 / SDK 适配 / PWA / 多模型 / 安全日志 / Web Push 的完整工程化产品——值得跟进
- **MiniMax 出现在 muselab 的 8 家支持列表里**——意味着 MiniMax 已经在 LLM agent 生态有开发者背书