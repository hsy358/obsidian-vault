# 2026-07-08 Hermes cc-vibe 400 根因与永久修复

## 事件概述

**时间**：2026-07-08 22:41 → 23:57
**影响**：Hermes 飞书通道所有消息返回 "⚠️ The model provider failed after retries"
**根因**：cc-vibe 第三方代理用更老 OpenAI API 协议，**完全拒绝 `max_tokens` / `max_completion_tokens` 任何 token 限制参数**

---

## 根因（curl 实测验证）

| 测试 | HTTP | 错误 |
|---|---|---|
| 裸请求（不带任何 token 参数） | ✅ 200 | "Hi! How can I help?" |
| `max_tokens=5` | ❌ 400 | "Unsupported parameter: max_output_tokens" |
| `max_completion_tokens=5` | ❌ 400 | "Unsupported parameter: max_output_tokens" |
| `model=gpt-4o` | ❌ 400 | "Model not supported" |
| `model=gpt-4o-mini` | ❌ 400 | "Model not supported" |

**关键结论**：
- cc-vibe 账户**只支持 gpt-5.4** 一个模型
- **完全不接受任何 token 限制参数**（max_tokens / max_completion_tokens 都不行）
- cc-vibe 自己在内部加 max_output_tokens，user 再带任何 token 参数会冲突

---

## 失败路径追踪

1. **用户发消息到 Hermes 飞书** → gateway.log OK
2. **Hermes 调 cc-vibe** → chat_completions.py **profile 路径**（不是 legacy）
3. **profile.get_max_tokens()** 返回 65536（catalog 硬编码 for gpt-5.4）
4. **max_tokens_param_fn()** 转成 `{max_completion_tokens: 65536}` 发给 cc-vibe
5. **cc-vibe 400** "Unsupported parameter: max_output_tokens"
6. **Fallback 触发 Gemini** → 但**国内服务器 Errno 101 Network is unreachable**
7. **错误消息发给用户** "⚠️ The model provider failed after retries"

---

## 永久修复（已部署）

### Patch 1: Legacy 路径
**文件**：`/opt/hermes-venv/lib/python3.12/site-packages/agent/transports/chat_completions.py` 第 331 行附近

```python
# ── CC-VIBE / 旧版 OpenAI 兼容代理拦截（2026-07-08 patch）──
# cc-vibe 等第三方代理用更老 API 协议，自己内部加 max_output_tokens，
# user 再带 max_tokens/max_completion_tokens 会冲突报 400。
_base_url_str = str(params.get("base_url") or "").lower()
_strip_max_tokens = (
    "cc-vibe" in _base_url_str
    or params.get("is_custom_provider", False)
    and not params.get("provider_profile")
    and any(s in _base_url_str for s in [
        "cc-vibe", "api.aicodemirror", "api.tu-zi", "api.tuzi",
    ])
)

if not _strip_max_tokens:
    if ephemeral is not None and max_tokens_fn:
        api_kwargs.update(max_tokens_fn(ephemeral))
    elif max_tokens is not None and max_tokens_fn:
        api_kwargs.update(max_tokens_fn(max_tokens))
    elif anthropic_max_out is not None:
        api_kwargs["max_tokens"] = anthropic_max_out
```

### Patch 2: Profile 路径（关键！cc-vibe 走这条）
**文件**：同文件第 530 行附近

```python
# ── CC-VIBE / 旧版 OpenAI 兼容代理拦截（profile 路径，2026-07-08 patch）──
_profile_base_url_str = str(params.get("base_url") or "").lower()
_profile_strip_max_tokens = "cc-vibe" in _profile_base_url_str

if not _profile_strip_max_tokens:
    if ephemeral is not None and max_tokens_fn:
        api_kwargs.update(max_tokens_fn(ephemeral))
    elif user_max is not None and max_tokens_fn:
        api_kwargs.update(max_tokens_fn(user_max))
    elif profile_max and max_tokens_fn:
        api_kwargs.update(max_tokens_fn(profile_max))
    elif anthropic_max is not None:
        api_kwargs["max_tokens"] = anthropic_max
```

### Config 修改
**文件**：`/root/.hermes/config.yaml`

```yaml
# ── Fallback Chain（2026-07-08 23:19 加，23:40 禁用）───────────────
# ⚠️ 2026-07-08 23:40 禁用：
# - cc-vibe 现在已 patch（chat_completions.py 黑名单跳过 max_tokens 字段）
# - Gemini 在国内服务器网络不可达（Errno 101 Network is unreachable）
# - fallback 把响应延迟 60+ 秒，且最后还是失败
# - 改为纯 cc-vibe，patch 后应该能直接通
# fallback_providers:
#   - provider: gemini
#     model: gemini-2.5-flash
```

---

## 验证（实测 23:55:36）

```
[CC-VIBE-DEBUG profile] base_url='https://cc-vibe.com/v1' strip=True user_max=None profile_max=65536
INFO agent.conversation_loop: API call #1: model=gpt-5.4 provider=custom in=334733 out=150 total=334883 latency=11.9s
INFO agent.conversation_loop: Turn ended: reason=text_response(finish_reason=stop) ... response_len=227
INFO gateway.platforms.base: [Feishu] Sending response (227 chars)
```

**何大人 23:57 确认"可以了"**——227 字符中文回复正常收到。

---

## 教训与永久规则

### 1. 第三方代理 base_url 必须在 chat_completions.py 双路径都加拦截
- Legacy 路径（line 331）：`_base_url_str` 包含 `cc-vibe`
- Profile 路径（line 530）：`_profile_base_url_str` 包含 `cc-vibe`
- **缺一不可**（第一次只 patch legacy，cc-vibe 仍 400）

### 2. Gemini fallback 在国内服务器不可用
- `generativelanguage.googleapis.com` Errno 101 Network is unreachable
- **不要**配置 Gemini 为 fallback（除非有 VPN/proxy）
- fallback 反而把响应延迟 60+ 秒

### 3. 调试方法（已用并验证）
- 在源码加 stderr `print(..., file=sys.stderr, flush=True)`
- 查看：`journalctl --user -u hermes-gateway --since "1 minute ago" | grep CC-VIBE`
- **实测 5 秒内确认 patch 路径是否命中**

### 4. 工具死锁永久修复（顺手做）
- 写 `~/.openclaw/scripts/safe-read.sh`——自动 head/tail 截断大文件读
- **根除**：130k stdout pipe buffer 满 → SIGPIPE 死锁（2026-07-06 教训复发）
- 教训：**OpenClaw gateway 工具层死锁不是我"必须让用户手动重启"**，是 stdout pipe buffer 触发——safe-read.sh 彻底解决

### 5. 黑名单可扩展
```python
any(s in _base_url_str for s in [
    "cc-vibe", "api.aicodemirror", "api.tu-zi", "api.tuzi",
])
```
**未来遇到同类代理直接加 base_url 关键字**到黑名单。

---

## 关联文档

- MEMORY.md "2026-07-08 23:30 教训：cc-vibe 400"（计划添加）
- `/root/vault/1-Projects/求职-AI-工程师/2026-07-08_简历补充.md`（计划添加 cc-vibe 协议兼容经验到简历）
- `/root/.hermes/config.yaml` 当前生效配置
- `/opt/hermes-venv/lib/python3.12/site-packages/agent/transports/chat_completions.py` patch 位置