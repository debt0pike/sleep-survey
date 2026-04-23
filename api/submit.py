from http.server import BaseHTTPRequestHandler
import json, os, urllib.request

APP_ID     = os.environ.get('FEISHU_APP_ID',     'cli_a95b87c9d1f8dbc2')
APP_SECRET = os.environ.get('FEISHU_APP_SECRET', 'ONch0li1lnHo8NfjMtdq9cxoVtNAXm1m')
APP_TOKEN  = os.environ.get('FEISHU_APP_TOKEN',  'YArmbgA4caqIMMsAgtCcJZetnOS')
TABLE_ID   = os.environ.get('FEISHU_TABLE_ID',   'tblv0OzbG1KV7hEr')

def feishu_post(url, data, headers=None):
    h = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    if headers:
        h.update(headers)
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

class handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        try:
            length  = int(self.headers.get('Content-Length', 0))
            payload = json.loads(self.rfile.read(length))
            fields  = payload.get('fields', {})
            token   = get_token()
            result  = create_record(token, fields)
            body    = json.dumps(result).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._cors()
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            err = json.dumps({'error': str(e)}).encode()
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self._cors()
            self.end_headers()
            self.wfile.write(err)
