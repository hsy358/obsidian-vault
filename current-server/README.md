---
title: 新服务器隔离空间 (101.33.212.119)
date: 2026-07-05
type: server-isolation
status: active
server: 新服务器 (101.33.212.119)
ip: 101.33.212.119
owner: 何四燕 (hesiyan2008@126.com)
purpose: 物理隔离新服务器独有的 vault 内容，避免与"之前的服务器"(101.35.52.96) 推送的 vault 内容冲突
---

# 🖥️ 新服务器隔离空间（101.33.212.119）

> **本目录专门存放新服务器独有的 vault 内容**——区别于"之前的服务器"已经推送到 GitHub 的内容。

---

## 🎯 为什么需要这个目录

- **之前的服务器**（101.35.52.96）已大量推送 vault 内容到 GitHub（master 分支）
- **新服务器**（101.33.212.119）vault 跟远端**历史分叉**（commit chain 不同），push 时会冲突
- **解决**：把新服务器产出的内容放在 `current-server/` 子目录，物理隔离

---

## 📋 目录约定

| 子目录 | 用途 | 自动 push？ |
|---|---|---|
| `current-server/deployment/` | AgentSpace / Paperclip / Hermes 等部署笔记 | ❌ 手动 |
| `current-server/decisions/` | 服务器关键决策记录 | ❌ 手动 |
| `current-server/incidents/` | 故障 / 修复 / 异常事件 | ❌ 手动 |
| `current-server/knowledge-base/` | 新服务器独有知识沉淀 | ❌ 手动 |
| 根目录其他位置 | 跟老服务器共用的 PARA 笔记 | ❌ 手动（需先解决分叉）|

---

## ⚠️ Push 注意事项

**当前 vault 状态**：
- 本地 master 有 5 个未推送 commit
- 远端 master HEAD: `47cb808f`（"移除 paperclip 笔记中已废弃的老服务器 IP"）
- **两历史分叉** → 直接 push 会被 rejected

**要 push 时的步骤**（手动）：
1. `git fetch origin`（或用 Contents API 拿远端元数据）
2. `git status` 看本 vs 远差距
3. 决定 rebase / merge / reset --hard
4. 解决冲突（如果有）
5. `git push origin master`

**Obsidian Git 配置**：
- `disablePush: true` ← 当前状态，不自动 push
- `autoSaveInterval: 5` ← 每 5 分钟自动 commit（本地留版本）

**手动 push 方式**：
- Obsidian Git 工具栏 → Push 按钮
- 命令行：`cd /root/vault && git push origin master`
- 让我（小助）帮你推

---

## 📊 服务器对照表

| 项目 | 之前的服务器 | 新服务器 |
|---|---|---|
| 公网 IP | ~~101.35.52.96~~（已废弃）| **101.33.212.119** |
| 部署位置 | 未知 | 腾讯云 Ubuntu 24.04 / 2C3.6G |
| vault 状态 | 已推送至 GitHub master | 本地 working tree（未推）|
| 主要服务 | 不详 | AgentSpace / Paperclip / Hermes |
| 当前操作 | 不可达（IP 废弃）| 运行中 |

---

## 🔖 标签约定

新服务器笔记建议加 frontmatter tag：
```yaml
---
server: 101.33.212.119
uploaded: false  # 是否已 push 到 GitHub
date: YYYY-MM-DD
---
```

---

**作者**：小助 — OpenClaw (MiniMax-M3) — 2026-07-05 12:24
