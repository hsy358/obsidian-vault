---
type: research-report
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: openclaw-2026-06-28
title: NemoClaw (NVIDIA) — GitHub 仓库研究
description: 1. Project Overview 2. Official Description 3. Core Functions 4. Technical Architecture 5. Comparison with OpenClaw 6. Deployment Assessment 7. Alignment with Deloitte Solution 8. Usage Recommendations 9. References
tags:
- AI
- Agent
- LLM
- NVIDIA
- Sandbox
- Tool-Use
- Security
- Physical-AI
- OpenSource
- Apache-2.0
source:
  url: https://github.com/NVIDIA/NemoClaw
  fetched: 2026-06-28T09:00+08:00
  by: 小助 via web_fetch + web_search
---

# NemoClaw (NVIDIA) — GitHub 仓库研究

**Date:** 2026-06-28  
**Prepared for:** 何大人 · Internal Research  
**Sources:** https://github.com/NVIDIA/NemoClaw · https://docs.nvidia.com/nemoclaw/ · SiliconANGLE · Lasso Security · Lightning AI

---

## 1. 项目概述

**NemoClaw**（`NVIDIA/NemoClaw`）是 **NVIDIA 官方** 推出的**开源参考栈**（open-source reference stack），专为在 **NVIDIA OpenShell** 安全沙箱中运行 AI Agent 而设计。

### 核心定位

```
OpenClaw（开源 Agent）→ NemoClaw（安全加固层）→ OpenShell（沙箱运行时）
```

NemoClaw 不是独立的 Agent，而是 **OpenClaw / Hermes / LangChain Agent 的企业级安全包装器**——在不影响 Agent 能力的前提下，加上网络隔离、凭证管理、推理路由、生命周期控制。

### 版本 & 现状

| 维度 | 信息 |
|---|---|
| **当前版本** | 0.0.58 |
| **项目状态** | **Alpha**（维护者按尽力而为原则响应，无保证 SLA） |
| **License** | Apache 2.0 |
| **维护方** | **NVIDIA 官方** |
| **发布时间** | 2026 年 3 月（与 OpenShell 同期发布） |
| **社区渠道** | GitHub Discussions · GitHub Issues · Discord |

---

## 2. 官方描述（英文原文）

> *"NVIDIA NemoClaw is an open source reference stack for running always-on AI agents more safely inside NVIDIA OpenShell sandboxes. It provides guided onboarding, a hardened blueprint, routed inference, network policy, and lifecycle management through a single CLI."*

### 支持的 Agents

