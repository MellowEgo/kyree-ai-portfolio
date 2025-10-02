import json, os, subprocess, sys, pathlib

PROJECT = pathlib.Path(__file__).resolve().parents[1]

def test_train_writes_metrics(tmp_path):
    # run train with temp artifacts dir
    art = tmp_path / "artifacts"
    cmd = [sys.executable, str(PROJECT / "src" / "train.py"), "--epochs", "1", "--sample", "50", "--out", str(art)]
    subprocess.check_call(cmd)

    fp = art / "metrics.json"
    assert fp.exists(), "metrics.json not found"

    m = json.loads(fp.read_text())
    assert "metrics" in m and "accuracy" in m["metrics"] and "loss" in m["metrics"]
    assert 0.0 <= m["metrics"]["accuracy"] <= 1.0
