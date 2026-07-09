---
type: wechat-article
title: "MindBase 开源的个人记忆中心，同步你与 AI 的上下文"
author: 深绘
url: https://mp.weixin.qq.com/s/um4XCHXEETjrI8gAWS-OdQ
publish_date: 2026-05-18
archived_date: 2026-07-09
archiver: 小助（何大人 7-9 晚授权"自我提升"专项）
related_repo: https://github.com/yanglongyun/mindbase
tags: [个人记忆中心, AI上下文同步, Cloudflare-Workers, D1-SQLite, MCP, OpenAPI, Anthropic-Skill, 开源]
---

# [开源] MindBase —— 开源的个人记忆中心，同步你与 AI 的上下文

> 来源：[深绘 微信公众号](https://mp.weixin.qq.com/s/um4XCHXEETjrI8gAWS-OdQ) · 2026-05-18 发布
> 配套仓库：https://github.com/yanglongyun/mindbase（MIT · Vue · 3 stars · 2026-05-26 创建 · 2026-07-08 最后更新）

## 一、项目定位

MindBase 是一个开源的记忆中心——同步你与 AI 的上下文。

🤖 **AI 互通** — 内置可查询数据的 agent，兼容大多数模型与市面上的各种 coding plan。同时提供 OpenAPI、MCP、Skill 三种方式打通你与 code agent 的互通——你的 code agent 在工作中能了解你的上下文，记录做过什么，积累经验，更新项目状态，记住你的偏好等。

🌱 **记忆有形状** — 记忆不是一条条抽象的数据，而是有自己形状、自己交互、自己功能的应用。内置 12 个应用，另有 40+ 可选，你还可以让 AI 快速开发属于你的记忆应用。

☁️ **数据在你手里** — 快速部署在 Cloudflare 上，底层依托 Workers、D1、R2，免费额度足够日常使用。D1 内建 30 天时间点恢复，兜住 AI 误操作，让你更放心地让 AI 读写你的数据。

## 二、🤝 同步你和 AI 的上下文

一份数据，所有 AI 共用。

### 内置 agent

产品内对话直连 D1，通过 `sql_query` 完成聚合、跨应用整理与批量更新，所有 SQL 在对话中可见。兼容 OpenAI 协议，可填写任意符合规范的 base URL。

### 外部 AI

`设置 → 协作` 开启，拿到一把 `mb_` token。三种接入：

- **Anthropic Skill** —— 下载 mindbase.zip 放入 skills 目录（Claude Code: `~/.claude/skills/mindbase/`），该 AI 在后续对话中即掌握 MindBase 的用法。
- **OpenAPI 3.1** —— 将 schema URL 与 token 粘贴进 ChatGPT 或任意支持 OpenAPI 的 AI，即可按需调用。
- **MCP** —— 通过 Model Context Protocol 接入，同样的两把工具（`apps_list` + `sql_query`）。

同一把 token，N 个 AI 共用同一份事实。

## 三、🌱 记忆有自己的形状

每个应用都有与之匹配的界面、交互与功能。

核心预置 12 个应用 —— 🏠 主页 · ✅ 待办 · 📚 笔记 · 💰 记账 · 📂 项目 · 🪶 个人档 · 🤖 大模型 · 📜 指令集 · 🔑 API · 📧 邮箱 · 🌐 域名 · 🗺️ 足迹。另有 40+ 免费模板在 **mindbase.me** 按需安装。

模板里没有的，在「设置 → 新建应用」里写下需求，自动拼出完整指令，交给 Claude Code 或 Codex，跑 `npm run deploy` 即可上线。

## 四、🏠 数据在你手里

- **免费即可用** —— Cloudflare 免费额度足够个人日常使用
- **30 天时间点恢复** —— D1 内建 point-in-time recovery，兜住 AI 误操作
- **一行导出** —— `wrangler d1 export` 整库带走，SQL 文件通用
- **开源自部署** —— MIT 协议，你的 token、你的 secret、你的数据

## 五、🚀 部署

需要：**Cloudflare 账号**、**Node 22+**

```bash
git clone https://github.com/realuckyang/mindbase
cd mindbase && npm install

# 1. 初始化 D1 与 R2
npx wrangler d1 create mindbase
```

```bash
# 数据导出
npx wrangler d1 export mindbase --remote --output backup-$(date +%Y%m%d).sql
```

## 六、🧱 技术栈

| 层 | 用了什么 |
|---|---|
| 运行时 | Cloudflare Workers |
| 存储 | D1 (SQLite) + R2 (图片) |
| 鉴权 | PBKDF2 + HS256 JWT cookie |
| 前端 | Vue 3 + Vite + Tailwind v4 |
| AI | OpenAI 兼容 Chat Completions + 流式 + 工具调用 |
| 标准 | OpenAPI 3.1 + Anthropic Skills + MCP |

## 七、目录结构

```
mindbase/
  schema.sql                 单一 DDL（系统 + 应用）
  AGENTS.md                  给 AI 加应用的契约
  server/
    index.js                 Worker 入口
    router.js                /api/<name> 统一分发
    apps/<name>/             用户应用（manifest / repository / service / api）
    system/
      auth/  utils/  image/  基础设施
      apps/<name>/           系统应用（chat / collab / settings / user）
    collab/                  对外 AI 接入（openapi / mcp）
  gui/
    main.js  App.vue  router.js  api.js
    apps/<name>/             用户应用 UI
    system/
      apps/<name>/           系统应用 UI
      components/            AppShell / Popover / Cover ...
      composables/ lib/      跨应用 hook / 工具
  skills/mindbase/           Anthropic Skill 源文件
```

## 八、License

MIT

---

## 九、深度分析（2026-07-09 补充）

> 这是何大人 7-9 晚授权"自我提升"专项分析。
> 详细借鉴分析见 `2-Areas/AI-Agent-研究/2026-07-09 - MindBase - Deep Research.md`

### 核心洞见

1. **"一份数据，多个 AI 共用"** —— MindBase 把个人记忆变成可被任意 AI 调用的服务
2. **三种 AI 互通方式**（OpenAPI / MCP / Skill）—— 同一 token 多 AI 共用同一份事实
3. **schema.sql 是单一事实源** —— 加新应用就是改 schema + 加目录
4. **AGENTS.md 是给 AI 加应用的契约** —— 直接规定每个新应用的目录结构（manifest / repository / service / api）
5. **事件流 + 上下文 pin** —— 完成度语义 + 系统级置顶上下文

### 对我的可借鉴点（详见 Deep Research）

- **MEMORY.md 顶部的「紧挨着的上下文」段 = 软版 "contexts pin"**（应该结构化）
- **schema.sql 单一事实源 → recommendations.json schema 应该更严格**
- **凭证不进代码**（重要：检查 OpenClaw 配置是否泄漏到 git）
- **轻量工程原则** = Yuxi 的 Simplicity First（v4 推荐策略已经在用）