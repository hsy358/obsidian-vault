---
title: "Superpowers 深度实战指南：从入门到精通"
author: "AgentBuff"
publish_date: "2026-05-08 18:20:37"
saved_date: "2026-05-10"
source: "wechat"
url: "https://mp.weixin.qq.com/s/BvrB7td8iJd4vNQW3T_UFg"
---
# Superpowers 深度实战指南：从入门到精通
## 介绍

**Superpowers** 是一个为 AI 编程代理设计的**软件开发方法论框架**。它覆盖 Claude Code、Codex CLI、Codex App、Cursor、Gemini CLI、OpenCode、GitHub Copilot CLI，以及 Factory Droid。它是一套"技能系统"（Skills System）——通过结构化的 Markdown 文档与各平台各自的 bootstrap 机制，把工作流约束注入到代理上下文中，从而**强制约束代理的行为模式**，使其遵循专业的软件工程实践。

**核心理念：** 代理不需要"被建议"怎么做，而是需要"被强制"怎么做。Superpowers 通过 `HARD-GATE`、`Iron Law`、`Red Flags` 等机制，将最佳实践从"建议"升级为"铁律"。

Superpowers 的核心理念是统一的，但不同平台的引导方式并不完全相同；`hooks/session-start` 只是其中一种实现路径，而不是所有 harness 的唯一入口。

---

## 架构全景

### #目录结构

```
superpowers/├── .claude-plugin/        # Claude Code 插件配置│   ├── plugin.json        # 插件元数据│   └── marketplace.json   # 市场注册信息├── .codex-plugin/         # Codex CLI/App 插件配置│   └── plugin.json├── .cursor-plugin/        # Cursor 插件配置│   └── plugin.json├── .opencode/             # OpenCode 插件配置│   ├── INSTALL.md│   └── plugins/├── hooks/                 # 会话启动钩子│   ├── hooks.json         # Claude Code 钩子配置│   ├── hooks-cursor.json  # Cursor 钩子配置│   ├── session-start      # 核心启动脚本（Bash）│   └── run-hook.cmd       # 跨平台包装器（Windows兼容）├── skills/                # 技能库（核心资产）│   ├── brainstorming/│   ├── dispatching-parallel-agents/│   ├── executing-plans/│   ├── finishing-a-development-branch/│   ├── receiving-code-review/│   ├── requesting-code-review/│   ├── subagent-driven-development/│   ├── systematic-debugging/│   ├── test-driven-development/│   ├── using-git-worktrees/│   ├── using-superpowers/       # 入口技能（引导文档）│   ├── verification-before-completion/│   ├── writing-plans/│   └── writing-skills/├── scripts/               # 工具脚本│   ├── bump-version.sh    # 版本管理│   └── sync-to-codex-plugin.sh├── tests/                 # 集成测试├── docs/                  # 文档├── CLAUDE.md              # Claude Code 项目指令├── GEMINI.md              # Gemini CLI 项目指令├── AGENTS.md              # 通用代理指令└── README.md
```

### #技能体系速览

