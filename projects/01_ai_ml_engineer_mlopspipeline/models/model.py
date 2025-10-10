import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

# Load dataset from absolute path
file_path = os.path.join(os.path.dirname(__file__), 'demo_dataset.csv')
df = pd.read_csv(file_path)

X = df.drop('treatment_successful', axis=1)
y = df['treatment_successful']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
model_output_path = os.path.join(os.path.dirname(__file__), 'model.joblib')
joblib.dump(model, model_output_path)

print("✅ Model trained and saved to:", model_output_path)
