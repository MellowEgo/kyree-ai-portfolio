# -------------------------------
# Repo Makefile (root-level)
# -------------------------------

.PHONY: help setup test \
	train serve serve-prod \
	serve-policy test-policy build-policy-index \
	index app \
	docker-mlops-build docker-mlops-run \
	docker-policy-build docker-policy-run \
	clean

# -------- Variables --------
P1_DIR := projects/01_ai_ml_engineer_mlopspipeline
P2_DIR := projects/02_genai_policy_assistant

P1_API := $(P1_DIR)/api
P2_API := $(P2_DIR)/api
P2_SCRIPTS := $(P2_DIR)/scripts

# Default ports (override with `make serve PORT1=9000`, etc.)
PORT1 ?= 8000
PORT2 ?= 8001

# -------- Help --------
help:
	@echo ""
	@echo "Targets:"
	@echo "  setup                 uv sync for the repo"
	@echo "  test                  run all tests (root)"
	@echo ""
	@echo "  train                 (P1) train and persist model"
	@echo "  serve                 (P1) run FastAPI (dev, reload) on PORT1=$(PORT1)"
	@echo "  serve-prod            (P1) run FastAPI (no reload) on PORT1=$(PORT1)"
	@echo ""
	@echo "  serve-policy          (P2) run FastAPI (dev, reload) on PORT2=$(PORT2)"
	@echo "  test-policy           (P2) run only policy-assistant tests"
	@echo "  build-policy-index    (P2) build embeddings index (scripts/index_policies.py)"
	@echo "  index                 (P2) run your existing src/ingest.py pipeline"
	@echo "  app                   (P2) run your existing Streamlit UI"
	@echo ""
	@echo "  docker-mlops-build    (P1) build Docker image"
	@echo "  docker-mlops-run      (P1) run Docker container (maps PORT1)"
	@echo "  docker-policy-build   (P2) build Docker image"
	@echo "  docker-policy-run     (P2) run Docker container (maps PORT2)"
	@echo ""
	@echo "  clean                 remove Python caches, build artifacts"
	@echo ""

# -------- Global setup/test --------
setup:
	uv sync

test:
	uv run pytest -q || true

# -------- Project 1 (MLOps) --------
train:
	uv run python $(P1_DIR)/src/train.py

serve:
	uv run uvicorn --app-dir "$(P1_API)" app:app --reload --port $(PORT1)

serve-prod:
	uv run uvicorn --app-dir "$(P1_API)" app:app --host 0.0.0.0 --port $(PORT1)

# -------- Project 2 (GenAI Policy Assistant) --------
# New recruiter-ready shortcuts (FastAPI-based)
serve-policy:
	uv run uvicorn app:app --reload --port $(PORT2) --app-dir "$(P2_DIR)/api"

test-policy:
	uv run pytest $(P2_DIR)/tests -q

build-policy-index:
	uv run python $(P2_SCRIPTS)/index_policies.py

# Your existing targets (Streamlit + ingest under src/)
index:
	uv run python $(P2_DIR)/src/ingest.py

app:
	uv run streamlit run $(P2_DIR)/src/app_streamlit.py

# -------- Docker (Project 1 & 2) --------
docker-mlops-build:
	docker build -t mlops-demo \
		-f $(P1_DIR)/Dockerfile \
		$(P1_DIR)

docker-mlops-run:
	docker run --rm -p $(PORT1):8000 mlops-demo

docker-policy-build:
	docker build -t genai-policy \
		-f $(P2_DIR)/Dockerfile \
		$(P2_DIR)

docker-policy-run:
	docker run --rm -p $(PORT2):8000 genai-policy

# -------- Clean --------
clean:
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
