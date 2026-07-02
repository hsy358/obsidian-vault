---
title: 又一个神级 skill 夯爆了
author: 开源日记
publish_date: 2026-07-02 15:10:25
saved_date: 2026-07-02
source: wechat
url: https://mp.weixin.qq.com/s/mfC7NwTsmmthfKzdarnTaQ
type: 公众号文章
tags:
  - AI
  - Agent
  - Skill
  - CAD
  - text-to-cad
  - Build123d
  - URDF
  - ROS
  - 3D-Printing
  - MCP
  - 垂直行业
  - 工业设计
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: openclaw-2026-07-02
related:
  - /root/vault/1-Projects/德勤/AI-Native/笔记/2026-07-01 - 第一阶段开源研究清单 v3.md
  - /root/vault/2-Areas/公众号文章/2026-07-02 - AIGC开源推荐-第一个真正的Agent RuntimeOS.md
---

# 又一个神级 skill 夯爆了

> **公众号**：开源日记
> **发布日期**：2026-07-02 15:10
> **项目**：**text-to-cad** — github.com/earthtojake/text-to-cad
> **Stars**：7400+
> **协议**：MIT

---

## 摘要

text-to-cad 是**面向 Agent 的 CAD 技能库**，让 AI 用自然语言生成**可编辑的 CAD 源代码**，并导出 STEP / URDF / DXF / G-code 等工程文件。

---

## 核心能力

| 能力 | 说明 |
|---|---|
| **参数化 CAD 源码** | AI 写 Build123d Python 代码，每个几何特征用 `@cad[feature_name]` 标记 |
| **可编辑性** | 改一个孔只需要改源代码参数，不用重画整零件 |
| **STEP 导出** | 直接导入 SolidWorks / Fusion 360 继续编辑 |
| **URDF 自动生成** | 机器人描述文件（links / joints / 坐标系）自动写入 XML |
| **标准件库** | step.parts catalog 真实可购买的螺丝/轴承/电机 |
| **本地浏览器预览** | WebGL 渲染器，支持 STEP/STL/URDF，**手机上就能看 3D 模型** |
| **DXF 工程图** | 3D 投影生成 2D 工程图，激光切割/钣金用 |
| **G-code 切片** | Bambu Labs 3D 打印机 / SendCutSend 钣金加工对接 |

---

## 安装方式

```bash
# Skills CLI 安装
npx skills install earthtojake/text-to-cad

# Claude Code 插件
claude plugin marketplace add earthtojake/text-to-cad
claude plugin install cad@text-to-cad

# Python CAD 环境
python3.11 -m venv .venv
. .venv/bin/activate
pip install -r requirements-cad.txt

# Viewer 前端
npm --prefix viewer install
npm --prefix viewer run dev
# 打开 http://localhost:4178
```

---

## 演示场景（原文摘录）

> 用户输入："生成一个矩形底座，有四个安装孔和两个电机支架"
> 
> 1. AI 写 Build123d Python 源码（孔位 / 支架大小 / 底座厚度）
> 2. 自动导出 STEP（导入 SolidWorks 可编辑）
> 3. 生成 URDF 机器人描述（ROS MoveIt2 可直接加载）

**整个过程用户只说一句话**。

---

## 局限性（原文诚实说明）

- ⚠️ Implicit CAD 试验性，不完善
- ⚠️ Viewer 需要 Node 环境（Python 用户门槛）
- ⚠️ Git LFS 资产默认不拉取（需手动 `git lfs pull`）
- ⚠️ **没有中文文档**（README / SKILL.md 都是英文）
- ⚠️ 复杂装配体未验证（只做单零件 benchmark）
- ⚠️ OpenCascade / step.parts 商业许可证要自查

---

## 与德勤 v0.3 的关联

### 1. 跟 AgentSpace / Hermes 思路一致

| AgentSpace 概念 | text-to-cad 对应 |
|---|---|
| Agent | Claude Code / Codex |
| Skill | `text-to-cad` 这个 skill 包 |
| Knowledge | step.parts catalog（标准件库）|
| Plugin | `claude plugin install cad@text-to-cad` |

**text-to-cad 是"Agent + 垂直行业技能"的成功案例**——证明 Agent 框架加上行业 skill 库就能开箱即用。

### 2. 借鉴价值

| v0.3 模块 | 借鉴方向 |
|---|---|
| **R1 数据模型** | `@cad[feature_name]` 标记体系是**参数化数据模型**的范例 |
| **R3 执行器抽象** | 体现"Agent + 工程软件技能"模式（AgentRouter 可以把"CAD 技能调用"当一个 harness）|
| **R5 KB** | step.parts catalog 是**结构化领域知识库**（螺丝/轴承/电机）+ 版本管理 |
| **R7 安全审批** | 标准件库避免"AI 幻觉造出买不到的螺丝"——**业务可执行性兜底** |

### 3. 调研建议

- **优先级**：P2（暂缓）
- **理由**：
  - 垂直行业（CAD/机器人），德勤项目主要在企业 SaaS 决策类
  - 但 "Agent + 行业 skill" 模式可借鉴到德勤**行业垂直 skill 库**设计
- **横向对比**：
  - 跟 [AIGC开源推荐 - ECC](/2-Areas/公众号文章/2026-07-02%20-%20AIGC开源推荐-第一个真正的Agent%20RuntimeOS.md) 一起看（都是 Agent 工具生态）
  - 跟 ECC 的 Skills/Memory/Hooks 概念高度同构

### 4. 实际可玩性

如果何大人有 CAD / 机器人项目需求，这个 skill **能直接装上 Claude Code 用**——不需要自己写代码就能生成 STEP 文件。我可以帮你装一个试试。

---

## 一句话总结

> "**text-to-cad** = AI 直接生成可编辑 CAD 源码 + 工程文件导出，**'自然语言 → CAD → 机器人 → 制造'** 链路打通的样板。"

---

**作者**：小助（OpenClaw · MiniMax-M3）— 2026-07-02 存档  
**判断**：⭐⭐⭐ **可玩性高**（如果何大人有相关项目），**借鉴价值中**（"Agent + 行业 skill"模式可学）。建议作为 P2 调研对象，**实际试用价值大于研究价值**。