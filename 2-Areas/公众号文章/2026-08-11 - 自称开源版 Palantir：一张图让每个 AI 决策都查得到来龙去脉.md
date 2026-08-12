---
title: "自称开源版 Palantir：一张图让每个 AI 决策都查得到来龙去脉"
author: "Hey AI Coder"
publish_date: "2026-08-11 17:10:47"
saved_date: "2026-08-12"
source: "wechat"
url: "https://mp.weixin.qq.com/s/Z9hkuWNY01mg5SHBnMRfZw"
---
# 自称开源版 Palantir：一张图让每个 AI 决策都查得到来龙去脉
# ![](https://mmbiz.qpic.cn/mmbiz_png/YeiaeCrb9vmQFd3vGyQNffGu9yhkX280zrqcZB9tnwfUFUiap8HicCEuKqHkaRdLwySJVIxFjQnicou95Utccl2NQw2CgRtdFBDvQLicUafZpjRo/640?wx_fmt=png&from=appmsg)

## 一个让老板后背发凉的问题

你是银行里搞 AI 平台的工程师，团队用大模型做贷款审批。模型批了笔贷款，流程走完，钱出去了。半年后监管上门：**"解释一下这次审批为啥通过，依据是啥，数据哪来的？"**

你打开日志——空的。向量数据库里就一堆数字，谁也说不清这堆数字到底代表啥。这真不赖工程师，是现在的 AI 架构天生就没带"账本"这功能：模型记的是"相似度"，不是"事实"；做决定的过程既不解释、也查不了账。

今天要聊的 Semantica，就是冲着这个坑来的。

**Github:**

> https://github.com/semantica-agi/semantica

## 它到底是啥：给 AI 装"行车记录仪"的开源基建

