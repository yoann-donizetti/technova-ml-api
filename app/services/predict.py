from app.services.audit import log_audit
from app.services.features import get_employee_features_by_id

from app.ml.predict import predict_manual, predict_from_employee_features


def run_predict_manual(payload: dict, model, threshold: float, engine):
    '''
    Gère une prédiction à partir des données envoyées par l’utilisateur.
    '''
    proba, pred, payload_enrichi = predict_manual(payload, model, threshold)

    if engine is not None:
        with engine.begin() as conn:
            log_audit(conn, payload_enrichi, proba, pred, threshold)

    return proba, pred, payload_enrichi


def run_predict_by_id(id_employee: int, model, threshold: float, engine):
    '''
    Gère une prédiction à partir d’un employé existant en base.
    '''
    employee = get_employee_features_by_id(engine, id_employee)
    if employee is None:
        raise KeyError(f"id_employee {id_employee} introuvable dans mart.employee_features")

    proba, pred, payload_enrichi = predict_from_employee_features(employee, model, threshold)

    if engine is not None:
        with engine.begin() as conn:
            payload_enrichi["id_employee"] = id_employee
            log_audit(conn, payload_enrichi, proba, pred, threshold)

    return proba, pred, payload_enrichi