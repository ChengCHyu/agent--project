import logging
from utils.path_tool import get_abs_path
import os
from datetime import datetime
import sys
LOG_ROOT = get_abs_path("log")
if not os.path.exists(LOG_ROOT):
    os.makedirs(LOG_ROOT, exist_ok=True)
DEFAULT_LOG_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s : %(lineno)s - %(message)s")
def get_logger(name: str="agent", log_file: str = None, console_level=logging.INFO,file_level=logging.DEBUG) -> logging.Logger:
    """
    获取日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    #避免重复添加Handler
    if logger.handlers:
        return logger
        #控制台handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)
    #文件handler
    if not log_file:        #日志文件的存放路径
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    file_handler = logging.FileHandler(log_file,encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_handler)
    return logger

#快捷获取日志器
logger = get_logger()
if __name__ == '__main__':
    logger.info("信息日志test")
    logger.debug("调试日志test")
    logger.error("错误日志test")
