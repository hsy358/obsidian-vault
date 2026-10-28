---
title: "Anthropic Knowledge Work Plugins：AI Native 组织 Workspace 的官方对标物"
type: document
source: video
file_type: md
file_path: /root/vault/2-Areas/AI-Agent-研究/2026-10-28 - Anthropic Knowledge Work Plugins - AI Native 组织 Workspace 对标分析.md
uploaded_date: 2026-10-28
title_short: "Knowledge Work Plugins 分析"
description: "Anthropic 官方 Claude Cowork 插件生态全面拆解：123 个插件、252 个 skill、插件规范（渐进披露/触发语/~~占位符/tool-agnostic）、三模式定制 SOP，以及对德勤 AI Native 组织 Workspace MVP 的直接映射"
size_bytes: 0
tags:
  - anthropic
  - claude-cowork
  - claude-code
  - plugin
  - skill
  - mcp
  - ai-native
  - agent-platform
  - workplace-workspace
  - research
related:
  - "2-Areas/AI-Agent-研究/2026-10-28 - SolidCraft - 纯 Rust 参数化 3D CAD 与 MCP Agent 接入.md"
  - "2-Areas/AI-Agent-研究/2026-10-28 - DeepSeek Harness + DS Bot - 架构分析与德勤项目借鉴点.md"
  - "1-Projects/求职-德勤/README.md"
source_note: "何大人提供（github.com/anthropics/knowledge-work-plugins），2026-10-28"
---

# Anthropic Knowledge Work Plugins —— AI Native 组织 Workspace 的官方对标物

> **何大人提供**：`github.com/anthropics/knowledge-work-plugins`（可直接搜仓库名）
> **已克隆到本机**：`/root/kw-plugins`（6.7 MB）
> **判断**：⭐⭐⭐ **这是德勤「AI Native 组织 Workspace / Agent 智能体平台」目标最直接的对标物** —— Anthropic 官方给出了这个命题的参考答案。

---

## 一、核实数据（GitHub API + 本地克隆，2026-10-28）

| 项 | 值 |
|---|---|
| 仓库 | `anthropics/knowledge-work-plugins` |
| 描述 | Open source repository of plugins primarily intended for knowledge workers to use in Claude Cowork |
| **Stars** | **33,569** |
| Forks | 3,687 |
| Open issues | 153 |
| **License** | **Apache-2.0**（可自由克隆商用）|
| 语言 | Python（主体是 **Markdown + JSON**）|
| 创建 | 2026-01-23 |
| 最近推送 | 2026-10-28（当天）|
| 仓库体积 | 6.7 MB |
| 订阅者 | 203 |

### 仓库内容体量
```
marketplace 注册插件总数 : 123
  ├─ 本仓库内置          :  22
  └─ 外部 partner 插件   : 101   ← 生态开放
SKILL.md 总数           : 252
agents/*.md             :   5
commands/*.md (legacy)  :  15
.mcp.json               :  21
hooks.json              :   0（内置插件没用 hooks）
```

### 分类分布（123 个插件）
```
productivity 31 | development 15 | finance 11 | monitoring 8 | security 5
database 4 | design 4 | deployment 4 | automation 3 | learning 1 | ...
```

### 内置的 22 个插件
```
bio-research        customer-support   data                 design
engineering         enterprise-search  finance              human-resources
legal               marketing          operations           pdf-viewer
productivity        product-management sales                small-business
cowork-plugin-management
```

---

## 二、核心范式：**插件 = 纯文件**

```
plugin-name/
├── .claude-plugin/plugin.json   # 清单（唯一必需）
├── .mcp.json                    # MCP 连接器（外部工具）
├── skills/                      # 领域知识（Agent 自动触发）
│   └── skill-name/
│       ├── SKILL.md             # 核心知识
│       └── references/          # 按需加载的详参
├── agents/                      # 子 Agent 定义（.md）
├── commands/                    # 旧版 slash command（legacy）
├── hooks/hooks.json             # 生命周期钩子
├── CONNECTORS.md                # 连接器说明
├── README.md
└── LICENSE
```

> **README 原话**：
> "Every component is file-based — **markdown and JSON, no code, no infrastructure, no build steps**."

### ⭐ 为什么这条对德勤最关键

