"""
MLOps Quest - Grader Orchestrator
==================================
Runs every 2 minutes via GitHub Actions cron.

For each student in students.yml:
  1. Clone (or update) their fork into /tmp/forks/<username>/
  2. Run every exercise grader against their code
  3. Compute XP earned (including bonuses)
  4. Update docs/scores.json and docs/history.json

Output files are then committed by the workflow and rendered by the
leaderboard page at docs/index.html.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# ----------------------------------------------------------------------
# Paths and config
# ----------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
FORKS_DIR = Path("/tmp/mlops_quest_forks")
SCORES_FILE = REPO_ROOT / "docs" / "scores.json"
HISTORY_FILE = REPO_ROOT / "docs" / "history.json"
STUDENTS_FILE = REPO_ROOT / "students.yml"
POINTS_FILE = REPO_ROOT / "points.yml"
GRADERS_DIR = REPO_ROOT / "graders"

# Max parallel student grading jobs. Tune based on student count.
MAX_WORKERS = 10


# ----------------------------------------------------------------------
# Load configs
# ----------------------------------------------------------------------
def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def load_history() -> dict:
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return {"passes": {}, "attempts": {}}


# ----------------------------------------------------------------------
# Per-student: clone and grade
# ----------------------------------------------------------------------
def sync_fork(username: str, repo_name: str) -> Path | None:
    """Clone or pull the student's fork. Return path to clone, or None on failure."""
    target = FORKS_DIR / username
    url = f"https://github.com/{username}/{repo_name}.git"

    try:
        if target.exists():
            # Update existing clone
            subprocess.run(
                ["git", "-C", str(target), "fetch", "origin"],
                check=True, capture_output=True, timeout=60,
            )
            subprocess.run(
                ["git", "-C", str(target), "reset", "--hard", "origin/main"],
                check=True, capture_output=True, timeout=30,
            )
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["git", "clone", "--depth", "1", url, str(target)],
                check=True, capture_output=True, timeout=120,
            )
        return target
    except subprocess.CalledProcessError as e:
        # Fork might not exist yet, or have no main branch - that's fine
        print(f"  ⚠️  {username}: could not sync fork ({e.stderr.decode()[:100] if e.stderr else 'no stderr'})")
        return None
    except subprocess.TimeoutExpired:
        print(f"  ⏱️  {username}: clone/fetch timed out")
        return None


def run_grader(exercise_id: str, fork_path: Path) -> dict:
    """
    Run the grader for a single exercise against a student's fork.
    Returns: {"passed": bool, "message": str, "details": {...}}
    """
    grader_script = GRADERS_DIR / f"{exercise_id}_grader.py"
    if not grader_script.exists():
        return {"passed": False, "message": f"No grader for {exercise_id} yet"}

    try:
        result = subprocess.run(
            [sys.executable, str(grader_script), str(fork_path)],
            capture_output=True, timeout=90, text=True,
        )
        if result.returncode == 0:
            # Grader prints a JSON blob on success
            try:
                payload = json.loads(result.stdout.strip().split("\n")[-1])
                return {"passed": True, **payload}
            except (json.JSONDecodeError, IndexError):
                return {"passed": True, "message": "Passed (no details)"}
        else:
            # Grader prints failure reason on stderr
            return {"passed": False, "message": (result.stderr or result.stdout).strip()[:200]}
    except subprocess.TimeoutExpired:
        return {"passed": False, "message": "Grader timed out"}
    except Exception as e:
        return {"passed": False, "message": f"Grader crashed: {e}"}


def grade_student(username: str, repo_name: str, exercises: dict, history: dict) -> dict:
    """
    Grade one student across all exercises.
    Returns a dict with their full score breakdown.
    """
    print(f"🎯 Grading {username}...")
    fork_path = sync_fork(username, repo_name)
    if fork_path is None:
        return {
            "username": username,
            "total_xp": 0,
            "exercises": {},
            "status": "no_fork",
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }

    results = {}
    for ex_id in exercises:
        result = run_grader(ex_id, fork_path)
        results[ex_id] = result

    return {
        "username": username,
        "exercises": results,
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "status": "ok",
    }


