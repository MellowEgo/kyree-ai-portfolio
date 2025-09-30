# GenAI Policy Assistant (Engineer Track)

![Policy Assistant CI](https://github.com/MellowEgo/kyree-ai-portfolio/actions/workflows/policy.yml/badge.svg)

**Role match:** AI Engineer / Applied LLM Engineer – Enterprise AI

A minimal, production-style policy Q&A service: FastAPI → JSON policy store → health checks → tests → Makefiles → Docker.

*(Swagger screenshot/GIF optional — drop in `assets/` and link it here.)*

---

## Quickstart (uv)

**From repo root**
```bash
uv sync
uv run uvicorn app:app --app-dir projects/02_genai_policy_assistant/api --reload --port 8001
# http://127.0.0.1:8001/health | /docs | POST /ask
```

**From project folder**
```bash
cd projects/02_genai_policy_assistant
make setup
make serve         # reload on :8001
```

---

## Endpoints

| Method | Path       | Purpose                          |
|------:|------------|----------------------------------|
|   GET | `/`        | Service info                     |
|   GET | `/health`  | Health + policy_count            |
|  POST | `/ask`     | Simple Q&A over local policies   |

### Example

**Request**
```bash
curl -s -X POST http://127.0.0.1:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the remote work policy?"}'
```

**Response**
```json
{"answer":"Employees may work remotely up to 3 days per week."}
```

*(If no match is found, the service returns a safe fallback message.)*

---

## What’s Inside

* **Service** (`api/app.py`)  
  FastAPI app using modern **lifespan** startup to load policies from `data/policies.json`.
* **Data** (`data/policies.json`)  
  Small demo policy set (HR/IT). Easily swapped for real content or a DB.
* **Tests** (`tests/`)  
  Smoke tests using `TestClient` (runs lifespan), plus JSON sanity checks.
* **Makefiles**  
  Project-local Makefile for DX; root Makefile targets to run from repo root.
* **Dockerfile** (`Dockerfile`)  
  Build a self-contained image and run on port 8000 (mapped to host).

### Layout

```
02_genai_policy_assistant/
├─ api/
│  ├─ __init__.py
│  └─ app.py                 # FastAPI service (lifespan loads policies)
├─ data/
│  └─ policies.json          # toy policy set
├─ tests/
│  ├─ test_api.py            # health + ask
│  └─ test_policies.py       # JSON loads
├─ assets/                   # (optional) docs GIFs/screens
├─ Dockerfile
├─ Makefile                  # project-local
└─ README.md
```

---

## Makefile shortcuts

**From this project folder**
```bash
make setup          # uv sync
make serve          # uvicorn app:app --app-dir api --reload --port 8001
make serve-prod     # host 0.0.0.0 --port 8001
make json-validate  # verify data/policies.json is valid JSON
make test           # run pytest (uses TestClient with lifespan)
make check          # boot, ping /health & /ask, then stop
make docker-build   # build image "genai-policy"
make docker-run     # run container on host :8001
```

**From repo root** (if you added proxy targets in root Makefile)
```bash
make serve-policy           # runs FastAPI for this project on PORT2 (default 8001)
make test-policy            # runs this project's tests
```

---

## Run tests & CI

**Local**
```bash
# from project folder
uv run pytest tests -q
```

**GitHub Actions (snippet)** — add to your root workflow before the test step:
```yaml
- name: Policy Assistant tests
  run: |
    uv run pytest projects/02_genai_policy_assistant/tests -q
```

---

## Docker (optional)

**Build & run**
```bash
# from project folder
make docker-build
make docker-run
# then visit http://127.0.0.1:8001/docs (container exposes 8000 → host maps 8001)
```

If you prefer raw docker:
```bash
docker build -t genai-policy -f Dockerfile .
docker run --rm -p 8001:8000 genai-policy
```

---

## Notes & Design Choices

* **Local-first**: pure FastAPI + JSON → easy to clone/run for recruiters.
* **Modern startup**: FastAPI **lifespan** (no deprecated `@on_event` warnings).
* **Deterministic tests**: `TestClient` context ensures startup/shutdown runs.
* **Clear upgrade path**:
  - Swap JSON search for **embeddings + vector store** (Chroma/FAISS/pgvector).
  - Add `/version` & Prometheus `/metrics`.
  - Optional LLM integration & streaming (OpenAI/Vertex/Anthropic), with env-gated keys.
  - Authn/authz (e.g., API key or OIDC) if you want to deploy publicly.

---

## Sample Data

`data/policies.json` (edit freely):
```json
[
  {"id":"remote_work","question":"What is the remote work policy?","answer":"Employees may work remotely up to 3 days per week."},
  {"id":"vacation","question":"How much vacation time do employees get?","answer":"Full-time employees accrue 15 days of vacation annually."},
  {"id":"security","question":"What is the password policy?","answer":"Passwords must be at least 12 characters and rotated every 90 days."}
]
```

---

## Troubleshooting

* **Import error (`No module named 'api'`)**  
  Use `--app-dir api` locally (or set `PYTHONPATH=.` for tests).
* **JSON decode error on startup**  
  Ensure `data/policies.json` exists and is valid JSON (`make json-validate`).
* **Port already in use**  
  Change the port: `make serve PORT=8011` or kill the old PID.

---

## Next (nice upgrades)

* Embeddings + semantic search (Chroma with `all-MiniLM-L6-v2`)  
* `/version` & `/metrics` endpoints  
* Streamed responses + LLM integration  
* Record a 5–8s Swagger demo GIF in `assets/` and link it up top
