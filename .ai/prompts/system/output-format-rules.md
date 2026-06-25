---
id: sys.output-format-rules
layer: system
version: 1.0.0
status: active
owner: workspace
prepend: most-runs
---

# Output Format Rules

A shared contract reused by all role/task prompts (DRY — do not restate format per prompt).

## Layering

Every run is assembled in this order:

1. **Governor** (`system/workspace-governor.md`) — global rules
2. **Role** (`roles/*.md`) — who you are acting as
3. **Task** (`tasks/*.md`) — the specific job (optional)
4. **Output format rules** (this file)
5. **Critic / repair** (optional follow-up pass)

## Structure Requirements

- Use markdown headings; keep sections short and scannable.
- When an artifact template exists in `templates/`, **fill it** — do not invent a new layout.
- Start with a one-line summary, then details.
- Use tables for comparisons, severity, and metrics.

## Required Sections (when applicable)

- `## Missing Inputs` — anything you need but were not given. Omit only if truly none.
- `## Assumptions` — explicitly label any assumption you had to make.
- `## Open Questions` — unresolved decisions, or "None".

## Tone & Length

- Bounded. No filler. No restating the question back at length.
- Cite exact files/areas as `path:line` where relevant.

## Anti-Hallucination

- If you do not know, say so and request the source.
- Mark inference vs. confirmed fact.
- Never fabricate file paths, API names, or metrics.
