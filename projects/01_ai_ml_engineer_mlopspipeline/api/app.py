# api/app.py
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, FileResponse
from pydantic import BaseModel
import numpy as np, os, joblib, json, time

app = FastAPI(title="MLOps Pipeline Demo", version="1.0")

# --- Model + artifacts paths ---
ROOT_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(ROOT_DIR, "..", "models", "model.joblib")
METRICS_PATH = os.path.join(ROOT_DIR, "..", "artifacts", "metrics.json")

model = None


# --- Startup hook: load model if available ---
@app.on_event("startup")
def load_model():
    global model
    try:
        model = joblib.load(MODEL_PATH)
    except Exception:
        model = None


# --- Pydantic input schema ---
class Features(BaseModel):
    features: list[float]


# --- Root route ---
@app.get("/")
def root():
    return {
        "service": "MLOps Pipeline Demo",
        "endpoints": ["/health", "/metrics", "/predict", "/docs"],
    }


# --- Health check ---
@app.get("/health")
def health():
    return {
        "status": "ok",
        "ts": int(time.time()),
        "model_loaded": bool(model),
    }


# --- New: Prometheus-style metrics endpoint ---
@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    """Expose metrics in Prometheus-style text format."""
    if not os.path.exists(METRICS_PATH):
        return PlainTextResponse("# No metrics available yet", status_code=404)
    with open(METRICS_PATH, "r") as f:
        data = json.load(f)
    acc = data["metrics"].get("accuracy", 0)
    loss = data["metrics"].get("loss", 0)
    return PlainTextResponse(f"accuracy {acc}\nloss {loss}\n", media_type="text/plain")


# --- Prediction route ---
@app.post("/predict")
def predict(payload: Features):
    x = np.array(payload.features, dtype=float).reshape(1, -1)
    if model:
        y_pred = model.predict(x)[0]
    else:
        # fallback simple heuristic if no model file is found
        y_pred = 0.5 * x.sum()
    return {"prediction": float(y_pred)}


# --- New: serve favicon to avoid 404 in browser ---
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    icon_path = os.path.join(ROOT_DIR, "..", "assets", "favicon.ico")
    if os.path.exists(icon_path):
        return FileResponse(icon_path)
    return {"detail": "No favicon found"}
