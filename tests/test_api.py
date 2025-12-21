from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_predict_ok():
    payload = {"age": 41, "revenu_mensuel": 3000, "heure_supplementaires": True}
    r = client.post("/predict", json=payload)
    assert r.status_code == 200, r.text

    data = r.json()
    assert "proba" in data
    assert "prediction" in data
    assert "threshold" in data


def test_predict_validation_error():
    # manque "age" -> validation Pydantic => 422
    payload = {"revenu_mensuel": 3000, "heure_supplementaires": True}
    r = client.post("/predict", json=payload)
    assert r.status_code == 422