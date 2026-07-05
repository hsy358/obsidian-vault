---
title: AgentSpace 部署踩坑与修复全集（归档版）
date: 2026-07-05
type: deployment-kb
status: ✅ 已跑通
deploy_path: /root/AgentSpace
web_port: 1455
public_url: http://101.35.52.96:1455
related:
  - 2026-07-02 - AgentSpace 本地部署与体验 SOP.md
  - 2026-07-02 - OpenClaw 子进程 Node 版本修复.md
  - 截图/2026-07-04_img_AgentSpace登录页_首次访问.md
purpose: 把 AgentSpace 部署全过程 + 8 个实战坑 + 登录相关问题归一化，给何大人存档 + 喂给新服务器部署参考
---

# 🚀 AgentSpace 部署踩坑与修复全集（归档版）

> **作者**：小助（OpenClaw / MiniMax-M3）
> **写于**：2026-07-05
> **用途**：何大人存档；新服务器部署参照；后续 AgentSpace 类项目踩坑预警
> **对象环境**：腾讯云 Ubuntu 24.04 / 2 vCPU / 3.6 GiB / 59 GiB / Node 22.22.2

---

## 0. 部署结论（先看这里）

| 维度 | 结果 |
|---|---|
| 部署耗时 | **25 分钟**（含 1 次 git clone 失败的踩坑）|
| 磁盘占用 | AgentSpace 目录 **730 MB** + Docker volume ~200 MB = **约 1 GB** |
| Web 端口 | **1455**（本地 + 公网） |
| 数据库 | PostgreSQL 16（Docker 容器，5432）|
| CLI doctor | **8/8 全绿** |
| AgentRouter → OpenClaw 链路 | ✅ **完全打通**（exitCode=0） |
| 安全审计（2026-07-04）| ⚠️ **HTTP 明文 + 密码明文** — 投产前必修 HTTPS |

---

## 1. 完整部署流程（按步骤）

### Step 1：装 Docker Compose v2 plugin

```bash
apt-get install -y docker-compose-v2
mkdir -p ~/.docker/cli-plugins
cp /usr/libexec/docker/cli-plugins/docker-compose ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose
docker compose version   # 期望 v2.40.3
```

> **坑 #1**：直接 `ln -s` 建软链不行，会报 `Text file busy`。**必须 `cp` 出独立副本**。

### Step 2：克隆 AgentSpace 源码（用 codeload tarball）

```bash
cd /root
curl -fL --connect-timeout 15 --max-time 300 \
  -o AgentSpace.tar.gz \
  https://codeload.github.com/HKUDS/AgentSpace/tar.gz/refs/heads/main
tar -xzf AgentSpace.tar.gz
mv AgentSpace-main AgentSpace
rm AgentSpace.tar.gz
```

> **坑 #2**：`git clone https://github.com/HKUDS/AgentSpace.git` 会卡死。GitHub Git 协议在国内服务器太慢（实测 >5 分钟未响应）。**改用 codeload 的 tarball 走 CDN，14 秒搞定**。

### Step 3：配置国内 npm 镜像 + 生成密钥

```bash
cd /root/AgentSpace
npm config set registry https://registry.npmmirror.com

ENCRYPTION_KEY=$(node -e "console.log(require('crypto').randomBytes(32).toString('base64'))")
OAUTH_SECRET=$(node -e "console.log(require('crypto').randomBytes(32).toString('hex'))")

cp .env.example .env
sed -i "s|NEXT_SERVER_ACTIONS_ENCRYPTION_KEY=replace_with_base64_encoded_32_byte_key|NEXT_SERVER_ACTIONS_ENCRYPTION_KEY=$ENCRYPTION_KEY|" .env
sed -i "s|AGENT_SPACE_OAUTH_STATE_SECRET=replace_with_a_long_random_hex_string|AGENT_SPACE_OAUTH_STATE_SECRET=$OAUTH_SECRET|" .env
sed -i "s|AGENT_SPACE_GOOGLE_WORKSPACE_TOKEN_ENCRYPTION_KEY=replace_with_base64_encoded_32_byte_key|AGENT_SPACE_GOOGLE_WORKSPACE_TOKEN_ENCRYPTION_KEY=$ENCRYPTION_KEY|" .env

mkdir -p /var/lib/agentspace/workspaces
```

