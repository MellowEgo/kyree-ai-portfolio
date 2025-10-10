# --------------------------------------------
# Project 1 — ML Engineer / MLOps Pipeline
# Location: projects/01_ai_ml_engineer_mlopspipeline/Makefile
# --------------------------------------------

SHELL := /bin/bash
.ONESHELL:
.PHONY: help setup test train eval serve check lint clean

# Defaults (override like: make train SAMPLE=1000 EPOCHS=2 PORT=8010)
ARTIFACTS ?= artifacts
EPOCHS    ?= 1
SAMPLE    ?= 500
PORT      ?= 8010

# Use uv everywhere locally
PY := uv run python

help:
	@echo ""
	@echo "Targets:"
	@echo "  setup   : uv sync this project"
	@echo "  test    : run unit tests (pytest)"
	@echo "  train   : quick training run writing to $(ARTIFACTS)"
	@echo "  eval    : load and check $(ARTIFACTS)/metrics.json"
	@echo "  serve   : run FastAPI app on PORT=$(PORT)"
	@echo "  check   : train -> eval (CI-safe pass/fail)"
	@echo "  lint    : ruff lint + format check"
	@echo "  clean   : remove caches and artifacts"
	@echo ""

setup:
	uv sync

test:
	# run from THIS folder; 'tests' is local
	PYTHONPATH=. uv run pytest -q tests

train:
	mkdir -p $(ARTIFACTS)
	$(PY) src/train.py --epochs $(EPOCHS) --sample $(SAMPLE) --out $(ARTIFACTS)

eval:
	$(PY) src/eval.py --in $(ARTIFACTS)/metrics.json

# NEW: one-command pipeline gate (used in README and CI)
check: train eval
	@echo "✅ Pipeline passed thresholds."

# NEW: serve FastAPI with health/metrics
serve:
	$(PY) -m uvicorn api.app:app --host 0.0.0.0 --port $(PORT)

lint:
	uv pip install -q ruff || true
	uv run ruff check .
	uv run ruff format --check .

clean:
	rm -rf $(ARTIFACTS) **/__pycache__ .pytest_cache *.pyc

# Kill any uvicorn serving api.app on any port (macOS)
stop: 
	-@pkill -f "uvicorn api.app" || true
	-@lsof -ti :(PORT) | xargs -I{} kill -9 {} || true
	@echo "Stopped any uvicorn on Port=$(PORT)"

# End of Makefile