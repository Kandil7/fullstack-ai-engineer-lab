# Git Cheat Sheet

## Basic Commands

### Repository Setup
```bash
git init                          # Initialize new repo
git clone <url>                   # Clone remote repo
git clone --depth 1 <url>         # Shallow clone (faster)
```

### Staging & Committing
```bash
git status                        # Show working tree status
git add <file>                    # Stage specific file
git add .                         # Stage all changes
git add -p                        # Stage interactively (patch mode)
git commit -m "message"           # Commit with message
git commit --amend                # Amend last commit
git commit --amend --no-edit      # Amend without changing message
```

### Viewing History
```bash
git log                           # Full log
git log --oneline                 # Compact log
git log --graph --oneline         # Visual branch graph
git log -5                        # Last 5 commits
git log --author="name"           # Filter by author
git log --since="2 weeks ago"     # Filter by date
git diff                          # Unstaged changes
git diff --staged                 # Staged changes
git show <commit>                 # Show commit details
```

---

## Branching

### Branch Operations
```bash
git branch                        # List local branches
git branch -a                     # List all branches (local + remote)
git branch <name>                 # Create new branch
git branch -d <name>              # Delete branch (safe)
git branch -D <name>              # Delete branch (force)
git branch -m <old> <new>         # Rename branch
```

### Switching Branches
```bash
git checkout <branch>             # Switch to branch
git checkout -b <branch>          # Create and switch
git switch <branch>               # Switch (modern)
git switch -c <branch>            # Create and switch (modern)
```

### Merging
```bash
git merge <branch>                # Merge branch into current
git merge --no-ff <branch>        # Merge with merge commit
git merge --squash <branch>       # Squash merge
git merge --abort                 # Abort merge
```

### Rebasing
```bash
git rebase <branch>               # Rebase onto branch
git rebase -i HEAD~5              # Interactive rebase last 5 commits
git rebase --abort                # Abort rebase
git rebase --continue             # Continue after resolving conflicts
```

---

## Collaboration

### Remote Operations
```bash
git remote -v                     # List remotes
git remote add origin <url>       # Add remote
git remote set-url origin <url>   # Change remote URL
git fetch origin                  # Fetch from remote
git fetch --all                   # Fetch all remotes
```

### Pushing & Pulling
```bash
git push origin <branch>          # Push to remote
git push -u origin <branch>       # Push and set upstream
git push --force-with-lease       # Safe force push
git pull origin <branch>          # Fetch and merge
git pull --rebase origin <branch> # Fetch and rebase
```

### Tracking Branches
```bash
git branch -vv                    # Show tracking branches
git branch --set-upstream-to=origin/<branch> <branch>  # Set upstream
```

### Stashing
```bash
git stash                         # Stash changes
git stash push -m "message"       # Stash with message
git stash list                    # List stashes
git stash pop                     # Apply and remove stash
git stash apply                   # Apply stash (keep it)
git stash drop                    # Delete stash
git stash clear                   # Delete all stashes
```

---

## Advanced

### Cherry-Picking
```bash
git cherry-pick <commit>          # Apply single commit
git cherry-pick <c1> <c2>         # Apply multiple commits
git cherry-pick --no-commit <c>   # Apply without committing
```

### Bisect (Binary Search for Bugs)
```bash
git bisect start                  # Start bisect
git bisect bad                    # Mark current as bad
git bisect good <commit>          # Mark commit as good
# Git checks out middle commit
# Test it, then mark as good/bad
git bisect reset                  # End bisect
```

### Reflog (Recover Lost Commits)
```bash
git reflog                        # Show reflog
git reflog show <branch>          # Show branch reflog
git checkout <commit-hash>        # Checkout lost commit
git branch <name> <commit-hash>   # Create branch at lost commit
```

### Cleaning
```bash
git clean -n                      # Dry run (show what would be removed)
git clean -f                      # Remove untracked files
git clean -fd                     # Remove untracked files and directories
git clean -fX                     # Remove only ignored files
```

### Advanced Logging
```bash
git log --stat                    # Show file changes per commit
git log --shortstat               # Show summary of changes
git log --name-only               # Show only changed files
git log --diff-filter=D --summary # Show deleted files
git log -S "function_name"        # Search for code changes
git log -G "regex"                # Search with regex
```

---

## This Repo's Conventions

### Branch Naming
- `feature/<name>` — New features
- `fix/<name>` — Bug fixes
- `docs/<name>` — Documentation changes
- `refactor/<name>` — Code refactoring
- `experiment/<name>` — Learning experiments

### Commit Messages
- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`
- Keep subject line under 72 characters
- Use imperative mood ("add feature" not "added feature")
- Reference issues when applicable

### Pull Requests
- One feature per PR
- Include description of changes
- Reference related ADRs
- Request review before merge
- Squash merge to main

### Protected Branches
- `main` — Protected, requires PR
- `develop` — Integration branch (if used)
- Feature branches — Delete after merge

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `git status` | What's changed? |
| `git diff` | What are the changes? |
| `git log --oneline` | What happened? |
| `git stash` | Save work temporarily |
| `git rebase -i` | Clean up history |
| `git bisect` | Find when bug was introduced |
| `git reflog` | Recover lost work |

---

*Last updated: 2026-08-06*
