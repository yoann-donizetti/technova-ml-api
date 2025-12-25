import pandas as pd

TEXT_COLUMNS = [
    "genre",
    "statut_marital",
    "departement",
    "poste",
    "domaine_etude",
    "frequence_deplacement",
]


def normalize_text(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in TEXT_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
    return df