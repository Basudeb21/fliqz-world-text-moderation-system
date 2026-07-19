# app/config/settings.py

import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Application

DEBUG = (
    os.getenv("DEBUG", "false").lower() == "true"
)

LOG_MESSAGE_CONTENT = (
    os.getenv("LOG_MESSAGE_CONTENT", "false").lower() == "true"
)

# Database

DB_HOST = os.getenv(
    "DB_HOST",
    "localhost"
)

DB_PORT = int(
    os.getenv("DB_PORT", 3306)
)

DB_USER = os.getenv(
    "DB_USER",
    "root"
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD",
    ""
)

DB_DATABASE = os.getenv(
    "DB_DATABASE",
    "myvault"
)

# Redis

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

REDIS_BRPOP_TIMEOUT = int(
    os.getenv("REDIS_BRPOP_TIMEOUT", 5)
)

TEXT_QUEUE = os.getenv(
    "TEXT_QUEUE",
    "fliqz_moderation_stream_text_queue"
)

# Ollama
LLAMA_API_URL = os.getenv(
    "LLAMA_API_URL",
    "http://localhost:11434/api/generate"
)

LLAMA_API_URL_TWO = os.getenv(
    "LLAMA_API_URL_TWO",
    "http://localhost:11434/api/chat"
)

LLAMA_MODEL = os.getenv("LLAMA_MODEL", "qwen2.5:7b-instruct")