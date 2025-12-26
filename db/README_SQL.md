# Technova ML API – Documentation SQL & Base de Données

## Objectif
Ce document décrit en détail l’architecture de la base de données PostgreSQL utilisée par **Technova ML API**.
La base est organisée selon une approche analytique en couches : **RAW → STAGING → MART → AUDIT**.

---

### Initialisation de la base de données

Les scripts SQL doivent être exécutés dans l’ordre suivant afin de garantir
la cohérence des données et des dépendances entre les schémas :

1. `schema.sql` : création des schémas PostgreSQL (raw, staging, mart, audit)
2. `raw.sql` : création des tables de données brutes
3. `load_raw.sql` : chargement des données sources
4. `staging.sql` : nettoyage, normalisation et jointure des données
5. `mart.sql` : création du dataset final pour le modèle ML
6. `audit.sql` : création des tables de traçabilité des prédictions

Cet ordre permet d’assurer l’intégrité des données et la reproductibilité
du pipeline de traitement.

Les scripts sont conçus pour être idempotents
(`DROP TABLE IF EXISTS`, `TRUNCATE`) afin de permettre
une réexécution sans effet de bord.

## Vue d’ensemble du pipeline de données

```text
RAW
 ├─ extrait_sirh
 ├─ extrait_eval
 └─ extrait_sondage
        │
        ▼
STAGING
 └─ employee_base
        │
        ▼
MART
 └─ employee_features
        │
        ├─ utilisé par le modèle de Machine Learning
        ▼
AUDIT
 ├─ prediction_requests
 └─ prediction_responses
```

---

## Diagramme UML – Modèle de données (ERD)

```mermaid
erDiagram

    RAW_EXTRAIT_SIRH {
        INT id_employee
        INT age
        TEXT genre
        INT revenu_mensuel
        TEXT statut_marital
        TEXT departement
        TEXT poste
        INT nombre_experiences_precedentes
        INT annee_experience_totale
        INT annees_dans_l_entreprise
        INT annees_dans_le_poste_actuel
    }

    RAW_EXTRAIT_EVAL {
        TEXT eval_number
        INT satisfaction_employee_environnement
        INT note_evaluation_precedente
        INT niveau_hierarchique_poste
        INT satisfaction_employee_nature_travail
        INT satisfaction_employee_equipe
        INT satisfaction_employee_equilibre_pro_perso
        INT note_evaluation_actuelle
        TEXT heure_supplementaires
        TEXT augementation_salaire_precedente
    }

    RAW_EXTRAIT_SONDAGE {
        INT code_sondage
        TEXT a_quitte_l_entreprise
        INT nombre_participation_pee
        INT nb_formations_suivies
        INT distance_domicile_travail
        INT niveau_education
        TEXT domaine_etude
        TEXT frequence_deplacement
        INT annees_depuis_la_derniere_promotion
        INT annes_sous_responsable_actuel
    }

    STAGING_EMPLOYEE_BASE {
        INT id_employee
        INT age
        TEXT genre
        INT revenu_mensuel
        TEXT statut_marital
        TEXT departement
        TEXT poste
        BOOLEAN heure_supplementaires
        BOOLEAN a_quitte_l_entreprise
    }

    MART_EMPLOYEE_FEATURES {
        INT id_employee
        FLOAT ratio_manager_anciennete
        FLOAT mobilite_relative
        INT evolution_performance
        FLOAT pression_stagnation
        BOOLEAN a_quitte_l_entreprise
    }

    AUDIT_PREDICTION_REQUESTS {
        BIGINT request_id PK
        TIMESTAMPTZ created_at
        INT id_employee
        JSONB payload
    }

    AUDIT_PREDICTION_RESPONSES {
        BIGINT response_id PK
        BIGINT request_id FK
        FLOAT proba
        INT prediction
        FLOAT threshold
    }

    RAW_EXTRAIT_SIRH }o--|| STAGING_EMPLOYEE_BASE : clean
    RAW_EXTRAIT_EVAL }o--|| STAGING_EMPLOYEE_BASE : clean
    RAW_EXTRAIT_SONDAGE }o--|| STAGING_EMPLOYEE_BASE : clean

    STAGING_EMPLOYEE_BASE ||--|| MART_EMPLOYEE_FEATURES : feature_engineering
    AUDIT_PREDICTION_REQUESTS ||--o{ AUDIT_PREDICTION_RESPONSES : logs
```

---

## Description des couches

### RAW
- Données brutes issues de différentes sources RH.
- Aucune transformation.
- Chargement via scripts SQL (`COPY`).

### STAGING
- Nettoyage des valeurs.
- Normalisation des types.
- Jointure des sources autour de `id_employee`.

### MART
- Dataset final utilisé par le modèle de Machine Learning.
- Features calculées (ratios, évolutions, indicateurs).
- Contient la cible `a_quitte_l_entreprise`.

### AUDIT
- Journalisation des appels API.
- Séparation claire entre requêtes et réponses.
- Garantit la traçabilité et l’auditabilité des prédictions.

---

