#!/bin/bash
# Exercise 2: Branching and Merging Practice

set -euo pipefail

echo "=== Branching & Merging Exercise ==="

PRACTICE_DIR="/tmp/git-branching-$$"
mkdir -p "$PRACTICE_DIR"
cd "$PRACTICE_DIR"

git init
git config user.name "Practice User"
git config user.email "practice@example.com"

# Initial commit
echo "Initial content" > file.txt
git add file.txt
git commit -m "Initial commit"

# Create feature branch
echo "Creating feature branch..."
git checkout -b feature/new-feature

# Work on feature
echo "Feature work" >> file.txt
git commit -am "feat: add feature work"

# More work
echo "More feature work" >> file.txt
git commit -am "feat: more feature work"

# Switch back to main
echo "Switching to main..."
git checkout main

# Create another branch (simulating parallel work)
git checkout -b feature/other-work
echo "Other work" >> file.txt
git commit -am "feat: add other work"

# Now try to merge both into main
echo "Merging first feature..."
git checkout main
git merge feature/new-feature

echo "Merging second feature (will conflict)..."
git merge feature/other-work || true

echo "Conflict status:"
git status

echo ""
echo "Resolve conflict in file.txt, then:"
echo "  git add file.txt"
echo "  git commit -m 'Merge: resolve conflict'"
echo ""
echo "Practice directory: $PRACTICE_DIR"