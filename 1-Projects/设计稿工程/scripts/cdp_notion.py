#!/usr/bin/env python3
"""
通过 CDP 驱动已登录的 Chrome 抓取 Notion 页面内容（绕过跨域/混合内容限制）

前置：浏览器已登录 Notion（本账号可访问 OUTIS 工作区）
用法：python3 cdp_notion.py
"""
import json, urllib.request, time, pathlib, datetime, websocket

CDP_HTTP = "http://127.0.0.1:9222"
DEST = pathlib.Path("/root/vault/1-Projects/设计稿工程/spec/notion/raw")
DEST.mkdir(parents=True, exist_ok=True)

# 从页面链接自动推导（主页面 DOM 里的 /p/<slug>）
JS_LIST = """
(() => Array.from(document.querySelectorAll('a')).map(a=>({t:(a.innerText||'').trim(), h:a.href}))
   .filter(x=>/\\/p\\//.test(x.h)).map(l=>{
     const seg=l.h.split('/p/')[1].split('?')[0];
     const hex=seg.replace(/-/g,'').slice(-32);
     return {t:l.t, pid: hex.length===32 ? hex.replace(/^(.{8})(.{4})(.{4})(.{4})(.{12})$/,'$1-$2-$3-$4-$5') : null};
   }).filter(x=>x.pid))()
"""

JS_FETCH = """
(async (pid) => {
  const r = await fetch('/api/v3/loadPageChunk', {method:'POST',
    headers:{'content-type':'application/json'},
    body: JSON.stringify({pageId:pid, limit:3000, cursor:{stack:[]}, chunkNumber:0, verticalColumns:false})});
  const j = await r.json();
  return JSON.stringify(j);
})(PID)
"""


def find_target():
    with urllib.request.urlopen(CDP_HTTP + "/json", timeout=10) as r:
        targets = json.loads(r.read().decode())
    for t in targets:
        if t.get("type") == "page" and "notion" in t.get("url", ""):
            return t
    raise SystemExit("找不到 Notion 页面 target")


class CDP:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, timeout=180, suppress_origin=True)
        self.i = 0

    def send(self, method, params=None):
        self.i += 1
        mid = self.i
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(msg["error"])
                return msg.get("result", {})

    def evaluate(self, expr, await_promise=True):
        r = self.send("Runtime.evaluate", {
            "expression": expr, "awaitPromise": await_promise,
            "returnByValue": True, "timeout": 120000})
        res = r.get("result", {})
        if r.get("exceptionDetails"):
            raise RuntimeError(json.dumps(r["exceptionDetails"])[:400])
        return res.get("value")


def main():
    tgt = find_target()
    print("target:", tgt["url"])
    c = CDP(tgt["webSocketDebuggerUrl"])
    pages = c.evaluate(JS_LIST)
    seen, todo = set(), []
    for p in pages:
        if p["pid"] in seen:
            continue
        seen.add(p["pid"])
        todo.append(p)
    root = "3bd46975-666d-816d-9dcc-c1c0fc7e1321"
    if root not in seen:
        todo.append({"t": "00｜研发需求 V1.0 总览", "pid": root})
    print(f"待抓取页面 {len(todo)} 个")
    for p in todo:
        name = (p["t"] or p["pid"]).replace("\\", "_").replace("/", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace('"', "_").replace("|", "_").replace("\n", "_")[:40]
        try:
            s = c.evaluate(JS_FETCH.replace("PID", json.dumps(p["pid"])))
            data = json.loads(s)
            n = len((data.get("recordMap") or {}).get("block") or {})
            (DEST / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False))
            print(f"✓ {name}: {n} blocks")
        except Exception as e:
            print(f"! {name}: {e}")
    print(f"\n落盘目录: {DEST}")


if __name__ == "__main__":
    main()
