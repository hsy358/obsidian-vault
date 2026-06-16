---
type: inbox-temp
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
---

# Goose - Your Native Open Source AI Agent

**官网：** https://goose-docs.ai/
**GitHub：** https://github.com/aaif-goose/goose（现属于 Linux Foundation 下的 Agentic AI Foundation）

## 概述

Goose 是一个开源、可扩展的通用 AI Agent，运行在本地机器上。不仅限于代码——可用于研究、写作、自动化、数据分析等一切需要完成的任务。

**数据亮点：** 45k+ GitHub stars | 500+ Contributors | 70+ MCP extensions

## 核心特性

### 多形态交付
- **桌面应用**：macOS / Linux / Windows 原生桌面客户端
- **CLI**：完整的终端工作流工具
- **API**：可嵌入任何地方
- **技术栈**：Rust 构建，追求性能和可移植性

### 多 LLM 支持
- 支持 **15+ providers**：Anthropic、OpenAI、Google、Ollama、OpenRouter、Azure、Bedrock 等
- 支持 API key 或现有订阅（Claude、ChatGPT、Gemini）通过 ACP 接入

### Recipes（工作流配置）
- 将工作流捕获为可移植的 YAML 配置
- 可与团队共享、在 CI 中运行
- 支持指令、扩展、参数和子 recipes

### MCP Apps
- 扩展可以在 goose Desktop 内直接渲染交互式 UI（按钮、表单、可视化）
- 新型 Agent 驱动工具的构建方式

### Subagents
- 生成独立的子 Agent 并行处理任务——代码审查、研究、文件处理
- 保持主对话干净

### 安全
- Prompt 注入检测
- 工具权限控制
- 沙箱模式
- **Adversary Reviewer**：监控不安全操作的对抗审查模式

## 开放标准

### Model Context Protocol (MCP)
- AI Agent 连接工具和数据源的开放标准
- goose 是最早的采用者之一，拥有最深入的集成之一
- 70+ 文档化的扩展且在增长

### Agent Client Protocol (ACP)
- 与编程 Agent 通信的标准
- goose 作为 ACP server 工作——可从 Zed、JetBrains、VS Code 连接
- 也可以使用 ACP Agent（如 Claude Code、Codex）作为 provider

### Agentic AI Foundation (AAIF)
- goose 属于 Linux Foundation 下的 AAIF
- 确保项目保持供应商中立、社区治理、长期开放

## 安装方式

**桌面应用：** 从 [官方下载页](https://goose-docs.ai/docs/getting-started/installation) 获取 macOS / Linux / Windows 版本

**CLI 安装：**
```bash
curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | bash
```

## 相关链接

- Discord：https://discord.gg/goose-oss
- YouTube：https://www.youtube.com/@goose-oss
- Twitter/X：https://x.com/goose_oss
- LinkedIn：https://www.linkedin.com/company/goose-oss