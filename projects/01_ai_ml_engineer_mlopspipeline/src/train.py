# stub training script
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib, os

def main():
    # synthetic data
    X = pd.DataFrame({'a':[1,2,3,4], 'b':[0,1,0,1]})
    y = X['a'] * 0.5 + X['b'] * 0.2
    model = LinearRegression().fit(X, y)
    os.makedirs("projects/01_ai_ml_engineer_mlopspipeline/models", exist_ok=True)
    joblib.dump(model, "projects/01_ai_ml_engineer_mlopspipeline/models/model.joblib")
    print("Model trained and saved.")

if __name__ == "__main__":
    main()