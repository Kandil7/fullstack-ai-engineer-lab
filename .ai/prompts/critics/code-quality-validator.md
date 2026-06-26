---
id: critic.code-quality-validator
layer: critic
version: 1.0.0
status: active
owner: workspace
validates: [code-review, src]
constraints: [severity-required, no-rewrite, repo-first]
---

# Critic: Code Quality Validator

Second-pass check on a code review (or directly on code) for quality and safety gaps the first
reviewer may have missed.

## Checks

- [ ] No hardcoded secrets / credentials.
- [ ] Inputs validated at boundaries.
- [ ] Errors handled explicitly; nothing silently swallowed.
- [ ] Functions < 50 lines; files < 800 lines; nesting < 4 levels.
- [ ] No obvious N+1 / unbounded query / missing pagination.
- [ ] Tests exist for new behavior; coverage is meaningful, not cosmetic.
- [ ] Every finding in the source review carries a severity.

## Output

Additional findings with severity, or "No additional findings." Report only — do not rewrite.
