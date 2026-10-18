---
title: "T3Code — Agent Harness 控制面"
source: github
url: https://github.com/pingdotgg/t3code
saved_date: 2026-10-02
tags: ["Agent-Platform", "Remote-Control", "Coding-Agent", "T3Code"]
description: "24k stars，远程控制 Claude Code/Codex/Cursor/Grok Build/OpenCode，支持手机/Web/桌面三端"
---

# T3Code — Agent Harness 控制面

**仓库**: [github.com/pingdotgg/t3code](https://github.com/pingdotgg/t3code)
**Star**: 24,111 ⭐
**语言**: TypeScript

## 定位

> "Agent harness control surface" — 用手机/Web/桌面控制本机的各种 Coding Agent

**不是新 Agent**，而是统一控制面板：Claude Code / Codex / Cursor / Grok Build / OpenCode / Google Antigravity 都接入。

## 三大客户端

| 客户端 | 链接 |
|---|---|
| iOS | App Store |
| Android | Google Play |
| Web | app.t3.codes |
| 桌面（Electron） | t3.codes / GitHub Releases |

## 安装

```bash
curl -fsSL https://t3.codes/install.sh | sh
# 或
npx t3@latest   # 免安装试用
```

支持：Windows (winget) / macOS (Homebrew) / Linux (deb/AUR)

## 远程接入方案

### 方案一：T3 Connect（云端中继，最推荐）

无需配置路由器/内网穿透：

1. Host 端：`t3 connect` → 登录 T3 账号 → 启用 T3 Connect
2. 另一设备：登录同一 T3 账号 → 自动发现 Host 端环境
3. SSH 场景：CLI 打印浏览器链接 + 短码，另一设备确认配对

**凭证自动续期**，断线重连后 diff / provider 设置保持不变。

### 方案二：LAN 直连（私有网络）

1. Host 端：`t3 serve --host <private-ip>` 或桌面端 Settings → Connections → 开启 Network access
2. 生成一次性配对链接（QR 码或 URL）
3. 手机/其他桌面扫码或粘贴链接 → 添加环境

## 多设备负载均衡

**Load balancing**（多机器自动分配新线程）：

- Settings → Connections → Load balancing
- 每台机器可设：**Normal** / **Prefer**（CPU+内存充足时优先） / **Less often** / **Manual only**（排除自动分配）
- 当 ≥2 台机器开机时，自动选新线程跑在哪台

> 💡 多机场景：每台机器是独立 "environment"，T3 Connect 把它们串成一个可统一控制的集群。

## 对德勤项目的参考价值

- **多 Agent 统一控制面** → 德勤 MVP 的 Workspace 多 Executor 管控 UI 参考
- **Load balancing 多机调度** → 德勤 AgentRouter 可借鉴：按机器负载分配任务
- **T3 Connect 云端中继** → 德勤企业部署可以考虑类似 relay 架构，避免暴露内网
- **认证 + 配对流程** → Agent 远程接入的鉴权设计参考
