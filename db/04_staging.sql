-- =====================================================
-- 04_staging.sql — Nettoyage + normalisation (STAGING)
-- =====================================================

-- Sécurité: recréer proprement
DROP TABLE IF EXISTS staging.sirh_clean;
DROP TABLE IF EXISTS staging.eval_clean;
DROP TABLE IF EXISTS staging.sondage_clean;
DROP TABLE IF EXISTS staging.employee_base;

-- -------------------------
-- 1) SIRH
-- - supprimer nombre_heures_travailless (valeur constante 80)
-- - normaliser genre (Homme/Femme vs M/F)
-- -------------------------
CREATE TABLE staging.sirh_clean AS
SELECT
    id_employee,
    age,
    CASE
        WHEN lower(trim(genre)) IN ('h', 'homme', 'm') THEN 'Homme'
        WHEN lower(trim(genre)) IN ('f', 'femme') THEN 'Femme'
        ELSE NULL
    END AS genre,
    revenu_mensuel,
    statut_marital,
    departement,
    poste,
    nombre_experiences_precedentes,
    annee_experience_totale,
    annees_dans_l_entreprise,
    annees_dans_le_poste_actuel
FROM raw.extrait_sirh;

-- -------------------------
-- 2) EVAL
-- - heure_supplementaires -> bool
-- - augmentation salaire -> numérique (retirer %)
-- - eval_number: retirer "e_" -> int
-- - renommer eval_number -> id_employee
-- -------------------------
CREATE TABLE staging.eval_clean AS
SELECT
    CAST(replace(lower(trim(eval_number)), 'e_', '') AS INT) AS id_employee,

    satisfaction_employee_environnement,
    note_evaluation_precedente,
    niveau_hierarchique_poste,
    satisfaction_employee_nature_travail,
    satisfaction_employee_equipe,
    satisfaction_employee_equilibre_pro_perso,
    note_evaluation_actuelle,

    CASE
        WHEN lower(trim(heure_supplementaires)) IN ('yes', 'y', 'oui', 'true', '1') THEN TRUE
        WHEN lower(trim(heure_supplementaires)) IN ('no', 'n', 'non', 'false', '0') THEN FALSE
        ELSE NULL
    END AS heure_supplementaires,

    NULLIF(REPLACE(TRIM(augementation_salaire_precedente), '%', ''), '')::INT AS augmentation_salaire_precedente
FROM raw.extrait_eval;

-- -------------------------
-- 3) SONDAGE
-- - supprimer ayant_enfants (constante Y)
-- - supprimer nombre_employee_sous_responsabilite (constante 1)
-- - a_quitte_l_entreprise -> bool
-- - code_sondage -> id_employee
-- - annes_sous_responsable_actuel -> annees_sous_responsable_actuel
-- -------------------------
CREATE TABLE staging.sondage_clean AS
SELECT
    code_sondage AS id_employee,

    CASE
        WHEN lower(trim(a_quitte_l_entreprise)) IN ('yes', 'y', 'oui', 'true', '1') THEN TRUE
        WHEN lower(trim(a_quitte_l_entreprise)) IN ('no', 'n', 'non', 'false', '0') THEN FALSE
        ELSE NULL
    END AS a_quitte_l_entreprise,

    nombre_participation_pee,
    nb_formations_suivies,

    distance_domicile_travail,
    niveau_education,
    domaine_etude,
    frequence_deplacement,
    annees_depuis_la_derniere_promotion,

    annes_sous_responsable_actuel AS annees_sous_responsable_actuel
FROM raw.extrait_sondage;

-- -------------------------
-- 4) Jointure STAGING (1 ligne = 1 employé)
-- -------------------------
CREATE TABLE staging.employee_base AS
SELECT
    s.*,
    e.satisfaction_employee_environnement,
    e.note_evaluation_precedente,
    e.niveau_hierarchique_poste,
    e.satisfaction_employee_nature_travail,
    e.satisfaction_employee_equipe,
    e.satisfaction_employee_equilibre_pro_perso,
    e.note_evaluation_actuelle,
    e.heure_supplementaires,
    e.augmentation_salaire_precedente,
    so.a_quitte_l_entreprise,
    so.nombre_participation_pee,
    so.nb_formations_suivies,
    so.distance_domicile_travail,
    so.niveau_education,
    so.domaine_etude,
    so.frequence_deplacement,
    so.annees_depuis_la_derniere_promotion,
    so.annees_sous_responsable_actuel
FROM staging.sirh_clean s
LEFT JOIN staging.eval_clean e USING (id_employee)
LEFT JOIN staging.sondage_clean so USING (id_employee);