### Step 4：装依赖

```bash
cd /root/AgentSpace
npm run setup   # ~20 秒，376 个包，730 MB
```

> 首次从 npmmirror 拉，二次走 npm 缓存 ~5 秒。

### Step 5：build daemon（CLI 必需，**关键**）

```bash
cd /root/AgentSpace/packages/daemon
npm run build   # 生成 dist/
```

> **坑 #3**：`npm run setup` **不**会 build daemon。直接跑 `npm run cli --` 会报 `Cannot find module 'agent-space-daemon/dist/index.js'`。**必须先 build**。

### Step 6：起 PostgreSQL 16

```bash
cd /root/AgentSpace
docker compose -f deploy/postgres/docker-compose.yml up -d
sleep 3
docker compose -f deploy/postgres/docker-compose.yml ps
# 期望：postgres-postgres-1  Up  0.0.0.0:5432->5432/tcp
```

### Step 7：初始化数据库

```bash
cd /root/AgentSpace
npm run db:pg:init   # 自动跑所有 schema 迁移
```

### Step 8：启动 Web（Next.js 16 + Turbopack）

```bash
cd /root/AgentSpace
nohup npm run dev:web > /tmp/agentspace-web.log 2>&1 &
# 端口 1455，~728ms ready
```

### Step 9：验证

```bash
curl -sI http://127.0.0.1:1455/ | head -1
# 期望: HTTP/1.1 200 OK

cd /root/AgentSpace
npm run cli -- doctor
# 期望: checks: 8/8 全 ok

npm run cli -- workspace status
# 期望: mode: im / database 连上 / 0 员工 0 频道
```

---

## 2. 部署过程的 8 个坑（症状 → 根因 → 解法 → 教训）

### 坑 #1：docker compose 命令缺失 + 软链报"Text file busy"

| 项 | 内容 |
|---|---|
| 症状 | `docker compose` → `command not found`；`ln -s` 后跑 `docker compose version` 报 `Text file busy` |
| 根因 | Ubuntu 24.04 默认 Docker 不带 compose v2；`ln -s` 创建的 symlink 在某些 FS（overlay）上会被锁 |
| 解法 | `cp` 完整文件到 `~/.docker/cli-plugins/docker-compose`，`chmod +x` |
| 教训 | **软链创建后立即执行可能失败** — 永远 `cp + chmod`，不要 `ln -s` |
| 等级 | 🔴 必踩 |

### 坑 #2：`git clone` 卡死（GitHub Git 协议被限速）

| 项 | 内容 |
|---|---|
| 症状 | `git clone https://github.com/HKUDS/AgentSpace.git` 一直 `Receiving objects: 67%` 不动，>5 分钟未完成 |
| 根因 | 国内服务器访问 GitHub 的 Git（smart HTTP）协议受 GFW 限速；但 codeload.github.com 走 Fastly CDN |
| 解法 | 用 `codeload.github.com/.../tar.gz/refs/heads/main` 下载 tarball（14 秒搞定）|
| 教训 | **下载 GitHub 大仓库永远用 codeload tarball，不用 git clone**（同步归档到 `vault/3-Resources/配置教程/`）|
| 等级 | 🔴 必踩 |

### 坑 #3：CLI 报 `Cannot find module 'agent-space-daemon/dist/index.js'`

| 项 | 内容 |
|---|---|
| 症状 | `npm run cli -- doctor` → `Error: Cannot find module 'agent-space-daemon/dist/index.js'` |
| 根因 | `npm run setup` 只 install + workspace link，不 build TypeScript |
| 解法 | `cd packages/daemon && npm run build` 单独 build |
| 教训 | **TypeScript monorepo 跑 CLI 前永远先 build dist** |
| 等级 | 🔴 必踩 |

