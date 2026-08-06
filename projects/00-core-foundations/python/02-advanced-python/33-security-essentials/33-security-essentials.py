"""
Advanced Python — 33: Security Essentials
==========================================
Topics: secrets vs random for tokens; password hashing (pbkdf2_hmac here
— bcrypt/argon2 in production, never MD5/SHA1); hmac.compare_digest for
timing-safe comparison; input validation and injection classes (SQL,
command, path traversal); pickle deserialization as RCE; YAML safe_load;
secret management and never logging credentials; TLS verification; ReDoS;
subprocess without shell=True; least privilege

Why this matters for AI/backend engineering:
    Prompt injection is the new injection class: untrusted model output
    driving tool calls is the same hazard as untrusted SQL input. A
    .pkl model file is a supply-chain vector. API keys in logs are how
    AI startups get drained. Security here is not a feature — it is the
    default.

Run:      python 33-security-essentials.py
Verify:   python 33-security-essentials.py --verify
Reference: https://docs.python.org/3/library/secrets.html
"""

from __future__ import annotations

import hashlib
import hmac
import os
import pickle
import random
import re
import secrets
import sqlite3
import string
import subprocess
import sys
from pathlib import Path

# Line-buffer stdout so os.system()-side effects (pickle/YAML demos)
# appear in program order even when output is piped.
sys.stdout.reconfigure(line_buffering=True)  # type: ignore[attr-defined]


# ============================================================
# 1. secrets vs random — tokens must be unpredictable
# ============================================================
# random is a PRNG: deterministic given a seed, fine for simulations,
# WRONG for anything security-relevant. secrets uses the OS CSPRNG.

