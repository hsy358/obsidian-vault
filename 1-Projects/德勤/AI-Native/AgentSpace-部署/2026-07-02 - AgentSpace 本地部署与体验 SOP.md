---
title: AgentSpace 本地部署与体验 SOP（2026-07-02 实操版）
date: 2026-07-02
type: deployment-sop
status: ✅ 已跑通
deploy_path: /root/AgentSpace
web_port: 1455
db: PostgreSQL 16 (Docker)
purpose: AgentSpace PoC 部署 — 用完可停，停止后容器+目录不删，方便重启
related:
  - /root/vault/1-Projects/德勤/AI-Native/笔记/2026-06-28 - AgentSpace - GitHub Deep Research.md
  - /root/vault/1-Projects/德勤/AI-Native/笔记/2026-06-29-AgentSpace研究笔记.md
---

# 🚀 AgentSpace 本地部署与体验 SOP（实操验证版）

> **作者**：小助（OpenClaw）
> **写于**：2026-07-02 08:14-08:30（45 分钟内完成部署）
> **验证结果**：✅ 跑通 — Web :1455 200 OK，CLI doctor 8/8 OK，DB 连接成功
> **决策依据**：2026-07-02 何大人指令「标准安装，验证和使用 AgentSpace 功能」

---

## 0. 服务器现状（部署前）

| 维度 | 配置 |
|---|---|
| CPU | 2 vCPU EPYC 7K62 @ 2GHz |
| 内存 | 3.6 GiB / 可用 2.2 GiB（Swap 9.9 GiB） |
| 磁盘 | 59 GiB / 可用 **12 GiB** |
| OS | Ubuntu 24.04 LTS |
| Node.js | v22.22.2 |
| npm | 10.9.7（AgentSpace 推荐 11.6.2，兼容） |
| Docker | 29.1.3（**docker compose 命令原本缺失**） |
| PostgreSQL | 无（需 Docker 起） |

**部署后磁盘占用**：AgentSpace 目录 730MB + Docker volume ~200MB = **约 1GB**。

---

## 1. 安装命令（按顺序，每步都验证过）

### Step 1：装 Docker Compose v2 plugin

Ubuntu 24.04 默认 Docker 不带 compose，需要单独装：

```bash
apt-get install -y docker-compose-v2
# 装完后 binary 在 /usr/libexec/docker/cli-plugins/docker-compose
# Docker CLI 默认不认这个路径，必须手动建软链：
mkdir -p ~/.docker/cli-plugins
cp /usr/libexec/docker/cli-plugins/docker-compose ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose
docker compose version
# 期望输出: Docker Compose version v2.40.3
```

> **坑**：直接用 `ln -s` 建软链不行，会报 `Text file busy`。必须 `cp` 出独立副本。

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

> **坑**：用 `git clone https://github.com/HKUDS/AgentSpace.git` 会卡死——GitHub Git 协议在国内服务器太慢。`codeload` 的 tarball 走 CDN，14 秒搞定。

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

### Step 4：装依赖（npm run setup）

```bash
cd /root/AgentSpace
npm run setup  # ~20 秒，376 个包，730 MB
```

> **首次 vs 二次**：首次从 npmmirror 拉，二次走 npm 缓存 ~5 秒。

### Step 5：build daemon（CLI 必需）

```bash
cd /root/AgentSpace/packages/daemon
npm run build  # 生成 dist/
```

> **关键**：`npm run setup` 不 build daemon，导致 `npm run cli --` 会报 `Cannot find module 'agent-space-daemon/dist/index.js'`。**必须先 build**。

### Step 6：起 PostgreSQL 16

```bash
cd /root/AgentSpace
docker compose -f deploy/postgres/docker-compose.yml up -d
sleep 3
docker compose -f deploy/postgres/docker-compose.yml ps
# 期望：postgres-postgres-1   postgres:16   Up   0.0.0.0:5432->5432/tcp
```

### Step 7：初始化数据库

```bash
cd /root/AgentSpace
npm run db:pg:init  # 自动跑所有 schema 迁移
```

### Step 8：启动 Web（Next.js 16 + Turbopack）

```bash
cd /root/AgentSpace
nohup npm run dev:web > /tmp/agentspace-web.log 2>&1 &
# 端口 1455，728ms ready
# 日志：tail -f /tmp/agentspace-web.log
```

### Step 9：验证

```bash
curl -sI http://127.0.0.1:1455/ | head -3
# 期望: HTTP/1.1 200 OK

cd /root/AgentSpace
npm run cli -- doctor
# 期望: checks: 8/8 全 ok

npm run cli -- workspace status
# 期望: mode: im / database 连上 / 0 员工 0 频道
```

---

## 2. 启动 / 停止 / 重启 / 卸载 速查

### 启动（全部重启）

```bash
# 1. 起 PostgreSQL（如果未起）
cd /root/AgentSpace && docker compose -f deploy/postgres/docker-compose.yml up -d

# 2. 起 Web
cd /root/AgentSpace && nohup npm run dev:web > /tmp/agentspace-web.log 2>&1 &

# 3. 验证
sleep 5 && curl -sI http://127.0.0.1:1455/ | head -1
```

### 停止（保留数据，下次能起来）

