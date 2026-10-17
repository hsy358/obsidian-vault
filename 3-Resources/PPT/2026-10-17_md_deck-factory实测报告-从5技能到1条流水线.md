---
tags: [PPT, deck-factory, 工作流]
date: 2026-10-17
related: "[[2026-10-17_md_PPT最佳可编辑生产方案-综合分析]]"
---

# deck-factory 实测报告：从 5 个技能到 1 条流水线

> 综合[[2026-10-17_md_PPT最佳可编辑生产方案-综合分析]]的结论已落地为单一 skill 并完成首轮实测。旧 5-skill 组合（knowledge-to-deck / consulting-deck-os / editable-architecture-ppt / ppt-production-engine / ppt-quality-review）**保留不动**，新 skill 成为默认入口。

## 1. 安装了什么

`C:\Users\hesiyan\.agents\skills\deck-factory\`（OpenCode / Codex / Cursor 同源生效）：

| 文件 | 内容 |
|---|---|
| SKILL.md | 4 步流水线 + 门禁 + 产物契约 + 反模式清单 |
| references/design-system.md | 字号阶梯 / 3 套配色 token / 每页一视觉锚 / 10 个页型 |
| references/qa-loop.md | PowerPoint COM 渲染命令 + 8 项视检清单 + P0/P1/P2 定义 |

## 2. 测了什么

用本次分析本身当主题，生成 9 页咨询风汇报 deck《PPT 工厂 v2：从 5 个技能到 1 条流水线》：

**产物只有 3 个**（旧流程是 10+ 份中间文档）：
- `slides.json` — 9 页结构化规格（受众双视角、风格 token、每页观点句标题）
- `deck-factory-v2-editable.pptx` — 最终可编辑交付
- `process.md` — 1 页 QA 记录

测试目录：`C:\Users\hesiyan\deck-factory-demo\`

## 3. 实测结果

**第 1 轮渲染自检抓到 7 个问题**（旧流水线从未做过这一步，同类问题会全部漏到交付）：
- P1×3：封面底部两行文字重叠；两处卡片内文字垂直失衡；文案 auto-wrap 致标点悬挂行首
- P2×4：标题多余空格、卡内正文偏移、底部间距过紧、半角冒号
- P3/P8/P9 首轮即通过

**第 2 轮**修复后复检：P0/P1 = 0，交付。

**可编辑性验证**（python-pptx 审计，红线达标）：

```
slides=9  shapes=165  editable_text_frames=123  native_tables=2  pictures=0
```

零整页贴图，全部原生文本框/形状/表格。

## 4. 新旧对比

| 维度 | 旧 5-skill | deck-factory |
|---|---|---|
| 流程 | 定调→资料→故事线→蓝图→编译→质检 6 环节 | 定调→内容→生成→自检 4 步 |
| 中间文档 | 8–10 份 md | 0 份（唯一结构在 slides.json） |
| 排版 | 手工坐标盲排，模板默认 6.5–9.5pt | design-system 硬约束（26–30pt 标题/12–13pt 正文） |
| 质检 | "if tools allow"——从未执行 | 强制 COM 渲染真图，≤2 轮收敛 |
| 产物 | 5+ 文件约定 | 3 个文件 |

## 5. 以后怎么用

对 AI 说"用 deck-factory 做一份 XX 的 PPT"即可。出稿简报（周会概览类）不开流水线；磨稿交付（汇报/咨询/路演）全流程；复杂单页架构图收窄为内容+生成两步；网页视觉作品类明示另走路。

实测样本已入库：[[2026-10-17_pptx_PPT工厂v2-实测9页-可编辑.pptx]]
