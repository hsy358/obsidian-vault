---
type: document-metadata
file_type: doc
file_path: 2026-07-14_doc_AI Native人机协作与多Agent平台开源选型方案.docx
source: user-upload
uploaded_date: 2026-07-14
original_date: 2026-07-14
title: "AI Native 人机协作与多 Agent 平台开源选型方案"
description: |
  V1.0 内部选型讨论稿，核心推荐：以 AgentSpace 为 Agent Control Plane，以
  CopilotKit/AG-UI 重构人机协作层，吸收 AgentTeams 的透明多 Agent 协作机制，
  以 Pi/Codex/Claude Code 等作为可插拔执行器，配套独立知识平台。
  文档给出三种组合方案（A 推荐方案 / B Tailchat 方案 / C Mattermost 方案）的
  加权评分（4.60 / 3.55 / 3.40）、分阶段建设路线（Phase 0-3）、关键风险与
  治理要求。
size_bytes: 477489
page_count: 10
sha256: 9e7bae999777b80e3eb5dd9f05c2abe72cd4a6fb98091b9bd23fde3b6e52bdb2
author: "AI Native System 项目组"
application: "Microsoft Macintosh Word"
tags:
  - ai-native
  - agent-platform
  - open-source-selection
  - agentspace
  - agentteams
  - copilotkit
  - ag-ui
  - pi
  - tailchat
  - openim
  - mattermost
  - opentag
  - hermes
  - openclaw
  - codex
  - claude-code
  - control-plane
  - human-agent-collab
  - multi-agent
  - collaboration-ux
  - knowledge-plane
  - licensing
  - apache-2.0
  - mit
  - agpl
  - architecture-decision
  - deloitte
  - 1-projects
  - 1-projects/deloitte/ai-native
language: zh-CN
related_entities:
  - project: "AI Native System"
  - parent_project: "德勤 / AI-Native"
  - deliverable_type: 选型报告
  - decision_level: V1.0 内部讨论稿
  - reference_documents:
      - /root/vault/1-Projects/德勤/AI-Native/agents/
      - /root/vault/1-Projects/德勤/AI-Native/executor/
      - /root/vault/1-Projects/德勤/AI-Native/AgentSpace-部署/
key_facts:
  - "核心建议：AgentSpace 为控制平面 + CopilotKit/AG-UI 协作层 + AgentTeams 协作机制 + Pi/Codex/Claude Code 可插拔执行器 + 独立知识平台"
  - "三种方案加权得分：A 推荐方案 4.60，B Tailchat 方案 3.55，C Mattermost 方案 3.40"
  - "明确四项取舍：不以 Mattermost 商业 Fork 底座、不以 OpenTag 为完整平台、不让 Pi 承担组织治理、聊天记录不等于知识"
  - "提出六个核心边界：身份 / 会话 / 任务 / 执行器 / 知识 / 协议"
  - "Phase 0（2 周）做许可证+技术验证并冻结核心边界；Phase 1（6-8 周）打通最小人机协作闭环"
  - "数据对象建议：Workspace/Tenant、Project/Channel/Topic/Thread、Agent/AgentProfile/Skill/Tool、Task/Subtask、Run/Step/ToolCall、Artifact/KnowledgeProposal、Approval/Policy/Credential/AuditLog"
  - "事件最小集：MESSAGE_CREATED / THREAD_UPDATED / TASK_* / RUN_* / TOOL_CALL_* / APPROVAL_* / ARTIFACT_CREATED / KNOWLEDGE_PROPOSED"
  - "Mattermost 风险点：AGPLv3、商标、社区版 vs 企业版功能边界、深度修改后私有化交付受限"
next_actions:
  - "阅读子 agent 审阅产出（P0/P1/P2 问题、与 Hermes 路线冲突点、待核验事实），沉淀到 1-Projects/德勤/AI-Native/笔记/开源项目调研/2026-07-14 - AI Native 选型方案审阅.md"
  - "将『六个核心边界』映射到现有 AgentSpace 仓库代码（/root/vault/1-Projects/德勤/AI-Native/agents/）的领域对象，确认命名/字段差异"
  - "在 Phase 0 ADR 清单中新增 ADR-005《选型方案 V1.0 收口》，记录三大方案的采纳结论与搁置项"
okf_metadata:
  schema: okf-v0.1-inspired
  sidecar_for: 2026-07-14_doc_AI Native人机协作与多Agent平台开源选型方案.docx
  added_by: small-zhu-after-binary-ingest
  rationale: |
    何大人 2026-07-14 08:31 上传 DOCX；按 vault 二进制文档处理规范
    6-System/standards/2026-06-16 - 二进制文档处理规范（sidecar + 命名 + Inbox 分类）.md
    自动归档到 1-Projects/德勤/AI-Native/报告/，与德勤项目既有 报告/ 目录对齐。
    原文件保留在 vault（重命名按 命名约定 YYYY-MM-DD_类型_标题.扩展名）。
---

# 2026-07-14 - AI Native 人机协作与多 Agent 平台开源选型方案 (V1.0 内部讨论稿)

