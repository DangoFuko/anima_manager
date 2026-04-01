import os
import sys
import platform


def get_base_dir():
    """
    获取程序根目录：
    - 打包后：exe 所在目录
    - 开发时：当前文件目录
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)


# 程序根目录
BASE_DIR = get_base_dir()


# ========================
# 下载基础目录（动漫库）
# ========================
if platform.system() == "Windows":
    BASE_PATH = os.path.join(os.environ.get("USERPROFILE", "C:\\"), "Anime")
else:
    BASE_PATH = os.path.join(os.path.expanduser("~"), "Anime")


# ========================
# 功能开关
# ========================
ENABLE_DOWNLOAD = True   # 是否启用 qB 下载


# ========================
# 日志目录（修复关键点）
# ========================
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)


# ========================
# qBittorrent 配置
# ========================
QB_URL = "http://localhost:8080"
QB_USERNAME = "admin"
QB_PASSWORD = "adminadmin"


# ========================
# LLM 通用配置
# ========================
USE_LLM = False

LLM_PROVIDER = "ollama"  
# 可选：
# "ollama" / "openai"


# ========================
# Ollama（本地）
# ========================
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"


# ========================
# OpenAI（或兼容API）
# ========================
OPENAI_API_KEY = "your-api-key"
OPENAI_BASE_URL = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-4o-mini"