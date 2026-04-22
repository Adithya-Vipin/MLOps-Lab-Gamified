#!/usr/bin/env python3
"""
Exercise 1 Grader: Baseline Model
==================================
Tests whether the student has produced a working baseline model.

Pass criteria:
  1. A file exists at exercises/ex01/model.pkl (or model.joblib)
  2. The model loads without error
  3. When evaluated on our held-out test set, it produces valid predictions
  4. RMSE on the held-out set is below a reasonable threshold

This design prevents cheating: students never see our test data.
They must actually train a model that generalizes.

Usage:
    python ex01_grader.py <path_to_student_fork>

Exit code 0 = pass. Exit code 1 = fail.
On pass, prints a JSON line with metrics.
On fail, prints the reason to stderr.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

# Threshold: the student's model must beat this RMSE on our held-out data.
# Set conservatively - any reasonable baseline (linear regression, small tree) passes.
# Tune based on your QuickFoods dataset characteristics.
RMSE_THRESHOLD = 15.0


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(1)


def find_model_file(fork_path: Path) -> Path | None:
    """Look for model.pkl or model.joblib in the expected location."""
    candidates = [
        fork_path / "exercises" / "ex01" / "model.pkl",
        fork_path / "exercises" / "ex01" / "model.joblib",
        fork_path / "exercises" / "ex01" / "starter" / "model.pkl",
        fork_path / "exercises" / "ex01" / "starter" / "model.joblib",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def load_test_data(grader_dir: Path) -> tuple[pd.DataFrame, pd.Series]:
    """Load our held-out test set (lives in the grader repo, not the student's fork)."""
    test_csv = grader_dir / "exercises" / "ex01" / "test_data" / "holdout.csv"
    if not test_csv.exists():
        fail(f"Held-out test data missing: {test_csv}")
    df = pd.read_csv(test_csv)
    if "delivery_time_minutes" not in df.columns:
        fail("Test data schema mismatch: no 'delivery_time_minutes' column")
    y = df["delivery_time_minutes"]
    X = df.drop(columns=["delivery_time_minutes"])
    return X, y


def main() -> None:
    if len(sys.argv) < 2:
        fail("Usage: ex01_grader.py <path_to_student_fork>")

    fork_path = Path(sys.argv[1]).resolve()
    grader_dir = Path(__file__).resolve().parent.parent

    # 1. Find the model file
    model_path = find_model_file(fork_path)
    if model_path is None:
        fail("No model.pkl or model.joblib found in exercises/ex01/")

    # 2. Load the model
    try:
        import joblib
        model = joblib.load(model_path)
    except Exception as e:
        fail(f"Failed to load model: {type(e).__name__}: {e}")

    # 3. Check it has a predict method
    if not hasattr(model, "predict"):
        fail("Loaded object has no .predict() method - is this actually a model?")

    # 4. Load our held-out test set
    X_test, y_test = load_test_data(grader_dir)

    # 5. Run predictions
    try:
        preds = model.predict(X_test)
    except Exception as e:
        fail(f"Model.predict() failed: {type(e).__name__}: {e}")

    # 6. Validate predictions
    preds = np.asarray(preds).ravel()
    if preds.shape[0] != len(y_test):
        fail(f"Prediction count mismatch: got {preds.shape[0]}, expected {len(y_test)}")
    if not np.all(np.isfinite(preds)):
        fail("Predictions contain NaN or inf - model is broken")

    # 7. Compute metrics
    rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
    r2 = float(r2_score(y_test, preds))

    # 8. Apply threshold
    if rmse > RMSE_THRESHOLD:
        fail(f"Model quality too low: RMSE={rmse:.2f} (threshold: {RMSE_THRESHOLD}). Keep training!")

    # 9. Pass!
    result = {
        "message": f"Model trained. RMSE={rmse:.2f}, R²={r2:.3f}",
        "metrics": {"rmse": round(rmse, 2), "r2": round(r2, 3)},
    }
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
