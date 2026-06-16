---
title: "Agent Harness 全景解析 模型不是产品，基础设施才是"
author: "AI炼金学徒"
publish_date: "2026-05-28 20:05:21"
saved_date: "2026-06-16"
source: "wechat"
url: "https://mp.weixin.qq.com/s/hFJ1MKhCQBnpsDKDzjwuqQ"
---
# Agent Harness 全景解析 模型不是产品，基础设施才是
# 深度拆解 Anthropic、OpenAI、LangChain 的 Agent 架构之争

阅读约 7 分钟 · 建议收藏

你有没有想过一个问题：

同一个 Claude 模型，放在网页里只能聊天，放在 Claude Code 里却能自己写代码、调 bug、完整交付一个项目。模型没变，为什么能力天差地别？

答案就是 Agent Harness——包裹在模型外面的那一层「外壳」。

今天这篇文章，带你拆解 Anthropic、OpenAI、LangChain 等巨头正在构建的 Agent 基础设施，以及为什么「选对 Harness」比「选对模型」更重要。

# 一、到底什么是 Agent Harness？

一条公式记住：Agent = Model + Harness

模型（Model）就是大脑——它只会接收文本/图片/音频，然后输出文本。不是模型的部分，就是 Harness。

Harness 具体包括哪些东西？

- 系统提示词（System Prompts）
- 工具、Skills、MCP 及其描述
- 捆绑基础设施（文件系统、沙箱、浏览器）
- 编排逻辑（子 Agent 生成、模型路由）
- Hook / 中间件（压缩、续跑、lint 检查）
一句话：模型提供智力，Harness 让智力变得可用。

# 二、为什么模型必须依赖 Harness？

从模型的角度看，它「天生残疾」——很多事情光靠自己是做不了的：

模型做不到的事

Harness 怎么补

跨会话保持状态

文件系统 + AGENTS.md，持久化工作记忆

执行代码

Bash 工具 + 沙箱环境

获取实时知识

Web Search + MCP 工具（如 Context7）

配置环境、装包

沙箱预装运行时 + 包管理器

长任务不跑偏

Ralph Loop + Plan 模式 + 自验证

核心逻辑：Harness 把人类经验「编码」进系统，让模型不用从零摸索。

# 三、Harness 的核心组件拆解

## 3.1 文件系统：最基础的 Harness 原语

Agent 需要持久化存储：读写真实数据、卸载超出上下文窗口的信息、跨会话保存进度。

文件系统 + Git 构成了一套「工作账本」：多个 Agent 和人类可以通过共享文件协作，版本控制让 Agent 能回滚错误、分支实验。

## 3.2 Bash + 代码：通用解题工具

与其为每种可能动作预制工具，不如给 Agent 一个 Bash 终端。模型可以自己写代码、执行、观察结果——等于给了它一台电脑，让它自己想办法。

这就是今天主流 Agent 的 ReAct 循环：推理 → 工具调用 → 观察结果 → 重复。

## 3.3 沙箱：安全执行环境

Agent 生成的代码不能直接在本地跑——安全风险太大。沙箱提供隔离环境，可以按需创建、批量扩展、用完销毁。

好的沙箱预装了语言运行时、Git CLI、测试框架、浏览器——Agent 开工即用，不需要手动配置环境。

## 3.4 记忆与搜索：让 Agent 持续学习

模型的权重是冻结的——它不知道训练截止日期之后发生的任何事。Harness 通过两个途径补这个缺口：

•文件记忆：AGENTS.md 文件跨会话注入上下文，Agent 自己读写的记忆在下次启动时自动加载

•实时搜索：Web Search + Context7 等 MCP 工具，让 Agent 获取最新的库版本、API 文档

## 3.5 上下文管理：对抗「上下文腐烂」

上下文腐烂（Context Rot）：随着上下文窗口被填满，模型推理能力持续下降。上下文是稀缺资源，Harness 必须精打细算：

•压缩（Compaction）：上下文快满时，智能摘要旧对话，让 Agent 能继续工作

•工具输出卸载：大工具输出只保留头尾片段，完整内容写入文件系统按需读取

•Skills 渐进披露：不在启动时加载全部工具描述，而是按需激活——避免启动即污染

## 3.6 长期自主执行：让 Agent 跑几个小时不跑偏

这是 Harness 工程的圣杯——让 Agent 自主完成复杂任务，跨越多个上下文窗口，不跑偏。

•Ralph Loop：Harness 拦截模型的退出信号，把原始任务注入干净的新上下文窗口，强制 Agent 继续工作

•Plan + 自验证：模型先拆解目标为步骤，写入计划文件；每完成一步，Harness 跑测试套件，失败就带着错误信息回环修复

•文件系统 + Git：作为持久化工作账本，新 Agent 启动时只需读 Git log 就能快速了解项目状态

这些原语叠加起来，才让 Agent 从「聊两句就跑偏」进化到「能独立完成一个完整项目」。

# 四、薄 Harness vs 厚 Harness：两种哲学

业内对 Harness 的设计存在一个频谱：

特征

薄 Harness

厚 Harness

代表

核心理念

信任模型，最少干预

编码最佳实践

——

编排逻辑

简单 ReAct 循环

复杂工作流 + 状态机

——

代表产品

Claude Code

LangGraph / deepagents

——

优势

灵活性高，模型越强越受益

确定性高，可控性强

——

劣势

模型弱时容易跑偏

可能限制模型自主性

——

没有绝对的对错。Anthropic 赌的是「模型会越来越强，Harness 应该越来越薄」；LangChain 赌的是「好的编排逻辑能让任何模型表现更好」。两种策略各有赢的场景。

# 五、模型训练与 Harness 的「共进化」陷阱

一个容易被忽视的事实：今天的 Agent 产品（Claude Code、Codex）是在模型和 Harness 共同参与下后训练的。

这意味着模型学会了依赖特定的 Harness 行为。就像长期用拐杖走路的人，突然拿走拐杖反而不会走了。

一个典型案例：Opus 4.6 在 Claude Code 中的 TerminalBench 得分，远低于同样的 Opus 4.6 在其他 Harness 中的得分。不是模型不行，是它被训练成了「只在自己的壳里好用」。

反过来也有好消息：LangChain 团队只换了 Harness，就把他们的编程 Agent 从 TerminalBench 前 30 名拉到了前 5 名。模型没变，只换壳。

结论：选对 Harness 的收益，可能比换一个更强模型的收益还要大。

# 六、Harness 工程的未来

随着模型越来越强，今天 Harness 中的部分功能会被模型吸收——比如规划、自验证、长程一致性。但这不意味着 Harness 会消失。

就像 Prompt Engineering 到今天依然有价值一样，Harness Engineering 也会持续存在——因为好的基础设施、正确的工具、持久化状态和验证循环，能让任何模型更高效。

三个前沿方向：

- 编排数百个 Agent 并行工作在共享代码库上
- Agent 自我分析执行轨迹，自动识别并修复 Harness 级别的故障模式
- Harness 根据任务动态组装正确的工具和上下文，而非启动时全量预配置

# 写在最后

模型提供智力，Harness 让智力变得可用。

如果你正在搭建自己的 Agent 系统，花在 Harness 上的精力不应该少于花在选模型上的精力。

同一个模型 + 不同 Harness = 完全不同的产品能力。这不是夸张——LangChain 从 30 名到第 5 名，只换了壳。

收藏这篇文章，下次有人问你「Claude Code 和 ChatGPT 用的不是同一个模型吗」，直接把 Agent = Model + Harness 这条公式甩给他。

转发给正在搭 Agent 的同事，他们会感谢你的。

— END —
