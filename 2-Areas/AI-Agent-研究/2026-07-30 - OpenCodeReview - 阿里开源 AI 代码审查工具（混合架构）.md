---
type: research-report
title: OpenCodeReview —— 阿里开源的 AI 代码审查工具（混合架构：确定性工程 + LLM Agent）
repo: alibaba/open-code-review
url: https://github.com/alibaba/open-code-review
homepage: https://open-codereview.ai
npm: https://www.npmjs.com/package/@alibaba-group/open-code-review
license: Apache-2.0 (Copyright 2026 Alibaba)
language: Go (70%) + TypeScript (17%, WebUI + Agent layer)
released: 2026-05（GitHub Trending 5-28 上榜，7-23 达到 #1）
stars: 14.4k（截至 2026-07-27）
benchmark: 50 popular repos + 200 real PRs + 10 languages + 80+ senior engineers / 1,505 ground-truth issues
tags: [ai-code-review, alibaba, hybrid-architecture, deterministic-engineering, agent, code-review, npe, thread-safety, xss, sql-injection, open-source, go, typescript, ocr-cli, mcp, tencent-hunyuan-equivalent]
source:
  url: https://github.com/alibaba/open-code-review
  fetched: 2026-07-30T22:30+08:00
  by: 小助 via web_search + GitHub README
context_origin: 何大人 2026-07-30 22:25 微信转发的公众号文章摘要
---

# OpenCodeReview —— 阿里开源 AI 代码审查工具

> **一句话判断**：OCR 不是又一个 AI 代码审查 agent，是**"混合架构"的工程化落地**——**确定性工程**（文件选择 / 智能 bundle / 模板规则 / 定位模块）处理"不能错"的硬约束，**LLM Agent**（场景化 prompt + 场景化工具集）处理"需要灵活判断"的动态决策。同等模型下精度/F1 显著更高、token 消耗仅 1/9、review 更快——**用 recall 换 precision** 的刻意取舍。

## 一、项目快照

