import os
from dataclasses import dataclass
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()#Charge automatiquement les variables définies dans un fichier .env


@dataclass(frozen=True)# Crée une classe de configuration immuable
class Settings:
    DATABASE_URL: str | None
    THRESHOLD_PATH: str
    MODEL_PATH: str | None
    HF_MODEL_REPO: str | None
    HF_MODEL_FILENAME: str
    HF_TOKEN: str | None
    API_KEY: str | None


@lru_cache # Cache le résultat de la fonction en mémoire
def get_settings() -> Settings:
    '''
    La fonction get_settings retourne explicitement 
    un objet de type Settings, ce qui rend la configuration claire,
      typée et plus sûre à l’échelle de l’application.
    '''
    return Settings(
        DATABASE_URL=os.getenv("DATABASE_URL"),
        THRESHOLD_PATH=os.getenv("THRESHOLD_PATH", "config/threshold.json"),
        MODEL_PATH=os.getenv("MODEL_PATH"),
        HF_MODEL_REPO=os.getenv("HF_MODEL_REPO"),
        HF_MODEL_FILENAME=os.getenv("HF_MODEL_FILENAME", "model.joblib"),
        HF_TOKEN=os.getenv("HF_TOKEN"),
        API_KEY=os.getenv("API_KEY"),
    )