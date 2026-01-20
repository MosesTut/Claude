from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Subscription Details
    tier = Column(String, default="free", nullable=False)  # "free", "pro_monthly", "pro_annual"
    status = Column(String, default="active", nullable=False)  # "active", "cancelled", "expired", "trial"

    # RevenueCat Integration
    revenuecat_customer_id = Column(String, nullable=True, index=True)
    revenuecat_entitlement = Column(String, nullable=True)  # "pro"

    # Pricing
    price = Column(Numeric(10, 2), nullable=True)  # 9.99 or 79.99
    currency = Column(String, default="USD", nullable=False)

    # Trial
    is_trial = Column(Boolean, default=False, nullable=False)
    trial_ends_at = Column(DateTime(timezone=True), nullable=True)

    # Dates
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    current_period_start = Column(DateTime(timezone=True), nullable=True)
    current_period_end = Column(DateTime(timezone=True), nullable=True)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
