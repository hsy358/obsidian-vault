---
title: 二进制文档处理规范（sidecar + 命名 + Inbox 分类）
type: standard
status: active
version: 1.0
effective_date: 2026-06-16
author: 小助（MiniMax M3）
scope: vault-wide + OpenClaw 工作区
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
  rationale: '何大人预告未来会上传文档让我查找/解析/操作。当前 vault 仅覆盖 Markdown，

    二进制文件（PDF/Word/Excel/图片）没有规范。本规范填补这个空缺。

    '
tags:
- OKF
- PPT
- Vault
- binary-document
- docs
- inbox-classification
- naming-convention
- sidecar
- standard
description: 按优先级（高 → 低）：
---
# 二进制文档处理规范（sidecar + 命名 + Inbox 分类）

## 1. 为什么需要本规范

**现状盘点：**
- vault 146 个 .md 文件，OKF 化已完成（L2 → L3）
- 二进制文件（PDF/Word/Excel/图片/PPT）**没有统一处理规范**
- 上传后只能丢 Inbox，**无法被 grep / recall / dataview 工具索引**

**未来场景：** 何大人会让我：
- 查找特定上传文档 → 需要按 type/date/source 过滤
- 解析 PDF/Excel 内容 → 需要元数据引导
- 跨 session 找回某次上传 → 需要稳定文件名 + 位置

**本规范目标：** 让二进制文件**通过 sidecar 元数据**实现 Markdown 同等的可索引性。

---

## 2. 文件命名约定

### 2.1 强制格式

```text
YYYY-MM-DD_类型_标题.扩展名
```

### 2.2 字段说明

| 字段 | 规则 | 示例 |
|---|---|---|
| **YYYY-MM-DD** | 上传日期（不是文档原始日期）| `2026-06-16` |
| **类型** | 见下表（小写英文）| `pdf` / `docx` / `xlsx` |
| **标题** | 中文 / 英文，可含空格但避免特殊字符 `/\:*?"<>\|` | `AI工程师招聘JD` |
| **扩展名** | 与类型匹配 | `.pdf` / `.docx` |

### 2.3 合法类型枚举

| 类型代码 | 含义 | 实际扩展名 |
|---|---|---|
| `pdf` | PDF 文档 | .pdf |
| `doc` | Word 文档 | .doc / .docx |
| `xls` | Excel 表格 | .xls / .xlsx |
| `ppt` | PowerPoint | .ppt / .pptx |
| `img` | 图片 | .png / .jpg / .gif / .webp |
| `zip` | 压缩包 | .zip / .tar.gz |
| `audio` | 音频 | .mp3 / .wav |
| `video` | 视频 | .mp4 / .mov |
| `txt` | 纯文本 | .txt |
| `code` | 源代码 | .py / .js / .ts / .sh |

### 2.4 反例（**禁止**使用的命名）

| 错误 | 原因 |
|---|---|
| `新建文档.pdf` | 无日期、无类型 |
| `Screenshot 2026-06-16.png` | 日期在中间、难以排序 |
| `简历-2026.docx` | 年份无月份、无法精确排序 |
| `final-final-v2.pdf` | 无法识别主版本 |
| `文档.pdf` | 无任何识别信息 |

---

## 3. Sidecar 元数据文件规范

### 3.1 什么是 sidecar

**Sidecar（边车文件）** = 与二进制文件同名、扩展名为 `.md` 的元数据文件，**始终与原文件同目录**。

```text
/root/vault/Inbox/
├── 2026-06-16_pdf_AI工程师招聘JD.pdf        ← 原文件
└── 2026-06-16_pdf_AI工程师招聘JD.md         ← sidecar
```

### 3.2 Sidecar 必须包含的字段（OKF frontmatter）

