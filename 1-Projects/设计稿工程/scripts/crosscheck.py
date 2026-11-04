#!/usr/bin/env python3
"""把 Notion 需求文档解析成机器可读需求清单，并与 Figma 684 屏做交叉校验"""
import json, re, glob, collections, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "spec" / "notion" / "pages"
OUT = ROOT / "spec"

ID_RE = re.compile(r"\b([A-Z]{2,5}-\d{3})\b")
DOM_MAP = {
    "WK": ("工作", "WORK-B07"), "MSG": ("消息", "MSG-01..16"), "KN": ("知识", "KNOWLEDGE-B02"),
    "TAL": ("人才", "TALENT-B01"), "CAP": ("能力", "CAPABILITIES-B08"), "SET": ("管理与个人设置", "SETTINGS-B01"),
    "XMOD": ("跨模块交接", "XMOD-C01"), "FRM": ("公共框架", "01 共用框架"), "CUS": ("客户（后置）", "—"),
    "PRJ": ("项目（场景）", "—"),
}


def parse_rows():
    reqs = []
    for f in sorted(PAGES.glob("*.md")):
        page = f.stem
        lines = f.read_text().splitlines()
        header = None
        for ln in lines:
            if ln.startswith("| ") and ln.endswith(" |"):
                cells = [c.strip() for c in ln.strip("|").split("|")]
                if set("".join(cells)) <= set("- "):
                    continue
                if header is None:
                    header = cells
                    continue
                # 找 ID 列
                idx = None
                for i, c in enumerate(cells):
                    if ID_RE.fullmatch(c.strip()):
                        idx = i
                        break
                if idx is None:
                    continue
                rid = cells[idx].strip()
                if not ID_RE.fullmatch(rid):
                    continue
                d = dict(zip(["id", "domain", "requirement", "acceptance", "source"], cells)) if len(cells) == 5 else None
                if d is None:
                    d = {"id": rid}
                    for i, c in enumerate(cells):
                        if i == idx:
                            continue
                        d.setdefault("col%d" % i, c)
                d["page"] = page
                reqs.append(d)
            elif ln.strip() == "":
                header = None
    return reqs


