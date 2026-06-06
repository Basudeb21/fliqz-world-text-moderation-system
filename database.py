# database.py

import os

from dotenv import load_dotenv

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

print("\n========== DATABASE ==========")

print("DB_USER      :", repr(DB_USER))
print("DB_HOST      :", repr(DB_HOST))
print("DB_PORT      :", repr(DB_PORT))
print("DB_DATABASE  :", repr(DB_DATABASE))

print("DATABASE URL :", URL)

print("==============================\n")

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