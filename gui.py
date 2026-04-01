import tkinter as tk
from tkinter import filedialog
import os

from torrent_parser import get_torrent_name
from parser import parse_anime_name
from matcher import find_best_match
from llm_matcher import llm_match
from downloader import Downloader
from logger import setup_logger, TkHandler
from config import BASE_PATH, LOG_DIR


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Anime Manager")

        self.base = BASE_PATH
        self.files = []
        self.downloader = Downloader()

        tk.Button(root, text="选择torrent", command=self.pick).pack()
        tk.Button(root, text="选择目录", command=self.pick_dir).pack()
        tk.Button(root, text="开始", command=self.run).pack()

        self.text = tk.Text(root, height=20)
        self.text.pack()

        self.logger = setup_logger(LOG_DIR)
        h = TkHandler(self.text)
        self.logger.addHandler(h)

    def pick(self):
        self.files = filedialog.askopenfilenames(filetypes=[("torrent", "*.torrent")])
        self.logger.info(f"选中{len(self.files)}个")

    def pick_dir(self):
        d = filedialog.askdirectory()
        if d:
            self.base = d

    def run(self):
        for f in self.files:
            try:
                real = get_torrent_name(f)
                name = real or os.path.basename(f)

                anime = parse_anime_name(name)

                match = llm_match(name, self.base)
                if not match:
                    match = find_best_match(anime, self.base)

                path = os.path.join(self.base, match)

                self.logger.info(f"真实名: {name}")
                self.logger.info(f"番剧: {anime}")
                self.logger.info(f"目录: {path}")

                self.downloader.add_torrent(f, path)

            except Exception as e:
                self.logger.error(f"失败: {e}")