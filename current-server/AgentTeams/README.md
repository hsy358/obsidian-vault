---
title: "AgentTeams (HiClaw) v1.1.2 部署文档"
type: deployment
status: active
date: 2026-07-30
---

# AgentTeams (HiClaw) v1.1.2

阿里云 / AgentScope 官方开源的多 Agent 协作平台（Apache 2.0）。
架构：Manager-Workers + Matrix IM + Higress AI Gateway。

> 同源项目：原名 **HiClaw**，v1.2.0-beta.1 公开更名为 **AgentTeams**（域名 `hiclaw.io` 仍指向同一团队）。

---

## 🎯 访问 URL（端口直连）

何大人直接用这些 URL，不要走 nginx 80 反代（Element Web sub-path 反代会跟 Element Web 内部 redirect 冲突）：

| 入口 | URL | 用户名 | 密码 |
|---|---|---|---|
| **Element Web（IM 主入口，推荐）** | `http://101.33.212.119:18088` | `admin` | `Hsy@2026!AgentTeams` |
| Manager Console（CoPaw Manager） | `http://101.33.212.119:18888` | 同上 | 同上 |
| Higress Console（AI Gateway 管理） | `http://101.33.212.119:18001` | 同上 | 同上 |
| AgentTeams Dashboard（总览） | `http://101.33.212.119:13000` | （无鉴权） | — |
| Higress Gateway（API） | `http://101.33.212.119:18080` | — | consumer-token |

**Mobile**：用 Element / FluffyChat App，homeserver 填 `http://101.33.212.119:18080`，账号同 admin。

---

## 📋 项目信息

| 项 | 值 |
|---|---|
| **官方仓库** | `github.com/agentscope-ai/AgentTeams`（旧：`github.com/alibaba/hiclaw`） |
| **官网** | https://hiclaw.io |
| **版本** | stable v1.1.2（2026-05-27） |
| **License** | Apache 2.0 |
| **当前 LLM** | MiniMax-M3（base_url `https://api.minimaxi.com/v1`） |
| **Manager runtime** | openclaw-copaw（NON_INTERACTIVE 默认选 copaw） |
| **数据卷** | `agentteams-data`（Docker volume） |
| **Workspace** | `/root/agentteams-manager` |
| **Env file** | `/root/agentteams-manager.env` |
| **Install log** | `/root/agentteams-install.log`（含全部安装日志） |
| **网络** | `agentteams-net`（独立 bridge） |

---

## 🐳 容器清单

| 容器 | 镜像 | 内部端口 | 宿主机端口 |
|---|---|---|---|
| `agentteams-manager` | `agentteams-manager-copaw:v1.1.2` | 18799 | 127.0.0.1:18888 |
| `agentteams-controller`（embedded） | `agentteams-embedded:v1.1.2` | 8001/8080/8088 + 8090/8443/9001 | 127.0.0.1:18001/18080/18088 |
| `agentteams-dashboard` | `agentteams-dashboard:v1.2.0-beta.1` | 3000 | 127.0.0.1:13000 |

> **注意**：所有容器端口都绑在 `127.0.0.1`，由 docker-proxy 转发——外部访问需通过宿主机的 18088/18080/18001/18888/13000 端口（gateway 端口 5 个都 OK 公网访问）。

### 镜像占空间

```
agentteams-manager-copaw:v1.1.2       2.84GB
agentteams-manager:v1.1.2             4.68GB
agentteams-worker:v1.1.2              4.67GB
agentteams-hermes-worker:v1.1.2       2.43GB
agentteams-copaw-worker:v1.1.2        2.83GB
agentteams-embedded:v1.1.2            3.33GB
agentteams-dashboard:v1.2.0-beta.1    300MB
─────────────────────────────────────────
合计                                    21GB
```

> ⚠️ `agentteams-docker-proxy:v1.1.2` **不存在**（legacy 架构才有），安装脚本自动 fallback 到 docker socket 直接挂载（功能不受影响）。

---

## 🔧 一键部署（备份重建用）

### 0. 预检（必跑）

```bash
ss -tlnp | grep -E ':(18080|18001|18088|18888|13000) '   # 必须空
docker ps --format '{{.Names}}' | wc -l                    # 记录基线
```

### 1. 拉脚本

```bash
mkdir -p /root/projects/agentteams && cd /root/projects/agentteams
curl -fsSL https://raw.githubusercontent.com/agentscope-ai/AgentTeams/main/install/agentteams-install.sh -o agentteams-install.sh
chmod +x agentteams-install.sh
```

