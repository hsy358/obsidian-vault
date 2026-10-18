# Claude Code Game Studios

- **GitHub**: https://github.com/donchitos/claude-code-game-studios
- **Stars**: 25.9k
- **Forks**: 3.7k
- **License**: MIT
- **归档日期**: 2026-10-09

---

## 核心价值

把一个 AI 编码助手（Claude Code）变成一个完整的游戏开发工作室——不是单兵作战，而是模拟真实工作室的层级架构。

---

## 规模

| 类别 | 数量 |
|---|---|
| AI Agent | 49 个 |
| Skills（斜杠命令） | 74 个 |
| Hooks（自动化钩子） | 12 个 |
| Coding Rules（编码规则） | 13 条 |
| Templates（文档模板） | 39 个 |

---

## 三层架构

### Tier 1 — 总监（3）
- creative-director、technical-director、producer

### Tier 2 — 部门负责人（8）
- game-designer、lead-programmer、art-director、audio-director、narrative-director、qa-lead、release-manager、localization-lead

### Tier 3 — 专家（37+）
- gameplay-programmer、engine-programmer、ai-programmer、network-programmer、tools-programmer、ui-programmer
- systems-designer、level-designer、economy-designer
- technical-artist、sound-designer、writer、world-builder、ux-designer
- prototyper、performance-analyst、devops-engineer、analytics-engineer
- security-engineer、qa-tester、accessibility-specialist
- live-ops-designer、community-manager

---

## 引擎支持

| 引擎 | Lead Agent | 专长 |
|---|---|---|
| Godot 4 | godot-specialist | GDScript、Shaders、GDExtension |
| Unity | unity-specialist | DOTS/ECS、Shaders/VFX、Addressables、UI Toolkit |
| Unreal Engine 5 | unreal-specialist | GAS、Blueprints、Replication、UMG/CommonUI |

---

## 关键设计理念

### 协作协议（每个 Agent 必须遵守）
1. **Ask** — 先问问题，再提方案
2. **Present options** — 给出 2-4 个选项及利弊
3. **You decide** — 用户始终做决定
4. **Draft** — 先展示草稿，再最终定稿
5. **Approve** — 没有用户签字不写入

### 委托模型
- **纵向委托**：总监 → 部门负责人 → 专家
- **横向咨询**：同层可以协作但无权做跨域决策
- **冲突升级**：设计争议找 creative-director，技术争议找 technical-director
- **变更传播**：跨域变更由 producer 协调

### rigor 模式（控制流程重量）
- **minimal**（默认）= jam 速度，不要求 GDD，最轻量 QA
- **standard** = 5 个 GDD 章节，平衡文档深度
- **full** = 全部 8 个 GDD 章节，严格 QA 证据要求

---

## 成本提示（用户评论提到）

Token 消耗较大——每月 200 刀可能不够用。

标准模式下，第一个游戏代码之前需要写 30 份文档，约 58 分钟 Token 消耗。

---

## 关联何大人求职方向

- **德勤 AI Native / Agent 平台**：Claude Code Game Studios 是 Agent 工作流设计的最佳参考范本之一
- 49 Agent 分层协作、Skills 体系、Hooks 自动化、Rules 编码标准——可直接借鉴到德勤 MVP 的 agent 设计里
- **尤其是 Hermes Agent 架构**：可以参考其"导演 → 负责人 → 专家"的三层分级设计
