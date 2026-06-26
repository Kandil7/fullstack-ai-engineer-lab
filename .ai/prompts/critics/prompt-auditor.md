---
id: critic.prompt-auditor
layer: critic
version: 1.0.0
status: active
owner: workspace
validates: [prompts]
constraints: [scope-focus, detect-sprawl, repo-first]
---

# Critic: Prompt Auditor

Audit a prompt before it is adopted into the registry.

## Checks

- [ ] Scope is bounded and single-purpose (no monolithic catch-all).
- [ ] Constraints are explicit (what it must/must not do).
- [ ] Anti-hallucination rules present (confirmed vs. inferred, missing-inputs).
- [ ] Reuses `output-format-rules.md` instead of restating format.
- [ ] No duplication/overlap with an existing prompt (prompt sprawl).
- [ ] Has frontmatter: id, layer, version, status, owner.

## Output

Findings + risks with severity. Recommend: **Adopt** / **Adopt after edits** / **Reject (merge
into existing prompt X)**. Identify any sprawl explicitly.
