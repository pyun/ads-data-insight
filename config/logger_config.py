import logging
import os
from logging.handlers import TimedRotatingFileHandler

# 设置环境变量
os.environ["BYPASS_TOOL_CONSENT"] = "true"

def setup_logger():
    """配置日志 - 同时输出到控制台和文件，每天轮转，保留30天"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),  # 控制台输出
            TimedRotatingFileHandler("./logs/agent.log", when="midnight", interval=1, backupCount=30, encoding="utf-8")  # 每日轮转，保留30天
        ]
    )