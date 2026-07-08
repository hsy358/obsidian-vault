---
type: open-questions
title: 待确认问题 — 元知思政教学端试点
related_clarification: 02-clarification.md
related_acceptance: 04-acceptance-criteria.md
analysis_date: 2026-07-08
analyst: 小助
status: draft-v1
---

# 05 · 待确认问题 / Open Questions

> 所有问题都追溯到具体用例、流程步骤、AC 或实施切片。
> 优先级：P0（不澄清无法启动）/ P1（影响部分功能设计）/ P2（细节问题）

---

## P0 · 高杠杆（必须先解决）

### Q-001：知识图谱 4 类子图的具体数据源和构建方法
- **Category**：engineering
- **Status**：pending
- **Problem**：4 类图谱（知识点/价值引领点/案例素材/模板）是怎么自动构建的？依赖什么数据源、什么模型？
- **To Clarify**：
  - Q-001.1：4 类图谱是同一模型生成还是不同模型/规则？
  - Q-001.2：价值引领点图谱的"思政导向"判定标准是什么？（参考 Q-005）
  - Q-001.3：图谱节点数/关系数的合理预期是多少？（P6 案例显示 512 节点，是平均还是峰值？）
- **Impact**：AR-04 知识图谱自动构建 / AC-005 / 切片 S-002
- **Clarification Target**：元知技术负责人
- **追溯**：UC-P02 Step 4 / AC-005 / S-002

### Q-002：9 类资产生成的 AI 模型/工具链清单
- **Category**：engineering
- **Status**：pending
- **Problem**：PPT/教案/讲义/题库等 9 类资产各自用什么 AI 模型/工具生成？
- **To Clarify**：
  - Q-002.1：9 类资产是否都用同一 LLM，还是有专用工具？
  - Q-002.2：每类资产的生成准确率/可用率有量化指标吗？
  - Q-002.3：生成 1 门课程的所有 9 类资产，需要多少算力/时间？
- **Impact**：AR-07 9 类资产批量生成 / AC-010 / 切片 S-003
- **Clarification Target**：元知技术负责人
- **追溯**：UC-P03 Step 1-7 / AC-010 / S-003

### Q-003：老师两次确认节点的 SLA
- **Category**：business
- **Status**：pending
- **Problem**：老师两次确认（结构确认 + 内容审核）的最迟反馈时间是多久？超时如何升级？
- **To Clarify**：
  - Q-003.1：结构确认的最迟反馈时间是 1 天？2 天？
  - Q-003.2：内容审核的最迟反馈时间是 2 天？4 天？
  - Q-003.3：超时后是触发提醒、升级到课程负责人、还是自动放行？
- **Impact**：AR-06 / AR-09 / 试点周期 6-14 天的可达成性
- **Clarification Target**：元知 PM + 校方
- **追溯**：UC-P02 Step 1 / UC-P04 Step 1 / AC-008 / AC-013

### Q-004：5 项验收标准的定量指标
- **Category**：business
- **Status**：pending
- **Problem**：5 项验收标准（政治方向/理论准确/教学可用/格式规范/沉淀复用）目前是定性描述，缺定量指标。
- **To Clarify**：
  - Q-004.1：政治方向正确的判定主体是元知方？校方？还是上级部门？
  - Q-004.2：理论准确的"准确率"如何量化？（如：与权威教材匹配度 95%+？）
  - Q-004.3：教学可用的"可用率"如何衡量？（如：老师直接使用不修改的比例？）
- **Impact**：AC-017 / 验收红线
- **Clarification Target**：元知 PM + 校方教学督导
- **追溯**：UC-P05 Step 3 / AC-017

### Q-005：价值引领点图谱的"思政导向"判定标准
- **Category**：business
- **Status**：pending
- **Problem**：思政课程的核心是"价值引领"，但"思政导向"如何判定？缺标准则验收有歧义。
- **To Clarify**：
  - Q-005.1：思政导向是否对齐教育部课程标准？具体哪个版本？
  - Q-005.2：是否需要马克思主义理论专家/思政课专家审核？
  - Q-005.3：是否有可量化的"思政元素覆盖率"指标？
- **Impact**：BR-07 / AC-017
- **Clarification Target**：元知 PM + 校方思政课专家
- **追溯**：UC-P04 Step 2 / BR-07

---

## P1 · 中等（影响部分功能，可先用默认方案）

### Q-006：知识图谱节点的"实体识别"准确率
- **Category**：engineering
- **Status**：pending
- **Problem**：知识图谱自动构建依赖实体识别（NER），思政课程术语（如"中国式现代化""伟大建党精神"）识别准确率未知。
- **To Clarify**：
  - Q-006.1：思政课程专用 NER 模型是否单独训练？
  - Q-006.2：实体识别的人工复核比例？
