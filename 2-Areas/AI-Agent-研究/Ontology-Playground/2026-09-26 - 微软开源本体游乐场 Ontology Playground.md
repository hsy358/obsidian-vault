---
title: "微软开源"本体游乐场"Ontology Playground：可视化搭本体、一键导出 Fabric IQ"
description: 微软开源可视化本体编辑器，支持 RDF/OWL 导入导出，对接 Microsoft Fabric IQ
source: https://mp.weixin.qq.com/s/KHX_2Z4Mmva0wJZVr-DYFQ
author: 视界君（玩转 AI 视界）
uploaded_date: 2026-09-26
tags: [Microsoft, Ontology, Fabric, 本体论, RDF, OWL, AI-Agent]
file_path: /root/vault/2-Areas/AI-Agent-研究/Ontology-Playground/2026-09-26 - 微软开源本体游乐场 Ontology Playground.md
---

# 微软开源"本体游乐场" Ontology Playground

> GitHub：https://github.com/microsoft/Ontology-Playground
> 在线体验：https://microsoft.github.io/Ontology-Playground
> 许可：MIT（推测）

## 是什么

**Ontology Playground** 是微软开源的免费 Web 应用，用于学习本体（Ontology）概念和 **Microsoft Fabric IQ**。

## 核心功能

| 功能 | 说明 |
|---|---|
| **可视化本体编辑** | 拖拽式设计本体结构 |
| **预置本体目录** | Explore 预构建本体（如 Fourth Coffee 供应链本体） |
| **导入/导出 RDF/OWL** | 支持完整 RDF/XML 格式 round-trip，可导出为 Fabric IQ 兼容格式 |
| **交互式图表** | 可视化实体关系图 |
| **自然语言查询** | NL2Ontology 自然语言查询本体 |
| **零后端** | 纯静态站点，完全前端实现 |

## 核心概念：Fabric IQ Ontology

Microsoft Fabric IQ 中的 Ontology（本 体）是**企业级语义层**，用于：

- 定义企业概念为实体类型（Entity Types）
- 定义属性（Properties）和关系（Relationships）
- 绑定到 OneLake 数据源（Lakehouse 表 + 实时数据）
- 为 AI Agent 提供共享上下文层（Shared Context Layer）

```
实体类型：Customer / Order / Product / Store / Supplier / Shipment
关系：places / contains / sourcedFrom / sentBy / deliveredTo / carries
```

## 对德勤 MVP 的参考价值

| 维度 | 关联 |
|---|---|
| **语义层设计** | Fabric IQ Ontology = 结构化业务语义层，德勤 Agent 也需要类似语义上下文 |
| **RDF/OWL 导出** | 本体可被 Agent 理解，适合知识密集型场景 |
| **实体关系可视化** | 可以借鉴用于德勤 MVP 的工单/项目本体设计 |
| **自然语言查询** | NL2Ontology = 用自然语言查询结构化本体，类似 RAG 的结构化检索 |

## 相关链接

- GitHub：https://github.com/microsoft/Ontology-Playground
- 在线体验：https://microsoft.github.io/Ontology-Playground
- Microsoft Fabric 文档：https://learn.microsoft.com/en-us/fabric/iq/ontology/overview

---

*存档时间：2026-09-26*
