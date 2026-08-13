---
title: StaffDeck 部署手册（OpenBMB 数字员工平台）
date: 2026-07-24
type: deployment-manual
status: running
ip: 101.33.212.119
port: 5180
url: http://101.33.212.119:5180
license: AGPL-3.0
source: https://github.com/OpenBMB/StaffDeck
official: https://staffdeck.openbmb.cn/
related:
  - /root/vault/current-server/开源软件访问清单.md
  - /root/vault/current-server/from-agent/2026-07-24/2026-07-24 - 公众号-StaffDeck-一飞开源.md
---

# 🏢 StaffDeck 部署手册

> **官方**：https://staffdeck.openbmb.cn/
> **GitHub**：https://github.com/OpenBMB/StaffDeck（⭐ 946）
> **定位**：企业级数字员工平台（OpenBMB / 面壁智能 / 清华 / 东大 联合研发）
> **开源时间**：2026-07-15（部署时**仅 9 天**）
> **许可证**：AGPL-3.0 ⚠️

---

## 🎯 1. 项目信息

| 项 | 值 |
|---|---|
| **访问 URL** | `http://101.33.212.119:5180/`（**带端口 5180**，不能用 80）|
| **默认账号** | `admin` / `admin`（首次登录后必须改密码）|
| **管理入口** | `http://101.33.212.119:5180/admin`（如未跳到登录，浏览器手输）|
| **健康检查** | `http://101.33.212.119:5180/api/health` → `{"status":"ok","app":"StaffDeck"}` |
| **工作区** | `http://101.33.212.119:5180/workspace/gallery` |
| **架构** | 单进程（FastAPI 同端口提供 UI + API），Python venv 部署 |
| **技术栈** | Python 3.11+ FastAPI + React 18 + TypeScript + Vite + SQLite + OpenAI 兼容模型 |

---

## 💻 2. 硬件依赖

| 维度 | 最低 | 当前服务器 |
|---|---|---|
| CPU | 2 核 | 8 核 ✅ |
| 内存 | 1 GB | 30 GB ✅（StaffDeck 实测占 154MB，build 峰值 700MB） |
| 磁盘 | 500 MB | 174 GB 可用 ✅ |
| Python | 3.11+ | 3.12.3 ✅ |
| Node.js | 20+ | 22.23.1 ✅ |
| 模型服务 | OpenAI 兼容 | `https://api.minimaxi.com/v1` (MiniMax-M3) ✅ |

---

## 🚀 3. 一键部署（从 0 到 1，按顺序复制可跑）

### 前置检查
```bash
ss -tlnp 2>/dev/null | grep 5180  # 确认 5180 端口未被占用
df -h / | tail -1                  # 确认 / 盘有 1G+ 空间
python3 --version                  # 确认 3.11+
node --version                     # 确认 20+
```

### 步骤 1: 克隆代码（用 gh-proxy 加速）
```bash
cd /root/projects
git clone --depth 1 https://gh-proxy.com/https://github.com/OpenBMB/StaffDeck.git staffdeck
cd /root/projects/staffdeck
```

### 步骤 2: 创建 Python venv + 装依赖
```bash
cd /root/projects/staffdeck
python3 -m venv backend/.venv
backend/.venv/bin/pip install -U pip setuptools wheel
backend/.venv/bin/pip install -e "backend[dev]"
# 约 1-2 分钟
```

### 步骤 3: 装前端依赖 + 构建
```bash
cd /root/projects/staffdeck
npm --prefix frontend-enterprise config set registry https://registry.npmmirror.com
npm --prefix frontend-enterprise ci
npm --prefix frontend-enterprise run build
# 约 1-3 分钟（ci 完成后 build 仅 6-7 秒）
```

### 步骤 4: 写 .env（独立 SQLite + 端口 5180 + MiniMax-M3）
```bash
mkdir -p /root/projects/staffdeck/data /root/projects/staffdeck/logs
# 生成 APP_SECRET
SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(48))")

cat > /root/projects/staffdeck/backend/.env << EOF
APP_NAME="StaffDeck"
DATABASE_URL="sqlite:////root/projects/staffdeck/data/staffdeck.db"
APP_SECRET="${SECRET}"
DEMO_MODEL_BASE_URL="https://api.minimaxi.com/v1"
DEMO_MODEL_NAME="MiniMax-M3"
DEMO_MODEL_API_KEY="<你的_MiniMax-M3_API_Key>"
MODEL_THINKING_MODE=""
MODEL_THINKING_MODELS=""
TOOL_TIMEOUT_SECONDS="60"
TOOL_BASE_URL="http://localhost:5180"
CORS_ORIGINS="http://localhost:5180,http://127.0.0.1:5180"
GENERAL_SKILL_RUNTIME_PACKAGES="requests,httpx"
GENERAL_SKILL_RUNTIME_AUTO_INSTALL="true"
WECHAT_ILINK_BASE_URL="https://ilinkai.weixin.qq.com"
APP_PORT="5180"
SINGLE_PORT="1"
APP_HOST="0.0.0.0"
BACKEND_HOST="127.0.0.1"
BACKEND_PORT="5180"
ENTERPRISE_HOST="127.0.0.1"
ENTERPRISE_PORT="5180"
AUTO_RESTART="0"
EOF
```

