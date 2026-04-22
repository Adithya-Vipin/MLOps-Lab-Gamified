# 🧑‍🏫 Instructor Runbook

> The 1-page class-day guide. Read this once before Session 1, then glance at it each session.

---

## 🗓️ One-time setup (do this once, before Session 1)

### 1. Create the gamified repo
```bash
# On GitHub, create a new PUBLIC repo named: MLOps-Lab-Gamified
# Then on your laptop:
cd ~/
git clone https://github.com/urmsandeep/MLOps-Lab-Gamified.git
cd MLOps-Lab-Gamified
# Copy in all files from this scaffold, then:
git add .
git commit -m "Initial MLOps Quest setup"
git push
```

### 2. Enable GitHub Pages
- Go to **Settings → Pages**
- Source: **Deploy from a branch**
- Branch: **`main`**, folder: **`/docs`**
- Save. Within a minute, your leaderboard is live at:
  **`https://urmsandeep.github.io/MLOps-Lab-Gamified/`**

### 3. Enable GitHub Actions
- Go to **Settings → Actions → General**
- Workflow permissions: **Read and write permissions** (so the bot can commit score updates)
- Save.
- Go to **Actions** tab, find "🎮 Grade Student Submissions", click **Enable workflow** if needed.

### 4. Test with yourself
- Add your own GitHub username to `students.yml` and push.
- Fork the repo (yes, fork your own repo to a different account, or use a colleague's).
- Submit an Ex01 model from the fork.
- Wait ~2 min. Leaderboard should update. If not — see Troubleshooting.

### 5. Install MLflow + ngrok on your laptop
```bash
pip install mlflow
# Download ngrok from https://ngrok.com/download
# Create free account, get auth token, run once:
ngrok config add-authtoken YOUR_TOKEN
```

---

## 🎬 At the start of each class (5 minutes)

### 1. Start MLflow
```bash
# In terminal 1
mlflow server --host 0.0.0.0 --port 5000
```

### 2. Expose it via ngrok
```bash
# In terminal 2
ngrok http 5000
# Copy the https://xxxx.ngrok-free.app URL
```

### 3. Project two tabs on the screen
- **Tab 1**: Leaderboard — `https://urmsandeep.github.io/MLOps-Lab-Gamified/`
- **Tab 2**: MLflow UI — the ngrok URL

### 4. Write these three URLs on the whiteboard
1. **Grader repo** (for new students to fork): `https://github.com/urmsandeep/MLOps-Lab-Gamified`
2. **Leaderboard**: `https://urmsandeep.github.io/MLOps-Lab-Gamified/`
3. **MLflow tracking**: the ngrok URL

### 5. Announce rules for the session
- "Points are live. Your row lights up green when CI passes."
- "First Blood bonuses — first to pass each exercise gets +5 XP."
- "Flawless bonus — pass on your first push, get +2 XP."
- Optional: "Today's stretch goal: reach the top 10 by end of session."

---

## 🕹️ During class

**What you do:**
- Walk around. Help students who are stuck (not with the solution — with git, CI failures, MLflow config).
- Glance at the leaderboard every 10 min. When someone gets First Blood on an exercise, announce it. Social reinforcement drives the game.
- Watch for stuck students — a row that hasn't turned green in 30 min is your cue to go sit with them.

**What you don't do:**
- Don't manually grade. The bot does it.
- Don't feed answers. Let them struggle productively. The game's dopamine comes from figuring it out.
- Don't worry if your MLflow server restarts — students just re-run with the new ngrok URL.

**The Drift Boss (mid-course surprise):**
Around Session 7 or 8, after students have built their monitoring, push a new data file to the class repo with obviously drifted distributions. First 3 teams whose monitoring catches it AND whose retraining restores accuracy get **+20 XP each**. Announce it dramatically. It's the most memorable moment of the course.

---

## 🎁 Boss battles — how to unlock

Boss battles are manually triggered. They live in `points.yml` but aren't auto-graded:
1. When you want to launch one, open an issue on the class repo titled "🐉 BOSS: Drift Awakens"
2. Commit the drifted dataset to the repo
3. Teams submit their solutions as PRs
4. You manually award XP via a PR to `docs/bonus_awards.json` (create this file, format: `{"username": ["drift_boss"]}`) — *or* just update it directly in the workflow next cycle.

---

## 🔧 Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| Leaderboard shows "No operators online" | `students.yml` has no entries, or grader hasn't run | Wait 2 min, check Actions tab for errors |
| Student's row stuck at 0 XP | Their fork isn't named `MLOps-Lab-Gamified`, or has no `main` branch | Ask them to rename or push to main |
| Grader fails with "git clone timed out" | GitHub API throttling with 50+ students | Increase `MAX_WORKERS` to 15 in `graders/run_all.py`; or cron every 3 min instead of 2 |
| MLflow connection refused | ngrok URL changed after laptop sleep | Restart ngrok, share the new URL on the board |
| Score commit fails with "permission denied" | Actions not given write permission | Settings → Actions → Workflow permissions → Read and write |

---

## 📊 After each session

```bash
git pull   # fetch the latest scores committed by the bot
```

Take a screenshot of the final leaderboard. Post it in the class chat. Call out the top 3 by name. Call out the biggest climbers of the session. This is retention fuel for next week.

---

**Remember: the game is a social contract, not a grading system.** You're not here to judge — you're here to referee. Keep it fast, fair, and a little bit chaotic.