# ----------------------------------------------------------------------
# XP computation (base + bonuses)
# ----------------------------------------------------------------------
def compute_xp(
    all_results: list[dict],
    points_config: dict,
    history: dict,
) -> list[dict]:
    """
    Take raw pass/fail results and compute XP including:
      - base points per exercise
      - first blood / podium bonuses (based on pass order)
      - flawless bonus (no prior failed attempts)
    Mutates history.
    """
    ex_config = points_config["exercises"]
    bonus_config = points_config["bonuses"]
    now_iso = datetime.now(timezone.utc).isoformat()

    # Track who has passed each exercise and in what order
    passes = history.setdefault("passes", {})  # {ex_id: [{"user": ..., "ts": ...}]}
    attempts = history.setdefault("attempts", {})  # {(user, ex_id): count}

    for student_result in all_results:
        user = student_result["username"]
        total_xp = 0
        breakdown = []

        for ex_id, ex_result in student_result.get("exercises", {}).items():
            ex_meta = ex_config.get(ex_id, {})
            base = ex_meta.get("base", 0)
            name = ex_meta.get("name", ex_id)
            emoji = ex_meta.get("emoji", "•")

            # Track attempt count
            key = f"{user}|{ex_id}"
            if not ex_result.get("passed"):
                attempts[key] = attempts.get(key, 0) + 1
                breakdown.append({
                    "exercise": ex_id, "name": name, "emoji": emoji,
                    "passed": False, "xp": 0,
                    "message": ex_result.get("message", "Not passed"),
                })
                continue

            # Passed! Compute XP.
            ex_passes = passes.setdefault(ex_id, [])
            already_passed = any(p["user"] == user for p in ex_passes)

            xp = base
            bonus_notes = []

            if not already_passed:
                ex_passes.append({"user": user, "ts": now_iso})

                # First blood / podium bonuses based on pass order
                pass_rank = len([p for p in ex_passes if p["user"] != user or p["ts"] == now_iso])
                if pass_rank == 1:
                    xp += bonus_config["first_blood"]
                    bonus_notes.append(f"🩸 First Blood +{bonus_config['first_blood']}")
                elif pass_rank == 2:
                    xp += bonus_config["podium_2nd"]
                    bonus_notes.append(f"🥈 Second +{bonus_config['podium_2nd']}")
                elif pass_rank == 3:
                    xp += bonus_config["podium_3rd"]
                    bonus_notes.append(f"🥉 Third +{bonus_config['podium_3rd']}")

                # Flawless bonus: passed without any prior failed attempts
                if attempts.get(key, 0) == 0:
                    xp += bonus_config["flawless"]
                    bonus_notes.append(f"✨ Flawless +{bonus_config['flawless']}")

            breakdown.append({
                "exercise": ex_id, "name": name, "emoji": emoji,
                "passed": True, "xp": xp, "bonuses": bonus_notes,
                "message": ex_result.get("message", "Passed"),
            })
            total_xp += xp

        student_result["total_xp"] = total_xp
        student_result["breakdown"] = breakdown

    # Sort by XP descending, then by name for tiebreaker
    all_results.sort(key=lambda r: (-r.get("total_xp", 0), r["username"].lower()))
    for rank, r in enumerate(all_results, start=1):
        r["rank"] = rank
    return all_results


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main() -> None:
    print("=" * 60)
    print("🎮 MLOps Quest - Grader Run")
    print(f"   Started at {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    # Load config
    students_config = load_yaml(STUDENTS_FILE)
    points_config = load_yaml(POINTS_FILE)
    history = load_history()

    students = students_config.get("students", []) or []
    exercises = points_config.get("exercises", {})
    repo_name = os.environ.get("GITHUB_REPOSITORY", "urmsandeep/MLOps-Lab-Gamified").split("/")[-1]

    print(f"📋 {len(students)} students × {len(exercises)} exercises = {len(students) * len(exercises)} grader runs")
    print()

    # Grade in parallel
    all_results: list[dict] = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {
            pool.submit(grade_student, user, repo_name, exercises, history): user
            for user in students
        }
        for fut in as_completed(futures):
            user = futures[fut]
            try:
                all_results.append(fut.result())
            except Exception:
                print(f"  ❌ {user}: grader crashed")
                traceback.print_exc()
                all_results.append({
                    "username": user, "total_xp": 0, "exercises": {},
                    "status": "crashed",
                })

    # Compute XP with bonuses
    all_results = compute_xp(all_results, points_config, history)

    # Build final scores.json for leaderboard
    scores_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "points_config": points_config,
        "leaderboard": all_results,
    }
    SCORES_FILE.parent.mkdir(exist_ok=True)
    with open(SCORES_FILE, "w") as f:
        json.dump(scores_payload, f, indent=2)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    # Summary
    print()
    print("=" * 60)
    print(f"✅ Graded {len(all_results)} students")
    print(f"🏆 Top 3:")
    for r in all_results[:3]:
        print(f"   #{r['rank']} {r['username']}: {r['total_xp']} XP")
    print("=" * 60)


if __name__ == "__main__":
    main()
