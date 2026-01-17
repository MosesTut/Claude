"""Tenant management utilities"""

from typing import Dict, Any, Optional
import uuid
from datetime import datetime, timedelta
import re

from ..database.models import (
    Tenant, Subscription, UsageQuota, TenantUser, PricingPlan, SessionLocal
)
from ..utils.logger import get_logger

logger = get_logger(__name__)


class TenantManager:
    """Manages multi-tenant operations"""

    def __init__(self):
        pass

    def create_tenant(
        self,
        tenant_name: str,
        company_name: str,
        email: str,
        plan_id: str = "starter_monthly",
        trial_days: int = 14
    ) -> Dict[str, Any]:
        """
        Create a new tenant with subscription

        Args:
            tenant_name: Unique tenant identifier
            company_name: Company name
            email: Primary contact email
            plan_id: Pricing plan ID
            trial_days: Trial period in days

        Returns:
            {
                "success": bool,
                "tenant_id": str,
                "schema_name": str,
                "subscription": {...}
            }
        """
        db = SessionLocal()
        try:
            # Validate tenant_name
            if not self._validate_tenant_name(tenant_name):
                return {
                    "success": False,
                    "error": "Invalid tenant name. Use lowercase alphanumeric and hyphens only."
                }

            # Check if tenant already exists
            existing = db.query(Tenant).filter(Tenant.tenant_name == tenant_name).first()
            if existing:
                return {
                    "success": False,
                    "error": f"Tenant {tenant_name} already exists"
                }

            # Get pricing plan
            plan = db.query(PricingPlan).filter(PricingPlan.plan_id == plan_id).first()
            if not plan:
                return {
                    "success": False,
                    "error": f"Pricing plan {plan_id} not found"
                }

            # Create schema name
            schema_name = f"tenant_{tenant_name.replace('-', '_')}"

            # Create tenant
            tenant = Tenant(
                tenant_name=tenant_name,
                company_name=company_name,
                schema_name=schema_name,
                subscription_tier=plan.tier,
                status="trial" if trial_days > 0 else "active",
                trial_ends_at=datetime.utcnow() + timedelta(days=trial_days) if trial_days > 0 else None,
                settings={
                    "primary_email": email,
                    "created_by": "system"
                }
            )
            db.add(tenant)
            db.flush()

            # Create subscription
            now = datetime.utcnow()
            subscription = Subscription(
                tenant_id=tenant.tenant_id,
                plan_id=plan_id,
                status="trialing" if trial_days > 0 else "active",
                current_period_start=now,
                current_period_end=now + timedelta(days=30),
                monthly_price_usd=plan.monthly_price_usd,
                metadata={
                    "trial_days": trial_days,
                    "auto_created": True
                }
            )
            db.add(subscription)
            db.flush()

            # Create usage quotas based on plan
            quotas = plan.quotas
            self._create_quotas(db, tenant.tenant_id, quotas, now)

            # Create database schema for tenant isolation
            self._create_tenant_schema(db, schema_name)

            db.commit()

            logger.info(
                f"Tenant created: {tenant_name}",
                extra={
                    "tenant_id": str(tenant.tenant_id),
                    "tier": plan.tier,
                    "trial_days": trial_days
                }
            )

            return {
                "success": True,
                "tenant_id": str(tenant.tenant_id),
                "tenant_name": tenant_name,
                "schema_name": schema_name,
                "subscription": subscription.to_dict(),
                "status": tenant.status,
                "trial_ends_at": tenant.trial_ends_at.isoformat() if tenant.trial_ends_at else None
            }

        except Exception as e:
            logger.error(f"Failed to create tenant: {str(e)}")
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            db.close()

    def get_tenant(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Get tenant details"""
        db = SessionLocal()
        try:
            tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
            if not tenant:
                return None

            # Get subscription
            subscription = db.query(Subscription).filter(
                Subscription.tenant_id == tenant_id,
                Subscription.status.in_(["active", "trialing"])
            ).first()

            # Get quotas
            quotas = db.query(UsageQuota).filter(UsageQuota.tenant_id == tenant_id).all()

            return {
                "tenant": tenant.to_dict(),
                "subscription": subscription.to_dict() if subscription else None,
                "quotas": [q.to_dict() for q in quotas]
            }

        finally:
            db.close()

    def check_quota(self, tenant_id: str, resource_type: str) -> Dict[str, Any]:
        """
        Check if tenant has quota available

        Returns:
            {
                "allowed": bool,
                "quota_limit": int,
                "current_usage": int,
                "remaining": int
            }
        """
        db = SessionLocal()
        try:
            # Get current quota
            now = datetime.utcnow()
            quota = db.query(UsageQuota).filter(
                UsageQuota.tenant_id == tenant_id,
                UsageQuota.resource_type == resource_type,
                UsageQuota.period_start <= now,
                UsageQuota.period_end >= now
            ).first()

            if not quota:
                logger.warning(f"No quota found for tenant {tenant_id}, resource {resource_type}")
                return {
                    "allowed": False,
                    "error": "No quota configured"
                }

            # -1 means unlimited
            if quota.quota_limit == -1:
                return {
                    "allowed": True,
                    "quota_limit": -1,
                    "current_usage": quota.current_usage,
                    "remaining": -1,
                    "unlimited": True
                }

            allowed = quota.current_usage < quota.quota_limit

            return {
                "allowed": allowed,
                "quota_limit": quota.quota_limit,
                "current_usage": quota.current_usage,
                "remaining": max(0, quota.quota_limit - quota.current_usage)
            }

        finally:
            db.close()

    def increment_usage(self, tenant_id: str, resource_type: str, amount: int = 1) -> bool:
        """Increment usage counter"""
        db = SessionLocal()
        try:
            now = datetime.utcnow()
            quota = db.query(UsageQuota).filter(
                UsageQuota.tenant_id == tenant_id,
                UsageQuota.resource_type == resource_type,
                UsageQuota.period_start <= now,
                UsageQuota.period_end >= now
            ).first()

            if not quota:
                logger.error(f"No quota found for tenant {tenant_id}, resource {resource_type}")
                return False

            quota.current_usage += amount
            db.commit()

            logger.info(
                f"Usage incremented for tenant {tenant_id}",
                extra={
                    "resource": resource_type,
                    "amount": amount,
                    "new_usage": quota.current_usage
                }
            )

            return True

        except Exception as e:
            logger.error(f"Failed to increment usage: {str(e)}")
            db.rollback()
            return False
        finally:
            db.close()

    def upgrade_subscription(self, tenant_id: str, new_plan_id: str) -> Dict[str, Any]:
        """Upgrade tenant subscription"""
        db = SessionLocal()
        try:
            # Get tenant
            tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
            if not tenant:
                return {"success": False, "error": "Tenant not found"}

            # Get new plan
            new_plan = db.query(PricingPlan).filter(PricingPlan.plan_id == new_plan_id).first()
            if not new_plan:
                return {"success": False, "error": "Plan not found"}

            # Get current subscription
            subscription = db.query(Subscription).filter(
                Subscription.tenant_id == tenant_id,
                Subscription.status.in_(["active", "trialing"])
            ).first()

            if subscription:
                # Update subscription
                subscription.plan_id = new_plan_id
                subscription.monthly_price_usd = new_plan.monthly_price_usd
                subscription.status = "active"
            else:
                # Create new subscription
                now = datetime.utcnow()
                subscription = Subscription(
                    tenant_id=tenant_id,
                    plan_id=new_plan_id,
                    status="active",
                    current_period_start=now,
                    current_period_end=now + timedelta(days=30),
                    monthly_price_usd=new_plan.monthly_price_usd
                )
                db.add(subscription)

            # Update tenant tier
            tenant.subscription_tier = new_plan.tier
            tenant.status = "active"

            # Update quotas
            now = datetime.utcnow()
            period_end = now + timedelta(days=30)

            for resource, limit in new_plan.quotas.items():
                if resource.endswith("_per_month"):
                    resource_type = resource.replace("_per_month", "")
                    quota = db.query(UsageQuota).filter(
                        UsageQuota.tenant_id == tenant_id,
                        UsageQuota.resource_type == resource_type
                    ).first()

                    if quota:
                        quota.quota_limit = limit
                    else:
                        quota = UsageQuota(
                            tenant_id=tenant_id,
                            resource_type=resource_type,
                            quota_limit=limit,
                            period_start=now,
                            period_end=period_end
                        )
                        db.add(quota)

            db.commit()

            logger.info(
                f"Subscription upgraded for tenant {tenant_id}",
                extra={"new_plan": new_plan_id, "tier": new_plan.tier}
            )

            return {
                "success": True,
                "subscription": subscription.to_dict(),
                "tier": new_plan.tier
            }

        except Exception as e:
            logger.error(f"Failed to upgrade subscription: {str(e)}")
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()

    def _validate_tenant_name(self, tenant_name: str) -> bool:
        """Validate tenant name format"""
        # Must be lowercase alphanumeric with hyphens, 3-63 chars
        pattern = r'^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$'
        return bool(re.match(pattern, tenant_name))

    def _create_quotas(self, db, tenant_id: uuid.UUID, quotas: Dict[str, Any], period_start: datetime):
        """Create usage quotas from plan"""
        period_end = period_start + timedelta(days=30)

        # Extract quota limits
        itinerary_limit = quotas.get("itineraries_per_month", 10)

        quota_configs = [
            ("itineraries", itinerary_limit)
        ]

        for resource_type, limit in quota_configs:
            quota = UsageQuota(
                tenant_id=tenant_id,
                resource_type=resource_type,
                quota_limit=limit,
                current_usage=0,
                period_start=period_start,
                period_end=period_end
            )
            db.add(quota)

    def _create_tenant_schema(self, db, schema_name: str):
        """Create database schema for tenant isolation"""
        try:
            # Create schema
            db.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
            logger.info(f"Created schema: {schema_name}")
        except Exception as e:
            logger.error(f"Failed to create schema {schema_name}: {str(e)}")
            raise


# Singleton instance
_tenant_manager = None

def get_tenant_manager() -> TenantManager:
    """Get or create tenant manager instance"""
    global _tenant_manager
    if _tenant_manager is None:
        _tenant_manager = TenantManager()
    return _tenant_manager
