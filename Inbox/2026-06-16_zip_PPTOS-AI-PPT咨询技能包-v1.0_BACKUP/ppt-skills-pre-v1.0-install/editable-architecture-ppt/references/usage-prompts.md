---
title: Usage Prompts
type: note
tags:
- Obsidian
- PPT
- Vault
- 产品经理
---
# Usage Prompts

## Minimal Prompt

```text
使用 editable-architecture-ppt 技能，给我生成一个可编辑 PPT。
主题：[填写主题]
风格：[例如 蓝白科技风 / 投资路演风 / 教育产品方案风]
要求：单页信息图，包含主流程、能力层、实现方式、数据回流，并记录过程。
```

## From Image

```text
使用 editable-architecture-ppt 技能，复刻这张图为可编辑 PPT。
要求：
1. 尽量保留原图的信息结构、排版密度、图标风格和色彩层级。
2. 先生成 HTML 预览，再生成可编辑 PPTX。
3. PPT 不要整页截图，文字、卡片、箭头要能编辑。
4. 记录生成过程和验证结果。
```

## From Obsidian Vault or Repository

```text
使用 editable-architecture-ppt 技能，读取这个仓库/Obsidian vault 里的相关笔记，生成一个可编辑 PPT。
主题：[填写主题]
请先识别相关资料，再整理成结构化模型，最后输出预览 HTML、可编辑 PPTX、生成脚本和过程文档。
```

## Strong Editability Requirement

```text
最终 PPT 必须可编辑：标题、模块文字、卡片、箭头、编号、底部说明都要是 PPT 原生对象。除 logo、截图、复杂插画外，不要使用图片代替内容。
```
