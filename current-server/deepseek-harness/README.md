---
type: deployment-research
project: deepseek-harness
date: 2026-08-14
status: research-only-no-deploy
trigger: InfoQ 公众号文章 https://mp.weixin.qq.com/s/hHCpyIlDiBHSzA3TzO5LmQ
source: https://github.com/deepseek-ai/deepseek-harness
tags: [deepseek, harness, ai-agent, research, 2026-08-14]
---

# DeepSeek Harness — 调研报告（不部署）

> **结论**：**不部署**。27 小时新发布的 monorepo 框架（65k stars / 117MB），官方支持 `npx @deepseek-ai/dsh web` 一行起 Web UI，但服务器部署价值低：
> ① 它是给 Claude Code / Codex 用的 **Harness 框架**，不是 web app
> ② 没有 Dockerfile / docker-compose
> ③ 0 个正式 release，只有 `0.1.0-rc.5` pre-release
> ④ 何大人 60 分钟沉默 → SOP §C 默认不部署

## 一句话定位

**DeepSeek Harness = "一切皆插件" 的 Agent 运行时底座**。模型、工具、技能、会话、沙箱、存储、Agent Loop、调度、UI 全部由 Cordis 插件系统组装。可替换范围从"某个搜索工具"延伸到"Agent 如何循环 / 调度子 Agent / 保存会话 / 用什么 UI"。

## 速查表

| 项 | 值 |
|---|---|
| 仓库 | https://github.com/deepseek-ai/deepseek-harness |
| 发布时间 | 2026-08-13 11:56:32Z（**距今 27 小时**） |
| License | MIT |
| Stars / Forks | **65,030 / 5,458** |
| 体量 | 117 MB / 52 顶层目录 / pnpm-lock 680KB |
| 主语言 | TypeScript + Python |
| 默认分支 | `master` |
| Release | **0 个正式 release**（仅 tag: `0.1.0-rc.5`） |
| Dockerfile / docker-compose | **❌ 都没有** |
| 公开入口 | `npx @deepseek-ai/dsh web`（README 唯一推荐路径） |
| 内嵌 AI 配置 | `.agents/` + `.claude/` + `AGENTS.md` + `CLAUDE.md` —— **目标就是被 Claude Code / Codex 加载** |

## 架构亮点（从文章 + 仓库结构）

1. **Cordis 元框架**：所有能力（Agent Loop、模型、工具、沙箱、UI）都是插件，可卸载/替换
2. **4 种运行模式**（同底座 + 不同插件组合）：
   - **标准模式**：完整工具组合
   - **PTC（Programmatic Tool Calling）**：模型生成代码组合多轮工具调用
   - **极简模式**：只留 shell + 文件编辑（最小环境测模型能力）
   - **创造模式**：Agent 自检运行时，在内存试装 Cordis 插件
3. **工具调用流水线**：Hook → 审批 → 权限 → 沙箱 → 超时 → 结果改写 → 记录 → UI 渲染（普通 / 程序化工具共享安全机制）
4. **多 Agent**：层级式 Supervisor-Worker 为主（父拆/分配/汇总），兼容并行、流水线、Ralph Loop；可把 Claude Code / Codex 接到子 Agent 接口
5. **append-only 事件流**：系统提示词 / 推理 / 工具调用 / 子 Agent 调度 / 上下文注入 → 同一份日志，Trajectory 视图可按来源检查

## 风险矩阵

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

## 三条方案

### A. 直接 `npx @deepseek-ai/dsh web`（官方支持，最稳）
- 5 分钟 / 4G RAM
- 不需要 Dockerfile（官方用 npm 包分发）
- 风险：npm registry 国内限速 + 这是开发预览版接口会变
- **不推荐原因**：跟 "部署一个能跑的应用" 不一样，它跑起来是个 **Claude Code / Codex 的 harness 后端**，对笔记本用户价值有限

### B. 全量 monorepo 构建部署
- 30-60 分钟 / 4-6G RAM
- 需自写 Dockerfile + docker-compose，**第一次失败概率 60%+**（vendor/ 必踩坑）
- 0.1.0 项目踩坑先例：OpenOPC 8/11 那次 0.1.0 也是 issue #38 + WS 不响应连踩
- **不推荐原因**：投入产出比极低

### C. 只调研不部署 ← **本次采用**
- 0 资源 / 1 分钟
- 写本文档归档
- 不动服务器现有 30+ 容器
- 等 2-3 个月 release 成熟 / 官方出 docker 镜像 / 用户明确需求时再启动 B

## 不部署的理由（结论）

1. **不是 web app**：是 Agent 框架 / 平台，对应 LangChain / LlamaIndex / Claude Agent SDK 的位置，不是产品
2. **官方还未提供生产部署方案**：0 个正式 release，没有官方 docker image
3. **风险矩阵指向 C**：按 SOP §6 fresh OSS 决策表（<14d + 无 Dockerfile → 默认 C）
4. **沉默处理**：本次会话已列方案矩阵，何大人 60 分钟无回复 → 按 SOP §C 默认走 C

## 想真要用怎么办（保留给未来）

如未来真要体验：
1. **最快**：在自己 Mac 上 `npx @deepseek-ai/dsh web`，不开服务器（这是给开发者本地用的）
2. **服务器部署**：等 DeepSeek 出官方 docker image（或自己做 GH Action 构建）+ 等 1.x 稳定 release
3. **替代品**：要看类似架构可直接用 LangChain / LlamaIndex / Anthropic Claude Agent SDK —— 已成熟

## 关联文档

- 文章原文 HTML 副本：`/tmp/wx_deepseek-harness-infoq.html`（3.2MB，vault 没存，文章已归档到公众号文章目录）
- 文章归档：`/root/vault/2-Areas/公众号文章/2026-08-14 - InfoQ-DeepSeek把Harness开源了：模型、工具、AgentLoop全是插件.md`
- SOP 来源：`/root/.hermes/skills/third-party-deployment-sop/`（2026-08-14 何大人新增）
- 类似不部署案例：
  - `ego-lite`（2026-08-08）— macOS 桌面应用，公众号文章归档
  - `cx-coze`（2026-08-04）— 内部依赖过重，方案 A 失败 → 调研报告