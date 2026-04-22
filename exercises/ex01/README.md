# 🎯 Exercise 01 — Baseline Model

> **Quest:** Train the first model for QuickFoods delivery time prediction and ship the artifact.
> **XP:** 10 (base) + up to 9 bonus XP
> **MLOps Stage:** Raw Data → Training

---

## 🎬 The story

QuickFoods, a food delivery startup, wants to predict how long each order will take. Their CTO just walked into your cubicle and said:

> "Ship me a baseline. Anything. I just need a number to point at in the Monday review. Don't over-engineer it — we're going to iterate."

Your job: train a simple regression model on the training data, save it as `model.pkl`, and push.

---

## 🎯 Win condition

The grader checks that:

1. A file exists at `exercises/ex01/model.pkl`
2. It loads successfully with `joblib.load()`
3. It has a working `.predict()` method
4. Predictions on our **secret held-out set** produce a **RMSE below 15 minutes**

You will **not** see the held-out set. No hardcoding the answer. Your model has to actually generalize.

---

## 🛠️ Getting started

```bash
cd exercises/ex01/starter
pip install -r requirements.txt
python train.py
```

The starter `train.py` gives you a working skeleton. You're expected to modify it — try different models (linear regression, decision tree, random forest), different feature engineering, anything that passes the threshold.

---

## 📤 How to submit

```bash
# From repo root
git add exercises/ex01/model.pkl
git commit -m "Ex01: baseline model"
git push
```

The grader runs every 2 minutes. Check the live leaderboard — your row will light up green when it passes.

---

## 🏆 Bonus XP available

| Bonus | When | XP |
|---|---|---|
| 🩸 First Blood | First student to pass Ex01 | +5 |
| 🥈 Podium 2nd | Second to pass | +3 |
| 🥉 Podium 3rd | Third to pass | +2 |
| ✨ Flawless | Pass on your very first push (no failed attempts before) | +2 |

---

## 💡 Hints (if you're stuck)

- Start with `sklearn.linear_model.LinearRegression`. That alone usually passes.
- The data has 6 features. All numeric. No missing values. Straightforward.
- If RMSE is too high, try `RandomForestRegressor` or engineer an `is_dinner_rush` feature (hour between 18-21).
- Save your model with `joblib.dump(model, "model.pkl")`.

---

## 🚫 Don't

- Don't commit `quickfoods_train.csv` changes.
- Don't try to look up the held-out set — it's not in any student fork.
- Don't hardcode predictions. The grader feeds in features and checks outputs.

---

**Good luck. Ship fast.** 🚀
