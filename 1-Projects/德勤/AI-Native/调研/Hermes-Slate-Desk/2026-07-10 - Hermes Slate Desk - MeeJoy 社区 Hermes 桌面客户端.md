---
title: Hermes Slate Desk - MeeJoy 社区 Hermes 桌面客户端
created: 2026-07-10
tags: [调研, AI-Native, Hermes, Tauri, 桌面客户端, 可借鉴]
source: https://gitee.com/8187735/Hermes-Slate-Desk
author: MeeJoy (Gitee @8187735)
license: MIT
status: 🟢 Active Development (最后更新 2026-05-18)
related_projects: [Hermes-Agent-v0.14, 德勤-AI-Native-MVP, AgentSpace]
---

# Hermes Slate Desk - MeeJoy 社区 Hermes 桌面客户端

> **一句话定位**：Hermes Agent 的极简桌面管理界面 —— 对话、工作区、文件管理、定时任务的轻量管理界面，面向日常用户，做减法，不堆砌。
>
> **来源**：Gitee `https://gitee.com/8187735/Hermes-Slate-Desk`

## 1. 项目基础信息

| 字段 | 值 |
|:-----|:---|
| 项目名 | Hermes Slate Desk |
| 作者 | MeeJoy (Gitee @8187735) |
| License | MIT (Copyright © 2026 MeeJoy) |
| 主仓库 | https://gitee.com/8187735/Hermes-Slate-Desk |
| 状态 | 🟢 Active Development |
| 最近更新 | 2026-05-18 |
| Hermes Gateway | 默认 `http://127.0.0.1:8642` |
| 平台支持 | macOS ✅ / Windows ✅ / Linux 🔄（coming soon）|

## 2. 8 大核心模块

| # | 模块 | 功能 |
|:--|:-----|:-----|
| 1 | 🏠 Home | 个人仪表板（会话快速入口 / 工作区切换 / 状态）|
| 2 | 💬 Chat | 流式对话（SSE `/v1/responses`）+ thinking 可视化 + 多模型切换 + 拖拽附件 + 上下文裁剪 |
| 3 | 📝 AI Notebook | Milkdown 编辑器（数学公式 / 代码高亮 / 流程图 / Mermaid）+ AI 辅助写作 + 一键导出 DOCX |
| 4 | ⏰ Scheduled Tasks | 可视化 cron 表达式构造器 + 任务 CRUD + 执行历史 + 桌面通知 |
| 5 | 📂 File Manager | 文件树（100+ 语言高亮）+ Tauri 原生编辑 + 多标签 + 拖拽上传 |
| 6 | 💻 Terminal | xterm.js + PTY（bash/zsh/sh）+ 多标签 + 分屏 + 命令历史 |
| 7 | ⚙️ Hermes Settings | Agent 管理 / Skills 市场 / Memory 管理 / Channel 配置 / Prompt 模板 / 分析面板 |
| 8 | 🔧 App Settings | Gateway 连接测试 + 主题（light/dark/system）+ 语言（zh/en/zh-tw）|

## 3. 技术栈（关键版本）

| 层 | 技术 | 版本 |
|:---|:-----|:-----|
| 桌面框架 | Tauri | 2.10.1 |
| 前端框架 | React | 19.2.4 |
| 构建工具 | Vite | 8.0.4 |
| UI 组件 | shadcn/ui + Radix UI | 本地管理 |
| 样式 | Tailwind CSS | 4.2.2 |
| 动画 | Framer Motion | 12.38.0 |
| 终端 | xterm.js | 5.3.0 |
| 图标 | Lucide React | 1.8.0 |
| 主题 | next-themes | 0.4.6 |
| 通知 | Sonner | 2.0.7 |
| 后端 | Rust | 2021 edition |
| 数据存储 | SQLite | `~/.hermes/hermes-slate-desk/sessions.db` |

## 4. 🔑 核心设计模式：Workspace Switching（**对德勤最有价值的点**）

> 每个项目拥有独立隔离的本地沙箱。

### 切换入口
- Sidebar 底部 `WorkspaceSwitcher` 组件
- Settings 面板的 Workspace 管理对话框

### 切换时同步隔离的维度

| 模块 | 行为 |
|:-----|:-----|
| 📚 Sessions | 自动过滤当前工作区的会话 |
| 📂 Files | 跳转到工作区目录 |
| 💻 Terminal | cwd 自动切换到工作区路径 |
| ⏰ Cron | 每个工作区独立存储 |
| 🧠 Env | 每个工作区独立存储 |
| 📝 Memory | 每个工作区独立存储 |

### 配置文件位置

```
~/.hermes/hermes-slate-desk/config.json
```

每个工作区结构：

```json
{
  "id": "unique-id",
  "name": "Project Name",
  "path": "/path/to/project",
  "icon": "🚀"
}
```

