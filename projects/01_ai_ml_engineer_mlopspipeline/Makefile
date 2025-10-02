# --------------------------------------------
# Project 1 — ML Engineer / MLOps Pipeline
# Location: projects/01_ai_ml_engineer_mlopspipeline/Makefile
# --------------------------------------------

SHELL := /bin/bash
.ONESHELL:
.PHONY: help setup test train eval lint clean

# Defaults (override like: make train SAMPLE=1000 EPOCHS=2)
ARTIFACTS ?= artifacts
EPOCHS    ?= 1
SAMPLE    ?= 500

# Use uv everywhere locally
PY := uv run python

help:
	@echo ""
	@echo "Targets:"
	@echo "  setup   : uv sync this project"
	@echo "  test    : run unit tests (pytest)"
	@echo "  train   : quick training run writing to $(ARTIFACTS)"
	@echo "  eval    : load and check $(ARTIFACTS)/metrics.json"
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

lint:
	uv pip install -q ruff || true
	uv run ruff check .
	uv run ruff format --check .

clean:
	rm -rf $(ARTIFACTS) **/__pycache__ .pytest_cache *.pyc
