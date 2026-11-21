import logging
from logging.handlers import RotatingFileHandler
from app.config import LOG_FILE

def configure_logging():
    logger = logging.getLogger("walled_dlp")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)
    return logger
