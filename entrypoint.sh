#!/bin/bash
set -e

# 如果配置了 vmess 节点，启动 sing-box 本地 SOCKS5 代理
if [ -n "$VMESS_ID" ]; then
  echo "Starting sing-box proxy..."
  mkdir -p /etc/sing-box
  cat > /etc/sing-box/config.json <<JSONEOF
{
  "log": {"level": "warn"},
  "inbounds": [
    {
      "type": "socks",
      "tag": "socks-in",
      "listen": "127.0.0.1",
      "listen_port": 1080
    }
  ],
  "outbounds": [
    {
      "type": "vmess",
      "tag": "proxy",
      "server": "${VMESS_ADD}",
      "server_port": ${VMESS_PORT},
      "uuid": "${VMESS_ID}",
      "security": "auto",
      "alter_id": 0,
      "transport": {
        "type": "ws",
        "path": "${VMESS_PATH}",
        "headers": {"Host": "${VMESS_HOST}"}
      }
    },
    {"type": "direct", "tag": "direct"}
  ],
  "route": {
    "rules": [{"outbound": "proxy"}]
  }
}
JSONEOF
  sing-box run -c /etc/sing-box/config.json &
  # 等待 SOCKS 端口就绪
  for i in $(seq 1 15); do
    if (echo > /dev/tcp/127.0.0.1/1080) 2>/dev/null; then
      echo "Proxy ready on 127.0.0.1:1080"
      break
    fi
    sleep 1
  done
  export PROXY_SERVER="socks5://127.0.0.1:1080"
else
  echo "VMESS_ID not set, running without proxy"
fi

echo "Worker starting..."
exec python /worker.py
