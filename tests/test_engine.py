from app.db.engine import get_engine
from app.core.config import get_settings

def test_get_engine_without_database_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    get_settings.cache_clear()

    engine = get_engine()
    assert engine is None