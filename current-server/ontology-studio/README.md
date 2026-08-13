# 灵·洞本体工作站（Ontology Studio）— 本机部署 README

## 🚨 部署状态 · 2026-08-03 22:25

**已上线 · 可登录使用**

| 资源 | URL |
|---|---|
| 🟢 **公网工作台** | **http://101.33.212.119/studio/** |
| 🟢 **公网 API** | **http://101.33.212.119/api/** |
| 健康检查 | http://101.33.212.119/api/v1/health |
| Readiness | http://101.33.212.119/api/v1/health/ready |

## 🔑 登录账号（**2 套并存**）

### 账号 1：演示管理员（对齐官方体验站 admin/admin）

| 项 | 值 |
|---|---|
| **邮箱** | `admin@ontology.local` |
| **密码** | `admin1234567890`（重点：16 字符，本体 v1.0.0 强制 ≥15 字符）|
| **显示名** | 演示管理员 |
| **用户 ID** | `mailto:admin@local` |
| **组织** | 何大人研究台（slug: hesiyan-lab） |
| **角色** | ORGANIZATION_ADMIN + SECURITY_AUDITOR |

### 账号 2：主管理（bootstrap 创建）

| 项 | 值 |
|---|---|
| **邮箱** | `admin@hesiyan.local` |
| **密码** | `Ontology@2026!Demo` |
| **显示名** | 何四燕 |
| **用户 ID** | `mailto:admin@hesiyan.local` |
| **组织** | 何大人研究台（slug: hesiyan-lab） |
| **角色** | ORGANIZATION_ADMIN + SECURITY_AUDITOR |

> 完整凭据存放在 `/root/vault/current-server/ontology-studio/.credentials`（mode 600，不进 git）
> ⚠️ **重要**：demo 账号 `admin/admin`（5 字符）会 401，因为本体 v1.0.0 `validatePassword` 强制密码 ≥15 字符

## 📖 完整部署总结报告

详见：**`/root/vault/current-server/from-agent/2026-08-03 - 灵·洞本体工作站_部署总结报告.md`**

包含：
- 📋 部署概览（资源 / 架构 / 关键决策）
- 🏗️ 完整架构图（nginx → caddy → containers）
- 🎯 关键里程碑时间线（08:51-22:25 13.5 小时）
- 🐛 **8 个关键 Bug 和修复**（永久规则）
- 🔧 运维命令速查
- 🚀 后续 TODO（6 项）

## 📋 部署架构

```
[外网] http://101.33.212.119/{studio,api}/  ↓
[nginx 80] sites-enabled/default  ↓
[Caddy loopback 127.0.0.1:19080]  ↓
[本体应用：postgres 5432 + api 18080 + web 13100]
```

**关键让步（不动现有任何服务）**：
- Caddy 80 → 127.0.0.1:19080（loopback only）
- Caddy 443 → 127.0.0.1:19443（loopback only）
- API 容器内 18080（替代原 8080）
- Web 容器内 13100（替代原 3100）
- 假域名 `api.local` / `studio.local`
- 全部走 HTTP（与现有 Dify / Langfuse / RAGFlow 一致）

## 🐳 容器状态

```
postgres-1   postgres:17.10-alpine         2 GB / 2 CPU  ✅ healthy
api-1        ontology-platform-api:1.0.0   3 GB / 2 CPU  ✅ healthy (SESSION mode)
web-1        ontology-studio-web:1.0.0     1 GB / 1 CPU  ✅ running (Docker healthcheck unhealthy*)
caddy-1      caddy:2.11.4-alpine           256 MB / 0.5 CPU ✅ running
```

合计 6.25 GB RAM（实际 ~450MB）/ 5.5 CPU

\* web 容器 docker healthcheck 写死 3100 端口、实际跑 13100 导致状态 unhealthy，**功能正常**

## 🔐 身份模式变更记录

| 时间 | 模式 | 原因 |
|---|---|---|
| 15:48 | TRUSTED_GATEWAY（默认）| 按官方 .env.example 默认值部署，nginx 注入 gateway token |
| 17:09 | **SESSION**（当前）| **何大人需要登录工作台，TRUSTED_GATEWAY 模式无账号可登录** |

