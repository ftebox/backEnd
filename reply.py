import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import crawl
import schedule
import time
import datetime

data = {}

def readJson():
    with open('data.json', 'r') as f:
        global data
        jsonData = json.load(f)
        data = jsonData['data']
        saveTime = jsonData['saveTime']
    # 如果数据有效性超过5分钟 就刷新
    if (time.time() - saveTime)/60 > 5:
        crawl.getData();
    # 获取当前的日期和时间
    now = datetime.datetime.now()
    # 格式化输出日期和时间
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    print('{} 读取数据！'.format(formatted_time))

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        readJson();
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(str(json.dumps(data)).encode())

def reply():
    httpd = HTTPServer(('0.0.0.0', 8456), SimpleHTTPRequestHandler)
    httpd.serve_forever()