> 本 sidecar 文件是
> [2026-07-14_doc_AI Native人机协作与多Agent平台开源选型方案.docx](./2026-07-14_doc_AI%20Native人机协作与多Agent平台开源选型方案.docx)
> 的元数据。DOCX 含 145 段、25 表、约 1.3 万字提取量、3 张嵌入媒体；
> 本 sidecar 给出结构化摘要与机读索引，便于 grep / dataview 工具检索。

## 0. 文档速览

| 字段 | 值 |
| --- | --- |
| **标题** | AI Native 人机协作与多 Agent 平台开源选型方案 |
| **副题** | 面向完全自主可控商业版本的架构与产品选型 |
| **版本 / 日期** | V1.0 内部选型讨论稿 / 2026-07-14 |
| **作者** | AI Native System 项目组 |
| **来源** | user-upload（何大人 2026-07-14 08:31 通过微信发送） |
| **大小 / 页数** | 477,489 字节 / 约 10 页（基于 9 个显式分页符） |
| **核心建议** | AgentSpace（控制平面） + CopilotKit/AG-UI（协作层） + AgentTeams（协作机制） + Pi/Codex/Claude Code（可插拔执行器） + 独立知识平台 |
| **三种方案加权** | A 推荐 4.60 / B Tailchat 3.55 / C Mattermost 3.40 |
| **目标方向** | 闭源商业产品 + 私有化交付 + Agent 原生 |

## 1. 方案摘要（人读版，约 350 字）

文档首先指出当前最核心的矛盾：AgentSpace 已经有较完整的 Agent 管理、任务、审批、
调度和执行路由（AgentRouter），但在『人↔Agent』『Agent↔Agent』的持续沟通、
透明协作和富交互上不够成熟；而 Mattermost/Tailchat/OpenIM 这类通信项目又缺少
完整的 Agent 控制平面。所以结论是不找“单一开源替代品”，而用**分层组合**：

- **控制平面**：Fork AgentSpace 稳定版本，冻结核心领域模型，上游能力评估后选择性合并。
- **协作层**：自建 Agent Native Collaboration Workspace，前端用 CopilotKit 作加速器，
  对外协议走 AG-UI，对内用自有的领域事件 + 版本化 Schema。
- **协作机制**：从 AgentTeams（HiClaw）吸收“房间式任务组 + Manager/Leader/Worker
  组织拓扑 + 通信 ACL + 共享凭证”，不引入 Matrix 依赖。
- **执行器**：Pi / OpenClaw / Codex / Claude Code 等通过统一 Runtime Adapter 接入，
  Pi 必须放在 Sandbox 中、由 Control Plane 下发最小权限。
- **知识平台**：独立建设 Knowledge Plane，聊天记录只能作为『候选知识』，
  经审核/版本化/ACL 后才入正式知识库。

文档给出 A/B/C 三方案加权评分（A=4.60 / B=3.55 / C=3.40）、四阶段路线
（Phase 0 验证→ Phase 1 最小闭环→ Phase 2 治理→ Phase 3 规模化）、
P0/P1/P2 风险控制清单，并强调六个核心边界（身份/会话/任务/执行器/知识/协议）
必须稳定。附录列出 8 个候选项目的 License 初判与需补齐的证据清单（固定
Commit / SBOM / 商标 / 漏洞跟踪等）。

## 2. 选型决策表

| 决策项 | 文档建议 | sidecar 备注 |
| --- | --- | --- |
| 核心控制平面 | AgentSpace Fork | 与本地已部署的 `/root/AgentSpace`（端口 1455）一致，2026-07-02 AgentRouter→OpenClaw 链路已通 |
| 人机协作界面 | CopilotKit（MIT）+ 自建 UI | 与 Hermes / OpenClaw 不冲突，AG-UI 作为外部协议层 |
| 交互协议 | AG-UI（外部）+ 自有领域事件（内部） | 内部事件需版本化、可回放、含 trace_id |
| 多 Agent 协作 | 吸收 AgentTeams 机制 | 房间式 Taskforce + 组织拓扑 + ACL，**不**引入 Matrix |
| 执行器 | Pi/OpenClaw/Codex/Claude Code 统一 Adapter | 与 MEMORY.md “产品线决策顺序”一致：Hermes 为主、其他为可插拔 |
| Web IM（一期快速版） | Tailchat | 许可证 Apache 2.0、React/Node 技术栈 |
| 中长期通信底座 | OpenIM | 适合移动端 / 私有化 / 规模化 |
| 知识平台 | 独立 Knowledge Plane | 聊天 ≠ 知识；候选知识须经审核 + 版本化 |

## 3. 六个核心边界

1. **身份边界**：Human/Agent/ServiceAccount 统一身份，Agent 须有所有者/职责/凭证/审计主体。
2. **会话边界**：Project/Channel/Topic/Thread 只承担协作上下文，不直接承担任务执行状态。
3. **任务边界**：Task = 目标 + 验收，Run = 一次执行实例，ToolCall = 运行中动作，Artifact = 可交付物。
4. **执行器边界**：Runtime Adapter 统一处理启动/事件/暂停/恢复/取消/凭证注入/产物回传/资源统计。
5. **知识边界**：聊天/文件/运行结果先为 Candidate Knowledge，经提取/审核/ACL/版本化后入正式 Knowledge Plane。
6. **协议边界**：AG-UI 等外部协议用于生态互通；内部领域事件必须独立、版本化、可回放。

