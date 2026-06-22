---
type: research
source: github
url: https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf
fetched: 2026-06-22
tags:
  - 知识管理
  - 知识图谱
  - markdown
  - YAML frontmatter
  - Google Cloud
  - LLM
  - RAG
  - Obsidian
related:
  - /root/vault/03-资源/
  - /root/vault/公众号文章/
---

# Google Cloud OKF — Open Knowledge Format

> **来源**：https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf
> **仓库**：GoogleCloudPlatform/knowledge-catalog（main 分支 /okf 目录）
> **状态**：新项目，2026 年开源

## 一句话定义

**OKF = 把"数据目录/知识库"用纯 Markdown + YAML frontmatter 文件表示的通用、厂商中立格式。**

不是 SDK、不是查询语言、不是中间件——就是**一组带 frontmatter 的 .md 文件 + 目录结构**。

## 核心设计原则

| 原则 | 说明 |
|---|---|
| **人类和 agent 都能读** | 工程师 `cat` 一下，LLM 直接 ingest |
| **Git 版本控制原生** | PR、diff、blame、review 都直接可用 |
| **不被厂商锁定** | 任何文件系统、任何 git 仓库、任何 tar 都能用 |
| **结构化 + 非结构化混用** | frontmatter 存可查询字段，body 存说明/schema/示例 |
| **最少化 opinion** | 几个必填字段保证互通，其他都可扩展 |
| **渐进披露** | 自动生成 `index.md`，逐级下钻，避免一次性加载全目录 |
| **图状而不仅树状** | 概念间用普通 markdown 链接互相引用 |

## 典型应用场景

1. **数据目录导出**：BigQuery、Dataplex、Unity Catalog、Collibra → OKF
2. **LLM 上下文加载**：直接把 .md 文件塞进 context window
3. **人类浏览**：Obsidian、Notion、MkDocs、Hugo、Jekyll 全都支持
4. **图可视化**：仓库自带 `viz.html` 渲染器
5. **agent 协作**：reference_agent 自动生成 + enrich

## 自带的参考实现（reference_agent）

**两阶段**：
- **BQ pass**：从 BigQuery 元数据自动生成 OKF（一个概念一篇 .md）
- **Web pass**：LLM 当爬虫，根据 `--web-seed` 列表抓权威文档 enrich

**可调参数**：
- `--web-max-pages` 抓取上限
- `--web-allowed-host` 同域白名单
- `--concept type/name` 单点迭代
- `--no-web` 跳过 web 抓取

## 三个示例 bundle

| Bundle | 数据源 | 演示能力 |
|---|---|---|
| `bundles/ga4/` | GA4 e-commerce | 单数据集导出 |
| `bundles/stackoverflow/` | Stack Exchange Data Dump | 多概念跨文档 enrich |
| `bundles/crypto_bitcoin/` | bitcoin-etl | 跨表外键关系 prose 化 |

每个 bundle 都带一个 `viz.html`，直接在浏览器看图谱。

## 安装与运行

```bash
python3.13 -m venv .venv
.venv/bin/pip install --index-url https://pypi.org/simple/ -e .[dev]

# 必备环境
gcloud auth application-default login
gcloud config set project <project>
export GEMINI_API_KEY=<key>  # 或用 Vertex AI 三个变量

# 最小调用
.venv/bin/python -m reference_agent enrich \
  --source bq \
  --dataset <project>.<dataset> \
  --web-seed-file <path/to/seeds.txt> \
  --out ./bundles/<name>
```

## 与何大人现有 vault 的关系

**关键观察**：何大人的 `/root/vault/` 实际上**已经在用 OKF 风格**——
- 文章用 markdown 存
- 部分有 YAML frontmatter（OKF 里 type / file_type / file_path 是必填）
- 用 git 版本控制
- 用 Obsidian 浏览

**差异/补强点**：
1. ❌ 缺 `index.md` 渐进披露（vault 目前是平铺 + 散落）
2. ❌ 缺"图状链接"（大部分文章孤立，缺 [[wikilink]]）
3. ❌ 缺必填 frontmatter 规范（部分有、部分没有）
4. ✅ 目录层级清晰，git 控制完善

## 关键启示

1. **行业方向**：Google 这种量级的厂也在做"知识 = markdown 文件"的事 = 方向正确
2. **本质是"文件即知识"**：拒绝用数据库/API 锁定，把知识装回文件系统
3. **LLM 当爬虫**：未来知识库的核心是 agent 自己读自己写，参考实现是范式
4. **可视化是亮点**：`viz.html` 这种零依赖的浏览器渲染 = 知识图谱的最低门槛

## 下一步可能行动

- [ ] 调研 Obsidian 是否有插件能自动生成 `index.md`（渐进披露）
- [ ] 把 vault 里没 frontmatter 的文档补 OKF 必填字段（type / source / tags）
- [ ] 试用 reference_agent 把某个 BigQuery 数据集导出成 OKF，看产出质量
- [ ] 评估能否把 vault 整体映射成 OKF 兼容的目录结构
- [ ] 看 viz.html 源码，看图可视化怎么实现的，能否自己改

## 引用

- **仓库**：https://github.com/GoogleCloudPlatform/knowledge-catalog
- **OKF 规范**：`/okf/SPEC.md`
- **参考 agent**：`/okf/reference_agent/`
- **示例 bundle**：`/okf/bundles/{ga4,stackoverflow,crypto_bitcoin}/`
- **图谱可视化**：`/okf/bundles/<name>/viz.html`（每个 bundle 一个）
