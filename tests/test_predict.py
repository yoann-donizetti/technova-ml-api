# tests/test_services_predict.py
import pytest


def test_run_predict_manual_without_engine(monkeypatch):
    """
    Cas simple : engine=None => pas d'audit, on renvoie proba/pred/payload enrichi.
    """
    from app.services import predict as predict_service

    # Fake predict_manual (ML)
    def fake_predict_manual(payload, model, threshold):
        return 0.8, 1, {"x": 1, "enrich": True}

    monkeypatch.setattr(predict_service, "predict_manual", fake_predict_manual)

    proba, pred, payload_enrichi = predict_service.run_predict_manual(
        payload={"x": 1},
        model=object(),
        threshold=0.3,
        engine=None,
    )

    assert proba == 0.8
    assert pred == 1
    assert payload_enrichi["enrich"] is True


def test_run_predict_manual_with_engine_calls_audit(monkeypatch):
    """
    Cas engine présent : log_audit doit être appelé.
    """
    from app.services import predict as predict_service

    # Fake predict_manual
    def fake_predict_manual(payload, model, threshold):
        return 0.2, 0, {"foo": "bar"}

    monkeypatch.setattr(predict_service, "predict_manual", fake_predict_manual)

    # Spy log_audit
    calls = {"count": 0, "args": None}

    def fake_log_audit(conn, payload, proba, prediction, threshold):
        calls["count"] += 1
        calls["args"] = (conn, payload, proba, prediction, threshold)
        return 123

    monkeypatch.setattr(predict_service, "log_audit", fake_log_audit)

    # Dummy engine.begin() context manager
    class DummyEngine:
        def begin(self):
            return self

        def __enter__(self):
            return "dummy-conn"

        def __exit__(self, exc_type, exc, tb):
            return False

    proba, pred, payload_enrichi = predict_service.run_predict_manual(
        payload={"hello": "world"},
        model=object(),
        threshold=0.292,
        engine=DummyEngine(),
    )

    assert proba == 0.2
    assert pred == 0
    assert payload_enrichi == {"foo": "bar"}
    assert calls["count"] == 1
    assert calls["args"][0] == "dummy-conn"
    assert calls["args"][1] == {"foo": "bar"}
    assert calls["args"][2] == 0.2
    assert calls["args"][3] == 0
    assert calls["args"][4] == 0.292


def test_run_predict_by_id_not_found_raises_keyerror(monkeypatch):
    """
    Cas id absent : get_employee_features_by_id renvoie None => KeyError attendu.
    """
    from app.services import predict as predict_service

    def fake_get_employee_features_by_id(engine, id_employee):
        return None

    monkeypatch.setattr(predict_service, "get_employee_features_by_id", fake_get_employee_features_by_id)

    with pytest.raises(KeyError):
        predict_service.run_predict_by_id(
            id_employee=999,
            model=object(),
            threshold=0.5,
            engine=object(),
        )


def test_run_predict_by_id_with_engine_calls_audit_and_adds_id(monkeypatch):
    """
    Cas nominal : on récupère un employé, on prédit, on log en audit,
    et on ajoute id_employee dans payload_enrichi avant log.
    """
    from app.services import predict as predict_service

    # Fake features fetch
    def fake_get_employee_features_by_id(engine, id_employee):
        return {"id_employee": id_employee, "age": 40}

    monkeypatch.setattr(predict_service, "get_employee_features_by_id", fake_get_employee_features_by_id)

    # Fake predict_from_employee_features
    def fake_predict_from_employee_features(employee, model, threshold):
        # payload enrichi sans id -> le service doit l'ajouter
        return 0.55, 1, {"age": employee["age"]}

    monkeypatch.setattr(predict_service, "predict_from_employee_features", fake_predict_from_employee_features)

    # Spy log_audit
    calls = {"count": 0, "payload": None}

    def fake_log_audit(conn, payload, proba, prediction, threshold):
        calls["count"] += 1
        calls["payload"] = payload
        return 456

    monkeypatch.setattr(predict_service, "log_audit", fake_log_audit)

    class DummyEngine:
        def begin(self):
            return self

        def __enter__(self):
            return "dummy-conn"

        def __exit__(self, exc_type, exc, tb):
            return False

    proba, pred, payload_enrichi = predict_service.run_predict_by_id(
        id_employee=7,
        model=object(),
        threshold=0.292,
        engine=DummyEngine(),
    )

    assert proba == 0.55
    assert pred == 1
    assert payload_enrichi["age"] == 40
    assert payload_enrichi["id_employee"] == 7

    assert calls["count"] == 1
    assert calls["payload"]["id_employee"] == 7