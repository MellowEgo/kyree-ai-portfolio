#!/usr/bin/env python
import argparse, json, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", required=True)
    args = ap.parse_args()

    with open(args.infile) as f:
        metrics = json.load(f)

    acc = metrics["metrics"]["accuracy"]
    print(f"Loaded metrics: accuracy={acc}, loss={metrics['metrics']['loss']}")
    # Simple gate: require accuracy >= 0.6
    if acc < 0.6:
        print("Accuracy below threshold", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