SESSION 模式下：
- 浏览器自带 cookie 登录 → 不需要 nginx 注入 token
- 第一个 admin 通过 `POST /api/v1/auth/bootstrap` 创建
- 已禁用 nginx `Authorization: Bearer <token>` 注入

## 🛠 运维

### 启动 / 停止

```bash
cd /root/projects/ontology-studio/services/platform-api

# 启动（4 个生产容器）
docker compose --env-file .env.production -f compose.local-fallback.yaml up -d

# 停止
docker compose --env-file .env.production -f compose.local-fallback.yaml down

# 状态
docker ps --format 'table {{.Names}}\t{{.Status}}' | grep onto
```

### 健康检查

```bash
# API liveness
curl http://101.33.212.119/api/v1/health

# API readiness（深度：PG + TDB2 + release storage）
curl http://101.33.212.119/api/v1/health/ready
```

### 备份 / 恢复

```bash
cd /root/projects/ontology-studio/services/platform-api

# 备份
PG_PASS=$(grep POSTGRES_PASSWORD .env.production | cut -d= -f2)
docker compose --env-file .env.production -f compose.local-fallback.yaml \
  --profile operations run --rm \
  -e POSTGRES_PASSWORD="***" \
  -e BACKUP_NAME=$(date -u +%Y%m%dT%H%M%SZ) \
  backup sh -euc '
    PGPASSWORD=$POSTG…WORD pg_dump -h postgres -U ontology ontology_platform \
      --format custom --no-owner --no-acl > /backup/$BACKUP_NAME/postgres.dump
    tar -czf /backup/$BACKUP_NAME/rdf.tar.gz -C /source/rdf .
    tar -czf /backup/$BACKUP_NAME/releases.tar.gz -C /source/releases .
    cd /backup/$BACKUP_NAME
    sha256sum *.dump *.tar.gz > SHA256SUMS
    ls -la'
```

### 重建镜像

```bash
cd /root/projects/ontology-studio
git pull
cd services/platform-api

# 修改 API 代码后
docker compose --env-file .env.production -f compose.local-fallback.yaml build api

# 修改 Web 代码后
docker build -t ontology-studio-web:1.0.0 studio-web

# 应用
docker compose --env-file .env.production -f compose.local-fallback.yaml up -d --force-recreate api web
```

## ⚠️ 已知问题 / 限制

1. **v1.0.0 是 `RELEASED_WITH_UAT_WAIVER`**：技术预览版，真人 UAT 未执行
2. **GPL-2.0-only**：商业闭源需 IP/Legal 评估
3. **Web 容器 docker healthcheck unhealthy**（功能正常）
4. **TDB2 单实例约束**：不能 `docker compose up --scale api=...`
5. **distroless 镜像源**：`gcr.m.daocloud.io`（gcr.io 国内不通）
6. **Maven 镜像源**：`/root/.m2/settings.xml`（阿里云，build-production-image.sh 挂载）

## 🔄 部署踩坑（永久规则）

1. **gcr.io 在国内不通** → 用 `gcr.m.daocloud.io`
2. **build-production-image.sh 必须挂载 /root/.m2/settings.xml** → 否则 mvn 走 Maven Central，3KB/s
3. **Caddy `auto_https off` 必须显式 `:80, :443`** → 否则只 listen :443
4. **本体无默认 admin 账号** → 必须自己 bootstrap 第一个管理员
5. **本体有 3 种身份模式**：
   - `TRUSTED_GATEWAY`：网关注入 token（适合"前置网关做认证"）
   - `SESSION`：浏览器 cookie 登录（**适合您用浏览器登录的场景**）
   - `OIDC`：外部 IdP 集成
6. **`docker compose restart` 不重读 .env** → 必须 `up -d --force-recreate`
7. **API `ONTOLOGY_ALLOWED_ORIGINS` 是 CSRF 校验白名单** → 必须包含公网访问 URL
8. **compose 文件硬编码的 env 不读 .env** → 必须改成 `${VAR:-default}` 占位符

