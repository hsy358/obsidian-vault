# Research/ Index

> 由 `gen_index.py` 自动生成（23 条目）。OKF 规范渐进披露。


## AI-Native / R&D

* [OKF 与 vault 差异 audit 表](2026-06-22 - OKF 与 vault 差异 audit 表.md) — 对比 Google OKF v0.1 规范与何大人 /root/vault 实际数据，给出兼容性评估、差距清单、改进优先级。  `research-report · 2026-06-22`
* [YX AI Delivery Harness 对照分析 + Self-Driving R&D 方案 v2.1](2026-06-17 - YX AI Delivery Harness 对照分析 + 方案 v2.1.md) — YX Harness 底部双栏结构：  `research-report · 2026-06-17`
* [Self-Driving R&D v3.5 — 架构深度设计（架构维度，无代码）](2026-06-17 - Self-Driving R&D v3.5 架构深度设计.md) — 我们的系统围绕 4 个核心轴设计：  `architecture-design · 2026-06-17`
* [Self-Driving R&D v3.3 — Loop Engineering 自主改进闭环](2026-06-17 - Self-Driving R&D v3.3 Loop Engineering.md)  `research-report · 2026-06-17`
* [Self-Driving R&D v3.2 — YX Harness 二次分析后的深化](2026-06-17 - Self-Driving R&D v3.2.md) — YX Harness 显示 1-2-3-4-5 小数字点，我们用 sub-step JSON 实现：  `research-report · 2026-06-17`
* [AI-Native R&D 自驱动闭环 v3.1（35min 规则 + Ralph Loop + HTN + 5-Layer Runtime + DeepWiki）](2026-06-17 - AI-Native R&D 自驱动闭环 v3.1.md) — 1. 35-min 是硬限制（不是建议）— 超过就降级 2. Ralph Loop 是 1 行 bash — 简单但有效 3. HTN 减少 75% LLM 调...  `research-report · 2026-06-17`
* [AI-Native R&D 自驱动闭环 v3.0（GAN 架构 + Loop Engineering + 长跑实战）](2026-06-17 - AI-Native R&D 自驱动闭环 v3.0.md) — 每次 subagent 输出后，强制 validator 跑一遍： - 输出中提到的文件存在吗？ - 提到的数字（如"覆盖率 85%"）能验证吗？ - 跟 sp...  `research-report · 2026-06-17`
* [AI-Native R&D 自驱动闭环方案 v2.0（扔需求进去，AI 跑 10+ 小时自己闭环）](2026-06-17 - AI-Native R&D 自驱动闭环 v2.0.md) — 1. 确认方向 ✓（已说"扔需求进去跑 10+ 小时"） 2. 选第一个项目（建议：context-recovery v2 升级 或 PPT 复刻 V2） 3....  `research-report · 2026-06-17`
* [AI-Native R&D 全流程方案 v1.0](2026-06-17 - AI-Native R&D 全流程方案 v1.0.md) — 1. Harness 先行：基础设施先固化（OpenClaw / Claude Code） 2. Skill 模块化：每个环节一个 Skill，可复用 3. S...  `research-report · 2026-06-17`
* [公众号文章入 AI 知识库 完整搭建指南（OpenClaw + Obsidian + GitHub）](2026-06-21 - 公众号文章入 AI 知识库 完整搭建指南（可发布版）.md) — 刷到一篇深度长文 → 收藏 → 再也没打开过。这是绝大多数人的现状。  `build-guide`
* [知识工程三角：OKF 格式层 + KDD 流程层 + 成熟度评估层](2026-06-16 - 知识工程三角：OKF 格式层 + KDD 流程层 + 成熟度评估层.md) — 1. TL;DR —— 一句话 2. 三篇文章的核心模型 3. 三角理论：格式层 + 流程层 + 评估层 4. 延伸视角：Agent Harness 动态层 5...  `research-report`
* [Routa — Deep Research Report](2026-06-12 - Routa - Deep Research.md) — Routa is a workspace-first multi-agent coordination platform for software delive...  `research-report`
* [Hermes Desktop — Deep Research Report](2026-06-12 - Hermes Desktop - Deep Research.md) — Hermes Desktop is a native cross-platform desktop application (macOS, Windows, L...  `research-report`
* [Harnss — Deep Research Report](2026-06-12 - Harnss - Deep Research.md) — The project is maintained by OpenSource03 and licensed under MIT. It is built wi...  `research-report`
* [Goose — Deep Research Report](2026-06-12 - Goose - Deep Research.md) — 1. Project Overview 2. Technical Architecture 3. All Major Features 4. The MCP E...  `research-report`


## OKF / 知识工程

* [Google Cloud OKF — Open Knowledge Format](2026-06-22 - Google Cloud OKF Open Knowledge Format.md) — 不是 SDK、不是查询语言、不是中间件——就是一组带 frontmatter 的 .md 文件 + 目录结构。  `research`


## 其他研究

* [Self-Driving R&D v3.4 — 每个环节细化设计方案](2026-06-17 - Self-Driving R&D v3.4 每个环节细化设计.md) — 详见 A1. Access stage。  `technical-spec · 2026-06-17`
* [Self-Driving R&D · 独立可移植版 v4.2（生态融合版）](2026-06-19 - Self-Driving R&D 方案 v4.2（生态融合版）.md)  `note`
* [Self-Driving R&D · 独立可移植版 v4.1（深度优化）](2026-06-19 - Self-Driving R&D 方案 v4.1（深度优化版）.md) — v4.0 把阶段当成"8 个独立 stage"，但真实 R&D 中： - 阶段可以跳过（小项目不需要探索） - 阶段可以重复（验证不通过要回到 apply 修复...  `note`
* [Self-Driving R&D · 独立可移植版 v4.0](2026-06-19 - Self-Driving R&D 新方案 v4.0（独立可移植版）.md) — 每个阶段声明自己需要哪些 Skill，由 SkillRouter 在该阶段触发时自动加载：  `note`
* [Self-Driving R&D · 实战成本分析（v4.2 冷静版）](2026-06-19 - Self-Driving R&D 实战成本分析（MVP 优先）.md) — 对单个小项目来说，纯手工可能更快。  `note`
* [Self-Driving R&D · v5.0-lite（3.5 原则 + 独立可移植）](2026-06-19 - Self-Driving R&D v5.0-lite（3.5 原则 + 独立可移植）.md) — 要不要我直接开始写 workflow.yaml + 核心 6 个 Python 文件的代码？  `note`
* [知识工程框架图（Mermaid 版）](2026-06-16 - 知识工程框架图（mermaid）.md) — 由 MiniMax M3（小助）根据 4 篇微信文章整理；v0.3 草稿，2026-06-16  `framework-diagram`