### 坑 #4：OpenClaw harness 调用失败 — `Node.js v22.19+ is required (current: v18.19.1)`

| 项 | 内容 |
|---|---|
| 症状 | `agent-router.js run --harness openclaw ...` → `exitCode: 1`，错误 `Node.js v22.19+ is required (current: v18.19.1)` |
| 根因（双层） | **第 1 层**：`/usr/local/bin/openclaw` wrapper 用 `$HOME/.nvm`，daemon 子进程 `$HOME` 为空 → nvm 不加载 → PATH 缺 v22<br>**第 2 层**：AgentRouter daemon 用 `process.env.PATH` 找 `openclaw`，**直接命中** `/root/.local/share/pnpm/openclaw`（pnpm 自动生成的 sh 脚本），里面 `exec node "$basedir/.../openclaw.mjs"` 不带 nvm 切换 → PATH 找 `node` → `/usr/bin/node`（v18）→ 失败 |
| 解法 | **修复 1**（wrapper 用绝对路径）：<br>`cat > /usr/local/bin/openclaw <<'EOF'<br>#!/bin/sh<br>export NVM_DIR="/root/.nvm"<br>[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"<br>export PNPM_HOME="/root/.local/share/pnpm"<br>export PATH="$PNPM_HOME:$PATH"<br>exec "/root/.local/share/pnpm/openclaw" "$@"<br>EOF`<br>**修复 2**（pnpm sh 脚本头部注入 nvm）：<br>`cat > /root/.local/share/pnpm/openclaw <<'EOF'<br>#!/bin/sh<br>export NVM_DIR="/root/.nvm"<br>[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"<br>EOF`<br>然后把 pnpm 原始内容追加到尾部 |
| 教训 | **pnpm 升级会覆盖修复 2**；**OpenClaw 重装会覆盖修复 1**。补救：写 systemd service 或 cron，每次开机/升级后自动重新注入（脚本见 §4）|
| 等级 | 🔴 必踩 |

### 坑 #5：公网 HTTP 标"不安全" + 密码明文传输

| 项 | 内容 |
|---|---|
| 症状 | Chrome 访问 `http://101.35.52.96:1455` → 地址栏标"不安全"；DevTools Network → RSC payload 中 `1_password=hesiyan123` 明文 |
| 根因 | Next.js 16 dev server 默认 HTTP；登录表单用 RSC（React Server Components），序列化字段 `1_email / 1_password` 直接提交 |
| 解法（投产前必修）| 1. 上 HTTPS（Let's Encrypt / 自签证书，nginx 反向代理）<br>2. 密码前端 bcrypt 加盐后再传输，或服务端 action 内处理<br>3. 加 CSRF token（Next.js server action 默认有，但仍需验证）<br>4. 警惕反射型 XSS（字段名带数字前缀）|
| 教训 | **部署 demo 给客户看之前，必须先解决公网 HTTPS + 凭据安全** — 投产 blocker |
| 等级 | 🔴 投产 blocker |

### 坑 #6：npm 11 vs 10.9.7 兼容性

| 项 | 内容 |
|---|---|
| 症状 | `packageManager` 字段声明 `npm@11.6.2`，系统装的是 `10.9.7` |
| 根因 | AgentSpace `package.json` 锁定 npm 11 |
| 解法 | **当前 10.9.7 兼容运行**（实际验证 setup + dev:web 都成功）；如有问题再 `npm i -g npm@11` |
| 教训 | Node 22 自带 npm 10，要 npm 11 需手动升 |
| 等级 | 🟢 可选 |

### 坑 #7：磁盘 12 GiB + 内存 3.6 GiB 资源紧张

