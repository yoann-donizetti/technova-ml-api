# app/core/config.py
import os
from dataclasses import dataclass
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str | None
    THRESHOLD_PATH: str
    MODEL_PATH: str | None
    HF_MODEL_REPO: str | None
    HF_MODEL_FILENAME: str
    HF_TOKEN: str | None
    API_KEY: str | None


@lru_cache
def get_settings() -> Settings:
    return Settings(
        DATABASE_URL=os.getenv("DATABASE_URL"),
        THRESHOLD_PATH=os.getenv("THRESHOLD_PATH", "config/threshold.json"),
        MODEL_PATH=os.getenv("MODEL_PATH"),
        HF_MODEL_REPO=os.getenv("HF_MODEL_REPO"),
        HF_MODEL_FILENAME=os.getenv("HF_MODEL_FILENAME", "model.joblib"),
        HF_TOKEN=os.getenv("HF_TOKEN"),
        API_KEY=os.getenv("API_KEY"),
    )