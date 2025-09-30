# GenAI Policy Assistant (Engineer Track)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

**Role match:** AI Engineer / Applied LLM Engineer – Enterprise AI

A minimal, production-style policy Q&A service: FastAPI → JSON policy store → health checks → tests → Makefiles → Docker.

*(Optional: add a Swagger screenshot/GIF in `assets/` and link it here.)*

---

## Quickstart

**From repo root**
```bash
uv sync
uv run uvicorn app:app --app-dir projects/02_genai_policy_assistant/api --reload --port 8001
# http://127.0.0.1:8001/health | /docs | POST /ask | POST /v1/search
````

**From project folder**

```bash
cd projects/02_genai_policy_assistant
make setup
make serve         # reload on :8001
```

---

## Endpoints

| Method | Path         | Purpose                                 |
| -----: | ------------ | --------------------------------------- |
|    GET | `/`          | Service info                            |
|    GET | `/health`    | Health + policy count                   |
|   POST | `/ask`       | Simple Q&A over local policies          |
|   POST | `/v1/ask`    | Versioned Q&A (same as `/ask`)          |
|   POST | `/v1/search` | Keyword search across policies (with k) |

### Examples

**Ask**

```bash
curl -s -X POST http://127.0.0.1:8001/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the remote work policy?"}'
```

**Search**

```bash
curl -s -X POST http://127.0.0.1:8001/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query":"password"}'
```

---

## What’s Inside

* **Service** (`api/app.py`) – FastAPI app using **lifespan** startup to load `data/policies.json`.
* **Data** (`data/policies.json`) – demo policy set (HR/IT).
* **Tests** (`tests/`) – Smoke tests with `TestClient` + JSON sanity checks.
* **Makefiles** – Local developer shortcuts; root Makefile proxies.
* **Dockerfile** – Build & run container on port `8001`.

### Layout

```
02_genai_policy_assistant/
├─ api/
│  └─ app.py                 # FastAPI service
├─ data/
│  └─ policies.json          # toy policy set
├─ tests/
│  ├─ test_api.py            # health + ask
│  └─ test_policies.py       # JSON sanity
├─ Dockerfile
├─ Makefile
└─ README.md
```

---

## Makefile shortcuts

**From this project folder**

```bash
make setup          # uv sync
make serve          # dev server on :8001
make serve-prod     # production mode, host 0.0.0.0:8001
make json-validate  # verify data/policies.json is valid JSON
make test           # run pytest
make check          # boot, ping /health & /ask, then stop
make docker-build   # build image "genai-policy"
make docker-run     # run container on host :8001
```

**From repo root**

```bash
make serve-policy
make test-policy
```

---

## Run tests & CI

**Local**

```bash
uv run pytest projects/02_genai_policy_assistant/tests -q
```

**GitHub Actions (example)** – save as `.github/workflows/policy-assistant.yml`:

```yaml
name: Policy Assistant CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - name: Install deps
        run: uv sync
      - name: Run tests
        run: uv run pytest projects/02_genai_policy_assistant/tests -q
```

---

## Docker

**Build & run**

```bash
make docker-build
make docker-run
# http://127.0.0.1:8001/docs
```

Raw docker:

```bash
docker build -t genai-policy -f Dockerfile .
docker run --rm -p 8001:8000 genai-policy
```

---

## Sample Data

`data/policies.json`:

```json
[
  {"id":"remote_work","question":"What is the remote work policy?","answer":"Employees may work remotely up to 3 days per week."},
  {"id":"vacation","question":"How much vacation time do employees get?","answer":"Full-time employees accrue 15 days of vacation annually."},
  {"id":"security","question":"What is the password policy?","answer":"Passwords must be at least 12 characters and rotated every 90 days."}
]
```

---

## Troubleshooting

* **Import error (`No module named 'api'`)** → use `--app-dir api`.
* **JSON decode error** → validate with `make json-validate`.
* **Port already in use** → run on another port: `make serve PORT=8012`.
