---
title: "AgentTeams（HiClaw）官方仓库与安装可行性评估"
source: web_fetch
urls:
  - https://hiclaw.io
  - https://github.com/agentscope-ai/AgentTeams
  - https://raw.githubusercontent.com/agentscope-ai/AgentTeams/main/install/agentteams-install.sh
saved_date: 2026-07-30
trigger: "何大人 2026-07-30 10:51 让评估 AgentTeams 部署可行性"
status: evaluated-not-installed
---

# AgentTeams（HiClaw）官方仓库与安装可行性评估

> 起源：何大人 10:43 转发《AgentTeams企业级智能体协作平台安装实战（二）》，10:51 让直接拉评估

## 🎯 结论先行

**可装，0 阻碍**。阿里云 / AgentScope 官方出品（Apache 2.0），国内镜像可达，端口不冲突，资源充足。

| 项 | 状态 | 备注 |
|---|---|---|
| 官方仓库 | ✅ 找到 | `github.com/agentscope-ai/AgentTeams` |
| 当前版本 | v1.2.0-beta.1（2026-07-17） | stable = v1.1.2（2026-05-27） |
| 国内镜像 | ✅ 可拉 | `higress-registry.cn-hangzhou.cr.aliyuncs.com` |
| 端口冲突 | ✅ 无 | 默认 18080/18001/18088/18888/13000 全空 |
| 资源 | ✅ 充足 | 8C30G / 137G 占 / x86_64 |
| LLM | ✅ 已有 | MiniMax-M3 / DeepSeek（脚本内置 KNOWN_MODELS） |

## 1️⃣ 官方入口（实测可达）

| 用途 | URL |
|---|---|
| 官网 | https://hiclaw.io |
| GitHub | https://github.com/agentscope-ai/AgentTeams |
| 安装脚本 | `https://raw.githubusercontent.com/agentscope-ai/AgentTeams/main/install/agentteams-install.sh` |
| Helm chart | `higress.io/agentteams`（K8s 部署） |
| 文档 | https://hiclaw.io/docs |

> **作者身份**：阿里云 / AgentScope 团队（前身是 Higress 团队内部项目，2026-03 开源）。

## 2️⃣ 架构（v1.1.0+）

**关键架构变化**（从 v1.1.0 起 manager 不再 bundle Higress/Tuwunel/MinIO）：

- **embedded controller 架构**（v1.1.0+ 默认）：agentteams-embedded（内部 kube-apiserver）+ agentteams-manager + agentteams-worker-*（多 Worker）
- **legacy all-in-one 架构**（<= v1.0.9）：单个 manager 容器 bundle 全部组件
- 安装脚本会**优先 pull `agentteams-embedded`**，不存在则报错而非自动回退 legacy

### 容器列表

| 容器 | 镜像 | 默认端口 |
|---|---|---|
| agentteams-manager | agentteams-manager:latest | 18888（manager 控制台） |
| agentteams-embedded | agentteams-embedded:latest | 内部 kube-apiserver |
| agentteams-docker-proxy | agentteams-docker-proxy:latest | （无对外端口） |
| agentteams-worker-<name> | agentteams-worker:latest（按 runtime 分） | 视 Worker 类型而定 |
| agentteams-dashboard（可选） | agentteams-dashboard:v1.2.0-beta.1 | 13000 |

### 核心组件

- **Higress AI Gateway**（18080 / 18001）：LLM 路由 + 凭证集中托管（Worker 只持 consumer-token）
- **Tuwunel**（Matrix IM 服务端）：Matrix 协议，去中心化聊天
- **Element Web**（18088）：Matrix Web 客户端
- **MinIO**：Agent 间共享文件系统（避免重复传递 token）
- **CoPaw / QwenPaw Manager**：确定性编排 runtime
- **OpenClaw / Hermes Worker**：Worker runtime（OpenClaw = 确定性，Hermes = 自主编码）
- **可选 Nacos Skills Registry**：Worker 按需拉 Skills

### Manager / Worker runtime 选项（helm）

```bash
--set manager.runtime=openclaw       # default：openclaw
--set manager.runtime=copaw
--set manager.runtime=hermes
--set worker.defaultRuntime=openclaw # default：openclaw
--set worker.defaultRuntime=copaw
--set worker.defaultRuntime=hermes
```

