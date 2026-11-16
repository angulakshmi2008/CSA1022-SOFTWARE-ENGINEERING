import hashlib
import json
import base64
import time
from typing import Optional, Dict, Any
from .models import Role

class AuthenticationError(Exception):
    """Raised when authentication credentials or token are invalid."""
    pass

class PermissionDeniedError(Exception):
    """Raised when an authenticated user attempts an unauthorized action."""
    pass

# Synthetic test user directory
TEST_USERS = {
    "cust_alex": {"user_id": "cust_alex", "password_hash": "alex123", "role": Role.CUSTOMER, "email": "alex@example.com"},
    "picker_john": {"user_id": "picker_john", "password_hash": "picker123", "role": Role.WAREHOUSE_PICKER, "email": "john@retailer.com", "warehouse_id": "WH-NORTH-01"},
    "support_sarah": {"user_id": "support_sarah", "password_hash": "support123", "role": Role.SUPPORT_AGENT, "email": "sarah@retailer.com"},
    "finance_frank": {"user_id": "finance_frank", "password_hash": "finance123", "role": Role.FINANCE_REVIEWER, "email": "frank@retailer.com"},
    "manager_mary": {"user_id": "manager_mary", "password_hash": "manager123", "role": Role.STORE_MANAGER, "email": "mary@retailer.com", "warehouse_id": "WH-NORTH-01"},
    "admin_alice": {"user_id": "admin_alice", "password_hash": "admin123", "role": Role.ADMINISTRATOR, "email": "alice@retailer.com"},
}

TOKEN_SECRET = "synthetic-assignment-token-secret-csa10"

class AuthService:
    @staticmethod
    def login(username: str, password: str) -> Dict[str, Any]:
        """Authenticate user and return a role-scoped session token."""
        user = TEST_USERS.get(username)
        if not user or user["password_hash"] != password:
            raise AuthenticationError("Invalid username or password.")

        expiry = int(time.time()) + 3600  # 1 hour session TTL
        payload = {
            "user_id": user["user_id"],
            "role": user["role"].value,
            "email": user["email"],
            "warehouse_id": user.get("warehouse_id"),
            "exp": expiry
        }
        raw_payload = json.dumps(payload)
        sig = hashlib.sha256(f"{raw_payload}:{TOKEN_SECRET}".encode()).hexdigest()
        token = base64.b64encode(f"{raw_payload}||{sig}".encode()).decode()

        return {
            "token": token,
            "user_id": user["user_id"],
            "role": user["role"],
            "email": user["email"],
            "expires_in": 3600
        }

    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """Verify session token integrity, expiry, and return claims."""
        try:
            decoded = base64.b64decode(token.encode()).decode()
            raw_payload, sig = decoded.split("||")
            expected_sig = hashlib.sha256(f"{raw_payload}:{TOKEN_SECRET}".encode()).hexdigest()
            if sig != expected_sig:
                raise AuthenticationError("Invalid session token signature.")

            claims = json.loads(raw_payload)
            if claims.get("exp", 0) < time.time():
                raise AuthenticationError("Session token has expired.")

            return claims
        except Exception as e:
            if isinstance(e, AuthenticationError):
                raise
            raise AuthenticationError(f"Malformed authentication token: {str(e)}")

    @staticmethod
    def require_role(token: str, allowed_roles: list[Role]) -> Dict[str, Any]:
        """Enforce role-based access control (RBAC)."""
        claims = AuthService.verify_token(token)
        user_role = Role(claims.get("role"))
        if user_role not in allowed_roles and user_role != Role.ADMINISTRATOR:
            raise PermissionDeniedError(
                f"Role '{user_role.value}' is not authorized. Required: {[r.value for r in allowed_roles]}"
            )
        return claims
