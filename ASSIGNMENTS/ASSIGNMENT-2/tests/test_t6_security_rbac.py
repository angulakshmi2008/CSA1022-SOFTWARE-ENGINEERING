from tests.test_helpers import get_test_client, get_auth_header
from backend.app.models.enums import UserRole

def test_t6_security_rbac():
    """T6: A customer or support agent attempting to approve a refund or access another customer's order."""
    client = get_test_client()
    
    cust_a_id = "user-t6-customer-a"
    cust_b_id = "user-t6-customer-b"
    support_id = "user-t6-support"
    finance_id = "user-t6-finance"
    
    cust_a_h = get_auth_header("custA", UserRole.CUSTOMER, cust_a_id)
    cust_b_h = get_auth_header("custB", UserRole.CUSTOMER, cust_b_id)
    support_h = get_auth_header("supportGuy", UserRole.SUPPORT_AGENT, support_id)
    finance_h = get_auth_header("financeGal", UserRole.FINANCE_REVIEWER, finance_id)
    
    # 1. Customer A places an order
    ord_a_res = client.post("/api/orders/", json={
        "items": [{"sku": "SKU-LAPTOP-001", "quantity": 1}],
        "region_id": "US-EAST"
    }, headers=cust_a_h)
    assert ord_a_res.status_code == 201
    order_a_id = ord_a_res.json()["order_id"]
    
    # SECURITY ATTACK 1: Customer B attempts to inspect Customer A's order
    cross_read_res = client.get(f"/api/orders/{order_a_id}", headers=cust_b_h)
    assert cross_read_res.status_code == 403, f"Expected 403 Forbidden on cross-read, got {cross_read_res.status_code}"
    assert "Access denied" in cross_read_res.json()["detail"]
    
    # 2. Customer A creates a refund request for $150.00 (> $50 threshold)
    refund_res = client.post("/api/refunds/", json={
        "order_id": order_a_id,
        "amount": 150.00,
        "reason": "Battery defect"
    }, headers=cust_a_h)
    assert refund_res.status_code == 201
    refund_id = refund_res.json()["refund_id"]
    
    # SECURITY ATTACK 2: Customer A attempts to approve their own refund
    cust_approve_res = client.post(f"/api/refunds/{refund_id}/decide", json={"decision": "APPROVE"}, headers=cust_a_h)
    assert cust_approve_res.status_code == 403, f"Expected 403 Forbidden on customer approval, got {cust_approve_res.status_code}"
    
    # SECURITY ATTACK 3: Support Agent attempts to approve high-value refund ($150 > $50)
    support_approve_res = client.post(f"/api/refunds/{refund_id}/decide", json={"decision": "APPROVE"}, headers=support_h)
    assert support_approve_res.status_code == 403, f"Expected 403 Forbidden on support agent approval, got {support_approve_res.status_code}"
    
    # LEGITIMATE OPERATION: Finance Reviewer approves -> SUCCEEDS
    fin_approve_res = client.post(f"/api/refunds/{refund_id}/decide", json={"decision": "APPROVE"}, headers=finance_h)
    assert fin_approve_res.status_code == 200, f"Expected 200 OK on finance reviewer approval, got {fin_approve_res.status_code}"
    assert fin_approve_res.json()["state"] == "APPROVED"
    
    return {
        "test_id": "T6_SECURITY_RBAC",
        "description": "Unauthorized refund approval and cross-customer order access rejection",
        "expected": "HTTP 403 on cross-customer read, HTTP 403 on customer approval, HTTP 403 on support approval, HTTP 200 on finance approval",
        "observed": f"Rejected cross-read ({cross_read_res.status_code}), rejected customer approve ({cust_approve_res.status_code}), rejected support approve ({support_approve_res.status_code}), allowed finance approve ({fin_approve_res.status_code})",
        "status": "PASSED"
    }

if __name__ == "__main__":
    res = test_t6_security_rbac()
    print("Test T6 Passed:", res)
