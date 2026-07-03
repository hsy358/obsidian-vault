#!/usr/bin/env bash
# 一键把 hesiyan-agent-skills 链接到各家 Agent 的 skills 目录
# 兼容：Claude Code / Codex / OpenCode / Gemini CLI

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/skills"

# 安全兜底：不覆盖已有同名目录
link_to_dir() {
  local target="$1"
  local label="$2"

  if [ -d "$target" ]; then
    # 已存在同名目录，跳过
    if [ -L "$target" ]; then
      echo "  ✓ $label (symlink already linked)"
      return 0
    fi
    echo "  ⚠️  $label exists but is a real dir, skip (manually manage)"
    return 0
  fi

  if mkdir -p "$(dirname "$target")" 2>/dev/null; then
    ln -s "$SKILLS_SRC" "$target"
    echo "  ✓ $label linked → $target"
  else
    echo "  ✗ $label failed"
  fi
}

echo "hesiyan-agent-skills 一键安装"
echo ""

# Claude Code: ~/.claude/skills/
if [ -d "$HOME/.claude" ] || [ -n "${INSTALL_CLAUDE:-}" ]; then
  link_to_dir "$HOME/.claude/skills/hesiyan-agent-skills" "Claude Code"
fi

# Codex: ~/.codex/skills/
if [ -d "$HOME/.codex" ] || [ -n "${INSTALL_CODEX:-}" ]; then
  link_to_dir "$HOME/.codex/skills/hesiyan-agent-skills" "Codex"
fi

# OpenCode: ~/.opencode/skills/obsidian-skills/ 全仓
if [ -d "$HOME/.opencode" ] || [ -n "${INSTALL_OPENCODE:-}" ]; then
  link_to_dir "$HOME/.opencode/skills/hesiyan-agent-skills" "OpenCode"
fi

echo ""
echo "Done. 验证: ls -la ~/.claude/skills/ 之类的目录能看到 hesiyan-agent-skills → /path/skills"
echo ""
echo "启用：restart Claude Code / Codex / OpenCode 后 skill 自动发现"