德勤交付金融/政务客户，**客户的安全团队必须能审计 Agent 的行为**。"纯文件、无代码、无构建"意味着：
- 交付物可版本化、可 diff、可 code review
- 客户可以直接读 markdown 就能知道 Agent 会做什么
- 换模型/换运行时**不需要重写**，只换执行器

这跟德勤 6-29 定的「Hermes v0.14 为唯一 Agent 框架」是**互补而非冲突** —— 框架层是 Hermes，**知识层是这些纯文件**。

---

## 三、Skill 规范（⭐ 最值得直接抄的部分）

### 1. 三层渐进披露（控制 context 成本）
| 层 | 内容 | 何时进入 context |
|---|---|---|
| **1. Metadata** | name + description（约 100 词）| **永远常驻** |
| **2. SKILL.md 正文** | 核心知识（< 5k 词，建议 1.5k–2k）| skill 触发时 |
| **3. Bundled resources** | references / examples / scripts（不限）| 按需 |

### 2. frontmatter 规范
```yaml
---
name: api-design              # 必填，kebab-case，与目录名一致
description: >                # 必填，第三人称 + 引号包裹的触发短语
  This skill should be used when the user asks to "design an API",
  "create API endpoints", "review API structure", or needs guidance
  on REST API best practices...
metadata:                      # 可选，任意键值
  version: "0.1.0"
---
```
> **description 的写法是灵魂**：不是描述"这个 skill 是什么"，而是描述"**什么时候该用我**"，并把用户可能的说法用引号列出来。→ Agent 靠这个学会何时加载自己。

### 3. 正文写作风格
- **frontmatter**：第三人称（"This skill should be used when..."）
- **正文**：命令式/不定式（"Parse the config file"，不是 "You should parse the config file"）
- **长度**：SKILL.md 正文 **< 3000 词**（理想 1500–2000），详细内容移到 `references/`

### 4. 一个真实例子（finance / journal-entry）
```markdown
---
name: journal-entry
description: Prepare journal entries with proper debits, credits, and supporting detail.
  Use when booking month-end accruals (AP, payroll, prepaid), recording depreciation
  or amortization, posting revenue recognition or deferred revenue adjustments,
  or documenting an entry for audit review.
argument-hint: "<entry type> [period]"
---

# Journal Entry Preparation

> If you see unfamiliar placeholders or need to check which tools are connected,
  see [CONNECTORS.md](../../CONNECTORS.md).

**Important**: This command assists with journal entry workflows but does not provide
financial advice. All entries should be reviewed by qualified financial professionals
before posting.
```
正文结构 = 编号工作流（1. 收集源数据 → 2. 计算分录 → …），且**每个工作流步骤都写明"连接器没连上时的降级路径"**：
> "If no data source is connected: Connect ~~erp or ~~data warehouse to pull GL data automatically. You can also paste trial balance data or upload a spreadsheet."

---

## 四、⭐ `~~占位符` + tool-agnostic（最巧妙的设计）

### 占位符语法
技能里用 **`~~category`** 表示"这一类工具"，而不是具体产品：
```
~~data warehouse  →  Snowflake / BigQuery / Databricks / Redshift 都行
~~chat            →  Slack / Teams 都行
~~erp             →  NetSuite / SAP / QuickBooks 都行
~~project tracker →  Jira / Linear / Asana 都行
~~email / ~~office suite / ~~analytics
```
`CONNECTORS.md` 里给出对照表：
| Category | Placeholder | Included servers | Other options |
|---|---|---|---|
| Data warehouse | `~~data warehouse` | Snowflake\*, Databricks\*, BigQuery | Redshift, PostgreSQL |
| ERP / Accounting | `~~erp` | —（暂无支持的 MCP server）| NetSuite, SAP, QuickBooks, Xero |
| Analytics / BI | `~~analytics` | —（暂无）| Tableau, Looker, Power BI |

> **⭐ 这就是德勤交付规模化���关键**：
> **技能按"能力类别"写，客户换技术栈只改 `.mcp.json`，一个字的 skill 都不用动。**
> 一个金融行业技能包可以同时卖给用 Snowflake 的和用 Databricks 的客户。

### `.mcp.json` 形态（stdio + streamable http）
```json
{
  "mcpServers": {
    "bigquery": { "type": "http", "url": "https://bigquery.googleapis.com/mcp" },
    "slack": {
      "type": "http",
      "url": "https://mcp.slack.com/mcp",
      "oauth": { "clientId": "1601185624273.8899143856786", "callbackPort": 3118 }
    }
  }
}
```

