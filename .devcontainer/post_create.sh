#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "============================================="
echo "  Setting up ACU CSE 101 Environment..."
echo "============================================="

# Install with the same interpreter used by the editor. Fail visibly on errors.
bash "$ROOT/scripts/check_environment.sh" --packages

# Configure safe git defaults for students
git config --global pull.rebase false
git config --global core.autocrlf input
if ! git config user.name >/dev/null 2>&1; then
    git config --global user.name "CSE 101 Student"
    git config --global user.email "student@cse101.acibadam.edu.tr"
fi

# Set execution permissions on scripts
chmod +x scripts/*.py 2>/dev/null || true

# Ensure upstream course remote is set
if ! git remote get-url upstream >/dev/null 2>&1; then
    git remote add upstream "https://github.com/Krr0ptioN/acu-cse-101-pract-ce.git" 2>/dev/null || true
fi

# Ensure student starts on the 'workspace' branch, keeping 'main' pristine
if git show-ref --verify --quiet refs/heads/workspace; then
    git checkout workspace
else
    git checkout -b workspace
fi

# Run non-blocking initial sync to pull any newly published course material
python3 "$ROOT/scripts/sync_course.py" 2>/dev/null || true

echo "✅ Course packages and workspace ready. Editor extensions will be checked when VS Code connects."