- **Impact**：AC-005
- **Default 方案**：用通用 LLM + 人工复核
- **追溯**：UC-P02 Step 4

### Q-007：资产生成失败的处理
- **Category**：engineering
- **Status**：pending
- **Problem**：资产生成失败（模型异常/超时/质量不达标）时如何处理？
- **To Clarify**：
  - Q-007.1：失败重试几次？
  - Q-007.2：重试失败后是降级（部分资产用模板填充）还是阻塞？
- **Impact**：AR-07 / 边界异常场景
- **Default 方案**：重试 3 次 + 升级人工
- **追溯**：UC-P03 Step 1-7 / 边界异常场景表

### Q-008：课程包 v2.0 触发条件
- **Category**：business
- **Status**：pending
- **Problem**：4.3 提到 v1.x → v2.0 需重新走完整 8 步，但 v2.0 触发条件未明确。
- **To Clarify**：
  - Q-008.1：政策变化（如党的二十大精神）是否自动触发 v2.0？
  - Q-008.2：教师对 v1.x 提了 3 次以上修改意见，是否升级 v2.0？
  - Q-008.3：v2.0 触发后是覆盖 v1.x 还是并存？
- **Impact**：4.2 状态流转 / 后续迭代
- **Default 方案**：政策变化自动触发，并存保留 v1.x
- **追溯**：4.3 状态流转图

### Q-009：校方模板规范的强制级别
- **Category**：business
- **Status**：pending
- **Problem**：8 类必交材料中的"学校模板规范"是必须提供，还是建议提供？
- **To Clarify**：
  - Q-009.1：无校方模板时元知方是否用"通用模板"兜底？
  - Q-009.2：校方模板与元知方风格的冲突如何解决？
- **Impact**：AC-001 / 资产风格
- **Default 方案**：建议提供，无则用通用模板
- **追溯**：AC-001 / 表 1 第 8 行

### Q-010：老师权限边界（删除/导出）
- **Category**：business
- **Status**：pending
- **Problem**：老师在工作台上的权限边界未明确。
- **To Clarify**：
  - Q-010.1：老师能否删除已上传的资料？
  - Q-010.2：老师能否导出资产包的全部内容？还是仅限定部分？
  - Q-010.3：老师能否在审核中拒绝元知方提交的修改？
- **Impact**：3.2 权限矩阵
- **Default 方案**：老师可读、可写自己上传的，不可删除他人资产，可导出 v1.0 全量
- **追溯**：3.2 权限矩阵

---

## P2 · 细节（开发中确认）

### Q-011：单门课程的资产生成顺序
- **Category**：engineering
- **Status**：pending
- **Problem**：7 步推荐生成顺序是固定还是可调？
- **Default 方案**：固定按 7 步顺序
- **追溯**：AR-07

### Q-012：资源库沉淀的检索机制
- **Category**：engineering
- **Status**：pending
- **Problem**：可复用资产库的检索（按学校/学科/章节）如何实现？
- **Default 方案**：按学校/学科/章节三级标签
- **追溯**：AR-13

### Q-013：版本号语义化
- **Category**：engineering
- **Status**：pending
- **Problem**：v1.0 → v1.1 → v2.0 的语义化规则是？
- **Default 方案**：v1.x = 局部修改 / v2.0 = 重大内容更新
- **追溯**：4.3 状态流转规则

---

## 跟踪表

| ID | Title | Priority | Category | Status | Owner |
|---|---|---|---|---|---|
| Q-001 | 知识图谱 4 类子图的数据源和构建方法 | P0 | engineering | pending | 元知技术 |
| Q-002 | 9 类资产生成的 AI 工具链 | P0 | engineering | pending | 元知技术 |
| Q-003 | 老师两次确认 SLA | P0 | business | pending | 元知 PM + 校方 |
| Q-004 | 5 项验收标准定量指标 | P0 | business | pending | 元知 PM + 教学督导 |
| Q-005 | 思政导向判定标准 | P0 | business | pending | 元知 PM + 思政专家 |
| Q-006 | 知识图谱 NER 准确率 | P1 | engineering | pending | 元知技术 |
| Q-007 | 资产生成失败处理 | P1 | engineering | pending | 元知技术 |
| Q-008 | v2.0 触发条件 | P1 | business | pending | 元知 PM |
| Q-009 | 校方模板规范级别 | P1 | business | pending | 元知 PM |
| Q-010 | 老师权限边界 | P1 | business | pending | 元知 PM |
| Q-011 | 资产生成顺序 | P2 | engineering | pending | 元知技术 |
| Q-012 | 资源库检索 | P2 | engineering | pending | 元知技术 |
| Q-013 | 版本号语义化 | P2 | engineering | pending | 元知 PM |
