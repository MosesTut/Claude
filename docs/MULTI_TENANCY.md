# Multi-Tenancy Guide

Complete guide to Timbuktoo's multi-tenant architecture, onboarding flow, and pricing.

## Overview

Timbuktoo supports full multi-tenancy with:
- **Schema-per-tenant** isolation for data security
- **Per-tenant vector namespaces** for knowledge separation
- **Usage quotas** per subscription tier
- **RBAC** enforced per tenant
- **Customer onboarding flow** from signup to itinerary

## Architecture

```
┌─────────────────────────────────────────┐
│         Shared Infrastructure           │
├─────────────────────────────────────────┤
│  • Main Database (PostgreSQL)           │
│  • Vector Storage (ChromaDB)            │
│  • Application Layer                    │
└─────────────────────────────────────────┘
           │
           ├──► Tenant A (schema: tenant_acme)
           │    ├─ Vector Namespace: tenant_abc-123_vectors
           │    ├─ Quotas: 10 itineraries/month
           │    └─ Tier: Starter
           │
           ├──► Tenant B (schema: tenant_globex)
           │    ├─ Vector Namespace: tenant_xyz-456_vectors
           │    ├─ Quotas: Unlimited
           │    └─ Tier: Pro
           │
           └──► Tenant C (schema: tenant_enterprise)
                ├─ Vector Namespace: tenant_ent-789_vectors
                ├─ Quotas: Unlimited + Custom
                └─ Tier: Enterprise
```

## Tenant Isolation

### Database Isolation
Each tenant gets a dedicated PostgreSQL schema:
- `tenant_acme` - All tables scoped to tenant
- Data cannot cross schema boundaries
- Queries automatically filtered by `tenant_id`

### Vector Database Isolation
Each tenant gets a dedicated ChromaDB collection:
- `tenant_abc-123_vectors` - Separate embeddings
- No cross-tenant vector search possible
- Tenant can have custom knowledge base

### Benefits
- **Security**: Complete data isolation
- **Privacy**: GDPR compliance ready
- **Customization**: Tenant-specific data
- **Performance**: Isolated workloads

## Pricing & Packaging

### Starter Tier
**$29/month**

Features:
- 10 itineraries per month
- 5 pilot cities (Lisbon, Barcelona, Mexico City, Tokyo, NYC)
- Email support
- Standard processing
- 1 user seat

Quotas:
```yaml
itineraries_per_month: 10
max_users: 1
max_api_cost_per_trip: 0.80
```

### Pro Tier
**$99/month**

Features:
- **Unlimited itineraries**
- All cities including premium destinations
- Priority email + chat support
- Advanced analytics
- Up to 10 user seats
- Higher API cost ceiling

Quotas:
```yaml
itineraries_per_month: -1  # unlimited
max_users: 10
max_api_cost_per_trip: 1.50
```

### Enterprise Tier
**Custom Pricing**

Features:
- **Unlimited itineraries**
- All cities + custom destinations
- Dedicated account manager + phone support
- Custom dashboards and reporting
- **Unlimited user seats**
- Dedicated tenancy option
- **99.9% SLA**
- **SOC-2 + HIPAA compliance**
- White-label options

Quotas:
```yaml
itineraries_per_month: -1  # unlimited
max_users: -1  # unlimited
max_api_cost_per_trip: 3.00
dedicated_schema: true
custom_vector_db: true
```

## Customer Onboarding Flow

### Step 1: Tenant Signup

```http
POST /api/v1/onboarding/start
{
  "email": "user@example.com"
}

Response:
{
  "success": true,
  "session_id": "uuid",
  "current_step": "signup"
}
```

### Step 2: Complete Signup

```http
POST /api/v1/onboarding/signup
{
  "session_id": "uuid",
  "tenant_name": "acme-travel",
  "company_name": "Acme Travel Co",
  "plan_id": "starter_monthly"
}

Response:
{
  "success": true,
  "tenant_id": "uuid",
  "subscription": {...},
  "trial_ends_at": "2024-07-01T00:00:00Z"
}
```

**What happens:**
- Tenant record created
- PostgreSQL schema created: `tenant_acme_travel`
- Vector collection created: `tenant_{id}_vectors`
- Subscription created with 14-day trial
- Usage quotas initialized
- Shared city data copied to tenant namespace

### Step 3: Preference Capture

```http
POST /api/v1/onboarding/preferences
{
  "session_id": "uuid",
  "preferences": {
    "vibes": ["local", "food", "nightlife"],
    "interests": ["food", "drink", "nature", "culture"],
    "budget_level": "mid",
    "travel_dates": {
      "start": "2024-06-01",
      "end": "2024-06-07"
    }
  }
}
```

### Step 4: City Recommendation

```http
POST /api/v1/onboarding/recommend-cities?session_id=uuid

Response:
{
  "success": true,
  "ranked_cities": [
    {
      "city_id": "uuid",
      "name": "Lisbon",
      "score": 0.95,
      "reasoning": "Perfect match for food, nightlife, and authenticity",
      "highlights": [...],
      "estimated_daily_budget_usd": 150
    }
  ]
}
```

**What happens:**
- Weather tool fetches forecasts
- Events tool checks local happenings
- City Selection Agent ranks cities
- Top 3 recommendations returned

### Step 5: City Selection

```http
POST /api/v1/onboarding/select-city
{
  "session_id": "uuid",
  "city_id": "uuid"
}
```

### Step 6: Itinerary Delivery

```http
POST /api/v1/onboarding/generate-itinerary?session_id=uuid

Response:
{
  "success": true,
  "itinerary": {
    "city": "Lisbon",
    "daily_itineraries": [...],
    "logistics": {...},
    "packing_list": {...}
  }
}
```

