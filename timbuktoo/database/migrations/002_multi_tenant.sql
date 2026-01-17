-- Multi-Tenant Schema Extensions
-- PostgreSQL 14+

-- Tenants table
CREATE TABLE tenants (
    tenant_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_name TEXT UNIQUE NOT NULL,
    company_name TEXT,
    schema_name TEXT UNIQUE NOT NULL,
    subscription_tier TEXT NOT NULL CHECK (subscription_tier IN ('starter', 'pro', 'enterprise')),
    status TEXT NOT NULL CHECK (status IN ('active', 'suspended', 'trial', 'cancelled')),
    trial_ends_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    settings JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_tenants_schema ON tenants(schema_name);
CREATE INDEX idx_tenants_tier ON tenants(subscription_tier);
CREATE INDEX idx_tenants_status ON tenants(status);

-- Subscriptions table
CREATE TABLE subscriptions (
    subscription_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    plan_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'cancelled', 'past_due', 'trialing')),
    current_period_start TIMESTAMP NOT NULL,
    current_period_end TIMESTAMP NOT NULL,
    cancel_at_period_end BOOLEAN DEFAULT false,
    monthly_price_usd DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

CREATE INDEX idx_subscriptions_tenant ON subscriptions(tenant_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);

-- Usage quotas table
CREATE TABLE usage_quotas (
    quota_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    resource_type TEXT NOT NULL, -- 'itineraries', 'api_calls', 'storage_gb'
    quota_limit INTEGER NOT NULL,
    current_usage INTEGER DEFAULT 0,
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_quotas_tenant ON usage_quotas(tenant_id);
CREATE INDEX idx_quotas_resource ON usage_quotas(resource_type);
CREATE UNIQUE INDEX idx_quotas_tenant_resource ON usage_quotas(tenant_id, resource_type, period_start);

-- Onboarding sessions table
CREATE TABLE onboarding_sessions (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    current_step TEXT NOT NULL CHECK (current_step IN ('signup', 'preferences', 'city_selection', 'itinerary', 'feedback', 'completed')),
    preferences JSONB,
    selected_city_id UUID,
    itinerary JSONB,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_onboarding_tenant ON onboarding_sessions(tenant_id);
CREATE INDEX idx_onboarding_email ON onboarding_sessions(email);
CREATE INDEX idx_onboarding_step ON onboarding_sessions(current_step);

-- Tenant users (for multi-user tenants)
CREATE TABLE tenant_users (
    tenant_user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tenant_id, user_id)
);

CREATE INDEX idx_tenant_users_tenant ON tenant_users(tenant_id);
CREATE INDEX idx_tenant_users_user ON tenant_users(user_id);

-- Pricing plans table
CREATE TABLE pricing_plans (
    plan_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    tier TEXT NOT NULL CHECK (tier IN ('starter', 'pro', 'enterprise')),
    monthly_price_usd DECIMAL(10, 2) NOT NULL,
    annual_price_usd DECIMAL(10, 2),
    features JSONB NOT NULL,
    quotas JSONB NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default pricing plans
INSERT INTO pricing_plans (plan_id, name, tier, monthly_price_usd, annual_price_usd, features, quotas) VALUES
('starter_monthly', 'Starter', 'starter', 29.00, 290.00,
    '{"itineraries": "10 per month", "cities": "5 pilot cities", "support": "email"}',
    '{"itineraries_per_month": 10, "max_users": 1, "max_api_cost_per_trip": 0.80}'
),
('pro_monthly', 'Pro', 'pro', 99.00, 990.00,
    '{"itineraries": "unlimited", "cities": "all cities including premium", "support": "priority email + chat", "analytics": "advanced"}',
    '{"itineraries_per_month": -1, "max_users": 10, "max_api_cost_per_trip": 1.50}'
),
('enterprise', 'Enterprise', 'enterprise', 999.00, NULL,
    '{"itineraries": "unlimited", "cities": "all cities + custom", "support": "dedicated account manager + phone", "analytics": "custom dashboards", "sla": "99.9%", "compliance": "SOC-2 + HIPAA"}',
    '{"itineraries_per_month": -1, "max_users": -1, "max_api_cost_per_trip": 3.00, "dedicated_schema": true}'
);

-- Modify trips table to add tenant_id
ALTER TABLE trips ADD COLUMN tenant_id UUID REFERENCES tenants(tenant_id) ON DELETE CASCADE;
CREATE INDEX idx_trips_tenant ON trips(tenant_id);

-- Modify feedback table to add tenant_id
ALTER TABLE feedback ADD COLUMN tenant_id UUID REFERENCES tenants(tenant_id) ON DELETE CASCADE;
CREATE INDEX idx_feedback_tenant ON feedback(tenant_id);

-- Modify cost_tracking table to add tenant_id
ALTER TABLE cost_tracking ADD COLUMN tenant_id UUID REFERENCES tenants(tenant_id) ON DELETE CASCADE;
CREATE INDEX idx_cost_tenant ON cost_tracking(tenant_id);

-- Update trigger for tenants
CREATE TRIGGER update_tenants_modtime
    BEFORE UPDATE ON tenants
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_subscriptions_modtime
    BEFORE UPDATE ON subscriptions
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_quotas_modtime
    BEFORE UPDATE ON usage_quotas
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_onboarding_modtime
    BEFORE UPDATE ON onboarding_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();
