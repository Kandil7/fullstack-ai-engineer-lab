"""
Challenge 33: Security Essentials — Solution
============================================
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import sqlite3
from pathlib import Path

import yaml


# ============================================================
# Bronze: Password Store
# ============================================================

def hash_password(password: str, salt: bytes | None = None,
                  iterations: int = 100_000) -> tuple[bytes, bytes]:
    """PBKDF2-HMAC-SHA256 hash with a fresh random salt. O(iterations)."""
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )
    return digest, salt


def verify_password(password: str, digest: bytes, salt: bytes,
                    iterations: int = 100_000) -> bool:
    """Timing-safe verify (hmac.compare_digest). O(iterations)."""
    candidate = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )
    return hmac.compare_digest(candidate, digest)


# ============================================================
# Silver: Safe Query Layer
# ============================================================

class SafeStore:
    """sqlite3 store with parameterized queries only."""

    def __init__(self) -> None:
        self._conn = sqlite3.connect(":memory:")
        self._conn.execute(
            "CREATE TABLE users (id TEXT, name TEXT)"
        )

    def add(self, user_id: str, name: str) -> None:
        """Insert a user. O(1)."""
        self._conn.execute(
            "INSERT INTO users VALUES (?, ?)", (user_id, name)
        )
        self._conn.commit()

    def find(self, user_id: str) -> list[tuple]:
        """Parameterized SELECT; injection payloads return []. O(1)."""
        cursor = self._conn.execute(
            "SELECT name FROM users WHERE id = ?", (user_id,)
        )
        return cursor.fetchall()


# ============================================================
# Gold: Safe Config Loader
# ============================================================

ALLOWED = {"model", "batch_size", "retries"}
TYPES = {"model": str, "batch_size": int, "retries": int}


def load_config(path: Path) -> dict:
    """yaml.safe_load + whitelist + type checks. O(keys)."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("config must be a mapping")
    unknown = set(raw) - ALLOWED
    if unknown:
        raise ValueError(f"unknown keys: {sorted(unknown)}")
    for key, expected in TYPES.items():
        if key in raw and not isinstance(raw[key], expected):
            raise ValueError(
                f"{key} must be {expected.__name__}, got "
                f"{type(raw[key]).__name__}"
            )
    return raw


def is_safe_path(root: Path, filename: str) -> Path:
    """resolve() then is_relative_to(); raise ValueError on escape. O(1)."""
    candidate = (root / filename).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise ValueError("path escapes the root")
    return candidate