```yaml
---
type: document-metadata          # 强制 type 字段（OKF）
file_type: pdf                   # 二进制类型（与命名约定一致）
file_path: 2026-06-16_pdf_AI工程师招聘JD.pdf
source: user-upload              # 来源：user-upload / web-fetch / api-download
uploaded_date: 2026-06-16
original_date: 2026-06-15        # 文档原始日期（可为空）
title: "某公司 AI 工程师招聘 JD"
description: "岗位职责 / 任职要求 / 加分项 / 公司福利"
size_bytes: 245678
page_count: 3                    # 仅 PDF/DOC 适用
tags: [recruitment, ai-engineer, jd]
language: zh-CN
related_entities:
  - company: "某公司"
  - position: "AI 工程师"
    level: "P5/P6"
key_facts:                       # 关键事实，结构化（按需填）
  - "要求 3 年以上 PyTorch 经验"
  - "团队规模 30+ 人"
  - "Base 30-60K·14 薪"
next_actions:                    # 何大人给小助的下一步指令（按需填）
  - "提取所有岗位关键技能 → 写入 03-资源/求职/"
  - "对比 DJI 面试准备资料"
okf_metadata:
  schema: okf-v0.1-inspired
  sidecar_for: 2026-06-16_pdf_AI工程师招聘JD.pdf
---

# 某公司 AI 工程师招聘 JD —— 内容摘要

> 本文件是 [2026-06-16_pdf_AI工程师招聘JD.pdf] 的 sidecar 元数据。
> 原文件为二进制 PDF，需要专用工具读取；本 sidecar 提供**人读 + 机读**元信息。

## 一、岗位职责
1. 负责大模型微调与部署
2. 负责 agent 框架设计
3. ...

## 二、任职要求
1. 计算机/AI 相关硕士及以上
2. 3 年以上 PyTorch / TensorRT 经验
3. ...

## 三、关键术语表
| 术语 | 含义 |
|---|---|
| LoRA | Low-Rank Adaptation |
| ... | ... |

## 四、原始文档摘要（人读）
> 此节由小助解析 PDF 后填充，便于人在不打开原文件的情况下理解内容。
>
> [300-500 字摘要]

## 五、引用与跳转
- 原文件：`./2026-06-16_pdf_AI工程师招聘JD.pdf`
- 相关内部资产：[[何四燕-DJI面试准备-题目与答案]]
- 相关研究：[[Research/2026-06-XX - 求职技能图谱]]
```

### 3.3 字段填写规则

| 字段 | 是否必填 | 填写时机 |
|---|---|---|
| `type` | **必填** | 立即 |
| `file_type` | **必填** | 立即 |
| `file_path` | **必填** | 立即 |
| `source` | **必填** | 立即 |
| `uploaded_date` | **必填** | 立即 |
| `original_date` | 选填 | 解析时发现填 |
| `title` | **必填** | 立即 |
| `description` | **必填** | 立即 |
| `size_bytes` | **必填** | 立即 |
| `page_count` | 选填 | 仅 PDF/DOC |
| `tags` | **必填**（≥1 个） | 立即 |
| `language` | 选填 | 默认 zh-CN |
| `related_entities` | 选填 | 解析后填 |
| `key_facts` | 选填 | 解析后填 |
| `next_actions` | 选填 | 何大人明确要求时填 |
| `okf_metadata` | **必填** | 立即 |

---

## 4. Inbox 自动分类规则

### 4.1 临时区 vs 归档区

```text
/root/vault/Inbox/             ← 临时区（≤ 7 天）
/root/vault/03-资源/...         ← 归档区（永久）
/root/vault/Research/...        ← 归档区（永久）
/root/vault/Inbox/_archive/     ← 已处理（按月归档，原文件保留 90 天后清理）
```

### 4.2 分类决策树

```
新文件进入 Inbox
    ↓
判断类型（按命名约定的 file_type 字段）
    ↓
┌──────────────┬──────────────┬──────────────┐
│ 课件 / 培训  │ 研究 / 报告  │  临时 / 工作  │
│ 03-资源/     │ Research/    │  Inbox/       │
│ {子目录}/    │ *.md         │  (保留)       │
└──────────────┴──────────────┴──────────────┘
```

### 4.3 自动归档触发

**时机：** 处理完成后，由小助根据 `next_actions` 字段自动移动。

**示例：**
```text
1. 用户上传 PDF → Inbox/2026-06-16_pdf_AI工程师招聘JD.pdf
2. 小助创建 sidecar → Inbox/2026-06-16_pdf_AI工程师招聘JD.md
3. 小助解析 PDF 填入摘要
4. 用户说"归档到 03-资源/求职/"
5. 小助移动两个文件 → 03-资源/求职/2026-06-16_pdf_AI工程师招聘JD.{pdf,md}
6. Git 自动 commit + push
```

