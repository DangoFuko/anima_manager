import requests
import os
from config import ENABLE_DOWNLOAD, QB_URL, QB_USERNAME, QB_PASSWORD
from logger import setup_logger
from config import LOG_DIR

logger = setup_logger(LOG_DIR)


class QB:
    def __init__(self):
        self.s = requests.Session()
        self.login()

    def login(self):
        r = self.s.post(f"{QB_URL}/api/v2/auth/login", data={
            "username": QB_USERNAME,
            "password": QB_PASSWORD
        })
        if r.text != "Ok.":
            raise Exception("qB登录失败")

    def add(self, torrent, path):
        with open(torrent, "rb") as f:
            self.s.post(
                f"{QB_URL}/api/v2/torrents/add",
                files={"torrents": f},
                data={"savepath": os.path.abspath(path)}
            )


class Downloader:
    def __init__(self):
        self.qb = None
        if ENABLE_DOWNLOAD:
            try:
                self.qb = QB()
                logger.info("qB连接成功")
            except:
                logger.error("qB连接失败，使用模拟模式")

    def add_torrent(self, torrent, path):
        os.makedirs(path, exist_ok=True)

        if not self.qb:
            logger.info(f"[模拟] {torrent} → {path}")
            return

        try:
            self.qb.add(torrent, path)
            logger.info(f"[下载] {torrent} → {path}")
        except Exception as e:
            logger.error(f"下载失败: {e}")