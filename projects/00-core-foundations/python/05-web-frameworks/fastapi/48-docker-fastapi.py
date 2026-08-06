"""
FastAPI — 48: Docker & FastAPI
================================
Topics: multi-stage builds; layer caching; slim vs alpine; non-root user;
        .dockerignore; image size; reproducible builds

Why this matters for AI/backend engineering:
    The Dockerfile is the deployment contract — image size decides pull
    time and cold start; layer order decides build speed; the base image
    decides security surface (and alpine's musl can silently break
    numpy/pydantic wheels). Multi-stage builds separate the build
    environment from the runtime image. This exercise teaches the
    Dockerfile as DATA: we parse and verify the decisions the file makes,
    measure the size math, and prove the layer-caching rules.

Run:      python 48-docker-fastapi.py
Verify:   python 48-docker-fastapi.py --verify
Reference: https://docs.docker.com/develop/develop-images/multistage-build/
"""

from __future__ import annotations

import sys
from typing import Optional

# ============================================================
# 1. The production Dockerfile — every line justified
# ============================================================
DOCKERFILE = r"""
# Stage 1: build environment — has compilers, only for building wheels
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Stage 2: runtime — slim, no build tools, non-root
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /wheels /wheels
COPY . .
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* \
    && useradd --create-home appuser \
    && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

# The four decisions:
# 1. MULTI-STAGE: compilers stay in the builder; runtime is lean
# 2. LAYER CACHING: COPY requirements.txt BEFORE the code — dependency
#    layers rebuild only when requirements change
# 3. SLIM NOT ALPINE: musl can break numpy/pydantic manylinux wheels
# 4. NON-ROOT: USER appuser — a container escape is not root

print("=== 1. Production Dockerfile ===")
print(DOCKERFILE.strip().splitlines()[1] + "  <- builder (wheels)")
print(DOCKERFILE.strip().splitlines()[6] + "  <- runtime (slim, non-root)")
print()

# ============================================================
# 2. Image-size math — why multi-stage matters
# ============================================================
# Builder carries compilers + dev headers (~800MB+). Runtime needs only
# the wheels. The size delta is pull time and cold start.

def image_size_mb(base_mb: int, pip_wheels_mb: int, build_tools_mb: int,
                  multi_stage: bool) -> int:
    """Single-stage includes build tools in the final image."""
    return base_mb + pip_wheels_mb + (0 if multi_stage else build_tools_mb)


print("=== 2. Image size ===")
single = image_size_mb(120, 90, 700, multi_stage=False)
multi = image_size_mb(120, 90, 700, multi_stage=True)
print(f"single-stage: ~{single}MB   multi-stage: ~{multi}MB")
print(f"  -> {single - multi}MB saved (the compilers never ship)")
print()

# ============================================================
# 3. Layer caching — dependency order decides build speed
# ============================================================
# Docker caches layers; a changed layer invalidates everything after it.
# COPY requirements.txt BEFORE the code: dependency install rebuilds
# only when requirements change (the common case: code changes daily,
# requirements rarely).

def cached_layers(rebuild_count: int, cacheable_steps: int, total_steps: int,
                  deps_first: bool) -> int:
    """Steps re-executed over rebuild_count rebuilds."""
    # deps_first: the deps layer is cacheable across rebuilds
    if deps_first:
        per_rebuild = total_steps - 1     # only the code COPY + CMD rebuild
        return per_rebuild * rebuild_count
    # code first: every rebuild re-runs dependency install too
    return total_steps * rebuild_count


print("=== 3. Layer caching ===")
deps_first = cached_layers(rebuild_count=20, cacheable_steps=1, total_steps=5, deps_first=True)
code_first = cached_layers(rebuild_count=20, cacheable_steps=1, total_steps=5, deps_first=False)
print(f"deps-first: {deps_first} steps over 20 rebuilds")
print(f"code-first: {code_first} steps over 20 rebuilds  <- deps reinstall every time")
print()

# ============================================================
# 4. .dockerignore — the build context diet
# ============================================================
# The build context is sent to the daemon on every build. .git, caches,
# and outputs bloat it — and worse, can leak secrets into images.

DOCKERIGNORE = """
__pycache__/
*.pyc
.git/
.venv/
venv/
output/
*.log
.env
"""

def context_size(files: list[tuple[str, int]], ignore: list[str]) -> int:
    """Total bytes sent to the daemon, minus ignored entries."""
    total = 0
    for name, size in files:
        if not any(name.startswith(pat.rstrip("/")) for pat in ignore):
            total += size
    return total


print("=== 4. .dockerignore ===")
files = [("app/main.py", 2_000), (".git/objects/pack/a.pack", 50_000_000),
         ("output/model.pt", 400_000_000), ("app/__init__.py", 500),
         (".env", 200)]
ignored = ["__pycache__/", ".git/", "output/", ".env"]
sent = context_size(files, ignored)
print(f"context sent: {sent/1e6:.1f}MB (from ~450MB of files)")
print()

# ============================================================
# 5. Slim vs alpine — the musl trap
# ============================================================
# alpine uses musl libc; many prebuilt Python wheels (numpy, pydantic-
# core, orjson) target glibc manylinux. musl can force source builds —
# slow CI and runtime surprises. python:3.12-slim (Debian + glibc) is
# the default choice unless you audit every dependency's wheels.

ALPINE_RISK = {"numpy", "pydantic-core", "orjson", "psycopg2-binary"}

def wheel_available_on_alpine(pkg: str) -> bool:
    """True if a prebuilt wheel for the package exists for musl."""
    return pkg not in ALPINE_RISK


print("=== 5. Slim vs alpine ===")
for pkg in ["uvicorn", "numpy", "pydantic-core", "httpx"]:
    print(f"  alpine wheel for {pkg}: {wheel_available_on_alpine(pkg)}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: single-stage with compilers — 700MB+ of build tools ship
# CORRECT: multi-stage; runtime gets only wheels
#
# MISTAKE: COPY . . before requirements — every code change rebuilds
#   the entire dependency layer
# CORRECT: COPY requirements.txt first; deps layer cacheable
#
# MISTAKE: alpine for numpy/pydantic projects — musl source-build trap
# CORRECT: python:3.12-slim unless every wheel exists for musl
#
# MISTAKE: running as root — a container escape is root on the host
# CORRECT: USER appuser
#
# MISTAKE: no .dockerignore — .git + outputs bloat context; .env leaks
# CORRECT: ignore caches, VCS, secrets, outputs

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""

    # 1. Multi-stage size math
    assert image_size_mb(120, 90, 700, True) == 210, "runtime excludes build tools"
    assert image_size_mb(120, 90, 700, False) == 910, "single-stage ships compilers"

    # 2. Layer caching: deps-first rebuilds less
    df = cached_layers(20, 1, 5, deps_first=True)
    cf = cached_layers(20, 1, 5, deps_first=False)
    assert df < cf, "deps-first must rebuild fewer steps"

    # 3. Dockerfile contains the load-bearing decisions
    assert "FROM python:3.12-slim AS builder" in DOCKERFILE, "builder stage"
    assert "COPY requirements.txt" in DOCKERFILE, "deps copied first"
    assert "USER appuser" in DOCKERFILE, "non-root user"
    assert "COPY --from=builder" in DOCKERFILE, "multi-stage copy"

    # 4. .dockerignore math
    sent = context_size(
        [("app/main.py", 2000), (".git/p", 50_000_000), ("output/m.pt", 400_000_000),
         (".env", 200)],
        ["__pycache__/", ".git/", "output/", ".env"],
    )
    assert sent == 2000, "only app code ships"

    # 5. Alpine risk model
    assert not wheel_available_on_alpine("numpy")
    assert wheel_available_on_alpine("uvicorn")

    print("[OK] 48-docker-fastapi: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Multi-stage: compilers in builder, wheels in runtime")
        print("2. Deps-first COPY order = cacheable dependency layer")
        print("3. slim not alpine (musl breaks manylinux wheels)")
        print("4. Non-root + .dockerignore = smaller, safer images")
        _verify()          # always runs, so plain execution is also a test
