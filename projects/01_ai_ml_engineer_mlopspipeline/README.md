# MLOps Pipeline (Engineer Track)

**Role match:** Senior AI/ML Engineer – Business Technology

A tiny, production-style ML pipeline: data prep → train → evaluate, with tests, Makefile, and CI. Optional FastAPI app for inference.

![Project 1 CI](https://github.com/MellowEgo/kyree-ai-portfolio/actions/workflows/ci.yaml/badge.svg)

---

## Quickstart

> From **this folder** (`projects/01_ai_ml_engineer_mlopspipeline/`)

```bash
uv sync
make test        # run unit tests
make train       # writes artifacts/metrics.json
make eval        # reads metrics.json and enforces a small quality gate

## API Preview
![FastAPI /docs](assets/fastapi-docs.png)

### Try it quickly
```bash
# from this folder
uv run python src/train.py
uv run uvicorn --app-dir "api" app:app --reload
```

# in another terminal:
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[4,1]}'

**Role match:** Senior AI/ML Engineer – Business Technology

This project demonstrates an end-to-end ML workflow:
- data cleaning & feature engineering
- model training & evaluation
- FastAPI service for inference
- Docker packaging and CI tests

## Quickstart
```bash
make train
make serve  # runs uvicorn
```
### Stack

-Python 3.12 (managed by uv)

- scikit-learn, pandas, numpy

- FastAPI + Uvicorn

- PyTest

- GitHub Actions CI

### Structure
```bash

01_ai_ml_engineer_mlopspipeline/
├─ api/
│  └─ app.py                  # (optional) FastAPI service (/health, /predict)
├─ src/
│  ├─ train.py                # writes artifacts/metrics.json
│  └─ eval.py                 # reads metrics.json and checks thresholds
├─ tests/
│  ├─ test_api.py
│  ├─ test_features.py
│  ├─ test_train.py
│  ├─ test_smoke.py
│  └─ test_metrics.py
├─ assets/
│  └─ fastapi-docs.png        # screenshot of /docs (optional)
├─ artifacts/                 # generated outputs (gitignored)
├─ Makefile
└─ README.md
```
### Make Targets
```bash
make setup    # uv sync
make test     # run pytest (from this folder)
make train    # generate artifacts/metrics.json
make eval     # read artifacts/metrics.json and assert threshold
make lint     # ruff lint/format check (if installed)
make clean    # remove artifacts and caches
```
### Notes 
- If artifacts/metrics.json doesn’t exist, run make train first.
-The API is optional—omit it if you’re showcasing pipeline work only.
-You can override defaults without editing the Makefile: