---
title: AI Agents 必读（PARA 版）
date: 2026-06-29
type: agents-config
purpose: 任何 AI Agent 第一次接触 vault 必读
related:
  - /root/vault/index.md
  - /root/vault/6-System/standards/
---

# 🤖 AI Agents 必读（OpenClaw / Hermes / Claude Code / Cursor）

> **这是何大人的第二大脑 + 项目库，按 Tiago Forte PARA 方法论组织。**
> 任何 AI Agent 第一次接触这个 vault，**先读这个文件**。

---

## 📂 顶层结构（PARA 7 大类）

| # | 目录 | 角色 | 文件数 | 典型内容 |
|---|---|---|---|---|
| 0 | `0-Inbox/` | **临时收集**（必须 < 20 文件 / < 100M）| 1 | 待归档 |
| 1 | `1-Projects/` | **当前活跃项目**（有截止日期）| 118 | 德勤、股票-A股、求职-DJI |
| 2 | `2-Areas/` | **持续关注领域**（无明确截止日期）| 110 | 公众号文章、元智-OS、AI-Agent-研究 |
| 3 | `3-Resources/` | **工具/素材/模板**（兴趣主题）| 15 | PPT、AI工具、配置教程 |
| 4 | `4-Archives/` | **历史归档**（已完成/暂停）| 0 | 暂空，备用 |
| 5 | `5-Journal/` | **日志/复盘**（个人记录）| 54 | 学习总结、公众号爆款日志 |
| 6 | `6-System/` | **系统文件**（vault 元数据）| 33 | standards、ai/、6-System/agents.md |

**vault 总索引**：`/root/vault/index.md`

---

## 🗂️ 各 PARA 类别详解

### 1️⃣ `1-Projects/` — 当前活跃项目
```
1-Projects/
├── 德勤/                         ← 德勤咨询项目（最重，89 文件）
│   ├── AI-Native/
│   │   ├── 公众号文章/
│   │   ├── 报告/
│   │   ├── 截图/
│   │   └── 笔记/                ← 26 份核心笔记（v0.3 + R&D + OKF）
│   └── NemoClaw-Physical-AI/
│       └── 报告/
├── 股票-A股/                     ← A 股每日跟踪（合并自 3 个原目录）
│   ├── 全景分析报告/
│   ├── 复盘日志/
│   ├── 持仓K线日报/
│   ├── 改进记录/
│   ├── 跟踪/
│   ├── 每日复盘/                ← 原 Research/daily-stock-review
│   └── 持仓截图/                ← 原 03-资源/股票/持仓截图
└── 求职-DJI/                     ← DJI 求职（6 月 22 日建）
    ├── DJI/
    ├── 参考资料/                ← 求职样章 PDF
    ├── index.md
    └── notes-index-备份.md
```

### 2️⃣ `2-Areas/` — 持续关注领域
```
2-Areas/
├── 公众号文章/                   ← 81 篇微信文章 + index.md 分类索引
├── 元智-OS/
│   └── yuanzhi-旧资料/          ← 原 notes/wechat/yuanzhi
└── AI-Agent-研究/                ← 原 Research + 部分图片
    ├── 2026-06-12 - Hermes Desktop - Deep Research.md
    ├── 2026-06-12 - Goose - Deep Research.md
    ├── 2026-06-12 - Routa - Deep Research.md
    ├── 2026-06-12 - Harnss - Deep Research.md
    ├── 2026-06-21 - 公众号文章入 AI 知识库 完整搭建指南.md
    ├── 2026-06-23 - muselab GitHub 仓库分析.md
    ├── images/
    └── index.md
```

### 3️⃣ `3-Resources/` — 工具/素材/模板
```
3-Resources/
├── PPT/                          ← 73M（最大，重资源）
│   ├── 毛概/
│   ├── 安盾安全监测系统/
│   └── 美的1106页摘要/
├── AI工具/                       ← 原 03-AI工具
└── 配置教程/                     ← 原 配置教程
```

### 5️⃣ `5-Journal/` — 日志/复盘
```
5-Journal/
├── 学习总结/                     ← 原 学习总结
└── 公众号爆款日志/
    └── 历史/                     ← 原 notes/wechat/爆款日志（5-10 → 6-28 共 50 天）
```

### 6️⃣ `6-System/` — 系统文件
```
6-System/
├── standards/                    ← 规范文档
│   ├── 2026-06-16 - 二进制文档处理规范.md
│   ├── 2026-06-29 - Obsidian Vault 现状评估与优化建议.md
│   └── index.md
├── ai/                           ← AI 文档（yuanzhi_os_analysis + yuanzhi_os_product）
└── agents.md                     ← 🆕 PARA 版 AI 助手必读（即本文件位置）
```

---

## 📐 命名规范（强制）

### 笔记（.md）
```
YYYY-MM-DD - <主题>.md
```
例：`2026-06-28 - AI Native 组织 Workspace 产品规划与开源落地方案 v0.3.md`

### 原始文件（.docx / .pdf / .pptx / .html 等二进制）
```
YYYY-MM-DD_<类型>_<标题>.<扩展名>
```
例：`2026-06-22_pptx_安盾安全监测系统产品胶片V0.1.pptx`

### Sidecar（同名 .md）
二进制文件必须配同名 .md sidecar：
- 必填字段：`type: document-metadata` / `file_type` / `file_path` / `source` / `uploaded_date` / `title` / `size_bytes` / `tags`
- 完整规范：`6-System/standards/2026-06-16 - 二进制文档处理规范.md`

