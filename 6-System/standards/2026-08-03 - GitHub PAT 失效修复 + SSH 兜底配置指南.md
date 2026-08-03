---
title: "GitHub PAT 失效修复 + SSH 兜底配置指南"
date: 2026-08-03
type: standards/guide
trigger: GitHub fine-grained PAT 401 Bad credentials，无法推送 vault
target_user: 何大人（hesiyan2008）
estimated_time: 10 分钟
status: 待执行
---

# GitHub PAT 失效修复 + SSH 兜底配置指南

> 适用场景：GitHub `push` 报 `Bad credentials (401)`，本地有积压 commits 需要推送。
> 触发日期：2026-08-03（PAT 失效）+ 同时配置 SSH 兜底（防再次失效）。

---

## Part A：重新生成 GitHub Fine-Grained PAT（必需）

### A1. 打开 PAT 生成页面

1. 浏览器访问：**https://github.com/settings/personal-access-tokens/new**
2. 用 hesiyan2008 账号登录（如果还没登录）

### A2. 填写 PAT 配置

| 字段 | 填什么 | 说明 |
|---|---|---|
| **Token name** | `vault-sync-2026-08` | 随便起，便于识别用途 + 日期 |
| **Expiration** | `90 days` 或 `1 year` | 推荐 1 年；最长就 1 年，**不会自动续期** |
| **Description** | （可选）留空或写"vault 自动同步" | |

### A3. 选仓库访问权限（关键！）

**Repository access** 这一段，选：
- ❌ **不要选** "All repositories"（太宽）
- ❌ **不要选** "Public Repositories (read-only)"（只读，推不了）
- ✅ **选第二个** "**Only select repositories**"
  - 点右边的 "Select repositories" 下拉
  - 选 **hsy358/obsidian-vault**（就这一个）

### A4. 勾选权限（关键！）

**Permissions → Repository permissions** 这一段，展开：

| 权限 | 是否勾选 | 说明 |
|---|---|---|
| **Contents** | ✅ **Read and write** | **必需**：用来 push commit |
| Issues | ⬜ | 不需要 |
| Pull requests | ⬜ | 不需要 |
| Actions / Metadata / etc. | ⬜ | 不需要 |

> ⚠️ **只勾 Contents 即可**，不要乱勾其他权限（最小权限原则）。

### A5. 生成 token

1. 滚到页面底部
2. 点绿色按钮 **"Generate token"**
3. ⚠️ **token 只显示一次！立刻复制保存到密码管理器或本地**

### A6. 把 token 发给"小助"

复制后通过微信发给我（小助），格式建议：
```
新 PAT: ghp_xxx... 或 github_pat_xxx...
```

我会做以下事情：
1. 更新 `/root/vault/.git/config` 里的 token URL
2. 更新 `~/.gitconfig` 里的 `[github] token`
3. 推送积压的 4 个 commit：
   - `03b4d5f` auto: 2026-08-03 22:30
   - `7876ff3` auto: 2026-08-03 15:35
   - `e111431` auto: 2026-08-03 14:50
   - `ed481d7` 归档公众号文章: 灵·洞本体工作站开源
4. 推今天新存档的 OKF 文章

---

## Part B：加 SSH 公钥（可选但强烈推荐）

> 目的：未来 PAT 再失效时，可走 SSH 路径推送（不依赖 PAT）。

### B1. 复制 public key

SSH public key 已经在 `/root/.ssh/id_ed25519_vault.pub` 生成好。

完整内容：
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICHnWt9PMj/LmqKRonYa/9E4m6r8LwS3Vo8KdFz9Bdkl hesiyan2008@126.com - vault sync fallback
```

> 这串内容是公开的，可以直接复制粘贴到 GitHub。

### B2. 在 GitHub 加 SSH key

1. 浏览器访问：**https://github.com/settings/keys/new**
2. 用 hesiyan2008 登录

### B3. 填写 SSH key

| 字段 | 填什么 |
|---|---|
| **Title** | `vault-fallback-2026-08` |
| **Key type** | `Authentication Key`（默认就是）|
| **Key** | 粘贴上面那串 `ssh-ed25519 AAAA...` |

### B4. 保存

1. 点绿色按钮 **"Add SSH key"**
2. 可能需要输入 GitHub 密码二次确认

### B5. 通知"小助"

加完后告诉小助。我会做：
1. 把 vault remote URL 从 `https://github.com/hsy358/obsidian-vault.git`
   改成 `git@github.com:hsy358/obsidian-vault.git`
2. 测试 SSH 连接：`ssh -T git@github.com`
3. 看到 `Hi hesiyan2008! You've been successfully authenticated...` = 成功

---

## Part C：故障排查（如果 A+B 都做了还是失败）

### C1. token 还是 401？

- 检查 fine-grained PAT 的 **Repository access** 是否选了 hsy358/obsidian-vault
- 检查 **Contents** 权限是否是 "Read and write"（不是 "Read-only"）
- 如果仓库是 Organization 的，看 Organization 是否启用了 SAML SSO：
  - 走 https://github.com/settings/personal-access-tokens
  - 找到 token，点右边的 "Configure SSO" → "Authorize" 该组织

### C2. SSH 还是 "Permission denied"？

- 本地运行：`ssh -T git@github.com`
- 看到 `git@github.com: Permission denied (publickey).` = key 没加对
- 检查：
  - 复制粘贴时**没多余空格**（特别是首尾）
  - GitHub 上 Title 不要重复（重复会被顶掉）
  - 本地文件 `/root/.ssh/id_ed25519_vault.pub` 是否完整

### C3. 推送还是卡住？

如果 A+B 都通了但 push 还是卡住，多半是 mihomo 代理问题：
- mihomo 服务如果挂了，github.com 直连不通
- 我可以**重启 mihomo 服务**（已在 2026-08-03 修好 binary）
- 或者临时改用 Contents API 兜底推送

---

## 附录：相关文件路径

| 文件 | 用途 |
|---|---|
| `/root/.ssh/id_ed25519_vault` | SSH 私钥（**不要泄露**）|
| `/root/.ssh/id_ed25519_vault.pub` | SSH 公钥（可贴到 GitHub）|
| `/root/.gitconfig` | 全局 git 配置（含旧 token）|
| `/root/vault/.git/config` | vault 仓库配置（含旧 token URL）|
| `/root/.config/mihomo.yaml` | mihomo 配置文件（如果存在）|
| `/root/bin/mihomo` | mihomo binary（2026-08-03 已重解压）|

---

## 验证清单

完成 A 后：
- [ ] 新 token 已生成 + 保存到密码管理器
- [ ] 新 token 已发给小助
- [ ] 4 个积压 commit 已推送
- [ ] GitHub 上看到最新 commit

完成 B 后（可选）：
- [ ] SSH 公钥已加到 GitHub
- [ ] vault remote URL 已改成 SSH 形式
- [ ] `ssh -T git@github.com` 输出 Hi hesiyan2008
- [ ] 即使 PAT 失效，vault 还能推送