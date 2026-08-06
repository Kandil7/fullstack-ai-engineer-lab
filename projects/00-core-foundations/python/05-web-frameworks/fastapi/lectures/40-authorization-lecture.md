# FastAPI — 40: Authorization

## Topic Overview

Authentication says *who you are*; authorization says *what you may do,
and on which resource*. The classic failure is checking the first and
skipping the second: "the user can read experiments" is a role check, but
"which experiments?" is a **resource-level** check — and in multi-tenant
AI products that second check is the product. Tenant isolation is
enforced by putting `tenant_id` in every query, never by post-filtering.
The production shape is **policy as data** (role→permission tables, ABAC
attribute rules) executed through **dependency-injected guards**, so the
enforcement point is one reusable function, not scattered if-statements.

The mental model: authorization is three nested questions — *can this
class of user do this class of action* (RBAC), *does this specific
resource allow this specific user* (resource check), *is the acting
service using the right identity* (confused deputy).

## Learning Objectives

By the end of this lecture, you will be able to:

1. Model RBAC as role→permission data, not if/else chains.
2. Add ABAC attribute rules (ownership, tenant, budget).
3. Write tenant-scoped queries that 404 on other tenants' rows.
4. Enforce permissions through reusable DI guards.
5. Explain the confused-deputy problem and fix it.

## Prerequisites

| Need | Where |
|---|---|
| Authentication | `38-auth-deep-lecture.md`, `39-oauth2-oidc-lecture.md` |
| FastAPI dependencies | `09-dependency-injection.py` |
| HTTP status codes | `23-exception-handling.py` |

---

## 1. Policy as data (RBAC)

Roles → permission sets live in a table or dict. Adding a role is editing
data, not hunting for endpoint code:

```python
ROLES = {
    "admin":    {"experiments.read", "experiments.write", "users.manage"},
    "engineer": {"experiments.read", "experiments.write"},
    "viewer":   {"experiments.read"},
}
def role_has(role, permission): return permission in ROLES.get(role, set())
```

The tests are one-liners; the policy is auditable at a glance.

## 2. Attribute-based rules (ABAC)

RBAC is coarse: role → permission. ABAC evaluates **attributes** — owner,
tenant, resource state, budget. Rules stay pure functions over
(user, resource, context):

```python
def can_cancel(user, run):
    if user["role"] == "admin": return True
    return user["role"] == "engineer" and run["owner_id"] == user["user_id"]
```

Ownership checks are the most common ABAC rule and the most commonly
forgotten one.

## 3. Resource checks and tenant isolation

The load-bearing pattern of multi-tenant software: the tenant filter is
**part of the query**, not a post-filter:

```python
def get_experiment(user, exp_id):
    return db.query(Experiment).filter_by(
        id=exp_id, tenant_id=user["tenant_id"]   # in the WHERE, always
    ).first()
```

Two details that leak or break products:
- Return **404**, not 403, for other tenants' rows — 403 leaks existence.
- Never fetch by id first and filter afterward — the fetch already touched
  the row.

## 4. DI-enforced permissions

FastAPI dependencies are the enforcement layer. A guard factory returns a
dependency that runs before the endpoint and raises if the permission is
missing:

```python
def require_permission(permission: str):
    def guard(current_user: User = Depends(get_current_user)):
        if not role_has(current_user.role, permission):
            raise HTTPException(403, f"missing permission: {permission}")
        return current_user
    return guard

@app.post("/experiments", dependencies=[Depends(require_permission("experiments.write"))])
```

One guard, reused everywhere; a new protected route cannot "forget" the
check because the dependency is visible in the route signature.

## 5. Confused deputy

A service that acts on a user's behalf must not use its own (more powerful)
credentials for user-requested work. The classic example: a copy service
authenticated as admin copying any tenant's data because the caller asked.
The fix is carrying the **caller's identity and tenant** through every hop
and scoping each action to it — service credentials only for service work.

## Common Mistakes to Avoid

### Mistake 1: Role check without resource check
```python
# WRONG - "can read experiments" but which ones?
# CORRECT - tenant_id/owner_id in the query itself
```

