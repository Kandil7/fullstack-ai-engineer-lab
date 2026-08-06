"""
FastAPI — 40: Authorization
=============================
Topics: RBAC vs ABAC; resource-level checks; multi-tenant isolation;
        policy as data; DI-enforced permissions; confused deputy

Why this matters for AI/backend engineering:
    Authentication answers "who are you?"; authorization answers "what
    are you allowed to do, on WHICH resource?". Multi-tenant AI products
    live or die on tenant isolation: user A must never read user B's
    fine-tuning runs, prompts, or eval results. The production shape is
    policy as DATA (roles -> permissions tables, ABAC rules) enforced
    through dependency-injected checks — never scattered if-statements.

Run:      python 40-authorization.py
Verify:   python 40-authorization.py --verify
Reference: https://fastapi.tiangolo.com/tutorial/security/
"""

from __future__ import annotations

import sys
from typing import Callable

# ============================================================
# 1. Policy as data: RBAC roles -> permissions
# ============================================================
# Authorization rules live in DATA (tables/dicts), not in if/else
# chains scattered through endpoints. Adding a role = editing data.

ROLES: dict[str, set[str]] = {
    "admin": {"experiments.read", "experiments.write", "experiments.delete",
              "users.manage", "runs.cancel"},
    "engineer": {"experiments.read", "experiments.write", "runs.cancel"},
    "viewer": {"experiments.read"},
}

def role_has(role: str, permission: str) -> bool:
    return permission in ROLES.get(role, set())


print("=== 1. RBAC: policy as data ===")
print(f"engineer can write experiments: {role_has('engineer', 'experiments.write')}")
print(f"viewer can delete experiments : {role_has('viewer', 'experiments.delete')}")
print()

# ============================================================
# 2. ABAC: attribute-based rules
# ============================================================
# RBAC answers "role -> permission". ABAC adds ATTRIBUTES: resource
# owner, tenant, time-of-day, budget caps. Model rules as functions
# over (user, resource, context) — still data-driven, still testable.

def abac_rule_can_cancel(user: dict, run: dict) -> bool:
    """Engineers cancel runs they own; admins cancel anything."""
    if user["role"] == "admin":
        return True
    if user["role"] == "engineer" and run["owner_id"] == user["user_id"]:
        return True
    return False


print("=== 2. ABAC: attribute rules ===")
run = {"run_id": 10, "owner_id": "u1", "status": "running"}
print(f"owner engineer cancels own run: {abac_rule_can_cancel({'role': 'engineer', 'user_id': 'u1'}, run)}")
print(f"other engineer cancels run    : {abac_rule_can_cancel({'role': 'engineer', 'user_id': 'u2'}, run)}")
print(f"admin cancels any run         : {abac_rule_can_cancel({'role': 'admin', 'user_id': 'u9'}, run)}")
print()

# ============================================================
# 3. Resource-level checks + multi-tenant isolation
# ============================================================
# The #1 authorization bug: you checked "can this user read
# experiments?" but NOT "is this experiment in the user's tenant?".
# Tenant-scoped queries are the load-bearing pattern — the tenant_id
# is part of EVERY query's WHERE clause, not a post-filter.

EXPERIMENTS = [
    {"id": 1, "tenant_id": "acme", "name": "acme-finetune-1"},
    {"id": 2, "tenant_id": "globex", "name": "globex-rag-1"},
    {"id": 3, "tenant_id": "acme", "name": "acme-finetune-2"},
]

def list_experiments(user: dict) -> list[dict]:
    """Tenant-scoped: the WHERE clause carries the user's tenant."""
    return [e for e in EXPERIMENTS if e["tenant_id"] == user["tenant_id"]]


def get_experiment(user: dict, exp_id: int) -> dict | None:
    """Resource check: find by id AND tenant — 404 if not in your tenant."""
    for e in EXPERIMENTS:
        if e["id"] == exp_id and e["tenant_id"] == user["tenant_id"]:
            return e
    return None


acme_user = {"user_id": "u1", "tenant_id": "acme", "role": "engineer"}
globex_user = {"user_id": "u2", "tenant_id": "globex", "role": "engineer"}
print("=== 3. Resource checks & multi-tenant isolation ===")
print(f"acme user sees: {[e['name'] for e in list_experiments(acme_user)]}")
print(f"globex user sees: {[e['name'] for e in list_experiments(globex_user)]}")
print(f"acme user GET exp 1: {get_experiment(acme_user, 1)['name']}")
print(f"acme user GET exp 2 (globex's): {get_experiment(acme_user, 2)}  <- 404, not 403")
print()

# ============================================================
# 4. DI-enforced permissions
# ============================================================
# FastAPI dependencies are the enforcement point: a permission
# dependency runs before the endpoint, and the endpoint receives the
# caller. One function, reused on every protected route — no scattered
# checks, no "forgot the check on the new route".

def require_permission(permission: str) -> Callable:
    """Factory returning a FastAPI-style dependency guard."""

    def guard(current_user: dict) -> dict:
        if not role_has(current_user["role"], permission):
            raise PermissionError(f"missing permission: {permission}")
        return current_user

    return guard


