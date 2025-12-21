from fastapi import FastAPI

app = FastAPI(title="Technova ML API")

@app.get("/health")
def health():
    return {"status": "ok"}