---

## 五、⭐⭐ `cowork-plugin-management` —— 企业落地的元方法论

这是整个仓库**对德勤最有商业价值**的部分。它是"如何把通用插件变成客户专属插件"的标准作业流程。

### 两个 skill
| Skill | 作用 |
|---|---|
| `create-cowork-plugin` | 从零造一个新插件（5 阶段）|
| `cowork-plugin-customizer` | **把现有插件改成某家组织的**（定制流程）|

### 定制模式自动判别（三种）
| 模式 | 判别依据 | 动作 |
|---|---|---|
| **1. 通用插件初始化** | 存在 `~~` 占位符 | 全量替换占位符（`~~Jira`→`Asana`、`~~your-team-channel`→`#engineering`）|
| **2. 局部定制** | 无 `~~` 占位符 + 用户指定了某个部分 | 只改那部分，不全盘扫描 |
| **3. 通用性改造** | 无 `~~` 占位符 + 用户想大改 | 先问用户想改什么 |

判别命令：`grep -rn '~~\w' /path/to/plugin --include='*.md' --include='*.json'`

### 四阶段定制流程
```
Phase 0  收集用户意图（区分 scoped / general；用户已给上下文就直接用，不重复问）
Phase 1  从知识 MCP 拉公司上下文（chat/Slack MCP、文档 MCP、邮件 MCP）
           → 工具名、流程、团队惯例、配置值（workspace ID、项目名、团队标识）
Phase 2  生成变更清单（用"业务语言"，不用技术语言）
Phase 3  逐项落地
```

### ⭐ 五条"金句"（应该直接进德勤的交付规范）
1. **"Never assume 'industry standard' defaults are correct"** —— 行业标准默认值不能想当然，每个细节都要问客户
2. **"Never change the name of the plugin or skill"** —— 定制不动名字（保证可追溯）
3. **"Nontechnical output"** —— 面向用户的输出必须是业务语言，**绝不暴露 `~~` 占位符、文件路径、schema 字段**
4. **"AskUserQuestion always includes a Skip button"** —— 允许用户跳过
5. **`compatibility` 字段** —— skill 可声明环境要求（如"需要 Cowork 桌面端"），不满足就中止并给出明确说明

### create-cowork-plugin 的 5 阶段
```
1. Discovery（发现需求）
2. Component Planning（决定需要哪些组件类型）
3. Design & Clarifying Questions（逐个组件定细节）
4. Implementation（生成所有文件）
5. Review & Packaging（交付 .plugin 文件）
```

### 组件规范速查
| 组件 | 位置 | 必填字段 |
|---|---|---|
| Manifest | `.claude-plugin/plugin.json` | `name`（kebab-case）；`version`（semver，起 0.1.0）；`description`；`author.name` |
| Skill | `skills/<name>/SKILL.md` | frontmatter: `name`、`description`（第三人称+触发短语）|
| Agent | `agents/<name>.md` | `name`（3–50 字符，kebab-case）、`description`（含 `<example>` 块）、`model`（inherit/sonnet/opus/haiku）、`color`（blue/cyan/green/yellow/magenta/red）、可选 `tools` 限定 |
| Hooks | `hooks/hooks.json` | 事件：PreToolUse / PostToolUse / Stop / SubagentStop / SessionStart / SessionEnd / UserPromptSubmit / PreCompact / Notification |
| MCP | `.mcp.json` | stdio / streamable http |

### Hook 机制
```json
{ "type": "prompt", "prompt": "Evaluate whether this file write follows project conventions: $TOOL_INPUT", "timeout": 30 }
{ "type": "command", "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.sh", "timeout": 60 }
```
命令式 hook 输出：`{"decision":"block","reason":"..."}`，可选 `approve` / `block` / `ask_user`。

### Agent 的颜色语义
蓝青=分析评审 / 绿=成功向 / 黄=谨慎校验 / 红=关键安全 / 品红=创意生成

---

## 六、合规模式（德勤金融客户必需）

**14 个 skill 带免责条款**，模式统一：
> **"This skill assists with ... but does not provide financial advice. All entries should be reviewed by qualified financial professionals before posting."**

legal 插件还把它写进**输出规范**：
> "**Close with the attorney-review line** — a final bullet saying this is a business read, not legal advice, and naming which specific flags are worth an attorney's hour before signing. **Every summary ends this way, including clean ones.**"

