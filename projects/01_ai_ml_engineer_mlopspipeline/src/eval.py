# src/eval.py
import pandas as pd
import joblib
import argparse
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import json

parser = argparse.ArgumentParser()
parser.add_argument('--in', dest='infile', default='artifacts/model.joblib', help='Path to model file')
parser.add_argument('--out', default='artifacts/metrics.json', help='Path to save metrics')
args = parser.parse_args()

df = pd.read_csv('models/demo_dataset.csv')
X = df.drop('treatment_successful', axis=1)
y = df['treatment_successful']
_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = joblib.load(args.infile)
y_pred = model.predict(X_test)

report = classification_report(y_test, y_pred, output_dict=True)
print("📊 Classification Report:\n", classification_report(y_test, y_pred))

# Save metrics
os.makedirs(os.path.dirname(args.out), exist_ok=True)
with open(args.out, 'w') as f:
    json.dump(report, f, indent=2)

print(f"✅ Metrics saved to {args.out}")
