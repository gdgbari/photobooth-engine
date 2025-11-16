import logging
from logging.handlers import RotatingFileHandler

def setup_logging() -> None:
    logger = logging.getLogger("photobooth.upload")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return  # evita duplicati

    handler = logging.FileHandler(
        "photobooth-upload.log",  # unico file
        mode="a",                 # append
        encoding="utf-8",
    )
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

