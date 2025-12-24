-- =====================================================
-- MART — Dataset final pour le modèle ML
-- =====================================================

CREATE SCHEMA IF NOT EXISTS mart;

DROP TABLE IF EXISTS mart.employee_features;

CREATE TABLE mart.employee_features AS
SELECT
    -- Identifiant (utile pour tracer / relier / debug)
    id_employee,

    -- =========================
    -- Variables de base (X)
    -- =========================
    age,
    genre,
    revenu_mensuel,
    statut_marital,
    departement,
    poste,
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
    domaine_etude,
    frequence_deplacement,

    -- =========================
    -- Features calculées
    -- =========================

    -- (annees_sous_responsable_actuel + 1) / (annees_dans_l_entreprise + 1)
    (
      (COALESCE(annees_sous_responsable_actuel, 0) + 1)::double precision
      /
      (COALESCE(annees_dans_l_entreprise, 0) + 1)::double precision
    ) AS ratio_manager_anciennete,

    -- mobilite_interne = annees_dans_l_entreprise - annees_dans_le_poste_actuel
    -- mobilite_relative = mobilite_interne / (annees_dans_l_entreprise + 1)
    (
      (COALESCE(annees_dans_l_entreprise, 0) - COALESCE(annees_dans_le_poste_actuel, 0))::double precision
      /
      (COALESCE(annees_dans_l_entreprise, 0) + 1)::double precision
    ) AS mobilite_relative,

    -- evolution_performance = note_evaluation_actuelle - note_evaluation_precedente
    (COALESCE(note_evaluation_actuelle, 0) - COALESCE(note_evaluation_precedente, 0)) AS evolution_performance,

    -- pression_stagnation = annees_depuis_la_derniere_promotion / (annees_dans_l_entreprise + 1)
    (
      COALESCE(annees_depuis_la_derniere_promotion, 0)::double precision
      /
      (COALESCE(annees_dans_l_entreprise, 0) + 1)::double precision
    ) AS pression_stagnation,

    -- =========================
    -- Target (y) pour training / audit
    -- =========================
    a_quitte_l_entreprise

FROM staging.employee_base;

-- (Optionnel mais utile) : index pour requêtes par id_employee
CREATE INDEX IF NOT EXISTS idx_mart_employee_features_id
ON mart.employee_features(id_employee);