| 项 | 内容 |
|---|---|
| 症状 | PostgreSQL + Next.js 同时跑会触发 swap；磁盘装完剩 11 GiB |
| 根因 | 腾讯云最低配 2C3.6G 跑双服务紧张 |
| 解法 | 1. 体验时关掉其他重进程（Chrome、VNC、holding 监控）<br>2. PostgreSQL 加 `shared_buffers=256MB` 限制内存<br>3. Next.js dev 模式加 `--memory-limit 1024` |
| 教训 | **不要在 3.6 GiB 机器上同时跑 PG + Web + 浏览器调试** |
| 等级 | 🟡 体验时注意 |

### 坑 #8：Feishu 集成未合主线

| 项 | 内容 |
|---|---|
| 症状 | `npm run cli -- integrations feishu worker --dry-run` 只看到 smoke plan，没有真实拉取 |
| 根因 | Feishu 集成还在分支 `codex/feishu-integration`，2026-07-01 未 merge |
| 解法 | 不要在主线 demo 中演示 Feishu 集成；要演示需手动 checkout 分支 |
| 教训 | **demo 前查 GitHub PR 状态**，别相信 README 标的"已支持" |
| 等级 | 🟡 暂不影响主流程 |

---

## 3. 登录页相关问题（7-4 何大人首次访问发现）

### 3.1 已确认的"坑"

1. **HTTP 明文**：浏览器标"不安全" → 投产前必须上 HTTPS
2. **密码明文提交**：DevTools Network → RSC payload 中 `1_password=hesiyan123` 原样
3. **缺 Logo / 品牌标识**：首次访问不知道是哪家产品
4. **缺 CTA 主色**：登录按钮没强颜色，"登录进入工作台"按钮颜色过浅
5. **文案生硬**：「原生 Agent 集群时代」「信用和复用」（→「被信任并复用」更通顺）
6. **缺辅助功能**：忘记密码 / 免费注册 / SSO / TOS / 隐私协议链接缺失
7. **排版**：4 张卡片 3+1 排版下方留白偏大

### 3.2 已确认的 DevTools 工程痕迹

- `_rsc=lquux / 1nal5 / wnywt`：React Server Components 多请求重渲染（正常）
- 表单字段 `1_xxx`：典型 RSC 客户端组件编号（**不是** bug，是 RSC 序列化机制）

### 3.3 后续行动（按优先级）

| 优先级 | 行动 | 责任 |
|---|---|---|
| P0 | 上 HTTPS（nginx + Let's Encrypt）| 部署侧 |
| P0 | 密码前端哈希 + 服务端加盐 | AgentSpace 项目（HKUDS） |
| P1 | 加 Logo / 品牌色 | AgentSpace 项目 |
| P1 | 加忘记密码 / 注册 / TOS / 隐私链接 | AgentSpace 项目 |
| P2 | 4 卡片排版优化 | AgentSpace 项目 |

---

## 4. 补救脚本（pnpm 升级后会失效的修复）

加到 `/root/bin/openclaw-patch.sh`，配 systemd 或 cron 每次开机后跑：

```bash
#!/bin/bash
# OpenClaw pnpm sh 脚本补丁（防 pnpm 升级覆盖）
PnpmSh="/root/.local/share/pnpm/openclaw"
if ! head -3 "$PnpmSh" | grep -q "nvm 加载"; then
    cp "$PnpmSh" "$PnpmSh.bak"
    cat > "$PnpmSh" <<'EOF'
#!/bin/sh
# 注入 nvm 加载（避免 AgentRouter 子进程因 PATH 缺 v22 而失败）
export NVM_DIR="/root/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
EOF
    cat "$PnpmSh.bak" >> "$PnpmSh"
    chmod +x "$PnpmSh"
    echo "[$(date)] openclaw pnpm sh 脚本已重新注入 nvm 加载" >> /var/log/openclaw-patch.log
fi
```

**新服务器第一次部署时直接执行此脚本**，省一次踩坑。

---

## 5. 时间线（实战日志）

