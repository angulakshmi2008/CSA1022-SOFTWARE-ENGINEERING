import os
from typing import Dict, Any

class Settings:
    PROJECT_NAME: str = "Omnichannel Order Fulfilment Platform (FulfillIQ)"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "academic-assignment-fulfiliq-secure-jwt-key-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GATEWAY_HMAC_SECRET: str = os.getenv("GATEWAY_HMAC_SECRET", "webhook-secret-hmac-sha256-key")
    
    # Database
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fulfiliq.db")))
    
    # Business Rules
    RESERVATION_LEASE_MINUTES: int = 15
    DISPATCH_SLA_HOURS: int = 24
    DEFAULT_REFUND_APPROVAL_THRESHOLD: float = 50.00
    
    # 12 Operating Regions Configuration
    INITIAL_REGIONS: Dict[str, Dict[str, Any]] = {
        "US-EAST": {"name": "US East (New York Hub)", "tax_rate": 0.0825, "shipping_fee": 5.00, "refund_threshold": 50.00},
        "US-WEST": {"name": "US West (California Hub)", "tax_rate": 0.0925, "shipping_fee": 5.50, "refund_threshold": 50.00},
        "US-CENTRAL": {"name": "US Central (Chicago Hub)", "tax_rate": 0.0750, "shipping_fee": 4.50, "refund_threshold": 50.00},
        "CAN-EAST": {"name": "Canada East (Toronto Hub)", "tax_rate": 0.1300, "shipping_fee": 6.00, "refund_threshold": 60.00},
        "UK-SOUTH": {"name": "UK South (London Hub)", "tax_rate": 0.2000, "shipping_fee": 4.00, "refund_threshold": 40.00},
        "EU-CENTRAL": {"name": "EU Central (Frankfurt Hub)", "tax_rate": 0.1900, "shipping_fee": 5.00, "refund_threshold": 45.00},
        "EU-WEST": {"name": "EU West (Paris Hub)", "tax_rate": 0.2000, "shipping_fee": 5.00, "refund_threshold": 45.00},
        "APAC-EAST": {"name": "APAC East (Tokyo Hub)", "tax_rate": 0.1000, "shipping_fee": 7.00, "refund_threshold": 75.00},
        "APAC-SOUTH": {"name": "APAC South (Singapore Hub)", "tax_rate": 0.0900, "shipping_fee": 6.50, "refund_threshold": 55.00},
        "AUS-EAST": {"name": "Australia East (Sydney Hub)", "tax_rate": 0.1000, "shipping_fee": 7.50, "refund_threshold": 65.00},
        "LATAM-BR": {"name": "Latin America (Sao Paulo Hub)", "tax_rate": 0.1700, "shipping_fee": 8.00, "refund_threshold": 40.00},
        "MEA-UAE": {"name": "Middle East (Dubai Hub)", "tax_rate": 0.0500, "shipping_fee": 9.00, "refund_threshold": 70.00},
    }

settings = Settings()