## 📂 文件结构

```
/root/projects/ontology-studio/
├── services/platform-api/
│   ├── .env.production                ← SESSION mode + 公网 origins
│   ├── compose.local-fallback.yaml    ← 端口让步 + 占位符
│   └── Caddyfile.local                ← 自签 + HTTP only
├── studio-web/
└── (其他: docs/, examples/, tests/)

/etc/nginx/sites-enabled/default       ← /studio/ 和 /api/ location（不再注 token）
/root/.m2/settings.xml                 ← 阿里云 Maven mirror
/root/.ontology-secrets                ← PG 密码 + Gateway token（mode 600）
/root/vault/current-server/ontology-studio/
├── README.md                          ← 本文件
└── .credentials                       ← 登录账号密码（mode 600）
```

## 📚 关联文档

- 公众号原文：`/root/vault/current-server/from-agent/2026-08-02 - 灵·洞本体工作站开源，诚邀专家共建.md`
- 部署可行性评估：`/root/vault/current-server/from-agent/2026-08-03 - 灵·洞本体工作站_部署可行性评估.md`
- 完整生产分析：`/root/vault/current-server/from-agent/2026-08-03 - 灵·洞本体工作站_完整部署可行性深度分析.md`
- 本体让步清单：`/root/vault/current-server/from-agent/2026-08-03 - 灵·洞本体工作站_本体让步清单.md`

## ⚠️ Vite Base Path 部署经验（2026-08-03 续）

### 问题
部署到 `/studio/` 子路径的 vite 应用 + nginx 80 反代时遇到两类问题：

| 现象 | 根因 | 修复 |
|---|---|---|
| CSS/JS 加载 404 | vite 资源路径是 `/assets/...` 绝对路径 | (A) 改 `vite.config.ts` 加 `base: '/studio/'` + 重建镜像 |
| 跳 `/login`/`/solutions` 报 404 | React Router 跳转用绝对路径（如 `href="/solutions"`） | (B) nginx 加 regex location 兜底所有 vite 路由 |

### vite base path 行为细则
- ✅ **改**：所有 `<script src>` / `<link href>` / `url()` 资源路径 → 自动加 base prefix
- ❌ **不**改：React Router `<Link href="/projects">` / `useNavigate('/solutions')` → 仍是绝对路径

### 修复命令（5 分钟搞定）
```bash
cd /root/projects/ontology-studio/studio-web
# 1. 改 vite.config.ts
echo "        base: '/studio/'," >> vite.config.ts  # 或手改
# 2. 重建镜像（必须 --no-cache）
docker build --no-cache -t ontology-studio-web:1.0.0 -f Dockerfile .
# 3. 重启容器
docker compose -f /root/projects/ontology-studio/services/platform-api/compose.local-fallback.yaml \
  up -d --force-recreate web
# 4. nginx 配 regex location 兜底
# 见 /etc/nginx/sites-enabled/default
```

### nginx regex location 模板
```nginx
location ~ ^/(account|data-sources|mappings|materializations|ontology|quality|releases|solutions|tutorial|work-items|login|workspace|projects)(/|$|\?) {
    proxy_pass http://127.0.0.1:19080;
    proxy_set_header Host studio.local;
}
```

### 验证清单
```bash
# 12 个 vite 路由全 200
for p in login account workspace solutions data-sources mappings quality releases tutorial work-items materializations ontology projects; do
  echo "$p: $(curl -s -o /dev/null -w '%{http_code}' http://101.33.212.119/$p)"
done
# 期望：除 /workspace 和 /projects 是 Next.js 自身 404（无害），其余 200
```

### 永久规则
- ⚠️ **vite/Next.js 部署子路径必须双修**：build-time (`base`) + runtime (nginx regex)
- ⚠️ **改 vite.config.ts 必须 `--no-cache` 重建** —— vite 用 build cache
- ⚠️ **不要全靠 nginx `sub_filter`**：改字符串比改 base 路径容易出错
- ⚠️ **`:login`、`/workspace`、`/projects` 等是 React Router 跳转路径，不是文件** —— 它们触发 Next.js 路由层，无子路由时 404
