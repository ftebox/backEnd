FROM ubuntu

# 设置时区为东八区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装 nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# 安装 Python3.10
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3-pip && \
    ln -s /usr/bin/python3.10 /usr/local/bin/python && \
    rm -rf /var/lib/apt/lists/*

# 更换pip镜像源
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn

# 创建并进入工作目录
WORKDIR /app

# 拷贝启动脚本
COPY . /app

# 赋予权限
RUN chmod +x /app/start.sh

# 安装依赖包
RUN pip install --no-cache-dir -r requirements.txt

# 创建目录
RUN mkdir -p /app/app /app/html

# 通过脚本启动
ENTRYPOINT ["/app/start.sh"]