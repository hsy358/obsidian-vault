# 2026-07-11 Hermes 切换 minimax-M3（从 cc-vibe → MiniMax-M3）

> 何大人 15:43 指令"hermes切换minimax模型"，15:48 完成，5 分钟切换干净。

## 切换前后对比

| 维度 | 切换前 | 切换后 |
|---|---|---|
| Provider | `custom/cc-vibe` | `custom/minimax-cn` |
| base_url | `https://cc-vibe.com/v1` | `https://api.minimaxi.com/v1` |
| Model | `gpt-5.4` | `MiniMax-M3` |
| API 协议 | OpenAI（旧版，拒 max_tokens） | OpenAI（标准） |
| max_tokens | 必须 `null`（patch 跳过） | 4096 默认（不敏感） |
| API key 来源 | `OPENAI_API_KEY` 环境变量 | config.yaml 明文（model 段不支持 env 引用） |
| Gateway 重启 | 不需要 | 不需要（lazy reload 自动检测） |

## 实测数据（关键证据）

### 1. base_url 探测（4 个端点）

| URL | 协议 | HTTP | 备注 |
|---|---|---|---|
| `https://api.minimax.io/anthropic/v1/messages` | Anthropic | 401 | ❌ global 不认这个 key |
| `https://api.minimax.io/v1/chat/completions` | OpenAI | 401 | ❌ global 不认这个 key |
| `https://api.minimaxi.com/v1/chat/completions` | OpenAI | 200 | ✅ **CN 端点** |
| `https://api.minimaxi.com/anthropic/v1/messages` | Anthropic | 200 | ✅ CN 端点也通 Anthropic |

### 2. max_tokens 兼容性（避开 cc-vibe 坑）

| 测试 | 结果 |
|---|---|
| `max_tokens=50` | ✅ 200, finish_reason=stop |
| `max_tokens=2000` | ✅ 200, finish_reason=stop |
| 不带 max_tokens | ✅ 200, finish_reason=stop（5.7s，比带 max_tokens 慢） |
| `max_completion_tokens=200` | ✅ 200（新协议也接受） |

**结论**：MiniMax-M3 对 max_tokens **完全不敏感**——不像 cc-vibe 必须 null patch。

### 3. Hermes 真实对话跑通

**CLI 测试**：
```bash
$ hermes chat -q "用一句话介绍你自己" -Q --max-turns 5 -m MiniMax-M3
session_id: 20260711_154753_bf768b
我是 Hermes Agent，由 Nous Research 打造的 CLI 编程助手，帮你在工作目录里读写代码、跑命令、排查问题...
```

**飞书实测**（何大人 15:48:25 飞书发"继续"）：
```
2026-07-11 15:48:37,310 agent.turn_context: conversation turn: session=20260711_085430_4010ec53 model=MiniMax-M3 provider=custom platform=feishu
2026-07-11 15:48:37,311 agent.conversation_loop: Stored system prompt has stale runtime identity; rebuilding for model=MiniMax-M3
2026-07-11 15:48:37,443 run_agent: OpenAI client created ... provider=custom base_url=https://api.minimaxi.com/v1 model=MiniMax-M3
2026-07-11 15:48:55,262 API call #1: model=MiniMax-M3 in=276915 out=471 latency=17.9s cache=1408/276915 (1%)
2026-07-11 15:49:03,531 API call #2: in=277922 out=303 latency=7.6s cache=277120/277922 (100%)
2026-07-11 15:49:10,855 API call #3: in=278686 out=305 latency=7.2s cache=277888/278686 (100%)
```

**结论**：gateway 自动 lazy reload，飞书链路完全正常工作，cache 命中率从 1% → 100%。

## 6 个关键发现（写进永久规则）

### 1. MiniMax-M3 **不在** hermes catalog 的内置 provider 中

`/root/.hermes/models_dev_cache.json` 里 `minimax` 和 `minimax-cn` 只有 M2.1 / M2.5 / M2.7 系列，**没有 M3**。

所以必须用 `provider: custom` 手动配置（不是 `provider: minimax-cn`）。

### 2. MiniMax CN 端点 `minimaxi.com` 才是这个 key 的归属地

global `minimax.io` 用 `MINIMAX_API_KEY` 这个 key 是 401（"invalid api key"）。**只用 CN 端点**：
- `https://api.minimaxi.com/v1` (OpenAI 协议)
- `https://api.minimaxi.com/anthropic/v1` (Anthropic 协议)

### 3. hermes `model` 段**不支持** `key_env`，只支持明文 `api_key`

我先写 `key_env: MINIMAX_CN_API_KEY` 想让 hermes 从 .env 读 key，结果报：
```
HTTP 401: login fail: Please carry the API secret key in the 'Authorization' field of the request header (1004)
```

代码证据：
- `agent/credential_pool.py:2289` 注释： `# Seed from model.api_key if model.provider=='custom'`
- `agent/chat_completion_helpers.py:1259` 用 `key_env` **只在 fallback chain** 里
- `agent/auxiliary_client.py:4158-4164` 自定义 endpoint 默认走 `OPENAI_API_KEY` 环境变量

**结论**：`model.api_key` 字段必须写明文（跟 .env 同 600 权限，安全等价）。

### 4. hermes gateway **lazy reload** config，不用重启