### 关键文件
- 前端状态：`src/App.jsx` 的 `currentWorkspace` / `workspaces`
- 后端命令：`src-tauri/src/commands/workspace.rs`

## 5. 后端 Tauri 命令分层

```
src-tauri/src/commands/
├── mod.rs
├── agent.rs         # Agent 命令
├── channels.rs      # Channel 管理
├── config.rs        # 配置管理
├── memory.rs        # 记忆存储
├── notebook.rs      # 笔记本功能
├── session.rs       # 会话管理
├── task.rs          # 任务管理
└── workspace.rs     # 工作区管理
```

## 6. 💡 对德勤 AI-Native MVP 的可借鉴点

### 6.1 高价值（直接可借鉴）

| 借鉴点 | 价值说明 | 落地建议 |
|:-------|:---------|:---------|
| **Workspace 隔离机制** | 客户/项目隔离 = 德勤核心合规需求 | 在 AgentSpace 里做 Workspace 抽象层（每个客户=独立沙箱）|
| **Skills 市场** | 可复用 Agent 能力的注册中心 | 已有 Hermes Settings 里的 SkillsPage，参考其 UI 形态 |
| **可视化 Cron 编辑器** | 德勤定时任务交付的 UI 直接可参考 | 直接借鉴 `CronView.jsx` 的视觉化 cron 构造器 |
| **多模型切换 UI** | 客户可按场景选不同 LLM | Chat 顶栏模型选择器（不用碰模型凭据，由 Hermes 环境变量管）|
| **三语国际化** | 德勤服务全球客户 | 已有 zh / en / zh-tw，直接 fork 即可 |
| **Tauri + Rust 桌面客户端形态** | 适合德勤内部审计/合规场景的本地化部署 | 桌面客户端作为企业版交付形态之一 |

### 6.2 中等价值（参考后自实现）

- **Milkdown 笔记 + AI 对话打通**（保存聊天片段到笔记）→ 德勤知识沉淀可用
- **可视化拖拽文件管理 + 100+ 语言高亮** → 德勤代码审查场景
- **xterm.js + PTY 分屏** → 德勤运维 Agent 调试终端
- **Session + 执行历史追踪** → 德勤可追溯交付需求

### 6.3 注意（**不要借鉴的坑**）

- ❌ **不要直接用 Hermes Gateway 8642 默认端口** —— 何大人 7-08 已暴露 cc-vibe 400 根因，端口/密钥要重新设计
- ❌ **不要抄 SKILL 设计** —— 已有 Hermes cc-vibe 400 根因，安全设计须独立审查

## 7. 🎯 跟德勤 AI-Native MVP 战略的对齐判断

### 决策链
1. **Hermes Agent v0.14 已是德勤 MVP 唯一选择**（何大人 5-11 决策 / 6-29 重申）
2. Hermes Slate Desk 是 MeeJoy 社区做的 Hermes **桌面客户端**，属于配套生态
3. **生态成熟度验证**：已有 GUI 客户端 → Hermes 在 B 端落地可行性 ↑

### 关键启示
- ✅ **Workspace 隔离 = 德勤核心需求**：每个客户工作区独立（数据 / 记忆 / 任务 / 凭据），这是 MeeJoy 社区验证过的设计模式
- ✅ **多形态交付**：Web（OpenClaw）+ 桌面（Tauri）+ CLI（hermes chat）全覆盖
- ✅ **Skills + Prompt 模板市场** = 德勤"Agent 能力中心"雏形

## 8. 调研结论

**评级**：⭐⭐⭐⭐（强烈推荐深度参考）

**3 条立刻可执行的下一步**：
1. clone 仓库本地跑通 `npm run tauri dev`，验证 Workspace Switching 流程（30 分钟）
2. 把 `CronView.jsx` + `WorkspaceSwitcher.jsx` 抽出来作为德勤 AgentSpace 的可视化模块（半天）
3. 把 SkillsPage + PromptTemplatesPage 的 UI 设计移植到德勤 AgentSpace 的"能力中心"页（1 天）

## 9. 关联资源

| 资源 | 链接 |
|:-----|:-----|
| Hermes Agent 指南 | https://hermes.xaapi.ai/guide/introduction |
| Hermes Skills 市场 | https://hermes-agent.nousresearch.com/docs/skills |
| Hermes Admin Panel | http://127.0.0.1:9119/ |
| Tauri 2 文档 | https://tauri.app/zh-cn/v2/ |
| shadcn/ui | https://ui.shadcn.com/ |

---

## 📎 引用说明

- **本笔记基于 Gitee 公开仓库 README 整理（不存原文，外部项目原文仅作引用）**
- **调研对象版本**：commit at 2026-05-18（README Last updated 字段）
- **调研时间**：2026-07-10
- **调研人**：小助（OpenClaw Agent）