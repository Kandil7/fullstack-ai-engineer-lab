# Task Index

This repo targets Windows/PowerShell, so automation lives in `infra/scripts/*.ps1` rather than
a Makefile. This file is the human-readable index of common tasks.

| Task                     | Command                                                              |
| ------------------------ | ------------------------------------------------------------------- |
| One-time setup           | `./infra/scripts/setup.ps1`                                         |
| Start infra (compose)    | `docker compose -f infra/docker/docker-compose.yml up -d`           |
| Stop infra               | `docker compose -f infra/docker/docker-compose.yml down`            |
| Run dev (auth-service)   | `./infra/scripts/dev-run.ps1`                                       |
| Seed database            | `./infra/scripts/seed-db.ps1`                                       |
| New ADR                  | `./infra/scripts/new-adr.ps1 "<title>"`                             |
| New code review          | `./infra/scripts/new-review.ps1 <project-path> "<feature>"`         |
| New source note          | `./infra/scripts/new-source-note.ps1 <doc|repo|book|notebook> "<title>"` |
| Test repo structure      | `Invoke-Pester tests/repo-structure`                                |
| Test templates           | `Invoke-Pester tests/templates`                                     |
| Test workflows           | `Invoke-Pester tests/workflows`                                     |
| Test prompts             | `Invoke-Pester tests/prompts`                                       |
| Test auth-service (Go)   | `cd projects/01-backend-go/01-auth-service; go test ./...`          |

> Prerequisites: PowerShell 5.1+, Go 1.22+, Docker Desktop (optional), Pester 5+
> (`Install-Module Pester -Scope CurrentUser`).
