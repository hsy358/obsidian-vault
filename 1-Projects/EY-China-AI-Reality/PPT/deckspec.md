# DeckSpec · EY《Seeing China's AI Reality》24P 复刻

> 复制本文件，按字段填写。**8 个字段缺一不可**。

---

## 项目信息

- **项目名**：`EY-China-AI-Reality`
- **PPT 主题**：EY 高管 deck《看清中国 AI 的现实》24P 一比一复刻
- **作者**：何大人 / 小助
- **日期**：2026-09-01
- **目标产出路径**：`/root/vault/1-Projects/EY-China-AI-Reality/PPT/`

---

## 8 个必填字段

### 1. 目标读者（who）

谁会看这份 PPT？

- [ ] 决策者（C-level / 总监 / VP）
- [x] 执行者（团队成员 / 工程师）
- [x] 客户（外部）
- [x] 内部分享（同事）
- [ ] 公开场合（路演 / 大会）
- [ ] 其他：___

**具体画像**：EY 内部高管 LELI China · 咨询同行 · 何大人自己学习参考 · 给同事/客户的借鉴材料

### 2. PPT 目标（why）

这份 PPT 要达到什么目的？

- [x] 说服（让对方同意某事）
- [ ] 汇报（让对方了解进展）
- [x] 培训（让对方学会某事）
- [ ] 审批（让对方签字）
- [ ] 路演（吸引投资/合作）
- [x] 知识沉淀（内部归档）

**一句话目标**：把 EY 24 页图像 PDF 一比一复刻成可二次编辑的 PPTX，保留原 EY 风格 + 全部数据 + 全部金句

### 3. 使用场景（where/when）

PPT 在什么场景下用？

- [x] 正式会议（董事会 / 客户评审）
- [x] 内部周会/月会
- [ ] 路演/大会演讲
- [ ] 在线分享（Zoom/腾讯会议）
- [x] 自学阅读（不演讲）
- [ ] 其他：___

**场景细节**：自学阅读 + 内部分享 + 给同事/客户做咨询 deck 借鉴

### 4. 时长（how long）

- **演讲时长**：自学为主，不强制
- **Q&A 时长**：N/A
- **总时长**：N/A

### 5. 页数（how many）

- **建议页数**：24 页（**严格保留原页数**）
- **页面密度**：
  - [ ] 极简（结论 + 1 个图，< 30 字）
  - [x] 标准（结论 + 3-5 个 bullet）
  - [ ] 密集（详细论证 + 数据）
  - [ ] 其他：___

**估算规则**：1 分钟 ≈ 1-2 页（演讲节奏）— 24 页约 12-24 分钟自学阅读

### 6. 风格（how）

- [x] 咨询级（麦肯锡/BCG/EY，少字大图，结论先）
- [ ] 技术架构（架构图 + 组件 + 流程）
- [ ] 教学/培训（节奏感 + 互动页）
- [ ] 爆款视觉（公众号风格，视觉冲击）
- [ ] 通用商务（中性，专业）
- [ ] 其他：___

**风格参考**：EY 安永 Executive Discussion Deck 系列（深蓝 + teal 青色 + 衬线大标题）

### 7. 可编辑要求（editable）

- [x] **必须可二次编辑**（架构/方案评审 / 客户后续改）
- [ ] 一次性使用（演讲完即可）
- [ ] 不确定（默认按可编辑做）

**如果可编辑，约束**：
- ✅ 文字必须可改 → 用 native text，不放进图片
- ✅ 形状必须可选中 → 用 native shapes
- ✅ 图表必须可改数据 → 用 native chart（如需）
- ✅ 整体视觉布局可调（不破坏可读性前提下）

### 8. 已有素材（input）

- **vault 里有的相关材料**：
  - `/root/vault/0-Inbox/2026-09-01_pdf_China_AI_Environment_and_Business_Reinvention_24P_FINAL.pdf`（EY 原 PDF 4.2MB）
  - `/root/vault/0-Inbox/2026-09-01_pdf_China_AI_Environment_and_Business_Reinvention_24P_FINAL.pdf.md`（sidecar 含 11 大金句 + 4 段结构）
  - 渲染的高清 PNG 页（/root/.openclaw/workspace/tmp/pdf_pages/）
- **数据/图表**：EY 报告 6 大数据卡片 + 5 大行业案例数据
- **视觉参考**：EY 安永 Executive Discussion Deck 风格
- **多模态识图提取**：已完成 24 页内容分析

---

## 路由判断

- **推荐子 skill**：
  - `consulting-deck-os`（主控 - 故事线 + deck-brief + storyline + slides.json）
  - `editable-architecture-ppt`（技术 - pptxgenjs native shape 实现）
  - `ppt-production-engine`（编译 - slides.json → PPTX）
- **理由**：用户明确要"一比一复刻 + 可编辑 PPTX"，必须用咨询级 storyline + 复杂架构图 native shape 技术
- **协同 skill**：3 个 skill 协同（咨询方法论 + 架构图技术 + 编译输出）

---

## 其他备注

- **强制要求**：
  - 24 页严格保留
  - 数据点不丢失（515M、36.5%、302→868、1.2T+、30%+、54%、10B+、43%+、99.98%、+275% 等）
  - 14 大金句全部保留
  - EY 风格（深蓝 + teal）
  - 可二次编辑
- **禁忌**：
  - 不能图片化扁平
  - 不能简化数据
  - 不能改视觉风格
- **特殊约束**：
  - 输出 pptxgenjs 生成脚本（可重跑）
  - 输出 preview.html（浏览器预览）
  - 输出 quality-report.md（质检报告）

---

## 验收标准

- [x] 8 个字段全填
- [x] 一句话能说清"把 EY 24 页 PDF 一比一复刻成可编辑 PPTX"
- [x] 路由判断完成
- [x] 已复制到项目目录 `/root/vault/1-Projects/EY-China-AI-Reality/PPT/deckspec.md`

---

**填写日期**：2026-09-01
**填表人**：何大人 / 小助