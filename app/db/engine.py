from app.core.config import get_settings
from sqlalchemy import create_engine
# Initialise la connexion à la base de données à partir de la configuration centralisée
def get_engine():
    settings = get_settings()
    if not settings.DATABASE_URL:
        return None
    return create_engine(settings.DATABASE_URL, pool_pre_ping=True)