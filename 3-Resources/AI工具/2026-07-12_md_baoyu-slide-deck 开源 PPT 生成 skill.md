---
title: "baoyu-slide-deck：开源的 AI Agent 生成 PPT 幻灯片 skill"
source: github
url: "https://github.com/JimLiu/baoyu-skills/blob/main/skills/baoyu-slide-deck/SKILL.md"
saved_date: "2026-07-12"
fetched_at: "2026-07-12 08:38"
version: "1.117.4"
license: "MIT"
tags:
  - ai-tool-review
  - agent-skill
  - openclaw-skill
  - slide-deck
  - ppt-generation
  - baoyu-skills
related_projects:
  - "1-Projects/德勤（PPT 交付物直接受益）"
  - "1-Projects/求职-德勤（求职 PPT 可用）"
source_repo:
  name: "JimLiu/baoyu-skills"
  stars: 23441
  forks: 2647
  created: "2026-01-13"
  updated: "2026-07-11"
---

# baoyu-slide-deck —— 把内容变成可分享的幻灯片图片

> **核心定位**：内容（大纲、文本）→ **专业幻灯片图片**（PNG）→ 可合并成 PPTX/PDF。
> 官方原话："designed for **reading and sharing** (self-explanatory slides, logical scroll flow, social-media-friendly) rather than live presentation"
>
> 即：**不是给现场演讲的**，是**给读者看的、自解释的、社交媒体友好**的 slide。每一页都是一张独立图片，适合微信/小红书/网页发布。

## 一句话价值主张

装上之后，对小助说"做一份关于 X 的 PPT"，小助会自动：

1. 问你风格（17 个 preset）、受众、语种、页数
2. 写大纲 → 写每页 prompt → 调图片生成 API → 输出 PNG → 合并成 PPTX/PDF

---

## 📦 它属于哪个仓库

| 字段 | 值 |
|---|---|
| Repo | [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) |
| Star | **23,441** ⭐ |
| Fork | 2,647 |
| License | MIT |
| Topics | `agent-skills`, `claude-skills`, `codex-skills`, `openclaw-skills` |
| 最新更新 | 2026-07-11 |

这是个**全家桶**，21 个 skills，覆盖内容创作全链路（写作 / 配图 / 翻译 / 转 PDF / 发微信 / 转 HTML / 抓 YouTube / 抓 X ...）。何大人已经用的 `baoyu-comic` / `baoyu-cover-image` / `baoyu-infographic` 也都是这个仓库的。

---

## 🧩 baoyu-slide-deck 本身（v1.117.4）

### 9 步工作流

1. 加载偏好（`EXTEND.md`）
2. **确认需求**（AskUserQuestion / 纯文本询问 — style / audience / slides / lang）
3. 分析内容 → 决定结构
4. **生成大纲**（outline.md）
5. 写每页 prompt（`prompts/NN-slide-{slug}.md`，**hard requirement** — 这是可复现性记录）
6. （可选）审 prompt
7. **生成图片**（调图片生成 API，**批量** 4 张并发）
8. 合并 PPTX/PDF
9. 交付

### 17 个风格 Preset（按 4 维组合）

| 维度 | 取值 |
|---|---|
| **Texture** | clean / grid / organic / pixel / paper |
| **Mood** | professional / warm / cool / vibrant / dark / neutral / macaron |
| **Typography** | geometric / humanist / handwritten / editorial / technical |
| **Density** | minimal / balanced / dense |

**预设例子**：

- `blueprint`（默认）：grid + cool + technical + balanced — **架构图、系统设计**
- `corporate`：clean + professional + geometric + balanced — **投资人 PPT、商业提案**（最贴近德勤咨询交付物）
- `editorial-infographic`：clean + cool + editorial + dense — **科技解释、研究报告**
- `bold-editorial`：clean + vibrant + editorial + balanced — **产品发布、keynote**
- `intuition-machine`：clean + cool + technical + dense — **技术文档、学术**
- `notion`：clean + neutral + geometric + dense — **产品 demo、SaaS**

### 自动匹配（按内容信号）

- `architecture, system, data, analysis, technical` → `blueprint`
- `investor, quarterly, business, corporate` → `corporate`
- `explainer, journalism, science communication` → `editorial-infographic`
- ...（共 17 条规则，未匹配则用 `blueprint` 默认）

### 内容信号 → 页数启发式

| 字数 | 推荐页数 |
|---|---|
| < 1000 | 5–10 |
| 1000–3000 | 10–18 |
| 3000–5000 | 15–25 |
| > 5000 | 20–30（**考虑拆分**） |

### 关键约定（不可违反）

- ⛔ **绝不**用 SVG / HTML / canvas 替代光栅图片（slide-deck 是图片资产）
- ⛔ **绝不**用 ImageMagick / Pillow 在已生成图片上"修补"文字（错字就重生成 prompt）
- ⛔ **绝不**用 subagent 只为并行渲染（subagent 留给创意探索）
- ⛔ **必须**每个 slide prompt 先存盘到 `prompts/NN-slide-{slug}.md` 再调 API（可复现性）

---

## 🔧 后端依赖：baoyu-image-gen（v2.1.0）

slide-deck 自己**不调任何图片生成 API**，完全委托给 `baoyu-image-gen`。

