---
title: "awesome-llm-apps (140k ⭐)"
author: Shubham Saboo
source: github
url: https://github.com/Shubhamsaboo/awesome-llm-apps
homepage: https://www.theunwindai.com
saved_date: 2026-10-02
tags: ["AI-Agent", "RAG", "LLM", "OpenSource"]
description: "100+ 开源 AI Agents / Agent Skills / RAG 应用，Apache-2.0，支持 Claude/GPT/Gemini/DeepSeek/Llama/Qwen"
---

# awesome-llm-apps (140k ⭐)

**Repo**: [github.com/Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)
**官网**: [theunwindai.com](https://www.theunwindai.com)
**Star**: 140k+，Trending #1
**License**: Apache-2.0（可克隆、可商用）

## 目录结构

| 目录 | 内容 |
|---|---|
| `starter_ai_agents/` | 入门级 AI Agent 模板（30秒可跑） |
| `advanced_ai_agents/` | 高级 Agent（含 multi-agent） |
| `agent_skills/` | 可插拔 Agent 技能（npx skills add 安装） |
| `voice_ai_agents/` | 语音 Agent |
| `always_on_agents/` | 常驻 Agent（如 HN 新闻简报） |
| `mcp_ai_agents/` | MCP 协议 Agent |
| `generative_ui_agents/` | 生成式 UI Agent |
| `advanced_llm_apps/` | 高级 LLM 应用 |
| `rag_tutorials/` | RAG 教程 |
| `ai_agent_framework_crash_course/` | Agent 框架速成课 |

## 亮点示例

### Agent Skills（用 npx 10秒安装到 Coding Agent）
- **Project Graveyard** — 分析你放弃的 side projects 原因
- **First Reader** — 模拟真实读者，报告哪里失去兴趣
- **Scope Creep Detector** — 检测 diff 是否超出原始需求
- **Commit Archaeologist** — 从 git commit 历史重建代码存在原因
- **Self-Improving Agent Skills** — 技能自我改进 against evals

### 特色 Agent
- **Insurance Claim Live Agent Team** — 语音理赔实时处理
- **AI Fraud Investigation Agent** — 公开记录交叉审讯
- **AI Home Renovation Agent** — 照片进，逼真重设计出
- **Always-on HN Briefing Agent** — 睡前读 Hacker News

## 快速启动

```bash
# 克隆任意 Agent
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd awesome-llm-apps/starter_ai_agents/ai_travel_agent
pip install -r requirements.txt
streamlit run travel_agent.py

# 给 Coding Agent 安装技能（10秒）
npx skills add https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/agent_skills/project-graveyard
```

## 对德勤项目的参考价值

- **Agent Skills 架构**：可插拔技能包 → 类似 Hermes 的 tool/技能设计
- **Multi-agent 协作**：保险公司理赔团队（多角色 Agent 协作）→ 德勤 MVP 的 Executor Router/调度设计
- **Always-on Agent**：长周期任务 → 可借鉴德勤 Workspace 的后台任务设计