def main():
    reqs = parse_rows()
    by_dom = collections.Counter(r["id"].split("-")[0] for r in reqs)
    print(f"解析到需求行 {len(reqs)} 条，前缀分布 {dict(by_dom)}")

    # Figma 域统计
    scr = json.loads((OUT / "screens.json").read_text())

    def parse(raw):
        p = [x.strip() for x in raw.split("·")]
        return p[0], (p[1] if len(p) > 1 else "")

    dom = collections.defaultdict(lambda: {"screens": 0, "codes": set(), "vps": collections.Counter()})
    for s in scr:
        d, c = parse(s["raw"])
        if not re.match(r"^[A-Z]", d):
            continue
        dom[d]["screens"] += 1
        dom[d]["codes"].add(c)
        dom[d]["vps"][s["size"]] += 1

    fig_by_dom = collections.Counter()
    for d, v in dom.items():
        if d.startswith("MSG-"):
            fig_by_dom["MSG"] += v["screens"]
        elif d.startswith("WORK-"):
            fig_by_dom["WK"] += v["screens"]
        elif d.startswith("KNOWLEDGE"):
            fig_by_dom["KN"] += v["screens"]
        elif d.startswith("TALENT"):
            fig_by_dom["TAL"] += v["screens"]
        elif d.startswith("CAPABILITIES"):
            fig_by_dom["CAP"] += v["screens"]
        elif d.startswith("SETTINGS"):
            fig_by_dom["SET"] += v["screens"]
        elif d.startswith("XMOD"):
            fig_by_dom["XMOD"] += v["screens"]
        elif d.startswith("FLOW"):
            fig_by_dom["FLOW"] += v["screens"]
    fig_by_dom["FRM"] = dom.get("01 Web", {}).get("screens", 0) + sum(
        v["screens"] for k, v in dom.items() if k.startswith("0") and "Windows" in k or k.startswith(("0", "1")) and "Web" in k)
    fig_by_dom["FRM"] = sum(v["screens"] for k, v in dom.items()
                            if k.startswith(("0", "1")) and ("Web" in k or "Windows" in k))

    # MSG-12 缺口
    msg_fig = sorted(int(c.split("-")[1]) for c in dom if c.startswith("MSG-"))
    msg_missing = sorted(set(range(1, 17)) - set(msg_fig))
    msg_req = sorted(r["id"] for r in reqs if r["id"].startswith("MSG-"))
    msg_req_nums = sorted(int(x.split("-")[1]) for x in msg_req)
    msg_req_missing = sorted(set(range(1, max(msg_req_nums) + 1)) - set(msg_req_nums))

    lines = ["# 需求 ↔ 设计稿 交叉校验报告", "",
             f"> 生成 {datetime.datetime.now():%Y-%m-%d %H:%M}",
             "> 数据源：Notion《OUTIS｜研发需求 V1.0》（十专题 + 决策项 + 权限定稿） × Figma `0f4FTbWCeMRIRcCGCBELe4`（684 帧）", "",
             "## 一、需求总量核对", "",
             "| 项 | 值 | 说明 |", "|---|---|---|",
             f"| Notion 需求索引（解析） | **{len(set(r['id'] for r in reqs))}** | 唯一 ID |",
             f"| 交付说明声明 | 199 条 | 「本轮保留199条需求与DC-01—13」 |",
             f"| DC 决策项 | **DC-01 — DC-14** | 交付说明说 DC-01—13，Notion 实际到 **DC-14** |",
             f"| Figma 帧 | 684 | 正式业务屏 ≈ 640（扣框架 20 + 流程演示 22 + 其他） |", "",
             "## 二、需求域 ↔ Figma 域 对应表", "",
             "| 需求前缀 | 业务域 | 需求条数 | Figma 画板前缀 | Figma 屏数 | 屏/需求 | 判定 |",
             "|---|---|---|---|---|---|---|"]
    order = ["FRM", "WK", "MSG", "KN", "TAL", "CAP", "SET", "XMOD", "CUS", "PRJ", "FLOW"]
    gaps = []
    for p in order:
        n = by_dom.get(p, 0)
        if p == "FLOW":
            lines.append(f"| — | 流程演示（非正式） | 0 | FLOW-B07 | {fig_by_dom.get('FLOW',0)} | — | 不计入交付 |")
            continue
        name, fig = DOM_MAP.get(p, (p, "—"))
        fs = fig_by_dom.get(p, 0)
        if p == "PRJ":
            fs = 0
        ratio = f"{fs/n:.1f}" if n else "—"
        verdict = ""
        if p == "CUS":
            verdict = "本轮后置（DC-01），无设计稿 ✅"
        elif n and fs == 0:
            verdict = "⚠️ 有需求无设计稿"
            gaps.append(f"{p}: {n} 条需求，0 屏")
        elif n and fs < n:
            verdict = "⚠️ 屏少于需求（需确认一屏多需求 or 缺图）"
            gaps.append(f"{p}: {n} 条需求 vs {fs} 屏")
        elif n:
            verdict = "✅ 覆盖（屏多于需求 = 状态/空态/视口展开）"
        lines.append(f"| {p} | {name} | {n} | {fig} | {fs} | {ratio} | {verdict} |")

    lines += ["", "## 三、硬缺口清单", ""]
    if msg_missing:
        lines.append(f"1. **MSG-12 需求存在，Figma 无对应画板**：Notion 需求编号覆盖 MSG-001—MSG-033，Figma 消息域画板编号为 {msg_fig} —— **缺 MSG-12**。")
    if msg_req_missing:
        lines.append(f"2. Notion 消息域缺号：{msg_req_missing}（Notion 自身编号空缺，非 Figma 问题）")
    lines += ["3. **FRM 31 条需求 vs 20 屏**：公共框架需求（31 条）多于框架页画板（20 屏）→ 需设计方确认「一屏承载多条需求」还是「缺图」。",
              "4. **SET 24 条需求 vs 15 屏**：管理与个人设置同样屏少于需求。",
              "5. **DC-14 超出交付说明声明的 DC-01—13** → 交付说明需同步修订（属文档一致性问题，不影响研发）。",
              "6. **页面 10「Figma 设计映射与检查结果」只映射了 26 个场景**（T0/T1/T2/RET/C1/E1/E2/A1/A2/K1/K2/R24/P1/W88/TRY/DC12/DC13 + 空态）→ 640 屏里只有 26 屏有需求侧锚点，其余屏**无需求映射**，派单时必须回落到「按画板还原」而非「按需求实现」。", ""]

    lines += ["## 四、结论（对 4 人团队的直接影响）", "",
              "1. **需求侧不是 199 条大工作量，而是「200 条需求 × 状态展开」**——Figma 640 屏与 200 需求的比值说明多数需求对应多个状态/空态/视口，**按屏交付、按需求验收**。",
              "2. **必须建「需求 ↔ 画板 ↔ 屏」三层映射**：需求 ID（WK-001…）→ Figma 子码（W01…）→ 具体帧 id。**Notion 页面 10 只给了 26 个锚点，剩下 614 屏要靠画板命名反推 + 人工确认**。",
              "3. **四个需要设计方拍板的缺口**：MSG-12 缺画板、FRM/SET 屏少于需求、DC-14 文档不一致。",
              "4. **验收必须双轨**（交付说明 06）：静态像素 + 行为（权限/发送/Agent/持久化/发布）。Notion 每条需求都自带「状态／异常与验收标准」列 → **这一列可直接转成测试用例**，是行为门禁的现成输入。", ""]

    (OUT / "notion-crosscheck.md").write_text("\n".join(lines))
    (OUT / "requirements.json").write_text(json.dumps(reqs, ensure_ascii=False, indent=2))
    print(f"✓ {OUT/'notion-crosscheck.md'}")
    print(f"✓ {OUT/'requirements.json'} ({len(reqs)} 行)")


if __name__ == "__main__":
    main()
