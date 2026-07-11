"""FastAPI application for serving the packaged Heart Disease model."""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, Request, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)
from pydantic import BaseModel, Field


MODEL_PATH = Path("models/heart_disease_pipeline.joblib")
METADATA_PATH = Path("models/model_metadata.json")

logger = logging.getLogger("heart_disease_api")
logging.basicConfig(level=logging.INFO)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)


class HeartDiseaseRequest(BaseModel):
    """Input schema matching the Cleveland Heart Disease feature columns."""

    age: float = Field(..., examples=[63.0])
    sex: float = Field(..., examples=[1.0])
    cp: float = Field(..., examples=[1.0])
    trestbps: float = Field(..., examples=[145.0])
    chol: float = Field(..., examples=[233.0])
    fbs: float = Field(..., examples=[1.0])
    restecg: float = Field(..., examples=[2.0])
    thalach: float = Field(..., examples=[150.0])
    exang: float = Field(..., examples=[0.0])
    oldpeak: float = Field(..., examples=[2.3])
    slope: float = Field(..., examples=[3.0])
    ca: float = Field(..., examples=[0.0])
    thal: float = Field(..., examples=[6.0])


class PredictionResponse(BaseModel):
    """Prediction response returned by the API."""

    prediction: int
    confidence: float
    risk_label: str
    model_name: str


@lru_cache(maxsize=1)
def load_model():
    """Load the packaged model once per process."""
    return joblib.load(MODEL_PATH)


@lru_cache(maxsize=1)
def load_metadata() -> dict:
    """Load model metadata for health and prediction responses."""
    if not METADATA_PATH.exists():
        return {"model_name": "unknown"}
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def request_to_frame(request: HeartDiseaseRequest) -> pd.DataFrame:
    """Convert a validated request body to a one-row DataFrame."""
    return pd.DataFrame([request.model_dump()])


app = FastAPI(
    title="Heart Disease Prediction API",
    version="1.0.0",
    description="Predicts binary heart disease risk from clinical features.",
)


@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    """Log request metadata and expose Prometheus counters/histograms."""
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    timestamp = datetime.now(timezone.utc).isoformat()

    logger.info(
        "timestamp=%s endpoint=%s method=%s status=%s latency_ms=%.2f",
        timestamp,
        request.url.path,
        request.method,
        response.status_code,
        duration * 1000,
    )

    endpoint = request.url.path
    REQUEST_COUNT.labels(
        request.method,
        endpoint,
        str(response.status_code),
    ).inc()
    REQUEST_LATENCY.labels(request.method, endpoint).observe(duration)
    return response


@app.get("/health")
def health_check() -> dict:
    """Return service and model health information."""
    metadata = load_metadata()
    return {
        "status": "ok",
        "model_loaded": MODEL_PATH.exists(),
        "model_name": metadata.get("model_name", "unknown"),
    }


@app.get("/metrics")
def metrics() -> Response:
    """Expose Prometheus metrics in text format."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.post("/predict", response_model=PredictionResponse)
def predict(request: HeartDiseaseRequest) -> PredictionResponse:
    """Predict heart disease risk and confidence for one patient record."""
    model = load_model()
    features = request_to_frame(request)
    probabilities = model.predict_proba(features)[0]
    prediction = int(model.predict(features)[0])
    confidence = float(probabilities[prediction])
    risk_label = "disease" if prediction == 1 else "no_disease"
    metadata = load_metadata()

    return PredictionResponse(
        prediction=prediction,
        confidence=round(confidence, 4),
        risk_label=risk_label,
        model_name=metadata.get("model_name", "unknown"),
    )
