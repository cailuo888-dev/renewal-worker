#!/bin/bash
set -e
# 启动时从 Forgejo 克隆代码
if [ -n "$FORGEJO_TOKEN" ]; then
  echo "Cloning from Forgejo..."
  rm -rf /app
  git clone https://xike:${FORGEJO_TOKEN}@forgejo.xike.blitz.cloud/xike/renewal-bot.git /app
  cd /app
  pip install --no-cache-dir -r requirements.txt 2>&1 | tail -1
else
  echo "FORGEJO_TOKEN not set!"
  exit 1
fi
exec python /worker.py
