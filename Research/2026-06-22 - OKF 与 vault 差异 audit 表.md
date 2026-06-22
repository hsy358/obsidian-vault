---
type: research-report
title: OKF 与 vault 差异 audit 表
description: 对比 Google OKF v0.1 规范与何大人 /root/vault 实际数据，给出兼容性评估、差距清单、改进优先级。
source: self-analysis
tags:
- OKF
- Obsidian
- Vault
- agent
- audit
- llm
- obsidian
- okf
- vault
- 知识管理
timestamp: 2026-06-22 11:20:00+08:00
related:
- 2026-06-22 - Google Cloud OKF Open Knowledge Format.md
- 2026-06-16 - 知识工程三角：OKF 格式层 + KDD 流程层 + 成熟度评估层.md
---
# OKF 与 vault 差异 audit 表

**审计时间**：2026-06-22 11:20
**审计对象**：`/root/vault`（Obsidian vault）
**对照规范**：Google OKF v0.1（Open Knowledge Format）
**vault 规模**：205 个 .md 文档，7 个顶层目录

---

## 1. 关键结论（一句话）

**vault 已 91% 兼容 OKF，缺 3 个高价值字段 + 1 个目录级基础设施——零成本就能补完。**

---

## 2. vault 现状快照

| 指标 | 数值 |
|---|---|
| 文档总数 | 205 |
| 有 frontmatter 的 | 187（91%）|
| 顶层目录 | 03-资源 / docs / Inbox / notes / Research / 公众号文章 / 学习总结 |
| 主要文档类型 | notes (103) / docs (28) / Research (23) / Inbox (23) / 公众号文章 (22) |
| OKF 风格 metadata | `okf_metadata` 158 次（说明已尝试对齐）|
| git 版本控制 | ✅ 已经在用 |
| GitHub 同步 | ✅ 仓库 `hsy358/obsidian-vault` |

---

## 3. 字段级对比（OKF 必填/推荐 vs vault 实际）

| OKF 字段 | 必填/推荐 | vault 现状 | 差距 | 优先级 |
|---|---|---|---|---|
| `type` | **REQUIRED** | 187/205 文档有，枚举：`wechat-article`(104), `requirement-doc`(20), `research-report`(12), `document-metadata`, `research`... | ✅ 几乎全覆盖；枚举值是 OKF 推荐的"描述性"风格 | — |
| `title` | 推荐（priority 1）| **❌ 缺失** | vault 全部依赖文件名当标题 | **P0** |
| `description` | 推荐（priority 2）| **❌ 缺失** | vault 没有"一句话摘要"，影响搜索/索引体验 | **P0** |
| `resource` | 推荐（priority 3）| ⚠️ 部分用 `source: "wechat"` 替代 | 命名差异；OKF 强调 URI 形式 | P2 |
| `tags` | 推荐（priority 4）| ✅ 频繁使用 | 仅个别文章缺 | P1 |
| `timestamp` | 推荐（priority 5）| ⚠️ 用 `saved_date` / `publish_date` | OKF 要求 ISO 8601，vault 是 `YYYY-MM-DD` | P1 |
| 扩展字段 | 允许任意 | `okf_metadata`, `status`, `saved_date` 等自定义 | ✅ 符合"扩展"原则 | — |

---

## 4. 结构级对比

| OKF 元素 | vault 现状 | 差距 | 优先级 |
|---|---|---|---|
| **Bundle 概念** | 整个 `/root/vault` = 1 个 bundle | ✅ 概念等价 | — |
| **目录结构** | 7 个顶层分类 + 多级子目录 | ✅ 完全契合 | — |
| **`index.md` 渐进披露** | **❌ 完全没有** | 每个目录都没有渐进入口，agent 必须遍历全文件 | **P0** |
| **`log.md` 更新历史** | **❌ 完全没有** | vault 靠 git log 代替，但 OKF 强调"知识级"变更 | P2 |
| **`# Citations` 章节** | ⚠️ 部分有 | vault 里公众号文章常常有"引用"段，但没用约定 heading | P2 |
| **保留文件名 `index.md` / `log.md`** | 未保留 | 不冲突，可以直接用 | — |

---

## 5. 链接语法对比（最大差异点）

| 链接类型 | OKF 规范 | vault 实际 | agent 解析 |
|---|---|---|---|
| 跨概念引用 | `[text](/path/to/concept.md)` 推荐 | 多数用 `[[wikilink]]`（Obsidian 私有）| ✅ 任何工具 |
| 相对路径 | `[text](./other.md)` 备选 | 部分使用 | ✅ |
| 普通 markdown 链接 | ✅ 规范语法 | 部分使用 | ✅ |
| 外部 URL | `[text](https://...)` | ✅ vault 标准做法 | ✅ |