![](https://mmbiz.qpic.cn/sz_mmbiz_png/YeiaeCrb9vmSPLXB6icuEgfqtHbMQB9y7nCZr9zcUbVlESXs27elcNfBD0Ln6Vdib7JIl8mk9wXMGaic62icEGsYDmSk858dU82RGu90AQibmGjicQ/640?wx_fmt=png&from=appmsg)
Semantica 官网自己说它是"开源版 Palantir"。Palantir 是啥？是美国情报圈和金融巨头在用的那套死贵的决策分析系统。Semantica 的想法是，用开源的方式把它的核心本事做出来：**把企业数据吃进来，抽成一张"关系图"，然后在这张图上面做推理、做决策记录，全程留痕**。

项目在 GitHub 上用的是 MIT 协议，4.5k Star、2,232 次提交，Python 包在 PyPI 直接 `pip install semantica` 就能装，当前版本 v0.6.0。代码量是真不小：347 个 Python 文件、大概 15 万行，配套有 247 个测试文件、约 7.4 万行。

它的核心想法，浓缩成三件事来讲。

## 第一件：把"查资料"升级成"查关系"

![](https://mmbiz.qpic.cn/sz_mmbiz_png/YeiaeCrb9vmQQtyYcGuzcd7FpPnhjQRHCsriaYKKxcMQD9NSOZiaf768upqeULQibiaSjZrQvrsjeVt8GIEgNLdQGNxzMqJbYlCs2XNDicBqkn1A0/640?wx_fmt=png&from=appmsg)
传统那套大模型知识库（也就是 RAG），你可以把它想成一个装满卡片的档案柜。你问"谁是这单合同的甲方"，它按关键词把最像的卡片翻出来递给你，但卡片和卡片之间是断开的，谁跟谁有关系，它不知道。

Semantica 干的事是**把知识织成一张网**，官方叫法 Context Graph（上下文图）。每个公司、每个人、每份合同、每次事件，都是图上的一个"节点"，节点之间有带类型的"连线"——谁给谁干活、谁签了哪份合同——线上还能挂时间和来源。

（代码位置：核心类 `ContextGraph` 在 `semantica/context/context_graph.py:413`，节点和边的数据结构里都带 `valid_from/valid_until` 这俩时间字段。）

这张网带来的能力，是"查关系"而不是"查相似"：**一个人和一份合同之间隔着 3 层关系，图遍历能找出来，但向量搜索永远发现不了。** 它还支持"时间旅行"——`state_at("2024-01-01")` 能直接调出某一天的图长啥样，历史随便回放，不用重新跑一遍。

## 第二件：每次"拍板"都记成账本里的一条

这是 Semantica 最特别的设计：**AI 的每一个决定，不是一行日志，而是图里的一个"一等公民"节点。**

（代码位置：`record_decision()` 在 `context_graph.py:2445`，写入时通过 `_add_decision_to_graph()`（context_graph.py:2923）把决策变成图里一个 `type="decision"` 的节点，然后连上三类边：决策涉及了哪些实体、属于哪个业务类别、是谁做的。）

记录一次决策，不是存一行字就完事了。它还支持：

- • `add_causal_relationship()`：把"贷款申请 → 审批 → 定利率"串成一条因果链
- • `trace_decision_chain()`：从最终决定一路往回追，追到最初的根因
- • `find_similar_decisions()`：按语义找类似的历史先例
- • `check_decision_rules()`：用规则集做合规闸门，不合规的直接拦下
**决策节点 + 因果边 + 先例搜索**，这三个一组合，就把"AI 为啥这么做"从玄学变成了可查询的数据库问题。这就叫 Decision Intelligence（决策智能）。

![](https://mmbiz.qpic.cn/mmbiz_png/YeiaeCrb9vmT3HvyYFpdslw3ibTM4ic1kge85GuZZlwDW0SJUYpC8ical327ibECAEZuS39Uj2TpnzVrNp15ZMkG83sPGk3HJgJgUz0Nu8cE8khc/640?wx_fmt=png&from=appmsg)

## 第三件：一本"撕不掉的账本"

光记录还不够，还得**保证这些记录没被动手脚**。这里用了一个很硬核的工程手法：**哈希链**。

（代码位置：`ProvenanceManager._save_entry()` 在 `semantica/provenance/manager.py:149-187`。每次写入新记录，先读一下账本链头，把上一条的校验和 `previous_checksum` 缝进当前这条，再算自己的校验和。）

你可以把它想成**每页都有页码、还把上一页的摘要印在本页页脚的连环账本**。中间任何一页被偷偷改过，页码就对不上了，`verify_chain()` 一查就露馅。还有个更妙的"墓碑"设计：被废弃的事实不是删掉，而是打个"作废"的戳（代码位置：`schemas.py:146-152`）——这样审计的人能证明"这条事实存在过、后来被复核、然后被撤销"。**删了，和从没存在过，是完全不一样的两回事。**

导出格式用的是 W3C 的 PROV-O 标准（provenance 模块大概 1,300 行手工构造 RDF 三元组，manager.py:1203），这是监管机构认的格式。

## 加分项：不靠大模型的"家谱推理"和"对稿"

Semantica 里有一块特别让人喜欢的模块：**确定性推理，压根不需要调用大模型。**

最典型的是 Datalog 推理器（`semantica/reasoning/datalog_reasoner.py:39`）。Datalog 是一种又像 SQL 又像逻辑的查询语言，最出名的用处是**家谱推理**：`parent(tom, bob)` + `parent(bob, ann)`，再定义一条"祖先"规则，它就能推出 Tom 是 Ann 的曾祖辈。它的实现是纯 Python 的 semi-naive 求值（derive_all() 在 datalog_reasoner.py:242），配有 40 多个测试用例来验证递归规则。**推理过程的每一步都能解释得出来**，不依赖任何 LLM——在受监管的场景里，这个性质简直跟金子一样值钱。

还有两块"编辑部日常"也做得很扎实：

- • **冲突检测**（`semantica/conflicts/conflict_detector.py:95`）：同一个实体，来自两个不同数据源的说法对不上？不覆盖，先给你标出来。默认有个 `MANUAL_REVIEW` 策略，说白了就是"拿不准就交给人来定"。
- • **去重**（`semantica/deduplication/duplicate_detector.py:322`）：用并查集把"同一个人的不同写法"合并成一坨，省得搞 O(n²) 的重复扫描。

## 工程上怎么支撑"随便换库"

这套系统能在 8 个向量库、4 个图数据库、5 个 RDF 三元组库之间无缝切换，靠的是**分层抽象 + 一堆设计模式**（策略、工厂、适配器、懒加载代理这些）。存储这块是"polyglot"（多语言存储）设计：属性图、RDF 三元组、向量库这三层各自独立抽象（代码位置：`vector_store/vector_store.py:112` 定义了 8 个后端常量，`graph_store` 负责分发 Neo4j/FalkorDB/AGE/Neptune 这几个）。

打个比方，**同一套电路，能插不同国家的插座**。本地开发时用零依赖的 SQLite 或者内存版就能跑，生产环境挂上 Neo4j + Qdrant，代码一行都不用改。官方给过一组性能数据（v0.5.0，11.8 万节点的生产图）：节点搜索从 24ms 优化到了 0.004ms，快了差不多 6,000 倍。

## 老实说：宣传和现实之间有几道缝

分析代码的时候，我发现了几个"宣传走在实现前面"的地方，值得大家留意：

- 1. **Rete 推理引擎是个骨架**。README 里提到了 Rete 网络推理，但代码里 `AlphaNode._matches()` 和 `BetaNode._can_join()` 恒返回 True（`semantica/reasoning/rete_engine.py:79-104`），相当于"网络搭好了、匹配逻辑还没填"。真正能用的是 Datalog 推理器。要上生产合规的话，请用 Datalog，别碰 Rete。
- 2. **worker.py 在空转**。`SemanticaWorker` 的循环就是在 `time.sleep(5)`（worker.py:39-46），没有真正的任务队列，注释里自己也承认了"待实现"。
- 3. **server 的 /build 接口是个占位**。返回"已接受"，但并不真去执行。
- 4. **"建图不依赖 LLM"得分情况看**。官方宣传说"No LLM required"，这个说法在**推理、溯源、冲突检测、去重**上完全成立，核心依赖里也确实不含任何 LLM SDK。但如果你输入的是**原始文本**，`GraphBuilder` 默认的实体抽取方式 `ner_method="llm"` 还是会去调大模型（graph_builder.py:241）——除非你手动切到 `pattern` 或 `ml`（spaCy）那种非 LLM 方案。真要"全程零 LLM"，记得自己把这个默认值关掉。

## 它适合谁，不适合谁

**适合**：金融、医疗、法律、政府这些"决策得能交代"的行业；把 AI 决策当产品来做的平台团队；已经在用 Databricks/Snowflake、想把表直接变成带血缘知识图的数据团队；还有想用 Claude Code/Cursor/Codex 插件快速接入的工程师——项目官方给这几个编辑器都写了插件。

**不适合**：只想快速搞个"聊天机器人+向量检索"的轻量场景，那套东西用不上这张图的全部威力；还有就是期望"装上就能跑全流程"的团队——v0.6.0 里 Rete、worker、部分 server 端点还是骨架呢，生产之前必须逐模块好好核实。

**Github:**

> https://github.com/semantica-agi/semantica

## 最后说两句

Semantica 做对了一件事：**它把"AI 要负责任"这个口号，拆成了建图、记账、留痕、推理四个能落地的工程动作。** 哈希链账本和 Datalog 推理这两块，是实打实的硬货；Rete 和 worker 的占位也提醒我们——开源项目的 README 写得漂亮，不代表每个模块都长大了。选型之前，自己花十分钟翻翻源码，比什么都值。

## 关注

如果这篇文章帮你把"AI 可审计"这事儿理清了，欢迎关注我。后面我还会继续拆更多值得研究的开源项目，用大白话把技术背后的门道讲明白。有想看的项目，也欢迎留言告诉我。

历史精彩内容

[视频转字幕、字幕翻译、AI 配音与声音克隆](https://mp.weixin.qq.com/s?__biz=Mzg5MDA2ODY2OA==&mid=2247484805&idx=1&sn=6e518b4c71fb017dfba7aeb9990f5675&scene=21#wechat_redirect)

[视频转字幕、字幕翻译、AI 配音与声音克隆、字幕烧录——免费开源的一站式桌面工具来了](https://mp.weixin.qq.com/s?__biz=Mzg5MDA2ODY2OA==&mid=2247484798&idx=1&sn=50d5281594b6e8e5b8e890e4141cf1ed&scene=21#wechat_redirect)

[9.2k+ 一套能自我沉淀经验的开源代理架构，Prime Agent 值得一看](https://mp.weixin.qq.com/s?__biz=Mzg5MDA2ODY2OA==&mid=2247484786&idx=1&sn=ebf418bade29cfd0e51a48824a1a1161&scene=21#wechat_redirect)

[AI 浏览器三大坑怎么解：登录态带不过去、标签页被抢、爬虫被 ban……](https://mp.weixin.qq.com/s?__biz=Mzg5MDA2ODY2OA==&mid=2247484780&idx=1&sn=3f7233a4cbe4345d935b58331705d0f4&scene=21#wechat_redirect)

[TencentDB Agent Memory：给 AI Agent 一支会积累经验的团队](https://mp.weixin.qq.com/s?__biz=Mzg5MDA2ODY2OA==&mid=2247484770&idx=1&sn=44360a8532399679177a9790b14cc905&scene=21#wechat_redirect)
