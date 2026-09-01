# Storyline · EY 24P 前 4 页 · image-to-editable-ppt 方案 D

> 按 `ppt-master` skill Stage ② 选题。

## 1. 决策问题（Decision Question）

**给定 EY 安永 24 页扫描 PDF，前 4 页如何做到视觉 1:1 + 完整可编辑？**

## 2. SCQA

### Situation（情境）
- EY 安永 2026 年发布 24 页高管 deck《Seeing China's AI Reality》
- 扫描版 PDF（4.2 MB，无文字层）
- 典型咨询级排版（深海军蓝 + teal 青色 + 衬线大标题）

### Complication（挑战）
- 程序化复刻（方案 A）极限：视觉 7-9/10（封面地图、装饰元素损失）
- 纯底图法（方案 B）问题：可编辑性有限
- OCR 自动提取（方案 C）问题：多列错位、错字

### Question（关键问题）
**前 4 页如何在 30-60 分钟内做到视觉 1:1 + 可编辑？**

### Answer（答案 · 方案 D 精准对齐）
1. **OCR 提取底图每页每个 word 的精确 bbox**（tesseract PSM 6）
2. **手工校对 OCR 错字**（"Al" → "AI"，"®" → "→" 等）
3. **用 OCR bbox 作为 native text 坐标**（精准对齐底图原文字）
4. **用 v2 校对文字内容作为 native text 内容**（数据 100% 准确）
5. **底图作为视觉基础**（装饰元素、地图、流程图保留原版）
6. **pptxgenjs 编译**（顺序：底图 → native text）

**结果**：视觉 1:1 + 完整可编辑（每页 4-22 个 native text shape）

---

## 3. 章节结构（前 4 页）

| 页 | Title | Section Message |
|---|---|---|
| p01 | Seeing China's AI Reality | 封面：中国 AI 现状 1 比 1 复刻入口 |
| p02 | Agenda | 议程：4 Part 议程结构 |
| p03 | What Changed in China? | Part I 章节过渡：环境扫描 |
| p04 | China's AI market is no longer the same market | 6 大数据：中国 AI 市场剧变的量化证据 |

---

## 4. 主线叙述

1. **封面（p01）**：用 EY 中国地图 + 上海天际线 + 5 步流程图（Productivity → Agent → Workflow → Process Redesign → Business Reinvention）建立视觉锚点
2. **Agenda（p02）**：4 个 Part 议程，让高管了解论述路径（环境 → 组织 → 业务 → 行动）
3. **章节过渡（p03）**：进入 Part I，预告 4 个分析维度（规模、速度、结构、产业纵深）
4. **数据基线（p04）**：6 大核心数据量化"中国 AI 已不同"——515M 用户、36.5% 渗透、302→868 服务、1.2T+ 产业、30%+ 制造商、10B+ 下载

---

## 5. 每页 Section Message

| 页 | Title | Section Message |
|---|---|---|
| 01 | Seeing China's AI Reality | 中国 AI 现状入口：从生产力到业务重塑的差异化路径 |
| 02 | Agenda | 4 个 Part 议程（环境/组织/业务/行动）|
| 03 | What Changed in China? | 中国 AI 环境发生了什么变化？|
| 04 | China's AI market is no longer the same market | 6 大数据：中国 AI 市场已不同 |

---

## 6. 14 大金句（前 4 页）

1. "Seeing China's AI Reality"（p01 主标题）
2. "A different path from productivity to business reinvention"（p01 副标题）
3. "What has changed in China since 2024?"（p01 小字）
4. "Agenda"（p02 标题）
5. "How the discussion will move from China's AI environment to enterprise action."（p02 副标题）
7. "PART 1"（p03 部分标签）
8. "What Changed in China?"（p03 主标题）
9. "Understanding how China's AI environment has changed since 2024."（p03 副标题）
10. "This section looks at the scale, speed, structure, and industrial depth of China's AI environment."（p03 callout）
11. "China's AI market is no longer the same market"（p04 标题）
12. "What changed in just two years?"（p04 副标题）
13. "AI is becoming part of China's operating environment."（p04 callout）
14. "China also accounted for 54% of the world's new industrial robot installations in 2024."（p04 callout）

---

## 7. 关键数据点（前 4 页）

| 数据 | 所在页 |
|---|---|
| 515M / 36.5% / 302 → 868 / RMB 1.2T+ / 30%+ / 10B+ | p04 |
| 5 大行业 | p02 |
| 4 维度（规模/速度/结构/产业纵深）| p03 |
| 5 步流程 | p01 |
| 54% 全球工业机器人 | p04 |

---

## 8. 复刻策略

| 层 | 来源 | 用途 |
|---|---|---|
| 底层 | 原 PDF 渲染 JPEG（13.33×7.5 in）| 视觉基础（地图、天际线、流程图、装饰） |
| 中层 | OCR 提取 word bbox → pptxgenjs native text 覆盖 | **可编辑**（标题/副标题/数字/金句/label/callout） |
| 内容 | v2 校对文字（已校）| 文字内容 100% 准确 |

**关键约束**：
- ✅ 文字层全 native（可改）
- ✅ 视觉 1:1（OCR 坐标精准对齐）
- ✅ 数据完整（v2 校对）
- ✅ 风格统一（EY 配色锁定）

---

## 9. 风险与对策

| 风险 | 对策 |
|---|---|
| OCR 错字（"Al" 应是 "AI"）| 手工校正 slides.json |
| OCR 多列错位（3 列数字被合并）| 按 word 级 bbox 单独提取每个数字 |
| 中文 label（OCR 不识别）| 用 v2 中文校对版 |
| 装饰元素（5 步流程图标、地图）| 不覆盖，让底图保留 |
| LibreOffice 字体 fallback | 标注字体优先级（serif → Calibri fallback）|