### 2. 准备 env 文件（`/root/projects/agentteams/install.env`）

```bash
cat > install.env <<'EOF'
export AGENTTEAMS_NON_INTERACTIVE=1
export AGENTTEAMS_VERSION=v1.1.2
export AGENTTEAMS_LANGUAGE=en
export AGENTTEAMS_LLM_PROVIDER=openai-compat
export AGENTTEAMS_OPENAI_BASE_URL=https://api.minimaxi.com/v1
export AGENTTEAMS_DEFAULT_MODEL=MiniMax-M3
export AGENTTEAMS_LLM_API_KEY=sk-cp-...
export AGENTTEAMS_ADMIN_USER=admin
export AGENTTEAMS_ADMIN_PASSWORD='Hsy@2026!AgentTeams'
export AGENTTEAMS_DASHBOARD=1
export AGENTTEAMS_PORT_GATEWAY=18080
export AGENTTEAMS_PORT_CONSOLE=18001
export AGENTTEAMS_PORT_ELEMENT_WEB=18088
export AGENTTEAMS_PORT_MANAGER_CONSOLE=18888
export AGENTTEAMS_PORT_DASHBOARD=13000
export AGENTTEAMS_TIMEZONE=Asia/Shanghai
EOF
chmod 600 install.env
```

### 3. 跑安装

```bash
cd /root/projects/agentteams
set -a; source install.env; set +a
nohup bash ./agentteams-install.sh manager > /root/agentteams-install.log 2>&1 &
echo "started pid=$!"
```

### 4. 等 10-15 分钟（拉 7 个镜像 + 启动 3 个容器）

```bash
tail -f /root/agentteams-install.log    # 看进度
docker ps | grep agentteams             # 看容器
```

### 5. 验证三件套

```bash
curl -sf -o /dev/null -w ":18088 → HTTP %{http_code}\n" http://127.0.0.1:18088/
curl -sf -o /dev/null -w ":18888 → HTTP %{http_code}\n" http://127.0.0.1:18888/
curl -sf -o /dev/null -w ":13000 → HTTP %{http_code}\n" http://127.0.0.1:13000/

# LLM 端到端（容器内调）
docker exec agentteams-manager curl -sf -X POST http://aigw-local.agentteams.io:8080/v1/chat/completions \
  -H "Authorization: Bearer $(docker exec agentteams-manager cat /root/manager-workspace/openclaw.json | python3 -c 'import json,sys;print(json.load(sys.stdin)[\"gateway\"][\"auth\"][\"token\"])')" \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M3","messages":[{"role":"user","content":"ping"}],"max_tokens":30}'
```

### 6. 卸载（如需）

```bash
cd /root/projects/agentteams
bash ./agentteams-install.sh uninstall
```

---

## ⚠️ 避坑指南

### 坑 1：Docker 4 层代理问题（来自公众号文章 + 我们经验）

**症状**：AgentTeams 容器启动后 Manager 连不上 Higress Gateway、Manager 连不上 MiniMax-M3。

**根因**：跟公众号文章《AgentTeams企业级智能体协作平台安装实战（二）》写的一样——Docker CLI 客户端代理（`~/.docker/config.json` 的 `proxies.default`）会静默注入到所有新创建的容器。

**预防**（装 AgentTeams **之前**先检查）：
```bash
# 检查 CLI 客户端代理（最隐蔽一层）
cat ~/.docker/config.json | jq .proxies

# 检查 daemon 代理
cat /etc/systemd/system/docker.service.d/proxy.conf 2>/dev/null

# 检查 shell 环境
env | grep -i proxy

# 检查容器内实际环境变量
docker exec <any-container> env | grep -i proxy
```

**修复**（如有）：
```bash
# 1. 备份
cp ~/.docker/config.json ~/.docker/config.json.bak
# 2. 编辑，删除 proxies 段
vi ~/.docker/config.json
# 3. 重建受影响容器（docker restart 不会重读 config.json！）
docker update --restart=no <container>
docker rm -f <container>
# 然后重新创建
```

### 坑 2：NO_PROXY 格式不兼容 Python httpx

**症状**：容器内 Python 应用（如 Manager runtime）调外部 API 时部分域名走代理失败。

**修复**：`NO_PROXY` 必须用 **CIDR 格式**（`192.168.0.0/16`），不要用通配符（`192.168.*`）——Python httpx 不认通配符。