---

## 5. 跨工具查询示例

### 5.1 查找所有上传的 PDF

```bash
grep -l "^file_type: pdf" /root/vault -r --include="*.md"
```

### 5.2 查找所有招聘 JD

```bash
grep -l "tags:.*recruitment" /root/vault -r --include="*.md"
```

### 5.3 查找某段时间内的所有上传

```bash
grep -l "^uploaded_date: 2026-06" /root/vault -r --include="*.md"
```

### 5.4 升级版 recall（未来实现）

```python
recall("AI 工程师招聘 JD", file_type="pdf", tags=["recruitment"])
# → 返回所有 file_type=pdf 且 tags 包含 recruitment 的 sidecar
```

---

## 6. 处理流程 SOP（小助侧）

### 6.1 用户上传文件后

```python
1. 检查文件类型 → 决定 file_type
2. 重命名（按 §2.1 强制格式）
3. 移动到 /root/vault/Inbox/
4. 创建 sidecar .md（按 §3.2 模板）
5. 立即 commit + push（占位入库）
6. 主动汇报给用户："已存档 + GitHub URL"
```

### 6.2 用户要求解析时

```python
1. 读取 sidecar 摘要（已有则不重复解析）
2. 如需原文 → 调对应解析工具（pdfplumber / python-docx / openpyxl）
3. 填回 sidecar 的"原始文档摘要"节
4. 更新 okf_metadata 的 parsed_at 字段
5. commit + push
```

### 6.3 用户要求归档时

```python
1. 读取 sidecar 的 next_actions
2. 移动 {pdf, md} 文件到目标目录
3. 更新 sidecar 的 file_path 字段
4. commit + push
```

---

## 7. 异常处理

| 异常 | 处理 |
|---|---|
| 用户上传时未指定类型 | 默认 `unknown`，让小助推断；推断失败标 `bin` |
| 用户上传文件无日期信息 | 用 `uploaded_date` 当兜底，original_date 留空 |
| 二进制文件损坏 | sidecar 加 `status: corrupted`，原文件移到 `_corrupted/` |
| Sidecar 丢失（只有原文件）| 小助检测时**自动重建**最小 sidecar |
| 同名文件重复上传 | 加时间戳后缀 `_2` / `_3`（不覆盖）|

---

## 8. 实施清单

按优先级（高 → 低）：

- [x] 写本规范文档（OKF frontmatter，type: standard）
- [ ] 更新 PATH_RULES 路径规则加 `docs/standards/.+\.md$` → `type: standard`
- [ ] 写一个**示例 sidecar**（找一个测试 PDF 走一遍全流程）
- [ ] 更新 recall.py 支持 file_type / tags 过滤
- [ ] 写 3 个 dataview 查询示例（PDF 总览 / 招聘 JD / 最近 7 天上传）
- [ ] 在 TOOLS.md 加"二进制文档处理快速参考"
- [ ] 在 MEMORY.md 顶部加"任何文件都要默认存档"细则

---

## 9. 与现有规范的关系

| 已有规范 | 关系 |
|---|---|
| MEMORY.md「任何文件都要默认存档」(2026-06-16)| 本规范是其在**二进制文件**场景的具体落地 |
| 知识工程三角（OKF/KDD/5级）| 本规范的 frontmatter 字段设计直接采用 OKF 思路 |
| 微信文章存档规范（公众号文章/）| 本规范是其兄弟——同结构、同 frontmatter 风格 |

---

## 10. 参考

- OKF 规范：`/root/vault/公众号文章/2026-06-16 - 谷歌突然开源Agent OKF新标准！...md`
- 知识工程三角：`/root/vault/Research/2026-06-16 - 知识工程三角：...md`
- Wikipedia "Sidecar file"：https://en.wikipedia.org/wiki/Sidecar_file
- Linux Foundation 文档：https://docs.linuxfoundation.org/

---

_本规范由 MiniMax M3（小助）根据何大人 2026-06-16 指令编写；v1.0 生效中_
