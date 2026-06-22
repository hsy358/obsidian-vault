---
title: 让 Claude Code 趁你睡觉就把活干完：使用6个核心命令
author: 码猿技术专栏
publish_date: '2026-06-15 14:04:50'
saved_date: '2026-06-15'
source: wechat
url: https://mp.weixin.qq.com/s/1WkaDrV4w6V9-btIY6ifCQ
type: wechat-article
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
  source_url: https://mp.weixin.qq.com/s/1WkaDrV4w6V9-btIY6ifCQ
description: Claude Code 不只是一个对话式编程助手。它有一整套内置命令，覆盖目标驱动的自主工作、定时轮询、批量重构、代码清理和故障诊断。用好这些命令，能从「你和...
timestamp: '2026-06-15T14:04:50'
resource: https://mp.weixin.qq.com/s/1WkaDrV4w6V9-btIY6ifCQ
tags:
- AI
- Claude
- 公众号
---
# 让 Claude Code 趁你睡觉就把活干完：使用6个核心命令
Claude Code 不只是一个对话式编程助手。它有一整套内置命令，覆盖目标驱动的自主工作、定时轮询、批量重构、代码清理和故障诊断。用好这些命令，能从「你和 Claude 一人一半」变成「你定方向，Claude 自己把活干完」。

下面逐一拆解六个核心命令的设计意图、适用场景和最佳用法。

> 本文基于 Claude Code v2.1.154+ 版本。命令的可用性和行为可能因版本、平台和订阅计划而异。在命令行输入 `/` 即可查看当前环境支持的所有命令。

**#ClaudeCode****#SlashCommands****#AI编程**

## /goal — 定目标，等状态

**功能：** 设置一个可验证的完成条件，Claude 会持续工作直至条件满足，不需要你每步都提示。

**解决什么问题：** 没有 `/goal` 时，Claude 做完一件事就停下来等你拍板。遇到跨多步的工程任务（修复 API 迁移的所有调用点、批量处理 issue 列表），你得一次又一次回来说「继续」。有了 `/goal`，你定好终点，Claude 自己走到头。

**机制：** 每轮结束后，一个小型快速模型检查条件是否成立。不成立就继续下一轮，成立则自动清除 goal，把控制权交还给你。

### 使用时机

- 模块迁移：把所有调用点从旧 API 改成新的，直到编译通过且测试通过
- 批量修复：处理 issue 列表直到列表为空
- 任何有明确「通过/失败」判定标准的多步骤工作

### 最佳用法

**写条件要可验证。** 「优化性能」不行，「测试通过率 100%」可以。条件越具体，Claude 越知道自己什么时候能做到。

**结合证据展示。** 让 Claude 展示测试输出、命令运行结果、截图，而不是让它说「看起来好了」。看完证据比你自己重新验证快得多。

**检查进度。** 用 `/goal` 不带参数可以查看当前 goal 的状态。条件满足后自动清除。

**提前结束。** 如果中途发现方向不对，再输入一次 `/goal` 可以清除当前目标。

## /loop — 定时查状态，睡觉也安心

**功能：** 在 CLI 会话内按设定的时间间隔重复执行一个 prompt，用于轮询状态或定时提醒。

**解决什么问题：** 部署要等 10 分钟、CI 跑半小时、PR 审核需要等。手动盯着输出页面不如让 Claude 自己每隔一段时间回来检查。`/loop` 让不离开终端就能持续关注。

**从官方文档：**「Scheduled tasks let Claude re-run a prompt automatically on an interval. Use them to poll a deployment, babysit a PR, check back on a long-running build, or remind yourself to do something later in the session.」

### 使用时机

- 部署轮询：每隔 N 分钟检查一次部署状态
- 长任务监护：定时查看长时间运行的构建或测试进度
- 定时提醒：过一段时间提醒自己做某事
- 配合 `/goal` 使用：先在 `/goal` 里定好完成条件，然后用 `/loop` 循环检查

### 最佳用法

**自定义 prompt。** 项目根目录放一个 `loop.md` 文件，`/loop` 会读取其中的内容作为默认 prompt。这比每次都手写 prompt 更省事。

**设置合理间隔。** 轮询间隔不要太短（浪费 token），也不要太长（信息滞后严重）。5-15 分钟是常用区间。

**配合其他调度方式。**`/loop` 是会话范围的轻量方案。如果需要跨会话持久运行，改用 Routines（Anthropic 云端执行）或 Desktop scheduled tasks（本地执行）。

**停止条件要明确。** prompt 里写清楚「当看到 State: Active → Succeeded 时就告诉我任务完成」，这样 `/loop` 输出有用结果而不是每次都扔给你无关输出。

## /batch — 拆任务，并行跑

**功能：** 将一个大型变更拆分成独立单元，每个单元在自己的 Git worktree 中并行执行。

**解决什么问题：** 跨整个代码库的大范围变更（如迁移框架、统一依赖版本），如果让 Claude 一次性处理，容易因代码库过大导致上下文窗口溢出、中间态冲突或单次修改量过大。`/batch` 把这些分解成互不依赖的小任务并行处理，每个任务在自己的隔离环境里跑。

### 使用时机

- 框架迁移：`/batch migrate src/ from Solid to React`
- 跨文件批量重命名、重构
- 统一多个模块的代码风格或依赖版本
- 大型代码库的并行修改任务

