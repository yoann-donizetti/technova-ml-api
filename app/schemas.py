from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    age: int = Field(..., ge=0)
    revenu_mensuel: int = Field(..., ge=0)
    heure_supplementaires: bool


class PredictionResponse(BaseModel):
    proba: float
    prediction: int
    threshold: float