### Mistake 2: 403 for other tenants' rows
```python
# WRONG - leaks that the resource exists
# CORRECT - 404 for anything outside the caller's tenant
```

### Mistake 3: Scattered authorization if-statements
```python
# WRONG - each endpoint re-implements policy; new routes forget it
# CORRECT - policy as data + one DI guard reused everywhere
```

### Mistake 4: Service credentials for user work
```python
# WRONG - deputy acts with the service's admin identity
# CORRECT - carry caller identity; scope every action to it
```

### Mistake 5: Fetch-then-filter
```python
# WRONG - exp = get(exp_id); if exp.tenant != user.tenant: 403  (touched the row)
# CORRECT - filter by id AND tenant in one query
```

## Best Practices

1. Policy as data — roles/permissions tables, ABAC rule functions.
2. Tenant/owner scoping in the WHERE clause of every query.
3. 404 for cross-tenant access; never reveal existence.
4. Centralize enforcement in DI guards; list them in route signatures.
5. Carry caller identity through service calls; never use service creds
   for user work.
6. Test authorization as data: role tables, ownership rules, tenant 404s.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| RBAC lookup | O(1) set | — |
| ABAC rule | O(1) per rule | — |
| Tenant-scoped query | indexed lookup | tenant index |
| DI guard | O(1) per request | — |

Authorization costs almost nothing when it is data + indexes. The expensive
version is the incident after a missing check.

## AI Engineering Relevance

**Where this shows up:** multi-tenant fine-tuning platforms, per-customer
RAG indexes, model registry promotion policies, and agent permissions —
which tools an agent may call on behalf of which user.

| Concept here | Used for |
|---|---|
| RBAC | user roles on an LLM gateway |
| ABAC | budget caps per tenant, model access per plan |
| tenant isolation | customer RAG stores never cross |
| resource checks | one user's eval runs invisible to others |
| confused deputy | agents acting for users with scoped tool creds |

**Scale note:** tenant isolation must hold at 1M rows — which means the
tenant filter is an indexed predicate, not a Python post-filter.

## Practice Exercises

### Exercise 1: RBAC data  (Difficulty: Easy)
Define role→permission tables; assert viewers cannot delete.

### Exercise 2: ABAC ownership  (Difficulty: Easy)
Engineers cancel own runs only; admins cancel anything. Assert both.

### Exercise 3: Tenant scoping  (Difficulty: Medium)
List and get scoped by tenant; assert cross-tenant get returns None (404).

### Exercise 4: DI guard  (Difficulty: Medium)
Guard factory raises for missing permission; assert both paths.

### Exercise 5: Confused deputy  (Difficulty: Hard)
Model a service copying on behalf of a user; show the leak and the fix;
assert cross-tenant copies are refused.

### Exercise 6: Isolation at scale  (Difficulty: Hard)
Simulate 10k rows across tenants with an indexed tenant filter; assert
query count for the tenant-scoped read is O(result), not O(all).

## Summary

| Concept | Description |
|---|---|
| RBAC | role → permissions as data |
| ABAC | attribute rules over user/resource/context |
| Resource check | the query carries tenant/owner scoping |
| 404 not 403 | never leak other tenants' existence |
| DI guards | one enforcement point per permission |
| confused deputy | scope service actions to the caller |

Authentication proves identity; authorization bounds it. In multi-tenant
AI products the second one is the product — and it lives in queries,
policy data, and DI guards, not in hopes.

## Quick Reference

| Task | Idiom |
|---|---|
| Permission check | `role_has(role, perm)` over `ROLES` dict |
| Ownership rule | pure function over (user, resource) |
| Tenant-scoped read | `WHERE id=? AND tenant_id=?` |
| Cross-tenant row | return None → 404 |
| Route guard | `Depends(require_permission("perm"))` |
| Service hop | pass caller identity; never reuse service creds |

## Next Steps

Next: **[41 — API Security](41-api-security-lecture.md)** — rate limiting,
CORS done right, headers, and secrets handling.

Continues in: **[42 — Security Testing](42-security-testing-lecture.md)** —
proving the boundaries hold.

Official docs:
- FastAPI security: https://fastapi.tiangolo.com/tutorial/security/
- OWASP authorization cheat sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
