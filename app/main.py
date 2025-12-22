import json
import os
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from huggingface_hub import hf_hub_download


from encoder.custom_encoder import CustomEncoder  

from app.schemas import PredictionRequest, PredictionResponse

# -------------------------------------------------------------------
# App
# -------------------------------------------------------------------
app = FastAPI(title="Technova ML API")

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
THRESHOLD_PATH = BASE_DIR / "config" / "threshold.json"

HF_MODEL_REPO = os.getenv("HF_MODEL_REPO", "donizetti-yoann/technova-ml-model")
HF_MODEL_FILENAME = os.getenv("HF_MODEL_FILENAME", "model.joblib")

# -------------------------------------------------------------------
# Utils
# -------------------------------------------------------------------
def load_threshold() -> float:
    with open(THRESHOLD_PATH, "r", encoding="utf-8") as f:
        return float(json.load(f)["threshold"])


def download_and_load_model():
    model_path = hf_hub_download(
        repo_id=HF_MODEL_REPO,
        filename=HF_MODEL_FILENAME,
    )
    return joblib.load(model_path)

# -------------------------------------------------------------------
# Startup
# -------------------------------------------------------------------
@app.on_event("startup")
def startup():
    """
    - En prod / HF Space : charge modèle + threshold
    - En tests : TESTING=1 → on ne télécharge rien
    """
    if os.getenv("TESTING") == "1":
        app.state.model = None
        app.state.threshold = None
        return

    try:
        app.state.threshold = load_threshold()
        app.state.model = download_and_load_model()
        print("[startup] model + threshold loaded OK")
    except Exception as e:
        app.state.model = None
        app.state.threshold = None
        print(f"[startup] ERROR: {e}")

# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    model = getattr(app.state, "model", None)
    threshold = getattr(app.state, "threshold", None)

    if model is None or threshold is None:
        raise HTTPException(
            status_code=503,
            detail="Model or threshold not loaded"
        )

    try:
        # Pydantic → dict → DataFrame (1 ligne)
        X = pd.DataFrame([payload.model_dump()])

        probas = model.predict_proba(X)
        proba = float(probas[0][1])  # ✅ robuste (liste ou numpy)

        prediction = int(proba >= threshold)

        return PredictionResponse(
            proba=proba,
            prediction=prediction,
            threshold=threshold,
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Prediction error: {e}"
        )