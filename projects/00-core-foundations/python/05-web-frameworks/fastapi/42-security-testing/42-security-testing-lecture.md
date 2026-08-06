# FastAPI — 42: Security Testing

## Topic Overview

Security features are real only when tests prove the boundaries hold. The
highest-value security tests are the **auth bypass matrix** — no token,
garbage token, expired token, tampered payload, wrong secret — because
they fail loudly and cheaply, and they protect the boundary that protects
everything else. **Fuzzing** throws hostile-but-valid-shaped inputs at
every boundary and the contract is zero 5xx. **Static analysis** (bandit)
and **dependency scanning** (pip-audit) automate the mechanical scans in
CI. And **threat modeling** is the generator: every threat an endpoint has
becomes a test or a documented residual risk.

The mental model: security testing is a loop — *model the threats, write
the bypass tests, fuzz the boundaries, scan the code and dependencies,
ship the loop in CI.*

## Learning Objectives

By the end of this lecture, you will be able to:

1. Build an auth bypass test matrix for a protected endpoint.
2. Fuzz input boundaries and hold the zero-5xx contract.
3. Run bandit and pip-audit in CI (and know what they catch).
4. Threat-model an endpoint into a concrete test list.

## Prerequisites

| Need | Where |
|---|---|
| Auth implementation | `38-auth-deep.py`, `39-oauth2-oidc.py` |
| Authorization rules | `40-authorization.py` |
| API security layers | `41-api-security.py` |

---

## 1. The auth bypass matrix

For every protected endpoint, test the full rejection set, not just the
happy path:

```python
attempts = {
    "no token": None,
    "garbage": "not.a.jwt",
    "expired": issue_token(... expires_in=-10),
    "tampered payload": forged_without_resigning,
    "wrong secret": signed_with_other_key,
}
# assert: every attempt -> 401
```

Plus the authorization cases from `40`: cross-tenant reads return 404, not
403 or 200. A matrix like this, run on every change, is what keeps auth
from rotting — the classic failure is a refactor that quietly drops a
check, which only the matrix catches.

## 2. Fuzzing boundaries

Fuzz inputs that are *valid shapes but hostile content*: null bytes,
unicode, 200-char strings, SQL-ish and path-ish text, control characters.
The contract is **zero 5xx** — a 500 on hostile input is an unhandled
code path, which is exactly where real exploits live. Keep the fuzz
corpus seeded and deterministic so failures reproduce.

## 3. Static and dependency scanning

- **bandit**: AST-level scan of your code — `eval`/`exec`, `shell=True`,
  unsafe `pickle`, hardcoded secrets, `assert` in non-test code.
- **pip-audit**: known CVEs in your dependency tree, checked against the
  OSV/vulnerability feeds.

Both are dumb, fast, and mechanical — exactly what belongs in CI on every
pull request, next to the tests. They do not replace review; they replace
the human's memory.

## 4. Threat modeling an endpoint

A two-minute model per sensitive endpoint: *assets* (what an attacker
wants), *attackers* (who), *vectors* (how), *mitigations* (what we built).
The output is the test list:

```python
/generate  -> oversize-prompt, prompt-injection-payload, rate-limit
/fetch-url -> ssrf-metadata, ssrf-localhost, bad-scheme
```

Every vector either has a test or is a documented residual risk. A threat
model that produces no tests is a review, not a model.

## Common Mistakes to Avoid

### Mistake 1: Happy-path-only tests
```python
# WRONG - 200s verified, 401/404 paths rot silently
# CORRECT - a bypass matrix per protected endpoint
```

### Mistake 2: No fuzzing at boundaries
```python
# WRONG - the one hostile input that 500s is the exploit
# CORRECT - seeded fuzz corpus; assert zero 5xx
```

### Mistake 3: Scans run manually ("when someone remembers")
```python
# WRONG - bandit/pip-audit sit unused on a laptop
# CORRECT - both in CI on every PR
```

### Mistake 4: Threat models that end as documents
```python
# WRONG - slide deck, no tests
# CORRECT - every vector -> a test or documented residual risk
```

## Best Practices

1. Bypass matrix on every protected endpoint, run in CI.
2. Fuzz boundaries with a seeded corpus; zero 5xx is the contract.
3. bandit + pip-audit in CI, gating merges.
4. Threat-model each sensitive endpoint into a test list.
5. Keep fuzz seeds fixed for reproducibility.
6. Test rejection semantics: 401 vs 404 vs 422 each mean something.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| Bypass matrix | one test file per auth boundary | — |
| Fuzzing | seconds in CI | — |
| bandit/pip-audit | seconds in CI | — |
| Threat model | 2 minutes per endpoint | — |

Security tests are cheap and permanent; security incidents are expensive
and temporary. The loop pays for itself on the first caught regression.

## AI Engineering Relevance

**Where this shows up:** LLM gateways (token auth + rate limits), agent
tool endpoints (SSRF, tool-arg validation), and any user-input boundary on
a model-serving path.

| Concept here | Used for |
|---|---|
| bypass matrix | proving /generate requires a valid key |
| fuzzing | hostile prompts never 500 the endpoint |
| static scan | no eval/shell in agent code |
| dependency scan | CVE'd inference libraries fail CI |
| threat model | agent tools enumerated as attack surfaces |

**Scale note:** the same matrix that guards one endpoint guards a fleet —
the tests are per-boundary, and boundaries are where attackers live.

## Practice Exercises

### Exercise 1: Bypass matrix  (Difficulty: Easy)
Build the five-attempt matrix; assert every attempt is rejected.

### Exercise 2: Cross-tenant 404  (Difficulty: Easy)
Assert other-tenants' rows return 404, never 200/403.

### Exercise 3: Fuzz contract  (Difficulty: Medium)
Fuzz 300 seeded hostile payloads; assert zero 5xx.

### Exercise 4: Static scan  (Difficulty: Medium)
Flag eval/shell/pickle patterns; assert clean code scans clean.

### Exercise 5: Threat-to-test  (Difficulty: Hard)
Threat-model `/fetch-url` and `/generate`; for each vector, write the
test that proves the mitigation.

### Exercise 6: CI wiring  (Difficulty: Hard)
Write the CI step list (unit → fuzz → bandit → pip-audit) as data and
assert every security job has a failing mode that stops the pipeline.

## Summary

| Concept | Description |
|---|---|
| bypass matrix | the rejection set, tested |
| fuzzing | hostile-shaped inputs; zero 5xx |
| bandit | static scan of your code |
| pip-audit | CVE scan of dependencies |
| threat model | vectors → tests |

Security testing is the discipline of proving boundaries. Bypass tests,
fuzz contracts, automated scans, and threat-to-test conversion — the loop,
in CI, on every change.

## Quick Reference

| Task | Idiom |
|---|---|
| Bypass suite | assert all of {none, garbage, expired, forged, wrong-secret} → 401 |
| Cross-tenant | assert → 404 |
| Fuzz | seeded corpus; `assert five_xx == 0` |
| Static scan | `bandit -r src` in CI |
| Dep scan | `pip-audit` in CI |
| Threat model | assets → vectors → tests |

## Next Steps

Next: **[43 — Structured Logging](43-structured-logging-lecture.md)** —
seeing the attacks that get through, in JSON with correlation IDs.

Continues in: **[44 — Metrics with Prometheus](44-metrics-prometheus-lecture.md)** —
the numbers that prove the service is alive and fast.

Official docs:
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- bandit: https://bandit.readthedocs.io/
- pip-audit: https://pypi.org/project/pip-audit/
