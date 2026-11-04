#!/usr/bin/env python3
"""
派单包生成器 —— 把 Figma 屏幕翻译成「Worker 可直接开工」的 ticket

用法:
  export FIGMA_TOKEN=figd_xxx
  python3 gen_tickets.py --page "10 工作｜发起与项目" --limit 3
  python3 gen_tickets.py --ids 446:172,448:1594,449:288 --out spec/tickets/pilot-S1-01.md

产物:
  figma-assets/baseline/<id>.png        屏幕基线（scale=2）
  spec/tickets/<out>.md                 派单包（含验收命令）
  spec/tickets/<out>.json              机器可读 ticket 列表
"""
import os, json, sys, time, urllib.request, urllib.error, urllib.parse, pathlib, argparse, datetime

TOKEN = os.environ.get("FIGMA_TOKEN", "").strip()
KEY = os.environ.get("FIGMA_KEY", "0f4FTbWCeMRIRcCGCBELe4").strip()
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "figma-assets"
BASE = OUT / "baseline"
BASE.mkdir(parents=True, exist_ok=True)
TICKETS = ROOT / "spec" / "tickets"
TICKETS.mkdir(parents=True, exist_ok=True)
API = "https://api.figma.com/v1"


def get(path, **params):
    q = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items() if v is not None)
    req = urllib.request.Request(f"{API}{path}" + (f"?{q}" if q else ""),
                                 headers={"X-Figma-Token": TOKEN})
    for a in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            b = e.read().decode()[:200]
            if e.code == 429:
                time.sleep(5 * (a + 1)); continue
            sys.exit(f"HTTP {e.code} {path}\n{b}")
        except Exception as e:
            if a == 3: sys.exit(str(e))
            time.sleep(3)


def render(ids, scale=2):
    got = {}
    for i in range(0, len(ids), 50):
        batch = ids[i:i+50]
        r = get(f"/images/{KEY}", ids=",".join(batch), format="png", scale=scale)
        for fid, url in (r.get("images") or {}).items():
            if not url: continue
            fn = BASE / f"{fid.replace(':', '_')}.png"
            with urllib.request.urlopen(url, timeout=180) as resp:
                fn.write_bytes(resp.read())
            got[fid] = fn
        time.sleep(1)
    return got


