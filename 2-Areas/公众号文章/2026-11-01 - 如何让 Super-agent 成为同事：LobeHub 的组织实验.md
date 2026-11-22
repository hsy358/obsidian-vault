---
title: "如何让 Super-agent 成为同事：LobeHub 的组织实验"
author: "赛博禅心"
publish_date: "2026-11-01 23:38:21"
saved_date: "2026-11-22"
source: "wechat"
url: "https://mp.weixin.qq.com/s/QVu2luIrRTtNvsH-U65A8g"
---
# 如何让 Super-agent 成为同事：LobeHub 的组织实验
昨天做了一份动态图解《[DeepSeek 的 Super-agent 架构](https://mp.weixin.qq.com/s?__biz=MzkzNDQxOTU2MQ==&mid=2247522173&idx=1&sn=b0e1b69edd6d0be1f39fde36d7d0240b&scene=21#wechat_redirect)》，然后便看到 Max（前段时间加入了 LobeHub）发了个朋友圈

![](https://mmbiz.qpic.cn/sz_mmbiz_png/jXSGuwJvpdj3YqsspOORISjGpG9P1GforHN4rNy6kJFlawUzlYBeOcbGZNlnLGojmITx2sRYEIHgryNXhzbCicic9Dyjia9OAERjuCfvgTlocM/640?from=appmsg)

于是，今天傍晚的时候，便约了他们的创始人文彬聊了下，也请教下他们：**如何将类似 super agent 的东西融入工作，让一群人协作产出**

**背景补充**LobeHub 是一款知名的 Agent 工具，拿了两个非常头部机构的投资。在 DeepSeek v3.2 发布的时候，也用的 LobeChat 作为工具调用的演示

![](https://mmbiz.qpic.cn/sz_mmbiz_png/jXSGuwJvpdia7aFPA7RUnp70wu0C6yjklug7S0iaU3Fc9H1g5Gsme5Sqrseadq8Zt8nBvp3PoafDm0ZNhuXKuHTX3bMjSnic2QOFvjP3dSDR4o/640?from=appmsg)

他们也一直在探索 Agent 的原生使用方式，比如让 Agent 集体到 Discord 群里上班、自动接活、写代码、背锅（划掉

对了...在探索之外，我非常喜欢他们对于「自动验收」的探索：**Acceptance**，在 Agent 干完活后，会会自己去真实的产品里点一遍，把截图、录屏整理成一份验收报告。而人只要看这份汇报的 PPT，就可以判断过，还是不过（后面细聊）

![](https://mmbiz.qpic.cn/mmbiz_jpg/jXSGuwJvpdh5gRgHT672ECQIjXHyYwXROFWvHCxicE2PnYVOdFPD7526b5CiaxkDwn8nsmHicbTyQ8yEyhRsVZNwVYgbyEM07wPrEcZ8XOb4HM/640?from=appmsg)
看 ppt 给评级，非常真实 hhhhh

---

## 协作的卡点，在交接

上一次和文彬聊天，还是在外滩大会的圆桌上（minghao 是主持人），当时便在感慨一切都太快了。现在只过了两个月，效率又有了天翻地覆的变化（Opus 5.5 确实牛逼）

但我们也发现，虽然 Agent 让每件事儿的实现都变快了，但任务之间的沟通成本并没有被压缩：**团队协作，卡于交接**

团队慢在交接- 过去现在调研转述设计转述开发调研转述设计转述开发一件事走完的时间调研、设计、开发都快了，中间两次转述还是那么长LobeHub 把这里的时间黑洞分为三类：**执行类**：比如我想把某项工作交给张三，需要进行背景同步、任务说明，完了还得验收工作成果，这些耗时的事儿恰好也是 Agent 最为擅长的，可以都给 Agent
- **决策类**：等需要拍板做决定的时候，通常需要支撑材料的东西摆在眼前，人来做最后决定。这时候 Agent 可以在工作的过程中提前整理好，供决策时直接拿出来
- **盲区类**：工作的过程中经常会有遗漏了的东西，比如鬼知道在哪里有个兼容性 bug，平时没人发现，但等到了某个节点后就炸了。这一类问题靠 Agent 按周期主动巡检，发现异常就上报
这三类问题从不同方向消耗了团队的时间，而通过对这三个问题的解决，便可以有效提升一个 agentic 团队的效率

---

## 主动，约束自职责

我们首先要知道：**人的注意力是极为有限的**倘若在人机协作的过程中，Agent 无论干什么都插一嘴，那么很快就会把人的注意力吃光

因此，Agent 作为人机协作中的一员，就势必要理解人的不足之处，既要随时在线，也不能过于主动的干扰对话：**Agent 需要在它的职责边界内完成主动**

对此，LobeHub 的探索与 DeepSeek Harness 的做法相仿，先通过规则进行过滤（关键词/频道/...）然后再交给模型判断（通过 Agent 本身的职责状态，判断要不要管）

此外，Agent 还会每小时还会把频道巡一遍，看看有没有哪些事儿被漏下来。就比如一天晚上，文彬在群里看了眼训练页，随口说了句“这个 UI 太 vibe 了，得想想怎么 refine”，然后大家各忙各的

**55 分钟后，设计 Agent 自己把这事接了过来，挑出三处问题，当晚交了改版稿**

Agent 会自己接活 · 10 月 23 日晚- 20:0021:0022:0023:0024:00Arvin：这个 UI 一眼看上去还是太vibe 了，得想想怎么 refine55 分钟设计 Agent 自己接手：挑出三处问题交出改前改后对比稿每小时巡一遍频道，归它管的事就接过来
## 如何保持 Agent 的持续在线

Agent 要当同事，首先得一直在线，不会被热心的保洁阿姨和上电脑盖子倘若 Agent 和某台机器绑在一起，当机器自动更新的时候，在跑着的任务就完了。因此我们不光要考虑怎么 @ 对应的 Agent 接活，还得让他能够稳定运行被 @ 只是入口运行环境关掉电脑，任务照样跑组织空间一个 Agent 学会的，全组都能用权限审计出了问题，找得到负责的人验收完成以人的验收为准@ 群聊入口四层都垫好，Agent 才接得住活对此，LobeHub 和 DeepSeek 想到了一起：把 Agent 的循环、会话状态、执行环境拆开来放（2025 年 9 月开始做，今年 1 月随 2.0 上线）我还挺好奇的，他们是如何想到这点的答：被逼的LobeHub 很多服务是跑在 Vercel 上的（俺也一样）然后 Vercel 的云服务单次执行最多 300 秒，远不足以支撑 Agent 的长程调用，于是他们把每一步（调一次模型或工具）都拆成一次单独调用，步和步之间靠队列和 Redis 推进一次后台调用最长 300 秒下一步已完成调模型调工具调模型调工具调模型队列 + Redis 记着：走到第每一步单独调用一次，步和步之间靠队列往前推同理，工具也没法在 Vercel 上跑，那么就把工具调用被发去 AWS 的沙箱执行，再把结果传回来：**Agent 自己意识不到这件事，它以为自己就活在沙箱里**在这种结构下，如果要切换运行电脑，本质上只是换一个执行工具的地方Remote Tool CallingAgent 循环Vercel我在沙箱里干活云端沙箱AWSMac mini你的电脑~/project电脑上的文件夹工具调用换一个执行工具的地方，就接上了你的电脑现在，这套架构十分稳健，每天承受几万次 Agent 执行
## 和 DeepSeek 不一样的两处

聊到这儿，我问文彬：LobeHub 的探索里，和 DeepSeek 不一样的地方在哪？
### 第一个是 Router

作为背景，DeepSeek 用一个常驻的 Router 统一接活、再分给下面的 Worker，可中间的事全塞进一个 Router，下面干的咋样是很难看清的，更不知道从哪插手于是，LobeHub 在这里的探索是：**每个 Agent 都得有自己的岗位，名字、职责、记忆和工具都是它自己的**之所以要把这些内容仔细拆开，是因为核心的运行环境和输出产物的回复要求不一样（不是模型能力不够或者工程上的问题）就比如设计师把排版规范、风格参考、素材流程做成一个专用 Agent，其他人在寻求设计帮助的时候，就能获得即时反馈
![](https://mmbiz.qpic.cn/sz_mmbiz_png/jXSGuwJvpdhhibFVErmz64G6akJjQ7x1sxr7O6DUr0e8iaZVVE9VdicP6pUCMbwSicnklB8k4gCE5ebPCejl435v9Km6xnzL56kTFnAsg78w0Rc/640?from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/jXSGuwJvpdguDk89J9cibvPu8AMmhgraQS25XtiajWZibJlJmZkFybxXW5747OljibbkroZBticYCHiaibxibhntFHOM6XWyp7hsicpdz3epg5xIqiabg/640?from=appmsg)
左右滑动查看 · 共 2 张当然，你还可以做一个 Deck Agent，这样 BD 要做客户案例时直接跟它说，就省掉了排队等设计的时间每个 Agent 一个岗位 · 能力留在组织里Deck Agent设计能力 + 执行环境设计师BD排版规范风格参考素材流程新加一个制造业客户案例对客页面设计师沉淀一次，BD 之后随时直接用
### 第二个是直通

作为背景，DeepSeek 的设计里，同一个话题的后续消息可以绕过 Router，直接送到正在干活的 WorkerLobeHub 也试过类似的做法，结果群里的干扰一下子多了起来，相当于人越过主管，直接微操干活的 Agent（凯申行为）于是，LobeHub 把汇报分成了三层：第一层，每个人一个 Personal Agent，替人过滤信息
- 第二层，每个项目一个主管 Agent，负责派活和验收
- 第三层，才是 Claude Code、Codex 这些干活的执行 Agent
**人只听自己的 Personal Agent，活由各个项目的主管 Agent 去派**

第二个是直通- 产品Personal Agent设计Personal Agent工程Personal AgentBDPersonal Agent过滤：只带回你关心的LobeHubClaude CodeCodex生态组件CodexLobe Design增长运营Claude CodeSEO Agent第 1 层Personal第 2 层主管第 3 层执行人只听自己的 Personal Agent，活由主管 Agent 去派（在 LobeHub 的组织里面，写代码的叫 Dario...奇怪的恶趣味）人要是想中途插手，通过就在 Task 卡片上开工单，让 Agent 去执行。Agent 能力还弱的时候，人坐主驾；Agent 能力强了，人就退到副驾，负责审核汇报只走主管 · TaskT-1271用量页的积分改成显示美元主驾驶副驾驶人SAgent负责审Agent 能力Agent 强了，人就坐到副驾驶，负责审
## 让 Agent 之间直接交接

倘若交接的两头都是 Agent，上下文就能原封不动地递过去，而在 LobeHub 内部已经跑起来了就比如在之前的一次迭代里，上游项目的主管 Agent 发现，暗色主题只能硬改全局样式，于是直接给组件库 lobe-ui 的主管 Agent 提了需求；第二天，lobe-ui 加好组件、自动发版，再回头通知上游升级Agent 之间直接交接 · 10 月 15–16 日agent-foundry上游项目的主管 Agentlobe-ui组件库的主管 Agent10 月 15 日10 月 16 日提需求：支持注册自定义中性色加组件registerLobeNeutralRelease CI 自动发版6.0.1通知升级升级，删掉临时覆盖两天，三条消息，两个项目的主管 Agent 直接谈完
## 新的瓶颈：验收

但随着 Agent 干活越来越快，人验收的速度却没跟上，团队的瓶颈便挪到了验收这里文彬跟我说，他已经三个月没在本地起过 dev 了：看完 Agent 交上来的验收报告，没问题就直接合，开发速度至少快了 `3 到 5 倍`（说起来，我这台过完年买的电脑，到现在也没装 IDE，后台放了台 Mac mini 挨个验收，结果用飞书发给我）至于 Agent 怎么验收？他们整了个非常有意思的验收工具，**叫 Acceptance（已开源）**
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/jXSGuwJvpdiaibrWZ1njicWrvibu49icy1AfS9RUpC9pcY8iaAdlEXsJkvFXnf0L07dwIiaRicGWMXucj4IfiaVv9c4xicw7dkPHx0NvibXAm5bcOcV9Jc/640?from=appmsg)
具体来说，有以下的功能Agent 先把一条需求拆成几个看得见的检查项，再到真实的产品里逐项去跑，附上截图、录屏和日志
- 人可以整体通过，或者部分打回，负责的 Agent 会收到推送，然后去改
- 每次打回，都会沉淀成一条标准，Agent 下次交付之前先自查

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/jXSGuwJvpdjZ5b3hBomwlHqPwabujdGOibORO2sib6odmFibhOdZM88EQJenHNvdibRB4I5bEW8JQVkcKN9Kb7hJk9nSTMj9ZXqYA5AeEqdKdGU/640?from=appmsg)

---

## 组织如何自己变聪明

与许多先进团队一样，LobeHub 也在先用飞书...啊不是，开始探索 Agentic 组织，团队的经验会被写进 Agent 的任务和标准里，每天自我迭代

甚至 Agent 干活时遇到问题，还会随手吐槽一句（LobeHub 管这个叫 Agent Vent）：每天有个任务把吐槽聚类、建 Task 去修，第二天再对比。10 月 29 日那天，新增的上报从 84 条降到了 49 条

组织自己变聪明 · Agent Vent- Agent 吐槽每日巡检建 Task 修次日对比新增上报high 级 32 → 1110 月 29 日：新增上报从 84 条降到 49 条harness 也是这样调出来的：Lobe Agent 自主优化 harness 之后，在 FrontierHarness 上的通过率为 `70%`，单任务成本中位数为 `1.68` 美元（Codex 为 66.7%、3.47 美元，Claude Code 为 63.3%、18.34 美元）组织自己变聪明 · FrontierHarness通过率单任务成本（中位数）LobeHubCodexClaude Code自己优化 harness 后：70% 通过，单任务 1.68 美元
## 组织也有自动驾驶分级

LobeHub 把 AI 组织的演进，看作把人一步步从执行里拿掉的过程，并像自动驾驶一样分了五级：**L1 问答工具**：问一句答一句，关掉窗口就结束
- **L2 个人助手**：能帮个人干活，但能力跟着个人走，同事用不上
- **L3 团队成员**：人和多个 Agent 在同一个现场协作，能 @、能派活
- **L4 自治业务单元**：Agent 之间自己接力，人只设目标和边界
- **L5 自演进组织**：组织在运行中自己改进，人只管方向和担责
上面提到的交接问题，便就是大家在 L2 时遇到的卡点：虽然每个流程都被 Agent 提速了，但靠人还是无法做到高效的转述和对齐

组织也有自动驾驶分级人负责的交给 Agent 的应答工具个人助手团队成员自治业务单元自演进组织LobeHub 现在正在迈进人一层层交出执行，最后留下方向和担责

LobeHub 认为自己目前在 L3，项目之间直接提需求，已经有了 L4 的雏形；再往后，他们希望各家企业部署的 Agent 能相互协作、对接&实现需求

---

## 最后

以上内容，便是对谈后的总结，如果你也在探索如何让 Agent 充分的参与团队中的分工、交接以及汇报工作，或许能提供一点帮助

同时，**这里非常推荐大家看看 Acceptance，也是开源的**，让你的 Agent 对开发后的成果进行自检，更好地完成丝滑的人机交互
