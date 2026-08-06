# FastAPI — 50: Configuration

## Topic Overview

Configuration is the separation of code from environment: the same image
runs in dev, staging, and prod because *config* differs, not code.
**pydantic-settings** gives typed, validated, env-backed settings with a
precedence chain (defaults < `.env` < real environment < explicit args).
Two rules carry the discipline: **fail fast** — a typo'd `DATABASE_URL`
surfaces at startup, not at the first request — and **no secrets in
code** — API keys arrive via env or a secret manager, and a missing
secret refuses to boot. **Feature flags** extend config into a runtime
dial: a flag flips a feature without a deploy and enables gradual
rollouts.

The mental model: config is a validated contract between the image and
its environment. Validate it all at startup; keep secrets out of it; and
keep code identical across environments.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Model settings with pydantic-settings and typed validation.
2. Explain and apply the env precedence chain.
3. Source secrets from env/secret managers and fail fast.
4. Use per-environment values, not per-environment code.
5. Gate features with flags and gradual rollout.

## Prerequisites

| Need | Where |
|---|---|
| Pydantic v2 | `26-pydantic-v2-deep-lecture.md` |
| Deployment | `48`, `49` lectures |
| Secrets | `41-api-security-lecture.md` |

---

## 1. Typed, validated settings

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env")
    database_url: str = "sqlite:///./dev.db"
    max_tokens: int = Field(default=2048, ge=1, le=128_000)
```

Env vars map onto typed fields (`APP_MAX_TOKENS=4096` → `max_tokens=4096`)
and validation runs at construction. A bad type, an out-of-range value, or
a custom validator failure raises **at startup** — the fail-fast rule that
turns a runtime mystery into an immediate error.

## 2. The precedence chain

```
defaults < .env file < real environment < explicit constructor args
```

Real environment beats the `.env` file — which is what lets containers
override everything (dev image, staging env) without touching code.
Explicit args win in tests. Document the chain; it is how environments
differ safely.

## 3. Secrets: env and secret managers

API keys never live in code or committed config. They arrive via:
- environment variables (containers),
- a secret manager (K8s secrets, Vault, cloud secret stores) injected at
  startup.

The loader is strict: a missing required secret raises and the service
refuses to start. A service that boots without its keys is a
misconfiguration waiting to become an outage.

## 4. Per-environment configuration

One schema; per-env values: `dev` has debug on and low limits, `prod`
has debug off and high limits. The rule is **values differ, code does
not** — `if env == "prod"` branches in code are a smell; the environment
should only select values.

## 5. Feature flags

Flags gate unfinished or risky features:

```python
flags = FeatureFlags({"hybrid_search": True})
if flags.enabled("hybrid_search"): ...
```

- Flipped without a deploy (config change, not code change).
- Gradual rollout by percent catches regressions early.
- Default off for new features; removed when stable — removal is editing
  config, not deleting code branches.

## Common Mistakes to Avoid

### Mistake 1: `os.environ.get` scattered through the code
```python
# WRONG - untyped, unvalidated, tested nowhere
# CORRECT - one Settings model validated at startup
```

### Mistake 2: Secrets in code or committed .env
```python
# WRONG - the leak is permanent in git history
# CORRECT - env/secret manager; fail fast when missing
```

### Mistake 3: No fail-fast
```python
# WRONG - a bad DATABASE_URL crashes at first request
# CORRECT - validation raises at startup
```

### Mistake 4: Env-specific code branches
```python
# WRONG - if env == 'prod': ...  (logic differs per env)
# CORRECT - per-env VALUES; identical code everywhere
```

### Mistake 5: Feature branches that need a deploy to remove
```python
# WRONG - dead code deletion requires a release
# CORRECT - flags as config; flip off, then remove
```

## Best Practices

1. One Settings model, validated at startup.
2. Follow the precedence chain; containers override via real env.
3. Secrets from env/manager; fail fast when missing.
4. Per-env values, identical code.
5. Flags for rollout; default off; remove when stable.
6. Namespace env vars with a prefix (`APP_`).
7. Never log settings that contain secrets.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| Settings model | one class | — |
| Startup validation | milliseconds | — |
| Secret manager calls | one per boot | cache values |
| Feature flags | one dict | — |

Configuration costs almost nothing at runtime — its value is entirely in
startup validation and environment separation.

## AI Engineering Relevance

**Where this shows up:** model/provider choice per environment, API keys
for LLM providers, per-tenant model limits, and rollout flags for
experimental inference features.

| Concept here | Used for |
|---|---|
| typed settings | model names, token limits, timeouts |
| env precedence | staging pointing at staging models |
| secret manager | provider API keys |
| feature flags | gradual rollout of a new reranker |
| fail fast | no half-configured gateway in prod |

**Scale note:** a fleet of gateways is only as consistent as its config
pipeline — one validated model per environment is what keeps 1000 pods
behaving identically.

## Practice Exercises

### Exercise 1: Typed settings  (Difficulty: Easy)
Env overrides default; bad values fail at construction.

### Exercise 2: Validation  (Difficulty: Easy)
Out-of-range field and bad scheme raise; assert both.

### Exercise 3: Precedence  (Difficulty: Medium)
Model the chain; assert explicit > env > .env > default.

### Exercise 4: Secrets  (Difficulty: Medium)
Load from env; missing secret raises before start.

### Exercise 5: Env configs  (Difficulty: Medium)
Per-env dicts; assert values differ while the schema is identical.

### Exercise 6: Flag rollout  (Difficulty: Hard)
Percent-based rollout; assert the fraction enabled matches the target
and flips without code changes.

## Summary

| Concept | Description |
|---|---|
| typed settings | one validated model |
| precedence | defaults < .env < env < explicit |
| secrets | env/manager only, fail fast |
| per-env | values differ, code identical |
| flags | runtime dials for rollout |

Config is the contract between the image and the environment — typed,
validated at startup, secret-free, and environment-separated. Get that
right and the same artifact runs everywhere safely.

## Quick Reference

| Task | Idiom |
|---|---|
| Settings model | `class Settings(BaseSettings)` |
| Env prefix | `SettingsConfigDict(env_prefix="APP_")` |
| Fail fast | validation at construction |
| Secret | env/manager; raise if missing |
| Per env | dict of value-sets |
| Flag | `flags.enabled("name")` default off |

## Next Steps

Next: **[51 — CI/CD](51-ci-cd-lecture.md)** — testing, building, scanning,
and shipping with the config in place.

Continues in: **[52 — Serving ML Models](52-serving-ml-models-lecture.md)** —
the payload that justifies the pipeline.

Official docs:
- pydantic-settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- 12-factor config: https://12factor.net/config
