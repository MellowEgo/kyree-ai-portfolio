# src/eval.py
import pandas as pd
import joblib
import argparse
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import json

# -------------------------------
# Parse CLI arguments
# -------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('--in', dest='infile', default='artifacts/model.joblib', help='Path to model file')
parser.add_argument('--out', default='artifacts/metrics.json', help='Path to save metrics')
args = parser.parse_args()

# -------------------------------
# Load dataset
# -------------------------------
df = pd.read_csv('models/demo_dataset_v2.csv')

# Encode categorical features
df = pd.get_dummies(df, columns=['gender', 'ethnicity'], drop_first=True)

X = df.drop('treatment_successful', axis=1)
y = df['treatment_successful']

# Split data
_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------------------
# Load trained model
# -------------------------------
model = joblib.load(args.infile)

# Predict
y_pred = model.predict(X_test)

# -------------------------------
# Evaluate
# -------------------------------
report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
accuracy = accuracy_score(y_test, y_pred)

print("📊 Classification Report:\n")
print(classification_report(y_test, y_pred, zero_division=0))
print(f"\n✅ Accuracy: {accuracy:.2f}")

# -------------------------------
# Save metrics
# -------------------------------
os.makedirs(os.path.dirname(args.out), exist_ok=True)
with open(args.out, 'w') as f:
    json.dump(report, f, indent=2)

print(f"💾 Metrics saved to {args.out}")
