# Code Review: <feature / file set>

- **Reviewer:** <Code Reviewer mode>
- **Date:** YYYY-MM-DD
- **Project path:** <projects/...>
- **Scope reviewed:** <files / diff>
- **Overall score:** <N>/10

> Reviewer does **not** rewrite code by default — findings only, with exact file references.

## Findings by Severity

<!-- REQUIRED. Every finding carries a severity. Empty sections may say "None". -->

### Critical
<!-- Security vulnerability or data-loss risk. BLOCKS merge. -->
- [ ] **<file:line>** — <issue> · _Why:_ <impact> · _Fix:_ <suggestion>

### High
<!-- Bug or significant quality issue. Should fix before merge. -->
- [ ] **<file:line>** — <issue> · _Why:_ <impact> · _Fix:_ <suggestion>

### Medium
<!-- Maintainability concern. Consider fixing. -->
- [ ] **<file:line>** — <issue> · _Fix:_ <suggestion>

### Low
<!-- Style or minor suggestion. Optional. -->
- [ ] **<file:line>** — <issue>

## What's Good

<!-- Reinforce patterns worth keeping. -->

## Checklist

- [ ] No hardcoded secrets
- [ ] Errors handled explicitly
- [ ] Inputs validated at boundaries
- [ ] Functions < 50 lines, files < 800 lines
- [ ] Tests exist for new behavior

## Approval

- Decision: **Approve** | **Approve with warnings** | **Block**
- Blocking items: <list or "None">
