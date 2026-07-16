# SDD-Project 部署文档

> **服务器部署**：2026-07-15，端口 5174/8010/9010/9011
> **公网访问**：`http://101.33.212.119:5174`（前端），`http://101.33.212.119:8010`（后端 API）

---

## 一、服务器端部署

### 架构

```
本地电脑浏览器
     ↓
┌─────────────────────────────────────────────────────┐
│              服务器 (101.33.212.119)                 │
│                                                     │
│  :5174  Vue3 Frontend                              │
│  :8010  Flask Backend Master                        │
│  :9010  Decision Service (Kimi LLM)                │
│  :9011  Executor (本地)                            │
│                                                     │
│  依赖已有服务: MySQL:3306, Redis:6379               │
└─────────────────────────────────────────────────────┘
```

### 端口规划

| 服务 | 端口 | 说明 |
|------|------|------|
| frontend | **5174** | Vue3 开发服务器 |
| backend | **8010** | Flask API |
| decision_service | **9010** | 决策服务 |
| executor | **9011** | 执行器节点 |

### 启停命令

```bash
# 查看状态
/root/workspace/SDD-project/start_sdd.sh status

# 停止
/root/workspace/SDD-project/start_sdd.sh stop

# 启动
/root/workspace/SDD-project/start_sdd.sh start
```

### 日志位置

```
/tmp/sdd/
├── decision.log   # Decision Service
├── backend.log    # Flask
├── celery.log     # Celery Worker
├── frontend.log  # Vite
└── executor.log   # Executor
```

### 验证

```bash
curl http://localhost:9010/health
curl http://localhost:8010/api/health
```

### 修改的配置（维护参考）

| 文件 | 修改内容 |
|------|---------|
| `backend/decision_service/mcp_server.py` | 改为读取 config.json 动态端口 |
| `backend/backend/flask_app.py` | 改为读取环境变量端口 |
| `backend/backend/config.local.json` | Kimi API Key 等配置 |
| `frontend/src/api.js` | API 地址 8000 → 8010 |
| `executor/config/executor.json` | 指向本机 8010/9011 |

---

## 二、本地 Windows 部署

> 本地部署连接**同一台服务器**的后端，不自己起数据库和 Redis。

### 2.1 前置依赖

**下载安装：**
- **Python 3.9+**：https://www.python.org/downloads/
- **Node.js 18+**：https://nodejs.org/
- **Git**：https://git-scm.com/download/win

安装时勾选 `Add Python to PATH`。

### 2.2 获取代码

```bash
# 克隆代码（在 D:\SDD-project 或任意目录）
git clone <仓库地址> SDD-project
cd SDD-project
```

### 2.3 安装后端依赖

```bat
:: 进入后端目录
cd backend\backend

:: 创建虚拟环境
python -m venv venv

:: 激活虚拟环境
venv\Scripts\activate

:: 安装依赖
pip install Flask>=3.0.0 requests>=2.31.0 psutil>=5.9.0 pymysql>=1.1.0 anthropic>=0.40.0 flask-cors celery redis gevent
```

### 2.4 配置后端

在 `backend\backend\` 目录下新建 `config.local.json`：

```json
{
  "KIMI_API_KEY": "你的Kimi API Key",
  "CLAUDE_PERMISSION_MODE": "bypassPermissions",
  "DECISION_SERVICE_URL": "http://101.33.212.119:9010",
  "AI_NATIVE_PORT": "8010"
}
```

### 2.5 启动 Backend

```bat
cd backend\backend
venv\Scripts\activate
set AI_NATIVE_DB_HOST=101.33.212.119
set AI_NATIVE_DB_PORT=3306
set AI_NATIVE_DB_USER=root
set AI_NATIVE_DB_PASSWORD=root
set AI_NATIVE_DB_NAME=sdd
python flask_app.py
```

看到 `Running on http://0.0.0.0:8010` 即成功，**不要关闭此窗口**。

### 2.6 安装前端依赖

新开一个命令行窗口：

```bat
cd frontend
npm install
```

### 2.7 修改前端 API 地址

打开 `frontend\src\api.js`，把 `localhost:8000` 替换为 `101.33.212.119:8010`：

