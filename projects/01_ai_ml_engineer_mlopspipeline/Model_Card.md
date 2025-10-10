# 🧾 Model Card — MLOps Pipeline Demo

**Model Type:** Logistic Regression (Demo Stub)  
**Domain:** Synthetic tabular data (simulated features for reproducibility)  
**Purpose:** Demonstrate an end-to-end MLOps workflow with CI-safe training, evaluation, and serving via FastAPI.

---

## ⚙️ System Overview

| Stage | Script | Description |
|--------|---------|-------------|
| **Training** | `src/train.py` | Generates synthetic metrics and outputs `artifacts/metrics.json`. |
| **Evaluation** | `src/eval.py` | Loads metrics, checks performance thresholds, and validates pipeline success. |
| **Serving** | `api/app.py` | FastAPI service exposing `/health`, `/metrics`, and `/predict` endpoints. |

---

## 📊 Key Metrics

| Metric | Value | Threshold | Result |
|---------|--------|------------|--------|
| Accuracy | ~0.79 | ≥ 0.60 | ✅ Pass |
| Loss | ~0.36 | ≤ 0.50 | ✅ Pass |

Stored in: `artifacts/metrics.json`

---

## 🧠 Responsible AI & Reproducibility

- ✅ **No real-world data used** (all synthetic)  
- ✅ **Deterministic workflow:** random seeds + Makefile gates  
- ✅ **Governance:** `make check` enforces accuracy ≥ 0.6  
- ✅ **Environment:** pinned via `uv` lock file for reproducibility  
- ✅ **Deployable:** FastAPI service supports `/health` and `/metrics` for observability  

---

## 🧱 Versioning & Change Log

| Version | Change Summary | Date |
|----------|----------------|------|
| 1.0.0 | Initial demo MLOps pipeline + FastAPI endpoints | 2025-10-09 |
| 1.0.1 | Added `/metrics` route + favicon handler | 2025-10-09 |
| 1.1.0 | Added governance docs + model card | 2025-10-10 |

---

📦 **Repository:** `kyree-ai-portfolio/projects/01_ai_ml_engineer_mlopspipeline`  
🧰 **Tech Stack:** Python, FastAPI, NumPy, Pydantic, Make, Uvicorn  
🔗 **Docs:** [http://127.0.0.1:8010/docs](http://127.0.0.1:8010/docs)