**What happens:**
- Quota checked (Starter: 10/month)
- Local Expert Agent queries tenant vector DB
- Travel Concierge Agent creates 7-day plan
- Itinerary saved to trip record
- Usage counter incremented
- Cost tracked per tenant

### Step 7: Feedback Loop

```http
POST /api/v1/onboarding/feedback
{
  "session_id": "uuid",
  "rating": 5,
  "comments": "Amazing recommendations!"
}

Response:
{
  "success": true,
  "message": "Thank you for your feedback!",
  "current_step": "completed"
}
```

## Usage Quotas & Enforcement

### Quota Check Example

```python
from timbuktoo.utils.tenant_manager import get_tenant_manager

tenant_mgr = get_tenant_manager()

# Check quota before operation
quota_check = tenant_mgr.check_quota(
    tenant_id="abc-123",
    resource_type="itineraries"
)

if not quota_check["allowed"]:
    return {
        "error": "Quota exceeded",
        "current_usage": quota_check["current_usage"],
        "limit": quota_check["quota_limit"],
        "upgrade_url": "/pricing"
    }

# Perform operation...

# Increment usage
tenant_mgr.increment_usage(
    tenant_id="abc-123",
    resource_type="itineraries",
    amount=1
)
```

### Quota Types

| Resource | Starter | Pro | Enterprise |
|----------|---------|-----|------------|
| Itineraries/month | 10 | Unlimited | Unlimited |
| User seats | 1 | 10 | Unlimited |
| API cost/trip | $0.80 | $1.50 | $3.00 |
| Vector storage | 100MB | 1GB | Custom |
| Support | Email | Priority | Dedicated |

## Subscription Management

### Upgrade Subscription

```http
POST /api/v1/tenants/{tenant_id}/upgrade
Authorization: Bearer {token}
{
  "new_plan_id": "pro_monthly"
}

Response:
{
  "success": true,
  "subscription": {
    "plan_id": "pro_monthly",
    "monthly_price_usd": 99.00,
    "status": "active"
  },
  "tier": "pro"
}
```

**What happens:**
- Subscription updated
- Quotas increased immediately
- Pro-rated billing applied
- Tier benefits activated

### Check Tenant Status

```http
GET /api/v1/tenants/{tenant_id}
Authorization: Bearer {token}

Response:
{
  "tenant": {
    "tenant_id": "uuid",
    "tenant_name": "acme-travel",
    "subscription_tier": "starter",
    "status": "active"
  },
  "subscription": {
    "plan_id": "starter_monthly",
    "current_period_end": "2024-07-01T00:00:00Z"
  },
  "quotas": [
    {
      "resource_type": "itineraries",
      "quota_limit": 10,
      "current_usage": 7,
      "remaining": 3
    }
  ]
}
```

## Multi-User Support

Tenants can have multiple users with different roles:

### Tenant Roles
- **Owner**: Full admin access, billing
- **Admin**: Manage users, create trips
- **Member**: Create trips, view analytics
- **Viewer**: Read-only access

### Add User to Tenant

```python
from timbuktoo.database.models import TenantUser, SessionLocal

db = SessionLocal()

tenant_user = TenantUser(
    tenant_id=tenant_id,
    user_id=user_id,
    role="member"
)
db.add(tenant_user)
db.commit()
```

## Security Considerations

### Data Isolation
- All queries include `tenant_id` filter
- Row-level security in PostgreSQL
- Vector searches scoped to tenant collection

### Audit Logging
All tenant operations logged:
- Onboarding completion
- Trip creation
- Subscription changes
- User access

### GDPR Compliance

Delete tenant data:
```python
from timbuktoo.database.tenant_vector_db import get_tenant_vector_db
from timbuktoo.utils.tenant_manager import get_tenant_manager

# Delete vector data
vector_db = get_tenant_vector_db()
vector_db.delete_tenant_data(tenant_id)

# Delete relational data (cascades)
# ... tenant deletion logic
```

## Production Deployment

### Environment Variables

```bash
# Tenant defaults
DEFAULT_TRIAL_DAYS=14
DEFAULT_PLAN_ID=starter_monthly

# Quota enforcement
ENABLE_QUOTA_CHECKS=true
QUOTA_GRACE_PERIOD_DAYS=3

# Multi-tenancy
TENANT_SCHEMA_PREFIX=tenant_
ENABLE_SCHEMA_ISOLATION=true
```

### Database Setup

```bash
# Run migrations
psql -d timbuktoo -f timbuktoo/database/migrations/001_initial_schema.sql
psql -d timbuktoo -f timbuktoo/database/migrations/002_multi_tenant.sql

# Load pricing plans (already in migration)
# Plans: starter_monthly, pro_monthly, enterprise
```

### API Server

```bash
# Run FastAPI server
uvicorn timbuktoo.api.app:app --host 0.0.0.0 --port 8000

# Or with gunicorn for production
gunicorn timbuktoo.api.app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## Monitoring

Track per-tenant metrics:
- API usage
- Cost per tenant
- Itinerary creation rate
- Quota utilization
- Churn risk indicators

Prometheus metrics:
```
timbuktoo_trip_requests_total{tenant="acme",tier="starter"}
timbuktoo_quota_utilization{tenant="acme",resource="itineraries"}
timbuktoo_tenant_cost_usd{tenant="acme"}
```

## Future Enhancements

- [ ] Self-service billing portal
- [ ] Custom branding per tenant
- [ ] API key management
- [ ] Webhook notifications
- [ ] Usage analytics dashboard
- [ ] Automated tier recommendations
- [ ] Volume-based discounts
- [ ] Annual billing options

## Support

For multi-tenancy questions:
- Starter: Email support@timbuktoo.ai
- Pro: Priority support via chat
- Enterprise: Dedicated Slack channel + account manager
