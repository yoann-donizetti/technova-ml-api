import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings


@pytest.fixture
def client(monkeypatch):
    # 1) On force une clé connue pour les tests
    monkeypatch.setenv("API_KEY", "test-key")

    # 2) IMPORTANT : vider le cache pour relire l'env
    get_settings.cache_clear()

    # 3) Import de l'app APRES le setenv (évite les surprises)
    from app.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_headers():
    # On génère le header depuis les settings réellement utilisés
    s = get_settings()
    return {"X-API-Key": s.API_KEY}