| 维度 | 信息 |
|---|---|
| 仓库 | [alibaba/open-code-review](https://github.com/alibaba/open-code-review) |
| 官网 | [open-codereview.ai](https://open-codereview.ai) |
| 文档 | [open-codereview.ai/docs](https://open-codereview.ai/docs) |
| 内部背景 | **阿里集团内部官方 AI 代码审查助手，2 年、数万开发者、数百万代码缺陷** |
| 发布时间 | 2026-05（5-28 首次 GitHub Trending，7-23 达到 #1） |
| Stars | 14.4k（7-27 快照） |
| Forks | 971（7-27） |
| 许可证 | **Apache-2.0**（无付费企业版，仓库里就是阿里内部用的同一份） |
| 主语言 | **Go 70%**（CLI 热路径 + 确定性流水线）+ **TypeScript 17%**（Agent 层 + WebUI） |
| 安装 | `npm install -g @alibaba-group/open-code-review` |
| CLI 命令 | `ocr` |
| 多语言 README | 英 / 简中 / 日 / 韩 / 俄 |

## 二、它解决什么具体问题

### 2.1 纯 LLM Agent 做代码审查的三大痛点

用过 Claude Code + Skills 做代码审查的开发者，都遇到过这三种"翻车"：

| 痛点 | 表现 | 根因 |
|---|---|---|
| **Incomplete coverage** | 大 changesets 上 agent"cut corners"，选择性 review，漏掉其他文件 | 纯语言驱动的 agent 没有"必须 review 全部文件"的硬约束 |
| **Position drift** | 报告的问题跟实际代码位置不匹配，行号或文件引用飘了 | 定位没专门的工程化保证，纯靠 LLM 注意力 |
| **Unstable quality** | 自然语言驱动的 Skills 难调试，prompt 稍微变一下质量就起伏 | prompt 是"软约束"，不是"硬规则" |

**根因**：**纯语言驱动的架构缺乏 review 过程的硬约束**。

### 2.2 OCR 的解法：混合架构

```
┌─────────────────────────────────────────────────────────┐
│                  OpenCodeReview 混合架构                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────┐  ┌─────────────────┐  │
│  │  Deterministic Engineering  │  │  LLM Agent      │  │
│  │  ────────────────────────   │  │  ─────────────  │  │
│  │  • 精确文件选择（哪些 review │  │  • 场景化 prompt│  │
│  │    / 哪些排除）             │  │  • 场景化工具集 │  │
│  │  • 智能文件 bundle          │  │  • 动态决策     │  │
│  │    （相关文件打包 + 子      │  │  • 动态上下文   │  │
│  │     agent 并发）            │  │    检索         │  │
│  │  • 细粒度规则匹配           │  │                 │  │
│  │    （模板引擎，非 LLM）     │  │                 │  │
│  │  • 外部定位 + 反思模块      │  │                 │  │
│  │    （独立模块，提高定位     │  │                 │  │
│  │     和内容准确度）          │  │                 │  │
│  │                             │  │                 │  │
│  │  ──────────                 │  │  ──────────     │  │
│  │  处理"不能错"的硬约束       │  │  处理"灵活判断" │  │
│  │                             │  │                 │  │
│  └─────────────────────────────┘  └─────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2.3 核心设计哲学（何大人原文没说的细节）

**1. 用 recall 换 precision（刻意取舍）**

> Note that its Recall is lower than general-purpose agents — **a deliberate trade-off favoring precision over noise**.

OCR 主动放弃一部分召回率，避免大量误报淹没开发者。**这是产品定位决定，不是技术缺陷**——审查工具最重要的不是"找到所有问题"，是"报告的每个问题都是真问题"。

**2. divide-and-conquer（分治 + 并发）**

- 相关文件被打成 bundle（例：`message_en.properties` + `message_zh.properties` 一起 review）
- 每个 bundle 跑一个 **sub-agent + 隔离上下文**
- 大 changesets 上**保持稳定**，天然支持并发 review

**3. 模板引擎规则匹配 > LLM 规则引导**

- 用模板引擎按文件特征匹配规则
- 比纯 LLM 引导更稳定、更可预测
- **LLM 的注意力被聚焦在真正需要判断的地方**

**4. 外部定位 + 反思模块**

- 独立的 comment-positioning + comment-reflection 模块
- 系统性提高**位置准确度 + 内容准确度**
- 不依赖单一 LLM call 的注意力

## 三、Benchmark（数字）

OCR 自建基准测试（这是关键差异化——他们**真做了 benchmark**，不是嘴炮）：

| 维度 | 数据 |
|---|---|
| 仓库数 | 50 个流行开源仓库 |
| PR 数 | 200 个真实 PR |
| 语言数 | 10 种 |
| 标注 | **80+ 高级工程师**手动标注 **1,505 个真实问题** |
| 关键指标 | F1 / Precision / Recall / Avg Time / Avg Token |

### 关键对比（同模型下）

| 指标 | 通用 Agent（Claude Code + Skills） | OCR 混合架构 |
|---|---|---|
| **Precision** | 较低 | **显著更高** |
| **F1** | 较低 | **显著更高** |
| **Avg Token** | 1× | **~1/9** |
| **Avg Time** | 较慢 | **更快** |
| **Recall** | 较高 | **故意较低**（换 precision） |

> **核心论断**："Compared to general-purpose agents (Claude Code), Open Code Review achieves significantly higher Precision and F1 with the same underlying model, while consuming **only ~1/9 of the tokens** and completing reviews faster."

## 四、支持的规则 + 集成方式

### 4.1 内置规则集

- **NPE**（空指针异常，Java/Kotlin）
- **Thread-safety**（线程安全）
- **XSS**（跨站脚本）
- **SQL injection**（SQL 注入）

### 4.2 支持的编程语言（10+）

Java / TypeScript / Go / Python / Kotlin / C++ / C / ...

### 4.3 集成方式

| 类型 | 工具 |
|---|---|
| **CI/CD** | GitHub Actions / GitLab CI / GitFlic / Gerrit |
| **Coding Agent 插件** | Claude Code / Codex / Cursor / OpenCode / Skill-compatible agents |
| **MCP Server** | `npx @opencodereview/mcp-server` |
| **可观测性** | OpenTelemetry |
| **会话回放** | Session Viewer（浏览器中回放 review 会话） |

### 4.4 两种 review 模式

| 模式 | 说明 |
|---|---|
| **Default（OCR-managed）** | OCR 自己跑 review，用它配置的 LLM |
| **Delegation Mode** | 让你的 coding agent（Claude Code / Codex）跑 review，**不需要 OCR 配 LLM** |

Delegation Mode 是关键卖点：**OCR 负责文件选择 + 规则解析，你自己的 agent 负责推理**——最大化利用用户已有的模型订阅。

## 五、CLI 速览

```bash
# 安装
npm install -g @alibaba-group/open-code-review

# 配置 LLM
ocr config provider    # 选择供应商
ocr config model       # 选择模型

# Workspace 模式：review 所有 staged/unstaged/untracked 改动
ocr review

# Branch 范围：比较两个引用
ocr review --from main --to feature-branch

# 单个 commit
ocr review --commit abc123

# 恢复中断的 review
ocr session list
ocr review --from main --to feature-branch --resume <session-id>

# 全文件扫描（无需 git 历史）
ocr scan                          # 整个仓库
ocr scan --path internal/agent    # 指定目录/文件

# Delegation 模式
ocr delegate preview
ocr delegate rule src/main.go src/handler.go
```

## 六、跟何大人研究的强对照

### 6.1 跟今天 5 个研究的串联（最有价值的部分）

| 时段 | 内容 | 在企业 AI 平台里的位置 |
|---|---|---|
| 早上 | **SaaS 企业知识库全景** | 概念层：4 层架构 |
| 中午 | **Harness Handbook**（Tencent Hunyuan） | 工程层：行为定位 + BGPD + resync |
| 下午 1 | **OKF 三段式**（AI云枢） | 格式层：多种来源 → OKF → 多种消费者 |
| 下午 2 | **Palantir AIP 12 模块** | 产品层：企业级 AI 平台完整蓝图 |
| **晚上（本项目）** | **OpenCodeReview 混合架构** | **执行层：怎么让 AI 审查代码** |

**6 个研究叠加** = **概念 + 工程 + 格式 + 产品 + 执行**的完整叙事。

### 6.2 跟 Harness Handbook 的对偶关系

| | Harness Handbook | OpenCodeReview |
|---|---|---|
| **问题** | 代码改哪里？ | 代码改得对不对？ |
| **输入** | 自然语言改动请求 | Git diff / 文件变更 |
| **输出** | verbatim EDIT plan | 结构化行级审查意见 |
| **角色** | **planner**（定位 + 方案） | **reviewer**（审查 + 评判） |
| **架构** | LLM + handbook 导航 | **工程确定性 + LLM agent** |
| **关键创新** | BGPD 渐进披露 | **模板引擎规则 + 外部定位模块** |

**两者是互补关系**：
- Harness Handbook → agent 知道**改哪里**
- OpenCodeReview → agent 知道**改的对不对**
- 合起来 = **planner + reviewer** 的完整闭环

### 6.3 跟 Palantir AIP 模块 06（安全与治理）的对标

| Palantir 模块 | OCR 对应 | 共同思路 |
|---|---|---|
| 06 安全与治理：审批 / 检查点 | "关键环节仍需人工确认" | **AI 不取代人决策** |
| 04 本体层（Ontology） | 内置规则集（NPE / XSS / SQL 注入） | **领域知识沉淀为规则** |

OCR 把"AI 审查 + 人类确认"做成**默认工作流**——这跟 Palantir 的"治理层"思路完全一致。

### 6.4 跟何大人平安 14 年经验的关联

OCR 的"混合架构"不是新概念——这是软件工程几十年的老问题：
- **静态分析工具**（SonarQube / ESLint）= OCR 的 Deterministic Engineering
- **AI Agent** = OCR 的 LLM Agent 部分
- **PR review** = OCR 的"关键环节仍需人工确认"

何大人 14 年交付经验里，**"工程确定性 vs AI 灵活性"**是反复出现的张力：
- 金融科技：合规规则不能错（确定性）
- 政务数字化：流程必须可追溯（确定性）
- 智慧城市：实时决策需要灵活性（灵活性）

**OCR 把这个老问题用新工具重新回答了——这就是"工程实践 + AI"的范式升级**。

## 七、可能的延伸应用（按 7-8 偏好不强挂钩）

### 7.1 自身工程实践（直接相关）

何大人的 `/root/AgentSpace` 已经跑 OpenClaw / Claude / Codex / Hermes 5 个 harness。**OCR Delegation Mode** 可以直接接入：

```bash
# 在 vault 里安装 OCR
npm install -g @alibaba-group/open-code-review

# 在 AgentSpace 配置：让 Hermes / Codex 自己跑 review
ocr delegate preview
```

**预期收益**：跟现在的 Hermes dispatcher 配合，**改动后自动 OCR 审查**——把"代码改动"做成可审查、可回放、可审计的工作流。

### 7.2 德勤 MVP（间接挂钩，按 6-29 决策）

德勤模块 07「智能体生命周期」缺"评估套件"——OCR 的混合架构正好填这个：

| 德勤模块 | OCR 借鉴 |
|---|---|
| 07 智能体生命周期 - 评估套件 | **OCR 的 benchmark 思路**：50 仓库 + 200 PR + 80 工程师标注 |
| 06 安全与治理 - 审批/检查点 | **OCR 的"关键环节仍需人工确认"** |
| 11 打包发布部署 | **OCR 的 deterministic pipeline**：发布流程不能错 |

**核心借鉴点**：德勤的 agent 不应该"全靠 LLM"，应该**借鉴 OCR 的分工思路**：
- 工程确定性 = 业务规则引擎、合规检查、权限校验
- LLM 灵活性 = 自然语言推理、内容生成、动态决策

### 7.3 求职差异化（按 6-30 决策）

德勤面试若问"你怎么看 AI 代码审查"或"你怎么设计智能体评估"：

1. **展示 OCR 的 benchmark 数字**：Precision / F1 / Token 1/9 / Time
2. **强调"用 recall 换 precision"的工程取舍**——这是产品定位不是技术缺陷
3. **引用 Palantir 治理层 + OCR 人类 in the loop**：AI 不取代人决策
4. **引用何大人平安 14 年经验**：工程确定性 vs AI 灵活性 是反复出现的张力

→ 体现"**工程判断 + 产品定位 + AI 落地**"的三层思维。

### 7.4 vault OKF 体系（弱挂钩）

OCR 的**模板引擎规则匹配**思路可以借鉴到 OKF schema：
- OKF schema 文档 = "模板引擎"（确定性）
- Datacore 自动提取 = "LLM 灵活判断"
- 两者结合 = "**确定字段校验 + 灵活语义提取**"

## 八、立即可做的下一步（建议清单）

1. **本地试用**：
   ```bash
   npm install -g @alibaba-group/open-code-review
   cd /root/AgentSpace && ocr scan --path executor/    # 审查 AgentSpace 的 executor 目录
   ```

2. **跟 Harness Handbook 配对使用**：
   - 用 Harness Handbook 的 BGPD 做代码改动规划
   - 用 OCR 做改动后审查
   - 在 vault 里写一份 `2026-07-31 - planner+reviewer 闭环工作流.md`

3. **德勤项目里加借鉴笔记**：
   - `/root/vault/1-Projects/德勤/AI-Native/2026-07-30 - 模块07智能体评估套件-OCR借鉴.md`
   - 把 OCR 的 50 仓库 + 200 PR benchmark 思路落到德勤 MVP

4. **写一份合并讲稿**：
   - `/root/vault/2-Areas/AI-Agent-研究/2026-07-31 - 6图叠加-企业AI平台完整叙事.md`
   - 把今天所有研究合成对外讲稿（德勤面试/客户提案用）

## 九、引用

```bibtex
@misc{alibaba2026opencodereview,
  title={Open Code Review: An AI-Powered Code Review CLI Tool with 
         Hybrid Architecture},
  author={Alibaba Group},
  year={2026},
  url={https://github.com/alibaba/open-code-review},
  note={Apache-2.0, Battle-tested at Alibaba's scale}
}
```

---

**核心 takeaway 写给何大人（人话版）**：

> 这不是"又一个 AI 审查工具"，是**"工程确定性 + AI 灵活性"混合架构**的范式——把"不能错"的环节（文件选择 / 规则匹配 / 位置定位）用工程逻辑保证，把"需要灵活判断"的环节用 LLM 处理。**结果**：同等模型下精度/F1 显著更高，token 仅 1/9，速度更快。
>
> **跟 Harness Handbook 配对用**：Harness Handbook 告诉你"改哪里"，OCR 告诉你"改的对不对"——**planner + reviewer 完整闭环**。
>
> **跟 Palantir 治理层思路一致**：AI 不取代人决策，关键环节保留人工确认。
>
> **跟何大人平安 14 年经验同源**："工程确定性 vs AI 灵活性"不是新问题，是软件工程老问题——OCR 用新工具重新回答了。