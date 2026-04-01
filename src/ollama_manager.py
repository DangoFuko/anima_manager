import requests
import subprocess
import time
import platform

from logger import setup_logger
from config import LOG_DIR

logger = setup_logger(LOG_DIR)


def is_ollama_running():
    try:
        r = requests.get("http://localhost:11434", timeout=2)
        return r.status_code == 200
    except:
        return False


def start_ollama():
    system = platform.system()

    try:
        if system == "Windows":
            # 方式1：直接调用 ollama（前提：已加入 PATH）
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        else:
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        logger.info("尝试启动 Ollama...")

    except Exception as e:
        logger.error(f"启动 Ollama 失败: {e}")


def ensure_ollama_running():
    if is_ollama_running():
        logger.info("Ollama 已运行")
        return True

    logger.warning("Ollama 未运行，尝试启动...")
    start_ollama()

    # 等待启动
    for i in range(10):
        time.sleep(1)
        if is_ollama_running():
            logger.info("Ollama 启动成功")
            return True

    logger.error("Ollama 启动失败")
    return False