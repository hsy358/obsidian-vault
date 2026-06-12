# Hermes Desktop - Desktop Companion for Hermes Agent

**Source:** https://github.com/fathah/hermes-desktop

## 概述

Hermes Desktop 是一个原生桌面应用，用于安装、配置和与 Hermes Agent 聊天——这是一个具有工具调用、多平台消息传递和闭环学习能力的自改进 AI 助手。

## 主要特性

### 安装与配置
- 引导式首次安装，带进度跟踪和依赖解析
- 支持本地或远程后端运行
- 多 provider 支持：OpenRouter、Anthropic、OpenAI、Google (Gemini)、xAI (Grok)、Nous Portal、Qwen、MiniMax、Hugging Face、Groq 等

### 功能亮点
- **流式聊天 UI**：SSE 流式传输、工具进度指示器、Markdown 渲染、语法高亮
- **Token 使用追踪**：实时显示 prompt/completion token 数量和成本
- **22 个斜杠命令**：/new, /clear, /fast, /web, /image, /browse, /code, /shell, /usage, /help 等
- **会话管理**：SQLite FTS5 全文搜索、按日期分组的历史记录
- **Profile 切换**：创建、删除和切换独立的 Hermes 环境
- **14 个工具集**：web、browser、terminal、file、code execution、vision、image gen、TTS、skills、memory 等
- **内存系统**：查看/编辑内存条目、用户 profile、容量追踪
- **Persona 编辑器**：编辑和重置 agent 的 SOUL.md 个性
- **定时任务**：cron 作业构建器，15 个投递目标
- **16 个消息网关**：Telegram、Discord、Slack、WhatsApp、Signal、Matrix、Email、短信、iMessage、DingTalk、飞书/Lark、企业微信、微信 Webhook 等
- **Hermes Office (Claw3d)**：可视化 3D 界面

### 技术栈
- Electron 39 — 跨平台桌面 shell
- React 19 — UI 框架
- TypeScript 5.9
- Tailwind CSS 4
- Vite 7 + electron-vite
- better-sqlite3 — 本地会话存储
- i18next — 国际化框架
- Vitest — 测试框架

### 文件位置
- `~/.hermes` — 主目录
- `~/.hermes/.env` — 环境配置
- `~/.hermes/config.yaml` — 配置文件
- `~/.hermes/profiles/` — profile 目录
- `~/.hermes/state.db` — 会话历史数据库
- `~/.hermes/cron/jobs.json` — 定时任务

## 平台支持
- macOS
- Windows（需要绕过 SmartScreen）
- Linux（.rpm、.deb 等）
- WSL 支持

## 相关链接
- Hermes Agent 主仓库：https://github.com/NousResearch/hermes-agent
- Atlas Cloud：https://www.atlascloud.ai
- 官网：https://hermesagents.cc/
- Telegram 群：https://t.me/hermes_agent_desktop