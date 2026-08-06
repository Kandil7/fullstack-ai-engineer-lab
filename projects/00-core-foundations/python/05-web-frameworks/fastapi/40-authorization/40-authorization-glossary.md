# Authorization — Glossary 40

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| ABAC | Model | Attribute-based access control — rules over user/resource/context |
| Confused deputy | Attack | A service using its own powers for a user's request |
| DI guard | Enforcement | A dependency that checks permission before the endpoint |
| Multi-tenancy | Concept | Many customers, isolated data, shared code |
| 404 vs 403 | Detail | 404 hides existence; 403 leaks it |
| Ownership check | Rule | Only the resource's owner may act on it |
| Policy as data | Design | Rules in tables/dicts, not scattered if-statements |
| RBAC | Model | Role-based access control — roles map to permissions |
| Resource check | Rule | Per-resource authorization (tenant/owner in the query) |
| Tenant isolation | Guarantee | One tenant's rows invisible to another |
| Tenant-scoped query | Pattern | tenant_id in the WHERE clause, never a post-filter |
| 403 | Status | Forbidden — the caller lacks the permission |

## Detailed Definitions

### ABAC
**Definition**: Attribute-based access control — authorization rules
evaluated over attributes (owner, tenant, resource state, budget), modeled
as pure functions over (user, resource, context).
**Related**: RBAC

### Confused deputy
**Definition**: A privileged service acting on a user's request with its
own (stronger) authority — e.g. a copy service using admin credentials for
any tenant's data. Fixed by scoping actions to the caller's identity.
**Related**: Tenant isolation

### DI guard
**Definition**: A FastAPI dependency that runs before the endpoint and
raises on missing permission — the centralized enforcement point reused
across routes.
**Related**: RBAC

### Multi-tenancy
**Definition**: One product serving many customers (tenants) with
data-isolation guarantees — the context that makes authorization the
product.
**Related**: Tenant isolation

### 404 vs 403
**Definition**: For other tenants' rows, return 404 (not found) — 403
admits the row exists and leaks information.
**Related**: Resource check

### Ownership check
**Definition**: The ABAC rule that a user may act only on resources they
own (or that the admin may act on) — the most commonly forgotten check.
**Related**: ABAC

### Policy as data
**Definition**: Authorization rules stored as role→permission tables and
rule functions — auditable, testable, and edited without touching endpoint
code.
**Related**: RBAC

### RBAC
**Definition**: Role-based access control — a user's role maps to a
permission set; `permission in ROLES[role]`.
**Related**: ABAC

### Resource check
**Definition**: The second authorization question — not just "may this
class of user do this action" but "may THIS user act on THIS resource"
(tenant/owner in the query).
**Related**: Tenant-scoped query

### Tenant isolation
**Definition**: The guarantee that one tenant's data is unreadable by
another — enforced by tenant_id in every query and 404s on cross-tenant
access.
**Related**: Multi-tenancy

### Tenant-scoped query
**Definition**: A query carrying the caller's tenant_id in the WHERE clause
— the load-bearing isolation pattern; never fetch-then-filter.
**Related**: Resource check

### 403
**Definition**: Forbidden — the authenticated caller lacks permission for
this action on this resource.
**Related**: 404 vs 403

## Key Concepts Summary

### The three authorization questions
1. RBAC: can this role do this class of action?
2. Resource check: may this user act on this specific resource?
3. Deputy check: is the acting service using the right identity?

### The isolation rules
- tenant_id in every query's WHERE.
- 404 (not 403) for other tenants' rows.
- Never fetch-then-filter.

### The enforcement shape
- Policy as data (roles, ABAC rules).
- DI guards reused on every protected route.
- Caller identity carried through service hops.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Roles map to permissions — ___
2. Rules over user/resource/context — ___
3. tenant_id in the WHERE clause — ___
4. 404 hides it; 403 leaks it — ___
5. The dependency enforcing a permission — ___
6. A service using its own powers for a user — ___
7. Rules in tables, not if-statements — ___
8. Only the owner may act — ___

**Answers:** 1-RBAC, 2-ABAC, 3-tenant-scoped query, 4-existence, 5-DI guard,
6-confused deputy, 7-policy as data, 8-ownership check
