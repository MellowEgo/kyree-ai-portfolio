# GenAI Policy Assistant (Engineer Track)

**Role match:** AI Engineer / Applied LLM Engineer – Enterprise AI

A minimal GenAI-powered service: serve policies → simple Q&A → health checks → tests → CI.  
Screenshot of live docs:

![FastAPI /docs](assets/fastapi-docs.png)

---

### Quickstart (uv)

```bash
# from repo root (or this folder)
uv sync
uv run uvicorn --app-dir "api" app:app --reload
# http://127.0.0.1:8001/health | /docs | POST /ask
```

### Endpoints 

| Method | Path      | Purpose                                 |
| -----: | --------- | --------------------------------------- |
|    GET | `/`       | Service info                            |
|    GET | `/health` | Health + policy count                   |
|   POST | `/ask`    | Query assistant → returns policy answer |

### Example 

Resquest 

```bash
curl -X POST http://127.0.0.1:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the remote work policy?"}'
```
Respond 

```bash
{
  "answer": "Employees may work remotely up to 3 days per week."
}
```
(If no match is found, the assistant responds with a safe fallback message.)

### What’s Inside

- Policies (data/policies.json)
Minimal demo set of HR/IT/Academic policies.

- Service (api/app.py)
Loads policies on startup; exposes /health and /ask.

- Tests (tests/)
Smoke tests for policy load and Q&A endpoint.

- Notebook (notebooks/00_exploration.ipynb)
Placeholder for experimenting with embeddings/vector search.

### Layout 
```pgsql
02_genai_policy_assistant/
├─ api/
│  └─ app.py              # FastAPI service
├─ data/
│  └─ policies.json       # toy policy set
├─ tests/
│  ├─ test_api.py
│  └─ test_policies.py
├─ notebooks/
│  └─ 00_exploration.ipynb
├─ assets/
│  └─ fastapi-docs.png
├─ Dockerfile
├─ Makefile
└─ README.md
```

### Makefile shortcuts 

```bash
# from repo root
make serve-policy   # uv run uvicorn --app-dir "projects/02_.../api" app:app --reload
make test-policy    # uv run pytest projects/02_.../tests -q
```

### Run test & CI 

```bash
uv run pytest -q
```
The repo root GitHub Actions workflow also installs deps and runs these tests.

### Dockerfile 
```DockeFile 
# projects/02_genai_policy_assistant/Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir fastapi uvicorn pydantic
EXPOSE 8000
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```