| 步骤 | 时间 | 备注 |
|---|---|---|
| 装 docker-compose-v2 + cp plugin binary | 8:05 | 修 docker compose 命令 |
| 第一次 git clone 卡死，放弃 | 8:07 | 网络太慢 |
| 改用 codeload tarball，14 秒下完 | 8:11 | 决定不再用 git clone |
| setup 装 376 包，730 MB | 8:13 | 23 秒 |
| .env 密钥生成 + 附件目录 | 8:14 | |
| PostgreSQL 容器 up | 8:15 | 5432 端口监听 |
| db:pg:init | 8:16 | 所有表创建 |
| npm run dev:web → Next.js 16 Ready in 728ms | 8:17 | |
| 主页 200 OK + 截图 | 8:18 | |
| 第一次跑 CLI 报 daemon dist 缺失 | 8:20 | 漏 build（坑 #3）|
| cd packages/daemon && npm run build | 8:22 | 修 CLI |
| CLI doctor 8/8 OK + workspace status | 8:24 | 全绿 |
| AgentRouter → OpenClaw 调通（exitCode=0）| 9:10 | 修完坑 #4 双层 |
| 何大人首次访问公网 + 安全审计 | 2026-07-04 22:04 | 发现 HTTP 明文 + 密码明文 |

**总耗时**：25 分钟（含 1 个 git clone 失败的踩坑）
**真正踩坑修复累计耗时**：约 1 小时（含 OpenClaw 子进程 debug）

---

## 6. 给新服务器部署时的关键差异提醒

| 项 | 老服务器（101.35.52.96）| 新服务器（待确认）|
|---|---|---|
| OS | Ubuntu 24.04 LTS | 待确认（建议同 Ubuntu 24.04）|
| Node | 22.22.2 | 需预装 v22.19+（OpenClaw 硬要求）|
| Docker | 29.1.3 + compose v2 | 需手动装 compose v2 |
| 磁盘 | 59 GiB / 12 GiB 可用 | 建议 ≥20 GiB 可用 |
| 内存 | 3.6 GiB / 2.2 GiB 可用 | 建议 ≥4 GiB |
| 公网 IP | 101.35.52.96 | 待确认 |
| 公网端口 | 1455（已放通腾讯云安全组）| 需提前放通 |
| HTTPS | ❌ 暂未上 | **投产前必须上** |
| 数据库 | PostgreSQL 16（Docker）| 同上 |

---

## 7. 已交付文件清单

| 文件 | 路径 |
|---|---|
| 部署 SOP（步骤化）| `/root/vault/1-Projects/德勤/AI-Native/AgentSpace-部署/2026-07-02 - AgentSpace 本地部署与体验 SOP.md` |
| OpenClaw 子进程修复 SOP | `/root/vault/1-Projects/德勤/AI-Native/AgentSpace-部署/2026-07-02 - OpenClaw 子进程 Node 版本修复.md` |
| 登录页首次访问截图 + 安全审计 | `/root/vault/1-Projects/德勤/AI-Native/AgentSpace-部署/截图/2026-07-04_img_AgentSpace登录页_首次访问.md` |
| 本文档（踩坑全集）| `/root/vault/1-Projects/德勤/AI-Native/AgentSpace-部署/2026-07-05 - AgentSpace 部署踩坑与修复全集（归档版）.md` |
| 新服务器速查版 | `/root/vault/1-Projects/德勤/AI-Native/AgentSpace-部署/2026-07-05 - AgentSpace 新服务器部署速查.md` |

---

## 8. 引用资源

- AgentSpace GitHub：https://github.com/HKUDS/AgentSpace
- codeload 镜像：`https://codeload.github.com/HKUDS/AgentSpace/tar.gz/refs/heads/main`
- npm 镜像：`https://registry.npmmirror.com`
- OpenClaw 文档：`/root/.local/share/pnpm/global/5/.pnpm/openclaw@2026.5.26/node_modules/openclaw/docs`
- 德勤项目 README：`/root/vault/1-Projects/德勤/README.md`

---

**作者**：小助 — OpenClaw (MiniMax-M3) — 2026-07-05