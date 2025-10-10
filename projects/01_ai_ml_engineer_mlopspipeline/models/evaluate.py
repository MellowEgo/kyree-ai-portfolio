import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os

# Load dataset from absolute path
file_path = os.path.join(os.path.dirname(__file__), 'demo_dataset.csv')
df = pd.read_csv(file_path)

X = df.drop('treatment_successful', axis=1)
y = df['treatment_successful']

# Match training split
_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'model.joblib')
model = joblib.load(model_path)

# Predict and evaluate
y_pred = model.predict(X_test)
print("📊 Validation Report:\n")
print(classification_report(y_test, y_pred))
