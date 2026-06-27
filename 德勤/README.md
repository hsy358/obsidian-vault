---
title: 德勤项目资料库
type: project-index
created: 2026-06-27
tags: [德勤, 项目, 索引]
---

# 德勤项目资料库

> 收集所有跟德勤工作相关的资料、文章、报告、笔记。

## 目录结构

```
德勤/
├── README.md                       # 本页（索引）
├── AI-Native/                      # 主题 1：AI-Native R&D 项目
│   ├── 公众号文章/
│   ├── 报告/
│   ├── 截图/
│   └── 笔记/
└── <其他主题>/                     # 后续按需新建
```

## 已有内容

### AI-Native

- [[AI-Native/公众号文章/2026-06-16 - Skill Zoo：一站式 Agent 技能管理工具|Skill Zoo：一站式 Agent 技能管理工具]]（2026-06-16，星汐引力）— 第三方 Agent Skills 管理工具的 SSOT 软链设计参考

## 关联文档（不在本目录，在 Research/）

> 历史研究文档保留在 `/root/vault/Research/`（避免破坏时间线），这里是关联引用：

- `/root/vault/Research/2026-06-17_AI-Native_R/` — 早期 AI-Native R&D 研究素材
- `/root/vault/Research/2026-06-17_AI-Native_RD/` — AI-Native R&D 截图与对照分析
- `/root/vault/Research/2026-06-17 - AI-Native R&D 全流程方案 v1.0.md` — v1.0 方案
- `/root/vault/Research/2026-06-17 - AI-Native R&D 自驱动闭环 v3.x.md` — v3.x 系列（v3.0 ~ v3.5）
- `/root/vault/Research/2026-06-19 - Self-Driving R&D v4.x ~ v5.0-lite.md` — 后续方案迭代
- `/root/vault/Inbox/2026-06-16_deloitte-ppt-screenshots/` — 德勤官方 PPT 截图
- `/root/vault/Inbox/2026-06-16_html_德勤2026趋势中国版报告页.md` — 德勤 Tech Trends 2026 中文版

## 入库规范

### 微信文章
```
AI-Native/公众号文章/YYYY-MM-DD - 标题.md
```
frontmatter 必带：`tags: [德勤, ai-native, 公众号, <主题标签>]`

### 报告（PDF / HTML）
```
AI-Native/报告/<原文件名>
```
按 2026-06-16 二进制文档处理规范建 sidecar（`type: document-metadata`）。

### 截图 / 图片
```
AI-Native/截图/YYYY-MM-DD_img_<描述>.jpg
```
配 sidecar，记录来源 / 上下文。

### 笔记 / 分析
```
AI-Native/笔记/YYYY-MM-DD - <主题>.md
```
自由格式 frontmatter + 正文。

## 添加新主题

```bash
cd /root/vault
mkdir -p "德勤/<新主题名>/{公众号文章,报告,截图,笔记}"
```

新增后在 `README.md` 的「目录结构」和「已有内容」两节同步更新。