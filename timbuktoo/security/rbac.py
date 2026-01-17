"""Role-Based Access Control (RBAC)"""

from typing import Dict, Any, Optional, List
from enum import Enum
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

from ..database.models import User, SessionLocal
from ..utils.logger import get_logger

logger = get_logger(__name__)


class Role(Enum):
    """User roles"""
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"


class Permission(Enum):
    """Permissions"""
    READ_TRIPS = "read_trips"
    CREATE_TRIPS = "create_trips"
    UPDATE_TRIPS = "update_trips"
    DELETE_TRIPS = "delete_trips"
    MANAGE_USERS = "manage_users"
    VIEW_METRICS = "view_metrics"
    MANAGE_DATA = "manage_data"


# Role to permissions mapping
ROLE_PERMISSIONS = {
    Role.ADMIN: [
        Permission.READ_TRIPS,
        Permission.CREATE_TRIPS,
        Permission.UPDATE_TRIPS,
        Permission.DELETE_TRIPS,
        Permission.MANAGE_USERS,
        Permission.VIEW_METRICS,
        Permission.MANAGE_DATA
    ],
    Role.OPERATOR: [
        Permission.READ_TRIPS,
        Permission.CREATE_TRIPS,
        Permission.VIEW_METRICS
    ],
    Role.VIEWER: [
        Permission.READ_TRIPS,
        Permission.VIEW_METRICS
    ]
}


class AuthManager:
    """Manages authentication and authorization"""

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = os.getenv("JWT_SECRET", "dev_secret_key_change_in_production")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 60

    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, user_id: str, role: str) -> str:
        """Create JWT access token"""
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode = {
            "user_id": user_id,
            "role": role,
            "exp": expire
        }
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            logger.error(f"Token verification failed: {str(e)}")
            return None

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with username and password"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()

            if not user:
                logger.warning(f"User not found: {username}")
                return None

            if not user.is_active:
                logger.warning(f"User is inactive: {username}")
                return None

            if not self.verify_password(password, user.password_hash):
                logger.warning(f"Invalid password for user: {username}")
                return None

            # Update last login
            user.last_login = datetime.utcnow()
            db.commit()

            logger.info(f"User authenticated: {username}")

            return {
                "user_id": str(user.user_id),
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "mfa_enabled": user.mfa_enabled
            }

        finally:
            db.close()

    def has_permission(self, role: str, permission: Permission) -> bool:
        """Check if a role has a specific permission"""
        try:
            role_enum = Role(role)
            return permission in ROLE_PERMISSIONS.get(role_enum, [])
        except ValueError:
            logger.error(f"Invalid role: {role}")
            return False

    def require_permission(self, token: str, permission: Permission) -> bool:
        """Verify token and check permission"""
        payload = self.verify_token(token)

        if not payload:
            return False

        role = payload.get("role")
        if not role:
            return False

        return self.has_permission(role, permission)


# Singleton instance
_auth_manager = None

def get_auth_manager() -> AuthManager:
    """Get or create auth manager instance"""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager
