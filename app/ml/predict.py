import pandas as pd
from app.ml.preprocessing import normalize_text

# Colonnes attendues par le modèle
FEATURE_COLUMNS = [
    "age",
    "genre",
    "revenu_mensuel",
    "statut_marital",
    "departement",
    "poste",
    "nombre_experiences_precedentes",
    "annees_dans_l_entreprise",
    "satisfaction_employee_environnement",
    "satisfaction_employee_nature_travail",
    "satisfaction_employee_equipe",
    "satisfaction_employee_equilibre_pro_perso",
    "heure_supplementaires",
    "augmentation_salaire_precedente",
    "nombre_participation_pee",
    "nb_formations_suivies",
    "distance_domicile_travail",
    "niveau_education",
    "domaine_etude",
    "frequence_deplacement",
    "ratio_manager_anciennete",
    "mobilite_relative",
    "evolution_performance",
    "pression_stagnation",
]


def add_features_from_raw(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute les features calculées À PARTIR DES CHAMPS BRUTS (manuel)."""
    df = df.copy()

    df["ratio_manager_anciennete"] = (
        (df["annees_sous_responsable_actuel"] + 1)
        / (df["annees_dans_l_entreprise"] + 1)
    )

    mobilite_interne = df["annees_dans_l_entreprise"] - df["annees_dans_le_poste_actuel"]
    df["mobilite_relative"] = mobilite_interne / (df["annees_dans_l_entreprise"] + 1)

    df["evolution_performance"] = df["note_evaluation_actuelle"] - df["note_evaluation_precedente"]

    df["pression_stagnation"] = (
        df["annees_depuis_la_derniere_promotion"]
        / (df["annees_dans_l_entreprise"] + 1)
    )

    return df


def predict_manual(payload: dict, model, threshold: float):
    """
    Cas /predict (manuel) : payload = champs bruts => on calcule features.
    """
    df = pd.DataFrame([payload])
    df = normalize_text(df)
    df = add_features_from_raw(df)

    X = df[FEATURE_COLUMNS]
    proba = float(model.predict_proba(X)[0][1])
    pred = int(proba >= float(threshold))

    payload_enrichi = df.iloc[0].to_dict()
    return proba, pred, payload_enrichi


def predict_from_employee_features(employee_row: dict, model, threshold: float):
    """
    Cas /predict/{id_employee} : la table mart.employee_features doit déjà contenir
    les colonnes calculées (ratio_manager_anciennete, etc.).
    """
    df = pd.DataFrame([employee_row])
    df = normalize_text(df)

    X = df[FEATURE_COLUMNS]
    proba = float(model.predict_proba(X)[0][1])
    pred = int(proba >= float(threshold))

    payload_enrichi = df.iloc[0].to_dict()
    return proba, pred, payload_enrichi