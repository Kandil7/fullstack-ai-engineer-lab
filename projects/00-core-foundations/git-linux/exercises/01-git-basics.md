# Exercise 01: Git Basics

> Initialize a repo, make commits, and explore the commit history.

## Goal

Master the core Git workflow: `init`, `add`, `commit`, `status`, `log`, and `diff`.

## Instructions

### 1. Initialize a Repository

```bash
mkdir my-project
cd my-project
git init
```

You should see: `Initialized empty Git repository in ...`

### 2. Make Your First Commit

```bash
echo "# My Project" > README.md
git status                    # README.md shows as untracked
git add README.md
git commit -m "Initial commit: add README"
```

### 3. Add More Files

```bash
echo "package main" > main.go
echo 'import "fmt"' >> main.go
echo "" >> main.go
echo "func main() {" >> main.go
echo '    fmt.Println("Hello, Git!")' >> main.go
echo "}" >> main.go

git add main.go
git commit -m "Add main.go with hello world"
```

### 4. Explore History

```bash
git log              # View commit history
git log --oneline    # Compact one-line view
git log --graph      # Graph view (useful for branches later)
git log -p           # Show diffs in log
```

### 5. Check Changes

```bash
# Modify README.md
echo "## Documentation" >> README.md
echo "This project demonstrates Git basics." >> README.md

git diff                        # See unstaged changes
git diff --staged               # See staged changes (none yet)
git add README.md
git diff --staged               # Now shows staged changes
git commit -m "Update README with documentation section"
```

### 6. View Commit Details

```bash
git show HEAD          # Show latest commit details
git show HEAD~1        # Show second-to-last commit
git show <commit-hash> # Show a specific commit
```

## Self-Check

- Can you see all 3 commits with `git log --oneline`?
- Can you see the diff of what changed in the second commit?
- What does `git status` show when all changes are committed?

## Key Commands Reference

| Command | Purpose |
|---------|---------|
| `git init` | Create a new repository |
| `git add <file>` | Stage changes for commit |
| `git commit -m "msg"` | Commit staged changes |
| `git status` | Show current state |
| `git log` | Show commit history |
| `git diff` | Show unstaged changes |
| `git show <ref>` | Show commit details |
