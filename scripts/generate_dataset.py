"""
Generate the QuickFoods dataset.

Creates two CSVs:
  - exercises/ex01/starter/quickfoods_train.csv   (given to students)
  - exercises/ex01/test_data/holdout.csv          (secret - used only by grader)

Both come from the same data-generating process, so a well-trained
model will generalize. But students can't just hardcode the test set.

Features:
  distance_km       - distance from restaurant to customer
  items_count       - number of items in order
  hour_of_day       - 0-23
  is_weekend        - 0 or 1
  restaurant_rating - 1.0-5.0
  traffic_level     - 1 (low) to 3 (high)

Target:
  delivery_time_minutes
"""

import numpy as np
import pandas as pd
from pathlib import Path


def generate(n: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    distance = rng.uniform(0.5, 15, n)
    items = rng.integers(1, 10, n)
    hour = rng.integers(0, 24, n)
    is_weekend = rng.integers(0, 2, n)
    rating = rng.uniform(2.5, 5.0, n).round(1)
    traffic = rng.integers(1, 4, n)

    # Target with a clear signal + some noise
    noise = rng.normal(0, 3, n)
    delivery_time = (
        8.0
        + 2.2 * distance
        + 0.6 * items
        + 1.5 * traffic
        + (1.8 * is_weekend)
        + ((hour >= 18) & (hour <= 21)).astype(int) * 4.0  # dinner rush
        - (rating - 2.5) * 0.8
        + noise
    )
    delivery_time = np.clip(delivery_time, 5, 90).round(1)

    return pd.DataFrame({
        "distance_km": distance.round(2),
        "items_count": items,
        "hour_of_day": hour,
        "is_weekend": is_weekend,
        "restaurant_rating": rating,
        "traffic_level": traffic,
        "delivery_time_minutes": delivery_time,
    })


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent

    # Training set - students see this
    train = generate(n=2000, seed=42)
    train_path = root / "exercises" / "ex01" / "starter" / "quickfoods_train.csv"
    train_path.parent.mkdir(parents=True, exist_ok=True)
    train.to_csv(train_path, index=False)
    print(f"✓ Training set: {train_path} ({len(train)} rows)")

    # Held-out test set - only the grader sees this
    test = generate(n=500, seed=1337)
    test_path = root / "exercises" / "ex01" / "test_data" / "holdout.csv"
    test_path.parent.mkdir(parents=True, exist_ok=True)
    test.to_csv(test_path, index=False)
    print(f"✓ Held-out set: {test_path} ({len(test)} rows)")
    print("\n⚠️  IMPORTANT: Do NOT publish the held-out set to students.")
    print("   The test_data/ folder should stay in the grader repo only.")
