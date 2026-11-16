from tests.test_helpers import get_test_client, get_auth_header
from backend.app.models.enums import UserRole

def test_t9_regional_policy():
    """T9: Regional policy changes during offline/buffered operation."""
    client = get_test_client()
    cust_h = get_auth_header("cust-t9", UserRole.CUSTOMER, "user-t9-cust", region_id="EU-CENTRAL")
    admin_h = get_auth_header("admin-t9", UserRole.ADMINISTRATOR, "user-t9-admin")
    
    # 1. Place Order 1 under Policy Version 1 (EU-CENTRAL: tax_rate = 0.19, shipping_fee = 5.00)
    ord1_res = client.post("/api/orders/", json={
        "items": [{"sku": "SKU-HEADSET-003", "quantity": 1}], # Base price: 149.00
        "region_id": "EU-CENTRAL"
    }, headers=cust_h)
    assert ord1_res.status_code == 201
    ord1_data = ord1_res.json()
    assert ord1_data["policy_version"] == 1
    # Subtotal 149.00 + 5.00 shipping + 28.31 tax = 182.31
    expected_total_v1 = round(149.00 + 5.00 + (149.00 * 0.19), 2)
    assert ord1_data["total_amount"] == expected_total_v1
    
    # 2. Administrator updates EU-CENTRAL policy: tax_rate becomes 0.25 (Version 2)
    update_res = client.put("/api/policies/EU-CENTRAL", json={
        "tax_rate": 0.25,
        "shipping_fee": 10.00,
        "refund_approval_threshold": 50.00
    }, headers=admin_h)
    assert update_res.status_code == 200
    assert update_res.json()["policy_version"] == 2
    
    # 3. Place Order 2 under new Policy Version 2
    ord2_res = client.post("/api/orders/", json={
        "items": [{"sku": "SKU-HEADSET-003", "quantity": 1}],
        "region_id": "EU-CENTRAL"
    }, headers=cust_h)
    assert ord2_res.status_code == 201
    ord2_data = ord2_res.json()
    assert ord2_data["policy_version"] == 2
    expected_total_v2 = round(149.00 + 10.00 + (149.00 * 0.25), 2)
    assert ord2_data["total_amount"] == expected_total_v2
    
    # 4. CRITICAL INVARIANT: Order 1 must NOT be retroactively recalculated!
    check_ord1 = client.get(f"/api/orders/{ord1_data['order_id']}", headers=cust_h).json()
    assert check_ord1["policy_version"] == 1
    assert check_ord1["total_amount"] == expected_total_v1, "Regression: Historical order was rewritten by policy update!"
    
    return {
        "test_id": "T9_REGIONAL_POLICY",
        "description": "Regional policy changes during operation and historical snapshot preservation",
        "expected": "Order 1 retains v1 total ($182.31); Order 2 calculates v2 total ($196.25)",
        "observed": f"Order 1 total: ${check_ord1['total_amount']} (v{check_ord1['policy_version']}), Order 2 total: ${ord2_data['total_amount']} (v{ord2_data['policy_version']})",
        "status": "PASSED"
    }

if __name__ == "__main__":
    res = test_t9_regional_policy()
    print("Test T9 Passed:", res)
