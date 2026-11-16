import os
import json
from typing import Dict, Any, Optional

DEFAULT_POLICIES = {
    "REG-NORTH": {
        "region_name": "Northern Regional Hub (Delhi/NCR)",
        "warehouse_id": "WH-NORTH-01",
        "tax_rate": 0.12,
        "shipping_flat_rate": 15.00,
        "free_shipping_threshold": 100.00,
        "single_finance_refund_limit": 500.00,
        "return_window_days": 14
    },
    "REG-SOUTH": {
        "region_name": "Southern Regional Hub (Chennai/Bangalore)",
        "warehouse_id": "WH-SOUTH-02",
        "tax_rate": 0.08,
        "shipping_flat_rate": 12.00,
        "free_shipping_threshold": 80.00,
        "single_finance_refund_limit": 400.00,
        "return_window_days": 14
    },
    "REG-WEST": {
        "region_name": "Western Regional Hub (Mumbai/Pune)",
        "warehouse_id": "WH-WEST-03",
        "tax_rate": 0.10,
        "shipping_flat_rate": 10.00,
        "free_shipping_threshold": 75.00,
        "single_finance_refund_limit": 600.00,
        "return_window_days": 21
    }
}

class RegionalPolicyService:
    def __init__(self, rules_file: Optional[str] = None):
        self.rules = DEFAULT_POLICIES.copy()
        if rules_file and os.path.exists(rules_file):
            try:
                with open(rules_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.rules.update(loaded)
            except Exception:
                pass

    def get_policy(self, region_code: str) -> Dict[str, Any]:
        policy = self.rules.get(region_code)
        if not policy:
            # Default to North if unspecified
            return self.rules["REG-NORTH"]
        return policy

    def calculate_charges(self, region_code: str, subtotal: float) -> Dict[str, float]:
        """Calculate regional tax, shipping, and grand total."""
        policy = self.get_policy(region_code)
        tax = round(subtotal * policy["tax_rate"], 2)

        if subtotal >= policy["free_shipping_threshold"]:
            shipping = 0.0
        else:
            shipping = policy["shipping_flat_rate"]

        total = round(subtotal + tax + shipping, 2)
        return {
            "subtotal": subtotal,
            "tax_rate": policy["tax_rate"],
            "tax_amount": tax,
            "shipping_amount": shipping,
            "total_amount": total,
            "warehouse_id": policy["warehouse_id"]
        }

    def validate_refund_threshold(self, region_code: str, refund_amount: float) -> bool:
        """Verify whether a single finance reviewer can approve this amount without dual authorization."""
        policy = self.get_policy(region_code)
        limit = policy.get("single_finance_refund_limit", 500.00)
        return refund_amount <= limit

    def get_return_window_days(self, region_code: str) -> int:
        policy = self.get_policy(region_code)
        return policy.get("return_window_days", 14)
