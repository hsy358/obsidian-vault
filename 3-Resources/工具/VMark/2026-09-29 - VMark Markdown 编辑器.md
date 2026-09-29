---
type: document-metadata
file_type: markdown
file_path: /root/vault/3-Resources/工具/VMark/2026-09-29 - VMark Markdown 编辑器.md
source: 微信转发
uploaded_date: 2026-09-29
title: VMark - AI 原生 Markdown 编辑器
description: 本地优先、AI 原生的 Markdown 编辑器，原生支持 MCP 协议
tags: [工具, Markdown, 编辑器, MCP, AI]
size_bytes: null
github_url: https://github.com/xiaolai/vmark
website_url: https://vmark.app
tech_stack: [Tauri-v2, Rust, React-19, TypeScript, Zustand-v5, Tiptap, CodeMirror-6, Tailwind-CSS-v4]
---

# VMark - AI 原生 Markdown 编辑器

## 项目信息

- **GitHub**: https://github.com/xiaolai/vmark
- **官网**: https://vmark.app
- **作者**: xiaolai
- **开发方式**: vibe-coded（100% AI 生成，人类监督）
- **安装**: `brew install xiaolai/tap/vmark` 或手动下载 Release

## 技术栈

- **Tauri v2**（Rust + WebView）— 桌面框架
- React 19 + TypeScript
- Zustand v5（状态管理）
- Tiptap（所见即所得编辑）
- CodeMirror 6（源码模式）

## 核心特点

### AI 集成（原生 MCP）
- Settings → Integrations → Install，**一键安装 MCP**
- 支持：**Claude Desktop、Claude Code、Codex CLI、Antigravity CLI、Grok CLI、opencode**
- AI Genies（内联写作辅助）
- AI 和人类操作同一份纯文本文件，无翻译层

### Schema-Aware 预览（亮点）

| 文件类型 | 预览效果 |
|---|---|
| `.github/workflows/*.yml` | 工作流图 |
| `Cargo.toml` | 依赖树 |
| `package.json` | 依赖树 |
| `pyproject.toml` | 依赖树 |
| JSON/YAML/TOML | 可导航树形结构 |

### 排版（CJC 特化）
- **20+ 中日韩排版规则**，原生内置
- 自动处理中英文间距和标点
- 无需手动调 CSS

### 编辑模式
- **WYSIWYG**（Tiptap/ProseMirror）— 默认
- **Source Peek**（F5）— 侧边源码预览
- **Source Mode**（F6，CodeMirror 6）— 纯源码

### 多语言
- **10 种语言**：EN、简中、繁中、日、韩、德、西、法、意、葡
- 首访自动检测

### 其他
- **多光标**：Mod+D 选下一个匹配、Alt+点击添加、Mod+Alt+↑↓ 垂直光标
- Tab Escape：自动配对括号/引号，按 Tab 跳到闭括号后
- 6 主题：White、Paper、Mint、Sepia、Night、Solarized
- **完全本地**：无云、无账号、无分析
- 165 个可定制快捷键

## 定位

本地优先 + AI 原生，适合：
- **中日韩混排**的专业写作（排版原生省心）
- **AI 辅助写作**（Claude/Codex 直接读写文件，MCP 一键接入）
- **本地优先**的私密性需求
- **Vibe coding 工作流**（xiaolai 全程 AI 写，VMark 本身也是 AI 写的）

## Obsidian 对比

| | VMark | Obsidian |
|---|---|---|
| AI 接入 | MCP 原生，一键 | 插件（Claudian 等） |
| 排版 | 20+ CJK 规则原生 | 主题/CSS |
| 格式预览 | Schema-aware 树视图 | 插件 |
| 知识管理 | 无（纯编辑） | 双向链接/dataview |
| 发布 | 无 | Obsidian Publish |
| 平台 | macOS 为主，Win/Linux 实验性 | 全平台 |
| 来源 | vibe-coded（AI 全程） | 传统开发 |
