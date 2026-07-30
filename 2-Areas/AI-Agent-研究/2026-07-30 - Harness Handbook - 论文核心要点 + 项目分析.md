---
type: research-report
title: Harness Handbook — 让 Agent Harness 可读、可导航、可编辑
authors:
  - Ruhan Wang（通讯，Indiana University）
  - Yucheng Shi（项目主导，Tencent HY LLM Frontier）
  - Zongxia Li, Zhongzhi Li, Yue Yu, Junyao Yang, Kishan Panaganti, Haitao Mi, Dongruo Zhou, Leoweiliang
affiliations:
  - 1. Tencent HY LLM Frontier（主导方）
  - 2. Indiana University
  - 3. University of Maryland
  - 4. University of Georgia
  - 5. National University of Singapore
arxiv: 2607.13285
huggingface_papers: https://huggingface.co/papers/2607.13285
github: https://github.com/Ruhan-Wang/Harness_Handbook
homepage: https://ruhan-wang.github.io/Harness-Handbook
demo: https://ruhan-wang.github.io/Harness-Handbook/studio/index.html
example: https://ruhan-wang.github.io/Harness-Handbook/terminus-handbook/index.html
released: 2026-07 (June 2026 paper, Tencent Hunyuan)
analyzed_date: 2026-07-30
tags: [ai-agent, coding-agent, agent-harness, behavior-localization, code-search, planning, behavior-map, progressive-disclosure, static-analysis, llm-narration, tencent, deepseek, opus]
source:
  url: https://github.com/Ruhan-Wang/Harness_Handbook
  fetched: 2026-07-30T08:53+08:00
  by: 小助 via web_search + GitHub README + 官方文档站
context_origin: 何大人 2026-07-30 08:52 GMT+8 转发的公众号文章摘要
---

# Harness Handbook — 论文核心要点 + 项目分析

> **一句话判断：** Harness Handbook 不是"给代码库生成文档"，而是给 **agent harness 这种特殊代码库** 建一张 **行为地图**：从"行为"反查"代码证据"，让 LLM 写编辑计划时不再做全仓 grep。Handbook + DeepSeek-V4-Pro 定位水平接近 Opus 4.8。

## 一、项目快照

