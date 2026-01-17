"""Configuration settings"""

import os
from typing import Dict, Any
import yaml
from pydantic import BaseModel, Field

from ..utils.logger import get_logger

logger = get_logger(__name__)


class AgentConfig(BaseModel):
    """Agent configuration"""
    concierge_tokens: int = 38000
    local_expert_tokens: int = 15000
    city_selection_tokens: int = 8000
    model: str = "claude-sonnet-4-5-20250929"
    temperature: float = 0.7


class CostConfig(BaseModel):
    """Cost control configuration"""
    max_trip_cost_usd: float = 0.80
    vector_chunks: int = 35
    enable_degradation: bool = True
    cache_enabled: bool = True


class SecurityConfig(BaseModel):
    """Security configuration"""
    encryption_enabled: bool = True
    mfa_required: bool = False
    session_timeout_minutes: int = 60
    audit_logging_enabled: bool = True


class DatabaseConfig(BaseModel):
    """Database configuration"""
    url: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", ""))
    pool_size: int = 10
    max_overflow: int = 20
    vector_db_path: str = Field(default_factory=lambda: os.getenv("VECTOR_DB_PATH", "./data/vector_db"))


class MonitoringConfig(BaseModel):
    """Monitoring configuration"""
    prometheus_enabled: bool = True
    prometheus_port: int = 9090
    log_level: str = "INFO"


class Settings(BaseModel):
    """Main settings class"""
    environment: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    agents: AgentConfig = Field(default_factory=AgentConfig)
    cost: CostConfig = Field(default_factory=CostConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)

    @classmethod
    def load_from_yaml(cls, config_path: str) -> "Settings":
        """Load settings from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
            return cls(**config_data)
        except Exception as e:
            logger.error(f"Failed to load config from {config_path}: {str(e)}")
            return cls()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.model_dump()


# Singleton instance
_settings = None

def get_settings() -> Settings:
    """Get or create settings instance"""
    global _settings
    if _settings is None:
        # Try to load from config file
        config_path = os.getenv("CONFIG_PATH", "config/timbuktoo.yaml")
        if os.path.exists(config_path):
            _settings = Settings.load_from_yaml(config_path)
            logger.info(f"Loaded settings from {config_path}")
        else:
            _settings = Settings()
            logger.info("Using default settings")
    return _settings
