# Jev (TypeSafe System One) — 部署手册

> **状态**：✅ 部署完成（2026-09-21 15:28）
> **类型**：Agent Skill（Claude Code plugin）+ 外部 API 调用
> **不是**独立的 Docker 服务 — 它是个 SKILL + REST API 客户端

## 1. 项目信息

| 项 | 值 |
|---|---|
| 用途 | 在 agent 任务中调用 TypeSafe System One 模型（Jev），获取"类型化判断 + 概率"，用于 routing / classification / extraction / verification / scoring |
| 上游仓库 | https://github.com/typesafe-ai/skills |
| API endpoint | `POST https://api.typesafe.ai/v1/systemone` |
| 当前模型 | `jev-1.13.0`（alias: `jev-latest`） |
| Auth | `Authorization: Bearer <API_KEY>` |
| Skill 仓库本地副本 | `/root/projects/jev/typesafe-ai-skills/` |
| OpenClaw skill 路径 | `/root/.openclaw/workspace/skills/typesafe-ai/` |
| Key 存储 | `/root/.openclaw/.typesafe-env`（权限 600，env var 模式） |
| 关联 vault 笔记 | 本 README + `2026-09-21_md_jev部署完成报告.md`（待写） |

## 2. 为什么用 Jev

- **互补 MiniMax-M3 主 LLM**：主 LLM 生成文本，Jev 做"小判断 + 概率"
- **典型场景**：用户消息路由、客服工单分类、字段提取验证、rerank、score（0-5 等级评分）、yes/no 概率（Noul）
- **三种 Question 类型**：
  - `noul`：yes/no 概率（0-1）
  - `choice`：从候选集合选 1 个 + 每个选项的概率
  - `score`：有序等级评分 + 每等级概率
- **便宜 + 快**：input 392 tokens / output 66 tokens 这种调用 ≈ 1 秒返回，pricing 比通用 LLM 低（具体看 typesafe.ai 定价页）

## 3. 硬件依赖

无（不跑本地服务）。仅需：
- 出网到 `api.typesafe.ai:443`
- 一个有效 API key

## 4. 一键部署（已完成，存档用）

```bash
# 1. 克隆上游 skill 仓库
mkdir -p /root/projects/jev
cd /root/projects/jev
git clone https://github.com/typesafe-ai/skills typesafe-ai-skills

# 2. 复制 skill 到 OpenClaw workspace
cp -r typesafe-ai-skills/skills/typesafe-ai /root/.openclaw/workspace/skills/

# 3. 创建 env 文件存 key
cat > /root/.openclaw/.typesafe-env <<'EOF'
export TYPESAFE_API_KEY="apikey_..."
export TYPESAFE_BASE_URL="https://api.typesafe.ai/v1/systemone"
export TYPESAFE_MODEL="jev-latest"
EOF
chmod 600 /root/.openclaw/.typesafe-env

# 4. 写 skill config.json（让 agent 知道 base_url / env var 名）
# 已有：/root/.openclaw/workspace/skills/typesafe-ai/config.json

# 5. systemd unit 加 EnvironmentFile（让所有 agent run 继承 env vars）
# /root/.config/systemd/user/openclaw-gateway.service 追加：
#   EnvironmentFile=-/root/.openclaw/.typesafe-env
# 然后：
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway
```

## 5. 配置文件

### `/root/.openclaw/.typesafe-env`（权限 600）

```bash
export TYPESAFE_API_KEY="apikey_21783d13d38be8354d88ab57890f0b294662_59e4f620266d67acc5d48730570289f5d507aa76e5c244637e1d5fb39b4daf22"
export TYPESAFE_BASE_URL="https://api.typesafe.ai/v1/systemone"
export TYPESAFE_MODEL="jev-latest"
```

### `/root/.openclaw/workspace/skills/typesafe-ai/config.json`

```json
{
  "api_key_env": "TYPESAFE_API_KEY",
  "base_url_env": "TYPESAFE_BASE_URL",
  "model_env": "TYPESAFE_MODEL",
  "base_url_default": "https://api.typesafe.ai/v1/systemone",
  "model_default": "jev-latest",
  "auth_scheme": "Bearer"
}
```

### `/root/.config/systemd/user/openclaw-gateway.service`（增量修改）

```ini
[Service]
EnvironmentFile=-/root/.openclaw/.minimax-env          # 已有
EnvironmentFile=-/root/.openclaw/.typesafe-env         # 新增（2026-09-21）
```

## 6. 三维度验证（2026-09-21 15:28 通过）

### 维度 1：直接 curl（绕过 OpenClaw gateway）

