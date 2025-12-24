import os
from sqlalchemy import create_engine

def get_engine():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL manquant.")
    return create_engine(db_url, pool_pre_ping=True)