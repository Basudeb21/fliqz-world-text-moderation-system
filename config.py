# config.py

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# -----------------------------------
# MySQL / SQLAlchemy settings
# -----------------------------------

DB_HOST = os.getenv("DB_HOST", "localhost")

DB_PORT = int(
    os.getenv("DB_PORT", 3306)
)

DB_USER = os.getenv("DB_USER", "root")

DB_PASSWORD = os.getenv("DB_PASSWORD", "")

DB_DATABASE = os.getenv(
    "DB_DATABASE",
    "myvault"
)

# -----------------------------------
# Redis settings
# -----------------------------------

REDIS_HOST = os.getenv(
    "REDIS_HOST",
    "localhost"
)

REDIS_PORT = int(
    os.getenv("REDIS_PORT", 6379)
)

REDIS_DB = int(
    os.getenv("REDIS_DB", 0)
)

# -----------------------------------
# LLaMA / Ollama endpoint
# -----------------------------------

LLAMA_API_URL = os.getenv(
    "LLAMA_API_URL",
    "http://localhost:11434/api/generate"
)

# -----------------------------------
# Redis Queue
# -----------------------------------

TEXT_QUEUE = os.getenv(
    "TEXT_QUEUE",
    "fliqz_moderation_stream_text_queue"
)

# -----------------------------------
# Worker settings
# -----------------------------------

REDIS_BRPOP_TIMEOUT = int(
    os.getenv("REDIS_BRPOP_TIMEOUT", 5)
)

# -----------------------------------
# Debug prints
# -----------------------------------

print("\n========== CONFIG ==========")

print("DB_HOST      :", repr(DB_HOST))
print("DB_PORT      :", repr(DB_PORT))
print("DB_USER      :", repr(DB_USER))
print("DB_DATABASE  :", repr(DB_DATABASE))

print("REDIS_HOST   :", repr(REDIS_HOST))
print("REDIS_PORT   :", repr(REDIS_PORT))

print("TEXT_QUEUE   :", repr(TEXT_QUEUE))

print("============================\n")