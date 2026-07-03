# kepano/obsidian-skills 差距分析

> 2026-07-03 何大人要求按 kepano CEO 出手这篇文章的思路反向研究 + 设计 vault skill 整理方案。
> 本文档为「决策参考」，配套的 `scaffold/` 子目录是可立即发布 GitHub 的项目骨架。

## ⚡ TL;DR

**kepano 的 obsidian-skills = 30+ AI skill 的规范集，按 Agent Skills spec 打包，1 行安装。**

您已经有 **71 个 skill** 散落在 `~/.openclaw/workspace/skills/`，**3 个差距**：
1. **schema 不一致**（仅 10/71 有合规 SKILL.md frontmatter）
2. **references 没拆解**（每个 skill 一坨长文档，浪费 token）
3. **没法一行安装**（只能靠软链手动同步）

**推荐动作**：把精选 30+ skill 整理成 `hesiyan/agent-skills` 仓库（合规化 + 拆 references + 加 marketplace.json），作为德勤 MVP / 求职「AI Native Workspace」的对外 demo。

---

## 1. kepano obsidian-skills 速览

```
kepano/obsidian-skills/             (MIT, Steph Ango = Obsidian CEO 亲自做)
├── .claude-plugin/
│   ├── plugin.json                 
│   └── marketplace.json            # 列出 plugin，npx 一行装
├── LICENSE                         # MIT
├── README.md
└── skills/                         # 5 个核心 skill
    ├── defuddle/SKILL.md
    ├── obsidian-bases/SKILL.md + references/
    ├── obsidian-cli/SKILL.md
    ├── obsidian-markdown/SKILL.md + references/{CALLOUTS,EMBEDS,PROPERTIES}.md
    └── json-canvas/SKILL.md + references/EXAMPLES.md
```

**SKILL.md 模板**（强制）：

```yaml
---
name: skill-name
description: |
  一句话描述能力 + "Use when ..." 触发场景。
---

# Skill 标题

主入口（教程 + 关键片段）。
详细文档放 references/ 子目录。
```

**5 大 skill**：

| skill | 作用 |
|---|---|
| obsidian-markdown | Obsidian Flavored Markdown 规范（wikilinks、embeds、callouts、properties）|
| obsidian-bases | Obsidian Bases 数据库视图（filter / formula / summary）|
| json-canvas | JSON Canvas 画布 |
| obsidian-cli | Obsidian CLI 操作 vault |
| defuddle | Web 页面 → 干净 Markdown |

**安装**：一行 `npx skills add https://github.com/kepano/obsidian-skills`。

---

## 2. 您 71 个 skill 现状

| 项 | kepano | 您 OpenClaw |
|---|---|---|
| 总 skill 数 | 5（精）| **71 个**（散）|
| 统一 schema | ✅ Agent Skills spec | ❌ 大多数无 frontmatter |
| SKILL.md | ✅ 100% 合规 | ⚠️ ~10/71 合规 |
| references/ 拆解 | ✅ 主+辅分离 | ❌ 长文档堆叠 |
| 一键安装 | ✅ | ❌ 软链手动 |
| 触发条件 | ✅ description 内 | ⚠️ 散落 |

**71 skill 分组**：

- AI 应用类（5）
- PPT / 内容创作（~12）
- 研发（~15）
- 工具 / 集成（~15）
- 流程 / 反思（~10）
- 搜索 / 调研（~5）
- 设计 / UX（~10）

---

## 3. 三阶段发布路线

**v0.1 — 骨架 + 5 个示范 skill（1 天）**
- 选 5 个核心 skill（context-recovery / wechat-article-to-obsidian / stock-recap / daily-stock-review / ai-native-product-requirement）
- 规范化 frontmatter + 拆 references/
- 写 plugin.json + marketplace.json + README + install.sh

**v0.5 — 10-15 skill + 校验脚本（3 天）**
- 用 validate-skill.py 批量扫 71 skill
- 合规的全部纳入；不规范的修后纳入
- 加 docs/ + examples/demo-vault/

**v1.0 — 30+ skill（1 周）**
- 接 OpenClaw 的 hermes chat / daemon
- 写 `pitch.md` 用于德勤 + 求职面试
- v0.1 先发私有仓库（公司 GitHub），v1.0 看情况发公网

---

## 4. 5 个核心 skill 规范化示例

（详见 `scaffold/` 子目录）

| skill | 触发条件 |
|---|---|
| `context-recovery` | "Use when 新会话启动 / 跨天 / 需要昨日工作上下文" |
| `wechat-article-to-obsidian` | "Use when 用户分享 mp.weixin.qq.com 链接，或提到"微信文章、公众号、保存微信"" |
| `stock-recap` | "Use when A 股复盘 / 持仓 K 线 / 推荐跟踪 / cron 15:30 跑" |
| `daily-stock-review` | "Use when 每日盘中 / 收盘后 / 生成复盘文档" |
| `ai-native-product-requirement` | "Use when 做 AI Native 产品需求 / 写 R&D 文档 / 评估 AI 落地" |

---

## 5. 决策点（请您回复）

| # | 决策 | 选项 |
|---|---|---|
| 1 | 项目名 | `hesiyan/agent-skills`（推荐）|
| 2 | 首批发布范围 | v0.1（5 skill） vs v0.5（15 skill） vs v1.0（30 skill）|
| 3 | 仓库可见性 | 私有（组织 GitHub） vs 公开（GitHub 公网）|
| 4 | 与 workspace 同步 | 单向（仓库 = workspace 导出版）vs 双向（互相同步）vs 仓库独立维护 |
| 5 | 与德勤 MVP 集成 | M9 Skill/MCP 模块拿此做 reference 实现 |

详见 `gap-analysis.md` 原文（`kepano-obsidian-skills/gap-analysis.md`）。