## 4. 协作事件最小集（机器可读 Schema 候选）

```yaml
event_types:
  - MESSAGE_CREATED
  - THREAD_UPDATED
  - TASK_CREATED
  - TASK_ASSIGNED
  - TASK_BLOCKED
  - TASK_COMPLETED
  - RUN_STARTED
  - RUN_PROGRESS
  - RUN_PAUSED
  - RUN_FAILED
  - RUN_COMPLETED
  - TOOL_CALL_STARTED
  - TOOL_CALL_COMPLETED
  - APPROVAL_REQUIRED
  - APPROVAL_RESOLVED
  - ARTIFACT_CREATED
  - KNOWLEDGE_PROPOSED
required_envelope:
  - tenant_id
  - project_id
  - actor
  - trace_id
  - timestamp
  - schema_version
  - permission_context
constraint: "敏感信息不得直接写入事件总线"
```

## 5. 阶段路线

| 阶段 | 时长 | 目标 | 关键产物 |
| --- | --- | --- | --- |
| Phase 0 | 2 周 | 许可证 + 技术验证，冻结核心边界 | Fork 清单 / SBOM / License 矩阵 / 架构 ADR-001~004 / 关键 Adapter Spike |
| Phase 1 | 6-8 周 | 打通最小人机协作闭环 | 项目空间 / Thread / @Agent / 任务卡片 / AG-UI Gateway / Runtime Adapter / 审批 / Artifact |
| Phase 2 | 8-12 周 | 透明多 Agent + 企业治理 | Agent 协作室 / 组织拓扑 / ACL / 多租户 / 审计 / 成本 / 评测 / Sandbox |
| Phase 3 | 持续 | 产品化 + 规模化 | 移动端 / OpenIM / 插件市场 / 国产化 / HA / DR / 升级工具链 |

## 6. 候选项目 License 初判

| 项目 | 初步 License | 商业化建议 |
| --- | --- | --- |
| AgentSpace | Apache 2.0 | 核心 Fork，保留 NOTICE 与第三方清单 |
| AgentTeams / HiClaw | Apache 2.0 | 复用设计与代码，注意依赖许可证 |
| CopilotKit | MIT | 用于自有 UI，保留版权和许可文本 |
| AG-UI | MIT | 协议和 SDK 基础，需核查各语言 SDK 依赖 |
| Pi / Pi Mono | MIT | 可作为 Runtime，需补 Sandbox 与企业治理 |
| Tailchat | Apache 2.0 | 可 Fork，需检查插件依赖与商标 |
| OpenIM | Apache 2.0 | 通信基础设施，需核查 SDK 与客户端依赖 |
| Mattermost Community | AGPLv3 | **不**建议核心 Fork；仅原型 / 内部 / 外部适配 |
| OpenTag | 取决于仓库 + Mattermost 组合 | 交互参考价值高，代码与组合边界需逐项确认 |

## 7. 待补齐的证据（决策前必须收口）

1. 各仓库固定 Commit / Release / License 文件 / 依赖清单
2. 关键依赖的许可证兼容性扫描 + SBOM
3. 各项目最新活跃度 / 维护者结构 / Issue 响应 / 版本节奏
4. 商标 / 云托管 / 企业功能 / 移动端 / 插件市场的额外限制
5. 自建 vs Fork 的三年维护成本 / 升级策略 / 安全响应机制

## 8. 与既有 vault 资产的关联

| 主题 | 关联路径 |
| --- | --- |
| AgentSpace 已部署实例 | `/root/vault/1-Projects/德勤/AI-Native/AgentSpace-部署/` |
| AgentSpace 源码 | `/root/vault/1-Projects/德勤/AI-Native/agents/` |
| 执行器抽象层（LangGraph adapter） | `/root/vault/1-Projects/德勤/AI-Native/executor/adapters/` |
| Hermes 验证 | `/root/vault/1-Projects/德勤/AI-Native/Hermes-*`（详见 2026-06-29 commit dc86987） |
| 协作（collab）模块 | `/root/vault/1-Projects/德勤/AI-Native/collab/` |
| 既有调研笔记 | `/root/vault/1-Projects/德勤/AI-Native/笔记/开源项目调研/` |
| 既有报告 | `/root/vault/1-Projects/德勤/AI-Native/报告/`（10 个历史文件） |

## 9. 原始文件引用

- 原文件：`./2026-07-14_doc_AI%20Native人机协作与多Agent平台开源选型方案.docx`
- SHA-256：`9e7bae999777b80e3eb5dd9f05c2abe72cd4a6fb98091b9bd23fde3b6e52bdb2`
- 关联标准：`/root/vault/6-System/standards/2026-06-16 - 二进制文档处理规范（sidecar + 命名 + Inbox 分类）.md`
- 提取文本（人读）：`/root/.openclaw/workspace/.scratch/2026-07-14-ai-native-selection-extracted.md`
