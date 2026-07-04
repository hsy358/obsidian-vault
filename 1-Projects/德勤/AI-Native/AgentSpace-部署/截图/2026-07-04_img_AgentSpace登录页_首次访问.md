---
type: document-metadata
file_type: img
file_path: 2026-07-04_img_AgentSpace登录页_首次访问.jpg
source: wechat-screenshot
uploaded_date: 2026-07-04
title: "AgentSpace 登录页首次访问"
description: "AgentSpace 公网部署（101.35.52.96:1455）登录页截图，何大人在 Chrome 中首次打开，DevTools Network 面板已开，可看到 RSC payload 中密码明文。"
size_bytes: 193463
tags: [AgentSpace, 截图, 登录页, 安全审计, RSC, 德勤MVP]
related_project: 德勤/AI-Native/AgentSpace-部署
status: 安全问题待修复
---

# AgentSpace 登录页首次访问（2026-07-04）

## 截图信息
- **公网 URL**：http://101.35.52.96:1455（HTTP，浏览器标"不安全"）
- **页面标题**：「最后，进入你的工作区。」
- **核心营销文案**：「让你的工作和组织一秒迈入原生 Agent 集群时代」
- **特性卡片**：调度 / 能力 / 协作 / 安全（3+1 排版）
- **登录字段**：工作区邀请码（可选）/ 邮箱 / 密码

## 🔴 安全问题（投产 blocker）

### 1. HTTP 明文传输
- 公网 1455 端口走 HTTP，浏览器地址栏标"不安全"
- 密码在网络中明文传输

### 2. 密码原样提交到 server action
- DevTools Network → Payload 显示 `1_password=hesiyan123` 原样在 RSC payload 里
- 字段命名 `1_email / 1_password / 1_workspaceJoinCode` 是 RSC 序列化痕迹
- 没有哈希、没有加密、没有 HTTPS 包装

### 3. 后续行动
- 上 HTTPS（Let's Encrypt / 自签证书）
- 密码至少 bcrypt 加盐后再传输或服务端处理
- 警惕反射型 XSS / CSRF（字段名带数字前缀）

## 设计/文案观察
- "信用和复用" → "被信任并复用" 更通顺
- 缺 Logo / 品牌标识
- 缺 CTA 主色（登录按钮没强颜色）
- 4 张卡片 3+1 排版下方留白偏大
- 副标题"原生 Agent 集群时代"略生硬
- 缺：忘记密码 / 免费注册 / SSO / TOS / 隐私协议

## DevTools 工程痕迹
- `_rsc=lquux / 1nal5 / wnywt`：React Server Components 多请求重渲染
- 表单字段 `1_xxx`：典型 RSC 客户端组件编号

## 进度节点
- 2026-07-04 22:04 何大人首次访问并截图分享
- 2026-07-02 AgentRouter → OpenClaw 链路已通（exitCode=0）
- 2026-07-02 OpenClaw 子进程 Node 版本修复 SOP 已落地