---
title: 刚刚！AWS 开源 Strands Harness：Agent 开始只换模型、不换"身体"
source: 微信公众号 - DataFunTalk
url: https://mp.weixin.qq.com/s/DWblbrYba92dPp9j2CnXxw
fetched_date: 2026-09-22
tags: [公众号, aws, strands, harness, agent, 执行器抽象, 德勤项目]
status: partial-fetch
---

# 刚刚！AWS 开源 Strands Harness：Agent 开始只换模型、不换"身体"

> 来源：DataFunTalk
> 链接：https://mp.weixin.qq.com/s/DWblbrYba92dPp9j2CnXxw
> 抓取日期：2026-09-22

## 备注

⚠️ 微信文章正文被反爬截断（rawLength=32，仅抓到标题）。需要浏览器渲染才能拿到完整正文。

后续如需深度阅读，可：
- 用 browser 工具带登录态抓
- 或在微信里手动复制粘贴原文
- 或直接搜 GitHub: `aws/strands-agents`（AWS 官方组织）

## 与当前工作的关联 ⭐⭐⭐

> **核心论点**：「只换模型、不换身体」= **执行器抽象层 + 可插拔适配器**
> 
> 这就是何大人 2026-06-29 为德勤项目定的架构方向。

直接对应 4 条已定决策：

| 已定决策（6-29）                                  | Strands Harness 对应                              |
| ------------------------------------------------ | -------------------------------------------------- |
| Hermes / OpenClaw / Codex / Claude Code 都是可插拔执行器 | Strands 的核心卖点："Agent 只换模型，不换身体"     |
| 调研整个工程栈，不是某个 Agent 框架               | Strands 提供 harness（身体）+ model（大脑）解耦    |
| 设计执行器抽象层                                  | 实质就是 harness layer                             |
| 整套系统可以单独部署                              | 每个组件独立可部署 + 模块化打包                    |

## 下一步建议

1. **优先级**：用 `web_fetch` 抓不到正文时，**直接上 browser 工具**带登录态抓
2. **价值判断**：如果 Strands 是 Python SDK + 异步流 + MCP 工具调用 → 大概率是 Hermes-based 德勤 MVP 的最佳**借鉴目标**（不是替代）
3. **不需要再问**："Strands 替代 Hermes 吗？"——已经在 6-29 决策里否定了

## 待办

- [ ] 用 browser 抓完整正文（重要技术参考）
- [ ] 跑通 Strands 的 hello world，验证 MCP / 工具调用接口
- [ ] 把"借鉴什么技术到 Hermes-based 德勤 MVP"写成 1 份 1 页笔记