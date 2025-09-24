from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np, os, joblib

app = FastAPI()
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "model.joblib")
model = None

@app.on_event("startup")
def load_model():
    global model
    try:
        model = joblib.load(MODEL_PATH)
    except Exception:
        model = None

class Features(BaseModel):
    features: list[float]

@app.get("/")
def root():
    return {"service":"MLOps Pipeline Demo","endpoints":["/health","/predict","/docs"]}

@app.get("/health")
def health():
    return {"status":"ok", "model_loaded": bool(model)}

@app.post("/predict")
def predict(payload: Features):
    x = np.array(payload.features, dtype=float).reshape(1, -1)
    if model is None:
        return {"prediction": float(0.5 * x.sum())}
    return {"prediction": float(model.predict(x)[0])}
