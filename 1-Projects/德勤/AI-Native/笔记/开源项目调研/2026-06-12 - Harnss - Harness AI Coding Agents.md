---
type: inbox-temp
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
title: Harnss - Harness AI Coding Agents
description: Harnss 是一个跨平台桌面应用，为 AI 编程 Agent（Claude Code、Codex 及任何 ACP 兼容 Agent）提供统一的运行、管理和切换...
tags:
- AI
- Agent
- Claude
- GPT
- Harness
---
# Harnss - Harness AI Coding Agents

**Source:** https://github.com/OpenSource03/harnss

## 概述

Harnss 是一个跨平台桌面应用，为 AI 编程 Agent（Claude Code、Codex 及任何 ACP 兼容 Agent）提供统一的运行、管理和切换界面。不再丢失上下文、会话或工具状态。

## 核心特性

### 多引擎支持
- **Claude Code** — 通过 Anthropic Agent SDK 运行，需要 Claude 账号（订阅或 API key）
- **Codex** — JSON-RPC app-server，需要 Codex CLI 在 PATH + OpenAI API key 或 ChatGPT 账号
- **ACP Agents** — Agent Client Protocol 兼容的任何 Agent

### Agent 运行与可视化
- 并行运行多个 Agent 会话，每个会话有独立状态、历史和上下文，瞬时切换
- **工具调用渲染为交互卡片** — 单词级 diff、语法高亮、内联 bash 输出，而非原始 JSON
- 子 Agent 任务嵌套显示，逐步进度追踪
- 变更面板按轮次汇总文件变更

### 内置工具集成
- **终端**：多标签 PTY，本地 shell 进程
- **浏览器**：内嵌浏览器，内联打开 URL
- **Git**：Stage/unstage/commit/push，分支浏览，提交历史，工作树管理，AI 生成提交信息
- **MCP 服务器**：支持 stdio、SSE、HTTP 传输，OAuth 自动处理，每个项目独立配置

### 项目与空间管理
- **Spaces**：用命名分组组织项目，自定义图标和颜色
- **Projects**：映射到磁盘文件夹，会话、历史、面板设置均按项目隔离
- 全局搜索：跨会话标题和消息内容搜索
- 导入并恢复 Claude Code CLI 之前的会话

### 安全与控制
- **Plan 模式**：Agent 先起草计划再执行变更
- **三级权限**：Ask First / Accept Edits / Allow All，随时切换不中断上下文

### 其他功能
- 内联截图和图片标注工具
- 语音输入（macOS 原生听写或本地 Whisper 模型，无需 API key）
- 可配置 OS 通知：计划审批请求、权限提示、Agent 问题、会话完成
- ACP 社区注册表浏览和安装
- 自定义 Agent 配置（命令、参数、环境变量、图标）
- 完整的文本搜索和会话历史

## 支持平台

| 平台 | 下载格式 |
|------|----------|
| macOS (Apple Silicon) | .dmg (arm64) |
| macOS (Intel) | .dmg (x64) |
| Windows (x64) | .exe installer |
| Windows (ARM64) | .exe installer |
| Linux | .AppImage / .deb |

## 技术与协议

- **协议**：基于 [Agent Client Protocol (ACP)](https://agentclientprotocol.com)
- **技术栈**：未明确说明（Electron/Tauri 类跨平台框架）
- **当前状态**：早期开发中，预构建二进制未签名

## 相关链接

- [Releases](https://github.com/OpenSource03/harnss/releases/latest)
- [ACP Agent Registry](https://agentclientprotocol.com/get-started/registry)
- [CLAUDE.md](https://github.com/OpenSource03/harnss/blob/main/CLAUDE.md)（项目约定）