### 步骤 5: 写 systemd user service（守护后台 + 开机自启）
```bash
mkdir -p /root/.config/systemd/user
cat > /root/.config/systemd/user/staffdeck.service << 'EOF'
[Unit]
Description=StaffDeck - Enterprise Digital Employee Platform (OpenBMB)
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/projects/staffdeck
Environment="APP_PORT=5180"
Environment="SINGLE_PORT=1"
Environment="APP_HOST=0.0.0.0"
Environment="BACKEND_HOST=127.0.0.1"
Environment="BACKEND_PORT=5180"
Environment="ENTERPRISE_HOST=127.0.0.1"
Environment="ENTERPRISE_PORT=5180"
Environment="AUTO_RESTART=0"
Environment="PATH=/root/projects/staffdeck/backend/.venv/bin:/root/.nvm/versions/node/v22.23.1/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/root/projects/staffdeck/backend/.venv/bin/python /root/projects/staffdeck/scripts/dev.py up
Restart=on-failure
RestartSec=5
StandardOutput=append:/root/projects/staffdeck/logs/staffdeck.stdout.log
StandardError=append:/root/projects/staffdeck/logs/staffdeck.stderr.log

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable staffdeck.service
systemctl --user start staffdeck.service
```

### 步骤 6: 验证（三维度）
```bash
# 1. 等 20-30 秒（首次启动要 npm run build）
sleep 30

# 2. 本机 health
curl http://127.0.0.1:5180/api/health
# 期望: {"status":"ok","app":"StaffDeck"}

# 3. 公网 health（模拟何大人访问）
curl http://101.33.212.119:5180/api/health

# 4. 公网 UI
curl -sL http://101.33.212.119:5180/workspace/gallery
# 期望: HTTP 200 + 607 bytes HTML
```

---

## 📂 4. 关键文件 / 目录

```
/root/projects/staffdeck/
├── backend/
│   ├── .venv/                      # Python 虚拟环境（约 250MB）
│   ├── .env                        # 关键配置（MiniMax-M3 key 在这里）
│   ├── app/                        # FastAPI 业务代码
│   ├── mock_servers/               # 本地 mock 服务
│   └── pyproject.toml              # 依赖声明
├── frontend-enterprise/
│   ├── node_modules/               # npm 依赖（约 500MB）
│   └── dist/                       # ✅ 构建产物（FastAPI 直接 serve）
├── scripts/
│   ├── dev.py                      # 统一 Python 生命周期入口
│   ├── dev_up.sh                   # 启动包装
│   └── dev_down.sh                 # 停止包装
├── data/
│   └── staffdeck.db                # SQLite 数据库（约 7MB 初始）
├── logs/
│   ├── staffdeck.stdout.log        # systemd stdout
│   └── staffdeck.stderr.log        # systemd stderr
├── .dev/
│   ├── supervisor.pid
│   ├── app.port
│   └── logs/                       # 应用实时日志
│       ├── app.log
│       ├── app.err.log
│       └── supervisor.log
└── design-qa.md                    # 设计文档
```

---

## ▶️ 5. 启动 / 停止 / 重启 / 状态

| 操作 | 命令 |
|---|---|
| **启动** | `systemctl --user start staffdeck.service` |
| **停止** | `systemctl --user stop staffdeck.service` |
| **重启** | `systemctl --user restart staffdeck.service` |
| **状态** | `systemctl --user status staffdeck.service` |
| **看日志（实时）** | `tail -f /root/projects/staffdeck/.dev/logs/app.log` |
| **看 supervisor 日志** | `tail -f /root/projects/staffdeck/.dev/logs/supervisor.log` |
| **手动前台** | `cd /root/projects/staffdeck && backend/.venv/bin/python scripts/dev.py up` |
| **手动停** | `cd /root/projects/staffdeck && backend/.venv/bin/python scripts/dev.py down` |

---

## 🔍 6. 验证（三维度已验证通过）

| 维度 | 期望 | 实际（2026-07-24 15:19 验证）|
|---|---|---|
| 本机 curl | `{"status":"ok","app":"StaffDeck"}` | ✅ HTTP 200, 1.2ms |
| 公网 IP curl | 同上 | ✅ HTTP 200, 9.5ms |
| 公网 UI | HTTP 200 | ✅ `/workspace/gallery` 200, 484ms |
| Dify | 不受影响 | ✅ 200 |
| Langfuse | 不受影响 | ✅ 200 |
| 端口 5180 | 0.0.0.0 监听 | ✅ LISTEN 0.0.0.0:5180 |
| 内存 | < 500MB | ✅ 154MB 稳态, 700MB 峰值（npm build 时） |
| SQLite | 数据创建 | ✅ 7.5MB 初始 |

---

## ⚠️ 7. 避坑指南（按时间倒序）

