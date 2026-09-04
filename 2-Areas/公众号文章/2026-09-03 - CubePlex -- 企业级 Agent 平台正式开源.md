---
title: "CubePlex -- 企业级 Agent 平台正式开源"
author: "酷博派"
publish_date: "2026-09-03 07:20:09"
saved_date: "2026-09-04"
source: "wechat"
url: "https://mp.weixin.qq.com/s/hj7jtM3su76GcX2yr8yuRA"
---
# CubePlex -- 企业级 Agent 平台正式开源
2026 年初，OpenClaw 火起来以后，公司里很快多了一批“养虾”的同事。有人养得很好，Agent 已经能接手不少日常工作；也有人折腾了很久，最后还是回到了原来的工具。

大家很快碰到了同一个问题。模型和系统内置的 Skills 只能处理通用任务，业务背景、内部系统的调用方式、例外情况的处理经验，这些只存在于团队内部，得有人一点点教给 Agent。一个同事调顺的流程，换个人接手，常常又得从头来一遍。

后来 Hermes Agent、WorkBuddy 等产品继续把 Agent 带进更多人的日常工作。我们也一直在关注和使用这些产品。个人 Agent 越来越好用，进入团队以后却还缺少一套稳定的组织方式。谁来维护和升级 Skills，MCP 连接由谁配置，普通成员能够使用哪些能力，这些事情不能再靠每个人各自维护一份配置。

这就是我们开始做 CubePlex 的原因。

今天，我们正式开源 CubePlex。CubePlex 是一套面向团队工作区的企业级智能体平台。它让团队集中管理 Agent 的 Skills、Memory 和 MCP 工具，并通过 Cloud Harness 与隔离 Sandbox 运行任务。

把个人经验放进 Workspace

企业里的 Agent 最终会学到很多只有团队内部才知道的东西。销售团队有自己的客户跟进方法，研发团队知道发布和回滚的顺序，财务、人力和法务也都有长期形成的处理规则。这些业务逻辑很少存在于某一个 SaaS 接口里，更多时候散落在文档、口头经验和一次次具体操作中。

Skills 适合保存这类工作方法。它可以告诉 Agent 应该读取哪些资料，按照什么顺序调用工具，结果需要满足哪些检查项。MCP 负责连接代码仓库、数据库和内部服务。Memory 则保存团队共同的背景和约定。

有了这些内容，还需要有人管理。CubePlex 的 Workspace 有明确的成员和角色。Workspace Admin 可以维护 Skills、Memory、MCP 和成员权限，Workspace Member 直接使用已经配置好的 Agent。普通成员不需要安装依赖，也不必知道服务凭据放在哪里。他提出任务时，Agent 会加载当前 Workspace 已经启用的工作方法和工具。

Skills 也有自己的版本。团队可以先在一个 Workspace 中试用内部 Skill，确认流程跑通以后再推广到更多工作区。管理员升级版本后，后续对话使用新的版本。业务专家负责把方法写对，平台管理员负责发布和维护，其他成员拿来完成工作。经验由此有了明确的归属，也有了继续修改的地方。

CubePlex 还提供个人、Workspace 和组织三个范围的 Memory。个人偏好可以留给个人，项目事实由 Workspace 成员共享，公司约定则可以放到组织范围。Agent 每次开始工作时，读取与当前用户和当前 Workspace 对应的内容。

这些能力共同组成了 CubePlex 的 Workspace。它会保存对话，也会保存团队允许 Agent 使用的知识、流程和工具。

桌面 Agent 留下的企业问题

桌面 Agent 很适合个人使用。它读取本地代码和文件，也能直接调用已经登录的浏览器、命令行工具和开发环境。用户授权一次，Agent 就可以开始工作。

到了企业环境，这种便利会带来新的管理问题。员工电脑里可能有环境变量、访问密钥和合同文件。Agent 可以访问什么，执行过哪些操作，哪些高风险动作需要确认，很难靠每个人分别维护自己的桌面配置来统一处理。

团队经验的管理也有同样的问题。Skill 放在某位同事的电脑上，其他人很难知道自己拿到的是不是最新版本。MCP 凭据由个人保存，人员变动后还要重新交接。Agent 做过的工作留在本地会话和目录中，另一位成员接手时只能重新恢复现场。

我们希望 Agent 在员工常用的入口里出现，同时把运行状态和执行环境放到团队能够管理的位置。飞书、Slack 或 Web 页面都可以是入口，Agent 本身需要由云端持续运行。

Cloud Harness 和 Sandbox

