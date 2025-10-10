## 🧠 Project 01 — AI/ML Engineer MLOps Pipeline

> **Goal:** Demonstrate an end-to-end AI engineering workflow — from data simulation to training, evaluation, and serving via FastAPI.

**Tech Stack:** Python • FastAPI • Make • Uvicorn • NumPy • Pydantic  
**Key Features:**
- 🧩 CI-safe `make check` pipeline for training + evaluation  
- 📈 `/metrics` endpoint returns model accuracy/loss in JSON  
- ⚙️ `/health` endpoint confirms live model + uptime  
- 🧠 `/predict` accepts feature arrays and returns mock predictions  
- 🧾 Includes [MODEL_CARD.md](projects/01_ai_ml_engineer_mlopspipeline/MODEL_CARD.md) for governance

**Live Docs Preview:**  
![Swagger UI Screenshot](projects/01_ai_ml_engineer_mlopspipeline/assets/fastapi-docs.png)

> ✅ *Validated end-to-end on local build using `uv` and Makefile orchestration.*

**What reviewers see in 60 seconds**
- `make check` runs a deterministic **train → eval** loop and **fails** if metrics regress  
- `artifacts/metrics.json` + `artifacts/run_id.txt` prove **traceability**  
- `api/app.py` exposes **/health** and **/metrics** for **observability**  
- `tests/` includes **smoke + unit** tests for CI readiness  
- `configs/local.yaml` sets **thresholds** — no magic numbers

---

## 🧩 System Diagram

```mermaid
flowchart LR
    A[Data (Iris)] --> B[Train (scikit-learn)]
    B --> C[metrics.json + run_id.txt]
    C --> D[Eval: Threshold Check]
    D -->|pass| E[Serve (FastAPI)]
    D -->|fail| F[[Pipeline Fails with Exit 1]]
    E --> G[/health + /metrics]
    G --> H[Monitoring / CI]


![Project 1 CI](https://github.com/MellowEgo/kyree-ai-portfolio/actions/workflows/ci.yaml/badge.svg)
![Swagger UI Screenshot](projects/01_ai_ml_engineer_mlopspipeline/assets/fastapi-docs.png)
---

### Quickstart

> From **this folder** (`projects/01_ai_ml_engineer_mlopspipeline/`)

Run these commands from this folder
projects/01_ai_ml_engineer_mlopspipeline/

```bash
# 1) Install dependencies (uv) and set up local env
make setup

# 2) Run the end-to-end pipeline (train -> metrics -> threshold check)
make check

# 3) Serve health/metrics endpoints
make serve     # http://127.0.0.1:8010  (GET /health, GET /metrics)

# 4) Run tests (unit + smoke)
make test
```

Prereqs: Python 3.10+, uv (or swap uv run for your venv runner).
Artifacts: created under artifacts/ (gitignored).

### Try it quickly
```bash
# from this folder
uv run python src/train.py
uv run uvicorn --app-dir "api" app:app --reload


# in another terminal:
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[4,1]}'
```

### This project demonstrates an end-to-end ML workflow:
- Data preparation & feature engineering
- Model training & evaluation with thresholds
- FastAPI service for inference
- Automated tests & CI integration\
- Docker-ready structure for deployment

### Stack
- Python 3.12 (managed by uv)
- scikit-learn, pandas, numpy
- FastAPI + Uvicorn
- PyTest
- GitHub Actions CI
- (Optional) Docker for containerized serving

### Structure
```bash

01_ai_ml_engineer_mlopspipeline/
├─ api/
│  └─ app.py                  # FastAPI service (/health, /predict)
├─ src/
│  ├─ train.py                # writes artifacts/metrics.json
│  └─ eval.py                 # reads metrics.json and checks thresholds
├─ tests/
│  ├─ test_api.py
│  ├─ test_features.py
│  ├─ test_train.py
│  ├─ test_smoke.py
│  └─ test_metrics.py
├─ configs/
│  └─ local.yaml              # evaluation thresholds
├─ assets/
│  └─ fastapi-docs.png        # screenshot of /docs (optional)
├─ artifacts/                 # generated outputs (gitignored)
├─ Makefile
└─ README.md

```
### Make Targets
```bash
make setup    # uv sync (install deps)
make train    # generate artifacts/metrics.json
make eval     # read metrics.json and enforce thresholds
make check    # full train + eval (CI-safe)
make serve    # run FastAPI locally
make test     # pytest suite (unit + smoke)
make lint     # optional: ruff format/lint check
make clean    # remove artifacts & caches
```
🟢 Tip: If artifacts/metrics.json doesn’t exist, run make train first.
🟢 The API is optional — omit if you’re focusing on pipeline behavior.

### Example Outputs 
artifacts/metrics.json
```json
{
  "accuracy": 0.91,
  "f1_macro": 0.90,
  "latency_ms": 43.5
}
```
configs/local.yaml 
```yaml 
eval:
  thresholds:
    accuracy: 0.85
    f1_macro: 0.85
```
run_id.txt
```bash
20251009T142015-7f3a9bcd
```
### HealthCare Context 
```bash
| Principle            | Implementation                             |
| -------------------- | ------------------------------------------ |
| **Reproducibility**  | Config-driven, seeded runs                 |
| **Traceability**     | Run ID + persisted metrics artifacts       |
| **Validation Gates** | Pipeline fails if thresholds unmet         |
| **Observability**    | `/health` + `/metrics` endpoints           |
| **Governance**       | `.env.example` pattern; no secrets in repo |
| **Auditability**     | Versioned configs & deterministic outputs  |
```

### Future Enhancements
- MLflow tracking for metrics & parameters
- ONNX packaging for portable inference
- Docker build for ECS/Fargate deployment
- Prometheus/Grafana monitoring dashboard
- Bedrock/LLM summarization endpoint (no PHI)


---
```yaml
### 💡 Why this version

✅ Clean, readable, and GitHub-formatted  
✅ CI badge + diagram render correctly  
✅ Narrative tied to J&J’s environment  
✅ Keeps technical detail but avoids redundancy  
✅ Recruiter or engineer can **grasp full system in 30–60 seconds**

---

