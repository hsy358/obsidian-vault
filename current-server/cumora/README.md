# Cumora

> yetone/cumora — 跨平台（Electron/PWA/iOS/Android）AI Agent 团队聊天客户端，BYOA 自托管

## 📌 部署状态

- ✅ **2026-08-20 部署完成**（公网可访问 `http://101.33.212.119/cumora/`）
- 📄 部署报告：[`部署报告.md`](./部署报告.md)

## 🚀 快速访问

- **笔记本浏览器**：`http://101.33.212.119/cumora/`
- **本地直连**：SPA `http://127.0.0.1:5182/` · API `http://127.0.0.1:5181/`

## 📚 文档

- [`部署报告.md`](./部署报告.md) — 2026-08-20 部署全过程 + 5 个坑的解法
- [`架构说明`](https://github.com/yetone/cumora#architecture) — 官方架构图（BYOA / Cloud 双 brain）
- [`BYOA 文档`](https://github.com/yetone/cumora/blob/main/docs/BYOA.md) — 官方 BYOA 接入指南

## 🔧 常用操作

```bash
# 状态
pm2 list | grep cumora

# 重启
pm2 restart cumora-server cumora-web

# 升级代码
cd /data/cumora && git pull && npm install && ./node_modules/.bin/vite build && pm2 restart cumora-web

# 日志
pm2 logs cumora-server --lines 100
pm2 logs cumora-web --lines 50
```

## 🧠 BYOA 模式（本机 Claude Code / Codex 当 brain）

Cumora 的亮点是 BYOA（Bring Your Own Agent）—— 跑 `npx cumora agent computer`，把本机的 Claude Code / Codex 当作 agent 的 brain，**server 不见你的 provider key**。

```bash
# 笔记本运行
npx cumora@latest agent computer --pair <code> --server http://101.33.212.119:5181
```

`--pair <code>` 从 Cumora Web UI 的 "Add Computer" 流程拿。

## ⚙️ 当前配置

- **模式**：BYOA 自托管
- **OpenAI key**：占位（server triage 不会真调 OpenAI，但 wake 不被 gate 拦截）
- **数据库**：postgres `cumora` 库 + root/root
- **Redis**：本地 6379
- **反代**：nginx `/cumora/*` → 5182，`/cumora-api/*` → 5181

## 📁 文件

| 项 | 路径 |
|---|---|
| 源码 | `/data/cumora/` |
| .env | `/data/cumora/.env` |
| nginx 块 | `/etc/nginx/sites-enabled/default`（在 `/python/` 之前） |

## 🔗 相关项目（同类部署）

- `../deepseek-harness/` — 8/15 同款 pm2 + nginx 部署（子域名方案）
- `../openclaw/` — OpenClaw gateway
- `../guyu/` — Guyu 内网改造