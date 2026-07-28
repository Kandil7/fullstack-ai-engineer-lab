#!/bin/bash
# Exercise 1: Git Basics Practice Script

set -euo pipefail

echo "=== Git Basics Exercise ==="

# Create a temporary directory for practice
PRACTICE_DIR="/tmp/git-practice-$$"
mkdir -p "$PRACTICE_DIR"
cd "$PRACTICE_DIR"

echo "Working in: $PRACTICE_DIR"

# Initialize repo
echo "1. Initializing repository..."
git init
git config user.name "Practice User"
git config user.email "practice@example.com"

# Create initial files
echo "2. Creating initial files..."
cat > README.md << 'EOF'
# Practice Repository

This is a practice repository for learning Git.
EOF

cat > main.go << 'EOF'
package main

import "fmt"

func main() {
    fmt.Println("Hello, Git!")
}
EOF

# First commit
echo "3. Making first commit..."
git add .
git commit -m "Initial commit: add README and main.go"

# View log
echo "4. Viewing commit history..."
git log --oneline

# Make changes
echo "5. Making changes..."
echo "// New feature" >> main.go
echo "func NewFeature() {}" >> main.go

# Check status
echo "6. Checking status..."
git status

# Stage and commit
echo "7. Staging and committing changes..."
git add main.go
git commit -m "feat: add NewFeature function"

# View log again
echo "8. Updated history..."
git log --oneline

# Show diff
echo "9. Showing diff of last commit..."
git show HEAD

echo ""
echo "=== Exercise Complete ==="
echo "Practice directory: $PRACTICE_DIR"
echo "You can now experiment with:"
echo "  git checkout -b feature-branch"
echo "  git merge feature-branch"
echo "  git rebase main"
echo "  git stash"
echo ""
echo "Clean up with: rm -rf $PRACTICE_DIR"