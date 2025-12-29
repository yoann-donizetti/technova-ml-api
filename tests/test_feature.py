def test_get_employee_features_not_found(monkeypatch):
    from app.services.features import get_employee_features_by_id

    class DummyResult:
        def mappings(self):
            return self

        def first(self):
            return None

    class DummyConn:
        def execute(self, *args, **kwargs):
            return DummyResult()

    class DummyEngine:
        def connect(self):
            return self
        def __enter__(self):
            return DummyConn()
        def __exit__(self, *args):
            pass

    result = get_employee_features_by_id(DummyEngine(), 999)
    assert result is None