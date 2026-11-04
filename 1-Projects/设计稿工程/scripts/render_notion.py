#!/usr/bin/env python3
"""把 raw/*.json（Notion recordMap）渲染成 markdown 专题文档 + 合订本"""
import json, pathlib, datetime, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "spec" / "notion" / "raw"
PAGES = ROOT / "spec" / "notion" / "pages"
OUT = ROOT / "spec" / "notion"
PAGES.mkdir(parents=True, exist_ok=True)

PIDS = {
    "00｜研发需求 V1.0 总览": "3bd46975-666d-816d-9dcc-c1c0fc7e1321",
    "01｜公共框架、权限与共用验收": "3d846975-666d-8188-aab0-d6e7431b642e",
    "02｜工作：空间、项目、工作包与任务": "3bd46975-666d-8118-9098-f23c95dc7e38",
    "03｜消息：会话、话题与工作衔接": "3bd46975-666d-8154-a642-e6273132e206",
    "04｜客户：后置范围": "40a46975-666d-818a-916b-c7d26c39b8fc",
    "05｜知识：六项能力与资料使用": "3bd46975-666d-81f6-96b2-d4aa56454685",
    "06｜人才：目录、联系与员工配置": "3bd46975-666d-81a0-be61-dc828f74b187",
    "07｜能力：技能、连接与发布版本": "40a46975-666d-813c-8a85-e1ad02e8102f",
    "08｜管理与个人设置": "3bd46975-666d-81b5-84aa-f0249d1b498b",
    "09｜跨模块闭环与联合验收": "3bd46975-666d-810c-8be4-f94adbb4064c",
    "10｜Figma 设计映射与检查结果": "40a46975-666d-816c-8c4c-ddb744ae66dc",
    "决策与待确认项": "3da46975-666d-811d-a267-cfec85178564",
    "OUTIS｜人与 Agent 权限体系设计 V1.0（定稿）": "40d46975-666d-819e-b7c2-d14fae9d79b1",
}

ORDER = [
    ("00｜研发需求 V1.0 总览", "00-总览"),
    ("01｜公共框架、权限与共用验收", "01-公共框架-权限-共用验收"),
    ("02｜工作：空间、项目、工作包与任务", "02-工作"),
    ("03｜消息：会话、话题与工作衔接", "03-消息"),
    ("04｜客户：后置范围", "04-客户后置"),
    ("05｜知识：六项能力与资料使用", "05-知识"),
    ("06｜人才：目录、联系与员工配置", "06-人才"),
    ("07｜能力：技能、连接与发布版本", "07-能力"),
    ("08｜管理与个人设置", "08-管理与个人设置"),
    ("09｜跨模块闭环与联合验收", "09-跨模块闭环与联合验收"),
    ("10｜Figma 设计映射与检查结果", "10-Figma设计映射与检查结果"),
    ("决策与待确认项", "X-决策与待确认项"),
    ("OUTIS｜人与 Agent 权限体系设计 V1.0（定稿）", "X-人与Agent权限体系设计V1.0"),
]


def plain(props, key):
    """Notion 老格式：properties[key] = [ [ "文本", [[style, {}]] ], ... ]"""
    out = []
    for seg in props.get(key) or []:
        if isinstance(seg, list):
            txt = seg[0] if seg and isinstance(seg[0], str) else ""
            style = seg[1] if len(seg) > 1 else []
            for st in style or []:
                if isinstance(st, list) and st:
                    if st[0] == "c":
                        txt = f"`{txt}`"
                    elif st[0] == "b":
                        txt = f"**{txt}**"
                    elif st[0] == "i":
                        txt = f"*{txt}*"
        elif isinstance(seg, str):
            txt = seg
        else:
            txt = seg.get("plain_text", "") if isinstance(seg, dict) else ""
        if txt:
            out.append(txt)
    return "".join(out)


def txt_of(v):
    p = v.get("properties") or {}
    t = v.get("type")
    if "title" in p:
        return plain(p, "title")
    if t in ("rich_text", "equation"):
        return plain(p, t)
    return ""


def block_of(rec, bid):
    b = rec.get(bid) or {}
    v = b.get("value") or {}
    return v.get("value") or v


