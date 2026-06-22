---
type: document-metadata
file_type: zip
file_path: 2026-06-16_zip_PPTOS-AI-PPT咨询技能包-v1.0.zip
source: user-upload
uploaded_date: 2026-06-16
title: PPTOS · AI PPT 咨询技能包 v1.0
description: 7 个独立 PPT 技能合集：consulting-deck-os / ppt-production-engine / knowledge-to-deck
  / ppt-quality-review / editable-architecture-ppt / education-training-deck（新增）/
  ai-ppt-consulting-skill-pack（统一入口 PPTOS）
size_bytes: 10039457
language: zh-CN / en
okf_metadata:
  schema: okf-v0.1-inspired
  sidecar_for: 2026-06-16_zip_PPTOS-AI-PPT咨询技能包-v1.0.zip
  contents:
  - consulting-deck-os（升级版 · 加 PPTOS 触发词）
  - education-training-deck（新增 · 教育培训垂直增强）
  - ppt-production-engine（PPT 生产引擎）
  - knowledge-to-deck（知识转 deck）
  - editable-architecture-ppt（可编辑架构 PPT）
  - ppt-quality-review（PPT 质量审查）
  - ai-ppt-consulting-skill-pack（统一入口 · README）
tags:
- AI
- PPT
- PPTOS
- consulting-deck
- education-training
- ppt-skill
- pptos
- skill-pack
- v1.0
- 知识管理
next_actions:
- 安装到 /root/.openclaw/workspace/skills/ppt-skills/
- 验证共享软链接（~/.shared/skills/）
- 未来毛概 PPT 用 education-training-deck 重做
---
# PPTOS · AI PPT 咨询技能包 v1.0

> 本文件是 zip 的 sidecar 元数据。

## 一、用途
跨平台咨询级可编辑 PPT 生产技能包。统一触发词：**PPTOS**。

## 二、7 个技能清单
1. **ai-ppt-consulting-skill-pack** — 顶层入口 / README
2. **consulting-deck-os** — 主控 skill（升级版 · 含 PPTOS 调度）
3. **education-training-deck** — 教育培训垂直增强（**新增** · 适合毛概 PPT）
4. **ppt-production-engine** — PPT 生产引擎
5. **knowledge-to-deck** — 知识转 deck
6. **editable-architecture-ppt** — 可编辑架构 PPT
7. **ppt-quality-review** — PPT 质量审查

## 三、与现有 skills 的对比
- 5 个**完全相同**（knowledge-to-deck / editable-architecture-ppt / ppt-production-engine / ppt-quality-review / consulting-deck-os 大部分）
- 1 个**升级**（consulting-deck-os 加了 PPTOS 触发词 + 调度 education-training-deck 的逻辑）
- 1 个**新增**（education-training-deck 适合教育培训场景）

## 四、推荐使用路径
```
PPTOS（触发词） → knowledge-to-deck（理解资料）
                → consulting-deck-os（决定路线）
                → education-training-deck（教育场景）
                → ppt-production-engine（生成 PPTX）
                → ppt-quality-review（QA 审查）
```

## 五、安装位置
- 实际存储：`/root/.openclaw/workspace/skills/ppt-skills/`
- 共享入口：`~/.shared/skills/ppt-skills/`（软链接）
- 多端共享：Claude / Codex / Codebuddy 同步访问
