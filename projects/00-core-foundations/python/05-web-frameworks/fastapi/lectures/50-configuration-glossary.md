# Configuration — Glossary 50

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| .env file | Source | Local file of env values (dev; never committed) |
| BaseSettings | Library | pydantic-settings base class for typed config |
| Env prefix | Detail | `APP_` namespacing env vars |
| Env var | Source | The real environment — beats .env |
| Fail fast | Principle | Startup validation over runtime surprises |
| Feature flag | Mechanism | A config dial gating a feature |
| Per-env config | Pattern | Values differ by env; code identical |
| Precedence | Concept | defaults < .env < env < explicit args |
| Rollout | Mechanism | Gradual flag enablement by percent |
| Secret manager | Source | Vault/K8s/cloud store for credentials |
| Settings | Model | The typed, validated config object |
| Startup validation | Practice | Config checked before serving |

## Detailed Definitions

### .env file
**Definition**: A local file of env values loaded by pydantic-settings —
dev convenience, never committed (see `41` secrets).
**Related**: Precedence

### BaseSettings
**Definition**: The pydantic-settings base class whose subclasses read
env vars onto typed fields with validation.
**Related**: Settings

### Env prefix
**Definition**: The `APP_` namespace prefix mapping env vars
(`APP_MAX_TOKENS` → `max_tokens`) — avoids collisions and documents
ownership.
**Related**: Env var

### Env var
**Definition**: A real environment variable — in the precedence chain it
beats the `.env` file, letting containers override everything.
**Related**: Precedence

### Fail fast
**Definition**: Raising at startup for invalid config — a bad
`DATABASE_URL` errors at boot, not at the first request.
**Related**: Startup validation

### Feature flag
**Definition**: A config value gating an unfinished/risky feature —
flipped without a deploy, enabled gradually.
**Related**: Rollout

### Per-env config
**Definition**: The pattern of per-environment value-sets over one schema
— dev/staging/prod differ in values, never in code.
**Related**: Env var

### Precedence
**Definition**: The lookup order defaults < `.env` file < real env <
explicit args — the rule that lets one image run everywhere.
**Related**: Env var

### Rollout
**Definition**: Gradually enabling a flag by percent of traffic — catches
regressions before full exposure.
**Related**: Feature flag

### Secret manager
**Definition**: Vault, K8s secrets, or cloud secret stores injecting
credentials at startup — the production source over env vars.
**Related**: Env var

### Settings
**Definition**: The typed, validated configuration object — one model,
one place where config is defined and checked.
**Related**: BaseSettings

### Startup validation
**Definition**: Validating all config when the service boots — the
mechanism behind fail fast.
**Related**: Fail fast

## Key Concepts Summary

### The precedence chain
- defaults < .env file < real environment < explicit args.
- Containers override via real env; tests via explicit args.

### The two rules
- Fail fast: invalid config raises at startup.
- No secrets in code: env/manager only, raise when missing.

### The config-as-dial idea
- Per-env values over per-env code.
- Feature flags with rollout, default off, removable via config.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. defaults < .env < env < args — ___
2. Raises at startup for bad config — ___
3. Vault/K8s/cloud store — ___
4. `APP_` namespacing — ___
5. Values differ, code identical — ___
6. A config dial gating a feature — ___
7. Gradual enablement by percent — ___
8. The typed validated config object — ___

**Answers:** 1-precedence, 2-fail fast, 3-secret manager, 4-env prefix,
5-per-env config, 6-feature flag, 7-rollout, 8-settings
