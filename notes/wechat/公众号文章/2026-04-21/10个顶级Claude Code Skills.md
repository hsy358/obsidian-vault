---
title: "10 个顶级 Claude Code Skills，装上就删不掉！附真实使用场景和效果对比"
author: "码哥跳动"
publish_date: "2026-04-21 09:01:52"
saved_date: "2026-05-09"
source: "wechat"
url: "https://mp.weixin.qq.com/s/_04FWvqJwDfPhOcNJr__hQ"
---
# 10 个顶级 Claude Code Skills，装上就删不掉！附真实使用场景和效果对比
三周前，我还没装 Claude Code Skills，把团队的一个新功能模块直接交给 Claude Code 来写。

需求说清楚了，上下文给足了，然后我去泡了杯茶。回来看到 Claude 告诉我"已完成"——代码看起来很整洁，跑起来也没报错。我打了个勾，推上去了。

两天后，QA 测试发现了 5 个边界 case 没处理，其中一个在高并发下会导致数据丢失。

复盘的时候我发现：Claude 没有骗我，它确实完成了我"说的"需求。但它没有质疑需求、没有问边界条件、没有主动写防护测试——因为我没有让它这么做。

这就是 Skills 存在的意义。

Skills 不是给 Claude 更强的模型能力，而是**给它一套工作方法论**。它让 Claude 在开始写代码之前先想清楚，在"完成"之前先验证，在调试之前先系统化定位问题。

我这一个月装了二十多个 Skills，删掉了一半，留下了这 10 个。下面说说为什么。

## 先说怎么装

这 10 个里有 9 个来自同一个包：`superpowers`。这是一个开源的 Claude Code Skills 集合，目前 GitHub 约 600+ stars，有中文社区维护版本。

安装只需要一个命令：

```
/plugin install superpowers-skills@anthropics-claude-code
```

安装完后 `/reload-plugins`，所有 Skills 立刻可用。

如果你想用中文社区优化版（部分交互提示词有汉化）：

```
/plugin install superpowers-zh@jnMetaCode
```

第 10 个（`excalidraw-diagram`）单独安装：

```
/plugin install excalidraw-diagram@claude-plugins-official
```

好，进入正题。

## 10 个删不掉的 Skills

