---
title: "Insomnia — macOS 定时防休眠菜单栏 App（Agent 长会话守护）"
source: github
url: https://github.com/krishhgg/Insomnia
saved_date: 2026-10-28
tags: ["GitHub-分析", "macOS", "Agent-基础设施", "工具链", "Swift"]
description: "1754 star，macOS 26 + Apple Silicon 专属：给 coding agent 会话设定到期时间，合盖不睡眠，崩溃也能自动恢复"
---

# Insomnia — GitHub 仓库分析

**仓库**: [github.com/krishhgg/Insomnia](https://github.com/krishhgg/Insomnia)
**Star**: 1,754 ⭐ | **语言**: Swift 6.2 | **License**: MIT
**创建**: 2026-09-14 | **最近推送**: 2026-10-27
**官网**: https://getinsomnia.app

> 一句话：macOS 菜单栏小眼睛图标，**让 Mac 保持清醒并给会话设定结束时间**——专门为长时间无人值守的 coding agent 会话设计。

## 定位与适用边界

- **平台硬约束**：macOS **26+** + **Apple Silicon**（`platforms: [.macOS(.v26)]`，release zip 仅 arm64）
- **非本机可装**：当前工作机是 Linux x86_64（VM-0-10-ubuntu），**无法安装**；只有何大人的 MacBook（macOS 26 + M 系列）才适用
- **状态**：实验性（experimental），README 明确写 "Recovery can fail, and a running timer is not a safety guarantee"

## 核心能力

| 能力 | 说明 |
|---|---|
| 定时防睡眠 | 设置 N 天/小时/分钟，期间 `pmset -a disablesleep 1` |
| 合盖行为 | 合盖后：屏幕/键盘灯灭（先存亮度）、冻结名单 App（SIGSTOP）、静音、开低电量模式、Docker 空闲时冻结（默认关） |
| 冻结名单 | 默认 Slack / WhatsApp / Discord；自动跳过 Zoom/Teams/Webex/FaceTime/OBS/Loom 等会议录制类 |
| 电池/温度规则 | 电量 <40% 开低电量模式，<10% 结束会话；温度 critical 结束会话（默认开） |
| tmux 续命 | 断网 90 秒后向标记过的 tmux pane 输入 `continue`（默认不按回车） |
| iPhone 热点接管 | Wi-Fi 掉线后自动切热点，密码存 login Keychain |
| 浏览器反限速 | Chrome/Chromium/Arc/Comet 可"重启为不 throttled"模式 |

## 架构亮点（最值得抄的部分）

### 1. Journal-first 恢复机制

每次改动**先写 recovery journal（磁盘文件）**，再执行变更。App 崩溃/被杀后，由 launchd 恢复代理（每 60 秒一次）在会话到期时按 journal 逆向回滚。

```
应用层 (Swift)  ──┐
                  ├──► APP_SUPPORT/.recovery.lock (flock 排他锁)
launchd backstop ─┘         └──► session.json / state.json (journal)
```

- `backstop.sh`（1489 行 bash）**完全脱离 Swift**，纯靠 journal 复原
- 每次运行是一个事务：读 journal → 判断 → 撤销 → 原子发布新 journal → 释放锁
- 锁拿不到就 `exit 75`，交给 launchd 一分钟后重试
- 冻结进程只对**能证明是自己冻结的** pid 发 SIGCONT（比对启动时间到微秒 + boot session + stopped 状态）

### 2. 代码签名封条

- `backstop.sh` 被封进 `Insomnia.app/Contents/Resources`，签名覆盖
- LaunchAgent 每次运行前 `codesign --verify --strict`，比对 plist 里钉住的 code requirement（ad-hoc 构建即 cdhash）
- 被编辑过的 bundle/脚本 → 校验失败 → 只写一行日志、不执行任何东西
- 安装器剥掉 bundle 的 group/other 写权限与所有 ACL；**任何可执行文件都不放在可写目录**

### 3. 安装/升级的事务性

- 升级先让运行中的 App 退出（拒绝退出就中止）
- 新 bundle 构建在 staging 目录 → 确认旧 LaunchAgent 已 unload → 才原子替换（app + agent 同步换）
- 失败回滚：把旧 bundle 放回并重新 load；实在放不回则保留在 `~/Applications/.Insomnia.app.previous` 并打印恢复命令
- 持锁期间所有 `sudo`/`pgrep`/`launchctl`/`codesign` 调用有 30s 超时，超时 SIGTERM→SIGKILL，保证锁一定释放

### 4. 安全边界处理得很克制

- sudoers 规则只放开 4 条 pmset 命令（`/usr/bin/pmset -a disablesleep 1/0`、`-b lowpowermode 1/0`）
- 但**该权限对同账号下任何程序都可用**——README 明确承认
- 不沙箱；`~/Library/LaunchAgents` plist 仍是用户可写（任何 LaunchAgent 都一样）
- App 也不沙箱；配置文件 owner-only，但**保留 symlink 和 ACL**（可能跨账号泄露）
- 日志可能包含 Wi-Fi 名称、进程信息、tmux target，分享前需检查

## 渠道与安装

| 渠道 | 说明 |
|---|---|
| Stable | `v0.1.0`（2026-10-10），GitHub 标记 Latest，**打包方式特殊**：手工打包、无 attestation、zip 内 `install.sh --app ./Insomnia.app` |
| Nightly | `nightly-<YYYYMMDD>-<12位commit>`，每天从 main 自动构建，最新为 `nightly-20261027-b8e7e20d617f` |

**安装（release 方式）**：
```bash
gh release download --repo krishhgg/Insomnia --pattern '*.zip' --pattern SHA256SUMS
shasum -a 256 -c SHA256SUMS
gh attestation verify <zip> -R krishhgg/Insomnia \
  --signer-workflow krishhgg/Insomnia/.github/workflows/release.yml \
  --source-ref refs/tags/v<version> --source-digest <40位commit>
ditto -x -k <zip> . && cd <zip名> && ./install.sh --allow-unverified-origin --app ./Insomnia.app
open "$HOME/Applications/Insomnia.app"
```

**源码构建**：需 Xcode + Swift 6.2+
```bash
git clone --branch v<version> --depth 1 https://github.com/krishhgg/Insomnia.git
cd Insomnia && ./scripts/install.sh
```

**卸载**：`./scripts/uninstall.sh`（加 `--purge` 连配置和日志一起删）

## 仓库自带 Agent Skill

- `skills/install-insomnia/SKILL.md` — 安装/升级
- `skills/maintain-insomnia/SKILL.md` — 排查恢复失败

安装 Skill 里明确写：**Agent 不得自己跑 sudo，也不得把密码传给 sudo**——需要管理员权限的步骤要把命令交给用户在 Terminal 里跑。这条边界写得很克制，值得学。

## 代码规模

- Swift 源文件 119 个
- Shell：`backstop.sh` 1489 行、`install.sh` 1191 行、`uninstall.sh` 1106 行
- Swift 重点模块：`NetworkFailover.swift` 1105 行、`Freezer.swift` 438 行、`RuntimeState.swift` 387 行
- CI：`ci.yml` + `mac-mini.yml`（真机 Mac mini 跑）+ `merge-gate.yml` + shellcheck/actionlint

## 我的判断

**对何大人的价值**：如果何大人在 MacBook 上跑长时间 Claude Code / Codex 会话，这是目前最完整的"合盖不睡 + 到点自动恢复"的方案，比手搓 `caffeinate` 强太多——尤其是 journal + launchd backstop 那一层，纯 `caffeinate` 一旦进程被杀就失效。

**但**：
1. 当前 Linux 工作机装不了，只能在 Mac 上用
2. sudoers 规则确实给了同账号全权限，Mac 上若有其他不可信程序需留意
3. 项目 2026-09 才创建，仅 1754 star，实验性——建议先跑短会话观察 `~/Library/Logs/Insomnia/insomnia.log`

**对德勤项目的可借鉴点**（跟执行器抽象层同源思路）：
- **Journal-first + 外部 backstop**：Agent 执行器崩溃后由独立守护进程按日志回滚——这正是 Hermes/OpenClaw 执行器抽象层该有的"补偿事务"模式
- **超时即信号**：持锁期间对外部命令一律 30s 超时 + SIGTERM→SIGKILL，保证锁释放。这个"锁不能泄漏"的纪律值得直接抄进我们的执行器 adapter
- **能力证明而非路径匹配**：只对能证明是自己冻结/创建的进程做恢复，不靠路径猜测
