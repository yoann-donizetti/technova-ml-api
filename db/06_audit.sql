-- =====================================================
-- AUDIT : Traçabilité des appels API / prédictions
-- =====================================================

CREATE SCHEMA IF NOT EXISTS audit;

-- 1) Requêtes (inputs envoyés au modèle)
DROP TABLE IF EXISTS audit.prediction_requests;

CREATE TABLE audit.prediction_requests (
    request_id    BIGSERIAL PRIMARY KEY,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    id_employee   INT NULL,
    payload       JSONB NOT NULL
);

-- 2) Réponses (outputs générés par le modèle)
DROP TABLE IF EXISTS audit.prediction_responses;

CREATE TABLE audit.prediction_responses (
    response_id    BIGSERIAL PRIMARY KEY,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    request_id     BIGINT NOT NULL
                 REFERENCES audit.prediction_requests(request_id)
                 ON DELETE CASCADE,

    proba          DOUBLE PRECISION NOT NULL,
    prediction     INT NOT NULL,
    threshold      DOUBLE PRECISION NOT NULL,

    status         TEXT NOT NULL DEFAULT 'OK',
    error_message  TEXT NULL
);

-- Index utiles
CREATE INDEX IF NOT EXISTS idx_pred_req_employee
  ON audit.prediction_requests(id_employee);

CREATE INDEX IF NOT EXISTS idx_pred_req_created_at
  ON audit.prediction_requests(created_at);

CREATE INDEX IF NOT EXISTS idx_pred_res_request_id
  ON audit.prediction_responses(request_id);
