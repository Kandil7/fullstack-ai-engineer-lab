# Exercise 02: Git Branching & Merging

> Create branches, make changes, merge them, and resolve conflicts.

## Goal

Master branch creation, switching, merging, and conflict resolution.

## Instructions

### 1. Create and Switch Branches

```bash
# Starting from the repo in exercise 01
git branch feature-login          # Create a branch
git checkout feature-login        # Switch to it
# Or in one command:
git checkout -b feature-login
```

### 2. Make Changes on the Feature Branch

```bash
echo "package main" > login.go
echo "" >> login.go
echo "func login(username, password string) bool {" >> login.go
echo '    return username == "admin" && password == "secret"' >> login.go
echo "}" >> login.go

git add login.go
git commit -m "Add login function"
```

### 3. Switch Back to Main

```bash
git checkout main
# Notice: login.go is gone! (it only exists on feature-login branch)
```

### 4. Make Conflicting Changes

```bash
echo "package main" > main.go
echo "" > main.go
echo "func main() {" >> main.go
echo '    println("Starting app...")' >> main.go
echo "}" >> main.go

git add main.go
git commit -m "Update main with startup message"
```

### 5. Merge the Feature Branch

```bash
git merge feature-login
```

This should succeed automatically (no conflict) because different files were changed.

### 6. Create a Merge Conflict

```bash
# Create a conflict scenario
git checkout -b feature-conflict

# Edit main.go to have different content
echo 'package main' > main.go
echo '' >> main.go
echo 'func main() {' >> main.go
echo '    println("Feature branch version")' >> main.go
echo '    login("admin", "secret")' >> main.go
echo '}' >> main.go

git add main.go
git commit -m "Feature branch changes to main.go"

git checkout main

# Edit the same lines on main
echo 'package main' > main.go
echo '' >> main.go
echo 'func main() {' >> main.go
echo '    println("Main branch version")' >> main.go
echo '}' >> main.go

git add main.go
git commit -m "Main branch changes to main.go"
```

### 7. Resolve the Conflict

```bash
git merge feature-conflict
# Git reports: CONFLICT in main.go

# Open main.go and look for conflict markers:
# <<<<<<< HEAD
# (main version)
# =======
# (feature version)
# >>>>>>> feature-conflict

# Edit main.go to keep the desired version:
echo 'package main' > main.go
echo '' >> main.go
echo 'func main() {' >> main.go
echo '    println("Merged version")' >> main.go
echo '    login("admin", "secret")' >> main.go
echo '}' >> main.go

git add main.go
git commit -m "Resolve merge conflict in main.go"
```

## Self-Check

- Can you list all branches with `git branch`?
- What does `git log --graph --oneline --all` show?
- Can you identify merge commits in the log?

## Key Commands Reference

| Command | Purpose |
|---------|---------|
| `git branch <name>` | Create a branch |
| `git checkout <branch>` | Switch to a branch |
| `git checkout -b <name>` | Create and switch |
| `git merge <branch>` | Merge branch into current |
| `git branch -d <name>` | Delete a branch |
| `git log --graph --all` | Visual branch history |
