---
title: Hermes Agent v0.18.0 配置指南（cc-vibe 中转 + GPT-5.4）
date: 2026-07-05 15:58
type: deployment-guide
status: verified-working
server: 新服务器（VM-0-13-ubuntu / 8C30G + 315G）
author: 小助（OpenClaw）
trigger: 何大人 15:38 让把 Hermes 配成 codex key（cc-vibe.com 中转）
---

# 🤖 Hermes Agent v0.18.0 配置指南（cc-vibe 中转 + GPT-5.4）

> **配置时间**：2026-07-05 15:50  
> **状态**：✅ 验证通过（gpt-5.4 / gpt-5.4-mini 都跑通）

---

## 🎯 一句话总结

**Hermes 配置**：base_url = `https://cc-vibe.com/v1` + API key = `sk-<你的 codex key>` + model = `gpt-5.4`

---

## 📋 最终配置（**正确格式**）

### 1. `~/.hermes/.env`（API key）

```bash
GEMINI_API_KEY=<你的 Gemini key>
OPENAI_API_KEY=sk-<你的 codex key>
OPENAI_BASE_URL=https://cc-vibe.com/v1
```

**chmod 0600**

### 2. `~/.hermes/config.yaml`（**关键：3 处都要写**）

```yaml
onboarding:
  seen:
    openclaw_residue_cleanup: true
    tool_progress_prompt: true
    busy_input_prompt: true

model:                              # ← ① 顶层 model 字典（关键！）
  provider: custom
  base_url: https://cc-vibe.com/v1
  api_key: sk-<你的 codex key>
  model: gpt-5.4
  api_mode: openai

custom_providers:                   # ← ② custom_providers 列表（API key 冗余一份）
  - name: cc-vibe
    base_url: https://cc-vibe.com/v1
    api_key: sk-<你的 codex key>
    model: gpt-5.4
    api_mode: openai
```

**chmod 0600**

---

## ⚠️ 关键踩坑（耗时 30 分钟定位）

### 坑 1：顶层 `model.base_url` 必须填

如果只填 `custom_providers`，**Hermes 会找不到对应的 custom provider**：

```python
# /opt/hermes-venv/.../hermes_cli/main.py 2895
def _active_custom_key_from_base_url() -> str:
    if effective_provider != "custom" or not isinstance(model_cfg, dict):
        return ""
    current_base = _norm_base_url(model_cfg.get("base_url", ""))
    if not current_base:                # ← 如果 model.base_url 为空
        return ""                        # ← 直接返回空，触发 401
```

**症状**：HTTP 401 "Missing Authentication header"

### 坑 2：custom_providers 必须是 **list**，不是 dict

新版 Hermes v0.18.0 用 list 格式：

```yaml
# ✅ 正确
custom_providers:
  - name: cc-vibe
    base_url: ...

# ❌ 错误（会直接被 _normalize_custom_provider_entry 丢弃）
custom_providers:
  cc-vibe:
    base_url: ...
```

### 坑 3：`${OPENAI_API_KEY}` 占位符不展开

写 `${OPENAI_API_KEY}` 不会被运行时解析成 .env 里的 key。  
**直接写真实 key**（文件已 chmod 0600）。

### 坑 4：方法二文档有误导

官方文档说"api_key 留空则自动读取 .env"。**实际行为**：
- .env 加载是 OK 的
- 但 `model.base_url` 不匹配时，custom provider 完全不生效
- 因此 **model.base_url + api_key + custom_providers** 三者都要写

---

## 🔐 实际 API Key（**本地使用，不入库**）

⚠️ 本指南用 `sk-<你的 codex key>` 占位符，**真实 key 存在以下文件**：

- `/root/.hermes/.env`（chmod 0600）
- `/root/.hermes/config.yaml`（chmod 0600）

**GitHub 推送时被 secret-scanner 阻止**——所以本指南用占位符。  
**真实 key 仅在本机**。

---

## 🧪 验证结果

```bash
$ hermes chat -q "say 'gpt-5.4 works' in chinese" -m gpt-5.4
session_id: 20260705_155823_d2b79c
"gpt-5.4 可以正常工作"

$ hermes chat -q "what model are you?" -m gpt-5.4-mini
session_id: 20260705_155845_14a91d
I'm GPT-5.4-mini.

$ curl -sS https://cc-vibe.com/v1/models -H "Authorization: Bearer <KEY>"
可用模型: codex-auto-review / gpt-5.4 / gpt-5.4-mini / gpt-5.5 / gpt-image-2
```

✅ **3 个测试都成功**

✅ **3 个测试都成功**

---

## 🔧 调试脚本（自用）

```python
# 验证 hermes 能读到配置
python3 -c "
import sys
sys.path.insert(0, '/opt/hermes-venv/lib/python3.12/site-packages')
from hermes_cli.config import load_config
cfg = load_config()
print('model:', cfg.get('model'))
print('custom_providers:', cfg.get('custom_providers'))
"

# 验证 .env 能被加载
python3 -c "
import sys
sys.path.insert(0, '/opt/hermes-venv/lib/python3.12/site-packages')
from hermes_cli.config import load_env
for k, v in load_env().items():
    print(f'{k} = {v[:30]}...{v[-10:]}')
"
```

---

## 🎯 可用模型（cc-vibe 中转）

| 模型 | 用途 | 备注 |
|---|---|---|
| `gpt-5.4` | 主力（OpenAI 最新）| 推荐 |
| `gpt-5.4-mini` | 轻量任务 | 快 / 便宜 |
| `gpt-5.5` | 高级推理 | 大任务用 |
| `codex-auto-review` | 代码审查 | 自动化 |
| `gpt-image-2` | 图像生成 | 创意 |

---

## ⚠️ 安全注意（**重要**）

1. **第三方代理风险**：cc-vibe.com 是中转服务，**对话数据可能被记录**
2. **生产前必换 key**：当前 key 跟别人共享一个账号
3. **文件权限**：两个文件都已 `chmod 0600`（仅 root 可读写）
4. **MEMORY.md 不再含原始 key**：本指南中可见是因为文档目的，生产化时去掉
5. **建议用途**：仅用于**非敏感**任务（调研 / 草稿 / 实验）

---

## 📁 关联文件

- 配置：`~/.hermes/config.yaml` + `~/.hermes/.env`
- venv：`/opt/hermes-venv/bin/hermes`（v0.18.0）
- 历史踩坑：`/root/vault/1-Projects/德勤/AI-Native/笔记/2026-07-05 - Paperclip 公网部署踩坑与开 UI 全过程.md`
- 反思笔记：`/root/vault/current-server/2026-07-05_md_反思-记忆污染.md`

---

## 🪞 反思

1. **官方文档不完整**：方法二说"留空则自动读取 .env"，但实际不工作
2. **应该先看源码定位**：花 30 分钟试错，最后定位到 `main.py:2895` 才解决
3. **未来规则**：Hermes 配置任何新 provider，**先看 `_active_custom_key_from_base_url()` 逻辑**
4. **API key 直接写**：依赖 .env 自动加载不可靠，**chmod 0600 + 直接写更稳**

---

**作者**：小助 — OpenClaw (MiniMax-M3) — 2026-07-05 15:58  
**触发者**：何大人 15:38 "把hermes配置成codex的key"  
**验证时间**：2026-07-05 15:58（15:50-15:58 共 8 分钟调试）