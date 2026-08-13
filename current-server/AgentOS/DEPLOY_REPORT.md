# Agno AgentOS 部署报告

**部署时间**：2026-07-25 17:13 CST
**部署人**：小助（OpenClaw agent, 何大人授权）
**目标**：在 101.33.212.119 上跑 Agno AgentOS（agno-agi/agentos-docker），零影响现有服务
**关联 README**：`/root/vault/current-server/AgentOS/README.md`
**关联分析**：`/root/vault/current-server/from-agent/2026-07-25/2026-07-25 - 网页-Agno部署分析.md`

---

## 🎉 最终结果

✅ **部署成功，公网可访问**

| 指标 | 值 |
|---|---|
| 公网 URL | `http://101.33.212.119:8001` |
| 反代 | nginx :8001 → agentos-api :8000 |
| 容器 | `agentos-api` (8000) + `agentos-db` (5435) |
| LLM | MiniMax（OpenAI 兼容协议）`MiniMax-Text-01` |
| LLM 延迟 (TTFT) | 0.46 - 0.97s |
| LLM 完整响应 | 1.5 - 1.8s |
| 现有服务影响 | **零干扰**（Dify/Langfuse/OnlyOffice 等 200 OK 不变） |

---

## 🔑 关键决策与坑（每个坑都解决过一次）

### 坑 1：DB 端口冲突 → host 端口 5435

**问题**：宿主 5432 已有 host PG16（Langfuse/Dify 共享），5433 已有 guyu postgres 容器
**解决**：compose.yaml 把 host 端口改 5435，容器内仍 5432。容器间用 `agentos-db:5432` 访问
**位置**：`/root/projects/agnos/compose.yaml` `agentos-db.ports: "5435:5432"`

### 坑 2：OpenAIResponses 模型 MiniMax 不支持 → 换 OpenAIChat

**问题**：agno 默认 `OpenAIResponses(id="gpt-5.6-sol")` 走 Responses API（gpt-5 专属协议），MiniMax 只支持 Chat Completions
**解决**：改 `app/settings.py` 用 `OpenAIChat`，model id 从 env `AGNO_MODEL_ID` 读
**位置**：
- `/root/projects/agnos/app/settings.py`：`OpenAIChat(id=..., timeout=600)`
- `/root/projects/agnos/.env`：`AGNO_MODEL_ID=MiniMax-Text-01`

### 坑 3：API hang 30s+ → uvicorn `--reload` 与 SSE 冲突 🎯 **最难发现**

**现象**：
- 容器内 `curl 127.0.0.1:8000/agents/web-search/runs` → 15s timeout，hang 在 `ModelRequestStarted` 后
- 容器内 `python httpx ASGITransport` → 5.94s 完整 21 个事件 ✅
- 容器内 `agent.arun(stream=True)` 直接调 → 5.71s 完整 8 个事件 ✅

**根因**：uvicorn `--reload` 模式下，stat reload watcher 与 SSE chunked transfer 交互，会导致 stream chunks 卡死。

**验证方法**：
1. 用 ASGI httpx 直连 → 工作（绕过 uvicorn HTTP 层）
2. 用真实 curl 走 uvicorn → hang
3. 差异 100% 在 uvicorn HTTP 层

**解决**：compose.yaml `command` 去掉 `--reload --reload-dir ...`
**修改前**：
```yaml
command: >
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  --reload-dir agents --reload-dir app --reload-dir db --reload-dir evals --reload-dir workflows
```
**修改后**：
```yaml
command: >
  uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**教训**：生产/部署场景永远不要用 `--reload`，开发场景调试 SSE 流式响应也要注意。

### 坑 4：nginx 反代 SSE 必须 proxy_buffering off

**现象**：如果 `proxy_buffering on`（默认），SSE chunks 会被 nginx 缓冲，client 看到 1.5s 后突然所有 chunks 一次性 flush —— 重现 hang 现象

**解决**：nginx site 必须配置
```nginx
proxy_buffering off;
proxy_cache off;
proxy_read_timeout 300s;
proxy_send_timeout 300s;
```

**位置**：`/etc/nginx/sites-available/agentos.conf`

---

## 📁 关键文件清单

### 部署目录：`/root/projects/agnos/`（注意拼写 typo，"agnos" 不是 "agentos"）

```
/root/projects/agnos/
├── compose.yaml          ← 已改：去掉 --reload，DB 端口 5435
├── Dockerfile            ← 已改：debian apt mirror 清华源
├── .env                  ← MiniMax 配置 + DB_PASS + MCP_CONNECT_SECRET + RUNTIME_ENV=dev
├── app/
│   ├── main.py           ← AgentOS 入口（含 MCP auth + scheduler + tracing）
│   ├── settings.py       ← default_model() = OpenAIChat(MiniMax-Text-01, timeout=600)
│   ├── config.yaml
│   ├── registry.py       ← Registry + ParallelTools/MCPTools
│   └── schedules.py
├── agents/
│   ├── web_search.py     ← web-search agent (MCPTools: parallel.ai)
│   ├── agent_builder.py  ← agent-builder agent (31 tools)
│   └── platform_manager.py
├── db.py                 ← Postgres DB + pgvector
├── workflows/
│   ├── deployment_check.py
│   └── run_evals.py
└── evals/
```

### 配置修改总结

| 文件 | 修改 |
|---|---|
| compose.yaml | DB 端口 5432→5435；去掉 uvicorn `--reload` 和 `--reload-dir` |
| .env | `OPENAI_BASE_URL=https://api.minimaxi.com/v1`，`OPENAI_API_KEY=<MiniMax key>`，`AGNO_MODEL_ID=MiniMax-Text-01`，`DB_USER/PASS/DATABASE=agentos`，`MCP_CONNECT_SECRET=<set>`，`RUNTIME_ENV=dev`，`AGENTOS_URL=http://127.0.0.1:8000` |
| app/settings.py | `OpenAIResponses` → `OpenAIChat` + `timeout=600`（env 可覆盖） |
| Dockerfile | debian apt mirror → tsinghua（默认源 404） |

