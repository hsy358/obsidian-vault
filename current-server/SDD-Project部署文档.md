# SDD-Project 部署文档

## 系统架构

```
┌─────────────────────────────────────────────────────┐
│                    前端 (Vue3)                       │
│               http://IP:5173                        │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP
┌──────────────────────▼──────────────────────────────┐
│              Backend Master (Flask)                  │
│                   port 8000                          │
│  /api/*                                            │
└──────┬──────────────┬──────────────┬────────────────┘
       │              │              │
       ▼              ▼              ▼
┌────────────┐  ┌──────────┐  ┌────────────────────────┐
│ Decision   │  │  MySQL   │  │   Executor (Node)       │
│ Service   │  │  sdd DB  │  │   port 9001             │
│ port 9000 │  │ port 3306│  │  (可选，分布式部署)      │
│ (Kimi LLM)│  │          │  │                         │
└────────────┘  └──────────┘  └────────────────────────┘
                    │
               ┌────▼────┐
               │  Redis  │
               │ port 6379│
               └─────────┘
```

## 端口规划

| 服务 | 端口 | 说明 |
|------|------|------|
| frontend | 5173 | Vue3 开发服务器 |
| backend | 8000 | Flask API + WebSocket |
| decision_service | 9000 | 决策服务（Kimi LLM） |
| executor | 9001 | 执行器节点（可选独立部署） |

## 前置依赖

已在服务器运行的服务（**无需重新安装**）：
- MySQL `127.0.0.1:3306`（root/root，数据库 `sdd`）
- Redis `127.0.0.1:6379`
- Node.js / npm

**需要准备：**
- Kimi API Key（用于决策服务）
- Claude API Key（用于代码生成）

---

## 部署步骤

### 一、数据库初始化

**1.1 创建数据库**

```sql
CREATE DATABASE IF NOT EXISTS sdd CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**1.2 执行数据库迁移**

```bash
cd /root/workspace/SDD-project/backend/backend/migrations
mysql -uroot -proot sdd < 001_init.sql
mysql -uroot -proot sdd < 002_phase1_pipeline.sql
mysql -uroot -proot sdd < 003_distributed.sql
mysql -uroot -proot sdd < 004_pipeline_config.sql
mysql -uroot -proot sdd < 005_add_executor_node.sql
```

> 如迁移文件不存在或格式不同，也可由后端启动时自动执行。

---

### 二、Backend 部署

**2.1 安装依赖**

```bash
cd /root/workspace/SDD-project/backend

# Python 虚拟环境
python3 -m venv venv
source venv/bin/activate

# 后端核心依赖
pip install Flask>=3.0.0 requests>=2.31.0 psutil>=5.9.0 pymysql>=1.1.0 anthropic>=0.40.0 flask-cors celery redis

# 决策服务依赖
cd decision_service
pip install flask>=2.3.0 requests>=2.31.0 aiohttp>=3.8.0
cd ..
```

**2.2 配置 config.local.json**

```bash
vim /root/workspace/SDD-project/backend/backend/config.local.json
```

内容：

```json
{
  "KIMI_API_KEY": "your-kimi-api-key",
  "CLAUDE_PERMISSION_MODE": "bypassPermissions",
  "DECISION_SERVICE_URL": "http://127.0.0.1:9000"
}
```

环境变量也可覆盖：

```bash
export AI_NATIVE_DB_HOST="127.0.0.1"
export AI_NATIVE_DB_PORT="3306"
export AI_NATIVE_DB_USER="root"
export AI_NATIVE_DB_PASSWORD="root"
export AI_NATIVE_DB_NAME="sdd"
export AI_NATIVE_PORT="8000"
```

**2.3 启动 Backend Master**

```bash
cd /root/workspace/SDD-project/backend/backend
source ../venv/bin/activate
python flask_app.py
```

日志出现 `Running on http://0.0.0.0:8000` 即成功。

**2.4 启动 Celery Worker（异步任务）**

```bash
cd /root/workspace/SDD-project/backend/backend
source ../venv/bin/activate
celery -A celery_config.celery_app worker --loglevel=info -P gevent -c 4 &
```

---

### 三、Decision Service 部署

```bash
cd /root/workspace/SDD-project/backend/decision_service

# 决策服务依赖（独立 venv 或复用 backend venv）
pip install flask>=2.3.0 requests>=2.31.0 aiohttp>=3.8.0

# 配置 Kimi API Key
export KIMI_API_KEY="your-kimi-api-key"

# 启动
python mcp_server.py
```

服务监听 `0.0.0.0:9000`。

---

### 四、Frontend 部署

**4.1 安装依赖**