![](https://mmbiz.qpic.cn/sz_mmbiz_png/c8WXahKZ0fOA4nsDyXXyXM8VKNTx5CxZ7fJvH8mQqYlzrJ5MQZoTiaVGLXC0IKYABBqeeX2bPLGNWEIKIf5T2MZic6S0CI9QRFWopylmibcXBU/640?wx_fmt=png&from=appmsg)

如果只看上面的目录树，最容易先注意到的是插件配置和 hooks，但这个仓库真正的主体其实是 `skills/`。更准确地说，Superpowers 是一套围绕软件开发流程拆出来的技能集合，不同技能分别负责不同阶段的约束：

- **入口与调度**：`using-superpowers` 负责把“先检查技能再做事”这条总规则立起来；`dispatching-parallel-agents`、`subagent-driven-development` 负责多代理协作和任务分发。
- **前期设计**：`brainstorming` 用来压住“先写再说”的冲动，要求先澄清需求、给出方案、写设计文档。
- **实现规划与执行**：`writing-plans` 负责把需求拆成能执行、能验证的小任务；`executing-plans` 则负责在没有强子代理支持时串行落地这些任务。
- **开发纪律**：`test-driven-development`、`systematic-debugging`、`verification-before-completion` 分别约束测试、调试和交付前验证，避免代理靠猜测推进工作。
- **交付与收尾**：`requesting-code-review`、`receiving-code-review`、`finishing-a-development-branch`、`using-git-worktrees` 负责代码审查、分支管理和最终收尾动作。
换句话说，这个目录不是一堆零散技巧的堆叠，而是一条完整开发流水线的拆分版：从接到任务、讨论设计、写计划、实现、调试、验证，到最后收尾，都有对应的技能在管。

### #工作原理

Superpowers 统一流程是：

```
会话启动/插件加载 → bootstrap 上下文注入 → 技能发现与按需加载 → 技能自动触发
```

也就是说，项目真正统一的是**行为约束模型**，不是单一的技术接入点。不同平台通过不同机制把 `using-superpowers` 这段“启动技能”送进上下文。

#### 路径 A：Claude Code / Cursor / GitHub Copilot CLI 风格的启动钩子

这条路径由 `hooks/session-start` 和两个 hook 配置文件驱动：

- `hooks/hooks.json`：Claude Code 使用 `SessionStart`
- `hooks/hooks-cursor.json`：Cursor 使用 `sessionStart`
- GitHub Copilot CLI 复用 `hooks/session-start` 的 SDK 标准输出格式
Claude Code 的 hook 配置如下：

```
{  "hooks": {    "SessionStart": [      {        "matcher": "startup|clear|compact",        "hooks": [          {            "type": "command",            "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" session-start",            "async": false          }        ]      }    ]  }}
```

`hooks/session-start` 会读取 `skills/using-superpowers/SKILL.md`，转义为 JSON 字符串后嵌入上下文。当前实现并不只是塞进技能全文，还会加一段明确提示，并在检测到旧版自定义技能目录时插入迁移警告。关键拼接如下：

```
session_context="<EXTREMELY_IMPORTANT>\nYou have superpowers.\n\n**Below is the full content of your 'superpowers:using-superpowers' skill - your introduction to using skills. For all other skills, use the 'Skill' tool:**\n\n${using_superpowers_escaped}\n\n${warning_escaped}\n</EXTREMELY_IMPORTANT>"
```

然后它再按平台输出不同 JSON 字段：

```
if [ -n "${CURSOR_PLUGIN_ROOT:-}" ]; then  printf '{\n  "additional_context": "%s"\n}\n' "$session_context"elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ] && [ -z "${COPILOT_CLI:-}" ]; then  printf '{\n  "hookSpecificOutput": {\n    "hookEventName": "SessionStart",\n    "additionalContext": "%s"\n  }\n}\n' "$session_context"else  printf '{\n  "additionalContext": "%s"\n}\n' "$session_context"fi
```

#### 路径 B：OpenCode 的插件注入

OpenCode 不走 `session-start` 钩子，而是使用 `.opencode/plugins/superpowers.js`：

- 通过 `config` hook 把 `skills/` 目录注册到 OpenCode 的技能搜索路径
- 通过 `experimental.chat.messages.transform` 把 bootstrap 文本注入到会话第一条用户消息前面
这意味着 OpenCode 的关键不是 shell hook，而是插件层面的消息变换与技能目录注册。

#### 路径 C：Gemini CLI 的上下文文件

Gemini 侧由 `gemini-extension.json` 指定 `contextFileName: "GEMINI.md"`，而 `GEMINI.md` 再显式引用：

- `@./skills/using-superpowers/SKILL.md`
- `@./skills/using-superpowers/references/gemini-tools.md`
换言之，Gemini 的引导方式是“扩展上下文文件 + 技能引用”，而不是 hook 脚本。

**结论：** `using-superpowers` 才是所有平台共享的行为入口；hook、插件 transform、context file 只是不同 harness 的装配层。

---

## 安装与配置

### #3.1 Claude Code

![](https://mmbiz.qpic.cn/sz_mmbiz_png/c8WXahKZ0fM2242lGGrWahOSjg5NEIYYttibXAFP6qriaavqX5ib9ziclGT5yWUCHq70mVahCQYhCWjERJmUR5NNZBrRWiccGqNIQDnpiaaUC1yKg/640?wx_fmt=png&from=appmsg)

#### 方式一：官方市场

```
/plugin install superpowers@claude-plugins-official
```

#### 方式二：Superpowers 市场

```
/plugin marketplace add obra/superpowers-marketplace/plugin install superpowers@superpowers-marketplace
```

### #Codex CLI

```
/plugins# 搜索 "superpowers" → Install Plugin
```

### #Codex App

Codex App 与 Codex CLI 复用同一个 `.codex-plugin/plugin.json` 包定义，但 UI 会额外读取其中的 `interface` 字段来展示名称、分类、默认提示词、品牌色等信息。

```
侧边栏打开 Plugins → 在 Coding 分类中找到 Superpowers → 点击 + 安装
```

### #Factory Droid

```
droid plugin marketplace add https://github.com/obra/superpowersdroid plugin install superpowers@superpowers
```

### #Cursor

```
/add-plugin superpowers
```

### #Gemini CLI

```
gemini extensions install https://github.com/obra/superpowers
```

### #OpenCode

把 Superpowers 加到 `opencode.json` 的 `plugin` 数组里。

```
{  "plugin": ["superpowers@git+https://github.com/obra/superpowers.git"]}
```

重启 OpenCode 后，插件会自动注册技能目录并注入 bootstrap 上下文。README 中这句：

```
Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md
```

更适合让代理在 OpenCode 会话里“自助安装”，但不是仓库里唯一也不是最底层的安装说明。

### # GitHub Copilot CLI

```
copilot plugin marketplace add obra/superpowers-marketplacecopilot plugin install superpowers@superpowers-marketplace
```

---

## 技能系统深度解析

### #技能文件结构

每个技能是一个目录，核心文件通常是 `SKILL.md`，采用 YAML frontmatter + Markdown 的格式：

```
---name: skill-namedescription: "Use when [触发条件]..."---# 技能标题## Overview核心原则## When to Use使用场景## Checklist / Process / Quick Reference工作流或操作步骤## Red Flags反模式清单## Common Rationalizations| 借口 | 现实 |
```

**关键设计：** `description` 字段优先描述"何时触发"，而不是把完整工作流塞进摘要里。`using-superpowers`、`brainstorming`、`writing-plans` 等技能都遵循这一模式，让代理先命中技能，再读取正文执行，而不是只靠一句简介“脑补流程”。

### #using-superpowers — 入口引导技能

这是整个系统的"启动器"。它定义了一条铁律：

> **如果有 1% 的可能性某个技能适用，你就必须调用它。**

它包含一个"红旗表"，专门用来识别代理的合理化借口：

代理的想法现实"这只是个简单问题"问题就是任务。检查技能。"我需要先了解更多上下文"技能检查在澄清问题之前。"让我先探索代码库"技能告诉你如何探索。先检查。"这个技能太重了"简单的事会变复杂。用它。"我先做这一件事"做任何事之前先检查。**优先级顺序：**

- 用户的明确指令（最高优先级）
- Superpowers 技能
- 默认系统提示（最低优先级）

### #brainstorming — 头脑风暴技能

![](https://mmbiz.qpic.cn/sz_mmbiz_png/c8WXahKZ0fOib3ft3IC1skhI6XIHPS4wCpibSMkhkgLpLyia8Fj4iazw7MibBf0M8e29o9HLldCW0lvOnWpLZyyic03lVvZOrd4zASGbb1AHO7sjA/640?wx_fmt=png&from=appmsg)

**触发条件：** 任何创造性工作之前——创建功能、构建组件、添加功能、修改行为。

**硬门控（HARD-GATE）：**

> 在呈现设计并获得用户批准之前，不得调用任何实现技能、编写任何代码、搭建任何项目。

**流程：**

```
探索项目上下文 → 一次一个问题澄清 → 提出2-3种方案 → 分段呈现设计 → 写设计文档 → 自审 → 用户审阅 → 转入 writing-plans
```

**关键原则：**

- 一次只问一个问题
- 优先使用选择题
- YAGNI（你不会需要它）—— 无情地移除不必要的功能
- 每个设计部分呈现后等待用户确认
- 设计文档保存到 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
- 写完设计文档后要做一次自审，并要求用户审核 written spec
- 设计文档需要提交到 git
**视觉伴侣：** 如果话题涉及视觉问题（布局、线框图），可以提供浏览器端的 mockup 展示。但这必须作为**单独一条消息**征得用户同意，不能和其他问题混在一起。它会启动一个本地服务Visual companion，将架构设计以图形化效果展示给用户。

![](https://mmbiz.qpic.cn/mmbiz_png/c8WXahKZ0fMNxzhF0me3SW3wgWBdVwu2uRnIg7lxAx4THFQg3fWMPoxwCwwtLTaTPO3xycoldd2ee3XrGNT7G17gmKkvBQxfPOniaib3mDrtU/640?wx_fmt=png&from=appmsg)

**关键约束：** brainstorming 结束后，唯一允许衔接的下一个技能是 `writing-plans`，不能直接跳去实现型技能。

### #writing-plans — 编写实现计划

**触发条件：** 有了规格说明或需求，准备开始编码之前。

**核心原则：** 假设执行者是一个"有技能但零上下文、品味存疑、不愿测试的热心初级工程师"。

**任务粒度——每个步骤是 2-5 分钟的一个动作：**

```
### Task N: [组件名]**Files:**- Create: `exact/path/to/file.py`- Modify: `exact/path/to/existing.py:123-145`- Test: `tests/exact/path/to/test.py`- [ ] **Step 1: Write the failing test**```pythondef test_specific_behavior():    result = function(input)    assert result == expected```- [ ] **Step 2: Run test to verify it fails**Run: `pytest tests/path/test.py::test_name -v`Expected: FAIL with "function not defined"- [ ] **Step 3: Write minimal implementation**...- [ ] **Step 4: Run test to verify it passes**...- [ ] **Step 5: Commit**
```

**禁止占位符：**

- "TBD"、"TODO"、"稍后实现"
- "添加适当的错误处理"
- "类似 Task N"（必须重复完整代码）
- 只描述做什么但不展示代码的步骤
**自审清单：**

- 规格覆盖：每个需求都有对应任务
- 占位符扫描：搜索红旗模式
- 类型一致性：后面的函数名、签名是否和前面定义的匹配
**保存位置：** 计划默认保存到 `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`。

**写完后续动作：** `writing-plans` 不直接开始编码，而是要求在保存计划后，明确让用户在 `subagent-driven-development` 和 `executing-plans` 之间二选一。

### #test-driven-development — 测试驱动开发

**铁律：**

```
没有先写失败测试，就不能写生产代码
```

**如果先写了代码？** 删除它。重新开始。不要保留作为"参考"，不要"改编"，不要看它。删除就是删除。

**RED-GREEN-REFACTOR 循环：**

```
RED（写失败测试）→ 验证失败 → GREEN（最简代码通过）→ 验证通过 → REFACTOR（重构）→ 下一个测试
```

**RED 阶段要求：**

- 一个行为
- 清晰的命名
- 真实代码（非 mock，除非不可避免）
**GREEN 阶段要求：**

- 写最简代码通过测试
- 不添加额外功能
- 不重构其他代码
**常见合理化借口及反驳：**

借口现实"太简单不需要测试"简单代码也会出错。测试只要30秒。"我之后再写测试"立即通过的测试证明不了任何东西。"删除X小时的工作太浪费"沉没成本谬误。保留未验证的代码才是技术债。"TDD太教条了"TDD 就是务实的：先测试比事后调试更快。"我已经手动测试过了"手动测试 ≠ 系统化测试。没有记录，无法重跑。
### # subagent-driven-development — 子代理驱动开发

**核心思想：** 每个任务分配一个全新的子代理，任务完成后进行两阶段审查，而且默认应当**连续执行完整个计划**，不要在每个任务之间回头问用户“还要不要继续”。

**为什么用子代理：**

- 隔离上下文，避免污染
- 精确构造指令和上下文
- 保留主代理的上下文用于协调工作
**流程：**

```
读取计划 → 提取所有任务 → 创建 TodoWrite  ↓每个任务：  派发实现者子代理 → 子代理提问？→ 回答 → 实现、测试、提交、自审  → 派发规格审查者 → 是否符合规格？→ 修复 → 重审  → 派发代码质量审查者 → 质量通过？→ 修复 → 重审  → 标记任务完成  ↓所有任务完成 → 派发最终代码审查 → finishing-a-development-branch
```

**模型选择策略：**

- 机械性实现任务（1-2个文件，清晰规格）→ 便宜快速的模型
- 集成和判断任务（多文件协调）→ 标准模型
- 架构、设计、审查任务 → 最强大的模型
**子代理状态处理：**

- `DONE`：进入审查
- `DONE_WITH_CONCERNS`：先评估担忧再审查
- `NEEDS_CONTEXT`：提供缺失上下文，重新派发
- `BLOCKED`：评估阻塞原因——上下文问题、需要更强模型、任务太大、计划有误
**三个提示模板：**

- **implementer-prompt.md** — 实现者模板，包含：任务描述、上下文、提问机制、自审清单、报告格式
- **spec-reviewer-prompt.md** — 规格审查者模板，关键指令："不要信任实现者的报告，独立验证一切"
- **code-quality-reviewer-prompt.md** — 代码质量审查者模板，基于 requesting-code-review 的审查者模板

### #executing-plans — 批量执行计划

**适用场景：** 已经有一份书面实现计划，但当前平台缺少高质量子代理支持，或者你刻意选择不用子代理，而是在单线程会话里按计划串行执行。

**与 subagent-driven-development 的区别：**

- `subagent-driven-development` 是当前会话里的“主控 + 新鲜子代理 + 两阶段审查”
- `executing-plans` 是由当前代理自己读计划、质疑计划、逐项执行
- 如果平台支持子代理，技能正文明确要求优先使用 `subagent-driven-development`
**流程：**

- 加载并批判性审查计划
- 若计划存在关键疑点，先和用户澄清，不可硬着头皮执行
- 逐个执行任务（标记 in_progress → 按步骤执行 → 运行验证 → 标记完成）
- 全部完成后调用 `finishing-a-development-branch`

### #systematic-debugging — 系统化调试

**铁律：**

```
没有根因调查，就不能提出修复方案
```

**四个阶段：**

#### Phase 1：根因调查

- 仔细阅读错误信息（不要跳过！）
- 一致地复现问题
- 检查最近的变更
- 在多组件系统中，先添加诊断仪器再分析
- 追踪数据流：坏值从哪里来？

#### Phase 2：模式分析

- 找到类似的工作代码
- 对比参考实现
- 识别差异

#### Phase 3：假设与测试

- 形成单一假设："我认为 X 是根因，因为 Y"
- 做最小的变更来测试
- 一次只改一个变量

#### Phase 4：实现

- 创建失败测试用例
- 实现单一修复
- 验证修复
- **如果 3 次修复都失败 → 质疑架构**
**支持技术（系统化调试的子文档）：**

- `root-cause-tracing.md` — 通过调用栈反向追踪 bug
- `defense-in-depth.md` — 在找到根因后，在多层添加验证
- `condition-based-waiting.md` — 用条件轮询替代任意超时

### #verification-before-completion — 完成前验证

**铁律：**

```
没有新鲜的验证证据，就不能声称完成
```

**门控函数：**

```
在声称任何状态之前：1. 识别：什么命令能证明这个声明？2. 运行：执行完整命令（新鲜的、完整的）3. 阅读：完整输出，检查退出码，计数失败4. 验证：输出是否确认了声明？5. 只有这时：才能做出声明
```

**常见失败模式：**

声明需要不够测试通过测试命令输出：0 failures上一次运行、"应该通过"构建成功构建命令：exit 0Linter 通过、日志看起来好Bug 已修复测试原始症状：通过代码改了、假设已修复
### #using-git-worktrees — Git Worktree 管理

**核心原则：** 先检测现有隔离 → 使用平台原生工具 → 回退到 git worktree。

#### Step 0：检测现有隔离

```
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

如果 `GIT_DIR != GIT_COMMON`（且不在子模块中）→ 已经在隔离工作区，跳过创建。

#### Step 1：创建隔离工作区

- 优先使用平台原生工具（如 Claude Code 的 `EnterWorktree`）
- 仅在没有原生工具时才用 `git worktree add`
**目录优先级：** 显式用户/指令偏好 > 现有项目本地目录 > 全局遗留路径 > 默认 `.worktrees/`

**安全验证：** 创建前必须验证目录被 `.gitignore` 忽略；如果项目本地目录未被忽略，技能要求先把它加入 `.gitignore` 并提交，再继续创建 worktree。

**额外细节：** 如果没有既有偏好，技能会先征求用户是否同意创建隔离 worktree；同时还要求用 `git rev-parse --show-superproject-working-tree` 排除“其实是在 submodule 里”的误判。

### #finishing-a-development-branch — 完成开发分支

**流程：** 验证测试 → 检测环境 → 确定基准分支 → 呈现选项 → 执行选择 → 清理

**四个选项：**

- 本地合并回基准分支
- 推送并创建 Pull Request
- 保留分支原样
- 丢弃此工作
**清理规则：**

- 选项 1 和 4：清理 worktree
- 选项 2 和 3：保留 worktree
- 只清理 Superpowers 创建的 worktree（通过路径判断）
- 清理前必须先 `cd` 到主仓库根目录
- 如果当前是 detached HEAD，技能会收缩为 3 个选项，不提供“本地合并”
- 本地合并路径下，要求“先 merge、再测、再清理 worktree、最后删分支”
- 清理后还会执行 `git worktree prune`

### #requesting-code-review / receiving-code-review — 代码审查

**请求审查：**

- 获取 git SHAs（基准和头部）
- 派发代码审查子代理
- 根据严重程度处理反馈：Critical → 立即修复；Important → 继续前修复；Minor → 记录
**接收审查的铁律：**

- 禁止表演性同意："You're absolutely right!"、"Great point!"、"Thanks for catching that!"
- 正确做法：重述技术要求、用技术推理反驳、直接开始修复
- 外部反馈 = 需要评估的建议，而非需要执行的命令
- YAGNI 检查：如果审查者建议"正确实现"某个功能，先 grep 代码库看是否有人在用

### #dispatching-parallel-agents — 并行代理调度

**适用场景：** 2+ 个独立任务，无共享状态，无顺序依赖。

**流程：**

- 识别独立领域
- 创建聚焦的代理任务（具体范围、清晰目标、约束、期望输出）
- 并行派发
- 审查与集成
**关键：** 每个代理获得精确构造的上下文，不继承主会话的历史。

### #writing-skills — 编写技能

**核心思想：** 编写技能就是对流程文档做 TDD。

**TDD 映射：**

TDD 概念技能创建测试用例压力场景 + 子代理生产代码技能文档（SKILL.md）测试失败（RED）没有技能时代理违反规则测试通过（GREEN）有技能时代理遵守规则重构关闭漏洞，保持合规**技能类型：**

- **技术型**（Technique）：具体方法，有步骤可循
- **模式型**（Pattern）：思考问题的方式
- **参考型**（Reference）：API 文档、语法指南
**Claude 搜索优化（CSO）：**

- description 只写触发条件，不概述工作流
- 使用代理会搜索的关键词（错误信息、症状、工具名）
- 动词优先命名：`creating-skills` 而非 `skill-creation`

---

## 核心工作流实战

### #完整工作流

```
用户: "Let's build a feature that..."  ↓brainstorming（头脑风暴）  → 探索上下文 → 一次一问 → 2-3方案 → 分段设计 → 设计文档 → 自审 → 用户审核  ↓using-git-worktrees（创建工作区）  → 检测隔离 → 创建 worktree → 项目设置 → 基线测试  ↓writing-plans（编写计划）  → 文件结构 → 任务分解 → 咬合粒度 → 自审  ↓subagent-driven-development（执行）  → 每个任务：实现者 → 规格审查 → 质量审查 → 完成  ↓finishing-a-development-branch（收尾）  → 验证测试 → 选择合并/PR/保留/丢弃
```

### #实战示例：构建一个 React Todo List

#### Step 1：会话启动

以 Claude Code / Cursor / Copilot CLI 这条接入路径为例，代理启动后会通过 `session-start` 钩子注入 `using-superpowers` 引导上下文。它看到的并不是一句简短提示，而是一段带 `<EXTREMELY_IMPORTANT>` 包裹的 bootstrap 文本，其中包含 `using-superpowers` 技能正文和必要说明。

```
<EXTREMELY_IMPORTANT>You have superpowers.[using-superpowers 技能正文 + 平台说明/警告]</EXTREMELY_IMPORTANT>
```

OpenCode 和 Gemini CLI 也会注入同样的“你拥有 superpowers”引导语义，但实现分别依赖插件 transform 与 `GEMINI.md` 引用，而不是这个 hook 文件本身。

#### Step 2：用户输入

用户说："Let's make a react todo list"

#### Step 3：brainstorming 自动触发

代理检测到这是"创建功能"，会先落到 `using-superpowers` 的规则：只要有 1% 的概率某个技能适用，就必须先调用技能；于是这里自动进入 `brainstorming`：

```
代理: I'm using the brainstorming skill to explore this design.Let me first check the project context...[探索项目文件、文档、最近提交]Before we dive in — some of what we're working on might be easier to explainif I can show it to you in a web browser. Want to try it?用户: No thanks代理: Got it. Let me ask a few questions to understand what you need.What's the primary use case for this todo list?A) Personal task managementB) Shared team tasksC) Learning/demo projectD) Something else用户: C, learning project代理: Should the todos persist across page refreshes?A) localStorageB) No persistence (in-memory only)C) Backend API用户: B[继续一次一个问题地澄清...]代理: Here's the design:**Section 1: Component Architecture**- App (root)  - TodoInput (add new todo)  - TodoList (display todos)    - TodoItem (single todo with toggle/delete)  - TodoFilter (all/active/completed)Does this look right?用户: Yes[继续下一个部分...][写设计文档并提交 → 自审 → 用户审阅]
```

#### Step 4：writing-plans

设计批准后，代理调用 writing-plans 技能，生成类似这样的计划：

```
# React Todo List Implementation Plan> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development**Goal:** Build a React todo list with add, toggle, delete, and filter**Architecture:** Single-page React app with component hierarchy**Tech Stack:** React, Vite, CSS Modules---### Task 1: Project Setup**Files:**- Create: `package.json`, `vite.config.js`, `index.html`, `src/main.jsx`- [ ] **Step 1: Initialize project**  Run: `npm create vite@latest . -- --template react`- [ ] **Step 2: Verify setup**  Run: `npm run dev`  Expected: Dev server starts on localhost:5173- [ ] **Step 3: Commit**  ```bash  git add -A  git commit -m "chore: initialize React project with Vite"  ```### Task 2: TodoItem Component**Files:**- Create: `src/components/TodoItem.jsx`- Test: `src/components/TodoItem.test.jsx`- [ ] **Step 1: Write failing test**  ...
```

#### Step 5：subagent-driven-development

代理读取计划，为每个任务派发子代理：

```
[派发实现者子代理执行 Task 1]实现者: DONE - Project initialized, dev server running[派发规格审查者]规格审查者: Spec compliant[派发代码质量审查者]质量审查者: Approved[标记 Task 1 完成，继续 Task 2...]
```

---

## 插件系统

### #多平台适配

Superpowers 并不是“每个平台一个完全独立插件工程”，而是**同一套 skills/ 与若干平台适配层**。如下：

平台接入形态Claude Code插件清单 + SessionStart hookCodex CLI / Codex App同一个插件包，App 额外读取 UI 元数据Cursor插件清单 + Cursor hookOpenCodeGit 插件 + 运行时消息 transformGemini CLI扩展清单 + 上下文文件GitHub Copilot CLI市场安装 + SDK 标准上下文注入Factory DroidREADME 中声明的市场安装入口
### #Codex 插件特殊配置

Codex 插件的 `interface` 字段主要定义了 Codex App UI 中的展示，但 Codex CLI / App 共享的是同一个插件包：

```
{  "interface": {    "displayName": "Superpowers",    "shortDescription": "Planning, TDD, debugging, and delivery workflows",    "category": "Coding",    "capabilities": ["Interactive", "Read", "Write"],    "defaultPrompt": [      "I've got an idea for something I'd like to build.",      "Let's add a feature to this project."    ],    "brandColor": "#F59E0B"  }}
```

### #跨平台钩子兼容

`run-hook.cmd` 是一个"多语言脚本"——在 Windows 上作为 batch 文件运行，在 Unix 上作为 bash 脚本运行。它还刻意使用**无扩展名**的 hook 脚本名，避免某些 Windows 环境对 `.sh` 命令做错误预处理：

```
: << 'CMDBLOCK'@echo offREM Windows: 找到 bash 并执行if exist "C:\Program Files\Git\bin\bash.exe" (    "C:\Program Files\Git\bin\bash.exe" "%HOOK_DIR%%~1" ...)CMDBLOCK# Unix: 直接执行exec bash "${SCRIPT_DIR}/${SCRIPT_NAME}" "$@"
```

另一个容易忽视的细节是：如果 Windows 上完全找不到 bash，它会**静默退出 0**。这意味着插件不会崩，但会失去 SessionStart 上下文注入能力。

### #版本管理

`scripts/bump-version.sh` 管理跨所有配置文件的版本同步：

```
# 查看当前版本./scripts/bump-version.sh --check# 更新版本./scripts/bump-version.sh 5.2.0# 审计：检查是否有遗漏的版本字符串./scripts/bump-version.sh --audit
```

配置文件 `.version-bump.json` 声明了哪些文件包含版本号；当前并不只覆盖 `package.json` 和两个插件文件，还包括 Cursor、Claude marketplace 与 Gemini 扩展：

```
{  "files": [    { "path": "package.json", "field": "version" },    { "path": ".claude-plugin/plugin.json", "field": "version" },    { "path": ".cursor-plugin/plugin.json", "field": "version" },    { "path": ".codex-plugin/plugin.json", "field": "version" },    { "path": ".claude-plugin/marketplace.json", "field": "plugins.0.version" },    { "path": "gemini-extension.json", "field": "version" }  ]}
```

---

## 技能设计哲学

### #"铁律"模式

每个核心技能都有一条不可违反的铁律：

技能铁律TDD没有先写失败测试，就不能写生产代码调试没有根因调查，就不能提出修复方案验证没有新鲜验证证据，就不能声称完成**违反文字就是违反精神。** 这句话切断了整个"我遵循精神而非文字"的合理化路径。

### #"合理化防范"机制

每个技能都包含：

- **Red Flags 表** — 代理可以自检的信号
- **Common Rationalizations 表** — 每个借口都有对应的反驳
- **具体的工作示例** — Good/Bad 对比
这种设计源于一个洞察：**AI 代理在压力下会找借口跳过纪律**。技能文档必须像一个严格的教练，预见每一种借口并提前堵死。

### #"人的搭档"语言

Superpowers 使用 "your human partner" 而非 "the user"。这是刻意的——它建立了代理与人类之间的协作关系，而非服务关系。代理应该：

- 在不确定时询问搭档
- 在审查反馈中保护搭档的利益
- 在外部审查与搭档的决定冲突时，优先考虑搭档

### #CSO（Claude 搜索优化）

技能的 `description` 字段是代理发现技能的关键。设计原则：

- 只写触发条件，不概述工作流
- 使用代理会搜索的关键词
- 第三人称撰写
- 以 "Use when..." 开头

---

## 贡献指南与质量标准

### #PR 模板要求

每个 PR 必须填写完整的模板，包括：

- 解决什么问题（必须是真实经历的问题）
- PR 改变了什么
- 是否适合核心库
- 考虑了哪些替代方案
- 是否包含多个不相关的变更
- Existing PRs 检查（必须看 open 和 closed）
- 测试环境表格
- 新 harness 的完整验收 transcript（如适用）
- 评估结果（前后对比）
- 技能改动的 rigor / adversarial testing 声明
- 人类审查清单

### #项目拒绝标准

- 添加第三方依赖
- 为"合规"重构技能
- 项目/个人特定配置
- 批量/喷洒式 PR
- 推测性修复
- 领域特定技能
- Fork 特定变更
- 捏造内容
- 捆绑不相关变更

### #新平台集成测试

新增平台支持必须通过验收测试：在新平台中打开干净会话，发送 "Let's make a react todo list"，brainstorming 技能必须自动触发。需要提供完整的会话记录。

---

## 深度实践建议

### #自定义技能

个人技能放在 `~/.claude/skills`（Claude Code）、`~/.agents/skills/`（Codex），OpenCode 还支持 `~/.config/opencode/skills/`；项目级技能则可放在 `.opencode/skills/`。

创建技能时遵循 TDD 流程：

- **RED：** 在没有技能的情况下运行压力场景，记录代理的违规行为
- **GREEN：** 编写最简技能解决这些具体违规
- **REFACTOR：** 发现新的合理化借口 → 堵住 → 重新验证

### #与现有工作流集成

Superpowers 的指令优先级是：

- 用户的 CLAUDE.md / GEMINI.md / AGENTS.md（最高）
- Superpowers 技能
- 默认系统提示（最低）
这意味着你可以在 CLAUDE.md 中覆盖任何 Superpowers 行为。例如：

```
# CLAUDE.mdDon't use TDD for configuration files.
```

### #调试 Superpowers

如果技能没有按预期触发：

- 先分清当前 harness 的引导路径：Claude/Cursor/Copilot 看 hook，OpenCode 看插件 transform，Gemini 看 `GEMINI.md`
- 检查 `using-superpowers` 是否真的进入了上下文
- 检查技能的 `description` 是否覆盖了正确的触发条件
- 查看代理是否在合理化跳过技能
- OpenCode 可额外检查插件日志；Windows 下若 hook 失效，还要确认 `run-hook.cmd` 能找到 bash

### #性能考量

- `using-superpowers` 技能在**每个会话**中加载，必须保持精简（<150 词）
- 频繁引用的技能目标 <200 词
- 其他技能目标 <500 词
- 使用交叉引用而非重复内容
- 代码示例只用一种语言（代理擅长移植）

---

## 写在最后

Superpowers 的本质是一套**行为塑造系统**。它不提供代码库功能，而是通过精心设计的 Markdown 文档，利用 AI 代理的上下文注入机制，强制代理遵循专业的软件工程实践。

**核心创新：**

- **技能即代码** — 文档就是行为约束，不是建议
- **铁律 + 红旗 + 合理化表** — 三层防线防止代理走捷径
- **子代理架构** — 隔离上下文，两阶段审查
- **跨平台统一** — 一套技能，多个代理平台
- **TDD 贯穿始终** — 从代码到技能本身
**适用场景：**

- 需要 AI 代理长时间自主工作的项目
- 需要高质量代码输出的团队
- 需要可预测、可审查的代理行为的工作流
**不适合：**

- 快速原型（brainstorming 流程会增加前期时间）
- 单文件脚本（工作流开销不值得）
- 不支持 bootstrap 上下文注入或技能发现机制的代理平台

如果你看到这里，那这篇文章对你还是有点帮助的，希望得到你的关注，获取更多有见解的内容，你的点赞，收藏，转发是我坚持写文的动力。