def render(blocks, recs, depth=0):
    out = []
    for bid in blocks:
        v = block_of(recs, bid)
        if not v:
            continue
        t = v.get("type")
        s = txt_of(v).strip()
        if t in ("page", "child_page"):
            out.append(f"{'#'*min(depth+2,6)} {s}".rstrip())
            continue
        if t == "table_row":
            props = v.get("properties")
            cells = []
            if isinstance(props, dict):
                for cell in props.values():
                    segs = []
                    for seg in (cell or []):
                        if isinstance(seg, list) and seg and isinstance(seg[0], str):
                            segs.append(seg[0])
                        elif isinstance(seg, dict):
                            segs.append(seg.get("plain_text", ""))
                        elif isinstance(seg, str):
                            segs.append(seg)
                    cells.append("".join(segs))
            out.append("| " + " | ".join(c.replace("\n", " ").replace("|", "\\|") for c in cells) + " |")
            continue
        if t == "bulleted_list_item":
            out.append("- " + s)
            out.extend(render(v.get("content") or [], recs, depth + 1))
            continue
        if t == "numbered_list_item":
            out.append("1. " + s)
            out.extend(render(v.get("content") or [], recs, depth + 1))
            continue
        if t == "to_do":
            checked = (v.get("properties") or {}).get("checked")
            out.append(f"- [{'x' if checked else ' '}] {s}")
            out.extend(render(v.get("content") or [], recs, depth + 1))
            continue
        if t == "toggle":
            out.append(f"- **{s}**")
            out.extend(render(v.get("content") or [], recs, depth + 1))
            continue
        if t == "quote":
            out.append(f"> {s}")
            out.extend(render(v.get("content") or [], recs, depth + 1))
            continue
        if t == "callout":
            icon = (v.get("icon") or {}).get("emoji") or ""
            out.append(f"> {icon} {s}")
            out.extend(render(v.get("content") or [], recs, depth + 1))
            continue
        if t == "divider":
            out.append("---")
            continue
        if t == "code":
            lang = (v.get("properties") or {}).get("language") or []
            lang = lang[0] if isinstance(lang, list) and lang else ""
            out.append(f"```{lang}")
            out.append(s)
            out.append("```")
            continue
        if t == "header":
            lvl = (v.get("format") or {}).get("header_level") or 1
            out.append(f"{'#'*min(lvl,6)} {s}")
            out.extend(render(v.get("content") or [], recs, depth))
            continue
        if t == "sub_header":
            out.append(f"### {s}")
            out.extend(render(v.get("content") or [], recs, depth))
            continue
        if t == "sub_sub_header":
            out.append(f"#### {s}")
            out.extend(render(v.get("content") or [], recs, depth))
            continue
        if t in ("paragraph", "text"):
            if s:
                out.append(s)
            out.extend(render(v.get("content") or [], recs, depth))
            continue
        if t in ("image", "video", "embed", "bookmark", "file", "pdf", "audio"):
            cap = (v.get("properties") or {}).get("caption") or []
            c = "".join(x.get("plain_text", "") for x in cap)
            out.append(f"**[{t}]** {c}" if c else f"**[{t}]**")
            continue
        if s:
            out.append(s)
        out.extend(render(v.get("content") or [], recs, depth))
    return out


def fix_tables(lines):
    out, i = [], 0
    while i < len(lines):
        if lines[i].startswith("| ") and i + 1 < len(lines) and lines[i+1].startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("| "):
                rows.append(lines[i]); i += 1
            ncol = rows[0].count("|") - 1
            out.append(rows[0])
            out.append("| " + " | ".join(["---"] * max(ncol, 1)) + " |")
            out.extend(rows[1:])
            continue
        out.append(lines[i]); i += 1
    return out


def main():
    combined = ["# OUTIS｜研发需求 V1.0（Notion 抓取合订本）", "",
                f"> 抓取时间 {datetime.datetime.now():%Y-%m-%d %H:%M} · 来源：Notion 工作区「森森的笔记本」",
                "> 口径：需求文档（与 Figma `00 交付说明｜V1.0` 互为印证；冲突时以「需求文档 + 交付说明」双证为准）", ""]
    stats = []
    for raw_name, slug in ORDER:
        fp = RAW / f"{raw_name}.json"
        if not fp.exists():
            print(f"! 缺 {raw_name}")
            continue
        data = json.loads(fp.read_text())
        recs = (data.get("recordMap") or {}).get("block") or {}
        if not recs:
            print(f"! 空 {raw_name}")
            continue
        # 根块：recordMap.block 里 type=page 且 id 以 pid 结尾
        root = PIDS.get(raw_name)
        if root not in recs:
            root = None
            for bid in recs:
                if block_of(recs, bid).get("type") == "page":
                    root = bid
                    break
        blocks = block_of(recs, root).get("content") or []
        lines = fix_tables(render(blocks, recs))
        md = "\n".join(lines)
        title = raw_name
        md = f"# {title}\n\n" + md
        (PAGES / f"{slug}.md").write_text(md)
        reqs = sorted(set(re.findall(r"\b[A-Z]{2,12}-[A-Z]\d{2}\b", md)))
        dc = sorted(set(re.findall(r"DC-\d{1,2}", md)))
        stats.append((title, len(md), len(reqs), len(dc)))
        combined += [f"\n---\n\n# {title}\n", md]
        print(f"✓ {title}: {len(md)} 字符 / 需求编号 {len(reqs)} / DC {len(dc)}")
    (OUT / "OUTIS｜研发需求 V1.0.md").write_text("\n".join(combined))
    print("\n=== 统计 ===")
    tot_req = set()
    for t, l, r, d in stats:
        print(f"{t[:28]:30s} {l:7d}字符  编号{r:4d}  DC{d:3d}")
    print(f"\n合订本: {OUT/'OUTIS｜研发需求 V1.0.md'}")


if __name__ == "__main__":
    main()
