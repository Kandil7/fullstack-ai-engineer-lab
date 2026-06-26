---
id: critic.architecture-validator
layer: critic
version: 1.0.0
status: active
owner: workspace
validates: [architecture-review, adr]
constraints: [flag-overengineering, require-tradeoffs, repo-first]
---

# Critic: Architecture Validator

Validate an architecture review or ADR before it is accepted.

## Checks

- [ ] Components have clear, non-overlapping responsibilities.
- [ ] Data flow is complete (no dangling component).
- [ ] Scalability claims are tied to concrete mechanisms.
- [ ] Failure points and fallbacks are stated.
- [ ] Tradeoffs are explicit (not a single option presented as inevitable).
- [ ] **No unjustified complexity** — no extra agents/services/layers without a driver.
- [ ] Hard-to-reverse choices are captured as ADR candidates.

## Output

A findings list with severity (Critical/High/Medium/Low). If over-engineered, route to
`repair/simplify-overengineered-plan.md`. Do not rewrite the design — report only.
