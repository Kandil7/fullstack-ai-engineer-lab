# Docker for ML — Glossary 06

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Base Image | Docker | The starting image a Dockerfile extends |
| Build Stage | Docker | An intermediate stage for compilation |
| Cache Hit | Docker | A layer reused because its inputs did not change |
| Dockerfile | Docker | The recipe file for building an image |
| GPU Passthrough | Docker | Exposing host GPU to the container |
| Layer | Docker | One instruction's filesystem delta |
| Multi-Stage Build | Docker | Build in one stage, ship from another |
| Pin | Packaging | Exact dependency version |
| Runtime Image | Docker | The final, shipped image |
| Slim Image | Docker | A minimal base image (e.g. python:3.13-slim) |

## Detailed Definitions
### Base Image
**Definition**: The `FROM` image that a Dockerfile builds on.
**Related**: Layer, Dockerfile

### Build Stage
**Definition**: An intermediate stage (e.g. `AS builder`) that installs
toolchains and produces artifacts; not shipped.
**Related**: Multi-Stage Build

### Cache Hit
**Definition**: A layer not rebuilt because its context (base, files) is
unchanged; rare-changing steps first maximize hits.
**Related**: Layer

### Dockerfile
**Definition**: A text recipe: FROM, RUN, COPY, CMD instructions.
**Related**: Layer

### GPU Passthrough
**Definition**: Using a CUDA base image and `--gpus all` so the container uses
the host GPU.
**Related**: Base Image

### Layer
**Definition**: The delta one instruction produces; layers stack into an image.
**Related**: Cache Hit

### Multi-Stage Build
**Definition**: Multiple FROM stages; the runtime stage copies only artifacts
from the build stage, keeping the image small.
**Related**: Build Stage, Runtime Image

### Pin
**Definition**: An exact dependency version (`numpy==2.1.3`) for reproducibility.
**Related**: Runtime Image

### Runtime Image
**Definition**: The final image that actually ships and serves.
**Related**: Multi-Stage Build

### Slim Image
**Definition**: A minimal base like `python:3.13-slim`, shrinking attack surface
and startup.
**Related**: Base Image

## Key Concepts Summary
### Ordering Rules
- Base -> deps -> code (rare-changing first)
- Code changes never rebuild deps

### Build vs Ship
- Build stage: compilers, CUDA toolkit
- Runtime stage: artifacts only

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Layer — ___
2. Cache hit — ___
3. Multi-stage — ___
4. Pin — ___
5. Slim image — ___

**Answers:** 1-b, 2-c, 3-d, 4-e, 5-a where a=minimal base, b=instruction delta,
c=reused layer, d=build-then-copy pattern, e=exact version.
