import time

import requests
from bs4 import BeautifulSoup
import re
import json
import datetime
import socket
import socks

cookies = {}

with open('data.json', 'r') as f:
    jsonData = json.load(f)
    cookies = jsonData['cookies']

# 设置代理服务器的 IP 和端口号
socks.set_default_proxy(socks.SOCKS5, "172.16.8.1", 1080)

# 将所有的 TCP 连接都通过代理服务器进行处理
socket.socket = socks.socksocket

def flushCookie():
    reqData = {
        'email': 'ftebox@qq.com',
        'passwd': '369958Na',
        'code': ''
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
        'Referer': 'https://www.freewhale.co/auth/login',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    try:
        # 发送登录请求
        response = requests.post('https://www.freewhale.co/auth/login', data=reqData, headers=headers, verify=False)
        # 判断是否登录成功
        if response.status_code == 200 and '"ret":1' in response.text:
            global cookies
            global jsonData
            # 读取cookie
            cookies = response.cookies.get_dict()
            # 将cookie写入jsonData
            jsonData['cookies'] = cookies;
            flushJson("cookie已刷新！");
        else:
            # 失败就重新登陆
            flushCookie();
    except requests.exceptions.RequestException as e:
        # 出现异常，打印异常 重新登陆
        print(e)
        flushCookie();


def getData():
    url = 'https://www.freewhale.co/user'  # 将此链接替换为您要抓取的实际链接
    global cookies
    try:
        response = requests.get(url, cookies=cookies, verify=False)
        # 如果发生了重定向 就刷新cookie
        if response.history:
            flushCookie();
            getData();
    # 如果发生了异常 就递归
    except requests.exceptions.RequestException as e:
        print(e)
        getData();
    else:
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        item = soup.findAll(class_='nodemain')
        item1 = soup.findAll('code')
        item2 = soup.findAll('input')
        # 在线设备数
        zxsb = item[2].find('dd').text.strip()
        # 上次使用时间
        sysj = item[2].findAll('div')[4].text[6:].strip()
        # 剩余流量
        syll = item1[2].text.strip()
        # 到期时间
        dqsj = item[0].findAll('div')[4].text[7:].strip()
        # ssr订阅链接
        ssr = item2[0]['value'].strip()
        ssr_bak = item2[1]['value'].strip()
        # clash订阅链接
        clash = item2[2]['value'].strip()
        # v2ray订阅链接
        v2ray = item2[4]['value'].strip()
        v2ray_bak = item2[5]['value'].strip()
        global jsonData
        jsonData['data'] = {
            'code': 1,
            'message': 'success!',
            'data': {
                'zxsb': zxsb,
                'sysj': sysj,
                'syll': syll,
                'dqsj': dqsj,
                'v2rayurl': v2ray,
                'v2rayBakurl': v2ray_bak,
                'SSRurl': ssr,
                'SSRBakurl': ssr_bak,
                'Clash': clash
            }
        }
        jsonData['saveTime'] = time.time();
        flushJson("数据已刷新");


def flushJson(msg):
    global jsonData;
    with open('data.json', 'w') as f:
        json.dump(jsonData, f)
    # 获取当前的日期和时间
    now = datetime.datetime.now()
    # 格式化输出日期和时间
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    print('{} '.format(formatted_time) + msg)
