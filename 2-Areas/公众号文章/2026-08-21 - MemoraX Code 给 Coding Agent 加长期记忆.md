---
title: MemoraX Code 给 Coding Agent 加长期记忆（Claude Code / Codex / DSH / OpenCode）
date: 2026-08-21
source: https://mp.weixin.qq.com/s/TSf0O1BONCtUAdMdxoJ2Kg
pub_time: 未抓取到公众号发布时间
type: wechat-article-summary
tags: [公众号, AI-Agent, 长期记忆, MemoraX, Claude Code, Codex, DeepSeek-Harness, OpenCode, MCP, Coding-Agent]
related:
  - /root/vault/2-Areas/公众号文章/2026-08-03 - 腾讯把 Agent 记忆系统开源了，TencentDB Agent Memory 实测.md
  - /root/vault/2-Areas/公众号文章/2026-07-16 - 我为什么改造Multica再它读懂AgentWaker.md
  - /root/vault/2-Areas/公众号文章/2026-06-15 - Agent-MemoryForge 2.0 今天发布.md
  - /root/vault/2-Areas/AI-Agent-研究/
---

# MemoraX Code — Coding Agent 的长期记忆插件

> **一句话**：给 Claude Code / Codex / DeepSeek Harness / OpenCode 装一个"项目记忆外挂"，下次开新会话 / 换 Agent 不用重新讲项目背景。

## 🎯 解决什么痛点

| 场景 | 没有 MemoraX Code | 有 MemoraX Code |
|---|---|---|
| **第二天开新对话** | Agent 又要从头扫描代码、问背景 | 项目经验自动带回 |
| **从 Codex 切到 Claude Code** | 重新交接项目知识、踩过的坑 | 跨 Agent 共享记忆 |
| **长对话压缩后** | 关键约束被一起压掉（"改这模块必须兼容旧 DB"） | 真正影响决策的记忆会被找回 |
| **个人工作习惯** | 每次都要重新说（UV/Python 环境、页面风格、测试顺序） | 偏好自动沿用 |
| **记忆本身** | 黑箱 | **平台可视化查看 / 修改 / 删除** |

## 📦 真实状态（npm + GitHub 实测）

| 项 | 值 | 来源 |
|---|---|---|
| **npm 包** | `@memorax/memorax-code` | registry.npmjs.org |
| **最新版本** | `0.1.5`（迭代中） | npm dist-tags.latest |
| **License** | MIT ✅ | npm |
| **包大小** | 2 MB（unpacked） | npm |
| **依赖** | 1 个 runtime（`smol-toml`）—— **极简** | npm dependencies |
| **CLI bin** | `memorax-cli` / `memorax-code` / `memorax-code-codex` / `memorax-code-claude` / `memorax-code-backend` | npm |
| **engines** | `node >=24` ⚠️ | npm |
| **GitHub 组织** | `memorax-ai`（real org） | api.github.com |
| **仓库** | github.com/memorax-ai/memorax-code | npm homepage |
| **官网 1** | `platform.memorax.net` 200 ✅ | curl |
| **官网 2** | `code.memorax.net` 200 ✅ | curl |
| **总 stars** | 未抓取 | — |
| **预/后 install 脚本** | `node ./bin/memorax-code-*-preinstall/postinstall.mjs` ⚠️ | npm scripts |

## ⚠️ 必须告诉你的 3 个风险

1. **预安装 / 后安装脚本会跑 Node 代码**（`preinstall` + `postinstall` 都是 `node bin/...mjs`）—— **会写本地配置 / 自动注入**—— 跟 8/8 openclaw gateway 那种 postinstall 自动改 PATH 类似，**装前最好先看脚本干了啥**
2. **`engines: node >=24`** —— 你的服务器 **Node v22.23.1**（8/15 DSH 部署时确认过）—— **不满足**，要么升级 Node，要么用 `nvm install 24 && nvm use 24` 单独给这个工具
3. **要先去 `platform.memorax.net` 拿 API Key** —— 这是个 SaaS 后端，**记忆是上传到他们服务器的**（不是本地纯 local-first），跟"项目经验带走"这种隐私敏感场景需要先评估

## 🚀 安装命令（公众号原文）

```bash
# 1. 去 https://platform.memorax.net 拿 MemoraX Key
# 2. 装包
npm install -g @memorax/memorax-code --foreground-scripts
```

`--foreground-scripts` 标志：让你能看到 preinstall/postinstall 在干啥

## 🤝 跟我现有部署的关系

| 我的服务 | MemoraX Code 是否支持 | 评估 |
|---|---|---|
| **dsh-web**（DeepSeek Harness · pm2 :5180 · 8/15 部署） | ✅ 官方声明支持 | 🟡 **可试用**，但 DSH 是 monorepo 不是单 Agent，安装方式可能不同（需看 README） |
| **cumora-server / cumora-web**（8/20 部署） | ❌ 不在支持列表 | — |
| **Cumora BYOA 本机 Claude Code** | ✅ Claude Code 在支持列表 | 🟢 **可装**（要 Node 24） |
| **vault Obsidian 知识库** | — | 无关 |
| **guyu**（内网 Paic） | ❌ | — |

## 🤔 跟已有同类方案对比

| 方案 | 定位 | 跟 MemoraX Code 对比 |
|---|---|---|
| **CLAUDE.md / MEMORY.md**（Anthropic 自带） | 单 Agent 项目内 | MemoraX Code 是**跨 Agent + 跨会话 + SaaS 记忆** |
| **TencentDB Agent Memory**（8/03 公众号） | 腾讯云 DB 落地的团队记忆 | MemoraX Code 更轻、不依赖云 DB |
| **Agent-MemoryForge 2.0**（6/15 公众号） | 可审计 / 可隔离 / 可检索 | MemoraX Code 定位更窄（专门 Coding Agent） |
| **MyContext**（8/17 公众号 · 千问办公） | 办公场景上下文 | 不在同一赛道 |

## 📋 我的建议（按 SOP）

按"诊断先行 + 第三方部署走 third-party-deployment-sop"原则，**不直接动手**：

1. ✅ **已归档**（本文件）
2. ⏸ **不立刻动手部署** —— 3 个未确认项：
   - **Node 24** 升级 / 隔离方案
   - **postinstall 脚本** 干啥（先看代码再装）
   - **数据隐私** —— 项目记忆上传到 `memorax.net`，敏感项目（guyu）**绝对不能接**
3. 🟢 **可低风险试用的场景**：
   - 您笔记本上的 Claude Code + DSH monorepo（不是 guyu）
   - 自己写的小项目（不是国央企）
4. ⏳ 等您看完本文 + 上面 3 个风险拍板

---

**归档时间**：2026-08-21
**摘要人**：OpenClaw
**PARA 类别**：2-Areas（持续关注领域）