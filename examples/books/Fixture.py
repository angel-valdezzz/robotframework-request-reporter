"""Fictional, loopback-only book catalog for the Request Reporter demo."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

from robot.api.deco import keyword, library


@library(scope="SUITE", auto_keywords=False)
class Fixture:
    def __init__(self):
        self.server = None

    @keyword
    def start_api(self):
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                path = self.path.split("?", 1)[0]
                catalog = [{"id": 41, "title": "Cartas al mar"}, {"id": 42, "title": ""}]
                payload = (
                    {"ok": True}
                    if path == "/health"
                    else catalog
                    if path == "/books"
                    else {"id": 42, "title": "", "category": "fiction"}
                )
                body = json.dumps(payload).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        Thread(target=self.server.serve_forever, daemon=True).start()
        return f"http://127.0.0.1:{self.server.server_port}"

    @keyword
    def stop_api(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
