import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_logger(log_dir):
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("anime")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    info = TimedRotatingFileHandler(
        os.path.join(log_dir, "app.log"),
        when="midnight",
        encoding="utf-8"
    )
    info.setFormatter(fmt)

    error = logging.FileHandler(
        os.path.join(log_dir, "error.log"),
        encoding="utf-8"
    )
    error.setLevel(logging.ERROR)
    error.setFormatter(fmt)

    console = logging.StreamHandler()
    console.setFormatter(fmt)

    logger.addHandler(info)
    logger.addHandler(error)
    logger.addHandler(console)

    return logger


class TkHandler(logging.Handler):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.insert("end", msg + "\n")
            self.text.see("end")

        self.text.after(0, append)