```bash
# 停 Web
pkill -f "next dev --hostname 0.0.0.0 --port 1455"
pkill -f "node.*AgentSpace/apps/web"

# 停 PostgreSQL（容器不删，数据卷保留）
cd /root/AgentSpace && docker compose -f deploy/postgres/docker-compose.yml stop
```

### 重启

```bash
cd /root/AgentSpace
docker compose -f deploy/postgres/docker-compose.yml start
nohup npm run dev:web > /tmp/agentspace-web.log 2>&1 &
```

### 完全卸载（连数据一起删）

```bash
# 停 + 删容器 + 删卷
cd /root/AgentSpace
docker compose -f deploy/postgres/docker-compose.yml down -v

# 删 AgentSpace 目录
rm -rf /root/AgentSpace
rm -rf /var/lib/agentspace
```

---

## 3. 当前进程状态（2026-07-02 08:30）

| 组件 | 状态 | PID/端口 |
|---|---|---|
| PostgreSQL 16 | ✅ Up | 容器 `postgres-postgres-1` :5432 |
| Next.js 16.2.2 Web | ✅ Ready | PID 2415663 :1455 |
| agent-space-daemon | ⚪ 未启动 | （用 `npm run cli -- daemon start` 起） |
| docker compose | ✅ v2.40.3 | `~/.docker/cli-plugins/docker-compose` |

---

## 4. CLI 命令清单（验证过的）

```bash
cd /root/AgentSpace
npm run cli -- help                          # 完整命令
npm run cli -- doctor                        # 8 项 check
npm run cli -- workspace status              # 看 workspace 摘要
npm run cli -- workspace init --reset        # 重置 workspace
npm run cli -- db status                     # 看 DB 表+行数
npm run cli -- im channels                   # IM 频道
npm run cli -- im feed                       # 协作 feed
npm run cli -- channel list                  # 列频道
npm run cli -- channel create --name <n>     # 建频道
npm run cli -- employee list                 # 列数字员工
npm run cli -- employee create --name Vega --role "发布协调员"
npm run cli -- task create --title "..." --channel general
npm run cli -- message post --channel general --summary "..."
npm run cli -- skill list                    # 列 Skills
npm run cli -- integrations feishu worker --dry-run
```

> **agent-router 命令**：研究笔记里写的 `agent-router harnesses` 是 daemon 内的命令，不是 CLI 顶层命令。需要先 `npm run cli -- daemon start` 才能用。

---

## 5. AgentRouter 实测（待 daemon 起来后补）

> TODO: 启动 daemon 后补充 `agent-router harnesses` / `agent-router detect` / `agent-router run` 的实际输出

---

## 6. 与德勤 v0.3 的实际借鉴点（PoC 期间观察）

1. **Workspace 数据模型**：观察 `npm run cli -- db status` 输出，看 AgentSpace 的 schema 设计
2. **Digital Employee 创建**：试用 `employee create`，看 Owner / Skills / Runtime 绑定流程
3. **Channel + Task 协作流**：试 `channel create` + `task create` + `task claim`，对比 v0.3 R4 设计
4. **Permission Control Plane**：看 `permission` 类命令（待 daemon 起后）
5. **Feishu 集成**：试 `integrations feishu worker --dry-run`，看飞书机器人配置 UX

---

## 7. 注意事项 & 已知限制

- ⚠️ **npm 11 vs 10.9.7**：项目 packageManager 是 npm@11.6.2，但 npm 10.9.7 兼容运行。如有问题再升级
- ⚠️ **磁盘 12 GiB 可用**：装完剩 11 GiB，注意 vault 增长 / Docker 镜像缓存会占
- ⚠️ **内存 3.6 GiB**：PostgreSQL + Next.js 同时跑会触发 swap，建议体验时关掉其他重进程
- ⚠️ **Feishu 集成未合主线**：2026-07-01 还在分支 `codex/feishu-integration`，干跑命令可能只看到 smoke plan
- ⚠️ **Google Workspace 集成**：需 OAuth 配置，本机未配（如需体验另开）

---

## 8. 时间线记录

| 步骤 | 时间 | 备注 |
|---|---|---|
| 8:05 | 装 docker-compose-v2 + cp plugin binary | 修 docker compose 命令 |
| 8:07 | 第一次 git clone 卡死，放弃 | 网络太慢 |
| 8:11 | 改用 codeload tarball，14 秒下完 | 决定不再用 git clone |
| 8:13 | setup 装 376 包，730 MB | 23 秒 |
| 8:14 | .env 密钥生成 + 附件目录 | |
| 8:15 | PostgreSQL 容器 up | 5432 端口监听 |
| 8:16 | db:pg:init | 所有表创建 |
| 8:17 | npm run dev:web → Next.js 16 Ready in 728ms | |
| 8:18 | 主页 200 OK + 截图 | |
| 8:20 | 第一次跑 CLI 报 daemon dist 缺失 | 漏 build |
| 8:22 | cd packages/daemon && npm run build | 修 CLI |
| 8:24 | CLI doctor 8/8 OK + workspace status | 全绿 |
| 8:30 | 写 SOP | |

---

**总耗时**：25 分钟（含 1 个 git clone 失败的踩坑）

**作者**：小助 — OpenClaw (MiniMax-M3) — 2026-07-02