# app/ml/loader.py
import json
import os
import joblib
from huggingface_hub import hf_hub_download

from app.core.config import get_settings


def load_threshold() -> float:
    settings = get_settings()
    threshold_path = settings.THRESHOLD_PATH

    if not os.path.exists(threshold_path):
        raise FileNotFoundError(f"Threshold file not found: {threshold_path}")

    with open(threshold_path, "r", encoding="utf-8") as f:
        return float(json.load(f)["threshold"])


def load_model():
    """
    Charge le modèle.
    - Sur HF Spaces: on utilise HF_MODEL_REPO + HF_MODEL_FILENAME
    - En local: on peut utiliser MODEL_PATH si tu l'as (optionnel)
    """
    settings = get_settings()

    # 1) modèle local si présent
    if settings.MODEL_PATH:
        if not os.path.exists(settings.MODEL_PATH):
            raise FileNotFoundError(f"Local model not found: {settings.MODEL_PATH}")
        return joblib.load(settings.MODEL_PATH)

    # 2) sinon HF
    if not settings.HF_MODEL_REPO or not settings.HF_MODEL_FILENAME:
        raise RuntimeError("HF_MODEL_REPO and/or HF_MODEL_FILENAME not set")

    model_path = hf_hub_download(
        repo_id=settings.HF_MODEL_REPO,
        filename=settings.HF_MODEL_FILENAME,
        token=settings.HF_TOKEN,  # ok même si None
    )
    return joblib.load(model_path)


def load_artifacts():
    model = load_model()
    threshold = load_threshold()
    return model, threshold