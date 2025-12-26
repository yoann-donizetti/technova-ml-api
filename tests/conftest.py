# tests/conftest.py
import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")      # <-- clé du fix
    monkeypatch.setenv("API_KEY", "test-key")

    get_settings.cache_clear()

    from app.main import app
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_headers():
    return {"X-API-Key": "test-key"}