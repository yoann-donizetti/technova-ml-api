-- =====================================================
-- MART — Dataset final pour le modèle ML
-- =====================================================

CREATE SCHEMA IF NOT EXISTS mart;

DROP TABLE IF EXISTS mart.employee_features;

CREATE TABLE mart.employee_features AS
SELECT
    -- Identifiant
    id_employee,

    -- =========================
    -- Variables de base (X)
    -- =========================
    age,

    lower(trim(genre)) AS genre,
    revenu_mensuel,
    lower(trim(statut_marital)) AS statut_marital,
    lower(trim(departement)) AS departement,
    lower(trim(poste)) AS poste,

    nombre_experiences_precedentes,
    annees_dans_l_entreprise,

    satisfaction_employee_environnement,
    satisfaction_employee_nature_travail,
    satisfaction_employee_equipe,
    satisfaction_employee_equilibre_pro_perso,

    heure_supplementaires,
    augmentation_salaire_precedente,
    nombre_participation_pee,
    nb_formations_suivies,
    distance_domicile_travail,
    niveau_education,

    lower(trim(domaine_etude)) AS domaine_etude,
    lower(trim(frequence_deplacement)) AS frequence_deplacement,

    -- =========================
    -- Features calculées
    -- =========================
    (
      (COALESCE(annees_sous_responsable_actuel, 0) + 1)::double precision
      /
      (COALESCE(annees_dans_l_entreprise, 0) + 1)::double precision
    ) AS ratio_manager_anciennete,

    (
      (COALESCE(annees_dans_l_entreprise, 0) - COALESCE(annees_dans_le_poste_actuel, 0))::double precision
      /
      (COALESCE(annees_dans_l_entreprise, 0) + 1)::double precision
    ) AS mobilite_relative,

    (COALESCE(note_evaluation_actuelle, 0) - COALESCE(note_evaluation_precedente, 0)) AS evolution_performance,

    (
      COALESCE(annees_depuis_la_derniere_promotion, 0)::double precision
      /
      (COALESCE(annees_dans_l_entreprise, 0) + 1)::double precision
    ) AS pression_stagnation,

    -- =========================
    -- Target (y)
    -- =========================
    a_quitte_l_entreprise

FROM staging.employee_base;

CREATE INDEX IF NOT EXISTS idx_mart_employee_features_id
ON mart.employee_features(id_employee);