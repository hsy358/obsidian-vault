---
title: "StaffDeck：企业级数字员工平台（OpenBMB 出品）"
source_url: https://mp.weixin.qq.com/s/_4beksjJU77Ba8cLVoa9Rg
source_account: 一飞开源
og_image: https://mmbiz.qpic.cn/sz_mmbiz_jpg/rvbNscYfLzYJxX4YhwAx3SG5JQkn37v6o5XCfsiauDaWIrUPSsib1oicibqxVT20wiaOibGiatc50wicM4yGUov0EaY4SvnCGvmVJFzhCKwbEMrWCsk/0?wx_fmt=jpeg
github: https://github.com/OpenBMB/StaffDeck
github_stars: 946
official_site: https://staffdeck.openbmb.cn/
license: AGPL-3.0
released: 2026-07-15
captured: 2026-07-24
captured_by: agent
tags: [agent, digital-employee, sop, state-machine, openbmb, modelbest, deployment-evaluation]
related:
  - /root/vault/current-server/开源软件访问清单.md
  - /root/vault/current-server/Dify/README.md
  - /root/vault/current-server/AgentSpace/README.md
---

# StaffDeck：企业级数字员工平台（OpenBMB 出品）

> **来源**：微信公众号「一飞开源」2026-07-15 推文
> **GitHub**：[OpenBMB/StaffDeck](https://github.com/OpenBMB/StaffDeck)（⭐ 946）
> **官方站**：https://staffdeck.openbmb.cn/
> **许可证**：AGPL-3.0（商用严限）
> **开源时间**：2026-07-15（**9 天前才正式开源**，高度新鲜）

---

## 🏷️ 一句话定位

> **"数字员工 = 岗位 + 能力 + 流程 + 记忆 + 反馈"** — 把员工经验沉淀为可执行 Agent，核心差异化是「状态机驱动的 SOP」+「文档结构感知检索」+「数字员工广场」。

联合研发方：**面壁智能 + 东北大学面壁数据智能联合实验室 + 清华 THUNLP + OpenBMB + AI9Stars**

---

## 🛠️ 技术栈（关键）

| 维度 | 技术 |
|---|---|
| Backend | Python 3.11+ / **FastAPI** / 单端口 5173 |
| Frontend | React + TypeScript + Vite（构建后由 FastAPI 统一对外） |
| 部署形态 | 单进程（API + UI + Swagger 同端口） / `--detach` 后台守护 |
| 数据库 | 默认 SQLite（轻量） |
| 模型依赖 | **OpenAI 兼容协议**（→ 我们 `MiniMax-M3` 直接可接） |
| 桌面客户端 | macOS（arm64 .dmg）/ Windows（.exe）/ Linux（.deb） |
| 协议 | HTTP API + **MCP** + 定时任务 |
| 启动 | `scripts/dev_up.sh --detach` / `scripts/dev.py up --detach` |

**资源占用估算**：Python + Node.js 构建后，估计 300-500 MB 内存（中等）。

---

## 🎯 4 个核心亮点（差异化点）

### 1. 数字员工构建与管理
- 工号 / 岗位边界 / 服务风格 / 权限隔离 / 能力档案 / 工作记录
- 普通用户不能编辑广场原件，只能**复制或绑定**到自己员工（权限模型清晰）

### 2. 状态机驱动的流程型技能 ⭐（最大差异化）
- 自然语言 → 结构化 SOP
- **状态机**保证复杂流程执行（vs Dify 的线性 DAG）
- 多流程实时切换 + 上下文保留 + 可视化编辑 + 版本管理 + 分支演化
- **适合**：审批流、合规审查、工单处理等**有明确分支条件**的场景

### 3. 文档结构感知知识检索 ⭐
- 不只检索文档，**先判断信息位于哪一层**（文档/章节/页面/摘要）
- 知识分桶 + 定向检索 + 来源引用 + 检索调试
- **vs RAGFlow**：RAGFlow 偏 chunk + embedding；StaffDeck 偏**结构化索引**

### 4. 自主执行 + 持续迭代闭环
- HTTP API + MCP + 定时任务执行真实业务
- 长期记忆 + 完整 Trace + 真人接管 + 用户反馈 + 反馈分析
- **MCP 支持** → 跟 OpenClaw 生态天然兼容

---

## ⚠️ 与现有部署的冲突分析

### 🔴 端口冲突（直接冲突）

| 默认端口 | StaffDeck 默认 | 现有占用 | 结论 |
|---|---|---|---|
| **5173** | FastAPI 单端口 | **`yuxi-web`（Yuxi 前端）** | **必须改端口** → 建议改 `5180`（5174 已被占：node 进程）|

**绕开方案**：`backend/.env` 或启动参数改 `APP_PORT` 到 `5180`，反代走 80 即可。

### 🟡 功能重叠（中等重叠，约 50-60%）

| 现有 | StaffDeck 对应 | 重叠度 |
|---|---|---|
| **Dify**（LLM Workflow / Agent 编排） | StaffDeck「数字员工 + 技能 + SOP」| **40-50%** — Dify 偏 workflow DAG，StaffDeck 偏 SOP 状态机 |
| **AgentSpace**（多 Agent / Harness 路由） | StaffDeck「多员工 + 广场」| **50-60%** — 都做 Agent 编排 |
| **RAGFlow**（RAG 引擎 / GraphRAG） | StaffDeck「文档结构感知检索」| **30-40%** — RAGFlow 偏检索，StaffDeck 偏应用层 |
| **Paperclip**（Agent 任务调度） | StaffDeck「定时任务 + 持续执行」| **20-30%** |
| **Langfuse**（LLM Tracing） | StaffDeck「完整 Trace + 检索调试」| **20%**（StaffDeck 自带轻量 Trace，Langfuse 更专业）|
| **Hermes Agent** | StaffDeck「数字员工构建」| **40-50%**（理念相近）|

**关键判断**：StaffDeck **不是 Dify 的完全替代品**——它定位"企业数字员工"（岗位 + SOP），Dify 定位"AI 应用编排"。两者可以共存，但心智上要分清楚。

### 🟢 不冲突的部分

- ✅ **数据库隔离**：默认 SQLite，独立数据库
- ✅ **模型 API**：复用现有 `MiniMax-M3`（OpenAI 兼容协议），无需新 key
- ✅ **MCP 兼容**：跟 OpenClaw 生态天然集成
- ✅ **知识库**：可独立建库，跟 RAGFlow 不冲突

---

## 📊 部署可行性评分

| 维度 | 评分 | 说明 |
|---|---|---|
| **项目质量** | ⭐⭐⭐⭐⭐ | OpenBMB（面壁智能）+ 清华 + 东大 联合出品，背景顶级 |
| **技术创新** | ⭐⭐⭐⭐⭐ | 状态机 SOP + 文档结构感知 + 数字员工广场，三个差异化点 |
| **成熟度** | ⭐⭐⭐ | ⚠️ **仅开源 9 天**，bug 未充分暴露，社区反馈少 |
| **商用兼容** | ⭐⭐ | ⚠️ **AGPL-3.0** — 通过网络提供服务必须开源整个项目代码（商用风险高）|
| **与现网兼容** | ⭐⭐⭐⭐ | 端口改 5180 即可，其他无冲突 |
| **资源占用** | ⭐⭐⭐ | 中等（Python + Node + FastAPI）|
| **学习成本** | ⭐⭐⭐ | 概念新（数字员工 / SOP / 状态机），但 OpenAI 兼容模型即接即用 |

**综合**：⭐⭐⭐⭐（4/5）— **值得评估性试装**

---

## 🤔 我的部署建议（请何大人决策）

### 🅰️ 推荐方案：**暂不部署，先观望 2-4 周**

**理由**：
1. ⚠️ **AGPL-3.0** 太严格，商用场景有合规风险（如果要对外提供服务）
2. ⚠️ **才开源 9 天**，社区反馈未沉淀，bug 风险高
3. ⚠️ 跟 Dify + AgentSpace 功能重叠，部署后**会不会用起来是个问号**
4. ✅ 但**值得每隔 2 周重新评估**（看 GitHub Issues、Star 增长、release 频率）

### 🅱️ 备选方案：**试装一个 demo 实例**（如果你强烈想体验）

**步骤**：
1. 端口改 `5180`（避免跟 Yuxi 冲突）
2. 用现有 `MiniMax-M3`（base_url + api_key + model name）
3. 部署到独立目录 `/root/projects/staffdeck`
4. 先用默认 admin/admin 体验 1-2 天
5. **不接入生产数据**（独立 SQLite）
6. 体验后报告 → 决定保留 / 移除

**预计用时**：30-60 分钟（依赖 Python + Node 依赖安装速度）

### 🅲️ 不推荐：**直接替换 Dify / AgentSpace**
- StaffDeck 跟它们不是替代关系（不同心智模型）
- 强替换会破坏现有工作流

---

## ❓ 何大人要决策的关键问题

1. **是否要部署 StaffDeck？**
   - A 暂不部署，观望 2-4 周
   - B 试装一个 demo 实例（端口 5180，独立数据）
   - C 直接替换 Dify / AgentSpace（不推荐）
2. **如果选 B，预算多少时间？**（建议给 1 小时）
3. **AGPL-3.0 商用风险**你能接受吗？
   - 如果未来 StaffDeck 要对外开放服务 → AGPL 必须开源整个后端代码
   - 如果只内部用 → AGPL 影响不大

---

## 📝 我的判断

> **建议选 A（暂不部署）**，但**每隔 2 周查一次 GitHub**（commits / issues / releases），看活跃度再决定。
>
> 如果**试装 demo**，**强烈推荐 B**（30 分钟成本低），看完再决定。
>
> AGPL-3.0 是最大顾虑——如果未来 StaffDeck 对外提供服务，整个项目代码必须开源。这是法律硬约束，不是 bug。

---

**附**：完整 README 已存到 `/root/.openclaw/workspace/inbox/article_img/StaffDeck_README.zh.md`（14 KB）
**作者**：小助 — OpenClaw (MiniMax-M3) — 2026-07-24 14:57
**触发者**：何大人 14:53 "这个你研究下 是否值得部署研究 和现有部署内容是否会冲突 是否会影响现有部署的软件"