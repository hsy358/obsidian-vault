#!/usr/bin/env python3
"""
Notion 需求文档抓取器 —— OUTIS｜研发需求 V1.0（十专题 + 决策项 + 权限定稿）

用法:
  export NOTION_COOKIE="notion_user_id=...; notion_sync_user_id=..."
  python3 notion_pull.py

产物（存 vault）:
  spec/notion/OUTIS｜研发需求 V1.0.md        十专题合订本
  spec/notion/raw/<page>.json                原始 block JSON（留证）
  spec/notion/pages/<page>.md                分页 markdown
"""
import os, json, re, time, urllib.request, urllib.error, pathlib, datetime, http.cookiejar

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "spec" / "notion"
PAGES_DIR = OUTDIR / "pages"
RAW_DIR = OUTDIR / "raw"
OUTDIR.mkdir(parents=True, exist_ok=True)
PAGES_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)

API = "https://www.notion.so/api/v3/loadPageChunk"

PAGES = [
    ("00-总览", "3bd46975-666d-816d-9dcc-c1c0fc7e1321"),
    ("01-公共框架权限与共用验收", "3d846975-666d-8188-aab0-d6e7431b642e"),
    ("02-工作", "3bd46975-666d-8118-9098-f23c95dc7e38"),
    ("03-消息", "3bd46975-666d-8154-a642-e6273132e206"),
    ("04-客户后置", "40a46975-666d-818a-916b-c7d26c39b8fc"),
    ("05-知识", "3bd46975-666d-81f6-962b-2d4aa56454685"),
    ("06-人才", "3bd46975-666d-81a0-be61-dc828f74b187"),
    ("07-能力", "40a46975-666d-813c-8a85-e1ad02e8102f"),
    ("08-管理与个人设置", "3bd46975-666d-81b5-84aa-f0249d1b498b"),
    ("09-跨模块闭环与联合验收", "3bd46975-666d-810c-8be4-f94adbb4064c"),
    ("10-Figma设计映射与检查结果", "40a46975-666d-816c-8c4c-ddb744ae66dc"),
    ("X-决策与待确认项", "3da46975-666d-811d-a267-cfec85178564"),
    ("X-人与Agent权限体系设计V1.0", "40d46975-666d-819e-b7c2-d14fae9d79b1"),
]


def cookie_header():
    c = os.environ.get("NOTION_COOKIE", "").strip()
    if not c:
        sys.exit("缺少 NOTION_COOKIE")
    return c


def load_page(pid):
    body = json.dumps({"pageId": pid, "limit": 2000, "cursor": {"stack": []},
                       "chunkNumber": 0, "verticalColumns": False}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Content-Type": "application/json",
        "Cookie": cookie_header(),
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/144 Safari/537.36",
        "Origin": "https://www.notion.so",
        "Referer": "https://www.notion.so/",
    })
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def rich_text(props, key="title"):
    out = []
    for t in props.get(key) or []:
        txt = t.get("plain_text") or ""
        if not txt:
            continue
        ann = t.get("annotations") or {}
        prefix = ""
        if ann.get("code"):
            txt = f"`{txt}`"
        if ann.get("bold"):
            txt = f"**{txt}**"
        out.append(txt)
    return "".join(out)


def block_text(b):
    v = b.get("value") or {}
    p = v.get("properties") or {}
    t = v.get("type")
    if t in ("title", "rich_text", "equation"):
        return rich_text(p, t)
    return ""


def is_heading(v):
    return v.get("type") == "header"


