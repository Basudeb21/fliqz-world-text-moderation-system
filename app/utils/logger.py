# app/utils/logger.py

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config.settings import DEBUG


# --------------------------------------------------
# Log Directory
# --------------------------------------------------

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "moderation.log"


# --------------------------------------------------
# Logger
# --------------------------------------------------

logger = logging.getLogger("moderation")

logger.setLevel(
    logging.DEBUG if DEBUG else logging.INFO
)

logger.propagate = False


if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    # Console

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)