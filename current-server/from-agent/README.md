---
title: "agent 在新服务器上处理的内容（独立收件处）"
date: 2026-07-18
type: agent-receipt
status: active
purpose: 物理隔离 agent 在 101.33.212.119（新服务器）上处理的内容，避免 git push 冲突
related:
  - /root/vault/current-server/README.md
  - /root/vault/current-server/2026-07-05_md_反思-记忆污染.md
---

# 🤖 agent 在新服务器上处理的内容（独立收件处）

> **本目录专门存放 agent 在 101.33.212.119（新服务器）上处理的文档。**
> 区别于"之前的服务器"（101.35.52.96，已废弃）已经推送到 GitHub master 的内容。

---

## 🎯 为什么有这个目录

来自 `/root/vault/current-server/README.md`（2026-07-05 建立）的规则：

> **新服务器（101.33.212.119）vault 跟远端历史分叉**（commit chain 不同），push 时会冲突。
> **解决**：把新服务器产出的内容放在 `current-server/` 子目录，**物理隔离**。

`from-agent/` 是 `current-server/` 下的一个子目录，**专门收 agent 在这台机器上处理的文档**（公众号文章、链接、用户主动转发的内容等）。

---

## 📋 归档规则（硬规则）

### ✅ 放这里

| 内容类型 | 例子 |
|---|---|
| agent 抓取的微信公众号文章（正文 + 元信息）| Multica 系列（2026-07-18）|
| agent 处理的用户转发的链接 | 何大人 9:47 转发的两篇 Multica 链接 |
| agent 抓取的网页（技术报告、GitHub README、博客等）| OpenAI/Anthropic/Changelog 抓取 |
| agent 处理的用户上传文件（除 Inbox 默认流程外）| 临时分析报告 |

### ❌ 不放这里（按 PARA 主目录归档）

| 内容类型 | 应该放 |
|---|---|
| 通用 AI 知识（跟德勤 / 当前服务器无关）| 旧规则 `2-Areas/公众号文章/`（**已废弃**，改为 `current-server/from-agent/`）|
| 德勤项目笔记 / 报告 | `1-Projects/德勤/` |
| 部署手册（每个项目独立）| `current-server/<项目名>/README.md` |
| 服务器故障事件 | `current-server/incidents/`（待建）|
| 服务器决策记录 | `current-server/decisions/`（待建）|
| 服务器独有知识沉淀 | `current-server/knowledge-base/`（待建）|

---

## 📁 命名规范

```
current-server/from-agent/
└── YYYY-MM-DD/                       ← 处理日期（不是公众号发布日期）
    ├── YYYY-MM-DD - <类型>-<标题>.md ← 文档
    └── ...
```

### 文件名格式（强制）
```
YYYY-MM-DD - <类型>-<标题>.md
```

类型示例：
- `公众号-<标题>` —— 微信公众号文章
- `网页-<标题>` —— 普通网页抓取
- `笔记-<主题>` —— agent 整理的笔记

---

## 🚦 处理 SOP

### 收到何大人转发的链接（默认动作）
1. **不**直接抓全文 + 归档（避免误判）
2. **先**用 web_fetch 试拿元信息（标题 / 作者 / 发布时间）
3. 元信息写进 `current-server/from-agent/YYYY-MM-DD/YYYY-MM-DD - <类型>-<标题>.md`（frontmatter 完整 + 状态标 `待抓全文`）
4. **等**何大人决定要不要用浏览器抓全文
5. 抓全文后 → 同一目录下补充正文 + 提炼要点
6. **若内容跟德勤 / 服务器强相关** → 在 `1-Projects/德勤/AI-Native/笔记/` 加一条引用（不复制正文）

### 定期清理
- **月度**：检查 `from-agent/` 下文件，确认哪些已经归档到 PARA 主目录、哪些可删除
- **永久保留**：所有 `from-agent/` 下的文件不自动删除（除非用户明确要求）

---

## ⚠️ Push 注意事项

- ✅ `current-server/` 不自动 push（README §目录约定 明确）
- ✅ 所有 `from-agent/` 内容默认 `uploaded: false`
- ✅ Push 前必须先解决 vault 远端分叉（master HEAD `47cb808f` vs 本地领先 commit）
- ❌ **不**直接 `git push origin master`（会被 rejected）

---

## 📊 违规回溯记录

| 时间 | 文件 | 原违规位置 | 回溯后位置 | commit |
|---|---|---|---|---|
| （待补） | 2026-07-09 又一个多 Agent IDE | `2-Areas/公众号文章/` | `current-server/from-agent/`（待回溯）| — |
| （待补） | 2026-07-10 Pi：2026 最被低估 | `2-Areas/公众号文章/` | `current-server/from-agent/`（待回溯）| — |
| （待补） | 2026-07-10 Spring AI 2.0 | `2-Areas/公众号文章/` | `current-server/from-agent/`（待回溯）| — |
| （待补） | 2026-07-11 OpenMaic | `2-Areas/公众号文章/` | `current-server/from-agent/`（待回溯）| — |
| （待补） | 2026-07-14 25K+ Star DeepTutor | `2-Areas/公众号文章/` | `current-server/from-agent/`（待回溯）| — |

---

**作者**：小助 — OpenClaw (MiniMax-M3) — 2026-07-18 11:36
**触发者**：何大人 11:34 "你这台机器的内容不是都应该放到current-server目录的吗"
**依据**：`/root/vault/current-server/README.md` §目录约定 + §目录约定