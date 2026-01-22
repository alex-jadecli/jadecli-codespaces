#!/usr/bin/env zsh
# Sync script for jadecli-codespaces
# Pulls latest, handles conflicts, pushes changes

set -euo pipefail

REPO_DIR="${1:-$(pwd)}"
cd "$REPO_DIR"

echo "=== jadecli-codespaces sync ==="

# Check for uncommitted changes
if [[ -n $(git status --porcelain) ]]; then
    echo "Uncommitted changes detected. Committing..."
    git add -A
    git commit -m "context: auto-sync $(date +%Y-%m-%dT%H:%M:%S)"
fi

# Pull with rebase
echo "Pulling latest..."
if ! git pull --rebase; then
    echo "ERROR: Merge conflict detected"
    echo "Resolve conflicts manually, then run: git rebase --continue"
    exit 1
fi

# Push changes
echo "Pushing..."
git push

echo "=== Sync complete ==="
