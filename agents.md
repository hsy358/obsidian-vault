# 🤖 AI Agents 必读（OpenClaw / Hermes / Claude Code / Cursor）

> **这是何大人的第二大脑 + 项目库。**
> 任何 AI Agent 第一次接触这个 vault，**先读这个文件**。

---

## 📂 顶层结构（9 大目录）

| # | 目录 | 角色 | 命名规范 |
|---|---|---|---|
| 1 | `03-资源/` | 工具/素材/PPT 模板 | 按子目录归类 |
| 2 | `docs/` | 规范/AI 文档 | `docs/standards/` + `docs/ai/` |
| 3 | `Inbox/` | 临时收集（**必须 < 20 文件**）| `YYYY-MM-DD_类型_标题.扩展名` |
| 4 | `notes/` | 个人笔记/求职 | 自由格式 |
| 5 | `Research/` | 深度调研 | `YYYY-MM-DD - 标题.md` |
| 6 | `公众号文章/` | 微信文章存档 | `YYYY-MM-DD - 标题.md`（**平铺，不建日期子目录**）|
| 7 | `学习总结/` | 学习笔记 | 自由格式 |
| 8 | `德勤/` | 德勤项目库（**最重，11M**）| 按主题（AI-Native / NemoClaw-Physical-AI）|
| 9 | `股票推荐复盘/` | 股票 | 5 个子目录（全景/日志/K线/改进/跟踪）|

**vault 总索引**：`/root/vault/index.md`

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
- 完整规范：`docs/standards/2026-06-16 - 二进制文档处理规范（sidecar + 命名 + Inbox 分类）.md`

---

## 🚦 处理 SOP（默认动作）

### 1. 收到任何文件
- 用户上传 → 立刻存档到 `Inbox/`（重命名按规范）
- 用户发 URL → 微信文章用 `wechat-article-to-obsidian` skill / 普通网页用 `doko` skill
- 用户发二进制 → 必须建 sidecar

### 2. 用户问项目相关问题
- **第一步**：`memory_search` 查 MEMORY.md
- **第二步**：查 vault `index.md` + 项目 README
- **第三步**：用 `grep "tags:"` 或 `grep "title:"` 找文件
- **找不到** → 告诉用户"未找到"，不要瞎猜

### 3. 处理链接
- 微信文章 → `/root/vault/公众号文章/YYYY-MM-DD - 标题.md`（平铺，**不建日期子目录**）
- 普通网页 → 看内容定（一般是 `Research/`）

### 4. 写新笔记
- 长期项目 → `1-Projects/<项目>/`（待重构时启用）
- 一次性研究 → `Research/`
- 个人心得 → `notes/` 或 `学习总结/`
- 微信文章 → `公众号文章/`

### 5. Inbox 清理规则
- **硬规则**：Inbox 文件 > 20 → 触发告警
- **硬规则**：Inbox 总大小 > 100M → 必须清理
- **处理顺序**：git mv 到对应目录 / 删无用 / git rm 占位文件

---

## 🎯 关键项目位置（速查）

| 项目 | 路径 |
|---|---|
| **德勤 v0.3 项目** | `德勤/AI-Native/笔记/` |
| **德勤 NemoClaw Physical AI** | `德勤/NemoClaw-Physical-AI/` |
| **德勤完整深度分析（hermes 风格）** | `德勤/AI-Native/笔记/2026-06-29 - 德勤项目完整深度分析报告（hermes 风格）.md` |
| **股票持仓 + 推荐** | `股票推荐复盘/` |
| **公众号文章索引** | `公众号文章/index.md` |
| **vault 规范** | `docs/standards/` |
| **OKF 知识工程** | `德勤/AI-Native/笔记/` (4 份 OKF) |

---

## 🔍 常用 grep 模式

```bash
# 找某标签
grep -l "tags:.*德勤" /root/vault -r --include="*.md"

# 找某作者公众号文章
grep -l "author:.*老王" /root/vault/公众号文章/*.md

# 找含某关键词的笔记
grep -ril "OpenClaw" /root/vault --include="*.md"

# 列出所有 pptx
find /root/vault -name "*.pptx" -not -path "*/.git/*"
```

---

## 🤝 与 OpenClaw Skills 协作

常用 skill（`/root/.openclaw/workspace/skills/`）：

| Skill | 用途 |
|---|---|
| `wechat-article-to-obsidian` | 抓取 + 解析微信公众号文章 |
| `wechat-monitor` | ⚠️ **已废弃**（Tavily 不索引公众号） |
| `tavily-search` | 通用搜索（但别指望搜公众号） |
| `stock-research` | 股票持仓 + K 线 + 推荐 |
| `consulting-deck-os` / `ppt-skills` | PPT 生成 |
| `wechat-article-to-obsidian` | 微信公众号抓取 |

---

## ⚠️ 红线（不要做）

1. **不要新建日期子文件夹**（公众号文章已统一平铺）
2. **不要删除 sidecar**
3. **不要擅自 commit 到 main 分支外的 branch**
4. **不要重命名 vault 顶层 9 个目录**（除非 B 重构方案通过）
5. **不要把 Inbox 当最终存放点**
6. **不要在 docs/standards/ 之外建规范**（统一规范入口）

---

## 📞 遇到问题

- 找不到文件 → `grep -r "tags:" --include="*.md" | head`
- 不知道放哪 → 查 `vault/index.md`
- 不确定规范 → `cat docs/standards/`
- 报错 / 异常 → 立即告诉何大人，**不要假装成功**

---

**最后更新**：2026-06-29（清空 Inbox 后 + 写 agents.md）