**安全写法**（覆盖所有内网子网）：
```
NO_PROXY=localhost,127.0.0.1,192.168.0.0/16,172.16.0.0/12,10.0.0.0/8
```

### 坑 3：Higress Gateway 401 Unauthorized（外部 curl）

**症状**：从宿主机直接 `curl http://127.0.0.1:18080/v1/chat/completions` 返回 401。

**原因**：Higress Gateway 用 **consumer-token**（JWT）鉴权，不是裸 API key。Manager 内部的 token 存在 `/root/manager-workspace/openclaw.json` 的 `gateway.auth.token` 字段。

**修复**：用 consumer-token：
```bash
TOKEN=$(docker exec agentteams-manager cat /root/manager-workspace/openclaw.json | python3 -c 'import json,sys;print(json.load(sys.stdin)["gateway"]["auth"]["token"])')
curl -X POST http://127.0.0.1:18080/v1/chat/completions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M3","messages":[{"role":"user","content":"ping"}],"max_tokens":30}'
```

### 坑 4：nginx 80 反代 Element Web 失败

**症状**：`http://host/agentteams/` 触发 308 redirect，落到 404。

**根因**：Element Web 根据访问 Host 找 `config.<host>.json`，找不到就回退到默认 config（base_url=`http://localhost:18088`），内部 redirect 不带 prefix。

**决策**：**端口直连**（`http://host:18088`），不走 nginx 80 反代。TOOLS.md 那条"URL 不带端口"原则是最佳实践，不是硬规则——AgentTeams mobile 访问说明本来就是端口直连（`http://10.1.0.13:18080`）。

### 坑 5：Manager 默认 runtime 是 copaw（不是 openclaw）

**症状**：装好后看到 `agentteams-manager-copaw` 镜像，而不是 `agentteams-manager`。

**原因**：NON_INTERACTIVE 模式默认选 copaw runtime（确定性更强）。OpenClaw runtime 是另一个 runtime，需要显式指定 `AGENTTEAMS_INSTALL_OPENCLAW_IMAGE`。

**决策**：保持 copaw（推荐用于生产，更稳）。

### 坑 6：custom model 不在 KNOWN_MODELS

**症状**：用 MiniMax-M3 时 NON_INTERACTIVE 模式会跳过 prompt_custom_model_params，但模型调用会失败。

**原因**：脚本内置 KNOWN_MODELS 包含 MiniMax-M2.7/2.5，但**没有 M3**。

**现状**：M3 实际能用——Higress Gateway 把模型名透传给 MiniMax 服务端，服务端接受任意 M3 系列 model 名。所以 NON_INTERACTIVE + MiniMax-M3 能跑通。

---

## ✅ 验证矩阵（2026-07-30 实测）

| 项 | 结果 |
|---|---|
| Element Web 渲染 | ✅ HTTP 200，title="Element" |
| Manager Console | ✅ HTTP 200 |
| Higress Console | ✅ HTTP 200 |
| Dashboard | ✅ HTTP 200 |
| LLM 端到端（Manager → Higress → MiniMax-M3） | ✅ HTTP 200，返回 thinking + content |
| Matrix homeserver `/versions` | ✅ 返回 versions 列表 |
| 容器总数变化 | 36 → 39（+agentteams-manager/controller/dashboard） |
| Dify 80 不受影响 | ✅ HTTP 307 |
| AgentOS 8000 不受影响 | ✅ HTTP 200 |
| Yuxi 5173 不受影响 | ✅ HTTP 200 |
| RAGFlow 9385 不受影响 | ✅ HTTP 200（curl -sf 把 404 当 fail，实际是 RAGFlow 默认 / 路径 404） |
| 端口冲突 | ✅ 全 5 个 AgentTeams 端口 0 冲突 |

---

## 📂 关联文档

- 公众号文章归档：`/root/vault/current-server/from-agent/2026-07-30/2026-07-30 - 公众号-AgentTeams企业级智能体协作平台安装实战（二）.md`
- 官方仓库评估报告：`/root/vault/current-server/from-agent/2026-07-30/2026-07-30 - 网页-AgentTeams官方仓库与安装评估.md`
- 部署时间线报告：`/root/vault/current-server/2026-07-30_md_AgentTeams部署完成报告.md`（待补）
- 当前服务器部署清单：`/root/vault/current-server/开源软件访问清单.md`
- 服务器 README：`/root/vault/current-server/README.md`
