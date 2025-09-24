import json
from pathlib import Path

def test_policies_json_loads():
    path = Path(__file__).resolve().parents[1] / "data" / "policies.json"
    assert path.exists()
    data = json.loads(path.read_text())
    assert isinstance(data, list)
    assert all("answer" in p for p in data)