> ⚠️ **名称歧义警告**：这里的 `openclaw` runtime 是 **AgentTeams 自己的确定性 runtime**，**不是**我们当前用的 OpenClaw 主项目（OpenClaw gateway 工具）。名字撞了但不是一回事。

## 3️⃣ 我服务器实测

### 3.1 端口检查

```bash
$ ss -tlnp | grep -E ':(8080|18080|18001|18088|18888|13000) '
LISTEN 0 4096 0.0.0.0:8080 users:(("docker-proxy",pid=1519204,fd=7))
# → 仅 8080 被 dify-nginx 占了
# → 18080/18001/18088/18888/13000 都空 ✅
```

### 3.2 镜像可拉性

```bash
$ docker pull higress-registry.cn-hangzhou.cr.aliyuncs.com/agentteams/agentteams-manager:latest
# → Download complete，pull 成功 ✅
```

### 3.3 安装脚本可下载

```bash
$ curl -fsSL https://raw.githubusercontent.com/agentscope-ai/AgentTeams/main/install/agentteams-install.sh > /tmp/agentteams-install.sh
# → 257512 bytes（4673 行）下载成功 ✅
```

### 3.4 服务器资源

| 资源 | 实测 | AgentTeams 要求 | 余量 |
|---|---|---|---|
| CPU | 8C | 2C 最低 / 4C 推荐 | ✅ |
| RAM | 30G（21G used / 9.4G avail） | 4G 最低 / 8G 推荐 | ⚠️ 紧（推荐关几个 worker 服务） |
| 磁盘 | 315G / 137G 用 / 166G avail | 50G+（多 worker + 日志） | ✅ |
| 架构 | x86_64 | x86_64 / ARM64 | ✅ |

## 4️⃣ 端口规划建议

| 端口 | AgentTeams 默认 | 我们服务器 | 用途 |
|---|---|---|---|
| 18080 | Higress Gateway（主入口） | ✅ 空 | 公网访问主 URL |
| 18001 | Higress Console | ✅ 空 | 网关管理 |
| 18088 | Element Web（IM） | ✅ 空 | Matrix Web 客户端 |
| 18888 | Manager Console | ✅ 空 | CoPaw / OpenClaw Manager |
| 13000 | Dashboard（可选） | ✅ 空 | 总览 UI |

**给何大人的访问 URL**（装好后）：
- `http://101.33.212.119:18088` ← 主入口（Element Web + Manager）
- `http://101.33.212.119:18080` ← Higress Gateway
- `http://101.33.212.119:13000` ← Dashboard

按 TOOLS.md "给何大人的 URL 永远用标准 80 端口"原则，未来应该 nginx 80 反代 18088。

## 5️⃣ LLM 接入选项

AgentTeams 安装脚本内置 KNOWN_MODELS 列表（已实测包含）：

```
gpt-5.4 gpt-5.3-codex gpt-5-mini gpt-5-nano
claude-opus-4-6 claude-sonnet-4-6 claude-haiku-4-5
qwen3.6-plus qwen3.5-plus
deepseek-chat deepseek-reasoner
kimi-k2.5 glm-5
MiniMax-M2.7 MiniMax-M2.7-highspeed MiniMax-M2.5
```

⚠️ **没有 MiniMax-M3** —— 需走 `prompt_custom_model_params` 自定义路径，输：
- context_window：建议 32768（按 M3 的能力）
- max_tokens：建议 4096
- reasoning：默认 false
- vision：默认 false

**推荐 LLM 选项**（按可行性排序）：

| # | Provider | base_url | 模型 | 备注 |
|---|---|---|---|---|
| 1 | **MiniMax-M3** | `https://api.minimaxi.com/v1` | MiniMax-M3 | 我们已有 key（`sk-cp-hQX2Y5GGz...`），需自定义 model 参数 |
| 2 | DeepSeek | `https://api.deepseek.com/v1` | deepseek-chat | 脚本内置，$1/M token 便宜 |
| 3 | Qwen | DashScope | qwen3.6-plus | 阿里官方，hiclaw 默认推荐 |

## 6️⃣ 推荐安装命令（非交互模式）

