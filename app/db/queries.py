from sqlalchemy import text

SQL_INSERT_REQUEST = text("""
INSERT INTO audit.prediction_requests (payload)
VALUES (CAST(:payload AS jsonb))
RETURNING request_id
""")

SQL_INSERT_RESPONSE = text("""
INSERT INTO audit.prediction_responses
(request_id, proba, prediction, threshold)
VALUES (:request_id, :proba, :prediction, :threshold)
""")

SQL_GET_EMPLOYEE_FEATURES = text("""
SELECT *
FROM mart.employee_features
WHERE id_employee = :id_employee
LIMIT 1
""")