# FastAPI — 48: Docker & FastAPI

## Topic Overview

The Dockerfile is the deployment contract. Four decisions dominate:
**multi-stage builds** (compilers stay in the builder, only wheels ship),
**layer ordering** (dependencies before code, so the expensive layer is
cacheable), **base image choice** (slim, not alpine — musl silently
breaks many manylinux wheels like numpy/pydantic-core), and **non-root
runtime** (a container escape must not be root on the host). A
`.dockerignore` keeps the build context lean and secrets out of images.
Together these decide build speed, image size, pull time, cold start, and
security surface.

The mental model: the Dockerfile is a layered diff — every line is a
layer, and order is caching policy. Cost is measured in megabytes and
rebuilds.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write a multi-stage Dockerfile for a FastAPI service.
2. Order COPY instructions to maximize layer caching.
3. Choose slim over alpine and justify it.
4. Run as a non-root user and size the context with .dockerignore.
5. Estimate image-size and rebuild-cost impact.

## Prerequisites

| Need | Where |
|---|---|
| FastAPI app structure | `01-introduction.py` |
| Deployment context | `46`, `47` lectures |
| ASGI server | `49-uvicorn-gunicorn-lecture.md` (next) |

---

## 1. Multi-stage builds

```dockerfile
FROM python:3.12-slim AS builder   # has compilers — only makes wheels
RUN pip wheel --wheel-dir /wheels -r requirements.txt
FROM python:3.12-slim              # runtime — no build tools
COPY --from=builder /wheels /wheels
RUN pip install --no-index --find-links=/wheels /wheels/*
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

The builder compiles/assembles; the runtime inherits only the artifacts.
Compilers, dev headers, and build caches (~700MB+) never ship — image
size drops, pull time drops, attack surface drops.

## 2. Layer caching

Docker caches layers; a changed layer invalidates everything after it.
`COPY requirements.txt .` **before** `COPY . .` means the dependency
install layer rebuilds only when requirements change — which is rare
compared to code. Code-first ordering reinstalls every dependency on
every commit: minutes of CI per push, for free.

## 3. Slim vs alpine

Alpine is small because it uses **musl** libc; most prebuilt Python
wheels target glibc manylinux. A numpy/pydantic project on alpine often
falls back to source builds — slow CI, surprising runtime behavior, and
silent failures. `python:3.12-slim` (Debian + glibc) is the default.
Alpine is defensible only when every dependency has a musl wheel.

## 4. Non-root + .dockerignore

- `USER appuser` (created in the Dockerfile): a container escape is then
  an unprivileged user, not root.
- `.dockerignore` (`.git/`, `__pycache__/`, `output/`, `.env`): the build
  context is uploaded on every build — caches bloat it, and a stray
  `.env` is a secret leak baked into the image.

## Common Mistakes to Avoid

### Mistake 1: Single-stage builds
```python
# WRONG - compilers + headers ship in the runtime image
# CORRECT - multi-stage; runtime gets wheels only
```

### Mistake 2: `COPY . .` before requirements
```python
# WRONG - every code commit reinstalls all dependencies
# CORRECT - requirements first; code second
```

### Mistake 3: Alpine for native-wheel projects
```python
# WRONG - musl forces source builds for numpy/pydantic-core
# CORRECT - slim unless every wheel exists for musl
```

### Mistake 4: Root runtime user
```python
# WRONG - container escape = root on host
# CORRECT - USER appuser
```

### Mistake 5: No .dockerignore
```python
# WRONG - .git + outputs bloat context; .env leaks secrets
# CORRECT - ignore caches, VCS, outputs, secrets
```

## Best Practices

1. Multi-stage: builder wheels, slim runtime.
2. Order COPY: requirements before code.
3. Default to `python:3.12-slim`; audit before alpine.
4. Non-root user; smallest privilege.
5. `.dockerignore` everything non-essential.
6. Pin base image tags; rebuild deterministically.
7. Scan the image for CVEs in CI.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| Build tools in runtime | +700MB image | multi-stage |
| Deps reinstall per commit | minutes CI | deps-first COPY |
| Alpine source builds | hours CI | slim |
| Root runtime | host compromise | USER appuser |
| Fat context | slow builds + leaks | .dockerignore |

Every decision is a cost line. Multi-stage, order, base, user, and ignore
file are the five knobs.

## AI Engineering Relevance

**Where this shows up:** serving images with model weights, GPU images,
and the CI pipeline that rebuilds them on every commit.

| Concept here | Used for |
|---|---|
| multi-stage | building wheels without shipping compilers |
| layer caching | fast CI for a service changing daily |
| slim vs alpine | numpy/pydantic/torch wheels working |
| non-root | GPU workers escaping to an unprivileged user |
| .dockerignore | keeping model weights out of the context |

**Scale note:** a 100MB image pulls in seconds; a 900MB image slows every
cold start and rollout — at fleet scale that is real cost and real
latency.

## Practice Exercises

### Exercise 1: Size math  (Difficulty: Easy)
Compute single vs multi-stage sizes; assert the delta.

### Exercise 2: Layer order  (Difficulty: Easy)
Compare rebuild steps for deps-first vs code-first; assert fewer.

### Exercise 3: Dockerfile review  (Difficulty: Medium)
Parse a Dockerfile; assert it has builder, deps-first COPY, non-root.

### Exercise 4: .dockerignore  (Difficulty: Medium)
Given a file list, compute the shipped context; assert secrets excluded.

### Exercise 5: Alpine audit  (Difficulty: Medium)
Given a dependency list, assert which packages break on musl.

### Exercise 6: Full image pipeline  (Difficulty: Hard)
Model build → scan → push → deploy with image sizes; assert the
multi-stage variant reaches production with the smaller image.

## Summary

| Concept | Description |
|---|---|
| multi-stage | compilers in builder, artifacts in runtime |
| layer caching | deps-first COPY order |
| slim vs alpine | glibc wheels vs musl source builds |
| non-root | USER appuser |
| .dockerignore | lean context, no secret leaks |

The Dockerfile is deployment math: megabytes and rebuilds. Multi-stage
for size, order for caching, slim for wheels, non-root for safety,
ignore-file for hygiene.

## Quick Reference

| Task | Idiom |
|---|---|
| Build wheels | builder stage `pip wheel --wheel-dir /wheels` |
| Copy artifacts | `COPY --from=builder /wheels /wheels` |
| Deps cache | `COPY requirements.txt .` first |
| Non-root | `RUN useradd ... && USER appuser` |
| Context diet | `.dockerignore` with .git, caches, .env |

## Next Steps

Next: **[49 — Uvicorn & Gunicorn](49-uvicorn-gunicorn-lecture.md)** — the
command that actually runs the image.

Continues in: **[50 — Configuration](50-configuration-lecture.md)** — the
env vars the image needs.

Official docs:
- Docker multi-stage: https://docs.docker.com/develop/develop-images/multistage-build/
- Best practices: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
