#!/bin/bash

# 启动 Nginx 服务
service nginx start

# 启动 Python 应用程序
cd /app/app && python Main.py