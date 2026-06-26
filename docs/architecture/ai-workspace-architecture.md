# AI Workspace Architecture (`.ai/`)

The `.ai/` directory is the "brain" of the repo: how AI operating modes are composed and invoked.

## Prompt Layering

Each AI run is assembled deterministically:

```text
1. system/workspace-governor.md      (global rules)
2. roles/<role>.md                   (who you are)
3. tasks/<task>.md                   (the specific job, optional)
4. system/output-format-rules.md     (shape)
5. critics/<critic>.md | repair/*    (optional follow-up pass)
```

This keeps prompts **modular** — no monolithic mega-prompt. Format lives once in
`output-format-rules.md` (DRY); each prompt only declares its own constraints.

## Roles ↔ Workflows ↔ Templates

| Role                     | Primary workflow            | Template produced            |
| ------------------------ | --------------------------- | ---------------------------- |
| Project Planner          | feature/01-plan             | project-plan                 |
| System Architect         | feature/02-design           | architecture-review / adr    |
| Pair Programmer          | feature/03-build            | (code, notes)                |
| Code Reviewer            | feature/04-review           | code-review                  |
| Debugging Specialist     | debugging/*                 | debugging-session            |
| Source Learning Agent    | learning/*                  | source-*                     |
| Principal System Designer| architecture/*, evaluation/*| architecture-review / eval   |
| Learning Coach           | feature/06-reflect, learning| daily/weekly-review          |

## Critics & Repair

- **Critics** run a second adversarial pass (architecture-validator, code-quality-validator,
  prompt-auditor) and emit findings with severity — they never rewrite.
- **Repair** prompts handle failure modes: missing context, over-engineering, wrong output shape.

## Governance

Everything in `.ai/` is registered in `registries/prompt-registry.yaml` and
`registries/workflow-registry.yaml` with id, version, owner, status, and constraints — the
single source of truth for what exists and what each artifact is allowed to do.
