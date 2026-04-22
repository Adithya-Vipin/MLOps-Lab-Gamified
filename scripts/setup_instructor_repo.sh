#!/usr/bin/env bash
# ================================================================
# MLOps Quest - Instructor Setup Helper
# ================================================================
# Pushes this scaffold to a new GitHub repo under your account.
#
# Prerequisites:
#   - You've created an empty PUBLIC repo on GitHub
#   - You have `git` installed and authenticated (gh CLI or SSH key)
#
# Usage:
#   bash scripts/setup_instructor_repo.sh <your-github-username> <repo-name>
#
# Example:
#   bash scripts/setup_instructor_repo.sh urmsandeep MLOps-Lab-Gamified
# ================================================================

set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <github-username> <repo-name>"
  exit 1
fi

USER="$1"
REPO="$2"

echo "🎮 Setting up MLOps Quest repo at github.com/$USER/$REPO"

# Ensure we're in the repo root
cd "$(dirname "$0")/.."

# Replace the placeholder username in docs and configs
echo "→ Personalizing files with your username..."
# README
sed -i.bak "s|YOUR_USERNAME|$USER|g" README.md && rm README.md.bak
# Also update any docs references
find instructor -type f -name "*.md" -exec sed -i.bak "s|YOUR_USERNAME|$USER|g" {} \; -exec rm {}.bak \;

# Initialize git if not already
if [ ! -d .git ]; then
  git init -b main
fi

# Stage and commit
git add .
if git diff --staged --quiet; then
  echo "→ No changes to commit."
else
  git commit -m "🎮 Initial MLOps Quest setup"
fi

# Add remote
if ! git remote | grep -q origin; then
  git remote add origin "https://github.com/$USER/$REPO.git"
else
  git remote set-url origin "https://github.com/$USER/$REPO.git"
fi

# Push
echo "→ Pushing to github.com/$USER/$REPO..."
git push -u origin main

echo ""
echo "✅ Done! Next steps:"
echo ""
echo "   1. Go to https://github.com/$USER/$REPO/settings/pages"
echo "      → Source: Deploy from a branch"
echo "      → Branch: main, folder: /docs"
echo ""
echo "   2. Go to https://github.com/$USER/$REPO/settings/actions"
echo "      → Workflow permissions: Read and write"
echo ""
echo "   3. Your leaderboard will be live at:"
echo "      https://$USER.github.io/$REPO/"
echo ""
echo "   4. Read instructor/RUNBOOK.md for class-day instructions."
