#!/usr/bin/env python3
"""本地接收器：浏览器把 Notion loadPageChunk 结果 POST 过来落盘"""
import http.server, socketserver, json, pathlib, sys, urllib.parse

DEST = pathlib.Path("/root/vault/1-Projects/设计稿工程/spec/notion/raw")
DEST.mkdir(parents=True, exist_ok=True)


class H(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        q = urllib.parse.urlparse(self.path)
        name = urllib.parse.parse_qs(q.query).get("name", ["unnamed"])[0]
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n)
        try:
            json.loads(body)
        except Exception:
            (DEST / f"{name}.bad").write_bytes(body)
        else:
            (DEST / f"{name}.json").write_bytes(body)
        self.send_response(200)
        self._cors()
        self.end_headers()
        self.wfile.write(b"ok")
        print(f"saved {name} ({len(body)} bytes)", flush=True)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    with socketserver.TCPServer(("127.0.0.1", 8913), H) as httpd:
        print("listening 127.0.0.1:8913", flush=True)
        httpd.serve_forever()
