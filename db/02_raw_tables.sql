-- =====================================================
-- Tables RAW - données brutes sans transformation
-- =====================================================

-- -------------------------------
-- Table extrait_sirh
-- -------------------------------
DROP TABLE IF EXISTS raw.extrait_sirh;
CREATE TABLE raw.extrait_sirh (
    id_employee INTEGER,
    age INTEGER,
    genre TEXT,
    revenu_mensuel INTEGER,
    statut_marital TEXT,
    departement TEXT,
    poste TEXT,
    nombre_experiences_precedentes INTEGER,
    nombre_heures_travailless INTEGER,
    annee_experience_totale INTEGER,
    annees_dans_l_entreprise INTEGER,
    annees_dans_le_poste_actuel INTEGER
);

-- -------------------------------
-- Table extrait_eval
-- -------------------------------
DROP TABLE IF EXISTS raw.extrait_eval;
CREATE TABLE raw.extrait_eval (
    satisfaction_employee_environnement INTEGER,
    note_evaluation_precedente INTEGER,
    niveau_hierarchique_poste INTEGER,
    satisfaction_employee_nature_travail INTEGER,
    satisfaction_employee_equipe INTEGER,
    satisfaction_employee_equilibre_pro_perso INTEGER,
    eval_number TEXT,
    note_evaluation_actuelle INTEGER,
    heure_supplementaires TEXT,
    augementation_salaire_precedente TEXT
);

-- -------------------------------
-- Table extrait_sondage
-- -------------------------------
DROP TABLE IF EXISTS raw.extrait_sondage;
CREATE TABLE raw.extrait_sondage (
    a_quitte_l_entreprise TEXT,
    nombre_participation_pee INTEGER,
    nb_formations_suivies INTEGER,
    nombre_employee_sous_responsabilite INTEGER,
    code_sondage INTEGER,
    distance_domicile_travail INTEGER,
    niveau_education INTEGER,
    domaine_etude TEXT,
    ayant_enfants TEXT,
    frequence_deplacement TEXT,
    annees_depuis_la_derniere_promotion INTEGER,
    annes_sous_responsable_actuel INTEGER
);