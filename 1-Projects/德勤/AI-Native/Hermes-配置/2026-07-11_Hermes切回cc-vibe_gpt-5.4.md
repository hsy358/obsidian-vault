# Hermes 切回 cc-vibe/gpt-5.4（2026-07-11）

## 背景

何大人 2026-07-10 21:23 切到 minimax-cn/MiniMax-M3，2026-07-11 00:42 又切回 custom/cc-vibe/gpt-5.4。

## 切换操作

**精准切换 model 段**，不破坏其他配置：
- provider: minimax-cn → **custom**
- default: MiniMax-M3 → **gpt-5.4**
- 恢复 base_url / api_key / api_mode / max_tokens: null（cc-vibe patch 必备）
- **保留**新增的 command_allowlist（delete in root path / find -delete）

## 备份位置

`~/.hermes/config.yaml.bak.2026-07-10-minimax-2126`（切到 minimax-cn 前的版本，含 cc-vibe 完整配置）

## 验证

- Yaml 语法 ✅ Python yaml.safe_load 通过
- systemd restart ✅ active
- 单测 "回复一个字:Hi" + gpt-5.4 模型 → 见会话记录

## 关联

- 切到 minimax-cn 的文档：`2026-07-10_Hermes切换MiniMax-M3模型.md`
- cc-vibe 400 修复文档：`2026-07-08_Hermes_cc-vibe_400_根因与永久修复.md`
