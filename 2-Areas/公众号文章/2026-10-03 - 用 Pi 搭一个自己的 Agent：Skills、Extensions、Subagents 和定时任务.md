---
type: article-metadata
file_type: wechat
file_path: /root/vault/2-Areas/公众号文章/2026-10-03 - 用 Pi 搭一个自己的 Agent：Skills、Extensions、Subagents 和定时任务.md
source: 微信公众号
uploaded_date: 2026-10-03
title: 用 Pi 搭一个自己的 Agent：Skills、Extensions、Subagents 和定时任务
description: 介绍 Pi Agent 框架的 Skills、Extensions、Subagents 和定时任务机制
tags: [agent, pi, skills, subagents, extensions]
url: https://mp.weixin.qq.com/s/uZrIlXZMq8Rz8cYRN1J5sQ
author: tc9011
---

# 用 Pi 搭一个自己的 Agent：Skills、Extensions、Subagents 和定时任务

> 来源：微信公众号，2026-10-03
> 作者：tc9011

## 摘要

Pi 是一个 AI Coding Agent，和 OpenClaw 有相似的设计理念。本文介绍 Pi 的四大扩展机制：

1. **Skills** - 按需加载的能力包，提供专业化工作流
2. **Extensions** - TypeScript 模块，钩入 Pi 生命周期（工具/命令/事件处理/自定义UI）
3. **Subagents** - 子 Agent 委托机制，主 Agent 把任务分派给隔离的子会话
4. **定时任务** - 调度式/事件驱动式 re-wake

## 核心机制

### Subagent 使用时机

- **主 Agent 执行任务前**：做 scouting、规划
- **主 Agent 执行任务中**：并行处理独立子任务
- **主 Agent 执行任务后**：代码审查、总结

### 子 Agent 适用场景

- 边界明确、独立于主任务的模块
- 代码审查、侦察任务
- 不需要主 Agent 直接观测修改内容的任务

### Subagent 痛点

- 阻塞式调用会卡住主 Agent
- 子 Agent 的"局部视野"导致上下文转述偏移
- 多 Agent 修改同一模块可能产生冲突

## Pi vs OpenClaw 对照

| 机制 | Pi | OpenClaw |
|------|-----|---------|
| Skills | `SKILL.md` 格式，技能包 | `skills/` 目录 + `SKILL.md` |
| Extensions | TypeScript 钩子 | 插件系统 |
| Subagents | `pi-subagents` npm 包 | `sessions_spawn` |
| 定时任务 | `pi-loop` 扩展 | `cron` |

## 相关链接

- Pi 官网：https://pi.dev
- Pi Package Catalog：https://pi.dev/packages
- 博客园笔记：https://www.cnblogs.com/somebottle/p/22642570/
