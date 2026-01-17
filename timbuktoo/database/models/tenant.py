"""Multi-tenant models"""

from sqlalchemy import Column, String, DateTime, Integer, DECIMAL, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid

from .base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    tenant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_name = Column(String, unique=True, nullable=False)
    company_name = Column(String)
    schema_name = Column(String, unique=True, nullable=False)
    subscription_tier = Column(String, nullable=False)  # starter, pro, enterprise
    status = Column(String, nullable=False)  # active, suspended, trial, cancelled
    trial_ends_at = Column(DateTime(timezone=True))
    settings = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "tenant_id": str(self.tenant_id),
            "tenant_name": self.tenant_name,
            "company_name": self.company_name,
            "schema_name": self.schema_name,
            "subscription_tier": self.subscription_tier,
            "status": self.status,
            "trial_ends_at": self.trial_ends_at.isoformat() if self.trial_ends_at else None,
            "settings": self.settings,
            "created_at": self.created_at.isoformat()
        }


class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    plan_id = Column(String, nullable=False)
    status = Column(String, nullable=False)  # active, cancelled, past_due, trialing
    current_period_start = Column(DateTime(timezone=True), nullable=False)
    current_period_end = Column(DateTime(timezone=True), nullable=False)
    cancel_at_period_end = Column(Boolean, default=False)
    monthly_price_usd = Column(DECIMAL(10, 2), nullable=False)
    metadata = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "subscription_id": str(self.subscription_id),
            "tenant_id": str(self.tenant_id),
            "plan_id": self.plan_id,
            "status": self.status,
            "current_period_start": self.current_period_start.isoformat(),
            "current_period_end": self.current_period_end.isoformat(),
            "cancel_at_period_end": self.cancel_at_period_end,
            "monthly_price_usd": float(self.monthly_price_usd),
            "metadata": self.metadata
        }


class UsageQuota(Base):
    __tablename__ = "usage_quotas"

    quota_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    resource_type = Column(String, nullable=False)  # itineraries, api_calls, storage_gb
    quota_limit = Column(Integer, nullable=False)
    current_usage = Column(Integer, default=0)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "quota_id": str(self.quota_id),
            "tenant_id": str(self.tenant_id),
            "resource_type": self.resource_type,
            "quota_limit": self.quota_limit,
            "current_usage": self.current_usage,
            "remaining": max(0, self.quota_limit - self.current_usage) if self.quota_limit != -1 else -1,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat()
        }


class OnboardingSession(Base):
    __tablename__ = "onboarding_sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"))
    email = Column(String, nullable=False)
    current_step = Column(String, nullable=False)  # signup, preferences, city_selection, itinerary, feedback, completed
    preferences = Column(JSONB)
    selected_city_id = Column(UUID(as_uuid=True))
    itinerary = Column(JSONB)
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "session_id": str(self.session_id),
            "tenant_id": str(self.tenant_id) if self.tenant_id else None,
            "email": self.email,
            "current_step": self.current_step,
            "preferences": self.preferences,
            "selected_city_id": str(self.selected_city_id) if self.selected_city_id else None,
            "itinerary": self.itinerary,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat()
        }


class TenantUser(Base):
    __tablename__ = "tenant_users"

    tenant_user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False)  # owner, admin, member, viewer
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "tenant_user_id": str(self.tenant_user_id),
            "tenant_id": str(self.tenant_id),
            "user_id": str(self.user_id),
            "role": self.role,
            "created_at": self.created_at.isoformat()
        }


class PricingPlan(Base):
    __tablename__ = "pricing_plans"

    plan_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    tier = Column(String, nullable=False)  # starter, pro, enterprise
    monthly_price_usd = Column(DECIMAL(10, 2), nullable=False)
    annual_price_usd = Column(DECIMAL(10, 2))
    features = Column(JSONB, nullable=False)
    quotas = Column(JSONB, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "plan_id": self.plan_id,
            "name": self.name,
            "tier": self.tier,
            "monthly_price_usd": float(self.monthly_price_usd),
            "annual_price_usd": float(self.annual_price_usd) if self.annual_price_usd else None,
            "features": self.features,
            "quotas": self.quotas,
            "is_active": self.is_active
        }
