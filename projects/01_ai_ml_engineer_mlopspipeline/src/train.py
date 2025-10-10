# src/train.py
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--out', default='artifacts', help='Output directory')
args = parser.parse_args()

df = pd.read_csv('models/demo_dataset.csv')

X = df.drop('treatment_successful', axis=1)
y = df['treatment_successful']
X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

os.makedirs(args.out, exist_ok=True)
joblib.dump(model, f'{args.out}/model.joblib')

print(f"✅ Model trained and saved to {args.out}/model.joblib")
