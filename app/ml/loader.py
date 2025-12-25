import json
import joblib
from huggingface_hub import hf_hub_download

from app.core.config import settings


def load_threshold() -> float:
    with open(settings.THRESHOLD_PATH, "r", encoding="utf-8") as f:
        return float(json.load(f)["threshold"])


def load_model():
    # 1) si un chemin local est fourni et existe
    if settings.MODEL_PATH:
        return joblib.load(settings.MODEL_PATH)

    # 2) sinon on charge depuis Hugging Face Hub
    if not settings.HF_MODEL_REPO or not settings.HF_MODEL_FILENAME:
        raise RuntimeError("MODEL_PATH ou HF_MODEL_REPO + HF_MODEL_FILENAME doivent être définis.")

    local_path = hf_hub_download(
        repo_id=settings.HF_MODEL_REPO,
        filename=settings.HF_MODEL_FILENAME,
        token=settings.HF_TOKEN,
    )
    return joblib.load(local_path)