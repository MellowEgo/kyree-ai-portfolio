# kyree-ai-portfolio

![CI](https://github.com/MellowEgo/kyree-ai-portfolio/actions/workflows/ci.yaml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12%2B-informational)
![Env](https://img.shields.io/badge/env-managed%20by%20uv-6f42c1)
![License](https://img.shields.io/badge/license-MIT-green)

Real, runnable proof-of-work across **AI/ML Engineering**, **Generative AI**, and **Discovery Statistics** — aligned to my Johnson & Johnson target roles.

---

## Quickstart (uv)

```bash
uv sync
uv run pytest
uv run uvicorn --app-dir "projects/01_ai_ml_engineer_mlopspipeline/api" app:app --reload
uv run streamlit run projects/02_genai_policy_assistant/src/app_streamlit.py