def parse(raw):
    """'WORK-B07 · W01 · 待我处理 · 1440' → (需求域, 编号, 标题, 视口)"""
    parts = [p.strip() for p in raw.split("·")]
    code = parts[0] if parts else ""
    num = parts[1] if len(parts) > 1 else ""
    title = parts[2] if len(parts) > 2 else ""
    vp = parts[-1] if len(parts) > 3 else ""
    return code, num, title, vp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page")
    ap.add_argument("--ids")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default="tickets.md")
    ap.add_argument("--shard", help="分片代号，如 S1/S2/.../S0")
    ap.add_argument("--no-render", action="store_true", help="只生成 ticket，不渲染基线（大批量用）")
    a = ap.parse_args()

    SHARDS = {
        "S0": ("01 ",), "S1": ("10 ", "11 ", "12 ", "13 "), "S2": ("20 ", "21 ", "22 "),
        "S3": ("40 ", "41 ", "42 ", "43 "), "S4": ("50 ", "51 ", "52 "),
        "S5": ("60 ", "61 ", "62 "), "S6": ("70 ", "80 "),
    }

    screens = json.loads((ROOT / "spec" / "screens.json").read_text())
    if a.ids:
        want = [i.strip() for i in a.ids.split(",")]
        sel = [s for s in screens if s["id"] in want]
    elif a.shard:
        pref = SHARDS[a.shard]
        sel = [s for s in screens if s["page"].startswith(pref)]
    else:
        sel = [s for s in screens if s["page"] == a.page]
        if a.limit:
            sel = sel[:a.limit]
    if not sel:
        sys.exit("没有匹配到屏幕")

    paths = {}
    if a.no_render:
        print(f"选中 {len(sel)} 屏（不渲染基线）")
    else:
        print(f"选中 {len(sel)} 屏 → 渲染基线")
        paths = render([s["id"] for s in sel])

    tokens = json.loads((ROOT / "spec" / "tokens.final.json").read_text())
    tickets = []
    for s in sel:
        code, num, title, vp = parse(s["raw"])
        fn = paths.get(s["id"])
        tickets.append({
            "id": s["id"], "page": s["page"], "req_domain": code, "req_no": num,
            "title": title, "viewport": vp, "size": s["size"],
            "baseline": str(fn.relative_to(ROOT)) if fn else None,
            "texts": s["texts"],
            "n_text": s["n_text"],
        })

    out_name = a.out if a.out.endswith(".md") else a.out + ".md"
    md = [f"# 派单包 {out_name[:-3]}（S0 组件层已就位）", "",
          f"> 生成 {datetime.datetime.now():%Y-%m-%d %H:%M} · 屏幕 {len(tickets)} · "
          f"基线目录 `figma-assets/baseline/`", "",
          "## 通用上下文（每个 Worker 都要带）", "",
          "**设计系统（官方口径，不得自行发挥）**",
          f"- 字体：{tokens['typography']['family']['value']} / 回退 {tokens['typography']['family']['fallback']}",
          f"- 官方 9 色：主画布 {tokens['color']['official']['surfaceCanvas']['value']} · "
          f"外壳 {tokens['color']['official']['surfaceShell']['value']} · "
          f"选中 {tokens['color']['official']['stateIconSelected']['value']} · "
          f"主文字 {tokens['color']['official']['textPrimary']['value']} · "
          f"主蓝 {tokens['color']['official']['actionPrimary']['value']} · "
          f"辅助文字 {tokens['color']['official']['textSecondary']['value']} · "
          f"细边 {tokens['color']['official']['borderHairline']['value']} · "
          f"悬停 {tokens['color']['official']['stateHover']['value']}",
          f"- 字阶：24/34 工作区标题 · 16/25 分节标题 · 14/24.5 阅读正文 · 14/20 导航操作 · 12/18 辅助说明",
          f"- 间距：{' / '.join(str(x) for x in tokens['spacing']['scale'])}",
          f"- 尺寸：图标栏 {tokens['size']['iconRail']['value']} · 图标 {tokens['size']['icon']['value']} · "
          f"命中 {tokens['size']['hitTarget']['value']} · 对象侧栏 {tokens['size']['objectSidebar']['value']} · "
          f"顶栏 {tokens['size']['headerSingleRow']['value']} · 对象行 {tokens['size']['objectRow']['value']} · "
          f"按钮 {tokens['size']['button']['value']} · 控件圆角 {tokens['radius']['control']['value']} · "
          f"弹窗圆角 {tokens['radius']['dialog']['value']}",
          "",
          "**基础组件（8 组 · 27 状态）**：RailIconButton · ToolbarIconButton · ObjectRow · WorkspaceTab · "
          "MenuItem · PrimaryPill · Tooltip · SendButton —— 全部实现为代码组件 + 变量绑定，"
          "禁止在页面里写裸样式（见 `figma-assets/component-baseline-catalog.md`）。",
          "",
          "**验收双轨（交付说明 06）**：",
          "1. 视觉：截图与基线 diff（阈值先松后紧；先 mask 动态区域）",
          "2. 行为：权限 / 发送 / Agent / 持久化 / 发布状态必须真实落地 —— 静态稿 ≠ 已实现",
          "",
          "**失败必须响亮**：规格缺陷或环境缺失 → 输出 `NEEDS_COORDINATOR` 停手，禁止 fallback 到当前实现自行猜测。",
          "",
          "---", ""]

    for t in tickets:
        md += [f"## {t['req_domain']} · {t['req_no']} · {t['title']}", "",
               f"- **屏幕 id**：`{t['id']}`",
               f"- **视口**：{t['viewport']}（{t['size']}）",
               f"- **基线图**：`{t['baseline'] or '待渲染：python3 scripts/gen_tickets.py --ids ' + t['id'] + ' --out baseline/' + t['id'].replace(':', '_') + '.md'}`",
               f"- **文案全文（{t['n_text']} 条，页面文字必须逐条还原，不得自造文案）**：", ""]
        md += ["> " + " / ".join(t["texts"][:80]), "",
               "**必填字段**：标题、正文、状态标签、右侧操作区（按基线图逐个还原）", "",
               "**验收命令**：`npm run visual:diff -- --screen " + t["id"] + "`", ""]

    # 需求附录：按分片挂对应需求域的需求条目
    SHARD_REQ = {"S0": ["FRM"], "S1": ["WK"], "S2": ["MSG"], "S3": ["KN"],
                 "S4": ["TAL"], "S5": ["CAP"], "S6": ["SET", "XMOD"]}
    if a.shard and (ROOT / "spec" / "requirements.json").exists():
        reqs = json.loads((ROOT / "spec" / "requirements.json").read_text())
        want = SHARD_REQ.get(a.shard, [])
        picked = [r for r in reqs if r["id"].split("-")[0] in want]
        if picked:
            md += ["---", "", f"## 附录：本分片需求清单（Notion《研发需求 V1.0》· {len(picked)} 条）", "",
                   "> 每条需求的「状态／异常与验收标准」列可直接转成行为测试用例；**静态稿还原 ≠ 行为已实现**。", ""]
            for r in picked:
                rid = r["id"]
                body = r.get("requirement") or r.get("col0") or ""
                acc = r.get("acceptance") or r.get("col2") or ""
                src = r.get("source") or r.get("col1") or ""
                md.append(f"### {rid}")
                if body:
                    md.append(f"- **要求**：{body}")
                if acc:
                    md.append(f"- **状态／异常与验收**：{acc}")
                if src:
                    md.append(f"- **来源／验收追踪**：{src}")
                md.append("")

    (TICKETS / out_name).write_text("\n".join(md))
    (TICKETS / (out_name[:-3] + ".json")).write_text(json.dumps(tickets, ensure_ascii=False, indent=2))
    print(f"✓ {TICKETS/out_name}")
    print(f"✓ {TICKETS/(out_name[:-3]+'.json')}")


if __name__ == "__main__":
    main()
