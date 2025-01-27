FROM node:latest

# 安装 Python 3 并将 python3 软链接为 python
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY js_code/package*.json ./

RUN npm install

COPY js_code/. .

EXPOSE 8000

CMD ["node", "server.js"]
