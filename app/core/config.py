import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    # DB
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

    # Threshold
    THRESHOLD_PATH: str = os.getenv("THRESHOLD_PATH", "config/threshold.json")

    # Model local (optionnel)
    MODEL_PATH: str | None = os.getenv("MODEL_PATH")

    # HF model (recommandé sur HF Spaces)
    HF_MODEL_REPO: str | None = os.getenv("HF_MODEL_REPO")
    HF_MODEL_FILENAME: str | None = os.getenv("HF_MODEL_FILENAME", "model.joblib")
    HF_TOKEN: str | None = os.getenv("HF_TOKEN")  # optionnel


settings = Settings()