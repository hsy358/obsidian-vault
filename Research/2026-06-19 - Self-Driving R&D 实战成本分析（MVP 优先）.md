# Self-Driving R&D · 实战成本分析（v4.2 冷静版）

> **核心问题**：v4.2 是不是"大杂烩"？从 1 行需求到落地，是否太复杂？token 消耗如何？实战可行吗？
> **立场**：诚实回答——v4.2 是"完整愿景"，**不是"立即可执行"**。需要拆解。
> **更新日期**：2026-06-19

---

## 一、坦白：v4.2 确实存在 5 个实战问题

| 问题 | 具体表现 | 后果 |
|------|---------|------|
| **概念过载** | Org Chart / Goal Ancestry / Heartbeat / Memento Man / Action Schema / MCP / ACP / Plugin / Template / DAG / 3 上下文模式 / review_loop... 30+ 概念 | **新成员看一周才能搞懂** |
| **配置成本高** | 写一个 8 阶段 workflow ≈ 200 行 YAML | **小项目配置时间 > 实际开发时间** |
| **token 消耗大** | 每个 agent 启动要加载 heartbeat checklist + ParaMemory + project state | **每个 session 起手 5-20k tokens 浪费** |
| **依赖复杂** | 需 Python + Node + React + SQLite + MCP servers + 各种 plugin | **部署要搞半天** |
| **过度抽象** | Action Schema 强制约束，但实际 80% agent 输出是自然语言 | **形式主义成本** |

**何大人原话警告**：**"会不会是大杂烩？正常给需求到落地会不会太复杂？"**——这是非常务实的质问。

---

## 二、用真实数字说话：v4.2 的"成本账"

### 2.1 Token 消耗估算

**单个 8 阶段项目（做一个简单的 Web App）**：

| 阶段 | 输入 token | 输出 token | 累计 |
|------|----------|----------|------|
| Memento Man 注入（4 个 agent × 启动） | 4 × 8k = 32k | - | 32k |
| Heartbeat checklist 加载 | 5k × 4 = 20k | - | 52k |
| ParaMemory 读取 | 3k × 4 = 12k | - | 64k |
| access 阶段 | 15k | 8k | 87k |
| explore 阶段（3 个并行） | 30k | 25k | 142k |
| propose 阶段 | 20k | 15k | 177k |
| task 阶段 | 10k | 5k | 192k |
| apply 阶段（review_loop 5 次） | 150k | 100k | 442k |
| verify 阶段（3 个并行） | 60k | 30k | 532k |
| review 阶段 | 30k | 20k | 582k |
| archive 阶段 | 10k | 5k | 597k |
| Action Schema 校验失败重试（~3 次）| 30k | 15k | 642k |
| **总计** | | | **~640k tokens** |

**按 MiniMax M3 0.84/1M output 计算**：
- Input: ~430k × 0.21/1M = 0.09 美元
- Output: ~210k × 0.84/1M = 0.18 美元
- **单个项目约 0.27 美元 ≈ 2 元 RMB**

**按时间估算**：
- access-execute 阶段：~1-3 分钟
- explore（并行）：~2-4 分钟
- propose：~2-3 分钟
- apply（含 review_loop）：~10-30 分钟（重头戏）
- verify：~3-5 分钟
- review：~3-5 分钟
- archive：~1-2 分钟
- **总时长：~25-55 分钟**

**对比纯人工**：
- 类似项目人工开发：2-8 小时
- v4.2 自动跑：25-55 分钟（**加速 2-15 倍**）

### 2.2 配置成本估算

**首次配置 v4.2**：
- 后端核心：~30 人天
- 前端 React：~10 人天
- 写 10 个核心 skill：~15 人天
- 测试：~10 人天
- 文档：~5 人天
- **总计：~70 人天 ≈ 3-4 个月（1 人）或 1 个月（3 人团队）**

**每次新加项目的配置成本**：
- 写 spec：~15 分钟
- 写 workflow YAML：~30 分钟
- 配置 agent：~10 分钟
- 配置 skill：~20 分钟
- **总计：~75 分钟/项目**

**对比纯手工**：
- 写 spec + plan：~30 分钟
- 写代码：~2-8 小时
- 测试：~30 分钟
- 文档：~30 分钟
- **总计：~3.5-10 小时/项目**

**v4.2 的总成本（含配置）**: 75 分钟配置 + 30 分钟运行 = **~2 小时**
**纯手工**: ~3.5-10 小时

**结论**：v4.2 只在**长期 + 多项目**场景下才划算。**单个小项目是亏的**。

---

## 三、复杂度分层架构：Lite / Standard / Pro

