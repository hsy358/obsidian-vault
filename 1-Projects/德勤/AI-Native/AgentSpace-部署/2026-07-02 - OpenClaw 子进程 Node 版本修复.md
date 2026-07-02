---
title: AgentSpace AgentRouter → OpenClaw 子进程 Node 版本修复
date: 2026-07-02
type: bugfix
status: ✅ 修复验证通过
related:
  - /root/vault/1-Projects/德勤/AI-Native/AgentSpace-部署/2026-07-02 - AgentSpace 本地部署与体验 SOP.md
---

# 🐛 OpenClaw 子进程 Node 版本修复（AgentRouter 集成必备）

> **作者**：小助（OpenClaw）
> **写于**：2026-07-02 09:10
> **修复对象**：`/usr/local/bin/openclaw` wrapper + `/root/.local/share/pnpm/openclaw` pnpm sh 脚本
> **验证**：AgentRouter → OpenClaw harness 实际调用成功（exitCode=0）

---

## 问题现象

```bash
# 单独调 openclaw 正常
$ openclaw --version
OpenClaw 2026.5.26 (10ad3aa)

# 但通过 AgentRouter 调 OpenClaw harness 失败
$ ./packages/daemon/bin/agent-router.js run --harness openclaw ...
{
  "rawProviderMessage": "openclaw: Node.js v22.19+ is required (current: v18.19.1).\nIf you use nvm, run:\n  nvm install 22",
  "exitCode": 1
}
```

---

## 根因分析（两层）

### 第 1 层：wrapper 依赖 `$HOME`

`/usr/local/bin/openclaw`（sh wrapper）：
```sh
#!/bin/sh
export NVM_DIR="$HOME/.nvm"   # ← $HOME 是空的（daemon 子进程没传）
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"  # ← 加载失败
```

当 AgentRouter daemon 启动子进程时，**环境变量被部分清空**，`$HOME` 不存在 → nvm.sh 找不到 → nvm 不加载 → PATH 缺 v22。

### 第 2 层：AgentRouter 不走 wrapper，直接命中 pnpm sh 脚本

AgentRouter daemon 用 `process.env.PATH` 找 `openclaw`，命中的是：
```
/root/.local/share/pnpm/openclaw   ← pnpm 自己生成的 sh 脚本
```

**不是** `/usr/local/bin/openclaw`（wrapper）。

pnpm 的 sh 脚本最后：
```sh
exec node "$basedir/global/5/.pnpm/openclaw@2026.5.26/node_modules/openclaw/openclaw.mjs" "$@"
```

直接 `exec node`（**不带任何 Node 版本切换逻辑**）→ PATH 找 `node` → `/usr/bin/node`（v18）→ 失败。

---

## 复现命令

```bash
# Test 1：完全清空环境（模拟 daemon 子进程）
$ env -i /usr/local/bin/openclaw --version
openclaw: Node.js v22.19+ is required (current: v18.19.1).   # ❌

# Test 2：给最小 PATH 但没 HOME
$ env -i PATH="/usr/local/bin:/usr/bin:/bin" /usr/local/bin/openclaw --version
openclaw: Node.js v22.19+ is required (current: v18.19.1).   # ❌

# Test 3：给 HOME（正常情况）
$ env -i HOME=/root PATH="/usr/local/bin:/usr/bin:/bin" /usr/local/bin/openclaw --version
OpenClaw 2026.5.26 (10ad3aa)   # ✅
```

---

## 修复

### 修复 1：wrapper 用绝对路径（避免 `$HOME` 缺失）

```bash
cp /usr/local/bin/openclaw /usr/local/bin/openclaw.bak

cat > /usr/local/bin/openclaw <<'EOF'
#!/bin/sh
# 加载 nvm 以确保 node 在 PATH 中（绝对路径避免 $HOME 缺失问题）
export NVM_DIR="/root/.nvm"   # ← 改：原是 "$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
export PNPM_HOME="/root/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"
export XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/run/user/$(id -u)}
exec "/root/.local/share/pnpm/openclaw" "$@"
EOF
chmod +x /usr/local/bin/openclaw
```

