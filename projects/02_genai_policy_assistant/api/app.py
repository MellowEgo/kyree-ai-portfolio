# projects/02_genai_policy_assistant/api/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from contextlib import asynccontextmanager
from json import JSONDecodeError
import json
import re

TITLE = "GenAI Policy Assistant"
VERSION = "0.1.2"

POLICY_PATH = Path(__file__).resolve().parents[1] / "data" / "policies.json"

class AskRequest(BaseModel):
    question: str

class SearchRequest(BaseModel):
    query: str
    k: int = 25  # max results

def _record_to_text(rec: dict) -> str:
    """Support either {question, answer} or {title, text} shapes."""
    return " ".join([
        str(rec.get("title", "")),
        str(rec.get("text", "")),
        str(rec.get("question", "")),
        str(rec.get("answer", "")),
    ])

def _snippet(s: str, n: int = 240) -> str:
    return (s[:n] + "…") if len(s) > n else s

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    try:
        print(f"[startup] Loading policies from: {POLICY_PATH.resolve()}")
        text = POLICY_PATH.read_text(encoding="utf-8")
        app.state.policies = json.loads(text) if text.strip() else []
    except FileNotFoundError:
        print("[startup] policies.json not found; continuing with empty list.")
        app.state.policies = []
    except JSONDecodeError as e:
        print(f"[startup] policies.json invalid JSON: {e}; continuing with empty list.")
        app.state.policies = []
    yield
    # --- shutdown ---
    # nothing to clean up

app = FastAPI(title=TITLE, version=VERSION, lifespan=lifespan)

# Provide a safe default so unit tests that import `app` without running lifespan won't crash
if not hasattr(app.state, "policies"):
    app.state.policies = []

@app.get("/")
def root():
    return {"service": TITLE, "endpoints": ["/health", "/ask", "/v1/ask", "/v1/search"]}

@app.get("/health")
def health():
    return {"ok": True, "policy_count": len(app.state.policies)}

# ----- ASK (unversioned + versioned alias) -----
@app.post("/ask")
@app.post("/v1/ask")
def ask(req: AskRequest):
    q = req.question.lower().strip()
    if not q:
        raise HTTPException(400, "question is required")

    q_terms = {t for t in re.findall(r"\w+", q) if len(t) > 2}
    scored = []
    for p in app.state.policies:
        text = _record_to_text(p)
        terms = {t.lower() for t in re.findall(r"\w+", text)}
        score = len(q_terms & terms)
        if score:
            scored.append((score, p, text))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = [
        {
            "id": p.get("id"),
            "title": p.get("title") or p.get("question"),
            "excerpt": _snippet(text, 420),
            "score": score
        }
        for score, p, text in scored[:3]
    ]

    if not top:
        return {"answer": "I couldn’t find a specific policy for that. Please rephrase or check the policy list.", "contexts": []}

    # Stubbed answer; replace with LLM call later.
    return {"question": req.question, "draft_answer": "Here are the most relevant policy excerpts.", "contexts": top}

# ----- SEARCH (versioned) -----
@app.post("/v1/search")
def search(req: SearchRequest):
    q = req.query.strip()
    if not q:
        raise HTTPException(400, "query must not be empty")

    pattern = re.compile(re.escape(q), re.IGNORECASE)
    hits = []
    for p in app.state.policies:
        text = _record_to_text(p)
        if pattern.search(text):
            hits.append({
                "id": p.get("id"),
                "title": p.get("title") or p.get("question"),
                "snippet": _snippet(text, 240),
            })
            if len(hits) >= max(1, min(req.k, 100)):
                break

    return {"query": q, "count": len(hits), "results": hits}
