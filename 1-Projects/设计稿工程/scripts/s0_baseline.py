#!/usr/bin/env python3
"""
S0 组件基线生成器 —— 为「600+ 设计稿大工程」建立组件级视觉基线

用途:
  1. 把 Figma 里 155 个 COMPONENT 逐个渲染成 PNG（scale=2）→ 组件库截图基线
  2. 渲染 90 规范页 / 91 组件源页 的图板 → tokens 权威截图
  3. 输出 component-baseline-manifest.json + 组件基线目录（含尺寸/命名）

用法:
  export FIGMA_TOKEN=figd_xxx
  python3 s0_baseline.py
"""
import os, json, sys, time, urllib.request, urllib.error, urllib.parse, pathlib, datetime

TOKEN = os.environ.get("FIGMA_TOKEN", "").strip()
KEY = os.environ.get("FIGMA_KEY", "0f4FTbWCeMRIRcCGCBELe4").strip()
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "figma-assets"
BASE = OUT / "component-baseline"
BASE.mkdir(parents=True, exist_ok=True)
API = "https://api.figma.com/v1"

SPEC_PAGES = {"90 规范｜色彩与字阶", "91 组件源｜通用控件与图标"}


def get(path, **params):
    if not TOKEN:
        sys.exit("缺少 FIGMA_TOKEN")
    q = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items() if v is not None)
    url = f"{API}{path}" + (f"?{q}" if q else "")
    req = urllib.request.Request(url, headers={"X-Figma-Token": TOKEN})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:300]
            if e.code == 429:
                time.sleep(5 * (attempt + 1)); continue
            sys.exit(f"HTTP {e.code} {path}\n{body}")
        except Exception as e:
            if attempt == 3: sys.exit(f"ERR {path}: {e}")
            time.sleep(3)
    sys.exit("retry exhausted")


def slug(s, maxlen=60):
    keep = "-_./ ·"
    out = "".join(c if (c.isalnum() or c in keep) else "-" for c in s)
    out = out.replace("/", "__").strip("-")
    return out[:maxlen]


def render(ids, scale=2):
    """分批渲染 ids -> {id: local_path}"""
    res = {}
    batches = [ids[i:i+50] for i in range(0, len(ids), 50)]
    for bi, batch in enumerate(batches):
        r = get(f"/images/{KEY}", ids=",".join(batch), format="png", scale=scale)
        for fid, url in (r.get("images") or {}).items():
            if not url:
                continue
            fn = BASE / f"{fid.replace(':', '_')}.png"
            try:
                with urllib.request.urlopen(url, timeout=180) as resp:
                    fn.write_bytes(resp.read())
                res[fid] = fn
            except Exception as e:
                print(f"  ! 下载失败 {fid}: {e}")
        print(f"  批次 {bi+1}/{len(batches)} 完成 ({len(batch)} 个)")
        time.sleep(1)
    return res


def main():
    structure = json.loads((OUT / "structure.json").read_text())
    comps, specs = [], []
    for p in structure:
        for f in p["frames"]:
            row = {"page": p["name"], "id": f["id"], "name": f["name"],
                   "type": f["type"], "w": f.get("w"), "h": f.get("h")}
            if f["type"] == "COMPONENT":
                comps.append(row)
            if p["name"] in SPEC_PAGES and f["type"] in ("FRAME", "COMPONENT"):
                specs.append(row)

    print(f"组件 {len(comps)} 个，规范页图板 {len(specs)} 个 → 开始渲染")
    paths = render([c["id"] for c in comps] + [s["id"] for s in specs])

    manifest = []
    for row in comps + specs:
        fn = paths.get(row["id"])
        if not fn:
            continue
        row = dict(row)
        row["file"] = str(fn.relative_to(ROOT))
        row["bytes"] = fn.stat().st_size
        manifest.append(row)

    (OUT / "component-baseline-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2))

    # 组件基线目录（按组件源页分组）
    md = ["# 组件视觉基线目录（S0）", "",
          f"> 生成 {datetime.datetime.now():%Y-%m-%d %H:%M} · 组件 {len(comps)} · 规范图板 {len(specs)}",
          "> PNG 均为 Figma 渲染 scale=2，作为组件库视觉回归的唯一基线。", ""]
    by_page = {}
    for m in manifest:
        by_page.setdefault(m["page"], []).append(m)
    for page, rows in by_page.items():
        md.append(f"\n## {page}（{len(rows)}）\n")
        md.append("| 组件名 | 尺寸 | id | 基线 |")
        md.append("|---|---|---|---|")
        for r in sorted(rows, key=lambda x: x["name"]):
            w = f"{int(r['w'])}×{int(r['h'])}" if r.get("w") else "-"
            md.append(f"| {r['name']} | {w} | `{r['id']}` | `{r['file']}` |")
    (OUT / "component-baseline-catalog.md").write_text("\n".join(md))
    print(f"✓ 落盘 {len(manifest)} 张基线 → {BASE}")
    print(f"✓ manifest: {OUT/'component-baseline-manifest.json'}")


if __name__ == "__main__":
    main()
