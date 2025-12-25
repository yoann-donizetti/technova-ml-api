from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from app.ml.loader import load_model, load_threshold
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.predict import run_predict_manual, run_predict_by_id


app = FastAPI(title="Technova ML API", version="0.4.0")


@app.on_event("startup")
def startup():
    # ... ton code existant (load env, load model, load threshold, create engine, etc.)

    # ✅ Important : stocker l'engine dans app.state (évite les NameError en tests)
    app.state.engine = engine  # engine peut être None si DATABASE_URL absent

    print("[startup] model + threshold loaded OK")

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health():
    model_loaded = hasattr(app.state, "model") and app.state.model is not None
    threshold = getattr(app.state, "threshold", None)

    engine = getattr(app.state, "engine", None)
    db_configured = engine is not None

    return {
        "status": "ok",
        "model_loaded": model_loaded,
        "threshold": threshold,
        "db_configured": db_configured,
    }

@app.post("/predict", response_model=PredictionResponse, tags=["default"])
def predict_manual(data: PredictionRequest):
    try:
        proba, pred, _payload = run_predict_manual(
            payload=data.model_dump(),
            model=app.state.model,
            threshold=float(app.state.threshold),
        )
        return PredictionResponse(proba=float(proba), prediction=int(pred), threshold=float(app.state.threshold))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/predict/{id_employee}", response_model=PredictionResponse, tags=["default"])
def predict_by_id(id_employee: int):
    try:
        proba, pred, _payload = run_predict_by_id(
            id_employee=id_employee,
            model=app.state.model,
            threshold=float(app.state.threshold),
        )
        return PredictionResponse(proba=float(proba), prediction=int(pred), threshold=float(app.state.threshold))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))