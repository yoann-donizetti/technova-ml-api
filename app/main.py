# app/main.py
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse

from app.security.auth import require_api_key
from app.ml.loader import load_model, load_threshold
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.predict import run_predict_manual, run_predict_by_id
from app.db.engine import get_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
#mode test
    if os.getenv("APP_ENV") == "test":
        class DummyModel:
            def predict_proba(self, X):
                return [[0.2, 0.8]]

        app.state.model = DummyModel()
        app.state.threshold = 0.292
        app.state.engine = None
        yield
        return

    # mode normal
    app.state.model = load_model()
    app.state.threshold = float(load_threshold())
    app.state.engine = get_engine()
    print("[startup] model + threshold loaded OK")
    yield


app = FastAPI(title="Technova ML API", version="0.4.0", lifespan=lifespan)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health():
    model_loaded = getattr(app.state, "model", None) is not None
    threshold = getattr(app.state, "threshold", None)
    engine = getattr(app.state, "engine", None)
    return {
        "status": "ok",
        "model_loaded": model_loaded,
        "threshold": threshold,
        "db_configured": engine is not None,
    }


@app.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["default"],
    dependencies=[Depends(require_api_key)],
)
def predict_manual(data: PredictionRequest):
    try:
        proba, pred, _payload = run_predict_manual(
            payload=data.model_dump(),
            model=app.state.model,
            threshold=float(app.state.threshold),
            engine=getattr(app.state, "engine", None),
        )
        return PredictionResponse(proba=float(proba), prediction=int(pred), threshold=float(app.state.threshold))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/predict/{id_employee}",
    response_model=PredictionResponse,
    tags=["default"],
    dependencies=[Depends(require_api_key)],
)
def predict_by_id(id_employee: int):
    try:
        proba, pred, _payload = run_predict_by_id(
            id_employee=id_employee,
            model=app.state.model,
            threshold=float(app.state.threshold),
            engine=getattr(app.state, "engine", None),
        )
        return PredictionResponse(proba=float(proba), prediction=int(pred), threshold=float(app.state.threshold))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))