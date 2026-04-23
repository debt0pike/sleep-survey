#!/usr/bin/env python3
"""
大萌博士 睡眠调查 · 代理服务器
浏览器 → /api/submit → 飞书 Bitable
"""
import json, os, urllib.request, urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import quote

APP_ID     = os.environ.get('FEISHU_APP_ID',     'cli_a95b87c9d1f8dbc2')
APP_SECRET = os.environ.get('FEISHU_APP_SECRET', 'ONch0li1lnHo8NfjMtdq9cxoVtNAXm1m')
APP_TOKEN  = os.environ.get('FEISHU_APP_TOKEN',  'YArmbgA4caqIMMsAgtCcJZetnOS')
TABLE_ID   = os.environ.get('FEISHU_TABLE_ID',   'tblv0OzbG1KV7hEr')
PORT       = int(os.environ.get('PORT', 8080))

def feishu_post(url, data, headers=None):
    h = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    if headers: h.update(headers)
    req = urllib.request.Request(url, json.dumps(data).encode(), h)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def get_token():
    r = feishu_post(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        {'app_id': APP_ID, 'app_secret': APP_SECRET}
    )
    return r.get('tenant_access_token', '')

def create_record(token, fields):
    return feishu_post(
        f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records',
        {'fields': fields},
        {'Authorization': f'Bearer {token}'}
    )

class Handler(SimpleHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _no_cache(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Pragma', 'no-cache')

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def end_headers(self):
        if hasattr(self, '_path') and self._path.endswith('.html'):
            self._no_cache()
        super().end_headers()

    def do_GET(self):
        # 根路径直接返回问卷 HTML，链接干净无中文
        if self.path in ('/', ''):
            html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '睡眠调查_v9.html')
            try:
                with open(html_path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(content)))
                self._no_cache()
                self._cors()
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404); self.end_headers()
            return
        self._path = self.path.split('?')[0]
        super().do_GET()

    def do_POST(self):
        if self.path != '/api/submit':
            self.send_response(404); self.end_headers(); return
        try:
            length = int(self.headers.get('Content-Length', 0))
            payload = json.loads(self.rfile.read(length))
            fields  = payload.get('fields', {})
            name    = fields.get('姓名标识', '?')
            print(f'[提交] {name} 字段数={len(fields)}', flush=True)
            token  = get_token()
            result = create_record(token, fields)
            code   = result.get('code', -1)
            rec_id = result.get('data', {}).get('record', {}).get('record_id', '')
            print(f'[飞书] code={code} record_id={rec_id}', flush=True)
            if code != 0:
                print(f'[飞书错误] {json.dumps(result, ensure_ascii=False)}', flush=True)
            body = json.dumps(result).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._cors()
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            import traceback; traceback.print_exc()
            err = json.dumps({'error': str(e)}).encode()
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self._cors()
            self.end_headers()
            self.wfile.write(err)

    def log_message(self, fmt, *args):
        path = args[0] if args else ''
        if '/api/' in str(path) or '.html' in str(path):
            print(f'{self.address_string()} {fmt % args}', flush=True)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    httpd = HTTPServer(('', PORT), Handler)
    print(f'服务器已启动，端口 {PORT}', flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('已停止')
