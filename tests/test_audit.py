def test_log_audit_returns_request_id(monkeypatch):
    from app.services.audit import log_audit

    class DummyResult:
        def scalar_one(self):
            return 42

    class DummyConn:
        def execute(self, *args, **kwargs):
            return DummyResult()

    req_id = log_audit(
        conn=DummyConn(),
        payload={"a": 1},
        proba=0.7,
        prediction=1,
        threshold=0.3,
    )

    assert req_id == 42