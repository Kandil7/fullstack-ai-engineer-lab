---
id: task.review-summarizer
layer: task
version: 1.0.0
status: active
owner: workspace
pairs_with_roles: [code-reviewer]
constraints: [preserve-severity, actionable, repo-first]
---

# Task: Review Summarizer

Condense one or more code reviews into a prioritized action list.

## Steps

1. Collect findings across the review(s).
2. Group by severity (Critical → Low), preserving original severities.
3. Deduplicate overlapping findings.
4. Produce an ordered fix list with file references.
5. Note which items block "done" vs. which are deferrable.

## Constraints

- Do not downgrade a Critical/High finding when summarizing.
- Every line stays actionable and located (`path:line`).
- Output feeds `feature/05-fix.md` and updates `mistakes.md`.