**核心思想**：v4.2 是 Pro 版，但 80% 的需求根本不需要 Pro。

```
┌──────────────────────────────────────────────────────────┐
│  Pro (v4.2 全功能)                                        │
│  - 适合：长期 R&D 平台 / 多项目并行 / 团队级协作          │
│  - 配置：~70 人天首次 + ~75 分钟/项目                     │
│  - token：~640k/项目                                     │
│  - 价值：跨项目复用 + 自改进                              │
│  ──────────────────────────────────────────────────────── │
│  Standard (v4.1 简化版)                                  │
│  - 适合：单个中等项目 / 个人开发者                        │
│  - 配置：~10 人天首次 + ~20 分钟/项目                     │
│  - token：~150k/项目                                     │
│  - 价值：自动化 8 阶段流程 + 状态机可跳转                │
│  ──────────────────────────────────────────────────────── │
│  Lite (MVP，2 周可上线)                                  │
│  - 适合：一次性任务 / 简单工具 / 验证想法                  │
│  - 配置：~2 人天 + 0 分钟/项目（直接用）                 │
│  - token：~30k/项目                                      │
│  - 价值：流程跑通即可，无花架子                          │
└──────────────────────────────────────────────────────────┘
```

### 3.1 Lite 版（推荐先做这个）

**核心理念**：**8 阶段是 Lite 的"配置项"，但默认只跑 3 阶段**。

```yaml
# workflows/lite-default.yaml
workflow:
  name: lite-default
  version: "1.0.0"
  
  # Lite 默认只跑这 3 个阶段
  stages:
    access:
      agent: pm
      timeout: 180
      # 极简：不加载 heartbeat / ParaMemory / Org Chart
    apply:
      agent: engineer
      timeout: 1800
      # 内部用 single ReAct loop
    verify:
      agent: qa
      timeout: 600
  
  safety:
    max_iterations: 30
    wall_clock_timeout_minutes: 60
```

**Lite 版砍掉的东西**：
- ❌ Org Chart（不需要，单一 agent）
- ❌ Heartbeat 队列（用单次调用即可）
- ❌ Memento Man（session 不跨天）
- ❌ Goal Ancestry（单项目用不到）
- ❌ Plugin（skill 直接 import）
- ❌ Template（YAML 复用就行）
- ❌ Action Schema（自由文本够了）
- ❌ MCP（先把核心跑通）

**Lite 版保留的东西**：
- ✅ YAML workflow（简单 + git 友好）
- ✅ 状态机（防止状态乱）
- ✅ 5 层裁决（保证基本质量）
- ✅ 3 上下文模式（last_only 为主）
- ✅ 错误恢复 3 档（避免跑飞）
- ✅ 审计日志（事后可追）

**Lite 版的 Token 消耗**：

| 阶段 | token | 备注 |
|------|------|------|
| 启动开销 | 3k | 没有 heartbeat / ParaMemory |
| access | 10k | LLM 解析需求 |
| apply（含 review_loop 2 次）| 30k | 实际写代码 |
| verify | 8k | 跑测试 |
| Action Schema 重试 | 5k | 偶尔 1 次 |
| **总计** | **~56k tokens** | 约 0.05 元 RMB |

**Lite 版的配置成本**：
- 后端核心：~5 人天
- 写 3-5 个核心 skill：~3 人天
- 前端（可选）：~3 人天
- **总计：~10 人天 ≈ 2 周（1 人）**

### 3.2 Standard 版（Lite + 必要扩展）

**适合**：个人开发者，做的项目都是中等复杂度（5-20 个文件）

**在 Lite 基础上加**：
- ✅ Org Chart（2-3 个 agent）
- ✅ Heartbeat（必要的 8 阶段）
- ✅ 简单的 Action Schema（关键 action）
- ✅ ParaMemory（基本记忆）
- ❌ 不加 MCP / Plugin / Template / Goal Ancestry / Memento Man

**Token 消耗**：~150-300k/项目
**配置成本**：~30 人天

### 3.3 Pro 版（v4.2 全功能）

**适合**：企业级 / 团队级 / 长期 R&D 平台
**只在前两个版本稳定后再考虑**。

---

## 四、改造方案：把 v4.2 拆成 3 个版本

### 4.1 v5.0-lite（MVP，2 周可上线）

**目标**：**先跑通**，不追求完美。