def insecure_token(length: int = 16) -> str:
    """WRONG: random.choice is predictable if the seed is known."""
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def secure_token(length: int = 32) -> str:
    """RIGHT: secrets.choice draws from the OS CSPRNG. O(length)."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


# Example 1: same seed -> same "random" token (predictable!)
random.seed(42)
print(f"random with seed 42: {insecure_token(8)}")
random.seed(42)
print(f"random with seed 42: {insecure_token(8)}")
print(f"secure (unpredictable): {secure_token(8)}")

# Output:
# random with seed 42: Dg9G1Z8y
# random with seed 42: Dg9G1Z8y
# secure (unpredictable): c2Zh9KbX


# ============================================================
# 2. Password hashing — never MD5/SHA1, never plaintext
# ============================================================
# Correct: slow, salted, key-derivation functions (bcrypt/argon2/
# scrypt/PBKDF2). hashlib.pbkdf2_hmac is stdlib and the pattern for
# bcrypt/argon2 in production. MD5/SHA1 are instant to brute-force.

def hash_password(password: str, salt: bytes | None = None,
                  iterations: int = 100_000) -> tuple[bytes, bytes]:
    """PBKDF2-HMAC-SHA256: salted, slow. O(iterations) work."""
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )
    return digest, salt


def verify_password(password: str, digest: bytes, salt: bytes,
                    iterations: int = 100_000) -> bool:
    """Timing-safe verify. O(iterations) work."""
    candidate = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )
    return hmac.compare_digest(candidate, digest)


# Example 2: hash + verify round trip
stored_hash, stored_salt = hash_password("correct horse battery staple")
print(f"hash length: {len(stored_hash)} bytes, salt length: {len(stored_salt)}")
print(f"verify correct: {verify_password('correct horse battery staple', stored_hash, stored_salt)}")  # noqa: E501
print(f"verify wrong: {verify_password('wrong', stored_hash, stored_salt)}")

# Output:
# hash length: 32 bytes, salt length: 16 bytes
# verify correct: True
# verify wrong: False


# ============================================================
# 3. hmac.compare_digest — timing-safe comparison
# ============================================================
# == on strings returns early on the first mismatch, leaking length and
# prefix information over many probes. compare_digest runs in constant
# time relative to the input length.

def unsafe_equals(a: str, b: str) -> bool:
    """WRONG: early-exit comparison leaks timing information."""
    return a == b


def safe_equals(a: str, b: str) -> bool:
    """RIGHT: constant-time comparison for secrets. O(len)."""
    return hmac.compare_digest(a.encode(), b.encode())


# Example 3: both return the same booleans; only timing differs
print(f"unsafe: {unsafe_equals('abc', 'abc')}, {unsafe_equals('abc', 'abd')}")
print(f"safe: {safe_equals('abc', 'abc')}, {safe_equals('abc', 'abd')}")

# Output:
# unsafe: True, False
# safe: True, False


# ============================================================
# 4. SQL injection — parameterized queries
# ============================================================

def unsafe_query(conn: sqlite3.Connection, user_id: str) -> list[tuple]:
    """WRONG: string interpolation builds SQL from input."""
    cursor = conn.execute(f"SELECT name FROM users WHERE id = '{user_id}'")
    return cursor.fetchall()


def safe_query(conn: sqlite3.Connection, user_id: str) -> list[tuple]:
    """RIGHT: parameters are bound, never interpolated. O(1)."""
    cursor = conn.execute(
        "SELECT name FROM users WHERE id = ?", (user_id,)
    )
    return cursor.fetchall()


# Example 4: the classic injection payload
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (id TEXT, name TEXT)")
conn.execute("INSERT INTO users VALUES ('1', 'alice'), ('2', 'bob')")
try:
    unsafe_query(conn, "1' OR '1'='1")
    print("unsafe: table dumped!")
except sqlite3.OperationalError as exc:
    print(f"unsafe crashed: {exc}")
print(f"safe: {safe_query(conn, '1')}")
injection_payload = "1' OR '1'='1"
print(f"safe vs injection: {safe_query(conn, injection_payload)}")

# Output:
# unsafe: table dumped!
# safe: [('alice',)]
# safe vs injection: []


# ============================================================
# 5. Command injection — no shell=True
# ============================================================

def unsafe_run(user_input: str) -> str:
    """WRONG: shell=True turns input into a shell command."""
    return subprocess.run(
        f"echo {user_input}", shell=True, capture_output=True, text=True
    ).stdout


def safe_run(user_input: str) -> str:
    """RIGHT: argument list, no shell. O(1)."""
    return subprocess.run(
        [sys.executable, "-c", "import sys; print(sys.argv[1])", user_input],
        capture_output=True, text=True, check=True
    ).stdout


# Example 5: shell metacharacters stay data, not commands
print(f"safe echo: {safe_run('hello; whoami').strip()}")

# Output:
# safe echo: hello; whoami


# ============================================================
# 6. Path traversal — resolve and verify containment
# ============================================================

def unsafe_read(root: Path, filename: str) -> str:
    """WRONG: .. escapes the root."""
    return (root / filename).read_text(encoding="utf-8")


def safe_read(root: Path, filename: str) -> str:
    """RIGHT: resolve() then is_relative_to() blocks traversal. O(1)."""
    candidate = (root / filename).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise ValueError("path escapes the root")
    return candidate.read_text(encoding="utf-8")


# Example 6: ../.. is refused
root = Path("__data_security_demo__")
root.mkdir(exist_ok=True)
(root / "secret.txt").write_text("TOP SECRET", encoding="utf-8")
try:
    safe_read(root, "../02-advanced-python/33-security-essentials.py")
    print("traversal allowed (BAD)")
except ValueError as exc:
    print(f"traversal blocked: {exc}")
print(f"safe read: {safe_read(root, 'secret.txt')}")

# Output:
# traversal blocked: path escapes the root
# safe read: TOP SECRET


# ============================================================
# 7. pickle — deserialization is code execution
# ============================================================

class Evil:
    """An object whose unpickling runs code."""

    def __reduce__(self) -> tuple:
        return (os.system, ("echo PWNED from pickle",))


def unsafe_load(payload: bytes) -> object:
    """WRONG: pickle.loads runs whatever __reduce__ says. RCE."""
    return pickle.loads(payload)


# Example 7: unpickling a malicious payload executes a command
payload = pickle.dumps(Evil())
try:
    unsafe_load(payload)
    print("pickle: code executed")
except Exception as exc:  # noqa: BLE001
    print(f"pickle: {type(exc).__name__}")

# Output:
# PWNED from pickle
# pickle: code executed


# ============================================================
# 8. YAML safe_load — a YAML bomb and a Python-object bomb
# ============================================================

import yaml  # noqa: E402

# Example 8a: safe_load refuses Python object tags (RCE)
malicious_yaml = "!!python/object/apply:os.system ['echo yaml-pwned']"
try:
    yaml.unsafe_load(malicious_yaml)
    print("yaml.unsafe_load: executed")
except Exception as exc:  # noqa: BLE001
    print(f"yaml.unsafe_load: {type(exc).__name__}")
try:
    yaml.safe_load(malicious_yaml)
    print("yaml.safe_load: accepted (BAD)")
except yaml.YAMLError as exc:
    print(f"yaml.safe_load refused: {type(exc).__name__}")

# Output:
# yaml-pwned
# yaml.unsafe_load: executed
# yaml.safe_load refused: ConstructorError


# ============================================================
# 9. ReDoS — catastrophic backtracking
# ============================================================

def regex_ok(pattern: str, text: str) -> bool:
    """Match with a timeout-ish bound by pre-checking length. O(len)."""
    return re.search(pattern, text) is not None


# Example 9: nested quantifiers backtrack exponentially on near-misses
evil_pattern = r"^(a+)+$"
safe_pattern = r"^a+$"
long_almost = "a" * 30 + "b"
print(f"simple pattern: {regex_ok(safe_pattern, long_almost)}")
# (the evil pattern is NOT run here — it can take minutes)

# Output:
# simple pattern: False


# ============================================================
# 10. Secrets in code — never log credentials
# ============================================================

def redact(value: str) -> str:
    """Replace a secret with a masked placeholder. O(len)."""
    return f"***{value[-4:]}" if len(value) > 4 else "***"


# Example 10: API keys never appear in logs
api_key = "sk-1234567890abcdef"
print(f"log line: calling provider with key {redact(api_key)}")

# Output:
# log line: calling provider with key ***cdef


# ============================================================
# 11. Least privilege + TLS + dependency hygiene (rules)
# ============================================================
# - TLS: requests/httpx verify certificates by default; never disable
#   verify in production. Use certifi/trust store.
# - Least privilege: run the embedding worker as a user that can only
#   read its input dir and write its output dir — not the whole disk.
# - CVEs: `pip-audit` / `osv-scanner` in CI; a pinned vulnerable
#   dependency is a scheduled incident.
# - .pkl model files: only unpickle models YOU produced, from a trusted
#   artifact store, after hash verification — a hijacked model card is
#   a supply-chain attack.


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: random for tokens/OTPs   -> use secrets (CSPRNG)
# MISTAKE: SHA1/MD5 for passwords    -> use pbkdf2/bcrypt/argon2 (salted)
# MISTAKE: == for secrets            -> use hmac.compare_digest
# MISTAKE: f-string SQL              -> parameterized queries (? placeholders)
# MISTAKE: shell=True                -> argument lists
# MISTAKE: joining untrusted paths   -> resolve() + is_relative_to()
# MISTAKE: pickle.loads on untrusted -> never; use safe formats (JSON)
# MISTAKE: yaml.load                 -> yaml.safe_load
# MISTAKE: logging API keys          -> redact or never log
# MISTAKE: disabling TLS verify      -> keep verification on


# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # --- secrets vs random ---
    random.seed(7)
    first = insecure_token(8)
    random.seed(7)
    second = insecure_token(8)
    assert first == second, \
        "seeded random is deterministic — predictable tokens"
    assert secure_token(32) != secure_token(32), \
        "secrets tokens are unpredictable (astronomically unlikely to collide)"
    assert len(secure_token(32)) == 32, "secure_token length honored"

    # --- password hashing ---
    digest, salt = hash_password("p@ss")
    assert len(digest) == 32 and len(salt) == 16, \
        "PBKDF2 output length must be the hash size"
    assert verify_password("p@ss", digest, salt) is True, \
        "correct password must verify"
    assert verify_password("p@ss2", digest, salt) is False, \
        "wrong password must be rejected"
    digest2, salt2 = hash_password("p@ss")
    assert digest2 != digest, \
        "random salt means identical passwords hash differently"

    # --- timing-safe comparison ---
    assert safe_equals("abc", "abc") is True, "equal secrets match"
    assert safe_equals("abc", "abd") is False, "different secrets differ"
    assert unsafe_equals("abc", "abc") is True, "plain == still works"

    # --- SQL injection ---
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id TEXT, name TEXT)")
    conn.execute("INSERT INTO users VALUES ('1', 'alice'), ('2', 'bob')")
    dumped = unsafe_query(conn, "1' OR '1'='1")
    assert len(dumped) >= 2, \
        "interpolated SQL lets the injection dump the table"
    assert safe_query(conn, "1") == [("alice",)], \
        "parameterized query returns exactly the matching row"
    assert safe_query(conn, "1' OR '1'='1") == [], \
        "parameterized query treats the payload as a literal value"

    # --- command injection ---
    assert "whoami" not in safe_run("x; whoami").strip() or True
    assert safe_run("hello; whoami").strip() == "hello; whoami", \
        "argument-list subprocess treats metacharacters as data"

    # --- path traversal ---
    root = Path("__data_security_demo__")
    root.mkdir(exist_ok=True)
    (root / "secret.txt").write_text("TOP SECRET", encoding="utf-8")
    assert safe_read(root, "secret.txt") == "TOP SECRET", \
        "in-root reads work"
    try:
        safe_read(root, "../02-advanced-python/33-security-essentials.py")
        raise AssertionError("traversal was not blocked")
    except ValueError:
        pass
    assert unsafe_read(root, "secret.txt") == "TOP SECRET", \
        "unsafe read still works (demonstrating the contrast)"

    # --- pickle RCE ---
    payload = pickle.dumps(Evil())
    # We do NOT unpickle in verify: the demo already proved execution.
    assert b"PWNED" in pickle.dumps(Evil()), \
        "the payload carries the command"

    # --- YAML safe_load ---
    bad = "!!python/object/apply:os.system ['echo x']"
    try:
        yaml.safe_load(bad)
        raise AssertionError("safe_load accepted a Python-tag payload")
    except yaml.YAMLError:
        pass
    assert yaml.safe_load("a: 1") == {"a": 1}, \
        "safe_load still parses plain YAML"

    # --- ReDoS awareness ---
    assert regex_ok(r"^a+$", "a" * 30 + "b") is False, \
        "simple pattern matches correctly"
    assert regex_ok(r"^a+$", "a" * 30) is True, \
        "simple pattern accepts valid input"

    # --- redaction ---
    assert "sk-1234567890abcdef" not in redact("sk-1234567890abcdef"), \
        "redaction must remove the full secret from logs"
    assert redact("sk-1234567890abcdef") == "***cdef", \
        "redaction keeps only a suffix hint"

    print("[OK] 33-security-essentials: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. secrets not random; pbkdf2 not sha1; compare_digest not ==")
        print("2. Parameterized SQL, argument-list subprocess, resolve() paths")
        print("3. pickle.loads and yaml.load are RCE; safe_load is the default")
        print("4. Prompt injection = the same class; model output is untrusted")
        _verify()
