---
type: tool-screenshot
title: PiHerdrAgents 界面截图分析
tool: PiHerdrAgents
uploaded_date: 2026-09-28
source: 何大人发送
tags:
  - AI-Agent
  - 多智能体
  - 并行
  - PiHerdr
---

# PiHerdrAgents 界面截图分析

## 工具概况

| 属性 | 值 |
|---|---|
| 工具名 | Pi Herdr Agents |
| 版本标签 | PI PACKAGE |
| 核心定位 | Parallel agents. One terminal. |
| 关键特性 | non-blocking / supervised / recoverable |

## 命令行参数（截图显示）

```
pi herdr --2 activo 1 open -- 1m 2m 7m
```

## 监控面板：pi - subagents

状态：`2 active • 1 open`

| # | 智能体 | 任务 | 状态 | 耗时 |
|---|---|---|---|---|
| 1 | Scout:Auth | 认证侦察 | active • read | 7m |
| 2 | Worker:API | API 工作 | active • bash | 2m |
| 3 | Reviewer | 审查 | waiting | 1m |

## 架构节点

- **PARENT PI**（interactive, returns immediately）
  - → DEDICATED HERDR SURFACES
  - → [中间节点]
  - → HERDR NATIVE

## 关键特性

- 非阻塞：子任务不阻塞父 Pi 会话
- 可监控：LIVE STATUS 实时可见
- 可恢复：recoverable 架构
- 工作树交接：WORKTREE HANDOFF 支持任务迁移

## 相关项目补充

### CLM（Contrastive Language Models）

| 类型 | 地址 |
|---|---|
| **GitHub** | https://github.com/Contrastive-LM/CLM |
| **HuggingFace** | https://huggingface.co/Contrastive-LM |
| **Blog** | https://contrastive-lm.notion.site |
| **Discord** | https://discord.gg/5dAQEDJBs |

**CLM-v0.1 定位**：System One 模型（快系统），用于快速决策
- 基于 Qwen3-8B + 60M Nemotron 问答对预训练
- 对标 Jev，在 computer-use / gaming / tool-calling 上延迟低 9 倍
- 核心思路：状态与动作解耦，embedding 独立缓存复用
- License: Apache-2.0

```bash
pip install contrastive-lm
# vLLM 跑 encoder，clm-serve 跑 CLM-8B
```

---

## 截图文件

`2026-09-28_screenshot_PiHerdrAgents.jpg`
