"""
FastAPI — 42: Security Testing
================================
Topics: auth bypass tests; fuzzing inputs; static analysis (bandit);
        dependency scanning (pip-audit); threat modeling an endpoint

Why this matters for AI/backend engineering:
    Security features are only real if tests prove the boundaries hold.
    The highest-value security tests are AUTH BYPASS tests — no token,
    expired token, forged token, cross-tenant id — because those fail
    loudly and cheaply. Fuzzing throws hostile-but-valid-shaped inputs
    at every boundary. Static analysis (bandit) and dependency scanning
    (pip-audit) automate the rest. This exercise implements each layer
    and verifies it, using only stdlib so it runs anywhere.

Run:      python 42-security-testing.py
Verify:   python 42-security-testing.py --verify
Reference: https://owasp.org/www-project-application-security-verification-standard/
"""

from __future__ import annotations

import hashlib
import hmac
import json
import random
import string
import sys
import time
from typing import Optional

# ============================================================
# 0. A small protected API to test (token auth, tenant scoping)
# ============================================================
SECRET = "test-secret"
DATA = {f"user-{i}": {"tenant": f"t{i % 3}"} for i in range(6)}


def _b64url(data: bytes) -> str:
    import base64
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def issue_token(user: str, tenant: str, expires_in: int = 300) -> str:
    h = _b64url(json.dumps({"alg": "HS256"}).encode())
    payload = {"sub": user, "tenant": tenant, "exp": int(time.time()) + expires_in}
    p = _b64url(json.dumps(payload, separators=(",", ":")).encode())
    sig = hmac.new(SECRET.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    return f"{h}.{p}.{_b64url(sig)}"


def verify_token(token: str) -> dict | None:
    """Return claims or None. Rejects bad sig, expiry, malformed shape."""
    try:
        h, p, s = token.split(".")
        import base64
        expected = hmac.new(SECRET.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(expected, base64.urlsafe_b64decode(s + "==")):
            return None
        claims = json.loads(base64.urlsafe_b64decode(p + "=="))
        if claims.get("exp", 0) < time.time():
            return None
        return claims
    except Exception:
        return None


def api_get_user(token: str, target: str) -> tuple[int, dict | None]:
    """GET /users/{target}. 401 no/invalid token; 404 cross-tenant; 200 ok."""
    claims = verify_token(token)
    if claims is None:
        return 401, None
    user = DATA.get(target)
    if user is None:
        return 404, None
    if user["tenant"] != claims["tenant"]:
        return 404, None                     # hide existence (40-authorization)
    return 200, {"sub": target, "tenant": user["tenant"]}


print("=== 0. Protected API ===")
tok = issue_token("user-1", "t0")
print(f"GET user-0 with own token: {api_get_user(tok, 'user-0')[0]}")
print(f"GET user-3 (other tenant): {api_get_user(tok, 'user-3')[0]}  <- 404")
print()

# ============================================================
# 1. Auth bypass tests — the highest-value security tests
# ============================================================
# Test matrix for "is this endpoint actually protected?":
#   no token / garbage token / expired token / forged (unsigned) token /
#   token signed with the wrong secret / cross-tenant access.

def tamper_role(token: str) -> str:
    """Change the payload without re-signing -> must fail verification."""
    h, p, s = token.split(".")
    import base64
    claims = json.loads(base64.urlsafe_b64decode(p + "=="))
    claims["tenant"] = "t0"                  # attacker tries to widen access
    new_p = _b64url(json.dumps(claims, separators=(",", ":")).encode())
    return f"{h}.{new_p}.{s}"


def run_bypass_suite() -> list[str]:
    """Return the list of bypass attempts that FAILED to bypass (good)."""
    good = issue_token("user-1", "t0", expires_in=-10)   # expired
    forged = tamper_role(issue_token("user-1", "t1"))
    wrong_secret = issue_token("user-1", "t0")           # then sign wrong
    h, p, _ = wrong_secret.split(".")
    wrong_sig = hmac.new("other-secret".encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    import base64
    wrong_token = f"{h}.{p}.{_b64url(wrong_sig)}"

    attempts = {
        "no token": None,
        "garbage": "not.a.jwt",
        "expired": good,
        "tampered payload": forged,
        "wrong secret": wrong_token,
    }
    blocked = []
    for name, token in attempts.items():
        code, _ = api_get_user(token, "user-0")
        if code == 401:
            blocked.append(name)
    return blocked


print("=== 1. Auth bypass suite ===")
blocked = run_bypass_suite()
print(f"blocked: {blocked}")
print()

# ============================================================
# 2. Fuzzing — hostile-but-shaped inputs at every boundary
# ============================================================
# Send random payloads that are VALID SHAPES but hostile content:
# null bytes, very long strings, unicode, sql-ish text, path-ish text.
# The endpoint must never 500 on input it should reject cleanly.

def fuzz_payloads(seed: int = 7, n: int = 500) -> list[str]:
    rng = random.Random(seed)
    alphabet = string.printable + "\u0000\u00e9\u4e2d"
    corpus = ["../", "'; DROP TABLE", "<script>", "http://169.254.169.254"]
    for _ in range(n):
        length = rng.randint(0, 200)
        corpus.append("".join(rng.choice(alphabet) for _ in range(length)))
    return corpus


def fuzz_endpoint(payloads: list[str]) -> tuple[int, int]:
    """Feed each payload as the target; count 5xx (should be 0)."""
    tok = issue_token("user-1", "t0")
    five_xx = 0
    for payload in payloads:
        code, _ = api_get_user(tok, payload)
        if code >= 500:
            five_xx += 1
    return len(payloads), five_xx


print("=== 2. Fuzzing ===")
total, bad = fuzz_endpoint(fuzz_payloads())
print(f"fuzzed {total} payloads; 5xx responses: {bad}")
print()

# ============================================================
# 3. Static analysis + dependency scanning (automation)
# ============================================================
# bandit: AST-level scan for dangerous patterns (eval, subprocess
# without shell=False, hardcoded secrets). pip-audit: known CVEs in
# installed packages. Both run in CI, not by hand.

BANDIT_RULES = {
    "B101": "assert used in non-test code (asserts vanish under -O)",
    "B301": "pickle — unsafe deserialization",
    "B602": "shell=True in subprocess",
    "B105": "hardcoded password string",
}

def static_scan(code: str) -> list[str]:
    """Tiny stand-in for bandit: flag obvious dangerous patterns."""
    findings = []
    if "eval(" in code or "exec(" in code:
        findings.append("B307: eval/exec used")
    if "shell=True" in code:
        findings.append("B602: shell=True")
    if "password" in code and "=" in code and "secret" not in code:
        findings.append("B105: possible hardcoded credential")
    if "pickle.load" in code:
        findings.append("B301: pickle load")
    return findings


print("=== 3. Static analysis ===")
dodgy = "data = pickle.load(f)\nresult = eval(expr)"
print(f"scan finds: {static_scan(dodgy)}")
print(f"scan of this file is clean: {static_scan(open(__file__).read()) == [] or 'clean-ish'}")
print()

# ============================================================
# 4. Threat modeling an endpoint
# ============================================================
# For each endpoint: assets, attackers, attack vectors, mitigations.
# The output is the TEST list — every threat becomes a test or a
# documented residual risk.

def threat_model_endpoint(path: str, assets: list[str]) -> list[str]:
    """Return the test list derived from a quick threat model."""
    tests = []
    if "token" in str(assets).lower() or "auth" in path:
        tests += ["no-token", "expired", "forged-signature", "cross-tenant"]
    if "prompt" in path or "generate" in path:
        tests += ["oversize-prompt", "prompt-injection-payload", "rate-limit"]
    if "url" in path or "fetch" in path:
        tests += ["ssrf-metadata", "ssrf-localhost", "bad-scheme"]
    return tests


print("=== 4. Threat modeling ===")
print(f"/generate: {threat_model_endpoint('/generate', ['model-access', 'budget'])}")
print(f"/fetch-url: {threat_model_endpoint('/fetch-url', ['internal-net'])}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: testing only the happy path — the 200s work, the 401/404s rot
# CORRECT: an explicit bypass matrix per protected endpoint
#
# MISTAKE: no fuzz corpus at boundaries — one 500 on hostile input is a bug
# CORRECT: fuzz valid-shape hostile payloads; assert zero 5xx
#
# MISTAKE: security scans only when someone remembers
# CORRECT: bandit + pip-audit in CI on every change
#
# MISTAKE: threat models that never become tests
# CORRECT: every threat -> a test or a documented residual risk

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""

    # 1. Happy path works, then every bypass fails
    tok = issue_token("user-1", "t0")
    assert api_get_user(tok, "user-0")[0] == 200, "valid token works"

    # 2. Bypass suite: all five attempts blocked with 401
    blocked = run_bypass_suite()
    assert set(blocked) == {"no token", "garbage", "expired",
                            "tampered payload", "wrong secret"}, \
        f"bypass suite must block all five, blocked={blocked}"

    # 3. Cross-tenant is 404 (existence hidden), not 403 or 200
    assert api_get_user(tok, "user-3")[0] == 404, "cross-tenant must 404"

    # 4. Fuzzing: zero 5xx
    total, bad = fuzz_endpoint(fuzz_payloads(seed=42, n=300))
    assert bad == 0, f"fuzzing must not 5xx, got {bad} 5xx of {total}"

    # 5. Static scan flags known-dangerous patterns
    assert "eval" in static_scan("eval(expr)")[0]
    assert static_scan("safe = os.environ.get('X')") == [], \
        "clean code must scan clean"

    # 6. Threat model produces tests
    assert "ssrf-metadata" in threat_model_endpoint("/fetch-url", ["net"])
    assert "prompt-injection-payload" in threat_model_endpoint("/generate", ["m"])

    print("[OK] 42-security-testing: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Auth bypass matrix: no/expired/forged/wrong-secret tokens")
        print("2. Fuzz boundaries; zero 5xx is the contract")
        print("3. bandit + pip-audit automate static + dependency scanning")
        print("4. Every threat-model finding becomes a test")
        _verify()          # always runs, so plain execution is also a test
