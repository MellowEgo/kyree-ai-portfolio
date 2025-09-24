from pathlib import Path
import json
import chromadb
from chromadb.utils import embedding_functions

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "policies.json"
DBDIR = ROOT / "data" / "chroma"

def main():
    with open(DATA) as f:
        policies = json.load(f)

    client = chromadb.PersistentClient(path=str(DBDIR))
    coll = client.get_or_create_collection(
        name="policies",
        embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"   # small, fast, no GPU required
        ),
    )
    # Clear & reinsert for idempotency
    try:
        coll.delete(ids=[p["id"] for p in policies])
    except Exception:
        pass

    coll.add(
        documents=[p["question"] + " " + p["answer"] for p in policies],
        metadatas=policies,
        ids=[p["id"] for p in policies],
    )
    print(f"Indexed {len(policies)} policies into {DBDIR}")

if __name__ == "__main__":
    main()
