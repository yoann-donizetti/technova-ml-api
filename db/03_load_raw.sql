-- =====================================================
-- 03_load_raw.sql — Chargement des données BRUTES
-- =====================================================

-- Nettoyage avant rechargement (idempotent)
TRUNCATE TABLE raw.extrait_sirh;
TRUNCATE TABLE raw.extrait_eval;
TRUNCATE TABLE raw.extrait_sondage;

-- -------------------------
-- Chargement SIRH
-- -------------------------
COPY raw.extrait_sirh
FROM 'C:/Users/yoann/OneDrive/Documents/OpenClassrooms/Déployez un modèle de Machine Learning/technova-ml-api/data/extrait_sirh.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

-- -------------------------
-- Chargement EVAL
-- -------------------------
COPY raw.extrait_eval
FROM 'C:/Users/yoann/OneDrive/Documents/OpenClassrooms/Déployez un modèle de Machine Learning/technova-ml-api/data/extrait_eval.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

-- -------------------------
-- Chargement SONDAGE
-- -------------------------
COPY raw.extrait_sondage
FROM 'C:/Users/yoann/OneDrive/Documents/OpenClassrooms/Déployez un modèle de Machine Learning/technova-ml-api/data/extrait_sondage.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';