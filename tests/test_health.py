def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200

    data = r.json()
    assert data["status"] == "ok"
    assert "model_loaded" in data
    assert "threshold" in data
    assert "db_configured" in data