```python
# v5.0-lite 目录结构
selfdriving-lite/
├── workflow.yaml           # 8 阶段，但默认 3 阶段
├── config.yaml            # 简化版（只配模型 + 通知）
├── selfdriving/
│   ├── __init__.py
│   ├── engine.py          # YAML 解析 + Jinja2 路由（~200 行）
│   ├── state.py           # SQLite + YAML（~300 行）
│   ├── llm.py             # 模型适配层（~150 行）
│   ├── skills.py          # Skill 调用（~200 行）
│   ├── decision.py        # 5 层裁决（~200 行）
│   └── self_correct.py    # 错误恢复 3 档（~150 行）
├── skills/
│   ├── web_search.py      # 必装
│   ├── code_generator.py  # 必装
│   ├── test_runner.py     # 必装
│   └── README.md
├── examples/
│   └── hello-world.yaml   # 一个完整 demo
└── README.md
```

**核心代码量估计**：
- engine.py: 200 行
- state.py: 300 行
- llm.py: 150 行
- skills.py: 200 行
- decision.py: 200 行
- self_correct.py: 150 行
- **总计：~1200 行 Python**

**2 周可完成**（前提：模型适配层复用现有的）。

### 4.2 v5.1-standard（Lite + 8 阶段，6 周）

**在 Lite 基础上加**：
- 完整 8 阶段 workflow 模板
- 简单的 Org Chart（2-3 agent）
- Heartbeat 单机版（不要求 DB 队列）
- ParaMemory 基础版
- Action Schema 关键 5 个 action

### 4.3 v5.2-pro（v4.2 全功能，3-4 月）

**包含所有 Pro 特性**：ACP / MCP / Plugin / Template / Goal Ancestry / Memento Man / 完整 Heartbeat 队列 / 公司模板市场

**只在 v5.1 稳定后再投入**。

---

## 五、实战建议：3 步走

### 步骤 1：先做 Lite MVP（**最重要**）

```bash
# 1. 1 天内写好 workflow.yaml
# 2. 3 天内写好 5 个核心模块
# 3. 1 天写 hello-world 例子
# 4. 用 1-2 周真实项目验证
```

**验证标准**：
- 跑通 1 个真实小项目（如：写个 CLI 工具）
- 每个项目 < 5 分钟人工介入
- token 消耗 < 100k

**这一步的目标是验证假设**，不是完成所有功能。

### 步骤 2：根据实际使用情况决定

**如果 Lite 已经够用 → 停在这里**
- 80% 的 R&D 任务都是小项目，Lite 足够
- **不要为了用 v4.2 而制造需求**

**如果 Lite 不够 → 升级到 Standard**
- 加 8 阶段
- 加 2-3 个 agent
- 加 Heartbeat（简单版）

**如果 Standard 也不够 → 才考虑 Pro**
- 这时候你已经有 6 个月实战数据
- 知道哪些功能真的需要
- 知道 v4.2 哪些设计是过度工程

### 步骤 3：边用边演进（不是先设计后实现）

**关键原则**：
- **MVP 优先**：先把 1 个项目跑通
- **实测驱动**：根据真实瓶颈加功能
- **拒绝过度抽象**：每加一个概念都要问"它解决了什么问题"
- **保持可降级**：随时能从 Pro 退到 Standard 再退到 Lite

---

## 六、v4.2 → v5.0 的取舍清单

| 特性 | v4.2 有 | v5.0-lite 是否要 | 理由 |
|------|---------|------------------|------|
| YAML workflow | ✅ | ✅ 必装 | 简单 + git 友好 |
| 状态机可跳转 | ✅ | ✅ 必装 | 防状态乱 |
| 5 层裁决 | ✅ | ✅ 必装 | 质量底线 |
| 3 上下文模式 | ✅ | ✅ 必装 | 节省 token |
| 错误恢复 3 档 | ✅ | ✅ 必装 | 防止跑飞 |
| SQLite 状态 | ✅ | ✅ 必装 | 事务保证 |
| OpenTelemetry | ✅ | ❌ 暂时不要 | Lite 不需要 |
| **Org Chart** | ✅ | ❌ 不要 | 单 agent 够用 |
| **Goal Ancestry** | ✅ | ❌ 不要 | 单项目用不到 |
| **Heartbeat 队列** | ✅ | ❌ 不要 | 单次调用 |
| **Memento Man** | ✅ | ❌ 不要 | session 不跨天 |
| **ACP** | ✅ | ❌ 不要 | Lite 只用内部 agent |
| **MCP** | ✅ | ❌ 不要 | 直接 import skill |
| **Plugin 架构** | ✅ | ❌ 不要 | skill 目录够用 |
| **Template** | ✅ | ❌ 不要 | YAML 复用即可 |
| **Action Schema** | ✅ | ⚠️ 部分 | 关键 2-3 个 action 即可 |
| **hash-chain 审计** | ✅ | ❌ 不要 | 普通日志够 |
| **多 session 隔离** | ✅ | ❌ 不要 | 单 session |

