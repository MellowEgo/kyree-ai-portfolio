.PHONY: setup test train serve index app

setup:
	uv sync

test:
	uv run pytest -q || true

# Project 1 (MLOps)
train:
	uv run python projects/01_ai_ml_engineer_mlopspipeline/src/train.py

serve:
	uv run uvicorn --app-dir "projects/01_ai_ml_engineer_mlopspipeline/api" app:app --reload

# Project 2 (GenAI)
index:
	uv run python projects/02_genai_policy_assistant/src/ingest.py

app:
	uv run streamlit run projects/02_genai_policy_assistant/src/app_streamlit.py