def create_experiment(current_user: dict, name: str) -> dict:
    """Endpoints receive the user and rely on the DI guard."""
    require_permission("experiments.write")(current_user)   # simulated DI
    return {"id": 99, "tenant_id": current_user["tenant_id"], "name": name}


print("=== 4. DI-enforced permissions ===")
try:
    create_experiment({"role": "viewer", "tenant_id": "acme"}, "x")
    print("viewer created an experiment (BUG!)")
except PermissionError as e:
    print(f"viewer blocked: {e}")
print(f"engineer creates: {create_experiment({'role': 'engineer', 'tenant_id': 'acme'}, 'run-9')}")
print()

# ============================================================
# 5. Confused deputy problem
# ============================================================
# A service that acts on behalf of a user must NOT use the service's
# own (more powerful) credentials to do user-requested work — the
# "deputy" is confused about whose authority applies. Fix: carry the
# caller's tenant/identity through, and scope every action to it.

def copy_experiment_as_service(user: dict, exp_id: int) -> dict:
    """BROKEN version: service credential (admin) copies anything."""
    src = get_experiment({"user_id": "svc", "tenant_id": "acme", "role": "admin"}, exp_id)
    if src is None:
        raise PermissionError("not found or not in service tenant")
    # WRONG: copies into the SERVICE tenant, ignoring the caller
    return {"copied_from": exp_id, "tenant_id": "svc-tenant"}


def copy_experiment_scoped(user: dict, exp_id: int) -> dict | None:
    """Correct: the action is scoped to the CALLER's tenant."""
    src = get_experiment(user, exp_id)          # caller's tenant only
    if src is None:
        return None
    return {"copied_from": exp_id, "tenant_id": user["tenant_id"]}


print("=== 5. Confused deputy ===")
try:
    copy_experiment_as_service(globex_user, 1)
    print("service copied acme data on globex user's behalf (BUG!)")
except PermissionError as e:
    print(f"scoped copy blocks cross-tenant: {e}")
print(f"scoped copy of own-tenant exp: {copy_experiment_scoped(acme_user, 1)}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: checking role but not resource ownership/tenant
#   user CAN read experiments  ->  but WHICH ones? tenant_id in WHERE
# CORRECT: tenant_id in every query; 404 (not 403) for others' rows
#
# MISTAKE: authorization logic as scattered if-statements
# CORRECT: policy as data + DI guard reused on every route
#
# MISTAKE: returning 403 for resources that exist in another tenant —
#   this LEAKS that the resource exists. 404 is the safe answer.
#
# MISTAKE: service credentials used for user-requested work
#   (confused deputy) — always scope actions to the caller's identity
# CORRECT: carry user identity through; service creds only for service work

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""

    # 1. RBAC data drives checks
    assert role_has("admin", "users.manage"), "admin has manage"
    assert role_has("engineer", "experiments.write"), "engineer can write"
    assert not role_has("viewer", "experiments.delete"), "viewer cannot delete"
    assert not role_has("nobody", "experiments.read"), "unknown role has nothing"

    # 2. ABAC attribute rules
    assert abac_rule_can_cancel({"role": "engineer", "user_id": "u1"},
                                {"owner_id": "u1", "status": "running"})
    assert not abac_rule_can_cancel({"role": "engineer", "user_id": "u2"},
                                    {"owner_id": "u1", "status": "running"})
    assert abac_rule_can_cancel({"role": "admin", "user_id": "u9"},
                                {"owner_id": "u1", "status": "running"})

    # 3. Tenant isolation: list and get are both scoped
    assert [e["name"] for e in list_experiments(acme_user)] == \
        ["acme-finetune-1", "acme-finetune-2"]
    assert list_experiments(globex_user) == [EXPERIMENTS[1]]
    assert get_experiment(acme_user, 2) is None, "cross-tenant get must 404"
    assert get_experiment(acme_user, 1) is not None, "own-tenant get must work"

    # 4. DI guard enforces permission
    try:
        require_permission("experiments.write")({"role": "viewer", "tenant_id": "acme"})
        assert False, "viewer must be blocked"
    except PermissionError:
        pass
    assert require_permission("experiments.read")({"role": "viewer"}) is not None

    # 5. Confused deputy fixed: service cannot cross tenant boundaries
    assert copy_experiment_scoped(globex_user, 1) is None, \
        "scoped copy must refuse cross-tenant reads"
    assert copy_experiment_scoped(acme_user, 1)["tenant_id"] == "acme", \
        "scoped copy stays in the caller's tenant"

    print("[OK] 40-authorization: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. RBAC = roles->permissions as data; ABAC adds attributes")
        print("2. Tenant isolation: tenant_id in EVERY query; 404 for others' rows")
        print("3. DI guards centralize enforcement; never scattered checks")
        print("4. Confused deputy: scope service actions to the caller")
        _verify()          # always runs, so plain execution is also a test
