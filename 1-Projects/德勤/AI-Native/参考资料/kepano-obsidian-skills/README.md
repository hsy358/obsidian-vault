# hesiyan/agent-skills （scaffold）

> AI Agent Skills 集合 —— 让 Claude Code / Codex / OpenCode 等 CLI Agent 更懂 Obsidian / vault / 知识管理。

> **状态**：scaffold 阶段（2026-07-03 起草），等何大人定决策点后再正式 git init。

---

## 这是什么

按 [Agent Skills specification](https://agentskills.io/specification) 打包的 skill 集合，**一行安装**到任意 skills-compatible Agent（Claude Code / Codex / OpenCode / Gemini CLI 等）。

对标 **kepano/obsidian-skills**（由 Obsidian CEO 维护），但侧重：
- **AI Native 工作流**（知识管理 / 内容创作 / 研发 / 流程 4 大领域）
- **中文场景**（公众号文章抓取、企业 IM、私有 vault 等）
- **可观测性**（推荐跟踪、复盘、K 线日报等含审计的 skill）

## 用户群

- 用 Obsidian / vault 做知识管理 + AI 工作流的开发者
- 在公司场景下用 Claude Code / Codex 做日常工作的 agent 用户
- 想给自己的 vault 接入 30+ 高质量 skill 的项目经理 / 顾问

## 路线图

- v0.1: 5 个示范 skill + scaffold（已完成，draft 状态）
- v0.5: 15 skill 批量规范化 + 校验脚本
- v1.0: 30+ skill + OpenClaw / Hermes 集成 + 中文 README

## 安装（待实施）

```bash
# 公共仓库
npx skills add hesiyan/agent-skills

# 或私有仓库
npx skills add git@github.com:hesiyan/agent-skills.git
```

装完自动发现到 `~/.claude/skills/`、`~/.codex/skills/`、`~/.opencode/skills/`。

## 项目结构

```
hesiyan/agent-skills/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── LICENSE                             # MIT
├── README.md
├── CONTRIBUTING.md
├── install.sh                          # 一键 link 到 ~/.claude/skills 等
├── scripts/
│   ├── validate-skill.py               # 扫所有 skills/*/SKILL.md，校验 frontmatter
│   └── build-manifest.py               # 生成 skill-manifest.yml
├── skills/                             # 30+ skill，每个 SKILL.md 规范
│   ├── context-recovery/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── wechat-article-to-obsidian/
│   ├── stock-recap/
│   ├── daily-stock-review/
│   ├── ai-native-product-requirement/
│   └── ...
├── docs/
│   ├── how-it-works.md
│   ├── adding-a-skill.md
│   └── migration-from-workspace.md      # 从 OpenClaw 私有仓迁移指南
└── examples/
    └── demo-vault/                     # 示例 vault（PARA 结构 + skill 触发样例）
```

## 许可

MIT License