### 最佳用法

**任务是独立的。**`/batch` 要求拆分后的任务互不依赖。如果任务 A 的输出是任务 B 的输入，不适合用 `/batch`。这种用 `/goal` 顺次执行更好。

**指定范围。** 明确告诉 `/batch` 要处理哪个目录或文件范围，避免扩散到不相关代码。

**配合 /simplify 收尾。** 批量修改完成后，用 `/simplify` 统一清理所有变更文件的代码质量。

## /simplify — 改完即扫，代码不积债

**功能：** 检查变更代码的清理机会，并自动应用修复。四个 review agent 并行审查：复用现有工具、代码简化、效率优化、抽象层级合理性。

**解决什么问题：** 代码改完后，很少记得回去清理。减少重复、抽象适当、效率合理的代码，通常需要一个更高层面的审视。`/simplify` 自动做这件事，而且不找 bug——找 bug 用 `/code-review`。

### 使用时机

- 完成一个功能或修复后，作为「清理收尾」步骤
- 提交 PR 前的代码质量检查
- 代码评审意见的批量处理

### 最佳用法

**收尾流程固定步骤。** 形成习惯：写完功能 → 跑测试 → `/simplify` → 审查 diff → 提交。这个顺序最合理。

**指定目标。**`/simplify [path]` 可以针对特定文件或目录，不改整个项目。

**不要指望它找 bug。** 从 v2.1.154 起，`/simplify` 不再检查正确性问题。需要 bug 检测用 `/code-review`。

**对比旧版本。** 在 v2.1.154 之前，`/simplify` 等同于 `/code-review --fix`（找 bug 的同时也清理代码）。

## /doctor — 配置健康检查

**功能：** 配置诊断——检查无效键、schema 错误、安装状态。

**解决什么问题：** Claude Code 的核心配置文件（CLAUDE.md、settings、hooks、MCP servers、skills）加载失败时不容易排查。文件路径不对、格式错误、权限不足都有可能导致 Claude 忽略你的指令。`/doctor` 一次性检查所有配置组件的健康状态，告诉你哪里出了问题。

### 使用时机

- Claude 无视你的 CLAUDE.md 指令时
- MCP server 连接不上
- skill 不生效
- 新装 Claude Code 后的首次配置验证
- 修改配置后确认加载正确

### 最佳用法

**先跑 /doctor 再问为什么。** 遇到「Claude 不听话」的情况，`/doctor` 通常 5 秒内给出原因，比你翻文档快得多。

**配合 /context 使用。**`/doctor` 做健康检查，`/context` 查看实际加载到上下文窗口的内容（系统 prompt、memory 文件、skills、MCP tools 等）。两者搭配使用定位问题最快。

## /debug — 运行时诊断

**功能：** 启用调试日志，让 Claude 利用日志输出和配置路径来诊断问题。

**解决什么问题：** 有些问题不是配置加载失败，而是运行时行为异常——命令执行结果不对、工具链不通、路径解析异常。`/debug` 启动一个包含了调试日志的会话，Claude 能通过查看完整的日志输出来定位原因。

### 使用时机

- 某个命令或工具执行行为异常
- 工具链路径问题（找不到 Node、Python 版本不对）
- Claude Code 自身功能表现异常
- 需要提交 bug report（`/feedback`）前的诊断步骤

### 最佳用法

**试之前先确认基础配置。** 先跑 `/doctor` 确认配置加载没问题，然后再用 `/debug` 排查运行时问题。二者是先后关系，不是替代关系。

**提供具体描述。**`/debug [issue]` 的 `[issue]` 参数尽量写具体：「当我让它跑 npm test 时，输出显示找不到 jest 命令，按理说应该在 node_modules 里」。越具体，debug 越准。

**提交 bug 前必做。** 如果 `/debug` 发现是 Claude Code 自身 bug，用 `/feedback` 提交 report，debug log 会自动附上。

## 工作流搭配建议

这些命令不是孤立的。组合使用的效果远好于单独用任何一个。

### 定目标 + 批量改 + 清理收尾

```
 /goal: 迁移所有组件从 Vue2 到 Vue3，编译通过且测试覆盖 90%+  → Claude 自主执行，每轮自动检查条件  /batch migrate src/components/ from Vue2 to Vue3  → 大范围并行迁移  /simplify src/components/  → 改完后自动清理代码质量
```

### 定时轮询 + 目标驱动

```
 /goal: 部署到 staging 并确认健康检查通过  → 定好终点/loop: 每 5 分钟检查一次部署状态，告诉我什么时候完成  → 定时轮询，执行期间去做别的事
```

### 排查流程

```
 Step 1: /doctor          → 配置健康检查（CLAUDE.md、MCP、settings）Step 2: /context         → 看实际加载了什么内容Step 3: /debug [问题]    → 启用调试日志定位运行时问题Step 4: /feedback        → 确认是 Claude Code bug 后提交报告
```

---

## 参考来源

- Claude Code 官方命令文档： https://code.claude.com/docs/en/commands
- `/goal` 命令详解： https://code.claude.com/docs/en/goal
- 定时任务与 `/loop` 文档： https://code.claude.com/docs/en/scheduled-tasks
- 配置调试与 `/doctor` 文档： https://code.claude.com/docs/en/debug-your-config
- Claude Code 最佳实践： https://code.claude.com/docs/en/best-practices