**结论**：vault **混用**了 `[[wikilink]]` + 普通 markdown 链接。`[[wikilink]]` 对 Obsidian 友好但对 agent 不友好（需要预处理）。

---

## 6. 改进优先级（按 ROI 排）

### P0 — 零成本 / 高收益（建议立即做）

| # | 行动 | 工作量 | 收益 |
|---|---|---|---|
| 1 | 给所有 vault 文档加 `title` 字段 | 1 个脚本批量 | 搜索/索引/可读性大幅提升 |
| 2 | 给所有 vault 文档加 `description` 字段 | 1 个脚本 + LLM 生成（一句话摘要） | 支持 `index.md` 渐进披露 |
| 3 | 写 `gen_index.py` 给每个目录生成 `index.md` | 1 个脚本 | agent 渐进加载，避免一次性塞满 context |

### P1 — 小成本 / 高收益（1-2 周内）

| # | 行动 | 工作量 | 收益 |
|---|---|---|---|
| 4 | 统一时间字段为 `timestamp`（ISO 8601）| 1 个映射脚本 | 跟 OKF 完全对齐 |
| 5 | 把 `source: "wechat"` 映射为 `resource: <url>` | 1 个转换脚本 | 资源可追溯 |
| 6 | tags 覆盖率补全（187 → 200+）| 1 个统计 + 补全 | 跨主题检索能力 |

### P2 — 锦上添花（1 个月内）

| # | 行动 | 工作量 | 收益 |
|---|---|---|---|
| 7 | 写 `okf_lint.py`：自动检查每篇文档是否合规 | 1 个 CI 脚本 | 防止后续新增文档走样 |
| 8 | 给 `[[wikilink]]` 自动加 mirror 普通链接 | 1 个预处理脚本 | 双重兼容：Obsidian 渲染 + agent 解析 |
| 9 | 引入 `log.md` 记录 vault 关键变更 | 习惯调整 | 知识级审计 |

### P3 — 探索性（季度级）

| # | 行动 | 工作量 | 收益 |
|---|---|---|---|
| 10 | 抄 OKF `viz.html` 思路，做 vault 图谱可视化 | 中等 | 知识图谱自主可控 |
| 11 | 跑 reference_agent 把 BigQuery 公开数据集导出成 OKF | 中等 | 验证 OKF 在企业数据场景的产出质量 |
| 12 | 评估能否把 vault 整体映射成 OKF bundle，提交到 OKF 生态 | 大 | 反向输出，向 Google 提 PR |

---

## 7. 风险与开放问题

| 风险 | 说明 | 缓解 |
|---|---|---|
| 推倒重来 | vault 已 187 篇有 frontmatter，全量重做代价大 | 用脚本批量补字段，不动原内容 |
| `[[wikilink]]` 失去 Obsidian 双链图谱 | 普通链接不会在 Graph View 出现 | mirror 双语法（保留 wikilink + 加普通链接）|
| 渐进披露过度激进 | 太多 `index.md` 反而冗余 | 只在顶层目录（7 个）生成，子目录看需要 |
| LLM 生成 description 的质量 | 摘要可能误导 | 让 LLM 生成后人工 review，或加"AI-generated"标记 |
| vault 跨多设备同步 | OKF 推 git-friendly，但 Obsidian 用 iCloud/Dropbox 可能冲突 | 现有方案已 OK（git + GitHub） |

---

## 8. 行动清单（给"做"的指令）

按 MEMORY.md 规则——任何"何大人说做"的动作都立刻执行。下方是 12 个可执行项，**告诉我从哪个开始**。

```text
□ P0-1: title 字段批量补全（脚本 1 个）
□ P0-2: description 字段批量补全（LLM 生成，1 个晚上）
□ P0-3: gen_index.py（7 个顶层目录）
□ P1-4: timestamp 字段统一
□ P1-5: source → resource 映射
□ P1-6: tags 覆盖率补全
□ P2-7: okf_lint.py
□ P2-8: wikilink → 普通链接 mirror
□ P2-9: log.md 习惯建立
□ P3-10: viz.html 自建
□ P3-11: reference_agent 试跑
□ P3-12: OKF 生态 PR
```

---

## 9. 引用

- **OKF SPEC**：https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
- **OKF 官方 README**：https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf
- **vault 6-16 已做研究**：`/root/vault/Research/2026-06-16 - 知识工程三角：OKF 格式层 + KDD 流程层 + 成熟度评估层.md`
- **vault 6-22 解读笔记**：`/root/vault/Research/2026-06-22 - Google Cloud OKF Open Knowledge Format.md`
- **vault 本地**：`/root/vault`
- **GitHub 同步仓库**：https://github.com/hsy358/obsidian-vault
