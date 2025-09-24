# projects/02_genai_policy_assistant/api/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from contextlib import asynccontextmanager
from json import JSONDecodeError
import json

TITLE = "GenAI Policy Assistant"
VERSION = "0.1.1"

POLICY_PATH = Path(__file__).resolve().parents[1] / "data" / "policies.json"

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

class AskRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"service": TITLE, "endpoints": ["/health", "/ask"]}

@app.get("/health")
def health():
    return {"ok": True, "policy_count": len(app.state.policies)}

@app.post("/ask")
def ask(req: AskRequest):
    q = req.question.lower().strip()
    if not q:
        raise HTTPException(400, "question is required")
    for p in app.state.policies:
        text = f"{p.get('question','')} {p.get('answer','')}".lower()
        if any(tok in text for tok in q.split()):
            return {"answer": p.get("answer", "No answer found.")}
    return {"answer": "I couldn’t find a specific policy for that. Please rephrase or check the policy list."}
