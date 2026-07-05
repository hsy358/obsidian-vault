---
title: Paperclip 公网测试访问信息
date: 2026-07-05
type: access-info
status: active
purpose: 转发给测试者使用
server: 新服务器（101.33.212.119）
author: 小助（OpenClaw）
---

# 🎫 Paperclip 公网测试访问信息（请转发）

> **用途**：把下面这页直接转发给测试者，复制即用。

---

## 🌐 公网访问地址

```
http://101.33.212.119:3100
```

- ✅ 全球可访问（已绑定 0.0.0.0:3100）
- ⚠️ HTTP（非 HTTPS），浏览器会显示 "不安全"——**测试用 OK，生产请忽略**

---

## 👤 测试账号（已注册，admin 权限）

| 项 | 值 |
|---|---|
| **邮箱** | `hesiyan2008@126.com` |
| **用户名** | `hsypaper` |
| **密码** | （invite 模式注册，**没有密码**——登录用 invite URL 注册过的浏览器会话）|
| **权限** | Owner（公司 `Deloitte` 拥有者）|
| **公司** | `Deloitte`（onboarding 已完成）|
| **登录态有效期** | 7 天（cookie + session）|

> ⚠️ **如果测试者用自己的浏览器**，需要走 invite URL 注册新账号（见下面）。

---

## 📨 新测试者注册（推荐）

把下面链接直接转发给测试者，**点开即可注册并进入**：

```
http://101.33.212.119:3100/invite/pcp_bootstrap_375d3ce425608f1a7a93be01ebba725710fcce04f45e116f
```

**步骤**：
1. 浏览器打开上面链接
2. 看到 Paperclip 注册页面，填邮箱 + 密码（自己设）
3. 点 Sign up
4. 自动登录 + 自动加入 `Deloitte` 公司（普通成员权限）
5. 跳到 dashboard

**有效期**：2026-08-04 过期（30 天）

**限制**：
- 一次性（accept 后失效）
- 注册后是 company member（非 owner）

---

## 🏢 测试者能干啥

进入 dashboard 后：

| 操作 | 可否 |
|---|---|
| 浏览公司信息 | ✅ |
| 看 agent 列表 | ✅（1 个 agent: `AI Native`，status=error 待修）|
| 创建新 agent | ✅ |
| 跑任务（task）| ✅ |
| 修改公司设置 | ❌（owner-only）|
| 邀请其他用户 | ❌（owner-only）|

如果需要 owner 权限或更多功能，用 `hesiyan2008@126.com` 这个 admin 账号登录。

---

## 📋 测试场景建议

**最简测试**（3 分钟）：
1. 打开 `http://101.33.212.119:3100/invite/pcp_bootstrap_375d3ce425608f1a7a93be01ebba725710fcce04f45e116f`
2. 注册 + 登录
3. 看 dashboard 布局
4. 截图反馈

**深度测试**（10 分钟）：
1. 进 Agent 页面
2. 看 `AI Native` agent 的 status=error（**预期内**——adapter 还需配置）
3. 创建新 agent 试一下
4. 派一个简单 task
5. 看 task 执行日志

**压测**（需要时）：
- 用 10+ invite 注册多人
- 多人同时派 task
- 看 session 表是否被锁

---

## ⚠️ 测试注意事项

| 注意事项 | 说明 |
|---|---|
| **不要删 hesiyan2008 账号** | 是 admin + 公司 owner |
| **不要改公司名 `Deloitte`** | 已经设好，是 demo 公司 |
| **不要执行 `delete` 类操作** | DB 没有 audit log，删了不可恢复 |
| **HTTP 非 HTTPS** | 测试 OK；生产必须升级 |
| **数据库 password 是 `paperclip`** | 内网测试用，**别外传** |

---

## 🐛 遇到问题反馈给谁

| 类型 | 联系 |
|---|---|
| 服务挂了 | 微信 / 飞书 → 何四燕 |
| Onboarding 问题 | 同上 |
| 配置咨询 | 同上 |
| 紧急回滚 | 同上 |

> **没有工单系统**，都是直接 IM 找何大人（小助会自动监控 + 通知）。

---

## 📝 我（测试者）注册完应该看到什么

```
✅ 注册成功
✅ 自动登录
✅ 跳到 /onboarding（4 步）
✅ Company 步骤已填好 = Deloitte
✅ Next → Agent 步骤
✅ Next → Task 步骤（可跳过）
✅ Launch → dashboard
✅ 看到 AgentSpace 主界面
```

如果不符合，截图发回。

---

**作者**：小助 — OpenClaw (MiniMax-M3) — 2026-07-05 13:03  
**归档位置**：`/root/vault/current-server/2026-07-05_md_paperclip-测试访问信息.md`