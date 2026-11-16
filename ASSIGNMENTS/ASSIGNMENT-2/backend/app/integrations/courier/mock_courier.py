import uuid
from typing import Dict, Any

class MockCourierAPI:
    """Simulates external Courier Partner API with timeout and reconciliation support."""
    
    _registered_shipments: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def reset(cls):
        cls._registered_shipments.clear()

    @classmethod
    def register_shipment(cls, correlation_key: str, order_details: dict, simulate_timeout: bool = False) -> Dict[str, Any]:
        # Idempotent reconciliation check
        if correlation_key in cls._registered_shipments:
            return {
                "success": True,
                "tracking_number": cls._registered_shipments[correlation_key]["tracking_number"],
                "reconciled": True
            }
            
        if simulate_timeout:
            # Simulate partner network socket drop after internal acceptance or failure
            raise TimeoutError("Courier API Gateway Timeout (504)")
            
        tracking_no = f"TRK-{uuid.uuid4().hex[:8].upper()}"
        cls._registered_shipments[correlation_key] = {
            "tracking_number": tracking_no,
            "order_details": order_details,
            "status": "IN_TRANSIT"
        }
        return {
            "success": True,
            "tracking_number": tracking_no,
            "reconciled": False
        }

    @classmethod
    def get_shipment_by_correlation_key(cls, correlation_key: str) -> Dict[str, Any]:
        return cls._registered_shipments.get(correlation_key)