### 坑 1: Node.js 不在 systemd PATH
**现象**：`error: Node.js is not available on PATH`，service 一直 restart 循环
**根因**：Node.js 装在 nvm（`/root/.nvm/versions/node/v22.23.1/bin/`），systemd user service 启动时没有自动加载 nvm
**修法**：service file 的 `Environment="PATH=..."` **必须**包含 nvm 的 bin 路径（参考上面 service 模板）
**永久规则**：✅ systemd user service 调 Node/Python/npm/pnpm 都要在 PATH 显式声明
**详见**：`/root/.openclaw/workspace/MEMORY.md` §"🚨 2026-07-06 21:25 教训" / "systemd-run --user"

### 坑 2: systemd service file 改了要 daemon-reload
**现象**：改了 service file 但 `systemctl restart` 后还是旧配置
**修法**：每次改完 service file 必跑 `systemctl --user daemon-reload` 再 restart
**告警**：`Warning: The unit file, source configuration file or drop-ins of staffdeck.service changed on disk. Run 'systemctl --user daemon-reload' to reload units.`

### 坑 3: 首次启动要等 30-60 秒（npm run build）
**现象**：service 启了但端口还没起
**根因**：`scripts/dev.py up` 会自动 `npm run build`（构建前端 dist）
**修法**：等 30-60 秒，看 `.dev/logs/app.log` 有 `Uvicorn running on http://127.0.0.1:5180` 就好了

### 坑 4: 端口必须用 5180（不能 80）
**原因**：80 端口被现有 nginx `default_server` 占用（反代 Dify），StaffDeck 是 SPA 加 prefix 会破坏路由
**给何大人的 URL**：`http://101.33.212.119:5180/`（带端口，但无影响）

### 坑 5: AGPL-3.0 商用限制
**风险**：如果 StaffDeck 后续对外提供服务，整个后端代码必须开源
**当前状态**：✅ 仅内部使用，不触发 AGPL 开源义务
**如果未来要公网开放**：要么**不部署 StaffDeck**，要么接受开源义务

### 坑 6: SQLite 用绝对路径（不是相对路径）
**配置**：`DATABASE_URL="sqlite:////root/projects/staffdeck/data/staffdeck.db"`（4 个斜杠 = 绝对路径）
**默认**：`sqlite:///./skill_agent_loop.db`（3 斜杠 = 相对 cwd，dev.py 在 backend/ 跑就会建到 `backend/skill_agent_loop.db`，混乱）

---

## 📊 8. 当前状态（2026-07-24 15:19）

| 维度 | 状态 |
|---|---|
| **service** | ✅ active (running) 60s+ 稳定 |
| **Main PID** | 1390408（dev.py supervisor）|
| **uvicorn PID** | 1391686（实际服务）|
| **Tasks** | 12（systemd cgroup 限制内）|
| **Memory** | 154.8M 稳态 / 667.9M 峰值 |
| **Restart Count** | 0 |
| **Database** | `data/staffdeck.db` 7.5MB |
| **Logs** | `logs/staffdeck.{stdout,stderr}.log` + `.dev/logs/{app,app.err,supervisor}.log` |
| **下次维护** | 2026-08-07 复查 GitHub commits/issues |

---

## 🛑 9. 回滚 SOP（一键全删）

```bash
# 1. 停 service
systemctl --user stop staffdeck.service
systemctl --user disable staffdeck.service

# 2. 删 service
rm /root/.config/systemd/user/staffdeck.service
systemctl --user daemon-reload

# 3. 杀残留进程（如果有）
pkill -9 -f "staffdeck" 2>/dev/null
pkill -9 -f "uvicorn single_port_app" 2>/dev/null

# 4. 删项目目录
rm -rf /root/projects/staffdeck

# 5. 确认端口释放
ss -tlnp 2>/dev/null | grep 5180 && echo "❌ 端口还在" || echo "✅ 端口已释放"

# 6. 确认其他服务无影响
curl -s -o /dev/null -w "Dify: HTTP %{http_code}\n" http://101.33.212.119/install
curl -s -o /dev/null -w "Langfuse: HTTP %{http_code}\n" http://101.33.212.119:3000
```

**预计回滚时间**：< 2 分钟
**对其他服务影响**：零

---

## 🔗 10. 关联文档

- **可行性评估**：`/root/vault/current-server/from-agent/2026-07-24/2026-07-24 - 公众号-StaffDeck-一飞开源.md`
- **现有部署清单**：`/root/vault/current-server/开源软件访问清单.md`
- **当前服务器隔离规则**：`/root/vault/current-server/README.md`
- **Agent 收件处规则**：`/root/vault/current-server/from-agent/README.md`

---

**部署者**：小助 — OpenClaw (MiniMax-M3)
**部署时间**：2026-07-24 15:13-15:19（约 6 分钟部署 + 1 分钟 systemd 调优）
**触发者**：何大人 15:13 "现在就部署 但是保证不要影响现有的任何服务功能"
**承诺**：✅ **零影响部署**（Dify / Langfuse / RAGFlow / Yuxi / AgentSpace / Paperclip / Hermes 全验证 200 / Up 状态）