### baoyu-image-gen 支持的 provider（11 个）

| Provider | 备注 |
|---|---|
| **OpenAI GPT Image 2** | 官方主力 |
| Azure OpenAI | 企业版 |
| Google | Gemini Image |
| OpenRouter | 聚合 |
| **DashScope（阿里通义万象）** | 国内可用 |
| **Z.AI GLM-Image** | 智谱 |
| **MiniMax** ⭐ | **何大人的 M3 模型供应商，原生支持** |
| Jimeng（即梦） | 字节 |
| Seedream（豆包） | 字节 |
| Replicate | 开源模型聚合 |
| Agnes | ？（未深查） |

**核心利好**：何大人用的是 **MiniMax-M3**，baoyu-image-gen **原生支持 MiniMax**。这意味着：

> ✅ 装上 baoyu-slide-deck + baoyu-image-gen，配 EXTEND.md 选 minimax provider，**直接能用**，不用额外申请 API key（前提：已有的 MiniMax 凭证能用于图片生成 API）。

⚠️ **需验证**：何大人的 MiniMax 凭证是不是图片生成 API 的，还是只对话 API？—— 这是装之前必须确认的 1 件事。

---

## 🎯 对何大人的价值评估

### 直接价值（高）

| 场景 | 用 baoyu-slide-deck 的收益 |
|---|---|
| **德勤咨询交付物 PPT** | 自动出 slide 图，`corporate` / `editorial-infographic` preset 直接对应咨询风 |
| **求职 PPT（已有 mini case）** | 包装自己的方案/作品集，可视化产出 |
| **元智 OS 介绍 PPT** | 产品 demo 类，用 `notion` preset |
| **公众号文章配图** | 已有 baoyu-cover-image / baoyu-infographic，但 slide-deck 是**多页连贯** |

### 潜在收益

| 场景 | 说明 |
|---|---|
| **Hermes / AgentSpace 平台演示 PPT** | 德勤 M5/M6 任务的产出可直接做成可读 slide 发给 stakeholder |
| **训练营/课程资料** | 复用 vault 里的笔记转成教学 slide，`chalkboard` / `hand-drawn-edu` preset |

### 局限（必须说）

1. **依赖图片生成 API 的额度**：20 页 deck × 2–4 次 retry = 40–80 张图，按 MiniMax / DashScope 0.1–0.3 元/张 ≈ **4–24 元/份 deck**。不算贵但不是 0 成本。
2. **每张图都是独立生成**：不像传统 PPT 一个模板批量套，**视觉一致性靠 prompt 工程的 session ID 维持**（有损）
3. **文字不能后期修补**：错字只能整张重生成，**对中文 OCR 质量敏感**
4. **不适合需要逐字动画 / 现场交互**的演讲场景（官方明确说不为此设计）

---

## 🔗 与 vault 已有材料的关联

| vault 现有 | 与 slide-deck 的关系 |
|---|---|
| `baoyu-comic` / `baoyu-cover-image` / `baoyu-infographic` | 同仓库兄弟 skill，**同一套 EXTEND.md 体系**（共享 `baoyu-image-gen` 后端） |
| `1-Projects/德勤/AI-Native/` 下的方案文档 | 这些 markdown → 一键转德勤交付 PPT（潜在巨大杠杆） |
| `2-Areas/公众号文章/` 里的笔记 | 转成 `editorial-infographic` 风格的 slide 长图，发小红书 / 知乎 |
| `3-Resources/PPT/毛概/` 等现有 PPT | 反向参考：现有 PPT 可拆成 prompt，反哺 slide-deck 的 outline 训练 |

---

## ❓ 装之前必须确认 1 件事

> **何大人手上的 MiniMax API key 是图片生成 API 的吗？还是只对话 API？**

- 如果是图片 API（或同账号有图片权限）→ **直接装，5 分钟跑通**
- 如果只是对话 API → 装 slide-deck 后还得**单独申请** MiniMax 图片 API（或换 DashScope / 即梦）

---

## 📥 推荐的安装顺序（如果决定装）

```bash
# 1. clone 到本地
git clone https://github.com/JimLiu/baoyu-skills.git /tmp/baoyu-skills

# 2. 装后端（图片生成）
mkdir -p ~/.openclaw/workspace/skills/baoyu-image-gen
cp -r /tmp/baoyu-skills/skills/baoyu-image-gen/* ~/.openclaw/workspace/skills/baoyu-image-gen/
# 跑 first-time setup：选 provider、模型、保存路径

# 3. 装前端（slide deck）
mkdir -p ~/.openclaw/workspace/skills/baoyu-slide-deck
cp -r /tmp/baoyu-skills/skills/baoyu-slide-deck/* ~/.openclaw/workspace/skills/baoyu-slide-deck/

# 4. 验证：跟小助说"做一份关于 X 的 PPT（5 页 corporate 风）"
```

> ⚠️ **必须跑通一次最小验证**（1 页 deck）再扩展，否则 30 页跑失败就白烧钱。

---

## 关键 URL

- **slide-deck SKILL.md**：https://github.com/JimLiu/baoyu-skills/blob/main/skills/baoyu-slide-deck/SKILL.md
- **repo**：https://github.com/JimLiu/baoyu-skills
- **JimLiu 本人**：活跃的 AI Agent skill 作者，MIT 协议友好