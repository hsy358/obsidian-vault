# Hermes 切换到 MiniMax-M3 模型（2026-07-10）

## 背景

何大人 2026-07-10 21:23 指令："Hermes切换minimax模型"。

## 切换前 vs 切换后

| 项 | 切换前 | 切换后 |
|---|---|---|
| provider | custom | **minimax-cn**（Hermes 内置）|
| base_url | https://cc-vibe.com/v1 | https://api.minimaxi.com/anthropic（自动）|
| api_mode | openai | **anthropic_messages**（自动）|
| model | gpt-5.4 | **MiniMax-M3** |
| env var | OPENAI_API_KEY | **MINIMAX_CN_API_KEY** |
| 网络路径 | cc-vibe 第三方代理（不透明）| MiniMax 国内官方 |
| 延迟 | 11.9s（cc-vibe）| **0.86s**（实测）|

## 切换原因（推断）

1. **价格**：gpt-5.4 走第三方代理，价格不透明；MiniMax 国内官方定价低
2. **稳定性**：cc-vibe 第三方代理经常 400（已 patch 修过 2 次）
3. **延迟**：实测 MiniMax-M3 0.86s，gpt-5.4 11.9s
4. **可观测**：MiniMax 官方 API，返回完整 usage（input/output/cache_creation/cache_read tokens）

## 操作步骤

```bash
# 1. 备份
cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.2026-07-10-minimax-2126

# 2. .env 加 MINIMAX_CN_API_KEY（复制 MINIMAX_API_KEY 的值）
echo "MINIMAX_CN_API_KEY=$KEY_VAL" >> ~/.hermes/.env

# 3. config.yaml 改 model 段
# 旧：provider: custom + base_url + api_key + api_mode + default: gpt-5.4 + max_tokens: null
# 新：provider: minimax-cn + default: MiniMax-M3
# （base_url/api_key/api_mode 由 Hermes 内置 profile 自动注入）

# 4. 重启 gateway
systemctl --user restart hermes-gateway.service

# 5. 验证
hermes chat -q "回复一个字:Hi" -m MiniMax-M3
# ✅ 返回 "Hi"
```

## 验证结果

| 测试 | 结果 |
|---|---|
| 单元测试（"回复一个字:Hi"）| ✅ 200 OK，0.86s |
| 复杂测试（带 tool call + ls 命令）| ✅ 4 messages / 2 tool calls，10s |
| systemd 状态 | ✅ active（重启后 PID 3296415 → 新 PID）|
| Yaml 语法 | ✅ Python yaml.safe_load 通过 |
| 日志无 error/timeout | ✅ clean |

## 关键技术细节

### Hermes 内置 MiniMax provider（源：/opt/hermes-venv/lib/python3.12/site-packages/plugins/model-providers/minimax/__init__.py）

3 个 provider profile：

| provider 名 | base_url | env_var | api_mode | 用途 |
|---|---|---|---|---|
| minimax | https://api.minimax.io/anthropic | MINIMAX_API_KEY | anthropic_messages | 海外（国内不通）|
| **minimax-cn** | **https://api.minimaxi.com/anthropic** | **MINIMAX_CN_API_KEY** | anthropic_messages | **国内（我们用这个）**|
| minimax-oauth | https://api.minimax.io/anthropic | OAuth | anthropic_messages | OAuth 流 |

### 关键发现

1. **provider profile 自动注入 base_url/api_key/api_mode**：不用在 config.yaml 里写
2. **api_mode 强制 anthropic_messages**：跟 OpenAI 不兼容（不能用 openai 端点）
3. **endpoint 校验**：`api.minimax.io` 才能用 OpenAI 兼容模式（带 reasoning_split 控制），CN 不行
4. **MiniMax-M3 模型**：默认主模型；M2.7 在 OAuth profile 里

## 配置备份

- `~/.hermes/config.yaml.bak.2026-07-10-minimax-2126`（切换前完整配置）
- `~/.hermes/config.yaml.bak.2026-07-08-23*`（cc-vibe patch 时备份）
- `~/.hermes/config.yaml.bak.2026-07-09-23*`（MiniMax pre-test 时备份）

## 回滚方法

如果新模型出问题要回到 cc-vibe/gpt-5.4：

```bash
# 1. 恢复备份
cp ~/.hermes/config.yaml.bak.2026-07-10-minimax-2126 ~/.hermes/config.yaml

# 2. 重启
systemctl --user restart hermes-gateway.service

# 3. 验证
hermes chat -q "test"
```

## 关联文档

- `/root/vault/1-Projects/德勤/AI-Native/2026-07-08_Hermes_cc-vibe_400_根因与永久修复.md`（之前的 patch）
- `~/.openclaw/workspace/MEMORY.md`（"🔧 OpenClaw gateway" 段）
- `/root/.hermes/.env`（API key 实际值）
