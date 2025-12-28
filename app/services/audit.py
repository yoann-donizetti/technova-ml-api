import json
from sqlalchemy import Connection

from app.db.queries import SQL_INSERT_REQUEST, SQL_INSERT_RESPONSE


def log_audit(conn: Connection, payload: dict, proba: float, prediction: int, threshold: float) -> int:

    '''
        log_audit sert à enregistrer une prédiction dans la base de données
        Elle trace :
        ce que l’API a reçu (entrée)
        ce que le modèle a produit (sortie)
    '''


    req_id = conn.execute(
        SQL_INSERT_REQUEST,
        {"payload": json.dumps(payload, ensure_ascii=False, default=str)},
    ).scalar_one()#récupère l’id généré par la base (clé primaire)

    conn.execute(
        SQL_INSERT_RESPONSE,
        {
            "request_id": req_id,
            "proba": float(proba),
            "prediction": int(prediction),
            "threshold": float(threshold),
        },
    )
    return int(req_id)