"""Encryption utilities for data at rest and in transit"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
import os

from ..utils.logger import get_logger

logger = get_logger(__name__)


class EncryptionManager:
    """Handles encryption and decryption of sensitive data"""

    def __init__(self):
        encryption_key = os.getenv("ENCRYPTION_KEY")

        if not encryption_key:
            logger.warning("No ENCRYPTION_KEY found, generating temporary key")
            encryption_key = Fernet.generate_key().decode()
            logger.warning("TEMPORARY KEY GENERATED - DO NOT USE IN PRODUCTION")

        # Ensure key is bytes
        if isinstance(encryption_key, str):
            encryption_key = encryption_key.encode()

        # If key is not valid Fernet key format, derive one
        if len(encryption_key) != 44:  # Fernet keys are 44 bytes base64 encoded
            encryption_key = self._derive_key(encryption_key)

        self.fernet = Fernet(encryption_key)

    def _derive_key(self, password: bytes) -> bytes:
        """Derive a Fernet key from a password"""
        salt = b'timbuktoo_salt_v1'  # In production, use unique salt per environment
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key

    def encrypt(self, data: str) -> str:
        """Encrypt string data"""
        try:
            encrypted = self.fernet.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Encryption failed: {str(e)}")
            raise

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        try:
            decrypted = self.fernet.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            raise

    def encrypt_dict(self, data: dict, sensitive_fields: list) -> dict:
        """Encrypt specific fields in a dictionary"""
        result = data.copy()
        for field in sensitive_fields:
            if field in result and result[field]:
                result[field] = self.encrypt(str(result[field]))
        return result

    def decrypt_dict(self, data: dict, sensitive_fields: list) -> dict:
        """Decrypt specific fields in a dictionary"""
        result = data.copy()
        for field in sensitive_fields:
            if field in result and result[field]:
                result[field] = self.decrypt(result[field])
        return result


# Singleton instance
_encryption_manager = None

def get_encryption_manager() -> EncryptionManager:
    """Get or create encryption manager instance"""
    global _encryption_manager
    if _encryption_manager is None:
        _encryption_manager = EncryptionManager()
    return _encryption_manager
