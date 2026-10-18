---
title: "Google AX (Agent Substrate) — Kubernetes 原生 Agent 编排器"
description: 谷歌开源的 Agent 编排框架，把 Agent 任务变成 K8s 有状态负载，YAML 声明式编排，gVisor 沙箱，崩溃快速拉起
source: https://github.com/google/ax
author: Google
uploaded_date: 2026-09-26
tags: [Google, AX, Agent-Substrate, Kubernetes, gVisor, 编排器, 开源]
file_path: /root/vault/2-Areas/AI-Agent-研究/Google-AX-Agent-Substrate/2026-09-26 - Google AX Agent Substrate 谷歌开源Agent编排器.md
---

# Google AX (Agent Substrate) — Kubernetes 原生 Agent 编排器

> GitHub：https://github.com/google/ax
> 官网：https://www.agentexecutor.io
> 许可：Apache 2.0
> 版本：v0.3.0（任务状态已移出 etcd）

## 是什么

Google AX 是开源的 **Agent 编排器和声明式运行时**，将 Agent 任务作为**有状态的 Actor** 在 Kubernetes 上运行，而非传统微服务或批处理任务。

核心思路：**把每个 Agent 任务变成 Kubernetes 上有状态的负载**，自带沙箱和网络隔离，崩溃后能快速拉起。

## 四大核心抽象（YAML 声明式）

| 抽象 | 作用 |
|---|---|
| **Task** | 定义 Agent 任务 |
| **Workspace** | Agent 工作空间 |
| **Gateway** | 网络出入控制 |
| **Model** | 模型配置 |

## 核心技术特性

| 特性 | 说明 |
|---|---|
| **Actor multiplexing** | 把大量稀疏 Agent（Actors）复用到少量密集物理 Worker（Pod 池）上 |
| **Sub-second suspend/resume** | Agent 空闲时（如等待推理或工具调用）checkpoint 执行状态，需要时亚秒级恢复 |
| **gVisor sandboxing** | 每个 Agent Session 运行在隔离的 Actor Sandbox 中，CPU/内存资源边界严格 |
| **Zero-trust networking** | 默认 deny，显式放行 |
| **轻量控制面** | 自带 ateapi 控制面，不走 K8s API Server（避免压垮 etcd） |
| **API budget controls** | API 成本控制 |
| **状态外置** | v0.3.0 已将任务状态移出 etcd |

## 架构定位

```
大量稀疏 Actors（Agent Sessions）
        ↓ multiplexing
少量密集 Workers（K8s Pod Pool）
        ↑
  Kubernetes 基础设施层
```

**关键洞察**：标准 K8s API Server 不是为"每秒数百万次快速调度事件"设计的。Agent Substrate 自带轻量控制面处理 Actor 生命周期和路由，降低延迟，同时利用 K8s 做基础设施编排和 Pod 管理。

## 适用场景

✅ **适合**：
- 已有 K8s 体系
- 需要多 Agent 并发
- 需要统一调度
- 云原生团队

❌ **不适合**：
- 轻量脚本场景（负担过重）

## 与 AI Native Node OS 的关系

| 维度 | AI Native Node OS | Google AX |
|---|---|---|
| **架构** | Control Plane + Worker Node | Actor multiplexing → Worker Pod Pool |
| **隔离** | RuntimeClass（native/gVisor/microVM/GPU） | gVisor sandbox |
| **状态** | Cell ephemeral，状态外置 | Suspend/resume checkpoint |
| **调度** | Scheduler Filter + Score | Actor → Worker multiplexing |
| **网络** | Policy-by-default | Zero-trust |
| **底层** | 自研 Node OS | 基于 K8s |
| **定位** | 更底层，偏向 OS 基础设施 | 更上层，偏向 K8s 上的编排层 |

## 核心相似点

1. **Cell/Sandbox 抽象**：都是隔离执行单元
2. **状态外置**：Cell 可死，状态外置 / Agent 可挂起，状态 checkpoint
3. **Policy-by-default**：网络默认 deny
4. **Declarative**：YAML 声明式对象

## 参考链接

- GitHub：https://github.com/google/ax
- 官网：https://www.agentexecutor.io
- Blog：https://cloud.google.com/blog/products/ai-machine-learning/agent-executor-googles-distributed-agent-runtime
- Solo.io 解析：https://www.solo.io/topics/ai-infrastructure/how-google-agent-substrate-works

---

*存档时间：2026-09-26*
