# Core Computer Science Foundations

> Phase 00: Build the bedrock skills that power every other module in this lab.

## Overview

Before writing production Go services, deploying containers, or building AI pipelines, you need rock-solid fundamentals. This phase covers three pillars:

| Module | What You'll Master | Why It Matters |
|--------|-------------------|----------------|
| **Go Fundamentals** | Types, concurrency, interfaces, testing | Every backend service in this lab is written in Go |
| **Git & Linux** | Branching, rebasing, shell scripting, permissions | DevOps, CI/CD, and deployment all run on Linux with Git |
| **Data Structures & Algorithms** | Arrays, trees, graphs, sorting, Big-O | Interview prep + writing efficient code for AI workloads |

## Module Breakdown

### 1. Go Fundamentals (`go/`)

Go is the backbone of this lab. By the end of this module, you'll be comfortable with:

- **Type system**: structs, interfaces, generics (Go 1.18+)
- **Concurrency**: goroutines, channels, select, sync package
- **Error handling**: custom errors, error wrapping, sentinel errors
- **Testing**: table-driven tests, benchmarks, fuzzing
- **Project layout**: cmd/, internal/, pkg/ conventions

**Project**: Build a CLI tool that reads JSON, transforms data, and writes output. Practice Go idioms, error handling, and testing.

```bash
# Example: what you'll build
$ go run . transform --input data.json --output result.json --field "name" --upper
```

### 2. Git & Linux (`git-linux/`)

Every engineer in this lab needs to be fluent in Git workflows and Linux fundamentals:

- **Git**: branching strategies (trunk-based, Git Flow), interactive rebase, cherry-pick, bisect
- **Linux**: file permissions, process management, cron jobs, networking basics
- **Shell scripting**: bash/zsh automation, pipes, xargs, find, grep
- **SSH & remote servers**: key management, tunneling, rsync

**Project**: Set up a multi-branch Git repository with proper CI hooks, write a shell script that automates deployment prep, and configure SSH access to a remote server.

### 3. Data Structures & Algorithms (`ds-algo/`)

AI engineering isn't just about frameworks — it's about understanding complexity, choosing the right data structure, and writing code that scales:

- **Time & space complexity**: Big-O analysis, amortized cost
- **Core structures**: arrays, linked lists, stacks, queues, hash maps, trees, heaps, graphs
- **Algorithms**: binary search, BFS/DFS, dynamic programming, greedy algorithms
- **AI-specific**: trie for tokenization, graph traversal for knowledge bases, priority queues for scheduling

**Project**: Solve 30 problems from LeetCode-style challenges, focusing on problems that appear in AI system design (caching, scheduling, search).

## How This Phase Supports Later Work

```
Phase 00: Foundations
    │
    ├── Phase 01: Backend Go ─────── Go skills → API services
    │
    ├── Phase 02: Frontend ───────── Git workflows → collaboration
    │
    ├── Phase 03: Databases ──────── SQL, Redis, vector DBs
    │
    ├── Phase 04: AI Engineering ─── Python + Go for ML pipelines
    │
    ├── Phase 05: System Design ──── DSA knowledge → architecture decisions
    │
    ├── Phase 06: DevOps ─────────── Linux + Git → CI/CD, Docker, K8s
    │
    └── Phase 07: Capstone ───────── Everything together
```

## Daily Routine (Recommended)

| Time Block | Activity |
|------------|----------|
| **Morning (2h)** | Go exercises or new concept |
| **Afternoon (1h)** | Git/Linux practice or DSA problems |
| **Evening (30m)** | Review, document learnings, push to repo |

## Resources

- [Go Tour](https://tour.golang.org/) — Interactive Go introduction
- [Pro Go (Adam Bell)](https://adam-f bell.com/pro-go) — Deep Go reference
- [Pro Git Book](https://git-scm.com/book/) — Free, comprehensive Git guide
- [Linux Upskill Challenge](https://linuxupskillchallenge.org/) — 30-day Linux fundamentals
- [NeetCode](https://neetcode.io/) — DSA problem sets with video explanations

## Progress Tracking

- [ ] Go: Complete all exercises in `go/`
- [ ] Git: Set up multi-branch workflow with CI hooks
- [ ] Linux: Write 10 shell scripts for common tasks
- [ ] DSA: Solve 30 problems (10 easy, 10 medium, 10 hard)

---

*This module typically takes 4-6 weeks at 2-3 hours/day. Don't rush — these foundations compound.*