gateway PID 268213 从 00:43 跑到现在（15+ 小时），config.yaml 改了之后：
- `hermes status` 立即识别 `Model: MiniMax-M3`
- 飞书收到消息后，gateway 检测到 `Stored system prompt has stale runtime identity; rebuilding for model=MiniMax-M3`
- 自动重建 OpenAI client 指向 minimaxi.com

**永久规则**：改 hermes config **不需要重启 gateway**（除非改的是 .env 里的 key 因为缓存了 OpenAI client）。

### 5. MiniMax-M3 输出有 `<think>...</think>` 标签，但 hermes 正确处理

实测 curl 返回的 content 包含 thinking 标签，但 hermes 转发给飞书的输出干净（没看到 `<think>`）。说明 hermes 的 chat_completion transport 处理 thinking tag 正确。

### 6. vision auxiliary 还是用 `gpt-5.4`（cc-vibe）

agent.log 显示：
```
2026-07-11 15:48:31,270 agent.auxiliary_client: Vision auto-detect: using main provider custom (gpt-5.4)
```

主对话（飞书 DM）走 MiniMax-M3 ✅，但**图片理解**辅助任务还是用 gpt-5.4。

**原因**：vision 走 auto-detect，main provider 是 custom/custom（自定义 endpoint 没标记为支持 vision），所以回退到 OpenRouter 链第一项（之前 cached 的是 cc-vibe）。

**影响**：日常 DM 不影响。要发图给 hermes 时才会调 cc-vibe（gpt-5.4）。

## 配置备份链

| 备份 | 时间 | 内容 |
|---|---|---|
| `config.yaml.bak.2026-07-08-2340` | 7-8 23:40 | Gemini fallback 启用状态 |
| `config.yaml.bak.2026-07-09-2352-pre-minimax` | 7-9 23:52 | 第一次尝试切 minimax 前的状态 |
| `config.yaml.bak.2026-07-09-2359-pre-minimax` | 7-9 23:59 | 第一次尝试切 minimax 前的状态 |
| `config.yaml.bak.2026-07-10-minimax-2126` | 7-10 21:26 | 第二次切 minimax |
| `config.yaml.bak.2026-07-11-1543-pre-minimax-M3` | 7-11 15:43 | **本次切换前** |

## 当前 config.yaml 关键段（保留供回滚）

```yaml
model:
  provider: custom
  base_url: https://api.minimaxi.com/v1
  api_key: sk-cp-hQX2Y5GGzChVYsg8CZVpLa6jcDzIyquiXtyk-TX1lAfp35M87ucgZMYulAVBrA9jOiEzHMysU9v3zfLbzIGlcP-fyc-dxcgQnkj6ztDv_YOSHQEDB4IteUQ
  api_mode: openai
  default: MiniMax-M3
  max_tokens: 4096

custom_providers:
  - name: minimax-cn           # 主 provider
    base_url: https://api.minimaxi.com/v1
    api_key: sk-cp-hQX2Y5GGzChVYsg8CZVpLa6jcDzIyquiXtyk-TX1lAfp35M87ucgZMYulAVBrA9jOiEzHMysU9v3zfLbzIGlcP-fyc-dxcgQnkj6ztDv_YOSHQEDB4IteUQ
    model: MiniMax-M3
    api_mode: openai
  - name: cc-vibe              # 备用（fallback chain 可用）
    base_url: https://cc-vibe.com/v1
    api_key: sk-5870692d21da8e2dae11708ff564f454eab902b71a8080294239d2aa4bb3b956
    model: gpt-5.4
    api_mode: openai
```

## 关键操作日志

- **15:43** 何大人指令"hermes切换minimax模型"
- **15:43-15:44** 调研：minimax/MiniMax-CN 内置 provider 是 Anthropic 协议，catalog 无 M3
- **15:44** 实测 4 个 base_url，确认 `minimaxi.com` 通
- **15:44** 实测 max_tokens 兼容性，4 种配置都 200
- **15:45** 备份 `config.yaml.bak.2026-07-11-1543-pre-minimax-M3`
- **15:46** 改 config.yaml（先用 key_env 引用 .env）
- **15:46** `hermes chat` 测试报 HTTP 401——发现 `key_env` 不被 model 段支持
- **15:47** 恢复 `api_key` 明文
- **15:47** `hermes chat` 跑通：返回 Hermes 自我介绍
- **15:48** 工具调用测试（exec 列文件）：返回 5 个最近文件
- **15:48** 飞书实测：何大人 15:48:25 发"继续"，gateway 15:48:37 lazy reload 到 MiniMax-M3
- **15:49** 飞书 cache 命中 100%，7.2s 延迟

## 关联文档

- `/root/vault/1-Projects/德勤/AI-Native/2026-07-08_Hermes_cc-vibe_400_根因与永久修复.md`（cc-vibe patch 原理）
- `~/.hermes/config.yaml`（当前生效）
- `~/.hermes/config.yaml.bak.2026-07-11-1543-pre-minimax-M3`（可回滚）

## 后续待办

- [ ] vision auxiliary 切到 MiniMax-M3（避免发图时调 cc-vibe）—— 待何大人确认
- [ ] 跟同事确认 MiniMax-M3 在国内访问稳定性（CN 端点应该 OK）
- [ ] 监控 1 周 MiniMax-M3 在飞书对话的稳定性