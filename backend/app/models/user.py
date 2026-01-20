from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    # Profile
    display_name = Column(String, nullable=True)

    # Consent
    ai_disclosure_accepted = Column(Boolean, default=False, nullable=False)
    data_use_accepted = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