### Nginx 配置

- `/etc/nginx/sites-available/agentos.conf`：新建（8001 端口 + SSE 必需配置）
- `/etc/nginx/sites-enabled/agentos.conf`：symlink
- `/etc/nginx/sites-enabled/default`：**未动**（Dify/OnlyOffice/zhishiku/cspaicser 等依赖它）

### Vault 归档

- `/root/vault/current-server/AgentOS/README.md`（部署手册）
- `/root/vault/current-server/AgentOS/DEPLOY_REPORT.md`（本文）
- `/root/vault/current-server/from-agent/2026-07-25/2026-07-25 - 网页-Agno部署分析.md`（GitHub 技术分析）

---

## 🧪 部署验证矩阵

### 容器状态
```
agentos-api    Up 4 minutes    0.0.0.0:8000->8000/tcp
agentos-db     Up 3 hours (healthy)    0.0.0.0:5435->5432/tcp
```

### 公网 endpoints（http://101.33.212.119:8001）

| Path | 期望 | 实际 |
|---|---|---|
| `/health` | 200 JSON | ✅ `{"status":"ok","instantiated_at":"2026-07-25T08:55:15.318688Z"}` |
| `/docs` | 200 Swagger UI | ✅ 1006 bytes |
| `/agents` | 200 JSON 数组 | ✅ 3 agents |
| `/config` | 200 | ✅ |
| `/mcp` | 401 (MCP OAuth) | ✅ |

### 3 个 agent stream 测试（POST /agents/{id}/runs，stream=true）

| Agent | input_tokens | output_tokens | duration | TTFT | 结果 |
|---|---|---|---|---|---|
| web-search | 2259 | 23 | 1.51s | 0.46s | ✅ 完整 6 个 events |
| agent-builder | 5024 | 16 | 1.54s | 0.83s | ✅ 完整 6 个 events |
| platform-manager | 2170 | 17 | 1.57s | 0.58s | ✅ 完整 6 个 events |

### 现有服务零干扰

| 服务 | URL | code |
|---|---|---|
| Dify | `http://101.33.212.119/install` | 200 ✅ |
| Langfuse | `http://101.33.212.119:3000` | 200 ✅ |
| OnlyOffice | `http://101.33.212.119:8443` | 302 ✅ |
| RAGFlow | `http://101.33.212.119:9385` | （防火墙未暴露，从一开始就这样） |

---

## 🎁 顺手收获

### OpenClaw gateway 工具死锁再次发生（教训复读）
- 事件：午后 14:00-14:36 工具层 exec/read/write 间歇性 hang
- 根因：参考 MEMORY.md "2026-07-06 20:50 教训"
- 修复：何大人手动 `systemctl --user restart openclaw-gateway.service`
- 永久规则：**绝对不让 exec 返回 >10k 字符**（必先 redirect 到 /tmp）

### 公网安全观察
- 日志显示公网暴露后有外部 IP 扫描（shadowserver.org, ipify.org 等）
- **不是攻击**，是常态噪音（公开 IP 都会被扫）
- **待办**：是否要加 fail2ban 或 nginx rate-limit？（何大人决定）

---

## 📝 后续 todo（备选）

1. ☐ **公网 HTTPS**：目前 8001 是 HTTP，要不要加 Let's Encrypt？
2. ☐ **rate limiting**：防滥用
3. ☐ **prod mode 切换**：`RUNTIME_ENV=prd` + JWT 验证
4. ☐ **miniMax 模型选择**：`MiniMax-Text-01` / `MiniMax-M2.7-highspeed`（速度优先）/ `MiniMax-M2.7`（质量优先）
5. ☐ **memory_search 重建**：`openclaw memory index --force`（embedding provider 可能变了）
6. ☐ **.env 实际 key 写入 vault secrets**（当前 MiniMax key 是直接写在 .env，备份到 vault 安全些）

---

## 🏗️ 一键恢复命令

```bash
# 重启容器（不重建 image）
cd /root/projects/agnos && docker compose restart

# 完全重启
cd /root/projects/agnos && docker compose up -d --force-recreate agentos-api

# 验证 stream
curl -sS -m 25 -X POST "http://101.33.212.119:8001/agents/web-search/runs" \
  -F "message=ping" -F "stream=true" 2>&1 | tail -10

# 关掉（不影响其他）
cd /root/projects/agnos && docker compose down
```