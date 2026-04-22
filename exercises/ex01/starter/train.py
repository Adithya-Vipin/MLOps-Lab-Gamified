"""
Exercise 1 — Baseline Model for QuickFoods delivery time prediction.

This is the starter. Modify it. Make it yours. Ship a working model.
"""

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np


def main() -> None:
    # 1. Load the training data
    df = pd.read_csv("quickfoods_train.csv")
    print(f"Loaded {len(df)} training rows")
    print(df.head())

    # 2. Split features and target
    y = df["delivery_time_minutes"]
    X = df.drop(columns=["delivery_time_minutes"])

    # 3. Local train/validation split (good practice - helps you estimate your grader score)
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 4. Train a baseline model
    # TODO: Try different models here! LinearRegression, DecisionTreeRegressor, RandomForestRegressor, etc.
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 5. Check your local validation RMSE
    val_preds = model.predict(X_val)
    rmse = float(np.sqrt(mean_squared_error(y_val, val_preds)))
    print(f"\nLocal validation RMSE: {rmse:.2f}")
    print(f"Grader threshold: 15.0 (you need to be below this on held-out data)")

    # 6. Save the model artifact where the grader expects it
    output_path = "../model.pkl"
    joblib.dump(model, output_path)
    print(f"\n✓ Model saved to exercises/ex01/model.pkl")
    print("Now: git add, commit, push, and watch the leaderboard.")


if __name__ == "__main__":
    main()
