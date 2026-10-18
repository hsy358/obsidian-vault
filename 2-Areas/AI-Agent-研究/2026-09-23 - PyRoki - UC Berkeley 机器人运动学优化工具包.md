---
type: document-metadata
title: "PyRoki - UC Berkeley 机器人运动学优化工具包"
description: "模块化可扩展的机器人运动学优化工具包，统一逆运动学、轨迹优化、运动重定向"
source: https://github.com/chungmin99/pyroki
uploaded_date: 2026-09-23
tags: [机器人, 运动学, 优化, UC-Berkeley, IROS-2025, JAX, Python]
---

# PyRoki — 机器人运动学优化工具包

**仓库**: https://github.com/chungmin99/pyroki
**主页**: https://pyroki-toolkit.github.io
**论文**: https://arxiv.org/abs/2505.03728
**作者**: Kim*, Yi*, Choi, Ma, Goldberg, Kanazawa — UC Berkeley
**会议**: IROS 2025 (IEEE/RSJ International Conference on Intelligent Robots and Systems)

## 核心定位

模块化、可扩展、跨平台的机器人运动学优化工具包，纯 Python 实现（JAX），支持 CPU/GPU/TPU。

统一问题：逆运动学（IK）、轨迹优化、运动重定向（retargeting），通过**可组合的运动学变量和代价函数**来实现。

## 核心特性

- **可微分前向运动学**: 从 URDF 自动生成
- **自动碰撞体生成**: 胶囊体等图元自动生成
- **可微分碰撞体**: numpy broadcasting 逻辑
- **常见代价函数**: 末端执行器姿态、自碰撞/世界碰撞、可操作性等
- **任意代价**: 支持自动微分或解析雅可比
- **LM 求解器集成**: 基于 [jaxls](https://github.com/brentyi/jaxls)，支持流形优化（lie groups）和硬约束（增广拉格朗日）
- **跨平台**: CPU / GPU / TPU，JAX 实现

## 技术限制

- **静态形状 & JIT 开销**: JAX JIT 在首次运行和输入形状变化时触发；需预填充数组以向量化
- **无采样规划器**: 不含采样类规划器（如 RRT）
- **关节类型**: 仅支持 revolute、continuous、prismatic、fixed
- **碰撞几何**: 仅支持球形、胶囊体、半空间、地形图；网格碰撞用胶囊体近似
- **运动学结构**: 仅支持运动树；不含闭环机构或并联机械臂

## 安装

```bash
git clone https://github.com/chungmin99/pyroki.git
cd pyroki
pip install -e .
```

要求 Python 3.10+。

## 与德勤/AI Agent 项目的关联

- **德勤 MVP**涉及 Agent 执行器抽象层，机器人领域是一个潜在扩展方向
- PyRoki 的**模块化可组合架构**（变量+代价函数）是 Hermes Agent 可借鉴的设计思路
- Goldberg 教授（UC Berkeley）是机器人操作和抓取领域的权威，PyRoki 代表了该领域的最新工程化实践
- 当前 AI Agent 在物理世界执行层面（机器人/具身智能）是一个前沿方向
