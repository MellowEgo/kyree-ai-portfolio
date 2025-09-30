# -------------------------------
# GenAI Policy Assistant Makefile
# Location: projects/02_genai_policy_assistant/Makefile
# -------------------------------

SHELL := /bin/bash
.ONESHELL:
.PHONY: help setup serve serve-prod test check json-validate docker-build docker-run clean

PORT ?= 8001

help:
	@echo ""
	@echo "Targets:"
	@echo "  setup           uv sync in this project"
	@echo "  serve           run FastAPI (reload) on PORT=$(PORT)"
	@echo "  serve-prod      run FastAPI (no reload) on PORT=$(PORT)"
	@echo "  test            run pytest"
	@echo "  json-validate   verify data/policies.json is valid JSON"
	@echo "  check           boot API, ping /health and /ask, then stop"
	@echo "  docker-build    build Docker image: genai-policy"
	@echo "  docker-run      run Docker image on PORT=$(PORT)"
	@echo "  clean           remove caches"
	@echo ""

setup:
	uv sync

serve:
	uv run uvicorn app:app --app-dir api --reload --port $(PORT)

serve-prod:
	uv run uvicorn app:app --app-dir api --host 0.0.0.0 --port $(PORT)

test:
	PYTHONPATH=. uv run pytest -q tests

json-validate:
	uv run python -m json.tool data/policies.json >/dev/null && echo "policies.json OK"

# Boots the API in the background, waits for readiness, hits /health and /ask, then stops it
check:
	@echo "• JSON validity"; uv run python -m json.tool data/policies.json >/dev/null && echo "OK"
	@echo "• Boot & ping"
	@uv run uvicorn app:app --app-dir api --host 127.0.0.1 --port $(PORT) & \
	PID=$$!; \
	for i in $$(seq 1 20); do \
	  curl -sf http://127.0.0.1:$(PORT)/health >/dev/null && break; \
	  sleep 0.5; \
	done; \
	curl -s http://127.0.0.1:$(PORT)/health | tee /dev/tty | grep -q '"ok": true'; \
	curl -s -X POST http://127.0.0.1:$(PORT)/ask \
	  -H "Content-Type: application/json" \
	  -d '{"question":"remote work policy"}' \
	  | tee /dev/tty | grep -Eq '"draft_answer"|"answer"'; \
	kill $$PID; \
	wait $$PID 2>/dev/null || true; \
	echo ""; echo "✅ Policy API looks good."

docker-build:
	docker build -t genai-policy -f Dockerfile .

docker-run:
	docker run --rm -p $(PORT):8000 genai-policy

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
