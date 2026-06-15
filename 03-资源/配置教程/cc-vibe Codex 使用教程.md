---
title: "cc-vibe Codex 使用教程"
source: 微信公众号（何大人转发）
date: 2026-06-16
type: 配置教程
---

# cc-vibe Codex 使用教程

## 支持的模型清单
- gpt-5.4
- gpt-5.4-mini
- gpt-5.5
- gpt-image-2
- codex-auto-review

**⚠️ 创建秘钥时，分组必须选择 Codex 分组**

## 配置文件 1: `~/.codex/config.toml`

```toml
model_provider = "OpenAI"
model = "gpt-5.5"
review_model = "gpt-5.5"
model_reasoning_effort = "xhigh"
disable_response_storage = true
network_access = "enabled"
model_context_window = 200000
model_auto_compact_token_limit = 140000

[model_providers.OpenAI]
name = "OpenAI"
base_url = "https://cc-vibe.com/v1"
wire_api = "responses"
supports_websockets = false
requires_openai_auth = true
request_max_retries = 4
stream_max_retries = 5
```

## 配置文件 2: `~/.codex/auth.json`

```json
{
  "OPENAI_API_KEY": "你的API_KEY秘钥"
}
```

## 其它工具（OpenAI 兼容协议）

### 1. chat/completions
```bash
curl https://cc-vibe.com/v1/chat/completions \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer sk-xxxx" \
 -d '{
  "model": "gpt-5.5",
  "messages": [{"role": "user", "content": "你是谁？"}],
  "stream": true
}'
```

### 2. /v1/messages（Anthropic 兼容）
```bash
curl https://cc-vibe.com/v1/messages \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer sk-xxxx" \
 -d '{
  "model": "gpt-5.5",
  "messages": [{"role": "user", "content": "你是谁？"}],
  "stream": true
}'
```

### 3. /v1/responses
```bash
curl --request POST \
 --url https://cc-vibe.com/v1/responses \
 --header 'Authorization: Bearer sk-xxxx' \
 --header 'Content-Type: application/json' \
 --data '{
  "model": "gpt-5.5",
  "input": [{"role": "user", "content": [{"type": "input_text", "text": "Hello"}]}],
  "stream": true,
  "reasoning": {"effort": "high"}
}'
```

## 关键修正（我之前猜错的）

| 项 | 我之前 | 官方正确 |
|----|--------|----------|
| `model_provider` | 用了 "ccvibe" | **"OpenAI"** |
| provider 名字 | "ccvibe" | **"OpenAI"**（允许的）|
| 模型 | gpt-4 | **gpt-5.5** |
| key 存储 | codex login 命令 | **auth.json 文件** |
| 关键字段 | 缺 | `disable_response_storage`, `network_access`, `model_context_window` 等 |
