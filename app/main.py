import os
import json
import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from huggingface_hub import hf_hub_download


# --------------------------------------------------
# CONFIG
# --------------------------------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # ex: postgresql+psycopg://user:pwd@host:5432/db

HF_MODEL_REPO = os.getenv("HF_MODEL_REPO")          # ex: donizetti-yoann/technova-ml-model
HF_MODEL_FILENAME = os.getenv("HF_MODEL_FILENAME")  # ex: model.joblib

THRESHOLD_PATH = os.getenv("THRESHOLD_PATH", "config/threshold.json")

engine = None
if DATABASE_URL:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

app = FastAPI(title="Technova ML API", version="0.2.3")


# --------------------------------------------------
# SCHEMAS Pydantic
# --------------------------------------------------
class PredictionRequest(BaseModel):
    age: int = Field(..., ge=0)
    genre: str
    revenu_mensuel: int = Field(..., ge=0)
    statut_marital: str
    departement: str
    poste: str
    nombre_experiences_precedentes: int = Field(..., ge=0)
    annees_dans_l_entreprise: int = Field(..., ge=0)

    satisfaction_employee_environnement: int = Field(..., ge=0)
    satisfaction_employee_nature_travail: int = Field(..., ge=0)
    satisfaction_employee_equipe: int = Field(..., ge=0)
    satisfaction_employee_equilibre_pro_perso: int = Field(..., ge=0)

    heure_supplementaires: bool
    augmentation_salaire_precedente: int = Field(..., ge=0)
    nombre_participation_pee: int = Field(..., ge=0)
    nb_formations_suivies: int = Field(..., ge=0)
    distance_domicile_travail: int = Field(..., ge=0)
    niveau_education: int = Field(..., ge=0)
    domaine_etude: str
    frequence_deplacement: str

    # champs nécessaires au calcul des features
    annees_sous_responsable_actuel: int = Field(..., ge=0)
    annees_dans_le_poste_actuel: int = Field(..., ge=0)
    note_evaluation_actuelle: int
    note_evaluation_precedente: int
    annees_depuis_la_derniere_promotion: int = Field(..., ge=0)


class PredictionResponse(BaseModel):
    proba: float
    prediction: int
    threshold: float


# --------------------------------------------------
# STARTUP
# --------------------------------------------------
@app.on_event("startup")
def startup():
    # --- modèle depuis Hugging Face Hub ---
    if not HF_MODEL_REPO or not HF_MODEL_FILENAME:
        raise RuntimeError("HF_MODEL_REPO and/or HF_MODEL_FILENAME not set")

    model_path = hf_hub_download(
        repo_id=HF_MODEL_REPO,
        filename=HF_MODEL_FILENAME,
    )
    app.state.model = joblib.load(model_path)

    # --- threshold ---
    if not os.path.exists(THRESHOLD_PATH):
        raise FileNotFoundError(f"Threshold file not found: {THRESHOLD_PATH}")

    with open(THRESHOLD_PATH, "r", encoding="utf-8") as f:
        app.state.threshold = float(json.load(f)["threshold"])

    print("[startup] model loaded from HF + threshold loaded OK")


# --------------------------------------------------
# ROUTES
# --------------------------------------------------
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": getattr(app.state, "model", None) is not None,
        "threshold": float(getattr(app.state, "threshold", 0.0)),
        "db_configured": engine is not None,
        "hf_model_repo": HF_MODEL_REPO,
        "hf_model_filename": HF_MODEL_FILENAME,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionRequest):
    try:
        # ------------------------------
        # 1) Conversion en DataFrame
        # ------------------------------
        df = pd.DataFrame([data.model_dump()])

        # ------------------------------
        # 1bis) Normalisation texte -> minuscule
        # ------------------------------
        TEXT_COLUMNS = [
            "genre",
            "statut_marital",
            "departement",
            "poste",
            "domaine_etude",
            "frequence_deplacement",
        ]
        for col in TEXT_COLUMNS:
            df[col] = df[col].astype(str).str.strip().str.lower()

        # ------------------------------
        # 2) Feature engineering
        # ------------------------------
        df["ratio_manager_anciennete"] = (
            (df["annees_sous_responsable_actuel"] + 1)
            / (df["annees_dans_l_entreprise"] + 1)
        )

        mobilite_interne = (
            df["annees_dans_l_entreprise"]
            - df["annees_dans_le_poste_actuel"]
        )
        df["mobilite_relative"] = mobilite_interne / (
            df["annees_dans_l_entreprise"] + 1
        )

        df["evolution_performance"] = (
            df["note_evaluation_actuelle"]
            - df["note_evaluation_precedente"]
        )

        df["pression_stagnation"] = (
            df["annees_depuis_la_derniere_promotion"]
            / (df["annees_dans_l_entreprise"] + 1)
        )

        # Colonnes finales attendues par le modèle
        X = df[
            [
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
        ]

        # ------------------------------
        # 3) Prédiction
        # ------------------------------
        proba = float(app.state.model.predict_proba(X)[0][1])
        threshold = float(app.state.threshold)
        prediction = int(proba >= threshold)

        # ------------------------------
        # 4) Audit en base (si DB configurée)
        # -> on log le payload ENRICHI (avec features calculées)
        # ------------------------------
        if engine is not None:
            payload_enrichi = df.iloc[0].to_dict()

            with engine.begin() as conn:
                req_id = conn.execute(
                    text(
                        """
                        INSERT INTO audit.prediction_requests (payload)
                        VALUES (CAST(:payload AS jsonb))
                        RETURNING request_id
                        """
                    ),
                    {
                        "payload": json.dumps(
                            payload_enrichi,
                            ensure_ascii=False,
                            default=str,
                        )
                    },
                ).scalar_one()

                conn.execute(
                    text(
                        """
                        INSERT INTO audit.prediction_responses
                        (request_id, proba, prediction, threshold)
                        VALUES (:request_id, :proba, :prediction, :threshold)
                        """
                    ),
                    {
                        "request_id": req_id,
                        "proba": proba,
                        "prediction": prediction,
                        "threshold": threshold,
                    },
                )

        return PredictionResponse(
            proba=proba,
            prediction=prediction,
            threshold=threshold,
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Prediction error: {str(e)}",
        )
