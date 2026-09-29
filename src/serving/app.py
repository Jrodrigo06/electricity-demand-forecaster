"""FastAPI app serving demand forecasts (Cloud Run)."""
from fastapi import FastAPI

app = FastAPI(title="ISO-NE Demand Forecaster")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/forecast")
def forecast():
    raise NotImplementedError
