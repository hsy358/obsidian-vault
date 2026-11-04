#!/usr/bin/env python3
"""
Figma 抓取器 —— 为「600+ 设计稿大工程」准备素材
用法:
  export FIGMA_TOKEN=figd_xxx
  export FIGMA_KEY=0f4FTbWCeMRIRcCGCBELe4
  python3 figma_pull.py variables      # 拉 local variables → tokens.json
  python3 figma_pull.py structure      # 拉页面/frame 树 → design-inventory.md
  python3 figma_pull.py components     # 拉组件清单 → components.md
  python3 figma_pull.py images <n>     # 拉前 n 个 frame 的 PNG 基线
  python3 figma_pull.py all
"""
import os, json, sys, time, urllib.request, urllib.error, pathlib, datetime

TOKEN = os.environ.get("FIGMA_TOKEN", "").strip()
KEY = os.environ.get("FIGMA_KEY", "0f4FTbWCeMRIRcCGCBELe4").strip()
OUT = pathlib.Path(os.environ.get("FIGMA_OUT", pathlib.Path(__file__).resolve().parent.parent / "figma-assets"))
BASE = "https://api.figma.com/v1"

def get(path, **params):
    if not TOKEN:
        sys.exit("缺少 FIGMA_TOKEN")
    q = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
    url = f"{BASE}{path}" + (f"?{q}" if q else "")
    req = urllib.request.Request(url, headers={"X-Figma-Token": TOKEN})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:300]
            if e.code == 429:
                time.sleep(3 * (attempt + 1)); continue
            sys.exit(f"HTTP {e.code} {path}\n{body}")
        except Exception as e:
            if attempt == 2: sys.exit(f"ERR {path}: {e}")
            time.sleep(2)
    sys.exit("retry exhausted")

def w(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / name
    if isinstance(data, (dict, list)):
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        p.write_text(str(data))
    print(f"→ {p}  ({p.stat().st_size/1024:.1f} KB)")
    return p

def flatten_variables(variables_meta, values_by_mode):
    """Figma variables: meta 里是结构，values_by_mode 里是实际值"""
    out = {}
    def walk(vid, node):
        nm = node.get("name", vid)
        for k, v in (node.get("valuesByMode") or {}).items():
            out.setdefault(nm, {})[k] = v
        for child in node.get("children") or []:
            walk(child.get("id", child.get("name", "")), child)
    for vid, node in (variables_meta.get("meta", {}).get("variables") or {}).items():
        walk(vid, node)
    resolved = {}
    for name, modes in out.items():
        resolved[name] = {}
        for mode, v in modes.items():
            resolved[name][mode] = {
                "type": v.get("type"), "value": v.get("value"),
                "resolvedType": v.get("resolvedType"),
                "variableId": (v.get("variableId") or (v.get("id") if isinstance(v, dict) else None)),
            }
    # 用 values_by_mode 补真实值
    for vid, modes in (values_by_mode.get("values") or {}).items():
        nm = (variables_meta.get("meta", {}).get("variables", {}).get(vid, {}) or {}).get("name")
        if not nm: continue
        for mode, v in modes.items():
            resolved.setdefault(nm, {})[mode] = {"type": "resolved", "value": v}
    return resolved

def cmd_variables():
    meta = get(f"/files/{KEY}/variables/local")
    vals = get(f"/files/{KEY}/variables/local", **{}) if False else meta
    data = {"meta": meta.get("meta"), "resolved": flatten_variables(meta.get("meta", {}), meta)}
    w("tokens.raw.json", data)
    # 同时产出扁平 CSV 便于人审
    rows = ["name,modes,values"]
    for name, modes in sorted(data["resolved"].items()):
        rows.append(f"{name}," + ";".join(f"{m}={str((d or {}).get('value'))}" for m, d in modes.items()))
    w("tokens.csv", "\n".join(rows))
    print(f"变量数: {len(data['resolved'])}")

def cmd_structure():
    doc = get(f"/files/{KEY}", depth=3)
    pages = []
    for p in doc.get("document", {}).get("children", []):
        frames = []
        def walk(n, depth=0):
            for c in n.get("children", []) or []:
                if c.get("type") == "FRAME" or c.get("type") == "COMPONENT":
                    frames.append({"id": c["id"], "name": c.get("name"), "type": c.get("type"),
                                   "w": c.get("absoluteBoundingBox", {}).get("width"),
                                   "h": c.get("absoluteBoundingBox", {}).get("height")})
                if depth < 3: walk(c, depth + 1)
        walk(p)
        pages.append({"id": p["id"], "name": p.get("name"), "frames": frames})
    w("structure.json", pages)
    total = sum(len(p["frames"]) for p in pages)
    md = [f"# 设计稿结构清单\n", f"文件 key: `{KEY}`", f"生成时间: {datetime.datetime.now():%Y-%m-%d %H:%M}", f"页面数: {len(pages)} / 顶层 frame 数: {total}\n"]
    for p in pages:
        md.append(f"\n## {p['name']}  ({len(p['frames'])} frames)\n")
        md.append("| frame 名 | 类型 | 尺寸 | id |")
        md.append("|---|---|---|---|")
        for f in p["frames"][:400]:
            md.append(f"| {f['name']} | {f['type']} | {f['w']}×{f['h']} | `{f['id']}` |")
    w("design-inventory.md", "\n".join(md))
    print(f"页面 {len(pages)}，frame {total}")

def cmd_components():
    data = get(f"/files/{KEY}/components")
    w("components.json", data)
    md = ["# 组件清单\n"]
    for k, v in (data.get("meta", {}) or {}).items():
        md.append(f"## {k}\n")
        for c in v or []:
            md.append(f"- **{c.get('name')}** `{c.get('description','')}` id=`{c.get('key')}`")
    w("components.md", "\n".join(md))

def cmd_images(n=10):
    doc = get(f"/files/{KEY}", depth=3)
    ids = []
    def walk(node):
        for c in node.get("children", []) or []:
            if c.get("type") in ("FRAME", "COMPONENT"):
                ids.append(c["id"])
            walk(c)
    walk(doc.get("document", {}))
    ids = ids[:n]
    print(f"导出 {len(ids)} 个 frame")
    res = get(f"/images/{KEY}", ids=",".join(ids), format="png", scale=2)
    base = OUT / "baseline"; base.mkdir(parents=True, exist_ok=True)
    manifest = []
    for fid, url in (res.get("images") or {}).items():
        if not url: continue
        fn = base / f"{fid.replace(':', '_')}.png"   # Figma node id contains ":" -> illegal on NTFS
        with urllib.request.urlopen(url, timeout=120) as r:
            fn.write_bytes(r.read())
        manifest.append({"id": fid, "file": str(fn), "size": fn.stat().st_size})
    w("baseline-manifest.json", manifest)
    print(f"PNG 落盘 {len(manifest)} 张 → {base}")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("variables", "all"): cmd_variables()
    if cmd in ("structure", "all"): cmd_structure()
    if cmd in ("components", "all"): cmd_components()
    if cmd in ("images", "all"): cmd_images(int(sys.argv[2]) if len(sys.argv) > 2 else 10)