```bash
cd /root/workspace/SDD-project/frontend
npm install
```

**4.2 配置后端地址**

如前端无法访问 `localhost:8000`，修改 `src/api.js` 中的 `apiBase`：

```javascript
// 开发环境 Vite 代理，或直接写死：
const apiBase = 'http://<服务器IP>:8000'
```

**4.3 启动前端**

```bash
npm run dev -- --host 0.0.0.0
```

访问 `http://<服务器IP>:5173`

---

### 五、Executor 部署（可选）

Executor 可与 Master 部署在同一机器，也可单独部署在局域网其他机器上。

**5.1 安装依赖**

```bash
cd /root/workspace/SDD-project/executor
pip install -r requirements.txt  # Flask requests psutil pymysql
```

**5.2 配置 executor.json**

```bash
cp config/executor.example.json config/executor.json
vim config/executor.json
```

关键配置：

```json
{
    "executor_id": "exec-node-1",
    "master_url": "http://<Master服务器IP>:8000",
    "endpoint": "http://<本机IP>:9001",
    "server": {
        "host": "0.0.0.0",
        "port": 9001
    },
    "supported_ide": ["claude_code", "trae", "cursor"],
    "workspace": {
        "root": "./executor_workspace"
    },
    "heartbeat": {
        "interval_seconds": 30
    }
}
```

> - `master_url`：Master 的地址（前端调用的那个地址）
> - `endpoint`：Master 回调 Executor 的地址（如有 NAT 需填写公网/可通地址）
> - Executor 会每 30 秒向 Master 发送心跳，超过 120 秒无心跳则 Master 认为其离线

**5.3 启动 Executor**

```bash
python executor_agent.py --config config/executor.json
```

---

## 启动汇总（一键脚本）

```bash
#!/bin/bash
set -e

# 1. 启动 Decision Service (后台)
cd /root/workspace/SDD-project/backend/decision_service
source ../../venv/bin/activate
python mcp_server.py &
DECISION_PID=$!

# 2. 启动 Backend
cd /root/workspace/SDD-project/backend/backend
source ../../venv/bin/activate
python flask_app.py &
BACKEND_PID=$!

# 3. 启动 Celery Worker
source ../../venv/bin/activate
celery -A celery_config.celery_app worker --loglevel=info -P gevent -c 4 &
CELERY_PID=$!

# 4. 启动 Frontend
cd /root/workspace/SDD-project/frontend
npm run dev -- --host 0.0.0.0 &
FRONTEND_PID=$!

echo "Decision Service: PID $DECISION_PID (port 9000)"
echo "Backend Master:   PID $BACKEND_PID (port 8000)"
echo "Celery Worker:    PID $CELERY_PID"
echo "Frontend:         PID $FRONTEND_PID (port 5173)"
echo ""
echo "停止所有服务: kill $DECISION_PID $BACKEND_PID $CELERY_PID $FRONTEND_PID"
```

---

## 验证部署

```bash
# Decision Service
curl http://localhost:9000/health

# Backend Master
curl http://localhost:8000/api/health

# 查看在线执行器
curl http://localhost:8000/api/executor-nodes
```

---

## 常见问题

### 1. 数据库连接失败
检查 `config.local.json` 中的数据库配置，或设置环境变量：
```bash
export AI_NATIVE_DB_HOST="127.0.0.1"
export AI_NATIVE_DB_USER="root"
export AI_NATIVE_DB_PASSWORD="root"
```

### 2. Decision Service 不可用
Backend 启动时会连接 `http://127.0.0.1:9000`，确认决策服务先启动。

### 3. Executor 无法注册
- 检查 Master 地址是否可通
- 检查防火墙是否开放 `9001` 端口
- 如 Executor 在 NAT 后，需确保 Master 能通过 `endpoint` 回调到 Executor

### 4. Kimi/Claude API Key 无效
在 `config.local.json` 或环境变量中配置正确 Key。

---

## 目录结构

```
/root/workspace/SDD-project/
├── frontend/                      # Vue3 前端
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── backend/
│   │   ├── flask_app.py          # Flask 入口
│   │   ├── config.local.json     # 本地配置
│   │   ├── config.py             # 配置读取
│   │   ├── migrations/           # 数据库迁移 SQL
│   │   └── ...                   # 业务模块
│   ├── decision_service/
│   │   ├── mcp_server.py         # 决策服务入口
│   │   └── config.json
│   ├── executor/                  # 执行器（可独立部署）
│   │   ├── executor_agent.py
│   │   └── config/
│   │       └── executor.json
│   └── scripts/
│       └── start_all.sh
└── ...
```
