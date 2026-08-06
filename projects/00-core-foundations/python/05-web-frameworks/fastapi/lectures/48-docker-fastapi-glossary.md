# Docker & FastAPI — Glossary 48

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Alpine | Base image | musl-libc Linux — small but breaks many wheels |
| Build context | Docker | The files sent to the daemon for a build |
| Builder stage | Multi-stage | The stage that compiles/assembles artifacts |
| Dockerfile | Docker | The layered deployment contract |
| glibc | Libc | The C library most manylinux wheels target |
| Layer | Docker | One Dockerfile instruction; cached units |
| Layer caching | Docker | Unchanged layers are reused across builds |
| musl | Libc | Alpine's C library — source-build trap for wheels |
| Multi-stage | Pattern | Build artifacts in one stage, runtime in another |
| Non-root | Security | Running the container as an unprivileged user |
| Runtime stage | Multi-stage | The slim stage shipping only what runs |
| Slim | Base image | Debian+glibc minimal Python image |
| .dockerignore | Docker | Excludes files from the build context |
| USER | Docker | The Dockerfile instruction setting the runtime user |

## Detailed Definitions

### Alpine
**Definition**: A tiny Linux base using musl libc — small images, but
prebuilt Python wheels (numpy, pydantic-core) targeting glibc may fail.
**Related**: musl

### Build context
**Definition**: The directory uploaded to the Docker daemon for a build —
bloated by caches/VCS, dangerous when it contains secrets.
**Related**: .dockerignore

### Builder stage
**Definition**: The first multi-stage stage with compilers and build
tools; its only job is producing wheels to copy forward.
**Related**: Multi-stage

### Dockerfile
**Definition**: The ordered instruction list Docker executes as layers —
the deployment contract, where caching and size are decided.
**Related**: Layer

### glibc
**Definition**: The GNU C library that manylinux wheels are built
against — the reason Debian-based slim is the safe default.
**Related**: Slim

### Layer
**Definition**: The filesystem diff of one Dockerfile instruction —
cached and reused when unchanged.
**Related**: Layer caching

### Layer caching
**Definition**: Docker reusing unchanged layers; ordering instructions so
the expensive (dependency) layer changes rarely is the caching strategy.
**Related**: Layer

### musl
**Definition**: Alpine's C library — lighter than glibc, but wheels built
for glibc may not run, forcing source builds.
**Related**: Alpine

### Multi-stage
**Definition**: Building artifacts in one stage and copying only them
into a lean runtime stage — compilers never ship.
**Related**: Builder stage

### Non-root
**Definition**: Running the container as `appuser` instead of root — a
container escape is then an unprivileged user, not root on the host.
**Related**: USER

### Runtime stage
**Definition**: The final multi-stage image containing only what executes
— code, wheels, runtime dependencies.
**Related**: Builder stage

### Slim
**Definition**: `python:3.12-slim` — Debian-based, glibc, minimal
packages: the default for native-wheel Python projects.
**Related**: glibc

### .dockerignore
**Definition**: The ignore list for the build context — caches, VCS,
outputs, and `.env` secrets never reach the daemon or image.
**Related**: Build context

### USER
**Definition**: The Dockerfile instruction switching the runtime user —
the mechanism for non-root execution.
**Related**: Non-root

## Key Concepts Summary

### The five knobs
- Multi-stage: size.
- COPY order: caching speed.
- slim vs alpine: wheel compatibility.
- USER: security.
- .dockerignore: context hygiene.

### The cost math
- Build tools in runtime: +hundreds of MB.
- Deps reinstall per commit: minutes of CI.
- musl source builds: hours of CI.
- Root runtime: host compromise.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Compilers stay in one stage — ___
2. Unchanged layers are reused — ___
3. Deps copied before code — ___
4. Alpine's C library — ___
5. Debian-based minimal Python image — ___
6. Runtime as unprivileged user — ___
7. Excludes files from the context — ___
8. The files sent to the daemon — ___

**Answers:** 1-multi-stage, 2-layer caching, 3-layer ordering, 4-musl,
5-slim, 6-non-root/USER, 7-.dockerignore, 8-build context