```javascript
// 第 7 行
return 'http://101.33.212.119:8010'
// 第 10-13 行
if (!port || port === '8010') {
    return ''
}
return `${protocol}//101.33.212.119:8010`
```

### 2.8 启动前端

```bat
npm run dev -- --host 0.0.0.0 --port 5174
```

访问 **`http://localhost:5174`**（或 `http://101.33.212.119:5174` 从其他设备访问）。

### 2.9 Windows 一键启动脚本

在 `SDD-project` 根目录下新建 `start_local.bat`：

```bat
@echo off
chcp 65001 >nul
echo ================================
echo   SDD-Project 本地启动
echo ================================

:: 启动后端
echo [1/2] 启动后端 Backend...
start "SDD-Backend" cmd /k "cd /d %~dp0backend\backend && venv\Scripts\activate && set AI_NATIVE_DB_HOST=101.33.212.119 && set AI_NATIVE_DB_PORT=3306 && set AI_NATIVE_DB_USER=root && set AI_NATIVE_DB_PASSWORD=root && set AI_NATIVE_DB_NAME=sdd && python flask_app.py"

:: 等待后端启动
timeout /t 5 /nobreak >nul

:: 启动前端
echo [2/2] 启动前端 Frontend...
start "SDD-Frontend" cmd /k "cd /d %~dp0frontend && npm run dev -- --host 0.0.0.0 --port 5174"

echo.
echo 前端: http://localhost:5174
echo 后端: http://101.33.212.119:8010
echo.
pause
```

### 2.10 验证

```bat
:: 检查后端
curl http://localhost:8010/api/health

:: 检查决策服务（需服务器端已启动）
curl http://101.33.212.119:9010/health
```

---

## 三、架构总览

```
┌──────────────────────────────────────────────────────────────┐
│                     本地 Windows                              │
│   浏览器 http://localhost:5174                               │
│        ↓                                                      │
│   Flask Backend (localhost:8010)  ──────────────────────────│
│                                                      ↓       │
└──────────────────────────────────────────────────────────────┘
                                                               ↓
                                            ┌─────────────────────────────────┐
                                            │      服务器 101.33.212.119      │
                                            │                                 │
                                            │  :9010  Decision Service        │
                                            │  :3306  MySQL (sdd)             │
                                            │  :6379  Redis                   │
                                            │  :9011  Executor                │
                                            └─────────────────────────────────┘
```

---

## 四、数据库初始化（服务器端，只需执行一次）

```bash
mysql -uroot -proot -e "CREATE DATABASE IF NOT EXISTS sdd CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

cd /root/workspace/SDD-project/backend/backend/migrations
mysql -uroot -proot sdd < 001_init.sql
mysql -uroot -proot sdd < 002_phase1_pipeline.sql
mysql -uroot -proot sdd < 003_distributed.sql
mysql -uroot -proot sdd < 004_pipeline_config.sql
mysql -uroot -proot sdd < 005_add_executor_node.sql
```

---

## 五、常见问题

### 1. 后端连接数据库失败
```bat
set AI_NATIVE_DB_HOST=101.33.212.119
set AI_NATIVE_DB_PORT=3306
set AI_NATIVE_DB_USER=root
set AI_NATIVE_DB_PASSWORD=root
set AI_NATIVE_DB_NAME=sdd
```

### 2. 前端报 API 错误
确认 `frontend\src\api.js` 中已把所有 `8000` 替换为 `101.33.212.119:8010`。

### 3. Decision Service 不可用
确认服务器端 Decision Service（9010）已启动：
```bash
curl http://101.33.212.119:9010/health
```

### 4. Kimi/Claude API Key 无效
在 `backend\backend\config.local.json` 中填写真实 Key。

---

## 六、目录结构

```
SDD-project/
├── frontend/
│   ├── src/api.js              # API 地址配置
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── backend/
│   │   ├── flask_app.py         # Flask 入口
│   │   ├── config.local.json    # 本地配置（新建）
│   │   ├── config.py            # 配置读取
│   │   └── migrations/           # 数据库迁移 SQL
│   ├── decision_service/
│   │   ├── mcp_server.py        # 决策服务入口
│   │   └── config.json
│   └── executor/
│       ├── executor_agent.py
│       └── config/
│           └── executor.json
├── start_local.bat              # Windows 一键启动脚本（新建）
└── start_sdd.sh                 # 服务器启停脚本
```