> ⭐ **"including clean ones"** —— 即使没问题也必须留这句。这是把"AI 不背锅、但流程留痕"写进了 skill 本身。

---

## 七、对德勤项目的映射

### 7.1 概念映射
| Anthropic | 德勤 AI Native MVP |
|---|---|
| Plugin（插件）| **行业交付包**（金融 / 政务 / 医疗 …）|
| `skills/*/SKILL.md` | 我们的 Skill 提示词开发（赛力斯 JD 那条能力）|
| `.mcp.json` | **ExecutorAdapter 的 MCP 侧适配**（接客户已有系统）|
| `agents/*.md` | 专业子 Agent（对应 Hermes 的角色）|
| `hooks/hooks.json` | 审批与审计钩子（德勤交付必备）|
| `marketplace.json` | **插件注册中心 / 资产目录** |
| `cowork-plugin-customizer` | **客户定制 SOP** ← 收费点所在 |

### 7.2 战略判断（这才是最重要的）
> **Anthropic 正在把"Agent 平台"从「框架竞争」推向「文件生态竞争」。**

这意味着德勤的竞争维度不是"用哪个 Agent 框架"（6-29 定的 Hermes 不变），而是：
1. **行业知识包的深度** —— 我能不能比 Anthropic 的通用 finance 包更懂中国金融客户的实际流程？
2. **落地产出的能力** —— 通用包 + 客户定制流程 = 可规模化的交付物
3. **合规与审计就绪** —— 纯文件 + 免责条款 + 钩子留痕

**而且这个仓库恰好证明了「通用行业包 → 客户定制」这条商业路径是成立的**（Anthropic 自己就是这么做的，123 个插件、101 个外部伙伴）。

### 7.3 可直接复用的资产
| 资产 | 数量 | 怎么用 |
|---|---|---|
| 通用行业 skill | 252 个 | **参考范本**，不是直接交付（要按 7.1 的映射改写 + 中国化）|
| 插件规范文档 | component-schemas.md | **直接抄成德勤的插件编写规范** |
| 定制 SOP | cowork-plugin-customizer | **直接抄成德勤的客户定制流程** |
| CONNECTORS.md 模式 | 21 个 | 抄结构，换成客户的系统清单 |
| 免责条款模式 | 14 处 | 抄 |

---

## 八、局限与风险

| # | 风险 | 说明 |
|---|---|---|
| 1 | **格式是 Anthropic 专有的** | Claude Code plugin format（含 `${CLAUDE_PLUGIN_ROOT}`），不能直接跑在 Hermes/OpenClaw 上。但 skills 本质是 **markdown + frontmatter** → 转换成本低 |
| 2 | **官方插件是"通用起点"** | README 明说 "These plugins are generic starting points" —— **必须做客户定制才有用**。这既是风险（交付工作量）也是机会（德勤的收费点）|
| 3 | **内容是 Anthropic 内部工作流沉淀** | 有 IP / 保密考量，**不要原样打包进交付物**。当作参考范本 |
| 4 | **partner-built 成熟度参差** | 101 个外部插件，765 个文件，质量不一，需甄别 |
| 5 | **无 hooks 实例** | 内置 22 个插件的 `hooks.json` 数量为 0 → hooks 规范有文档但没范例 |
| 6 | **agents 仅 5 个** | 子 Agent 规范文档完善但实例少 |
| 7 | **Python 语言占比高** | 主体是 Markdown+JSON，Python 部分在 partner 插件里 |

---

## 九、待办

- [ ] **重点精读 `sales`（41 文件）和 `small-business`（214 文件）** —— 最大的两个，可能藏着更多模式
- [ ] 把 `component-schemas.md` 提炼成**德勤版插件编写规范**
- [ ] 把 `cowork-plugin-customizer` 的四阶段流程提炼成**德勤客户定制 SOP**
- [ ] 评估：能否把 `~~category` 占位符机制 + 渐进披露**移植到德勤的 Skill/ExecutorAdapter 设计**
- [ ] 对照赛力斯 JD 的"配置驱动的 Tool 动态 Schema 注册"，看 Anthropic 这套是不是另一种解法
- [ ] 找一个德勤真实金融/政务客户场景，用 `finance` 插件走一遍定制流程做原型

---

*记录人：小助 ｜ 2026-10-28 ｜ 数据源：GitHub API + 本地克隆 `/root/kw-plugins`（HEAD `2574e29`）*