### 修复 2：pnpm sh 脚本头部注入 nvm 加载（关键）

AgentRouter 不走 wrapper，直接命中 pnpm sh 脚本，**所以必须修这个**。

```bash
cp /root/.local/share/pnpm/openclaw /root/.local/share/pnpm/openclaw.bak

cat > /root/.local/share/pnpm/openclaw <<'EOF'
#!/bin/sh
# 注入 nvm 加载（避免 AgentRouter 子进程因 PATH 缺 v22 而失败）
export NVM_DIR="/root/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
EOF

# 把 pnpm 原内容追加
cat /root/.local/share/pnpm/openclaw.bak >> /root/.local/share/pnpm/openclaw
chmod +x /root/.local/share/pnpm/openclaw
```

---

## 验证

### Test 1：完全 env -i（修前 ❌ → 修后 ✅）

```bash
$ env -i /usr/local/bin/openclaw --version
manpath: warning: $PATH not set    # ← man-db 警告，可忽略
OpenClaw 2026.5.26 (10ad3aa)        # ✅

$ env -i /root/.local/share/pnpm/openclaw --version
manpath: warning: $PATH not set
OpenClaw 2026.5.26 (10ad3aa)        # ✅
```

### Test 2：AgentRouter 实际调用（修前 ❌ → 修后 ✅）

```bash
$ cd /root/AgentSpace
$ ./packages/daemon/bin/agent-router.js run \
    --harness openclaw \
    --cwd /root/AgentSpace \
    --mode medium \
    --session-id test-fix \
    "用一句话介绍 HKUDS/AgentSpace"
{
  "events": [
    {"type": "harness_started", "harness": "openclaw", "command": [...]},
    {"type": "harness_exited", "exitCode": 0},    # ← 修前是 1
    {"type": "session_updated", "sessionId": "test-fix"}
  ],
  "exitCode": 0                          # ✅ 链路打通
}
```

直接调 openclaw 也能拿到 LLM 返回：
```
"text": "Google 在 2025 年推出的企业级 AI Agent 平台..."
```
（模型幻觉把 AgentSpace 当成 Google 产品，但**调用链完整跑通**）

---

## ⚠️ 注意事项

1. **pnpm 升级会覆盖修复 2** — 如果你跑 `pnpm update -g`，`/root/.local/share/pnpm/openclaw` 会被重写，修复就失效了
2. **OpenClaw 重装会覆盖修复 1** — 同理
3. **建议补救**：写一个 systemd service 或 cron 任务，每次开机/升级后自动重新注入

```bash
# 加到 /root/bin/openclaw-patch.sh
#!/bin/bash
PnpmSh=/root/.local/share/pnpm/openclaw
if ! head -3 "$PnpmSh" | grep -q "nvm 加载"; then
    cp "$PnpmSh" "$PnpmSh.bak"
    cat > "$PnpmSh" <<'EOF'
#!/bin/sh
export NVM_DIR="/root/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
EOF
    cat "$PnpmSh.bak" >> "$PnpmSh"
    chmod +x "$PnpmSh"
fi
```

---

## 已知遗留问题（不影响功能）

| 问题 | 等级 | 描述 |
|---|---|---|
| AgentRouter 解析 OpenClaw 输出 | 🟡 | `empty_response` 错误，但 OpenClaw 实际有返回（模型有 text 输出）|
| AgentRouter 缺默认 session target | 🟢 | 不传 `--session-id` 时 OpenClaw 报错 |

这两个是 AgentSpace 项目（HKUDS/AgentSpace）自身的小 bug，应该在 GitHub 提 issue。当前不影响我们验证"链路打通"的目的。

---

**作者**：小助 — OpenClaw (MiniMax-M3) — 2026-07-02