# DeckSpec · EY《Seeing China's AI Reality》24P 一比一复刻

> 按 `image-to-editable-ppt` skill 的 deckspec-template 填写。

---

## 项目信息

- **项目名**：`EY-24P-Reproduction`
- **PPT 主题**：EY 安永《看清中国 AI 的现实》24 页高管 deck 一比一复刻
- **作者**：何大人 / 小助
- **日期**：2026-09-01
- **目标产出路径**：`/root/vault/1-Projects/image-to-editable-ppt-demo/EY-24P/`
- **使用 skill**：`image-to-editable-ppt`

---

## 8 个必填字段

### 1. 目标读者（who）

- [ ] 决策者
- [x] 执行者（团队成员 / 工程师）
- [x] 客户（外部）
- [x] 内部分享（同事）
- [ ] 公开场合
- [ ] 其他

**具体画像**：EY 内部 LELI China 高管 · 咨询同行 · 何大人自己学习参考 · 给同事/客户的借鉴材料

### 2. PPT 目标（why）

- [x] 说服
- [ ] 汇报
- [x] 培训
- [ ] 审批
- [ ] 路演
- [x] 知识沉淀

**一句话目标**：把 EY 24 页扫描 PDF 一比一复刻为可二次编辑的 PPTX，保留原 EY 风格 + 全部数据 + 全部金句

### 3. 使用场景（where/when）

- [x] 正式会议
- [x] 内部周会/月会
- [ ] 路演/大会
- [ ] 在线分享
- [x] 自学阅读
- [ ] 其他

**场景细节**：自学阅读 + 内部分享 + 给同事/客户做咨询 deck 借鉴

### 4. 时长（how long）

- **演讲时长**：自学为主，不强制
- **Q&A 时长**：N/A
- **总时长**：N/A

### 5. 页数（how many）

- **建议页数**：**24 页（严格保留原页数）**
- **页面密度**：[x] 标准（结论 + 3-5 个 bullet）

### 6. 风格（how）

- [x] 咨询级（EY 安永 Executive Discussion Deck）
- [ ] 技术架构
- [ ] 教学/培训
- [ ] 爆款视觉
- [ ] 通用商务
- [ ] 其他

**风格参考**：EY 安永 Executive Discussion Deck 系列（深海军蓝 + teal 青色 + 衬线大标题）

### 7. 可编辑要求（editable）

- [x] **必须可二次编辑**

**约束**：
- 文字必须可改 → 用 native text
- 形状必须可选中 → 用 native shapes
- 整体视觉布局可调

### 8. 已有素材（input）

- **输入文件**：
  - `/root/vault/0-Inbox/2026-09-01_pdf_China_AI_Environment_and_Business_Reinvention_24P_FINAL.pdf`（EY 原 PDF 4.2 MB，扫描版）
- **vault 里有的相关材料**：
  - sidecar 含 14 大金句 + 4 段结构
  - 渲染的高清 PNG 页（/root/.openclaw/workspace/tmp/pdf_pages/）
- **数据/图表**：EY 报告 14 项关键数据
- **视觉参考**：EY 安永 Executive Discussion Deck 风格
- **多模态识图提取**：已完成 24 页内容分析

---

## 路由判断

- **使用 skill**：`image-to-editable-ppt`
- **下游 skill 协同**：
  - Stage ⑤ 编译借鉴：`editable-architecture-ppt` 的 pptxgenjs 技术
- **理由**：用户明确要求"用 image-to-editable-ppt skill 一比一复刻"

---

## 其他备注

- **强制要求**：
  - 24 页严格保留
  - 14 项关键数据全部保留（515M、36.5%、302→868、1.2T+、30%+、54%、10B+、43%+、99.98%、+275% 等）
  - 14 大金句全部保留
  - EY 配色锁定（深蓝 + teal）
  - 可二次编辑（核心诉求）
- **禁忌**：
  - 不能图片化扁平
  - 不能简化数据
  - 不能改视觉风格
- **特殊约束**：
  - 复用之前 v2 沉淀的 31 个 PIL 自绘图标 + 1 中国地图底图
  - 输出 pptxgenjs 生成脚本（可重跑）

---

## 验收标准

- [x] 8 个字段全填
- [x] 一句话能说清"用 image-to-editable-ppt skill 把 EY 24 页 PDF 转成可编辑 PPTX"
- [x] 路由判断完成
- [x] 已复制到项目目录 `/root/vault/1-Projects/image-to-editable-ppt-demo/EY-24P/deckspec.md`

---

**填写日期**：2026-09-01
**填表人**：何大人 / 小助
**使用 skill**：`image-to-editable-ppt` (v1.0)