# src/train.py

import pandas as pd
import joblib
import os
import argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score

parser = argparse.ArgumentParser()
parser.add_argument('--out', default='artifacts', help='Output directory')
args = parser.parse_args()

# Load dataset
df = pd.read_csv('models/demo_dataset_v2.csv')
df = pd.get_dummies(df, columns=['gender', 'ethnicity'], drop_first=True)

X = df.drop('treatment_successful', axis=1)
y = df['treatment_successful']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Grid search with cross-validation
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [None, 5, 10],
    'min_samples_split': [2, 5]
}

model = RandomForestClassifier(random_state=42)
grid = GridSearchCV(model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid.fit(X_train, y_train)

best_model = grid.best_estimator_
y_pred = best_model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

# Save best model
os.makedirs(args.out, exist_ok=True)
joblib.dump(best_model, f'{args.out}/model.joblib')

# Output
print("✅ Model trained with GridSearchCV")
print(f"🔍 Best Params: {grid.best_params_}")
print(f"📊 Accuracy on test set: {acc:.2f}")
print(f"💾 Saved to {args.out}/model.joblib")
