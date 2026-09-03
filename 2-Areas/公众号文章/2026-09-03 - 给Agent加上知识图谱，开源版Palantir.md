---
title: "给Agent加上知识图谱，开源版Palantir"
author: "GitHubStore"
publish_date: "2026-09-03 08:03:51"
saved_date: "2026-09-03"
source: "wechat"
url: "https://mp.weixin.qq.com/s/bHRmjivvmNSWAN5bu3ZnEQ"
---
# 给Agent加上知识图谱，开源版Palantir
## 项目简介

多数 AI Agent 跑在嵌入向量上，而不是意义上：只有相似度分数，没有结构、没有关系，也无法解释结果从何而来。Semantica 是 LLM、向量库与 Agent 框架之下的语义/上下文层：一套确定性基础设施（构图、推理、溯源均不必依赖 LLM），把碎片化企业数据变成结构化、可查询的上下文图与知识图谱，并由本体与受控词表（OWL、SHACL、SKOS）治理，让数据的含义被显式表达，而不只是嵌入。决策溯源与审计轨迹是这种结构带来的属性，而不是单独卖点；在监管可能追问的领域，同一套结构恰好能直接回答「为什么」。

**面向谁：**

- **AI/ML 平台团队**：上线会做重大决策的 Agent，需要从碎片化原始数据构建结构化、可查询的上下文，而不只是向量索引
- **Databricks / Snowflake 上的数据平台团队**：要把已在 Unity Catalog 或 Snowflake 数仓里的表变成受治理、带血缘的知识图谱，而不必先导出到第三方 SaaS
- **合规、风险与审计团队**：需要能被监管方接受的「AI 为什么这么做」的直白答案
- **受监管企业**（金融、医疗、法律、政府、国防）：不能交付黑盒，也不能把数据送到别人的 SaaS 才能得到答案
- **平台与基础设施工程师**：希望知识图谱、推理与溯源栈可自托管、可替换，不被锁死在单一厂商后端
- **数据与知识工程师**：从多源脏数据构建 KG：抽取实体与关系，冲突或矛盾事实会被标记而非静默覆盖，重复项在变成噪声前合并
![](https://mmbiz.qpic.cn/sz_mmbiz_gif/ZstIPjm4pIcbzFEFjs3ghxFQS24ZuoHh9NiaMYkGvFdCibicYnWWseAorKhpJ1gCLyIicN4l1s8ht4dMM5Gs4XKrnHdb3H90LEMIvF2CkicialkR8/640?wx_fmt=gif&from=appmsg)

## Semantica 能给你什么

- **上下文图：** 对 Agent 所知、所决、所推理的一切，形成结构化、可查询的图
- **决策智能：** 每个决策都是一等对象：可追溯、可按先例检索、有因果关联
- **AI 治理与本体：** SHACL 约束、冲突检测、合规规则、OWL 生成、SKOS 词表管理，以及可视化编辑器
- **完整可审计性：** 每条事实带 W3C PROV-O 溯源，审计轨迹可导出为 JSON、CSV 或 RDF
- **确定性推理：** 前向链、Rete 网络、Datalog 与 SPARQL，路径完全可解释，而非黑盒
- **知识流水线：** 多源接入、实体感知分块、NER/关系/事件抽取、知识图谱构建，全程语义去重与保留溯源的合并
- **企业数据平台：** Databricks（Unity Catalog + Delta Lake，PAT/OAuth M2M，目录/模式/表/血缘探查）与 Snowflake（仓库/库/模式，密钥对与 OAuth）原生连接器，湖仓或数仓中的表直接成为带溯源的图节点，而不是再做一轮导出导入
- **图分析：** 中心性、社区发现、链路预测、最短路径，跑在你刚构建的图上
- **多语言图存储：** 原生 RDF（嵌入式 Oxigraph、Blazegraph、Apache Jena、Eclipse RDF4J，经 SPARQL）与属性图 LPG（Neo4j、FalkorDB、Apache AGE、AWS Neptune，经 Cypher），外加向量库，切换存储不必改业务代码
- **可视化：** 在交互式浏览器工作台中探索任意图、本体或时间线
- **即插即用集成：** 原生 Agno、CrewAI、LangChain，功能完整的 MCP 服务器，全面 CLI、REST API，以及主流编辑器插件

---

## 为何选择 Semantica

向量库 + RAG

普通 LLM 记忆

**Semantica****召回方式**嵌入相似度

Token 窗口

图遍历 + 语义检索

**决策历史**不存储

不存储

一等、可查询对象

**溯源**无

无

W3C PROV-O，关联来源

**推理**无

黑盒

前向链、Rete、Datalog、SPARQL

**冲突检测**静默覆盖

静默覆盖

检测、标记、解决

**时间旅行**无

无

任意时点的图快照

**合规导出**无

无

PROV-O、SHACL、OWL、RDF

**策略执行**无

无

内置规则引擎 + SHACL

**实体解析**无

无

Blocking + 语义去重

**多智能体上下文**各 Agent 隔离

各 Agent 隔离

单一共享智能层

Semantica 补全现有栈，而不是替换它。LLM、向量库、Agent 框架可以原样保留；Semantica 在其上增加决策记录、因果推理、溯源、本体治理、冲突检测与审计轨迹。推理引擎、KG 构建与溯源层完全确定性，使用它们不必调用 LLM。

---

## 快速开始

```
pip install semantica
```

```
from semantica.context import ContextGraphgraph = ContextGraph(advanced_analytics=True)# Every agent decision becomes a queryable, auditable knowledge nodedecision_id = graph.record_decision(    category="vendor_selection",    scenario="Choose cloud provider for HIPAA workload",    reasoning="AWS offers BAA, mature HIPAA tooling, and existing team expertise",    outcome="selected_aws",    confidence=0.93,)# Ask "why did this happen?" and get a real, structured answerchain     = graph.trace_decision_chain(decision_id)       # full causal ancestrysimilar   = graph.find_similar_decisions("cloud vendor", max_results=5)  # precedentsimpact    = graph.analyze_decision_impact(decision_id)    # downstream influence mapcompliant = graph.check_decision_rules({"category": "vendor_selection"})  # policy gate
```

**5 秒验证安装：**

```
semantica doctor# Python 3.11.9         pass# semantica 0.6.7       pass# faiss vector store    pass# Config file           pass    ~/.semantica/config.yaml
```

在脚本或 CI 中运行时，进度条仅在 stdout 为交互终端（或 Jupyter）时写出，管道与重定向默认干净。可用 `SEMANTICA_DISABLE_PROGRESS=1` 全局关闭，或 `SEMANTICA_FORCE_PROGRESS=1` 在重定向时仍显示。`SEMANTICA_DISABLE_PROGRESS` 优先。

## 架构

Semantica 是端到端流水线，不是套了营销名的单一库。下列每一阶段都是已发布、可独立导入的模块：

```
来源 → 接入 → 解析 → 规范化 → 分块 → 抽取 → 冲突检测 → 去重   → 知识图谱 → [ 本体 · 推理 · 溯源 · 决策 ] → 富化 KG   → 向量库 + 多语言图存储（RDF 与 LPG） → 导出 / 可视化 / REST · MCP · CLI
```

- **接入：** 文件、网页、数据库、企业数据平台（Databricks、Snowflake）、云（Google Drive、Elasticsearch）、流（Kafka、Kinesis）、Git、邮件、MCP
- **解析 → 规范化 → 分块：** 文档解析，文本/实体/日期规范化，面向 GraphRAG 的实体感知分块
- **抽取 → 冲突检测 → 去重：** NER、关系、事件、三元组；冲突事实在合并前被标记并解决
- **知识图谱：**`GraphBuilder` 构图；双时态事实与完整图分析（中心性、社区、链路预测）跑在其上
- **本体 · 推理 · 溯源 · 决策：** 坐在 KG 上的智能层：SHACL/OWL 治理、Rete/Datalog/SPARQL 推理、W3C PROV-O 血缘、一等决策记录
- **存储：** 天生多语言：RDF 三元组库（嵌入式 Oxigraph、Blazegraph、Apache Jena、Eclipse RDF4J）、属性图（Neo4j、FalkorDB、Apache AGE、AWS Neptune）与向量库，切换不必改代码
- **输出：** 导出（RDF、OWL、Parquet、Cypher、JSON-LD）、交互可视化，以及 REST API、MCP 服务器或 CLI

## 决策智能

决策智能把每一次 AI 选择从短暂推理变成永久、可审计、可查询的记录。它回答的是：「你的 AI 决定了什么、为什么、随后发生了什么？」——监管与企业风险团队越来越急迫地问这个问题。

在 Semantica 中，决策不是一行日志，而是带完整生命周期的一等图节点。在受监管领域，每个 AI 决策必须能追溯到来源、能向审计师辩护：`record_decision()` 创建永久结构化记录，可导出为多数合规框架接受的 W3C PROV-O。

```
record_decision()             → 存为带完整结构化上下文的图节点add_causal_relationship()     → 关联上游原因与下游效应find_similar_decisions()      → 在全部历史决策上做语义先例检索trace_decision_chain()        → 追溯到根因的完整因果链analyze_decision_impact()     → 下游影响图——该决策影响的一切check_decision_rules()        → 对照可配置规则集的策略合规门控export / audit trail          → W3C PROV-O、CSV 或 JSON，供监管提交
```

```
from semantica.context import ContextGraphgraph = ContextGraph(advanced_analytics=True)app_id = graph.record_decision(    category="credit_application",    scenario="Personal loan, $85k income, 31% DTI, 3yr employment",    reasoning="Income meets threshold; employment stable; no adverse credit events",    outcome="proceed_to_underwriting",    confidence=0.88,    metadata={"applicant_id": "A-7291"},)uw_id = graph.record_decision(    category="loan_underwriting",    scenario="Underwriting review for A-7291",    reasoning="DTI within policy; clean 36-month credit history",    outcome="approved",    confidence=0.94,)rate_id = graph.record_decision(    category="interest_rate",    scenario="Rate assignment for approved loan A-7291",    outcome="rate_set_8.9pct",    reasoning="Prime + 2.4% based on risk tier B2",    confidence=0.99,)# relationship_type 必须是 CAUSED、INFLUENCED 或 PRECEDENT_FOR 之一graph.add_causal_relationship(app_id, uw_id,   relationship_type="CAUSED")graph.add_causal_relationship(uw_id,  rate_id, relationship_type="INFLUENCED")chain     = graph.trace_decision_chain(rate_id)similar   = graph.find_similar_decisions("personal loan approval, 31% DTI", max_results=5)impact    = graph.analyze_decision_impact(uw_id)compliant = graph.check_decision_rules({"category": "loan_underwriting", "confidence": 0.94})insights  = graph.get_decision_insights()
```

---

---

---

## CLI

能力均可在终端使用，随包装入，无需另装。

```
pip install semanticasemantica        # 启动仪表盘semantica doctor # 健康检查semantica --help# 完整分组命令
```

**命令组：**`ingest` · `parse` · `extract` · `kg` · `reason` · `decision` · `temporal` · `provenance` · `ontology` · `embed` · `deduplicate` · `validate` · `export` · `visualize` · `pipeline` · `server` · `explorer` · `mcp` · `doctor` · `shell` · `init` · `watch`

最快上手（无需 Node.js）：

```
pip install "semantica[explorer]"semantica-explorer --graph my_graph.json# 仪表盘打开于 http://127.0.0.1:8000
```

---

## 集成

为 Claude Code、Cursor、Codex、Windsurf、Cline、Continue、VS Code、OpenClaw 提供原生插件包；面向任意 MCP 客户端的完整 MCP 服务器；全面 REST API；以及对 Agno、CrewAI、LangChain 的一等支持。主流 LLM 已通过 `semantica.llms` 与 LiteLLM 支持。

**Agent 框架：**

- 原生：`pip install semantica[agno]` / `[crewai]` / `[langchain]`
- 经 REST API 与 MCP 已可用：LangGraph、LlamaIndex、AutoGen、OpenAI Agents、Google ADK
- 专用 SDK 工具包：规划中

---

## 项目地址

```
https://github.com/semantica-agi/semantica
```

### 参考资料

[1] CHANGELOG.md: *https://github.com/semantica-agi/semantica/blob/main/CHANGELOG.md*
