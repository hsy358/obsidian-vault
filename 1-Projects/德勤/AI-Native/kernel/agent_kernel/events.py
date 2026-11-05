"""事件规范化与注入防护（内核基线 #3：指令数据分离 + 字段白名单）

规则：
1. 外部事件只允许一组"数据字段"，任何试图影响"派活决策"的控制字段一律拒收。
   —— 借鉴 Agent Autoloop：事件里带 cwd / agent / access 的直接丢弃。
2. 外部自由文本（text / 任何字符串字段）**永远不进入提示词**，只作为 payload 落库；
   提示词由规则里的模板 + 经过白名单的结构化字段拼装。
3. 拒收必须留痕（拒收原因入事实表），不得静默丢弃。
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Any

#: 外部事件允许携带的数据字段（白名单）
ALLOWED_EVENT_FIELDS = frozenset(
    {
        "source",  # 事件来源，如 cron / github / gitlab / local
        "type",  # 事件类型，如 cron.fire / issue.opened
        "subject",  # 事件主体标识（同一主体的事件可合并成一轮）
        "text",  # 外部自由文本（只落库，不进提示词）
        "refs",  # 结构化引用（编号、链接、文件名），白名单内的字符串数组
        "fields",  # 额外结构化字段，键必须在 EXTRA_FIELD_WHITELIST 内
        "timestamp",  # 事件发生时间（ISO8601）
    }
)

#: 外部事件**禁止**携带的控制字段（一旦出现 → 整条拒收）
FORBIDDEN_EVENT_FIELDS = frozenset(
    {
        "cwd",
        "agent",
        "access",
        "prompt",
        "skill",
        "command",
        "rule",
        "rules",
        "mode",
        "group",
        "hops",
        "permissions",
        "escalate",
        "auto_approve",
    }
)

#: fields 里允许出现的键（防止在嵌套结构里夹带控制语义）
EXTRA_FIELD_WHITELIST = frozenset(
    {
        "priority",
        "level",
        "severity",
        "repo",
        "issue_number",
        "pipeline_id",
        "job_id",
        "build_id",
        "checked_at",
        "host",
        "count",
        "window",
    }
)

#: refs 里允许出现的 scheme（避免外部 URL 诱导内核去取任意地址）
ALLOWED_REF_SCHEMES = ("http://", "https://", "file://", "path://")

_MAX_TEXT = 20_000


@dataclass(frozen=True)
class NormalizedEvent:
    """通过白名单校验的规范化事件。"""

    source: str
    type: str
    subject: str
    text: str
    refs: tuple[str, ...] = ()
    fields: dict[str, Any] = field(default_factory=dict)
    timestamp: str | None = None

    @property
    def fingerprint(self) -> str:
        """事件指纹：用于同一主体事件的合并判定。"""
        raw = f"{self.source}|{self.type}|{self.subject}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def payload(self) -> dict[str, Any]:
        """落库的 payload（文本在此，只是不进提示词）。"""
        return {
            "source": self.source,
            "type": self.type,
            "subject": self.subject,
            "text": self.text,
            "refs": list(self.refs),
            "fields": self.fields,
            "timestamp": self.timestamp,
            "fingerprint": self.fingerprint,
        }


class EventRejected(ValueError):
    """事件被拒收。reason 用于留痕。"""

    def __init__(self, reason: str, detail: dict[str, Any] | None = None) -> None:
        super().__init__(reason)
        self.reason = reason
        self.detail = detail or {}


def _check_ref(ref: str) -> str:
    if not isinstance(ref, str):
        raise EventRejected("refs 只允许字符串")
    if len(ref) > 2000:
        raise EventRejected("refs 条目过长")
    if "://" in ref and not ref.startswith(ALLOWED_REF_SCHEMES):
        raise EventRejected(f"refs scheme 不在白名单: {ref[:60]}")
    return ref


def normalize(raw: dict[str, Any]) -> NormalizedEvent:
    """把外部原始事件规范化；不合规即抛 EventRejected。

    注意：这里**不做**任何"猜测式修复"——安全基线要求宁可拒收，不可带病执行。
    """
    if not isinstance(raw, dict):
        raise EventRejected("事件必须是对象")

    # 1) 控制字段检测（先于一切读取）
    forbidden = sorted(set(raw.keys()) & FORBIDDEN_EVENT_FIELDS)
    if forbidden:
        raise EventRejected(
            f"事件含禁止的控制字段: {','.join(forbidden)}",
            {"forbidden": forbidden},
        )

    # 2) 未知顶层字段检测
    unknown = sorted(set(raw.keys()) - ALLOWED_EVENT_FIELDS)
    if unknown:
        raise EventRejected(
            f"事件含白名单外字段: {','.join(unknown)}",
            {"unknown": unknown},
        )

    source = raw.get("source")
    etype = raw.get("type")
    subject = raw.get("subject") or ""
    if not source or not isinstance(source, str):
        raise EventRejected("source 缺失或类型错误")
    if not etype or not isinstance(etype, str):
        raise EventRejected("type 缺失或类型错误")
    if not isinstance(subject, str) or len(subject) > 200:
        raise EventRejected("subject 类型错误或过长")

    text = raw.get("text", "")
    if not isinstance(text, str):
        raise EventRejected("text 必须是字符串")
    if len(text) > _MAX_TEXT:
        text = text[:_MAX_TEXT] + f"...[truncated {len(text) - _MAX_TEXT} chars]"

    refs_raw = raw.get("refs", []) or []
    if not isinstance(refs_raw, list) or len(refs_raw) > 50:
        raise EventRejected("refs 必须是长度 <= 50 的数组")
    refs = tuple(_check_ref(r) for r in refs_raw)

    fields_raw = raw.get("fields", {}) or {}
    if not isinstance(fields_raw, dict):
        raise EventRejected("fields 必须是对象")
    bad_fields = sorted(set(fields_raw.keys()) - EXTRA_FIELD_WHITELIST)
    if bad_fields:
        raise EventRejected(
            f"fields 含白名单外键: {','.join(bad_fields)}",
            {"bad_fields": bad_fields},
        )
    fields = {k: v for k, v in fields_raw.items()}

    timestamp = raw.get("timestamp")
    if timestamp is not None and not isinstance(timestamp, str):
        raise EventRejected("timestamp 必须是字符串")

    return NormalizedEvent(
        source=source,
        type=etype,
        subject=subject,
        text=text,
        refs=refs,
        fields=fields,
        timestamp=timestamp,
    )


_CONTROL_PATTERNS = (
    re.compile(r"ignore\s+(all\s+)?previous", re.I),
    re.compile(r"忽略(上面|以上|之前|前面)", re.I),
    re.compile(r"disregard\s+(the\s+)?system", re.I),
    re.compile(r"you\s+are\s+now\b", re.I),
)


def looks_like_injection(text: str) -> list[str]:
    """检测外部文本里的提示词注入迹象（命中即在审计里标注，不删除原文）。

    策略：**不删原文、不静默**，只标记并让规则决定是否升级为人工确认。
    """
    hits = []
    for pat in _CONTROL_PATTERNS:
        m = pat.search(text or "")
        if m:
            hits.append(m.group(0))
    return hits


def json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
