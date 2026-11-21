"""
Application configuration for the Smart Campus Facility Platform.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Smart Campus Facility Platform"
    APP_VERSION: str = "2.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = Field(default="sqlite:///./smart_campus.db")

    # Security & JWT
    SECRET_KEY: str = Field(default="dev-insecure-secret-key-change-in-production-192524402")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # Campus Booking Policies
    DEFAULT_MAX_BOOKING_MINUTES: int = 180
    DEFAULT_SENSOR_TEMP_THRESHOLD: float = 28.0

    # SLA Policies (in hours)
    SLA_HOURS_M1: int = 2
    SLA_HOURS_M2: int = 8
    SLA_HOURS_M3: int = 24
    SLA_HOURS_M4: int = 72

    # External integrations
    CALENDAR_SERVICE_URL: str = "https://calendar.campus.internal/api/v1"
    ISSUE_TRACKER_URL: str = "https://jira.campus.internal/rest/api/2"
    INTEGRATION_TIMEOUT_SECONDS: float = 2.0
    MAX_SYNC_RETRIES: int = 3

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
