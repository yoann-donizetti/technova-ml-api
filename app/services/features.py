from app.db.engine import engine
from app.db.queries import SQL_GET_EMPLOYEE_FEATURES


def get_employee_features_by_id(id_employee: int) -> dict | None:
    if engine is None:
        raise RuntimeError("DATABASE_URL non configurée (engine = None).")

    with engine.connect() as conn:
        row = conn.execute(SQL_GET_EMPLOYEE_FEATURES, {"id_employee": id_employee}).mappings().first()
        return dict(row) if row else None