我们在[《Managed Agents Harness 架构与选择》](https://mp.weixin.qq.com/s?__biz=Mzg4MDU3NzA2Ng==&mid=2247485408&idx=1&sn=e390cbc096cefabc98c797d7a7355f8b&scene=21#wechat_redirect)中比较过两种方案。一种把 Harness 与 Agent 一起放进 Sandbox，任务结束后释放整个环境。另一种由控制面持有 Harness，需要执行代码和操作文件时再分配 Sandbox。

CubePlex 选择了后一种方案，并把它实现为 Unified Managed Agent Harness。

Cloud Harness 持有 Agent loop 和会话上下文，处理模型请求、工具调度与审批。Agent 等待用户、定时任务或外部事件时，长期状态仍然留在控制面。Sandbox 提供 Shell、文件、浏览器和本地进程，需要执行时才参与一次运行。

一条持续几个月的会话不必长期占着同一个运行进程。Sandbox 出现故障时，Harness 仍然保留已经完成的步骤。平台可以在执行前检查身份和权限，遇到需要确认的命令就暂停 Agent loop，等待成员决定是否继续。

在 CubePlex 中，每条进入平台的消息都属于一个真实用户。用户只能进入自己所属的 Workspace，也只能使用该身份获准访问的模型和工具。团队可以把成员邀请进同一条对话，共享消息历史和这条对话使用的 Sandbox；IM 频道也可以根据场景选择成员隔离或多人共享。

这套结构让 Workspace 成为团队使用 Agent 的组织单位，Cloud Harness 负责持续运行，Sandbox 则承担具体执行。

CubePi 取代 LangGraph

CubePlex 最初使用 LangGraph 构建 Agent runtime。随着系统变复杂，我们花在图节点、状态通道和序列化上的精力越来越多。

今天的通用 Agent 通常不会提前画好一张固定流程图。模型会根据上下文选择工具，读取结果，再决定继续执行还是结束。代码仍然要控制权限、持久化和异常处理，任务路径则由模型在 Agent loop 中动态形成。对这类运行方式，图运行时增加了不少没有直接服务于任务的结构。

因此我们实现了 CubePi，并用它替换 CubePlex 中原来的 LangGraph runtime。CubePi 的核心是一段可以直接读懂的异步 while loop。工具是普通函数，模型输出和工具结果通过统一的事件流返回。开发者可以顺着一次运行读下去，不需要在节点、边和回调之间来回跳转。

架构变简单以后，生产环境需要的机制仍然保留。CubePi 提供类型明确的 Middleware，可以在模型调用和工具执行前后加入权限、审批与观测逻辑。CubePlex 原先的 LangGraph Checkpoint 会随对话增长写入完整消息状态，I/O 为 O(n)。CubePi 改用 append-only，每一步只写入新增消息，Checkpoint I/O 相对于会话长度保持 O(1)。

工具数量增加时，CubePi 可以先向模型提供一份紧凑目录，需要时再加载对应的 MCP 工具。工具数组和系统 Prompt 在运行中保持稳定，不会因为动态加载工具反复破坏 Prompt Cache。长会话和大量工具因此更容易利用模型提供方的缓存机制，减少重复输入带来的成本。

CubePi 目前已经独立开源。它既是 CubePlex 的 Harness Core，也可以作为 Python Agent 框架单独使用。

一个可以交给团队使用的 Agent 平台

CubePlex 把 Agent 的工作入口、团队资产和执行环境放进一套系统。成员可以从 Web 应用发起任务，也可以在飞书、Slack、钉钉、Teams 或 Discord 中使用 Workspace 内的 Agent。无论消息从哪里进入，Agent 使用的仍然是该 Workspace 已启用的 Skills、Memory 和 MCP 工具。

任务需要操作文件或运行代码时，Agent 会进入隔离 Sandbox。生成的报告、表格、代码和网页可以作为版本化产物留在会话里，其他成员能够打开结果并继续修改。计划任务和 Webhook 可以在没有人守着聊天窗口时启动同一套 Agent 工作流程。

管理员可以配置模型和 Workspace 可用的工具。执行策略可以阻止命令，也可以要求成员确认后再继续。在 Kubernetes 部署中，平台还可以让长期凭据留在 Sandbox 之外，只在获准的网络请求到达出口时注入真实值。

这些能力现在已经进入开源仓库。团队可以用 Docker Compose 在一台机器上启动 CubePlex，也可以通过 Helm 部署到 Kubernetes，再接入自己的模型和内部服务。

自托管和开放协作

企业把业务流程交给 Agent 时，通常也希望自己决定数据、凭据和执行环境放在哪里。自托管因此是 CubePlex 的产品前提。团队可以阅读完整源码，检查 Agent 怎样调用模型、怎样保存状态，再按照现有基础设施调整部署。

开源还有另一个现实原因。Agent 仍在快速变化，新的模型、Skills 和 MCP 服务不断出现，不同公司使用的业务系统也相差很大。CubePlex 团队会继续维护平台的核心架构，社区可以补充行业 Skills、工具连接和部署适配。客户为自己的系统开发的能力，也可以选择留在内部。

我们选择 Apache-2.0，希望企业可以放心部署和二次开发，也希望 CubePlex 能够与正在形成的 Agent 开源社区一起演进。

CubePlex 这个名字

CubePlex 的名字来自数学中的立方复形。简单的方体沿着面对彼此连接，就能织出复杂而处处有序的空间。这个空间的好处有两个来源：一是连接——一个人养好的 Agent、一套经过验证的 Skill、一次完成任务的经验，都能在同一个空间里找到自己的位置，被更多人使用和改进；二是秩序——每个顶点只需遵守同样简单的规则，全局的优良结构便自动成立。

我们想做的正是这样一个空间：清晰的成员与权限、统一的 Workspace 规则、结构自带的边界，让团队的经验彼此连接，让复杂业务自然归位。CubePlex，让智能体升维思考，让复杂业务回归秩序。

从源码开始

CubePlex 的源码、部署说明和贡献指南已经公开。

CubePlex GitHub 仓库：https://github.com/cubeplexai/cubeplex

CubePlex 文档：https://docs.cubeplex.ai

CubePi：https://github.com/cubeplexai/cubepi

贡献指南：https://github.com/cubeplexai/cubeplex/blob/main/CONTRIBUTING.md

欢迎部署 CubePlex，也欢迎通过 Issue 和 Pull Request 参与项目。

关于

CubePi

原生支持异步的 Python Agent Harness 框架，专为高性能、高可读性及生产级持久化能力而设计。

https://github.com/cubeplexai/cubepi

CubePlex

CubePlex 是为团队构建的企业级智能体平台。Agent 的 Skills、Memory、工具、自动化任务和整个工作现场都在 Workspace 里持久保存，任务可以交接，经验可以复用，交付物以版本化产物留存。

https://github.com/cubeplexai/cubeplex
