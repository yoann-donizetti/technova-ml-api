import json
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException

from app.schemas import PredictionRequest, PredictionResponse

app = FastAPI(title="Technova ML API")

THRESHOLD_PATH = Path("config/threshold.json")


def load_threshold() -> float:
    with open(THRESHOLD_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return float(data["threshold"])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    try:
        threshold = load_threshold()

        # Pydantic -> dict -> DataFrame (1 ligne)
        X = pd.DataFrame([payload.model_dump()])
        _ = X  # on branchera le modèle plus tard

        # POC: proba fixe
        proba = 0.30
        prediction = int(proba >= threshold)

        return PredictionResponse(proba=proba, prediction=prediction, threshold=threshold)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
from fastapi.responses import RedirectResponse

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")