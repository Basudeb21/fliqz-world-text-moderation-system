# database.py

import os

from dotenv import load_dotenv
from app.utils.logger import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# -----------------------------------
# Load .env
# -----------------------------------

load_dotenv()

# -----------------------------------
# Database environment variables
# -----------------------------------

DB_USER = os.getenv(
    "DB_USER",
    "root"
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD",
    ""
)

DB_HOST = os.getenv(
    "DB_HOST",
    "localhost"
)

DB_PORT = os.getenv(
    "DB_PORT",
    "3306"
)

DB_DATABASE = os.getenv(
    "DB_DATABASE",
    "myvault"
)

# -----------------------------------
# SQLAlchemy URL
# -----------------------------------

URL = (
    f"mysql+pymysql://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}"
    f"/{DB_DATABASE}"
    f"?charset=utf8mb4"
)

# -----------------------------------
# Debug
# -----------------------------------


logger.info(
    f"Database Connected -> {DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)

# -----------------------------------
# SQLAlchemy Engine
# -----------------------------------

engine = create_engine(
    URL,
    pool_pre_ping=True,
    echo=False
)

# -----------------------------------
# Session Factory
# -----------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -----------------------------------
# Base ORM class
# -----------------------------------

Base = declarative_base()

# -----------------------------------
# DB Dependency
# -----------------------------------

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()