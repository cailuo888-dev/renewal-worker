#!/usr/bin/env python3
"""后台 worker：定时运行三个续期脚本"""
import os, time, logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# 上次运行时间
last_run = {'lunes': None, 'katabump': None, 'bot_hosting': None}
# 间隔（天）
intervals = {'lunes': 10, 'katabump': 3, 'bot_hosting': 4}

def run_script(name, module_func):
    try:
        logger.info(f"开始运行 {name}...")
        result = module_func()
        logger.info(f"{name} 结果: {result}")
    except Exception as e:
        logger.error(f"{name} 异常: {e}")

def should_run(name):
    if last_run[name] is None:
        return True
    return datetime.now() - last_run[name] >= timedelta(days=intervals[name])

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/app')
    from scripts.lunes_renew import renew_lunes
    from scripts.katabump_renew import renew_katabump
    from scripts.bot_hosting_renew import renew_bot_hosting
    
    scripts = {
        'lunes': renew_lunes,
        'katabump': renew_katabump,
        'bot_hosting': renew_bot_hosting,
    }
    
    logger.info("Worker 启动，等待定时任务...")
    while True:
        for name, func in scripts.items():
            if should_run(name):
                run_script(name, func)
                last_run[name] = datetime.now()
        time.sleep(3600)  # 每小时检查一次