- **[OpenClaw](https://openclaw.ai)**（默认，NemoClaw 的核心用例）
- **[Hermes](https://get-hermes.ai/)**
- **[LangChain Deep Agents Code](https://docs.langchain.com/oss/python/deepagents/code/overview)**

---

## 3. 核心功能拆解

### 3.1 OpenShell 沙箱（核心安全基座）

**OpenShell** 是 NemoClaw 的底层运行时，扮演"安全网关"角色：

- **进程级隔离**：Agent 跑在沙箱内，零额外权限启动
- **网络访问限制**：默认完全阻断外访，管理员可配 egress 策略
- **推理隐私**：所有 LLM 推理流量经 OpenShell 代理，不直连外部 API
- **零代码修改**：现有 OpenClaw/Hermes Agent 无需改造即可入沙箱
- **凭证保护**：API Key 等敏感信息在沙箱内加密存储，Agent 无法直接访问 host 文件（如 `~/.openclaw/openclaw.json`）

> ⚠️ **已知风险**（来自 Lasso Security 研究）：默认配置下 Agent 仍可通过沙箱内路径访问 `~/.openclaw/openclaw.json`，含明文凭证。建议生产环境启用自定义网络策略并收紧文件访问权限。

### 3.2 Routed Inference（推理路由）

- 支持本地推理和云端推理两种路径
- 统一 CLI 配置 inference provider（NVIDIA NIM /第三方 API）
- 推理请求经过 OpenShell 代理，支持审计和流量控制

### 3.3 Network Policy（网络策略）

| 能力 | 说明 |
|---|---|
| **默认拒绝** | 沙箱启动时无任何外访权限 |
| **白名单规则** | 管理员预设允许的 egress 目标 |
| **Operator 审批流** | 高权限操作需人工审批 |
| **动态修改** | 运行时通过 OpenShell CLI 调整策略 |

### 3.4 Blueprint（加固蓝图）

- 预定义安全配置模板（"hardened blueprint"）
- 覆盖：Capability drops（Linux capability 剥离）、进程资源限制、文件系统只读挂载点
- 适用于多 Agent 批量部署场景

### 3.5 Lifecycle Management（生命周期管理）

- **Single CLI** 管理所有操作：安装、配置、启动、监控、销毁
- 支持 sandbox 模板化（同一 blueprint 批量起多个 Agent 实例）
- 日志汇集：所有 Agent 输出汇总到 CLI

---

## 4. 技术架构

```
┌──────────────────────────────────────────────────────┐
│                  NemoClaw CLI                        │  ← 统一管理入口
│   nemoctl create / start / stop / logs / policy      │
└──────────┬───────────────────────┬───────────────────┘
           │                       │
┌──────────▼──────────┐  ┌─────────▼──────────────────┐
│   NVIDIA OpenShell  │  │      Blueprint             │
│   Sandbox Runtime   │  │  (Hardened Config Template)│
│  - 进程隔离         │  │  - Capability drops        │
│  - 网络过滤         │  │  - 进程资源限制            │
│  - 推理代理         │  │  - 文件系统策略            │
└──────────┬──────────┘  └────────────────────────────┘
           │
    ┌──────▼──────┐
    │   AI Agent  │  ← OpenClaw / Hermes / LangChain Agent
    │  (Sandboxed)│
    └──────┬──────┘
           │ 推理请求
    ┌──────▼──────────┐
    │  Routed         │  ← 本地推理 / 云端 API（NIM / OpenAI / Anthropic）
    │  Inference      │
    └─────────────────┘
```

### 栈关系

| 层 | 项目 | 说明 |
|---|---|---|
| **Agent** | OpenClaw / Hermes / LangChain Agent | 被托管的 AI Agent |
| **安全加固层** | **NemoClaw** | Blueprint + 生命周期管理 |
| **沙箱运行时** | **OpenShell** | 进程隔离 + 网络过滤 + 推理代理 |
| **推理层** | Nemotron / NIM / 第三方 API | LLM 推理后端 |

> **关键洞察**：NemoClaw ≈ OpenShell（沙箱）+ Blueprint（加固模板）+ CLI（管理面）。Nemotron 是 NVIDIA 推理引擎，NemoClaw 将其作为可选推理后端集成，而非独立项目。

---

## 5. 与 OpenClaw 的关系和区别

### 5.1 定位对比

| 维度 | OpenClaw | NemoClaw |
|---|---|---|
| **定位** | 通用 AI Agent 工作台 | Agent 安全运行框架 |
| **范围** | Agent 本身（skills / memory / tools） | Agent 的**安全沙箱 + 管理面** |
| **关系** | 被托管的 Agent | 托管 OpenClaw 的平台 |
| **目标用户** | 开发者 / 个人用户 | 企业 / IT 管理员 |
| **安全隔离** | ❌ 无（直接跑在 host） | ✅ 有（OpenShell 沙箱） |
| **网络控制** | ❌ 无限制 | ✅ 默认阻断，可配白名单 |
| **凭证保护** | ❌ 明文存储在 `~/.openclaw/` | ✅ 沙箱内加密隔离 |
| **部署复杂度** | 低（一键安装） | 中（需配置 blueprint + policy） |

### 5.2 互补关系

```
OpenClaw（能力） + NemoClaw（安全） = 安全增强的 OpenClaw
```

- **OpenClaw 负责"能做什么"**（skills / tool-use / memory）
- **NemoClaw 负责"能接触什么"**（网络 / 文件 / 凭证）

### 5.3 版本与项目状态

| 维度 | OpenClaw | NemoClaw |
|---|---|---|
| **版本** | v2026.x（活跃开发） | 0.0.58（Alpha） |
| **成熟度** | 成熟（生产可用） | 早期（Alpha，生产谨慎） |
| **NVIDIA 关系** | 独立开源项目，NVIDIA 集成 | **NVIDIA 官方项目** |

---

## 6. 与德勤方案的匹配度分析

### 6.1 德勤 NemoClaw 业务材料核心要素

根据已有信息，德勤文档提到以下关键能力：
- **咨询智能体平台**：基于 NemoClaw 构建企业级 Agent 平台
- **安全沙箱**：OpenShell 提供的进程级隔离
- **Physical AI**：与 NVIDIA Isaac Sim 等物理仿真平台联动
- **Blueprint**：标准化部署模板
- **NVIDIA 生态**：与 NeMo / TensorRT / Triton 集成

### 6.2 匹配度评分

| 德勤方案要素 | NemoClaw 支持情况 | 匹配度 |
|---|---|---|
| 安全沙箱 / 隔离执行 | ✅ OpenShell 进程级隔离 + 网络过滤 | ⭐⭐⭐ 高 |
| Blueprint 标准化部署 | ✅ 内置 hardened blueprint + CLI 批量管理 | ⭐⭐⭐ 高 |
| 多 Agent 支持 | ✅ OpenClaw / Hermes / LangChain Agent | ⭐⭐⭐ 高 |
| NVIDIA 生态集成 | ✅ NeMo / TensorRT / Triton / Isaac Sim | ⭐⭐⭐ 高 |
| Tool-use Capabilities | ✅ 继承 Agent 自身 tool-use，OpenShell 保护 tool 执行环境 | ⭐⭐ 高 |
| Physical AI 联动 | ⚠️ 需额外集成（Isaac Sim / Omniverse），NemoClaw 本身不含物理仿真 | ⭐⭐ 中 |
| 企业级凭证管理 | ✅ 沙箱内隔离（但有已知风险，需加固配置） | ⭐⭐ 中 |
| 运营监控 / 日志 | ✅ CLI 日志汇集 | ⭐⭐ 中 |

### 6.3 关键结论

> **NemoClaw 是 NVIDIA 官方的开源安全 Agent 框架，德勤的 NemoClaw 业务方案是基于 NVIDIA 开源版做的咨询二次包装。**  
> 德勤材料中的"咨询智能体平台"可以直接基于 NemoClaw 开源版构建，无需从零开发。Physical AI 部分需叠加 Isaac Sim / Omniverse，NemoClaw 本身不包含物理引擎。

---

## 7. 部署评估

### 7.1 优势

| 优势 | 说明 |
|---|---|
| **NVIDIA 官方背书** | 大厂维护，生态联动确定性强 |
| **零代码改造** | 现有 OpenClaw Agent 无需修改即可入沙箱 |
| **单 CLI 管理** | 安装、配置、运维一条命令 |
| **Apache 2.0** | 完全开源，无供应商锁定 |
| **网络策略灵活** | 从"完全阻断"到"白名单"可配 |
| **多 Agent 支持** | 同时托管 OpenClaw / Hermes / LangChain Agent |

### 7.2 风险与限制

| 风险 | 说明 |
|---|---|
| **Alpha 状态** | 无保证响应 SLA，生产环境需评估风险 |
| **默认配置有漏洞** | Lasso Security 发现默认配置下 Agent 可访问 host 凭证文件（`~/.openclaw/openclaw.json`），需手动加固 |
| **文档尚不完整** | 官方文档部分页面 404，生态页面（如 Isaac Sim 集成）细节缺失 |
| **NVIDIA 强绑定** | OpenShell / NemoClaw 与 NVIDIA 生态深度耦合，非 NVIDIA 环境下可能有限制 |
| **Physical AI 需额外工作** | NemoClaw 本身不包含物理仿真，联动 Isaac Sim 需自行集成 |

### 7.3 部署路径建议

```
实验环境（单 Agent）：
  OpenClaw → NemoClaw → OpenShell
  → 验证安全策略有效性

预生产（多 Agent）：
  Blueprint 批量配置
  → 自定义 Network Policy
  → 收紧文件访问权限

生产：
  → 修复默认凭证暴露问题（Lasso Security 建议）
  → 企业 LDAP / SSO 集成（需调研）
  → 与 Isaac Sim 联动（如需 Physical AI）
```

---

## 8. 使用建议

### 8.1 何时用 NemoClaw（替代纯 OpenClaw）

| 场景 | 推荐 |
|---|---|
| 企业 IT 要求 Agent 网络隔离 | ✅ NemoClaw |
| 多 Agent 批量部署 + 统一管理 | ✅ NemoClaw |
| 合规要求：推理流量必须经过审计代理 | ✅ NemoClaw |
| 个人开发 / 实验 / 快速原型 | ❌ 纯 OpenClaw（轻量） |
| 需要物理仿真（Isaac Sim / Omniverse） | ⚠️ NemoClaw + 额外集成 |

### 8.2 德勤方案建议

1. **直接基于 NemoClaw 开源版**：德勤无需自研安全沙箱，直接用 NVIDIA OpenShell 作为基座
2. **Blueprint 定制**：在 NemoClaw 内置 blueprint 基础上，根据客户行业定制（金融/医疗/制造）
3. **Physical AI 增值**：在 NemoClaw + OpenShell 之上叠加 Isaac Sim 集成层，作为"德勤 Physical AI Blueprint"
4. **安全加固优先**：部署时必须修复 Lasso Security 发现的凭证暴露问题，并将加固步骤纳入交付标准

---

## 9. Quick Reference

| 项目 | 信息 |
|---|---|
| **GitHub** | https://github.com/NVIDIA/NemoClaw |
| **官方文档** | https://docs.nvidia.com/nemoclaw/latest/ |
| **License** | Apache 2.0 |
| **当前版本** | 0.0.58 |
| **项目状态** | Alpha |
| **CLI 工具** | `nemoctl`（NemoClaw 管理）· `openshell`（OpenShell 沙箱） |
| **支持 Agents** | OpenClaw（默认）· Hermes · LangChain Deep Agents Code |
| **核心组件** | OpenShell（沙箱）+ Blueprint（加固模板）+ Routed Inference（推理路由） |
| **社区** | GitHub Discussions · Discord · GitHub Issues |

---

## 10. 参考来源

| 来源 | 链接 | 备注 |
|---|---|---|
| GitHub 主仓库 | https://github.com/NVIDIA/NemoClaw | 官方 README + 架构文档 |
| 官方文档 | https://docs.nvidia.com/nemoclaw/latest/ | 部分页面尚不完整 |
| SiliconANGLE | https://siliconangle.com/2026/03/16/nvidia-launches-nemoclaw-agent-toolkit-enhance-ai-agents | 2026 年 3 月发布报道 |
| Lasso Security | https://www.lasso.security/blog/sandboxed-ai-agents-attack-surface | 安全研究：默认配置凭证暴露风险 |
| Lightning AI | https://lightning.ai/blog/nvidia-openshell-nemoclaw | OpenShell 技术分析 |
| ThoughtMinds | https://thoughtminds.ai/blog/openclaw-vs-nemoclaw | OpenClaw vs NemoClaw 对比 |

---

**研究完成。** 本文档已存档到 vault：`/root/vault/Research/2026-06-28 - NemoClaw (NVIDIA) - GitHub Deep Research.md`