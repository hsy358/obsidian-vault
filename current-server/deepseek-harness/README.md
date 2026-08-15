---
type: deployment-research
project: deepseek-harness
date: 2026-08-14
status: research-only-no-deploy
trigger: InfoQ 公众号文章 https://mp.weixin.qq.com/s/hHCpyIlDiBHSzA3TzO5LmQ
source: https://github.com/deepseek-ai/deepseek-harness
tags: [deepseek, harness, ai-agent, research, 2026-08-14]
---

# DeepSeek Harness — 调研 + 部署状态

> **⚠️ 状态变更**：**已于 2026-08-15 部署上线**（**与本调研的"不部署"结论相反**）。当时 8/14 是按 SOP §C 沉默默认走的只调研路径；8/15 你要求"动手"后改为方案 A4（npm 包 + pm2）部署。
>
> **详情见**：[`部署报告.md`](./部署报告.md)（7.4 KB，含完整步骤/教训/自验）
>
> 访问入口：`http://dsh.101.33.212.119.nip.io/`（子域名方案）

---

## 历史调研快照（2026-08-14，已过时，仅保留作记录）

> **当时结论**：**不部署**。27 小时新发布的 monorepo 框架（65k stars / 117MB），官方支持 `npx @deepseek-ai/dsh web` 一行起 Web UI，但服务器部署价值低：
> ① 它是给 Claude Code / Codex 用的 **Harness 框架**，不是 web app
> ② 没有 Dockerfile / docker-compose
> ③ 0 个正式 release，只有 `0.1.0-rc.5` pre-release
> ④ 何大人 60 分钟沉默 → SOP §C 默认不部署

### 一句话定位

**DeepSeek Harness = "一切皆插件" 的 Agent 运行时底座**。模型、工具、技能、会话、沙箱、存储、Agent Loop、调度、UI 全部由 Cordis 插件系统组装。

### 速查表（调研快照）

| 项 | 值 |
|---|---|
| 仓库 | https://github.com/deepseek-ai/deepseek-harness |
| 发布时间 | 2026-08-13 11:56:32Z |
| License | MIT |
| Stars / Forks（调研时）| 65,030 / 5,458 |
| 体量 | 117 MB / 52 顶层目录 / pnpm-lock 680KB |
| 主语言 | TypeScript + Python |
| 默认分支 | `master` |
| Release | **0 个正式 release**（仅 tag: `0.1.0-rc.5`，8/15 已升级到 `0.1.0-rc.6`） |
| Dockerfile / docker-compose | **❌ 都没有** |
| 公开入口 | `npx @deepseek-ai/dsh web`（README 唯一推荐路径） |

### 调研时风险矩阵（历史快照）

| 维度 | 评估 | 严重度 |
|---|---|---|
| 发布时间 <14d | 27 小时 | 🔴 |
| 缺 Dockerfile | 顶层没有 | 🔴 |
| 缺 docker-compose | 顶层没有 | 🔴 |
| 缺正式 release | 0 个正式，1 个 RC | 🔴 |
| 大 monorepo | 117MB / pnpm-lock 680KB | 🟡 |
| 多语言栈 | TS + Python 双栈 | 🟡 |
| 需自写 Docker 构建 | 4-6G RAM / 30-60 分钟 | 🟡 |
| npm registry 限速 | ghcr / npm 在国内常抽 | 🟡 |
| 内网依赖 | 0（MIT 公网） | 🟢 |
| License MIT | 公网可改可商用 | 🟢 |

### 调研时的方案矩阵（已被 8/15 部署推翻）

### A. 直接 `npx @deepseek-ai/dsh web`（官方支持，最稳）
- 5 分钟 / 4G RAM
- 不需要 Dockerfile（官方用 npm 包分发）
- 风险：npm registry 国内限速 + 这是开发预览版接口会变
- 调研时未推荐：跟"部署一个能跑的应用"不一样，它跑起来是个 Claude Code / Codex 的 harness 后端，对笔记本用户价值有限
- **8/15 实际采用**：用 npm 包 + pm2 保活，等于 A 路径升级版

### B. 全量 monorepo 构建部署（8/15 试了失败）
- 30-60 分钟 / 4-6G RAM
- 需自写 Dockerfile + docker-compose，**第一次失败概率 60%+**
- **8/15 实际失败**：tsc -b 30+ 文件报 `Property 'X' does not exist on TypertClientRemote` 错误，monorepo 4-stage build 链断在 client 编译
- 验证了调研时的预判（"0.1.0 项目踩坑先例：OpenOPC 8/11 那次 0.1.0 也是 issue #38 + WS 不响应连踩"）

### C. 只调研不部署（调研时采用，8/15 已推翻）

---

## 关联文档

- **部署报告（2026-08-15）**：[`部署报告.md`](./部署报告.md) — 含完整步骤、命令、自验、教训
- 文章原文 HTML 副本：`/tmp/wx_deepseek-harness-infoq.html`
- 文章归档：`/root/vault/2-Areas/公众号文章/2026-08-14 - InfoQ-DeepSeek把Harness开源了：模型、工具、AgentLoop全是插件.md`
- SOP 来源：`/root/.hermes/skills/third-party-deployment-sop/`
- 类似不部署后改部署案例：
  - `ego-lite`（2026-08-08）— macOS 桌面应用，公众号文章归档
  - `cx-coze`（2026-08-04）— 内部依赖过重，方案 A 失败 → 调研报告
  - **本项目**（2026-08-15）— 调研说不动，但用户要求动手后改走 npm 包部署