# Architecture Decision Records (ADRs)

ADRs capture **why** a decision was made, the options considered, and the consequences. They are
the architectural memory of the workspace. New ADRs are created with `infra/scripts/new-adr.ps1`.

## Index

| ID   | Title                                   | Status   | Date       |
| ---- | --------------------------------------- | -------- | ---------- |
| [0001](0001-repo-centric-workspace.md)    | Repo-centric agentic workspace          | Accepted | 2026-06-26 |
| [0002](0002-prompt-modularization.md)     | Prompt modularization & `.ai` namespace | Accepted | 2026-06-26 |
| [0003](0003-hybrid-stack-go-fastapi.md)   | Hybrid stack — Go core + FastAPI AI     | Accepted | 2026-06-26 |

## Statuses

`Proposed` → `Accepted` → (`Superseded by ADR-XXXX` | `Deprecated`)

## Conventions

- File name: `NNNN-kebab-title.md` (4-digit, zero-padded).
- Every ADR must have a non-empty **Consequences** section.
- Keep `registries/decision-log.yaml` in sync with this index.
