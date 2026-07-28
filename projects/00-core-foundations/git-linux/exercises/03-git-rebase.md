# Exercise 03: Git Rebase & Interactive Rebase

> Rewrite history with rebase, squash commits, and reorder them.

## Goal

Master `git rebase` for clean commit history and interactive rebase for squashing, rewording, and reordering.

## Instructions

### 1. Set Up a Branch with Multiple Commits

```bash
git checkout -b messy-history

# Make several small commits
echo "feature-1" > feature.txt && git add feature.txt && git commit -m "Add feature 1"
echo "feature-2" >> feature.txt && git add feature.txt && git commit -m "WIP: working on feature"
echo "feature-3" >> feature.txt && git add feature.txt && git commit -m "Add feature 3"
echo "fix" > fix.txt && git add fix.txt && git commit -m "Fix typo in docs"
echo "oops" >> fix.txt && git add fix.txt && git commit -m "Actually fix the real bug"
echo "feature-4" >> feature.txt && git add feature.txt && git commit -m "Add feature 4 - final version"

git log --oneline
# Should show 6 commits on top of main
```

### 2. Interactive Rebase to Squash

```bash
# Squash the last 5 commits into the first one
git rebase -i HEAD~6
```

In the editor, change the second through sixth lines from `pick` to `squash` (or `s`). Save and exit. The commits will be combined into one.

### 3. Rebase Feature Branch onto Main

```bash
git checkout main
git checkout -b feature-to-rebase

# Make some commits
echo "new-feature" > new.txt && git add new.txt && git commit -m "New feature"
echo "more" >> new.txt && git add new.txt && git commit -m "More changes"

# Simulate main advancing
git checkout main
echo "main-update" > main-update.txt && git add main-update.txt && git commit -m "Update on main"

# Rebase our feature onto the updated main
git checkout feature-to-rebase
git rebase main

# Now feature-to-rebase sits on top of the latest main
git log --oneline
```

### 4. Rebase vs Merge Comparison

| Aspect | Rebase | Merge |
|--------|--------|-------|
| History | Linear, clean | Preserves actual timeline |
| Conflict resolution | One commit at a time | All at once |
| When to use | Feature branches, PR cleanup | Public/shared branches |
| Safety | Rewrites history | Safe for shared branches |

### 5. The Golden Rule

> **Never rebase commits that have been pushed to a shared repository.**

If you've already pushed, use `git merge` instead. After a rebase, you need `git push --force-with-lease` (not `--force`).

## Self-Check

- What's the difference between `git merge` and `git rebase`?
- When would you use `rebase -i`?
- What does `squash` do in interactive rebase?

## Key Commands Reference

| Command | Purpose |
|---------|---------|
| `git rebase <branch>` | Reapply commits on top of another branch |
| `git rebase -i HEAD~N` | Interactive rebase for last N commits |
| `git rebase --abort` | Cancel rebase if things go wrong |
| `git rebase --continue` | Continue after resolving conflicts |
| `git push --force-with-lease` | Force push after rebasing (safer than --force) |
