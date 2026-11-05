"""规则加载与确定性匹配（内核基线 #2/#7/#8）

- 规则是**人工维护 + 确定性匹配**的，内核不调用模型、不做 AI 自规划。
- 每份规则集带 version 与内容哈希（sha256），派活时写入 run —— 授权可审计、可回溯。
- Agent 描述是厂商中立的：只认 {name, use, access, command?}，不认识 Claude / Codex / Hermes。
- rule.mode 支持 observe（只记录不执行）/ dry（走空执行器）/ execute（真派活）。
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

#: 厂商中立的 Agent 描述允许的键
ALLOWED_AGENT_KEYS = frozenset({"name", "use", "access", "command"})

#: 允许的执行器类型（use）—— 只是一个**标识**，内核不关心背后是谁
ALLOWED_USES = frozenset({"hermes-chat", "claude-code", "langgraph", "custom", "dryrun"})

VALID_MODES = frozenset({"observe", "dry", "execute"})


class RuleError(ValueError):
    """规则不合法。"""


@dataclass(frozen=True)
class AgentSpec:
    """厂商中立的 Agent 描述。"""

    name: str
    use: str
    access: tuple[str, ...] = ()
    command: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"name": self.name, "use": self.use, "access": list(self.access)}
        if self.command:
            d["command"] = list(self.command)
        return d


@dataclass(frozen=True)
class Rule:
    name: str
    source: str
    types: tuple[str, ...]
    to: AgentSpec
    cwd: str | None
    skill: str | None
    prompt: str
    mode: str
    group: str
    parallel: int
    max_hops: int

    def matches(self, source: str, etype: str) -> bool:
        """确定性匹配：source 全等 + type 前缀命中（支持 "cron.*" 通配）。"""
        if self.source != source:
            return False
        if not self.types:
            return False
        for pat in self.types:
            if pat == "*" or pat == etype:
                return True
            if pat.endswith(".*") and etype.startswith(pat[:-1]):
                return True
        return False


@dataclass(frozen=True)
class RuleSet:
    version: int
    digest: str
    rules: tuple[Rule, ...]
    path: str | None = None

    def find(self, source: str, etype: str) -> list[Rule]:
        return [r for r in self.rules if r.matches(source, etype)]


def _require(cond: bool, msg: str) -> None:
    if not cond:
        raise RuleError(msg)


def _parse_agent(raw: Any, rule_name: str) -> AgentSpec:
    _require(isinstance(raw, dict), f"规则 {rule_name}: to 必须是对象")
    unknown = sorted(set(raw.keys()) - ALLOWED_AGENT_KEYS)
    _require(not unknown, f"规则 {rule_name}: Agent 描述含厂商/控制字段外的键 {unknown}")
    name = raw.get("name")
    use = raw.get("use")
    _require(isinstance(name, str) and name, f"规则 {rule_name}: Agent 缺 name")
    _require(isinstance(use, str) and use, f"规则 {rule_name}: Agent 缺 use")
    _require(use in ALLOWED_USES, f"规则 {rule_name}: use={use} 不在允许列表 {sorted(ALLOWED_USES)}")
    access = raw.get("access", []) or []
    _require(isinstance(access, list) and all(isinstance(a, str) for a in access),
             f"规则 {rule_name}: access 必须是字符串数组")
    command = raw.get("command", []) or []
    _require(isinstance(command, list) and all(isinstance(c, str) for c in command),
             f"规则 {rule_name}: command 必须是字符串数组")
    return AgentSpec(name=name, use=use, access=tuple(access), command=tuple(command))


def parse_ruleset(raw: dict[str, Any], path: str | None = None) -> RuleSet:
    version = raw.get("version")
    _require(isinstance(version, int) and version > 0, "rules 必须带正整数 version")
    rules_raw = raw.get("rules")
    _require(isinstance(rules_raw, list), "rules 必须是数组")
    _require(len(rules_raw) <= 500, "rules 数量超过上限 500")

    rules: list[Rule] = []
    seen: set[str] = set()
    for item in rules_raw:
        _require(isinstance(item, dict), "每条规则必须是对象")
        name = item.get("name")
        _require(isinstance(name, str) and name, "规则缺 name")
        _require(name not in seen, f"规则名重复: {name}")
        seen.add(name)

        when = item.get("when", {}) or {}
        _require(isinstance(when, dict), f"规则 {name}: when 必须是对象")
        unknown_when = sorted(set(when.keys()) - {"source", "types"})
        _require(not unknown_when, f"规则 {name}: when 含未知键 {unknown_when}")
        source = when.get("source")
        types = when.get("types", []) or []
        _require(isinstance(source, str) and source, f"规则 {name}: when.source 必填")
        _require(isinstance(types, list) and types, f"规则 {name}: when.types 必填")

        mode = item.get("mode", "execute")
        _require(mode in VALID_MODES, f"规则 {name}: mode={mode} 非法，应为 {sorted(VALID_MODES)}")

        prompt = item.get("prompt", "")
        _require(isinstance(prompt, str), f"规则 {name}: prompt 必须是字符串")
        _require(len(prompt) <= 20_000, f"规则 {name}: prompt 过长")

        cwd = item.get("cwd")
        if cwd is not None:
            _require(isinstance(cwd, str), f"规则 {name}: cwd 必须是字符串")
            _require(os.path.isabs(cwd), f"规则 {name}: cwd 必须是绝对路径")

        skill = item.get("skill")
        if skill is not None:
            _require(isinstance(skill, str), f"规则 {name}: skill 必须是字符串")

        group = item.get("group", name)
        _require(isinstance(group, str) and group, f"规则 {name}: group 必须是字符串")

        parallel = item.get("parallel", 1)
        _require(isinstance(parallel, int) and 1 <= parallel <= 8,
                 f"规则 {name}: parallel 必须是 1..8 的整数")

        max_hops = item.get("max_hops", 8)
        _require(isinstance(max_hops, int) and 1 <= max_hops <= 8,
                 f"规则 {name}: max_hops 必须是 1..8 的整数")

        rules.append(
            Rule(
                name=name,
                source=source,
                types=tuple(types),
                to=_parse_agent(item.get("to"), name),
                cwd=cwd,
                skill=skill,
                prompt=prompt,
                mode=mode,
                group=group,
                parallel=parallel,
                max_hops=max_hops,
            )
        )

    canonical = json.dumps(raw, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return RuleSet(version=version, digest=digest, rules=tuple(rules), path=path)


def load_ruleset(path: str | Path) -> RuleSet:
    p = Path(path)
    _require(p.exists(), f"规则文件不存在: {p}")
    raw = json.loads(p.read_text(encoding="utf-8"))
    return parse_ruleset(raw, path=str(p))


def render_prompt(rule: Rule, event_fields: dict[str, Any]) -> str:
    """拼装提示词 —— **只来自规则模板 + 白名单结构化字段**。

    外部自由文本不在这里（它躺在事件 payload 里，需要时由 Agent 自己去读）。
    """
    parts = [rule.prompt.strip(), "", "【本次事件（结构化，已校验）】"]
    for key in sorted(event_fields):
        parts.append(f"- {key}: {event_fields[key]}")
    if rule.skill:
        parts += ["", f"【指定 skill】{rule.skill}"]
    if rule.cwd:
        parts += ["", f"【工作目录】{rule.cwd}"]
    parts += [
        "",
        "【回执】结论写在回复第一行；如需人工拍板，附一段 ```agent-kernel 代码块，"
        "内容为 {\"ask\":[{\"title\":\"...\",\"text\":\"...\",\"options\":[\"...\"],\"key\":\"...\"}]}。"
        "字符串内部禁止出现英文双引号（需要引号请用中文括号），只允许一个代码块。",
    ]
    return "\n".join(parts)


_SECRET = re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[=:]\s*\S+")


def redact(text: str) -> str:
    """对要写入日志的文本做最小脱敏（避免密钥进事实表）。"""
    return _SECRET.sub(r"\1=[REDACTED]", text or "")
