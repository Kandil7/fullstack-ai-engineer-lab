# Security Testing — Glossary 42

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Auth bypass | Test | Proving a protected endpoint rejects every invalid token shape |
| bandit | Tool | Static analyzer for dangerous Python patterns |
| Bypass matrix | Test | The rejection set: no/expired/forged/wrong-secret tokens |
| CVE | Concept | Known vulnerability in a dependency |
| Fuzzing | Test | Hostile-but-valid-shaped inputs; zero 5xx contract |
| pip-audit | Tool | Scans installed packages for known CVEs |
| Residual risk | Model | A documented, accepted, untested threat |
| Seed | Test | Fixed random value making fuzz runs reproducible |
| Static analysis | Test | AST-level scanning without running code |
| Threat model | Method | Assets → attackers → vectors → mitigations |
| 5xx | Signal | Server error — the fuzz contract forbids these |
| 401 | Status | Unauthenticated — the bypass matrix expects this |

## Detailed Definitions

### Auth bypass
**Definition**: The class of test proving an endpoint rejects invalid
credentials — the highest-value security test because it guards the
boundary that guards everything else.
**Related**: Bypass matrix

### bandit
**Definition**: A static analyzer (AST-level) flagging dangerous patterns —
`eval`/`exec`, `shell=True`, unsafe `pickle`, hardcoded secrets, `assert`
in non-test code.
**Related**: Static analysis

### Bypass matrix
**Definition**: The explicit rejection set per protected endpoint — no
token, garbage, expired, tampered payload, wrong secret — all asserted to
return 401.
**Related**: Auth bypass

### CVE
**Definition**: A known, catalogued vulnerability in a package — what
`pip-audit` checks your dependency tree against.
**Related**: pip-audit

### Fuzzing
**Definition**: Sending hostile-but-valid-shaped inputs (null bytes,
unicode, long strings, SQL/path text) at boundaries; the contract is zero
5xx responses.
**Related**: 5xx

### pip-audit
**Definition**: A CLI that scans installed packages for known CVEs against
OSV/vulnerability feeds — the dependency half of automated scanning.
**Related**: CVE

### Residual risk
**Definition**: A threat deliberately not tested — documented and accepted;
threat models must end in tests or explicit residuals, never silence.
**Related**: Threat model

### Seed
**Definition**: The fixed random seed for a fuzz corpus, making failures
reproducible in CI.
**Related**: Fuzzing

### Static analysis
**Definition**: Scanning source without executing it — AST-level pattern
matching for dangerous constructs; fast, mechanical, CI-able.
**Related**: bandit

### Threat model
**Definition**: The assets → attackers → vectors → mitigations analysis of
an endpoint, whose output is the test list.
**Related**: Residual risk

### 5xx
**Definition**: Server-error responses — a fuzz 5xx is an unhandled code
path and a likely exploit site; the fuzz contract is zero.
**Related**: Fuzzing

### 401
**Definition**: Unauthenticated — what every invalid-token attempt must
return in the bypass matrix.
**Related**: Bypass matrix

## Key Concepts Summary

### The security-testing loop
1. Threat-model each sensitive endpoint.
2. Write the bypass matrix (401 set).
3. Fuzz boundaries (zero 5xx).
4. Scan statically (bandit) and by dependency (pip-audit).
5. Run the whole loop in CI on every change.

### The rejection semantics
- 401: unauthenticated (invalid/absent token).
- 404: cross-tenant or nonexistent (hide existence).
- 422: invalid input shape.
- 5xx: forbidden — a bug.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. No/expired/forged/wrong-secret tokens — ___
2. Hostile-shaped inputs; zero 5xx — ___
3. Static analyzer for dangerous patterns — ___
4. Scans dependencies for CVEs — ___
5. Assets → attackers → vectors → mitigations — ___
6. A documented, accepted untested threat — ___
7. Fixed random value for reproducibility — ___
8. What the bypass matrix expects — ___

**Answers:** 1-bypass matrix, 2-fuzzing, 3-bandit, 4-pip-audit,
5-threat model, 6-residual risk, 7-seed, 8-401
