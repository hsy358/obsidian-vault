# EY-24P · image-to-editable-ppt skill 示范项目

> **来源**：EY 安永《Seeing China's AI Reality》24 页高管 deck PDF（扫描版）
> **使用 skill**：`image-to-editable-ppt` v1.0
> **复刻时间**：2026-09-01
> **最终评分**：7/7 核心质检通过

## 这是什么

本项目是 `image-to-editable-ppt` skill 的**实战示范**：
- 输入：EY 安永 24 页高管 deck 扫描 PDF（4.2 MB，无文字层）
- 输出：24 页可编辑 PPTX（916 KB，13.33 × 7.5 in）
- 关键约束：100% 可二次编辑、所有数据/金句零丢失、EY 风格一致

## 7 件套产出

| 文件 | 大小 | 说明 |
|---|---|---|
| `deckspec.md` | 2.4 KB | 8 字段需求规格 |
| `slides.json` | 39 KB | 24 页结构化定义 |
| `theme-tokens.json` | 5.7 KB | EY 配色 + 字体配置 |
| `EY-24P-editable.pptx` | 916 KB | ⭐ 24 页可编辑 PPTX |
| `generate-deck.js` | 49 KB | pptxgenjs 生成脚本（可重跑）|
| `EY-24P-preview.html` | (待生成) | reveal.js 浏览器预览 |
| `quality-report.md` | 5.4 KB | 7 项质检报告 |
| `icons/` | 31 个 PNG | PIL 自绘 EY 蓝青图标 + 中国地图 |

## 怎么复现

```bash
cd /root/vault/1-Projects/image-to-editable-ppt-demo/EY-24P
NODE_PATH=/root/.nvm/versions/node/v22.22.2/lib/node_modules \
  node generate-deck.js
# ✓ Generated: EY-24P-editable.pptx
```

## 怎么用新输入

参考 `~/.openclaw/workspace/skills/image-to-editable-ppt/SKILL.md` 的 6 阶段工作流：
1. 解析（pymupdf + 多模态识图）
2. 规划（填 deckspec.md）
3. 主题（写 theme-tokens.json）
4. 规格（写 slides.json）
5. 编译（跑 generate-deck.js）
6. 质检（跑 quality-gates 7 项）

## 相关项目

- 上一版（v2）：`/root/vault/1-Projects/EY-China-AI-Reality/PPT/`（首次产出，9.3/10 数据卡片评分）
- 本版（v3 · 示范）：`/root/vault/1-Projects/image-to-editable-ppt-demo/EY-24P/`（用 skill 标准化产出）

## 视觉评分（vs EY 原版）

| 维度 | 评分 |
|---|---|
| 整体视觉 | 8/10 |
| 数据卡片（p04）| **9.3/10** |
| 封面（p01）| 7/10 |
| 时间轴（p05）| 8/10 |
| 可编辑性 | **10/10** |

完整评分见 `quality-report.md`。
