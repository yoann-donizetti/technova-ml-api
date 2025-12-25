from sqlalchemy import create_engine
from app.core.config import settings

engine = None
if settings.DATABASE_URL:
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)