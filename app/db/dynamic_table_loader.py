# dynamic_table_loader.py
from sqlalchemy import MetaData, Table
from app.db.database import engine

metadata = MetaData()

def get_dynamic_table(table_name: str):
    """
    Load ANY table dynamically at runtime (reflection).
    """
    return Table(table_name, metadata, autoload_with=engine)
