#!/usr/bin/env python
import argparse, json, os, time, random

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--sample", type=int, default=500)
    ap.add_argument("--out", type=str, default="artifacts")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    # Fake a quick "train"
    time.sleep(0.2)
    metrics = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "params": {"epochs": args.epochs, "sample": args.sample},
        "metrics": {
            "accuracy": round(0.7 + random.random() * 0.3, 4),
            "loss": round(0.5 * random.random(), 4)
        }
    }

    out_fp = os.path.join(args.out, "metrics.json")
    with open(out_fp, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"Wrote {out_fp}")

if __name__ == "__main__":
    main()
