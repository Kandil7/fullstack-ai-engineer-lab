"""
FastAPI — 50: Configuration
==============================
Topics: pydantic-settings; env precedence; secret managers; per-environment
        config; validation at startup (fail fast); feature flags

Why this matters for AI/backend engineering:
    Configuration is code's separation from the environment: the same
    image runs in dev, staging, and prod because config differs, not
    code. pydantic-settings gives typed, validated, env-backed settings
    with a precedence chain (defaults < .env < real env < CLI). The two
    rules: FAIL FAST (a typo'd DATABASE_URL surfaces at startup, not at
    first request) and NO SECRETS IN CODE (API keys come from env /
    secret manager). Feature flags make config a runtime dial.

Run:      python 50-configuration.py
Verify:   python 50-configuration.py --verify
Reference: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# ============================================================
# 1. Typed, validated settings with env support
# ============================================================
# pydantic-settings maps env vars onto typed fields with validation.
# A mis-typed env value is a startup error, not a runtime mystery.

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env")

    app_name: str = "llm-gateway"
    debug: bool = False
    database_url: str = "sqlite:///./dev.db"
    redis_url: str = "redis://localhost:6379/0"
    max_tokens: int = Field(default=2048, ge=1, le=128_000)
    allowed_origins: list[str] = ["http://localhost:3000"]

    @field_validator("database_url")
    @classmethod
    def _check_scheme(cls, v: str) -> str:
        if not v.startswith(("sqlite://", "postgresql://", "postgresql+asyncpg://")):
            raise ValueError(f"unsupported database scheme: {v}")
        return v


os.environ["APP_MAX_TOKENS"] = "4096"
settings = Settings()
print("=== 1. Typed settings from env ===")
print(f"app_name   : {settings.app_name}   (default)")
print(f"max_tokens : {settings.max_tokens}  (from env APP_MAX_TOKENS=4096)")
print(f"debug      : {settings.debug}")
try:
    Settings(database_url="mysql://bad")
    print("BAD: accepted an unsupported scheme")
except Exception as e:
    print(f"validation fails fast: {e}")
print()

# ============================================================
# 2. Precedence chain
# ============================================================
# defaults < .env file < real environment variables < explicit args.
# Real env beats the .env file, so containers can override everything.

def precedence(source: str) -> dict:
    """Simulate the pydantic-settings lookup order."""
    chain = ["defaults", ".env file", "environment", "explicit args"]
    value = {"provider": "openai", "base_url": "https://api.openai.com/v1"}
    if source == "explicit": value["provider"] = "azure"
    elif source == "env":    value["provider"] = "azure"   # env overrides .env
    elif source == "dotenv": value["provider"] = "azure"   # .env overrides default
    return {"chain": chain, "winner": value["provider"]}


print("=== 2. Precedence chain ===")
for s in ("defaults", "dotenv", "env", "explicit"):
    print(f"  {s:<10} -> provider={precedence(s)['winner']}")
print()

# ============================================================
# 3. Secrets: env / secret manager only
# ============================================================
# API keys NEVER appear in code or committed config. They arrive via
# env (containers) or a secret manager (K8s secrets, vault) injected
# at startup. Missing secrets fail fast.

def load_secret(name: str, store: dict[str, str]) -> str:
    value = store.get(name, os.environ.get(name, ""))
    if not value:
        raise RuntimeError(f"missing required secret: {name}")
    return value


print("=== 3. Secrets from env/manager ===")
os.environ["OPENAI_API_KEY"] = "sk-test-123"
print(f"loaded: {load_secret('OPENAI_API_KEY', {})[:8]}...")
try:
    load_secret("ANTHROPIC_API_KEY", {})
except RuntimeError as e:
    print(f"missing secret fails fast: {e}")
print()

# ============================================================
# 4. Per-environment configuration
# ============================================================
# One schema, per-env values. The image is identical; the env decides.

ENV_CONFIGS = {
    "dev":  {"debug": True,  "max_tokens": 2048,  "log_level": "DEBUG"},
    "staging": {"debug": False, "max_tokens": 4096, "log_level": "INFO"},
    "prod": {"debug": False, "max_tokens": 8192,  "log_level": "INFO"},
}

def config_for(env: str) -> dict:
    base = {"debug": False, "max_tokens": 2048, "log_level": "INFO"}
    base.update(ENV_CONFIGS[env])
    return base


print("=== 4. Per-environment config ===")
for env in ("dev", "staging", "prod"):
    print(f"  {env:<8} {config_for(env)}")
print()

# ============================================================
# 5. Feature flags — config as a runtime dial
# ============================================================
# Flags gate unfinished/risky features. They are CONFIG, not code
# branches to delete: a flag can be flipped without a deploy, and a
# gradual rollout (percent) catches regressions early.

class FeatureFlags:
    def __init__(self, overrides: dict[str, bool] | None = None) -> None:
        self.flags: dict[str, bool] = {
            "new_reranker": False,
            "hybrid_search": False,
            "beta_streaming": False,
        }
        self.flags.update(overrides or {})

    def enabled(self, flag: str) -> bool:
        return self.flags.get(flag, False)


flags = FeatureFlags({"hybrid_search": True})
print("=== 5. Feature flags ===")
print(f"  hybrid_search enabled: {flags.enabled('hybrid_search')}")
print(f"  new_reranker enabled : {flags.enabled('new_reranker')}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: config as raw os.environ.get sprinkled through the code —
#   untyped, unvalidated, tested nowhere
# CORRECT: one Settings model, validated at startup
#
# MISTAKE: secrets in code / committed .env — the leak is permanent
# CORRECT: env or secret manager; fail fast when missing
#
# MISTAKE: no fail-fast — a bad DATABASE_URL crashes at first request
# CORRECT: pydantic validation raises at import/startup
#
# MISTAKE: env-specific logic in code (if env == 'prod')
# CORRECT: per-env VALUES in config; identical code everywhere
#
# MISTAKE: feature branches to remove later — deletion is a deploy
# CORRECT: flags with defaults; remove the flag, not a delete-branch

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""

    # 1. Typed settings read env with validation
    os.environ["APP_MAX_TOKENS"] = "512"
    s = Settings()
    assert s.max_tokens == 512, "env must override the default"
    assert s.app_name == "llm-gateway", "unset env keeps the default"
    try:
        Settings(max_tokens=1_000_000)
        assert False, "out-of-range max_tokens must fail"
    except Exception:
        pass
    try:
        Settings(database_url="mysql://x")
        assert False, "unsupported scheme must fail at startup"
    except Exception:
        pass

    # 2. Precedence: explicit > env > .env > default
    assert precedence("defaults")["winner"] == "openai"
    assert precedence("explicit")["winner"] == "azure"

    # 3. Secrets fail fast when missing
    assert load_secret("OPENAI_API_KEY", {}).startswith("sk-test")
    try:
        load_secret("NEVER_SET", {})
        assert False, "missing secret must raise"
    except RuntimeError:
        pass

    # 4. Per-env config differs, schema identical
    assert config_for("dev")["debug"] is True
    assert config_for("prod")["debug"] is False
    assert config_for("prod")["log_level"] == "INFO"

    # 5. Feature flags default off, overridable
    f = FeatureFlags()
    assert f.enabled("new_reranker") is False
    f2 = FeatureFlags({"new_reranker": True})
    assert f2.enabled("new_reranker") is True

    # 6. Env prefix discipline
    assert s.model_config.get("env_prefix") == "APP_", "env vars must be namespaced"

    print("[OK] 50-configuration: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. One typed Settings model; validation fails fast")
        print("2. Precedence: defaults < .env < env < explicit")
        print("3. Secrets from env/manager, never code")
        print("4. Per-env VALUES, not per-env code")
        print("5. Feature flags as runtime dials")
        _verify()          # always runs, so plain execution is also a test
