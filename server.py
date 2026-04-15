#!/usr/bin/env python3
"""
ChiroActive dev server — static file server with clean URL routing.
Usage: python3 server.py
"""
import http.server, os, socketserver, urllib.parse

PORT = 3000
ROOT = os.path.dirname(os.path.abspath(__file__))

MIME = {
    '.html': 'text/html; charset=utf-8',
    '.css':  'text/css',
    '.js':   'application/javascript',
    '.json': 'application/json',
    '.png':  'image/png',
    '.jpg':  'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif':  'image/gif',
    '.svg':  'image/svg+xml',
    '.ico':  'image/x-icon',
    '.woff': 'font/woff',
    '.woff2':'font/woff2',
    '.webp': 'image/webp',
}

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.unquote(urllib.parse.urlparse(self.path).path)
        fp = self._resolve(path)
        if fp is None:
            self.send_error(404); return
        ext = os.path.splitext(fp)[1].lower()
        ct  = MIME.get(ext, 'application/octet-stream')
        try:
            data = open(fp, 'rb').read()
            self.send_response(200)
            self.send_header('Content-Type', ct)
            self.send_header('Content-Length', len(data))
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_error(500, str(e))

    def _resolve(self, path):
        if path in ('', '/'):
            path = '/index.html'
        local = os.path.join(ROOT, path.lstrip('/'))
        if os.path.isfile(local): return local
        # try .html extension for clean URLs
        if not os.path.splitext(local)[1]:
            h = local + '.html'
            if os.path.isfile(h): return h
        return None

    def log_message(self, fmt, *args):
        print(f"  {args[1] if len(args)>1 else '?'}  {self.path}")

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('', PORT), Handler) as s:
        print(f"ChiroActive → http://localhost:{PORT}")
        s.serve_forever()