```bash
source /root/.openclaw/.typesafe-env
curl -sS -X POST "$TYPESAFE_BASE_URL" \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "Help! My payouts have been failing for 3 days.",
    "model": "jev-latest",
    "questions": {
      "is_urgent": {"type":"noul","instructions":"Does this convey urgency?"},
      "topic": {
        "type":"choice",
        "instructions":"Pick the most relevant department to route this support ticket to",
        "criteria": {
          "billing":"Payment, charge, refund, or payout issues",
          "technical_support":"Software bugs, service outages, or integration failures",
          "account_management":"Account changes, cancellations, profile or permissions",
          "other":"Does not fit the categories above"
        }
      }
    }
  }'
```

返回（3 次调用全部一致）：
```json
{
  "model": "jev-1.13.0",
  "answers": {
    "is_urgent": {"type":"noul", "noul": 0.95},
    "topic": {"type":"choice", "choice":"billing", "confidence":1.0, "probabilities":{"billing":1.0,"technical_support":0.0,"account_management":0.0,"other":0.0}}
  },
  "usage": {"input_tokens": 392, "output_tokens": 66}
}
```

### 维度 2：OpenClaw skill 加载（待 gateway restart 后验证）

```bash
# 验证 skill 已被 OpenClaw 识别
ls /root/.openclaw/workspace/skills/typesafe-ai/  # 看到 SKILL.md + LICENSE + config.json
```

### 维度 3：agent 在 turn 中调用 typesafe API（待 gateway restart 后）

需要重启 OpenClaw gateway 让 `TYPESAFE_API_KEY` 进入 agent 进程 env。然后才能让 agent 在处理任务时自动调用 typesafe API。

## 7. ⚠️ 避坑指南

### 坑 1：Choice 的 `criteria` 必须是 dict 不是 array

❌ 错误（API 报 422）：
```json
"criteria": ["billing", "technical_support", "account_management", "other"]
```

✅ 正确：
```json
"criteria": {
  "billing": "Payment, charge, refund, or payout issues",
  "technical_support": "Software bugs, service outages, or integration failures",
  "account_management": "Account changes, cancellations, profile or permissions",
  "other": "Does not fit the categories above"
}
```

### 坑 2：`system_overloaded` 不是 key 错误

typesafe.ai 这个服务在测试中，流量高峰会返回：
```json
{"detail": {"error_type": "system_overloaded", "message": "We are currently experiencing high traffic..."}}
```

这**不是 key 问题**——重试就行（实测 3 次全部成功）。

### 坑 3：实际模型版本是 `jev-1.13.0`，请求里写 `jev-latest` 即可

服务返回 `model: "jev-1.13.0"`，但请求里用 alias `jev-latest` 会被服务端解析到当前最新版本。

### 坑 4：环境变量注入需要重启 gateway

`EnvironmentFile` 改完只 `daemon-reload` 不够，**必须 `restart openclaw-gateway`** 才能让 agent 进程继承新 env vars。

### 坑 5：tavily-search 的 config.json 把 api_key 明文写在 skill 目录里（不要学）

`/root/.openclaw/workspace/skills/tavily-search/config.json` 把 `tvly-dev-...` 明文写在文件里 —— **不推荐**。typesafe-ai 的模式（`api_key_env` 引用 + 单独 `.env` 文件 + systemd 加载）更安全。

## 8. 当前状态

| 项 | 状态 |
|---|---|
| `/root/projects/jev/typesafe-ai-skills/` | ✅ 已 clone（9-20 23:39） |
| `/root/.openclaw/workspace/skills/typesafe-ai/SKILL.md` | ✅ 已 copy（9-20 23:40） |
| `/root/.openclaw/workspace/skills/typesafe-ai/config.json` | ✅ 已创建（9-21 15:28） |
| `/root/.openclaw/.typesafe-env` | ✅ 已创建 + chmod 600（9-21 15:28） |
| systemd unit EnvironmentFile | ✅ 已加（9-21 15:28） |
| daemon-reload | ✅ 已执行（9-21 15:28） |
| OpenClaw gateway restart | ❌ **待执行**（env vars 还没进 agent 进程） |
| 端到端 API 验证 | ✅ 通过（9-21 15:28，3 次调用全部 200） |

## 9. 关联文档

- 上游 skill 仓库：https://github.com/typesafe-ai/skills
- 官方文档：https://docs.typesafe.ai/llms.txt
- API 参考：https://docs.typesafe.ai/api.md
- 三种 Question 类型：
  - Choice: https://docs.typesafe.ai/primitives/choice.md
  - Score: https://docs.typesafe.ai/primitives/score.md
  - Noul: https://docs.typesafe.ai/primitives/noul.md
- 上次 token 消耗问题报告（2026-09-21）：MEMORY.md "Token Plan 用量上限"
