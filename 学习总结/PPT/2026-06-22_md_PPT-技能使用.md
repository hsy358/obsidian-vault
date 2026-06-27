---
title: PPT-技能使用
description: 这 5 个 skill 的组合方式，可以理解成一条 咨询级 PPT 生产流水线。
type: study-note
tags:
- Obsidian
- PPT
- Vault
- 知识管理
---
这 5 个 skill 的组合方式，可以理解成一条 **咨询级 PPT 生产流水线**。

标准顺序是：

`1. knowledge-to-deck → 2. consulting-deck-os → 3. editable-architecture-ppt → 4. ppt-production-engine → 5. ppt-quality-review`

**每个 skill 负责什么**

1. **knowledge-to-deck**  
    当你有资料来源时用。比如 Obsidian vault、公众号文章、PRD、PDF、Word、会议纪要。  
    作用：把资料整理成观点、证据、来源地图。
    
2. **consulting-deck-os**  
    总控。  
    作用：确定受众、目标、故事线、页面结构、走哪种生成路线。
    
3. **editable-architecture-ppt**  
    专门处理复杂单页图。  
    比如架构图、流程图、能力地图、平台蓝图。
    
4. **ppt-production-engine**  
    把 slides.json、页面规格、内容结构真正生成成可编辑 PPTX。
    
5. **ppt-quality-review**  
    最后审查。  
    看逻辑、版式、可编辑性、是否整页图片、文字是否能抽取、是否能交付。
    

**典型用法 1：从资料生成咨询 PPT**  
你可以这样说：

`使用 Consulting Deck OS 技能组，读取 D:\Obsidian\MyVault\notes\wechat\公众号文章 中和 AI PPT 相关的文章，做一份“AI 咨询级 PPT 生产体系”方案 deck。 要求：15 页，咨询公司风格，可编辑 PPT，附过程记录和质量检查。`

我会自动按：

`knowledge-to-deck → consulting-deck-os → ppt-production-engine → ppt-quality-review`

如果中间有复杂架构图页面，再调用：

`editable-architecture-ppt`

**典型用法 2：只做一张复杂架构图**

`使用 editable-architecture-ppt，帮我做一张“AI Hub 课程资产自动生成流程图”的可编辑 PPT 单页。 要求：像咨询报告里的架构图，蓝白科技风，保留生成过程。`

这时不一定需要全套 5 个，只用：

`editable-architecture-ppt → ppt-quality-review`

**典型用法 3：已有 slides.json，直接生成 PPT**

`使用 ppt-production-engine，根据这个 slides.json 生成一份可编辑 PPTX，并保留讲稿。 生成后使用 ppt-quality-review 检查可编辑性和版式问题。`

**一句话规则**

- 有资料：先 knowledge-to-deck
- 要咨询方案：用 consulting-deck-os
- 有复杂图：用 editable-architecture-ppt
- 要生成 PPT：用 ppt-production-engine
- 要交付：必须用 ppt-quality-review

![[ppt-skills.rar]]