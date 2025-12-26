# app/core/config.py
import os
from dataclasses import dataclass
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

    THRESHOLD_PATH: str = os.getenv("THRESHOLD_PATH", "config/threshold.json")

    MODEL_PATH: str | None = os.getenv("MODEL_PATH")

    HF_MODEL_REPO: str | None = os.getenv("HF_MODEL_REPO")
    HF_MODEL_FILENAME: str | None = os.getenv("HF_MODEL_FILENAME", "model.joblib")
    HF_TOKEN: str | None = os.getenv("HF_TOKEN")

    API_KEY: str | None = os.getenv("API_KEY")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()