---

## 🚦 处理 SOP（默认动作）

### 1. 收到任何文件
- 用户上传 → 立刻存档到 `0-Inbox/`（重命名按规范）
- 用户发 URL → 微信文章用 `wechat-article-to-obsidian` skill / 普通网页用 `doko` skill
- 用户发二进制 → 必须建 sidecar

### 2. 用户问项目相关问题
- **第一步**：`memory_search` 查 MEMORY.md
- **第二步**：查 vault `index.md` + PARA 类别索引
- **第三步**：用 `grep "tags:"` 或 `grep "title:"` 找文件
- **找不到** → 告诉用户"未找到"，不要瞎猜

### 3. 处理链接
- 微信文章 → `/root/vault/2-Areas/公众号文章/YYYY-MM-DD - 标题.md`（**PARA 后新位置**）
- 普通网页 → 看内容定（一般是 `2-Areas/AI-Agent-研究/`）

### 4. 写新笔记（PARA 判断）
| 内容性质 | PARA 类别 | 路径 |
|---|---|---|
| 当前活跃项目（如新接的咨询/工作）| Projects | `1-Projects/<项目>/` |
| 持续关注领域（无截止日期）| Areas | `2-Areas/<领域>/` |
| 工具/素材/模板 | Resources | `3-Resources/<类别>/` |
| 已完成的旧项目 | Archives | `4-Archives/<项目>/` |
| 日志/复盘/学习 | Journal | `5-Journal/<类别>/` |

### 5. Inbox 清理规则（硬规则）
- **Inbox 文件 > 20** → 触发告警
- **Inbox 总大小 > 100M** → 必须清理
- **处理顺序**：git mv 到对应 PARA 类别 / 删无用 / git rm 占位文件

---

## 🎯 关键项目位置（PARA 后速查）

| 项目 | PARA 类别 | 路径 |
|---|---|---|
| **德勤 v0.3 项目** | Projects | `1-Projects/德勤/AI-Native/笔记/` |
| **德勤 NemoClaw Physical AI** | Projects | `1-Projects/德勤/NemoClaw-Physical-AI/` |
| **德勤完整深度分析（hermes 风格）** | Projects | `1-Projects/德勤/AI-Native/笔记/2026-06-29 - 德勤项目完整深度分析报告（hermes 风格）.md` |
| **股票持仓 + 推荐** | Projects | `1-Projects/股票-A股/` |
| **公众号文章索引** | Areas | `2-Areas/公众号文章/index.md` |
| **元智 OS（yuanzhi）** | Areas | `2-Areas/元智-OS/` |
| **AI Agent 深度研究** | Areas | `2-Areas/AI-Agent-研究/` |
| **PPT 模板 + 资源** | Resources | `3-Resources/PPT/` |
| **AI 工具** | Resources | `3-Resources/AI工具/` |
| **学习总结** | Journal | `5-Journal/学习总结/` |
| **公众号爆款日志** | Journal | `5-Journal/公众号爆款日志/` |
| **vault 规范** | System | `6-System/standards/` |
| **AI 文档（OKF）** | System | `6-System/ai/` |

---

## 🔍 常用 grep 模式（PARA 后）

```bash
# 找某 PARA 类别的所有文件
find /root/vault/1-Projects -type f
find /root/vault/2-Areas -type f

# 找某标签（跨 PARA）
grep -rln "tags:.*德勤" /root/vault --include="*.md"

# 找含某关键词的笔记
grep -ril "OpenClaw" /root/vault --include="*.md"

# 列出所有 pptx
find /root/vault/3-Resources -name "*.pptx"
```

---

## 🤝 与 OpenClaw Skills 协作

常用 skill（`/root/.openclaw/workspace/skills/`）：

| Skill | 用途 |
|---|---|
| `wechat-article-to-obsidian` | 抓取 + 解析微信公众号文章 → **存到 `2-Areas/公众号文章/`** |
| `tavily-search` | 通用搜索（但别指望搜公众号） |
| `stock-research` | 股票持仓 + K 线 + 推荐 → **存到 `1-Projects/股票-A股/`** |
| `consulting-deck-os` / `ppt-skills` | PPT 生成 → **存到 `3-Resources/PPT/`** |
| `ai-native-requirement-analysis` | 需求分析 → **存到 `1-Projects/<项目>/笔记/`** |

---

## ⚠️ 红线（不要做）

1. **不要**跳过 PARA 直接放 vault 根目录（必须先归类）
2. **不要**把活跃项目放到 `2-Areas/`（必须是 `1-Projects/`）
3. **不要**把持续关注领域放到 `1-Projects/`（必须是 `2-Areas/`）
4. **不要**删 sidecar
5. **不要**把 Inbox 当最终存放点
6. **不要**在 `6-System/standards/` 之外建规范（统一规范入口）
7. **不要**改顶层 7 大类骨架（除非何大人明确同意再重构）

---

## 📞 遇到问题

- 找不到文件 → `grep -r "tags:" --include="*.md" | head`
- 不知道放 PARA 哪类 → 查 `vault/index.md` + 本文件 §"写新笔记" 表
- 不确定规范 → `cat 6-System/standards/`
- PARA 边界模糊 → 问何大人，不要自己拍板
- 报错 / 异常 → 立即告诉何大人，**不要假装成功**

---

**最后更新**：2026-06-29（PARA 顶层重构完成）
**维护者**：何大人 + OpenClaw (小助)
**架构师**：OpenClaw