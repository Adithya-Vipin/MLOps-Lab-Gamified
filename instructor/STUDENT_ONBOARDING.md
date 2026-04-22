# 🎮 Welcome to MLOps Quest

> Your onboarding guide. Takes about 10 minutes. Do this once, then you're in the game.

---

## 🎯 What you're doing here

You're going to ship real MLOps code. Every exercise you complete = XP. Every push gets auto-graded by a bot. Your progress is **live on the leaderboard projected in class**. Speed matters. Quality matters more.

This isn't theory. You'll leave this course with:
- A public GitHub portfolio of 10 working MLOps projects
- Hands-on experience with MLflow, Docker, FastAPI, CI/CD
- The ability to talk about production ML in an interview

---

## 🪪 Prerequisites

- A **free GitHub account** — create one at https://github.com/signup if you don't have one yet
- **Git installed** on your laptop
- **Python 3.10+** installed
- About 10 GB free disk space (for Docker later)

---

## 🚀 Step-by-step setup

### Step 1: Fork the class repo

Go to the instructor's repo (URL is on the whiteboard) and click **Fork** in the top right. This creates your own copy under your GitHub account.

### Step 2: Clone your fork

```bash
# Replace urmsandeep with your actual GitHub username
git clone https://github.com/urmsandeep/MLOps-Lab-Gamified.git
cd MLOps-Lab-Gamified
```

### Step 3: Add yourself to the roster

Open `students.yml` and add your GitHub username to the list:

```yaml
students:
  - urmsandeep
  - urmsandeep   # ← add this line
```

Commit and push:

```bash
git add students.yml
git commit -m "Register for MLOps Quest"
git push
```

### Step 4: Open a Pull Request

Go to your fork on GitHub. You'll see a banner saying "This branch is 1 commit ahead." Click **Contribute → Open pull request**.

Title: `Register: urmsandeep`
Body: `Signing up for the quest.`

Submit the PR. The instructor will merge it.

Once merged, the grader bot will start tracking your fork.

### Step 5: Configure MLflow tracking (needed from Exercise 2 onwards)

Get the MLflow ngrok URL from the classroom screen. Set it as an environment variable:

```bash
export MLFLOW_TRACKING_URI="https://xxxx-xx-xx-xxx-xxx.ngrok-free.app"
```

Add this to your shell profile (`~/.bashrc` or `~/.zshrc`) if you want it to persist.

### Step 6: Start Exercise 1

```bash
cd exercises/ex01
cat README.md       # read the brief
cd starter
pip install -r requirements.txt
python train.py     # runs the baseline
```

---

## 🔄 The submission loop

This is what you'll do for every exercise:

```bash
# 1. Work on the exercise in your fork
#    (edit code, train models, build APIs, whatever the exercise asks)

# 2. Commit and push when ready
git add .
git commit -m "Ex01: baseline model"
git push

# 3. Wait ~2 minutes for the grader bot

# 4. Check the leaderboard
#    If your row turned green for that exercise → you earned XP
#    If not → click the exercise cell to see the failure message, fix, repush
```

---

## 🏆 Maximizing your XP

| Tactic | XP |
|---|---|
| Push working code fast (first to pass) | +5 XP (First Blood) |
| Be second or third to pass | +3 / +2 XP |
| Pass on your first push (no failed attempts) | +2 XP (Flawless) |
| Complete 3 exercises consecutively in one class | +5 XP (Streak) |
| Beat the Drift Boss when it spawns | +20 XP |
| Crush the Final Boss | +25 XP |

**Honest strategy:** getting Flawless on Ex01 is the easiest bonus — the starter code works out of the box. Read it, think about it, push once. That's +2 XP for ~15 minutes of work.

---

## ❓ Common issues

| Issue | Fix |
|---|---|
| "My commit pushed but my row didn't light up" | Wait up to 2 min. Check the Actions tab on the instructor's repo to see grader status. |
| "My fork is behind the class repo" | Click **Sync fork** on your fork's GitHub page. |
| "I got a merge conflict on students.yml" | Sync fork first, resolve the conflict, push again. |
| "MLflow says connection refused" | The ngrok URL probably changed (instructor's laptop restarted). Get the new URL from the screen. |
| "CI keeps failing but works on my laptop" | Python version mismatch or missing `requirements.txt` entry. The grader uses Python 3.11. |

---

## 🚫 What not to do

- **Don't** try to read the grader's test data. It lives only in the instructor's repo, not in your fork.
- **Don't** modify files outside `exercises/` and `students.yml`. Your changes won't be used by the grader anyway.
- **Don't** commit `__pycache__`, virtual environments, or large datasets. Use `.gitignore`.
- **Don't** copy a friend's model.pkl and submit it as your own. If you want to collaborate, pair program — both of you push to your own forks.

---

## 🎲 You're ready

Now go earn some XP. First Blood on Ex01 is up for grabs.

> The best MLOps engineers I know got that way by shipping. Repeatedly. Imperfectly. Publicly.
> This is your low-stakes dojo for exactly that.

🎮 **GAME ON.**