```bash
# 先备份当前服务器状态
cd /root/vault/current-server

# 一键安装（用 MiniMax-M3 自定义参数）
export AGENTTEAMS_NON_INTERACTIVE=1
export AGENTTEAMS_LLM_PROVIDER=openai-compat
export AGENTTEAMS_OPENAI_BASE_URL=https://api.minimaxi.com/v1
export AGENTTEAMS_LLM_API_KEY='sk-cp-hQX2Y5GGzChVYsg8CZVpLa6jcDzIyquiXtyk-TX1lAfp35M87ucgZMYulAVBrA9jOiEzHMysU9v3zfLbzIGlcP-fyc-dxcgQnkj6ztDv_YOSHQEDB4IteUQ'
export AGENTTEAMS_DEFAULT_MODEL=MiniMax-M3
export AGENTTEAMS_MODEL_CONTEXT_WINDOW=32768
export AGENTTEAMS_MODEL_MAX_TOKENS=4096
export AGENTTEAMS_ADMIN_USER=admin
export AGENTTEAMS_ADMIN_PASSWORD='<何大人设的密码>'
export AGENTTEAMS_DASHBOARD=1

bash <(curl -sSL https://raw.githubusercontent.com/agentscope-ai/AgentTeams/main/install/agentteams-install.sh)
```

或者用 DeepSeek（脚本内置，不用自定义 model）：

```bash
export AGENTTEAMS_NON_INTERACTIVE=1
export AGENTTEAMS_LLM_PROVIDER=openai-compat
export AGENTTEAMS_OPENAI_BASE_URL=https://api.deepseek.com/v1
export AGENTTEAMS_LLM_API_KEY='<deepseek-key>'
export AGENTTEAMS_DEFAULT_MODEL=deepseek-chat
bash <(curl -sSL https://raw.githubusercontent.com/agentscope-ai/AgentTeams/main/install/agentteams-install.sh)
```

## 7️⃣ 风险点 / 注意事项

1. **Docker socket 挂载**：脚本默认 mount docker socket（`AGENTTEAMS_MOUNT_SOCKET=1`），允许 manager 创建 Worker 容器——这是它的工作机制，但攻击面增加
2. **资源压力**：9.4G avail 内存 + 50G+ 磁盘空间没问题，但**多个 Worker 会按 runtime 各起独立容器**——保守 1-2 个 Worker，监控内存
3. **重启即失效风险**（历史教训 2026-07-06）：SSH 登出会 kill nohup 启动的子进程——但 AgentTeams 容器由 docker daemon 管理，**不受影响** ✅
4. **TLS**：默认 HTTP，Element Web 有 SW / crypto 警告（跟作者踩的坑一样）——内网自用可忽略
5. **端口 18080 公网暴露**：要不要走 nginx 80 反代？待何大人决策
6. **Dify 的 8080 占用了**：不影响 AgentTeams（它默认 18080，不是 8080），但**别误改**
7. **镜像大小**：article 说 1.7GB image shrink（v1.1.0），按 5 个 image × 1-2GB ≈ 5-10GB 磁盘占用
8. **跟 OpenClaw 的关系**：OpenClaw 是 AgentTeams 的 worker runtime 之一（确定性 runtime），**但**跟我们的 OpenClaw gateway 主项目不是同一个东西——名字撞了，别混
9. **AgentTeams v1.2.0-beta.1** 是 prerelease（2026-07-17），建议**先用 stable v1.1.2**

## 8️⃣ 待决策（何大人拍板）

1. **是否安装**：默认推荐 ✅（资源 / 端口 / 镜像 / LLM 全 OK）
2. **装哪个版本**：
   - stable **v1.1.2**（保守）
   - beta **v1.2.0-beta.1**（新功能：plugin platform / TeamHarness / WorkerFlow / Matrix AppService / Human SSO / model-provider routing / LLM preflight）
3. **用哪个 LLM**：
   - **MiniMax-M3**（我们已有 key + 自定义 model 参数）
   - **DeepSeek**（脚本内置，省心，但需要 key）
4. **是否安装 Dashboard**（AGENTTEAMS_DASHBOARD=1）
5. **管理员密码 / 端口是否需要改**（默认全 OK）
6. **是否走 nginx 80 反代 18088**（何大人访问 URL 简化）

## 9️⃣ 关联文档

- 公众号文章归档：`/root/vault/current-server/from-agent/2026-07-30/2026-07-30 - 公众号-AgentTeams企业级智能体协作平台安装实战（二）.md`
- 当前服务器部署清单：`/root/vault/current-server/开源软件访问清单.md`
- README 规范：`/root/vault/current-server/README.md`