**v5.0-lite 砍掉 14 个 v4.2 特性，只保留 7 个核心**。

---

## 七、对何大人 3 个具体问题的回答

### Q1：是不是大杂烩？

**是**。v4.2 融合了 Paperclip / Conductor / Anthropic / Goose / Routa / Harnss / GitHub 7 大生态的精华，单一项目用不到这么多。**适合做"研究/参考"，不适合直接照搬**。

**正解**：**v4.2 是"v5.0-Pro 的设计蓝图"，不是"v5.0 的实现"**。

### Q2：正常给需求到落地会不会太复杂？

**会**。v4.2 全套跑通一个项目需要：
- 写 6 个 agent 配置
- 写 8 阶段 workflow YAML
- 装 10+ 个 skill
- 配 MCP server
- 配插件
- 写公司模板
- **总配置时间：~2 小时/项目**

对单个小项目来说，**纯手工可能更快**。

**正解**：Lite 版只配 3 阶段 + 1 个 agent，**配置时间 5 分钟**。

### Q3：token 消耗如何？

**v4.2 估算**：~640k tokens / 项目 ≈ 0.27 美元 / 项目（MiniMax M3 价格）
**v5.0-lite 估算**：~56k tokens / 项目 ≈ 0.05 元 / 项目（便宜 5 倍）

**实战对比**：
- Claude Code 单次中型项目：~100-500k tokens
- Cursor Composer 1 小时：~200-800k tokens
- v5.0-lite 单项目：~56k tokens
- v4.2 单项目：~640k tokens（**比 Claude Code 还费**）

**结论**：**v4.2 的 token 消耗比主流 IDE 还高**，因为概念多、agent 多。**Lite 才有性价比**。

---

## 八、最终建议

### 立即行动（本周）

**做 Lite MVP**：
1. 写 `workflow-lite.yaml`（3 阶段）
2. 写 `engine.py`（YAML 解析 + 路由，200 行）
3. 写 `state.py`（SQLite，300 行）
4. 复用现有 LLMInterface
5. 跑通 1 个真实小项目（如：写个 CLI 工具）

**验证标准**：
- 单项目 < 5 分钟人工介入
- token 消耗 < 100k
- 配置文件 < 50 行

**预计工作量**：**1 人 2 周可完成**。

### 中期演进（3-6 个月）

**根据实际使用情况决定**：
- 如果 Lite 不够 → 加 Standard
- 如果 Standard 够用 → 停在这里
- 任何时候都不要直接上 Pro

### 长期愿景（6-12 个月）

**v5.2 Pro 仅在以下情况才做**：
- 已经用 Lite/Standard 跑过 20+ 项目
- 团队 ≥ 3 人
- 明确有跨项目复用需求
- 已经有预算支撑 3-4 月开发

---

## 九、对比主流方案的真实选择

| 场景 | 推荐方案 | 理由 |
|------|---------|------|
| **个人小项目**（1-2 文件）| **Lite MVP**（我们自己）| 简单 / 便宜 / 0 学习成本 |
| **个人中型项目**（5-20 文件）| **Claude Code / Codex** | 成熟 / 文档全 / 社区活跃 |
| **个人多项目并行** | **v5.0 Standard** | 我们自建 + Lite 演进 |
| **团队 R&D 平台** | **Paperclip**（直接用）| 70k stars / 已成熟 / 开箱即用 |
| **企业级 + 多团队** | **Paperclip + 自定义 plugin** | 商业可用 / 治理完善 |
| **研究 / 探索** | **v4.2 思路作为参考** | 了解前沿设计，但**不要直接照搬** |

**最重要的一点**：
> **v4.2 不应该作为"我们要做的产品"，应该作为"我们做 Lite/Standard 时参考的设计原则库"**。

---

## 十、结论

**v4.2 是设计蓝图，v5.0-lite 是可执行版本。**

**实战路径**：
```
本周    2 周     1 月       3-6 月       6-12 月
 │      │        │          │            │
 ▼      ▼        ▼          ▼            ▼
写    Lite   跑 10 个   加 Standard   (可选) Pro
YAML  MVP    真实项目   按需扩展
```

**拒绝大杂烩**——**Lite 优先，实测驱动，按需升级**。

要不要现在就启动 v5.0-lite 的开发？我可以基于现有 v4.2 设计先写好 Lite 版的 workflow-lite.yaml 和核心代码骨架。
