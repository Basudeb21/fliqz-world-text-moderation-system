# app/utils/logger.py
import logging
from pathlib import Path
from datetime import datetime

# Log Folder

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")

LOG_FILE = LOG_DIR / f"moderation_{today}.log"

# Logger
logger = logging.getLogger("moderation")
logger.setLevel(logging.DEBUG)
logger.propagate = False

# Prevent duplicate handlers
if logger.handlers:
    logger.handlers.clear()

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)s",
    "%Y-%m-%d %H:%M:%S",
)

# Console

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

# File

file_handler = logging.FileHandler(
    LOG_FILE,
    encoding="utf-8",
)

file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(file_handler)