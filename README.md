# 🎮 MLOps Quest — Gamified Lab Manual

> Learn MLOps by shipping code, earning XP, and climbing the leaderboard.

This is the **gamified companion** to the [MLOps Lab Manual](https://github.com/urmsandeep/MLOps-Lab-Manual). Same 10 exercises, same curriculum — but every exercise is auto-graded, every pass awards XP, and everyone's progress is live on a projected leaderboard during class.

---

## 🎯 How the game works

1. **Fork this repo** to your own GitHub account.
2. **Register yourself** by adding your GitHub username to `students.yml` via Pull Request.
3. **Complete each exercise** in your fork.
4. **Push your code** — a grader bot runs every 2 minutes and tests your submission.
5. **Earn XP** for every exercise you pass. Speed bonuses for being first. Streak bonuses for consistency. Boss battles for glory.
6. **Watch the leaderboard** — projected live during class.

---

## 🏆 Scoring at a glance

| Action | XP |
|---|---|
| Pass an exercise | 10–30 XP (by difficulty) |
| First to pass (First Blood) | +5 XP |
| Second / Third to pass | +3 / +2 XP |
| Pass on first push (Flawless) | +2 XP |
| 3 exercises in a row (Streak) | +5 XP |
| Drift Boss challenge | +20 XP |
| Production Meltdown (Final Boss) | +25 XP |

**Max possible: ~270 XP.** Full rules in [`points.yml`](./points.yml).

---

## 📚 Exercise lineup

| # | Exercise | XP | Stage |
|---|---|---|---|
| 01 | 🎯 Baseline Model | 10 | Training |
| 02 | 📊 Experiment Tracking | 10 | Evaluation |
| 03 | ⚖️ Multi-Metric Selection | 15 | Evaluation |
| 04 | 📦 Docker Packaging | 20 | Deployment |
| 05 | 🎛️ Hyperparameter Tuning | 20 | Training |
| 06 | 🚀 FastAPI Serving | 20 | Deployment |
| 07 | 👁️ Logging & Monitoring | 15 | Monitoring |
| 08 | 🏷️ Model Versioning | 15 | Versioning |
| 09 | 🔁 Retraining Pipeline | 20 | Retraining |
| 10 | 🏆 End-to-End Pipeline | 30 | Full Lifecycle |

---

## 🚀 Quick start for students

See [`instructor/STUDENT_ONBOARDING.md`](./instructor/STUDENT_ONBOARDING.md) for the full walkthrough.

```bash
# 1. Fork this repo on GitHub (click the Fork button)

# 2. Clone your fork
git clone https://github.com/urmsandeep/MLOps-Lab-Gamified.git
cd MLOps-Lab-Gamified

# 3. Add yourself to students.yml, then:
git add students.yml
git commit -m "Register for MLOps Quest"
git push

# 4. Open a PR from your fork to the instructor's main repo

# 5. Start Exercise 1
cd exercises/ex01
cat README.md
```

---

## 🧑‍🏫 For instructors

See [`instructor/RUNBOOK.md`](./instructor/RUNBOOK.md) — the one-page class-day guide.

---

## 📺 Live leaderboard

**[→ View the leaderboard](https://urmsandeep.github.io/MLOps-Lab-Gamified/)**

*(Replace `urmsandeep` with the instructor's GitHub username once GitHub Pages is enabled.)*