![](https://mmbiz.qpic.cn/sz_mmbiz_png/sgicmTR46ZvsoGPicnADd4IAQUibJEXRD7JvqBkP8NpdiaVyE8LSMK2MhPng2ibiciacMkfkmQFZBO3odqSkXz8Gic2LnORJSUa7R8CW7gcB9gCUaRg/640?wx_fmt=png&from=appmsg)
*图：10 个 Skills 按规划思考、质量保障、协作效率、工程配套四类分组一览*

#

Skill

核心价值

最适合的场景

1

`superpowers:brainstorming`在动手前想清楚

新功能、架构决策

2

`superpowers:writing-plans`把复杂任务拆碎

涉及多个文件的功能

3

`superpowers:executing-plans`执行不跑偏

按计划落地

4

`superpowers:test-driven-development`TDD 工作流

需要高质量覆盖的核心模块

5

`superpowers:systematic-debugging`结构化调试

线上 bug、诡异问题

6

`superpowers:requesting-code-review`5 个 Agent 并行审查

推 PR 前

7

`superpowers:dispatching-parallel-agents`多任务并行

跨模块批量改动

8

`superpowers:verification-before-completion`完工前检查清单

任何"完成"声明前

9

`superpowers:using-git-worktrees`分支隔离

功能开发 + 紧急修复并行

10

`excalidraw-diagram`自动生成架构图

需要图示的技术方案

### Skill #1：superpowers:brainstorming — 先让 Claude 想清楚再动手

这个 Skill 做的事很简单：**在你开口让 Claude 做任何有创造性的工作之前，强制先跑一轮头脑风暴**。

具体来说，它会让 Claude 先列出：

- 这个需求背后的真正问题是什么
- 至少 3 种实现路径和各自的权衡
- 可能的边界 case 和风险点
- 哪些假设需要你确认
然后 Claude 呈现方案给你选，你确认后才开始实现。

**为什么这让我删不掉？**

我之前有个习惯：拿到需求直接描述给 Claude，让它开写。大多数时候结果还行，但偶尔会遇到那种"写了两百行发现方向错了"的情况。

装了 brainstorming 之后，Claude 开始"讲理"了。上周让它给一个高并发接口做限流，它先列出了令牌桶、漏桶、滑动窗口三种方案，然后问我是要保护下游数据库还是保护接口本身——这是两个不同的目标，选择方案也不一样。

我之前根本没想到这个区别。

**调用方式：**

Skills 里明确写了：凡是涉及"创造新功能、设计方案、架构决策"的任务，Claude 应该自动触发 brainstorming。你也可以手动调用：

```
/brainstorming 我想给用户模块加上 OAuth2 登录
```

触发后 Claude 会输出一个结构化的分析报告，包含 3-5 个方案对比，以及一个明确的推荐意见（不是"各有优劣"的废话，是有立场的判断）。

**一个小提示：** 这个 Skill 有时候会显得"啰嗦"——尤其是简单的小改动，不需要三个方案对比。这是正常的，你可以在指令里加"小改动，直接执行不用 brainstorm"跳过它。技巧是：让大决策走 brainstorming，小任务直接说清楚就好。

### Skill #2：superpowers:writing-plans — 复杂任务不再令人窒息

有一类任务是这样的：你知道要做什么，但不知道从哪里开始，感觉每一步都依赖另一步，Claude 开始写之后也容易在中途迷路。

`writing-plans` 就是专门处理这种情况的。

**它的工作方式：**

给 Claude 一个复杂需求，它会先输出一份实施方案，包含：

- 5-10 个有序的实施步骤（每步都是明确的、可验证的动作）
- 每步的预期输出是什么
- 步骤之间的依赖关系
- 哪些假设需要你确认
**真实案例：**

我让它计划"给现有的 REST API 加上 gRPC 支持"，它输出了 7 步：

- 分析现有 API 接口，整理需要暴露的方法列表
- 安装 protobuf 工具链，定义 `.proto` 文件
- 生成 server stub 代码
- 实现 gRPC server，复用现有 service 层
- 处理错误映射（HTTP status → gRPC status code）
- 写集成测试
- 更新 Docker Compose 端口配置和 README
每步都具体到什么文件、做什么事。相比之下，我自己列的计划通常停在"2. 实现 gRPC 部分"这种层面，然后实际执行起来磕磕绊绊。

**为什么删不掉：**

大任务不再是一个黑盒。你可以在执行前检查计划，发现"步骤 4 在步骤 3 之前应该先确认依赖版本"这类问题，提前调整。这比事后补救便宜得多。

### Skill #3：superpowers:executing-plans — 执行的时候不跑偏

有了计划之后，`executing-plans` 接管执行。

这个 Skill 的核心逻辑是：**Claude 每完成一步，都必须验证这步的预期输出，再继续下一步**。

没有这个约束，Claude 有时候会在某步遇到问题，然后"绕过"而不是解决，最终输出看起来完整但有隐藏的破损。

**它的工作方式：**

```
/executing-plans[粘贴 writing-plans 生成的计划]
```

Claude 会按步骤执行，每步完成后明确报告：

- 这步做了什么
- 预期输出是否已验证（测试通过、文件存在、命令运行成功）
- 下一步是什么
如果某步失败，它不会跳过，而是停下来报告问题，等你给出指引。

**搭配使用：**

`writing-plans` + `executing-plans` 是一对最常用的组合。写计划用前者，执行用后者。这两个 Skill 可以让你把一个大任务切成两个阶段：先对齐方向，再稳定落地。

### Skill #4：superpowers:test-driven-development — 让 Claude 先写测试

这是我从"懂 TDD 是好事"到"真的在用 TDD"的转折点。

坦白讲，没有这个 Skill 之前，我让 Claude 写代码，它会先写实现，然后我问"帮我补测试"，它补的测试几乎都是在测它自己的实现，而不是在验证业务行为。测试覆盖率数字好看，但没什么用。

**tdd Skill 的工作方式：**

触发后，Claude 会拒绝直接写实现，而是先问：

- 这个功能的用户行为是什么（不是技术实现）
- 成功的标准是什么
- 边界情况有哪些
然后先写测试用例，让你确认这些测试是否覆盖了你真正关心的场景，再开始写通过这些测试的实现。

**真实效果对比：**

方式

结果

让 Claude 直接实现 + 补测试

测试覆盖实现路径，边界 case 容易漏

用 TDD Skill

测试覆盖业务行为，实现可以完全重写而测试不变

一个具体的例子：让 Claude 实现"用户余额扣减"逻辑。直接实现路线会写一个 `deductBalance(userId, amount)` 方法然后测它。TDD 路线会先问：负数余额怎么处理？并发扣减的顺序语义是什么？扣减失败应该报错还是静默失败？这些问题的答案会直接影响实现。

**调用方式：**

```
/test-driven-development 实现用户积分系统的兑换功能
```

或者在 CLAUDE.md 里声明对某个目录强制走 TDD，这样不需要每次都手动触发。

### Skill #5：superpowers:systematic-debugging — 结构化调试，不再随机乱试

这个 Skill 是我用得最频繁的一个，原因很简单：线上出问题的时候，随机应激（猜测、尝试、撤回）既慢又不稳定。

`systematic-debugging` 给 Claude 装了一套调试方法论，分四个阶段：

**阶段一：Observe（观察）**明确描述问题的现象、复现条件、已知的正常/异常边界。Claude 会拒绝在这步没做完之前猜原因。

**阶段二：Hypothesize（假设）**基于观察，生成 3-5 个可能的原因假设，按"如果是这个原因，会有什么其他表现"来排序（优先验证那些有预测力的假设）。

**阶段三：Test（测试）**为每个假设设计最小化验证方法，通常是加日志、写单元测试、或隔离复现。Claude 会给出具体的验证命令或代码片段。

**阶段四：Fix（修复）**确定根因后，再给出修复方案。修复方案里会说明为什么这样改（不只是把症状消掉）以及防止复发的建议。

**为什么这让我删不掉：**

有一次排查一个接口偶发超时问题，我原本已经准备让 Claude 直接"加个 timeout 处理就行了"。触发 systematic-debugging 之后，第一步观察阶段就发现：超时只在周三下午 2-4 点出现。这个规律直接把排查范围缩小了 90%，最后发现是定时任务和接口请求争抢数据库连接池。

"加 timeout"根本没有解决问题，只是掩盖了症状。

**调用方式：**

```
/systematic-debugging 现象：下单接口偶发 504，频率约 1%，集中在工作日下午日志：[粘贴相关日志]
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/sgicmTR46ZvtHJX9mKHODZF04nSaA1IcARlJLV7qqh15W4e290UIGXQdZnKwArfbAyFRWeKyw6FlXMUjaRqT4elI8Ihpx3usdobHBtkehWMY/640?wx_fmt=png&from=appmsg)
*图：Observe → Hypothesize → Test → Fix，每步有明确的输出和边界*

### Skill #6：superpowers:requesting-code-review — 5 个专项 Agent 同时帮你 review

这个 Skill 是 superpowers 里最"炫"的一个，但它的价值远不只是炫。

**它的工作方式：**

触发后，Claude 会并行召唤 5 个 subagent，每个负责一个专项：

- **安全审查 Agent**：检查注入、越权、敏感数据暴露
- **性能审查 Agent**：检查 N+1、不必要的同步调用、内存泄漏风险
- **正确性审查 Agent**：逻辑错误、边界 case、并发问题
- **代码风格 Agent**：可读性、命名、与现有代码风格一致性
- **测试覆盖 Agent**：测试是否充分、有没有遗漏的场景
5 个 Agent 同时工作，然后汇总成一份报告，每个问题有置信度评分和具体位置（文件名 + 行号）。

**真实效果：**

我上周用这个审查了一个支付回调处理模块（大约 300 行 Java）。人工 review 没发现问题，5 个 Agent 的报告里有 2 个高优先级问题：

- 安全 Agent 发现回调没有对请求来源做 IP 白名单校验
- 正确性 Agent 发现幂等处理有竞态条件（两个相同的回调同时进来可能都通过幂等检查）
这两个问题如果进了生产，一个有安全风险，一个会造成重复计费。

**置信度评分的价值：**

报告里的问题不是平铺直叙的，而是按置信度分级：`HIGH / MEDIUM / LOW`。高置信度的一定要修，低置信度的是"值得关注但可能是误报"。这让你知道把精力放在哪里，不会被一堆低价值建议淹没。

**调用方式：**

```
/requesting-code-review# 或者指定重点/requesting-code-review 重点关注并发安全和幂等性
```

![](https://mmbiz.qpic.cn/mmbiz_png/sgicmTR46ZvuR4mEjicmoknKoMD1pZWq3afdwvbsv3k3BO1BOaZ0jp6BYyIjqw5CJo7jIq3FXciahEcHRD7ZvzdgPLU8X9a2KEt5Bypibud19rw/640?wx_fmt=png&from=appmsg)
*图：5 个 Agent 同时工作，最终汇总成一份按置信度分级的 Review 报告*

### Skill #7：superpowers:dispatching-parallel-agents — 把小时级的工作变成分钟级

这个 Skill 的核心思想很朴素：**如果几个任务之间没有依赖，为什么要顺序执行？**

`dispatching-parallel-agents` 让 Claude 识别任务中的独立部分，然后并行分发给多个 subagent 同时处理。

**典型使用场景：**

- 给三个微服务同时加链路追踪
- 对一批文件做相同的重构操作
- 同时生成前端组件、后端接口、数据库 migration
**真实案例：**

我需要给一个系统的 6 个模块（用户、订单、支付、通知、库存、日志）都加上统一的请求入参校验。如果顺序执行，Claude 每个模块大概需要 2-3 分钟，6 个模块就是 15 分钟以上。

用 `dispatching-parallel-agents`，6 个模块的工作同时开始，总共花了不到 5 分钟。

**调用方式：**

```
/dispatching-parallel-agents我需要给以下 6 个模块加上统一的请求日志中间件：- user-service- order-service- payment-service- notification-service- inventory-service- audit-service每个模块独立，可以并行处理。
```

**注意事项：**

并行 Agent 之间没有共享状态，所以每个任务的描述必须是自包含的（不能依赖其他 Agent 的输出）。如果任务之间有依赖，用 `writing-plans` + `executing-plans` 更合适。

### Skill #8：superpowers:verification-before-completion — 让"完成"这个词有点分量

这是我认为最容易被低估的一个 Skill。

不装这个 Skill 之前，Claude 的"完成"有时候意味着"代码写完了"，而不是"这件事真的做好了"。差别在于：测试有没有跑、边界 case 有没有处理、文档有没有更新、配置有没有补齐。

`verification-before-completion` 的作用是：**在 Claude 宣布完成之前，强制跑一遍核查清单**。

**核查清单包含：**

- 测试是否通过（运行命令，不是"应该能通过"）
- 是否有硬编码的值应该提取为配置
- 错误处理是否完整（不只是 happy path）
- 是否引入了安全风险（SQL 注入、XSS、SSRF 等）
- 相关文档是否需要更新
- 代码是否有明显的性能问题（如全表扫描）
**为什么这改变了我的工作方式：**

装了这个 Skill 之后，我发现 Claude 的"完成"报告里开始出现这种格式：

```
✅ 单元测试通过（12/12）✅ 无硬编码配置⚠️  错误路径返回了 500，建议改为 400（参数错误）✅ 无明显安全风险❌ README 中的 API 文档未更新
```

这比一个简单的"已完成"信息量大得多。`❌` 和 `⚠️` 会在提交代码前让你看清楚还差什么。

**调用方式：**

这个 Skill 理论上应该在每次任务结束时自动触发，superpowers 里配置了对应的规则。但你也可以在任务完成后主动调用：

```
/verification-before-completion
```

### Skill #9：superpowers:using-git-worktrees — 真正的多任务并行

这个 Skill 很多人会觉得"我自己会用 git worktree，为什么要用 Skill？"

原因是：`using-git-worktrees` 不只是会创建 worktree，它会**建立一套配套的工作规范**：

- 为每个功能分支创建独立的 worktree（物理隔离，不影响主目录）
- Claude 在这个 worktree 里工作，不会动你主目录的任何文件
- 功能完成后，提供 merge、PR、或放弃的标准化流程
**为什么这很重要：**

没有 worktree 之前，我的工作流是这样的：功能开发到一半，线上出 bug，`git stash`，切分支，修 bug，`git stash pop`，回来继续。每次 stash 都是一次心跳加速的操作（万一冲突了呢）。

用 worktrees 之后：feature-A 在 `/projects/myapp-feature-a/` 目录里，hotfix 在 `/projects/myapp-hotfix-prod/` 目录里。两个终端窗口，两个完全独立的工作状态，互不干扰。

**调用方式：**

```
/using-git-worktrees 开始开发用户通知功能
```

Claude 会创建 worktree、切换到新分支、然后在隔离环境里开始工作。整个过程不需要你记那些 `git worktree add` 命令的参数。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/sgicmTR46ZvvTjoytDYMxhib8ch5gxNWenTfMoNI3NS0998GicAIbJotM7shXico4qEzjPliaOMycZN05YPUblV1aFo7MEUALOl6p690HXDFwDdo/640?wx_fmt=png&from=appmsg)
*图：左侧是焦虑的 stash 流，右侧是两个完全隔离的并行工作目录*

### Skill #10：excalidraw-diagram — 再也不手画架构图

最后一个不来自 superpowers 包，但我现在几乎每天都在用。

`excalidraw-diagram` 的作用：**用自然语言描述你想画的图，它生成可编辑的 Excalidraw 文件**。

**支持的图表类型：**

- 架构图（服务拓扑、模块依赖）
- 时序图（API 调用链、消息流）
- 流程图（业务逻辑、状态机）
- 对比图（Side-by-Side 技术对比）
- ER 图（数据库关系）
**为什么是 Excalidraw 而不是 Mermaid：**

Mermaid 的问题是：一旦生成就很难改。Excalidraw 是可编辑的——生成之后你可以在浏览器里直接拖动调整，改颜色、加注释、重新排版，最后导出 PNG 或 SVG。

而且 Excalidraw 文件是纯 JSON，可以提交到 git 仓库里，下次继续改。

**调用方式：**

```
/excalidraw-diagram 画一个电商订单系统的服务架构图，包含：用户服务、订单服务、支付服务、库存服务、消息队列（Kafka），订单服务同步调用库存服务，异步通过 Kafka 通知支付和用户服务
```

生成的是 `.excalidraw` 文件，用 Excalidraw 桌面应用或浏览器插件打开就能看到完整的图。

**实际效果：**

我之前用 draw.io 画一张类似的图大概需要 20-30 分钟（对齐、调间距、改颜色，这些都很费时间）。用这个 Skill，2 分钟内有一张可用的草图，再花 5 分钟微调，完成。

## 常见问题

**Q：superpowers 这个包免费吗？安装到哪里？**

A：完全免费，开源在 GitHub（`obra/superpowers-skills`）。安装后存放在 `~/.claude/plugins/superpowers-skills/` 目录里，所有项目都可以用。如果只想某个项目用，可以把对应的 `SKILL.md` 文件复制到项目的 `.claude/skills/` 目录下。

**Q：这些 Skills 会强制改变 Claude 的所有行为吗？**

A：不会强制。大多数 Skills 是在"有明确意图触发"时才生效，比如 brainstorming 在你说"帮我设计一个功能"时才激活，不是所有对话都强制跑。你也可以在指令里明确说"跳过 brainstorming，直接执行"来绕过。

**Q：这些 Skills 和 Claude 原生的 Hooks 有什么区别？**

A：Skills 是"方法论层面"的扩展，给 Claude 提供结构化的工作流程。Hooks 是"事件触发层面"的扩展，在特定工具调用前后自动执行 shell 命令。两者可以组合使用，比如用 Hook 在每次 `git commit` 前自动触发 `verification-before-completion`。

**Q：安装了这么多 Skills，会不会让 Claude 的响应变慢或者出现冲突？**

A：Skills 不会常驻内存，只在被触发时加载，所以不会影响正常响应速度。至于冲突，superpowers 里的 Skills 设计上是互补的，但如果你同时安装了来自不同来源的多个 Skills，偶尔会出现"两个 Skills 都想处理同一类任务"的情况。superpowers 的 `using-superpowers` 这个元 Skill 有优先级规则，一般能处理。

**Q：有没有针对特定语言或框架的 Skills？**

A：有，GitHub 上搜 `claude code skills java` 或 `claude code skills react` 能找到社区维护的语言特定 Skills。不过我自己的经验是，这 10 个通用 Skills 已经覆盖了工作流的大部分瓶颈，语言特定的可以按需补充。

## 最后说一句

我不认为 Skills 让 AI 变聪明了，它们让 AI 变**自律**了。

Claude 本身已经很聪明，它能写出复杂的代码、解释难懂的概念、发现非显而易见的 bug。但"聪明"不等于"可靠"——没有约束的时候，它倾向于走捷径，就像人一样。

这 10 个 Skills 本质上是一套工程规范的数字化：先想、再计划、再执行、测试覆盖、验证完成、clean branch。这套规范对人有效，对 AI 也有效。

装完这 10 个，去 GitHub 搜一下 `awesome-claude-code`，里面有 700+ 个社区 Skills 等着被发现。
