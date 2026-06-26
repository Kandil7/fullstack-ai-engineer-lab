# SaaS Architecture Patterns

> Complete guide to building multi-tenant SaaS applications.

## Table of Contents
1. [Overview](#overview)
2. [Multi-Tenancy](#multi-tenancy)
3. [Subscription Billing](#subscription-billing)
4. [Feature Flags](#feature-flags)
5. [Analytics Pipeline](#analytics-pipeline)
6. [Admin Dashboard](#admin-dashboard)
7. [Security](#security)
8. [Scaling](#scaling)

---

## Overview

### What is SaaS?

Software as a Service (SaaS) is a cloud-based software delivery model where:
- Multiple customers (tenants) share the same infrastructure
- Each tenant's data is isolated and secure
- Updates are deployed once and serve all tenants
- Billing is subscription-based

### SaaS Architecture Principles

1. **Multi-tenancy**: Shared infrastructure, isolated data
2. **Configurability**: Tenant-specific customization
3. **Scalability**: Grow from 10 to 10,000 tenants
4. **Security**: Data isolation, access control
5. **Observability**: Per-tenant metrics and logging

### SaaS vs Traditional Software

| Aspect | Traditional | SaaS |
|--------|-------------|------|
| Deployment | Per-customer | Shared infrastructure |
| Updates | Manual per customer | Automatic, all customers |
| Scaling | Vertical | Horizontal, per-tenant |
| Billing | License-based | Subscription-based |
| Support | Reactive | Proactive, self-service |

---

## Multi-Tenancy

### Multi-Tenancy Models

#### 1. Shared Database, Shared Schema
```
┌─────────────────────────────────────────────────────────┐
│                    PostgreSQL                            │
│  ┌───────────────────────────────────────────────────┐  │
│  │ users table                                       │  │
│  │ ┌─────┬──────────┬────────────┐                   │  │
│  │ │ id  │ tenant_id│ email      │                   │  │
│  │ ├─────┼──────────┼────────────┤                   │  │
│  │ │ 1   │ tenant_a │ a@test.com │                   │  │
│  │ │ 2   │ tenant_b │ b@test.com │                   │  │
│  │ │ 3   │ tenant_a │ c@test.com │                   │  │
│  │ └─────┴──────────┴────────────┘                   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Pros:**
- Cost-efficient
- Easy to maintain
- Simple queries

**Cons:**
- Data isolation risk
- Noisy neighbor problem
- Complex backup/restore

**Best for:** Small to medium SaaS, cost-sensitive

#### 2. Shared Database, Separate Schemas
```
┌─────────────────────────────────────────────────────────┐
│                    PostgreSQL                            │
│  ┌──────────────────────┐  ┌──────────────────────┐    │
│  │ tenant_a schema      │  │ tenant_b schema      │    │
│  │ ┌──────────────────┐ │  │ ┌──────────────────┐ │    │
│  │ │ users            │ │  │ │ users            │ │    │
│  │ │ conversations    │ │  │ │ conversations    │ │    │
│  │ │ messages         │ │  │ │ messages         │ │    │
│  │ └──────────────────┘ │  │ └──────────────────┘ │    │
│  └──────────────────────┘  └──────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

**Pros:**
- Better data isolation
- Easier per-tenant operations
- Schema customization possible

**Cons:**
- More complex migrations
- Higher resource usage
- Schema sprawl

**Best for:** Medium SaaS, need for customization

#### 3. Separate Databases
```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ tenant_a DB      │  │ tenant_b DB      │  │ tenant_c DB      │
│ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │
│ │ users       │ │  │ │ users       │ │  │ │ users       │ │
│ │ conversations│ │  │ │ conversations│ │  │ │ conversations│ │
│ │ messages    │ │  │ │ messages    │ │  │ │ messages    │ │
│ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

**Pros:**
- Maximum isolation
- Independent scaling
- Easy backup/restore

**Cons:**
- High cost
- Complex management
- Resource waste

**Best for:** Enterprise SaaS, compliance requirements

### Tenant Resolution

```go
// Middleware to resolve tenant from request
func TenantMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Method 1: From subdomain
        tenant := extractSubdomain(r.Host)
        
        // Method 2: From header
        // tenant := r.Header.Get("X-Tenant-ID")
        
        // Method 3: From JWT claim
        // tenant := getTenantFromToken(r)
        
        if tenant == "" {
            http.Error(w, "Tenant not found", http.StatusNotFound)
            return
        }
        
        // Add tenant to context
        ctx := context.WithValue(r.Context(), "tenant", tenant)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

### Tenant Context Propagation

```go
type TenantContext struct {
    TenantID    string
    TenantName  string
    Plan        string
    Features    []string
    DB          *sql.DB
}

func GetTenant(ctx context.Context) *TenantContext {
    return ctx.Value("tenant").(*TenantContext)
}
```

---

## Subscription Billing

### Subscription Tiers

```yaml
plans:
  free:
    name: "Free"
    price: 0
    features:
      - 100 messages/month
      - 5 conversations
      - Basic models only
      - Community support
    
  pro:
    name: "Pro"
    price: 20
    interval: month
    features:
      - 1000 messages/month
      - Unlimited conversations
      - All models
      - Priority support
      - File uploads
    
  enterprise:
    name: "Enterprise"
    price: 100
    interval: month
    features:
      - Unlimited messages
      - Unlimited conversations
      - All models + custom fine-tuning
      - Dedicated support
      - SSO/SAML
      - SLA guarantee
      - Audit logs
```

### Billing Schema

```sql
-- Tenants
CREATE TABLE tenants (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(255) NOT NULL,
    slug        VARCHAR(100) UNIQUE NOT NULL,
    plan        VARCHAR(50) DEFAULT 'free',
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Subscriptions
CREATE TABLE subscriptions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID REFERENCES tenants(id),
    stripe_sub_id   VARCHAR(255),
    status          VARCHAR(50),
    current_period  TIMESTAMPTZ,
    cancel_at       TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Usage tracking
CREATE TABLE usage (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id   UUID REFERENCES tenants(id),
    metric      VARCHAR(100),  -- 'messages', 'tokens', 'uploads'
    quantity    BIGINT,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Stripe Integration

```go
// Webhook handler for Stripe events
func HandleStripeWebhook(w http.ResponseWriter, r *http.Request) {
    payload, err := io.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "Error reading body", http.StatusBadRequest)
        return
    }
    
    sigHeader := r.Header.Get("Stripe-Signature")
    event, err := webhook.ConstructEvent(payload, sigHeader, webhookSecret)
    if err != nil {
        http.Error(w, "Invalid signature", http.StatusBadRequest)
        return
    }
    
    switch event.Type {
    case "checkout.session.completed":
        handleCheckoutComplete(event.Data.Object)
    case "invoice.paid":
        handleInvoicePaid(event.Data.Object)
    case "customer.subscription.updated":
        handleSubscriptionUpdated(event.Data.Object)
    case "customer.subscription.deleted":
        handleSubscriptionDeleted(event.Data.Object)
    }
}
```

### Usage Metering

```go
// Track usage for billing
func TrackUsage(tenantID string, metric string, quantity int64) error {
    // Insert usage record
    _, err := db.Exec(`
        INSERT INTO usage (tenant_id, metric, quantity, recorded_at)
        VALUES ($1, $2, $3, NOW())
    `, tenantID, metric, quantity)
    
    // Check usage limits
    plan := GetTenantPlan(tenantID)
    limit := GetPlanLimit(plan, metric)
    
    currentUsage := GetCurrentUsage(tenantID, metric)
    if currentUsage+quantity > limit {
        return ErrUsageLimitExceeded
    }
    
    return nil
}
```

---

## Feature Flags

### Feature Flag System

```go
type FeatureFlag struct {
    ID          string
    Name        string
    Description string
    Enabled     bool
    Conditions  []Condition
}

type Condition struct {
    Attribute string      // 'plan', 'tenant_id', 'user_id'
    Operator  string      // 'eq', 'in', 'gt', 'lt'
    Value     interface{}
}

// Check if feature is enabled
func IsFeatureEnabled(ctx context.Context, feature string) bool {
    tenant := GetTenant(ctx)
    user := GetUser(ctx)
    
    flag := GetFeatureFlag(feature)
    
    if !flag.Enabled {
        return false
    }
    
    for _, condition := range flag.Conditions {
        if !evaluateCondition(condition, tenant, user) {
            return false
        }
    }
    
    return true
}
```

### Feature Flag Configuration

```yaml
features:
  - name: "advanced_analytics"
    description: "Advanced analytics dashboard"
    enabled: true
    conditions:
      - attribute: "plan"
        operator: "in"
        value: ["pro", "enterprise"]
    
  - name: "custom_models"
    description: "Custom fine-tuned models"
    enabled: true
    conditions:
      - attribute: "plan"
        operator: "eq"
        value: "enterprise"
    
  - name: "new_ui"
    description: "Redesigned user interface"
    enabled: false
    rollout:
      percentage: 10
      tenant_ids: ["tenant_abc123"]
```

### Feature Flag Database

```sql
CREATE TABLE feature_flags (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    enabled     BOOLEAN DEFAULT false,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE feature_conditions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flag_id     UUID REFERENCES feature_flags(id),
    attribute   VARCHAR(100),
    operator    VARCHAR(50),
    value       JSONB,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Analytics Pipeline

### Analytics Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Event Sources                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ Frontend│  │ Backend │  │ Billing │  │ Support │   │
│  │ Events  │  │ Events  │  │ Events  │  │ Events  │   │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │
└───────┼────────────┼────────────┼────────────┼─────────┘
        │            │            │            │
        ▼            ▼            ▼            ▼
┌─────────────────────────────────────────────────────────┐
│                  Event Queue (Kafka)                     │
└─────────────────────────┬───────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ Real-time     │ │ Batch         │ │ Archival      │
│ Processing    │ │ Processing    │ │ Storage       │
│ (Redis)       │ │ (Spark)       │ │ (S3)          │
└───────┬───────┘ └───────┬───────┘ └───────────────┘
        │                 │
        ▼                 ▼
┌───────────────┐ ┌───────────────┐
│ Dashboards    │ │ Data Warehouse│
│ (Grafana)     │ │ (BigQuery)    │
└───────────────┘ └───────────────┘
```

### Event Schema

```json
{
  "event_id": "evt_abc123",
  "event_type": "message.sent",
  "timestamp": "2025-01-15T10:30:00Z",
  "tenant_id": "tenant_xyz",
  "user_id": "usr_abc123",
  "properties": {
    "conversation_id": "conv_abc123",
    "model": "gpt-4",
    "tokens_used": 150,
    "response_time_ms": 1200
  },
  "context": {
    "platform": "web",
    "browser": "chrome",
    "os": "windows"
  }
}
```

### Analytics Events

| Event | Description | Properties |
|-------|-------------|------------|
| user.signup | New user registration | method, plan |
| user.login | User login | method, device |
| message.sent | User sent message | model, tokens |
| message.received | AI response received | latency, tokens |
| conversation.created | New conversation | topic |
| conversation.deleted | Conversation deleted | reason |
| subscription.upgraded | Plan upgrade | from, to |
| subscription.downgraded | Plan downgrade | from, to |
| feature.used | Feature flag used | feature, result |

### Analytics Queries

```sql
-- Daily Active Users
SELECT DATE(created_at) as day, COUNT(DISTINCT user_id) as dau
FROM events
WHERE event_type = 'user.login'
AND created_at > NOW() - INTERVAL '30 days'
GROUP BY day
ORDER BY day;

-- Messages per Tenant
SELECT tenant_id, COUNT(*) as messages
FROM events
WHERE event_type = 'message.sent'
AND created_at > NOW() - INTERVAL '1 day'
GROUP BY tenant_id
ORDER BY messages DESC;

-- Model Usage Distribution
SELECT 
    properties->>'model' as model,
    COUNT(*) as count,
    SUM((properties->>'tokens_used')::int) as total_tokens
FROM events
WHERE event_type = 'message.sent'
AND created_at > NOW() - INTERVAL '7 days'
GROUP BY model;
```

---

## Admin Dashboard

### Dashboard Components

```
┌─────────────────────────────────────────────────────────┐
│                    Admin Dashboard                       │
├─────────────────┬───────────────────────────────────────┤
│                 │                                       │
│  ┌───────────┐  │  ┌─────────────────────────────────┐ │
│  │ Sidebar   │  │  │  Overview                       │ │
│  │           │  │  │  ┌─────┐ ┌─────┐ ┌─────┐       │ │
│  │ Overview  │  │  │  │DAU  │ │Rev  │ │Msgs │       │ │
│  │ Tenants   │  │  │  │1.2K │ │$45K │ │250K │       │ │
│  │ Users     │  │  │  └─────┘ └─────┘ └─────┘       │ │
│  │ Billing   │  │  │                                 │ │
│  │ Features  │  │  │  [Chart: Daily Active Users]    │ │
│  │ Analytics │  │  │  ┌─────────────────────────────┐│ │
│  │ Settings  │  │  │  │  📈                        ││ │
│  │           │  │  │  │    📈                       ││ │
│  └───────────┘  │  │  │       📈                    ││ │
│                 │  │  └─────────────────────────────┘│ │
│                 │  └─────────────────────────────────┘ │
│                 │                                       │
│                 │  ┌─────────────────────────────────┐ │
│                 │  │  Tenant List                    │ │
│                 │  │  ┌─────────────────────────────┐│ │
│                 │  │  │ Acme Corp  │ Pro  │ $20/mo  ││ │
│                 │  │  │ TechStart  │ Free │ $0      ││ │
│                 │  │  │ Enterprise │ Ent  │ $100/mo ││ │
│                 │  │  └─────────────────────────────┘│ │
│                 │  └─────────────────────────────────┘ │
└─────────────────┴───────────────────────────────────────┘
```

### Admin API Endpoints

```yaml
# Tenant Management
GET    /admin/tenants           # List tenants
GET    /admin/tenants/:id       # Get tenant details
PUT    /admin/tenants/:id       # Update tenant
DELETE /admin/tenants/:id       # Delete tenant
POST   /admin/tenants/:id/impersonate  # Impersonate tenant

# User Management
GET    /admin/users             # List users
GET    /admin/users/:id         # Get user details
PUT    /admin/users/:id         # Update user
DELETE /admin/users/:id         # Delete user

# Feature Flags
GET    /admin/features          # List feature flags
POST   /admin/features          # Create feature flag
PUT    /admin/features/:id      # Update feature flag
DELETE /admin/features/:id      # Delete feature flag

# Analytics
GET    /admin/analytics/overview    # Dashboard overview
GET    /admin/analytics/usage       # Usage metrics
GET    /admin/analytics/revenue     # Revenue metrics
GET    /admin/analytics/churn       # Churn analysis

# Billing
GET    /admin/billing/subscriptions  # List subscriptions
POST   /admin/billing/invoices       # Generate invoices
POST   /admin/billing/refunds        # Process refunds
```

### Admin Database Schema

```sql
-- Admin users
CREATE TABLE admin_users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       VARCHAR(255) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    role        VARCHAR(50) DEFAULT 'admin',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Audit logs
CREATE TABLE audit_logs (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    admin_id    UUID REFERENCES admin_users(id),
    action      VARCHAR(100),
    resource    VARCHAR(100),
    resource_id VARCHAR(255),
    details     JSONB,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_admin_id ON audit_logs(admin_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

---

## Security

### SaaS Security Checklist

- [ ] Tenant data isolation enforced
- [ ] Row-level security (RLS) enabled
- [ ] Admin access audit logged
- [ ] API keys rotated regularly
- [ ] Secrets stored in vault (not env vars)
- [ ] Penetration testing quarterly
- [ ] SOC 2 compliance (if needed)
- [ ] GDPR data export/deletion supported

### Row-Level Security (PostgreSQL)

```sql
-- Enable RLS on tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their tenant's data
CREATE POLICY tenant_isolation ON users
    USING (tenant_id = current_setting('app.tenant_id')::uuid);

CREATE POLICY tenant_isolation ON conversations
    USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- Set tenant context per request
SET app.tenant_id = 'tenant_abc123';
```

### Data Isolation Middleware

```go
func DataIsolationMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        tenant := GetTenant(r.Context())
        
        // Set tenant context for database
        _, err := db.Exec("SET app.tenant_id = $1", tenant.ID)
        if err != nil {
            http.Error(w, "Internal error", http.StatusInternalServerError)
            return
        }
        
        next.ServeHTTP(w, r)
    })
}
```

---

## Scaling

### Scaling Strategy by Tenant Size

| Tenant Size | Model | Isolation | Scaling |
|-------------|-------|-----------|---------|
| < 100 users | Shared DB | Logical | Horizontal |
| 100-1000 users | Shared DB | Schema | Horizontal |
| 1000-10000 users | Separate DB | Physical | Vertical + Horizontal |
| > 10000 users | Dedicated cluster | Physical | Auto-scaling |

### Cost Optimization

```yaml
# Resource allocation by plan
resources:
  free:
    cpu: 0.25 cores
    memory: 512MB
    storage: 1GB
    rate_limit: 10 req/min
  
  pro:
    cpu: 1 core
    memory: 2GB
    storage: 10GB
    rate_limit: 60 req/min
  
  enterprise:
    cpu: 4 cores
    memory: 8GB
    storage: 100GB
    rate_limit: 200 req/min
```

### Auto-Scaling Rules

```yaml
autoscaling:
  metrics:
    - type: TenantCount
      target: 100  # per pod
    - type: CPU
      target: 70%
    - type: Memory
      target: 80%
    - type: RequestRate
      target: 1000  # per pod
  scale_up:
    cooldown: 60s
    pods: 2
  scale_down:
    cooldown: 300s
    pods: 1
```

---

## Implementation Checklist

### Phase 1: Foundation
- [ ] Multi-tenant schema design
- [ ] Tenant resolution middleware
- [ ] Basic subscription management
- [ ] Admin API scaffold

### Phase 2: Billing
- [ ] Stripe integration
- [ ] Usage metering
- [ ] Subscription lifecycle
- [ ] Invoice generation

### Phase 3: Features
- [ ] Feature flag system
- [ ] A/B testing framework
- [ ] Rollout management
- [ ] Analytics pipeline

### Phase 4: Admin
- [ ] Admin dashboard UI
- [ ] Tenant management
- [ ] User management
- [ ] Audit logging

### Phase 5: Scale
- [ ] Auto-scaling configuration
- [ ] Performance optimization
- [ ] Cost monitoring
- [ ] Disaster recovery

---

## Reference Architectures

- [Stripe SaaS Billing](https://stripe.com/docs/billing)
- [LaunchDarkly Feature Flags](https://launchdarkly.com/)
- [Segment Analytics](https://segment.com/)
- [Auth0 Multi-Tenancy](https://auth0.com/multi-tenant)

---

*This guide provides patterns, not prescriptions. Adapt to your specific needs.*
