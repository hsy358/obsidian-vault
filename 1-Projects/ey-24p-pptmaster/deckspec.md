# DeckSpec · EY《Seeing China's AI Reality》前 4 页

> 按 `ppt-master` skill 的 5 阶段工作流，路由到 `image-to-editable-ppt` 子 skill，用方案 D（OCR 精准对齐 + 原 PDF 底图）生成。

---

## 项目信息

- **项目名**：`ey-24p-pptmaster`
- **PPT主题**：EY 安永《Seeing China's AI Reality》24 页高管 deck → 前 4 页一比一还原
- **使用 skill**：`ppt-master` → `image-to-editable-ppt`
- **方法**：方案 D（OCR 提取底图文字位置 + v2 校对文字 + 原 PDF 底图）
- **作者**：何大人 / 小助
- **日期**：2026-09-01
- **目标产出路径**：`/root/vault/1-Projects/ey-24p-pptmaster/`

---

## 8 个必填字段

### 1. 目标读者（who）

- [ ] 决策者（C-level / 总监 / VP）
- [x] 执行者（团队成员 / 工程师）
- [x] 客户（外部）
- [x] 内部分享（同事）
- [ ] 公开场合（路演 / 大会）
- [ ] 其他：___

**具体画像**：EY 内部 LELI China 高管 · 咨询同行 · 何大人自己学习参考 · 给同事/客户的借鉴材料

### 2. PPT 目标（why）

- [x] 说服（让对方同意某事）
- [ ] 汇报（让对方了解进展）
- [x] 培训（让对方学会某事）
- [ ] 审批（让对方签字）
- [ ] 路演（吸引投资/合作）
- [x] 知识沉淀（内部归档）

**一句话目标**：把 EY 24 页扫描 PDF 一比一复刻为可二次编辑的 PPTX，保留原 EY 风格 + 全部数据 + 全部金句

### 3. 使用场景（where/when）

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

- **建议页数**：**4 页（先做前 4 页验证效果）**
- **页面密度**：[x] 标准（结论 + 3-5 个 bullet）

### 6. 风格（how）

- [x] 咨询级（EY 安永 Executive Discussion Deck）
- [ ] 技术架构
- [ ] 教学/培训
- [ ] 爆款视觉
- [ ] 通用商务
- [ ] 其他：___

**风格参考**：EY 安永 Executive Discussion Deck 系列（深海军蓝 + teal 青色 + 衬线大标题）

### 7. 可编辑要求（editable）

- [x] **必须可二次编辑**

**约束**：
- ✅ 文字必须可改 → 用 native text
- ✅ 形状必须可选中 → 用 native shape
- ✅ 整体视觉布局可调

### 8. 已有素材（input）

- **输入文件**：
  - `/root/vault/0-Inbox/2026-09-01_pdf_China_AI_Environment_and_Business_Reinvention_24P_FINAL.pdf`（4.2 MB，扫描版）
- **vault 里有的相关材料**：
  - sidecar 含 14 大金句 + 4 段结构
  - 渲染的高清 PNG 页（`/root/.openclaw/workspace/tmp/pdf_pages/`）
- **多模态识图提取**：已完成 24 页内容分析（之前会话）

---

## 路由判断（ppt-master 标准）

按 ppt-master 路由表：
- 用户场景：**把已有 PDF 报告 → 可编辑 PPTX**（扫描版复刻）
- 最接近的子 skill：**`image-to-editable-ppt`**（用户后装的，专门处理此场景）
- 路由结果：`ppt-master` 编排 → `image-to-editable-ppt` 执行 → `ppt-production-engine` 编译

---

## 其他备注

- **强制要求**：
  - 前 4 页严格保留（p01 封面、p02 Agenda、p03 Part I 章节过渡、p04 6 大数据卡片）
  - 14 项关键数据全部保留（515M、36.5%、302→868、1.2T+、30%+、54%、10B+、41%、2、43%+、99.98%、+275% 等）
  - 14 大金句全部保留
  - EY 配色锁定（深蓝 + teal）
  - 可二次编辑（核心诉求）
- **禁忌**：
  - 不能图片化扁平（保留 native text 覆盖层）
  - 不能简化数据
  - 不能改视觉风格
- **特殊约束**：
  - 用方案 D（OCR 提取底图文字位置 + v2 校对文字 + 原 PDF 底图作 visual context）
  - 输出 pptxgenjs 生成脚本（可重跑）

---

## 验收标准

- [x] 8 个字段全填
- [x] 一句话能说清"用 ppt-master → image-to-editable-ppt 把 EY 24 页 PDF 一比一复刻成可编辑 PPTX"
- [x] 路由判断完成
- [x] 已复制到项目目录 `/root/vault/1-Projects/ey-24p-pptmaster/deckspec.md`

---

**填写日期**：2026-09-01
**填表人**：何大人 / 小助
**使用 skill 链路**：`ppt-master` → `image-to-editable-ppt`（方案 D）