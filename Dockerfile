FROM python:3.12-slim
RUN apt-get update && apt-get install -y git curl \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libasound2 libpango-1.0-0 libcairo2 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir playwright && playwright install chromium
# 安装 sing-box（vmess 代理客户端）
RUN curl -Lo /tmp/sing-box.tar.gz https://github.com/SagerNet/sing-box/releases/download/v1.14.3/sing-box-1.14.3-linux-amd64.tar.gz \
    && tar -xzf /tmp/sing-box.tar.gz -C /tmp \
    && mv /tmp/sing-box-1.14.3-linux-amd64/sing-box /usr/local/bin/sing-box \
    && chmod +x /usr/local/bin/sing-box \
    && rm -rf /tmp/sing-box.tar.gz /tmp/sing-box-1.14.3-linux-amd64
COPY entrypoint.sh /entrypoint.sh
COPY worker.py /worker.py
COPY scripts/ /scripts/
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