def render_blocks(blocks, recs, depth=0):
    """按 content 顺序递归渲染成 markdown"""
    out = []
    for bid in blocks:
        b = recs.get(bid)
        if not b:
            continue
        v = b.get("value") or {}
        t = v.get("type")
        txt = block_text(b).strip()
        if t == "page" or t == "child_page":
            title = txt or (v.get("title") or "")
            out.append(f"{'#'*(min(depth+2,6))} {title}".rstrip())
            continue
        if t == "table":
            w = (v.get("format") or {}).get("table_width")
            h = (v.get("format") or {}).get("table_header")
            out.append(f"<!-- table {w}x -->")
            out.append("")
            out.extend(render_blocks(v.get("content") or [], recs, depth))
            continue
        if t == "table_row":
            cells = []
            for cell in v.get("properties", {}).values() if isinstance(v.get("properties"), dict) else []:
                cells.append("".join(x.get("plain_text", "") for x in (cell or [])))
            out.append("| " + " | ".join(c.replace("\n", " ").replace("|", "\\|") for c in cells) + " |")
            continue
        if t in ("bulleted_list_item", "numbered_list_item"):
            prefix = "- " if t == "bulleted_list_item" else "1. "
            body = render_blocks(v.get("content") or [], recs, depth + 1)
            if body:
                out.append(prefix + txt)
                out.extend(body)
            else:
                out.append(prefix + txt)
            continue
        if t == "to_do":
            mark = "x" if (v.get("properties") or {}).get("checked") else " "
            out.append(f"- [{mark}] {txt}")
            out.extend(render_blocks(v.get("content") or [], recs, depth + 1))
            continue
        if t in ("toggle", "quote", "callout", "divider", "code", "image", "video", "embed", "bookmark"):
            if t == "toggle":
                out.append(f"- **{txt}**")
                out.extend(render_blocks(v.get("content") or [], recs, depth + 1))
            elif t == "quote":
                out.append(f"> {txt}")
                out.extend(render_blocks(v.get("content") or [], recs, depth + 1))
            elif t == "callout":
                icon = (v.get("icon") or {}).get("emoji") or ""
                out.append(f"> {icon} {txt}")
                out.extend(render_blocks(v.get("content") or [], recs, depth + 1))
            elif t == "divider":
                out.append("---")
            elif t == "code":
                lang = (v.get("properties") or {}).get("language") or ""
                lang = lang[0] if isinstance(lang, list) and lang else ""
                out.append(f"```{lang}")
                out.append(txt)
                out.append("```")
            else:
                cap = (v.get("properties") or {}).get("caption") or []
                capstr = "".join(x.get("plain_text", "") for x in cap)
                if capstr:
                    out.append(f"[{t}] {capstr}")
                else:
                    out.append(f"[{t}]")
            continue
        # 标题族
        if t == "header":
            lvl = v.get("format", {}).get("header_level") or 1
            out.append(f"{'#'*min(lvl,6)} {txt}")
            out.extend(render_blocks(v.get("content") or [], recs, depth))
            continue
        if t == "sub_header":
            out.append(f"### {txt}")
            out.extend(render_blocks(v.get("content") or [], recs, depth))
            continue
        if t == "sub_sub_header":
            out.append(f"#### {txt}")
            out.extend(render_blocks(v.get("content") or [], recs, depth))
            continue
        if t == "paragraph":
            if txt:
                out.append(txt)
                out.extend(render_blocks(v.get("content") or [], recs, depth))
            else:
                out.extend(render_blocks(v.get("content") or [], recs, depth))
            continue
        if txt:
            out.append(txt)
        out.extend(render_blocks(v.get("content") or [], recs, depth))
    return out


def table_fix(lines):
    """把 table_row 序列组装成 markdown 表格"""
    out, i = [], 0
    while i < len(lines):
        if lines[i].startswith("| ") and i + 1 < len(lines) and lines[i + 1].startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("| "):
                rows.append(lines[i]); i += 1
            if len(rows) >= 1:
                header = rows[0]
                sep = "| " + " | ".join(["---"] * (header.count("|") - 1)) + " |"
                out.append(header); out.append(sep)
                out.extend(rows[1:])
            continue
        out.append(lines[i]); i += 1
    return out


def main():
    combined = [f"# OUTIS｜研发需求 V1.0（Notion 抓取）", "",
                f"> 抓取时间 {datetime.datetime.now():%Y-%m-%d %H:%M} · 来源 Notion 工作区「森森的笔记本」",
                "> 口径：需求文档（与 Figma `00 交付说明` 互为印证）", ""]
    alljson = {}
    for name, pid in PAGES:
        try:
            j = load_page(pid)
        except Exception as e:
            print(f"! {name} 失败: {e}")
            continue
        recs = j.get("recordMap", {}).get("block", {})
        alljson[name] = {"pageId": pid, "recordMap": j.get("recordMap")}
        root = recs.get(pid, {})
        root_val = root.get("value", {})
        blocks = root_val.get("content") or []
        lines = render_blocks(blocks, recs)
        lines = table_fix(lines)
        md = "\n".join(lines)
        (RAW_DIR / f"{name}.json").write_text(json.dumps(j.get("recordMap"), ensure_ascii=False))
        (PAGES_DIR / f"{name}.md").write_text(md)
        print(f"✓ {name}: {len(md)} 字符 / {len(blocks)} 顶层块")
        combined += [f"\n---\n\n# 专题：{name}\n", md]
    (OUTDIR / "OUTIS｜研发需求 V1.0.md").write_text("\n".join(combined))
    print(f"\n✓ 合订本: {OUTDIR/'OUTIS｜研发需求 V1.0.md'}")


if __name__ == "__main__":
    main()