| 维度 | 信息 |
|---|---|
| 论文 | Harness Handbook: Making Evolving Agent Harnesses Readable, Navigable, and Editable |
| 论文号 | arXiv 2607.13285 / Hugging Face Papers |
| 主导单位 | **Tencent HY LLM Frontier**（混元）+ Indiana University 等 4 所高校 |
| 一作/通讯 | Ruhan Wang（Indiana University，ruhwang@iu.edu） |
| 项目主导 | Yucheng Shi（Tencent HY） |
| GitHub | [Ruhan-Wang/Harness_Handbook](https://github.com/Ruhan-Wang/Harness_Handbook) |
| 官方站 | [ruhan-wang.github.io/Harness-Handbook](https://ruhan-wang.github.io/Harness-Handbook) |
| Studio Demo | [ruhan-wang.github.io/Harness-Handbook/studio](https://ruhan-wang.github.io/Harness-Handbook/studio/index.html) |
| 样例 handbook | [Terminus 2 Handbook](https://ruhan-wang.github.io/Harness-Handbook/terminus-handbook/index.html) |
| 许可证 | （README 未明示，需到 LICENSE 文件确认） |
| README 语言 | 英文 / 简体中文 / 俄文 |
| 发布时间 | 2026-06 论文，2026-07 上榜 HF Papers |

> 仓库 README 多语言（en/zh/ru），文档站和 demo 站都是 GitHub Pages。论文是 Tencent Hunyuan 主导，但 GitHub 仓库挂在个人账号下（学术界常见）。

## 二、它在解决什么具体问题

### 2.1 痛点：Harness 代码规模 vs 行为定位能力

官方用 Codex 当例子（这一组数字非常说明问题）：

| 指标 | Codex 实际规模 |
|---|---|
| 源文件数 | **2,267** |
| 函数数 | **34,000+** |
| 代码连接（call graph edges） | **≈160,000** |

在这个规模下，传统方法的问题：

1. **目录树告诉你"代码在哪里"**，但不告诉你"代码如何组合成一个行为"。
2. **grep/语义搜索返回"零散片段"**，需要人工拼成完整行为链。
3. **长上下文也救不了**——Codex 这种规模 100K tokens 也只能装下冰山一角。

### 2.2 一个具体例子：删除前确认

"删除文件前要先问用户"——听起来是一条规则，但要回答"它真的会问吗？"必须跑通整条链路：

```
model 是否请求 confirmation
  ↓
tool wrapper 是否拦截
  ↓
permission 配置里有没有 Bypass 路径
  ↓
用户的 yes/no 写到哪里
  ↓
最终 delete 真正执行的条件
  ↓
如果哪一步报错，fallback 走哪条
```

**没有任何一个函数能代表完整行为**——比如根本没有 `confirmBeforeDelete()` 这种入口。这是 harness 跟普通业务代码的本质差别：**行为是散落的实现点的运行时组合，不是源代码中的一棵树**。

### 2.3 论文命名这个问题为：Behavior Localization

> 把"行为"映射回"代码证据"的完整性，决定了你能否：
> - **理解** harness 实际怎么跑
> - **审计** 行为是否符合预期（包括旁路、fallback、罕见分支）
> - **改动** 一个行为时画准边界（不漏 prompt、不漏 permission rule、不漏 fallback）

### 2.4 三个目标，统一到一张地图

| 目标 | 传统做法 | Harness Handbook |
|---|---|---|
| **Understand** 看 harness 怎么跑 | 读 README + 跳源码 | 沿 L1→L2→L3 顺行为走 |
| **Audit** 验证行为符合预期 | 手工 grep + 反复验证 | 沿 L3 单元核对每个决策 |
| **Adapt** 改/适配自己的 agent | 重读全部相关模块 | 锁定行为单元 → 精确定位改动边界 |

## 三、核心方法论

### 3.1 三层结构（L1 / L2 / L3）

```
L1 · System overview
  └─ 一个请求如何穿过整个 harness
     └─ 从模型接到请求 → 阶段 → 状态流转 → 输出真实动作
     └─ 回答："整个 harness 怎么跑？"

L2 · Behavior-unit overview
  └─ 把系统拆成"行为单元"
     └─ 每个单元有：职责 / 输入输出 / 依赖 / 关键状态
     └─ 回答："复杂行为是怎么拆解的？块之间怎么连？"

L3 · Behavior-unit detail
  └─ 单个行为单元的完整细节
     └─ 触发条件 / 执行步骤 / 状态变更 / 异常路径 / 代码证据
     └─ 回答："这个行为在哪些文件、哪些函数里实现？旁路在哪？"
```

**关键设计**：每一层都保留**可验证的代码证据**（文件路径 + 函数名 + 行号），所以 L3 不是"叙述"，是"叙述 + 链接"，LLM 沿着链接可以回到真实源码核对。

### 3.2 Behavior-Guided Progressive Disclosure (BGPD)

论文提出的检索/导航范式：

1. **从高层行为描述开始**（不是从关键词搜索开始）
2. **逐步下钻**：L1 → L2 → L3
3. **每一步对照当前源码验证**：候选位置要回源码核对一次
4. **最终输出"verbatim EDIT plan"**：可逐字粘贴到 code agent 的 patch 指令里

跟传统 "file-as-leaf" 文档（比如 docstring 自动生成）最大的区别：

| 维度 | 传统代码文档 | Harness Handbook |
|---|---|---|
| 组织维度 | 文件 / 函数 / 类 | **行为**（跨多个实现点） |
| 入口 | 文件树 | 行为目录 + 状态寄存器 |
| 证据 | 代码片段 | 文件 + 函数 + 行号 + 旁路说明 |
| 适用对象 | 普通代码库 | **agent harness 这类行为分散的系统** |

### 3.3 行为地图的内容

从 Terminus 2 的样例 handbook 看，输出包含：

```
work/<repo>/handbook/
├── overview.md        ← L1 系统总览
├── index.md           ← 行为阶段的路由索引（核心导航骨架）
├── register.md        ← 跨阶段状态寄存器
├── stages/<id>.md     ← L2/L3 每个行为单元一页
└── html/overview.html ← 可浏览的 HTML 站点（--phase3-html）
```

每个 stage 页里有：

- **Behavior unit name**（语义命名，不是文件名）
- **Trigger**（什么时候触发）
- **Inputs / Outputs**
- **State changes**
- **Execution path**（主路径）
- **Exception / fallback paths**（旁路！）
- **Code evidence**（文件路径 + 函数）

## 四、工程实现

### 4.1 仓库结构

```
Harness_Handbook/
├── handbook_generate_large/    ← 大代码库生成器（file-as-leaf bottom-up）
├── handbook_generate_small/    ← 小代码库生成器（skeleton-driven）
└── handbook_as_helper/         ← 把 handbook 喂给 code agent 的 planner
    ├── pipeline/
    │   ├── code_agent.py      ← handbook planner（单 read-only agent）
    │   ├── targets.py          ← 评估目标定义（每个 harness 一项）
    │   └── update_handbook.py  ← resync：代码改了之后滚动手册
    ├── handbook_skills/        ← handbook → SKILL.md 转换器
    └── prompts/planner_handbook.md
```

### 4.2 两个生成器怎么选

| | `handbook_generate_large` | `handbook_generate_small` |
|---|---|---|
| 适用规模 | **大代码库**（如 Codex） | 小代码库（自己写 skeleton 的） |
| 骨架来源 | **LLM 自动合成**（doctor 模式：actor-critic） | **手写** `skeleton.yaml` |
| 覆盖策略 | Bottom-up file-as-leaf，**保证每个文件都覆盖** | Skeleton-driven，按骨架生成 |
| 适用场景 | 不想手工整理目录 | 代码库小到可以枚举主要行为 |
| 是否需要手写 | 不需要 | 需要写 `skeleton.yaml` |

**经验法则**：拿不准就用 large（保证全覆盖）；只有骨架很清晰时才用 small。

### 4.3 三阶段流水线

```
Phase 1 · 静态分析（不需要 LLM）
  └─ tree-sitter 解析 → 调用图 → 函数索引
  └─ 可独立跑，用来"烟雾测试" parse 是否正确

Phase 2 · LLM 分类（需要 LLM）
  └─ 对每个文件/函数做 actor-critic doctor 合成
  └─ 生成分阶段骨架（仅 large 需要）

Phase 3 · LLM 叙述（需要 LLM）
  └─ 从叶子向上叙述 → 系统总览
  └─ 可生成多页 HTML 站点（--phase3-html）
```

### 4.4 作为 code agent planner（最关键的工程产出）

```python
# handbook_as_helper/ 提供的核心 API
import sys; sys.path.insert(0, "pipeline")
from code_agent import run_query

out = run_query(
    "<自然语言改动请求>",
    Path("/path/to/source"),       # 目标代码库
    Path("runs/case1"),            # scratch sandbox（git copy）
    # arm="handbook" 是默认值，也是唯一选项
)
print(out["plan"])  # 输出 verbatim EDIT plan
```

**架构亮点（值得记一下）**：

- **只有一个 read-only agent**（不是 locator sub-agent + map-reduce）
- 导航靠 handbook 的 SKILL / index / registers / stage pages
- 输出的 plan **逐字可贴**到 code agent 的 patch 指令里
- planner **不修改代码**（plan-only），改了的话走 resync

### 4.5 Resync：代码改了之后怎么滚动手册

```bash
# 准备 case_dir
# edited/    ← 应用了 PR 的源码
# plan.md    ← 改动描述（驱动 reconcile）
# agent.diff ← edited/ 与 pristine 的 diff（可选）

python pipeline/update_handbook.py <case_dir>
python pipeline/update_handbook.py <case_dir> --no-translate
```

这是工程上最被低估的一块——**长生命周期系统里，文档过期是头号问题**。他们直接内置 resync 流水线。

### 4.6 LLM 配置（OpenAI 兼容即可）

```bash
export OPENAI_API_KEY=sk-...           # 必填
export OPENAI_MODEL=gpt-4o-mini        # 默认
export OPENAI_BASE_URL=https://api.openai.com/v1
# 任意 OpenAI 兼容端点都支持（vLLM / LiteLLM 代理都行）
```

> 论文评测里 handbook + DeepSeek-V4-Pro 接近 Opus 4.8 水平——说明 **prompt + 导航结构能极大降低对模型能力的依赖**。

## 五、跟现有方案的横向对比

| 方案 | 解决什么 | 跟 Handbook 关系 |
|---|---|---|
| **GitHub Copilot Coding Agent** (2026-02) | 仓库内自定义 agent / 自审 / 安全扫描 | 不同抽象层（VS Copilot 是产品） |
| **OpenAI Harness Engineering** | Codex 自己维护的 agent-legibility 工程实践 | **方法论同源**（progressive disclosure / 知识库前置），但 OpenAI 是闭源 |
| **DeepWiki**（cursor 早期实验） | 自动仓库文档 | **子类**：DeepWiki 是 file-as-leaf，Handbook 是 behavior-as-leaf |
| **Codex Aider / Aider 自己** | 仓库内 chat + 自动改 | 跟 Handbook 是**互补**关系——Handbook 给 planner，Aider 是 runner |
| **AGENTS.md**（Open SWE） | 给 agent 注入仓库惯例 | 也是 progressive disclosure，但**没有行为结构化** |

**最关键的差异化**：Harness Handbook 是**面向 agent harness 这种特殊代码库**的，而上述工具是**通用代码库**。它把"行为分散"作为一等公民。

## 六、何大人可能的应用场景

> 7-8 何大人明确：**不要每个链接都挂钩德勤项目**。这里列**实质性的**应用，避免过度挂钩。

### 6.1 德勤项目：执行器抽象层（直接相关，已有研究边界）

根据 2026-06-29 决策：

- **Hermes Agent v0.14 是德勤 Agent 框架唯一选择**
- **执行器抽象层** = Hermes / OpenClaw / Codex / Claude Code 都可插拔
- **研究边界**：调研的是**具体技术借鉴点**，不是"X 替代 Y"

**Harness Handbook 可借鉴的具体技术**：

| 德勤组件 | 可借鉴的技术点 | 怎么用 |
|---|---|---|
| **执行器抽象层 adapter** | 三个 phase 流水线 + tree-sitter 静态分析 | 给每个 adapter 加一层 "behavior layer"，让上层 planner 看 harness 时不需要懂底层 |
| **Hermes dispatcher** | BGPD 渐进披露 | 任务描述模糊 → 用 BGPD 让 dispatcher 先看行为地图，再 claim 任务（避免 v0.14 那种"标 blocked"） |
| **可观测性** | register.md（跨阶段状态寄存器） | 德勤 MVP 仪表板里加 "状态寄存器视图"，跨执行器对齐 |
| **Resync 机制** | 改代码后自动滚动文档 | 德勤交付物里所有 ADR / 决策文档自动 resync 到代码 |

### 6.2 自身研究：长期项目文档保鲜

何大人的 vault 已经 1-Projects / 2-Areas / 3-Resources 几百个文件。**文档过期**是常见痛点。Harness Handbook 的 resync 流水线思路（`update_handbook.py`）可以借鉴到一个简化版：

- 每天凌晨扫 vault
- 检测 ADR / README / 笔记 提到的文件是否还存在
- 自动开 PR 修正过期引用

### 6.3 Agent 自己定位 vault 内代码

何大人的 `/root/AgentSpace` 已经在跑 OpenClaw / Claude / Codex / Hermes 5 个 harness 切换。如果给 AgentSpace 加一个"vault behavior handbook"：

- OpenClaw 接任务时，先读 vault 的"行为地图"
- 知道"找何大人最近指令 → 2-Areas/MEMORY.md 顶部"
- 知道"找德勤项目当前状态 → 1-Projects/德勤/README.md"

相当于给 AgentSpace 装一张"vault 的 L1/L2/L3 导航图"。

## 七、风险与局限

| 局限 | 说明 |
|---|---|
| **依赖 LLM 质量** | Phase 2/3 都重度依赖 LLM 分类和叙述质量，模型换了输出风格大变 |
| **token 成本** | Deep read（`--read-detail deep`）要 LLM 读全文件，大代码库成本可观 |
| **行为边界定义** | LLM 自动合成的行为单元，可能切分不准确（行为切错 → 整段导航失效） |
| **多语言支持** | 显式支持 Python/Rust/TypeScript/Go + Starlark/Shell/PowerShell，其它语言需要 adapter |
| **resync 鲁棒性** | 大改之后行为结构可能整个变，resync 未必能跟得上 |
| **可重复性** | LLM 输出的随机性 → 同一份代码两次生成 handbook 可能不完全一致 |

## 八、立即可做的下一步（建议清单）

1. **克隆仓库本地试跑**：
   ```bash
   cd /root
   git clone https://github.com/Ruhan-Wang/Harness_Handbook.git
   cd Harness_Handbook
   python3 -m venv .venv && source .venv/bin/activate
   pip install tree-sitter tree-sitter-language-pack pyyaml requests markdown pygments
   ```
   先拿 `/root/AgentSpace`（小代码库）跑 small pipeline，验证能生成中文 handbook。

2. **读完整论文**：arXiv 2607.13285，看具体 benchmark 表（DeepSeek-V4-Pro vs Opus 4.8 的对照数字）。

3. **写借鉴笔记**：在 `/root/vault/1-Projects/德勤/AI-Native/executor/` 下加一个 `2026-07-30 - Harness Handbook 借鉴点.md`，把上面 6.1 的表格展开成"哪些具体代码 / 设计文档可以落到 Hermes adapter"。

4. **如果决定试**：在 Hermes v0.14 的 adapter 仓库里加 `behavior_layer/` 子目录（参考 handbook_generate_large 的 phase 1 静态分析），最小可用版即可。

## 九、引用

```bibtex
@misc{wang2026harnesshandbookmakingevolving,
  title={Harness Handbook: Making Evolving Agent Harnesses Readable, 
         Navigable, and Editable},
  author={Ruhan Wang and Yucheng Shi and Zongxia Li and Zhongzhi Li and 
          Yue Yu and Junyao Yang and Kishan Panaganti and Haitao Mi and 
          Dongruo Zhou and Leoweiliang},
  year={2026},
  eprint={2607.13285},
  archivePrefix={arXiv},
  primaryClass={cs.AI},
  url={https://arxiv.org/abs/2607.13285}
}
```

---

**核心 takeaway 写给何大人（人话版）**：

> 这不是"AI 写文档"的工具，是"给 agent harness 这种代码库建行为地图"的工具。三层结构（L1→L2→L3）+ BGPD 渐进披露，让一个相对便宜的模型（DeepSeek-V4-Pro）做出接近 Opus 4.8 的代码定位能力。
>
> **最值得借鉴到德勤的不是"生成手册"，而是"行为地图 + resync + planner 单 agent 不分拆"这三件套**——尤其 resync 那块，长期项目里文档过期是头号问题。
