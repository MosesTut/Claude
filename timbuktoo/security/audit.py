"""Audit logging for SOC-2 compliance"""

from typing import Dict, Any, Optional
import uuid
from datetime import datetime

from ..database.models import AuditLog, SessionLocal
from ..utils.logger import get_logger

logger = get_logger(__name__)


class AuditLogger:
    """Logs security and compliance events"""

    def __init__(self):
        pass

    def log_event(
        self,
        event_type: str,
        action: str,
        status: str,
        user_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Log an audit event

        Args:
            event_type: Type of event (e.g., 'authentication', 'data_access', 'trip_creation')
            action: Action performed (e.g., 'login', 'read', 'create')
            status: Result status ('success', 'failure', 'error')
            user_id: User who performed the action
            resource_type: Type of resource accessed (e.g., 'trip', 'user')
            resource_id: ID of resource accessed
            ip_address: Client IP address
            user_agent: Client user agent
            details: Additional context
        """

        db = SessionLocal()
        try:
            audit_log = AuditLog(
                event_type=event_type,
                action=action,
                status=status,
                user_id=uuid.UUID(user_id) if user_id else None,
                resource_type=resource_type,
                resource_id=uuid.UUID(resource_id) if resource_id else None,
                ip_address=ip_address,
                user_agent=user_agent,
                details=details
            )

            db.add(audit_log)
            db.commit()

            logger.info(
                f"Audit event logged: {event_type}",
                extra={
                    "event_type": event_type,
                    "action": action,
                    "status": status,
                    "user_id": user_id
                }
            )

        except Exception as e:
            logger.error(f"Failed to log audit event: {str(e)}")
            db.rollback()
        finally:
            db.close()

    def log_authentication(
        self,
        username: str,
        success: bool,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """Log authentication attempt"""
        self.log_event(
            event_type="authentication",
            action="login",
            status="success" if success else "failure",
            ip_address=ip_address,
            user_agent=user_agent,
            details={"username": username, **(details or {})}
        )

    def log_data_access(
        self,
        user_id: str,
        resource_type: str,
        resource_id: str,
        action: str = "read",
        success: bool = True,
        details: Optional[Dict[str, Any]] = None
    ):
        """Log data access"""
        self.log_event(
            event_type="data_access",
            action=action,
            status="success" if success else "failure",
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details
        )

    def log_trip_creation(
        self,
        user_id: Optional[str],
        trip_id: str,
        city_id: str,
        success: bool = True,
        details: Optional[Dict[str, Any]] = None
    ):
        """Log trip creation"""
        self.log_event(
            event_type="trip_creation",
            action="create",
            status="success" if success else "failure",
            user_id=user_id,
            resource_type="trip",
            resource_id=trip_id,
            details={"city_id": city_id, **(details or {})}
        )

    def log_configuration_change(
        self,
        user_id: str,
        config_key: str,
        old_value: Any,
        new_value: Any,
        success: bool = True
    ):
        """Log configuration change"""
        self.log_event(
            event_type="configuration_change",
            action="update",
            status="success" if success else "failure",
            user_id=user_id,
            details={
                "config_key": config_key,
                "old_value": str(old_value),
                "new_value": str(new_value)
            }
        )

    def get_audit_trail(
        self,
        event_type: Optional[str] = None,
        user_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> list:
        """Query audit logs"""
        db = SessionLocal()
        try:
            query = db.query(AuditLog)

            if event_type:
                query = query.filter(AuditLog.event_type == event_type)
            if user_id:
                query = query.filter(AuditLog.user_id == user_id)
            if resource_id:
                query = query.filter(AuditLog.resource_id == resource_id)
            if start_date:
                query = query.filter(AuditLog.timestamp >= start_date)
            if end_date:
                query = query.filter(AuditLog.timestamp <= end_date)

            logs = query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
            return [log.to_dict() for log in logs]

        finally:
            db.close()


# Singleton instance
_audit_logger = None

def get_audit_logger() -> AuditLogger:
    """Get or create audit logger instance"""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger
