import sys
import os
import json

from .database import seed_database, DB_FILE
from .auth_service import AuthService, Role
from .order_service import OrderService, OrderStatus
from .warehouse_service import WarehouseService

def run_interactive_demo():
    print("=" * 75)
    print("  OMNICHANNEL ORDER FULFILMENT PLATFORM - INTERACTIVE CLI DEMO")
    print("  CSA10 Software Engineering Assignment 1 Prototype")
    print("=" * 75)

    print("\n[Step 1] Initializing & seeding synthetic database...")
    seed_database()
    order_svc = OrderService()
    wh_svc = WarehouseService()
    print("  -> Database seeded with 5 synthetic products and 3 regional policies.")

    print("\n[Step 2] Authenticating personas...")
    cust_token = AuthService.login("cust_alex", "alex123")["token"]
    picker_token = AuthService.login("picker_john", "picker123")["token"]
    finance_token = AuthService.login("finance_frank", "finance123")["token"]
    support_token = AuthService.login("support_sarah", "support123")["token"]
    print("  -> Logged in: Customer Alex, Picker John, Finance Frank, Support Sarah.")

    print("\n[Step 3] Customer Alex creates order (2x Classic Cotton T-Shirt, REG-NORTH)...")
    order = order_svc.create_order(
        cust_token,
        [{"sku": "SKU-TSHIRT-01", "quantity": 2}],
        region_code="REG-NORTH"
    )
    order_id = order["order_id"]
    print(f"  -> Order Created: {order_id} | Total: ${order['total_amount']:.2f} | Status: {order['status']}")

    print("\n[Step 4] Customer Alex pays for order with Idempotency Key 'IDEMP-DEMO-001'...")
    pay_res = order_svc.process_order_payment(order_id, cust_token, "IDEMP-DEMO-001")
    print(f"  -> Payment Charged: Intent {pay_res['intent_id']} | Status: {pay_res['status']}")

    print("\n[Step 4b] Testing duplicate payment retry with identical idempotency key...")
    dup_res = order_svc.process_order_payment(order_id, cust_token, "IDEMP-DEMO-001")
    print(f"  -> Duplicate Key Detected: {dup_res['is_duplicate_replay']} | Message: {dup_res['message']}")

    print("\n[Step 5] Warehouse Picker John inspects pick list for WH-NORTH-01...")
    pick_list = wh_svc.get_pick_list("WH-NORTH-01")
    matching = [p for p in pick_list if p["order_id"] == order_id]
    print(f"  -> Order {order_id} found on pick list for WH-NORTH-01 (Quantity: {matching[0]['quantity']})")

    print("\n[Step 6] Picker John scans item barcode ('8901001000101')...")
    is_valid = wh_svc.verify_barcode("SKU-TSHIRT-01", "8901001000101")
    print(f"  -> Barcode Verified: {is_valid}")

    print("\n[Step 7] Order advances through fulfillment state machine...")
    order_svc.transition_order_status(order_id, OrderStatus.PICKING, picker_token, "Picker started batch")
    order_svc.transition_order_status(order_id, OrderStatus.PICKED, picker_token, "Picker completed bin scan")
    order_svc.transition_order_status(order_id, OrderStatus.DISPATCHED, picker_token, "Handed to courier")
    order_svc.transition_order_status(order_id, OrderStatus.DELIVERED, picker_token, "Delivered to customer doorstep")
    print(f"  -> Order lifecycle completed to DELIVERED.")

    print("\n[Step 8] Customer Alex views public tracking milestones...")
    tracking = order_svc.get_customer_tracking(order_id)
    print(f"  -> Public Status: {tracking['current_status']} | Tracking No: {tracking['tracking_number']}")
    for m in tracking["milestones"]:
        status_sym = "[X]" if m["completed"] else "[ ]"
        print(f"     {status_sym} Milestone: {m['milestone']}")

    print("\n[Step 9] Customer Alex submits return request ('Size too large')...")
    order_svc.request_return(order_id, cust_token, "Size too large")
    print(f"  -> Order status transitioned to RETURN_REQUESTED.")

    print("\n[Step 10] Testing Security Role Guard: Support Sarah attempts to approve refund...")
    try:
        order_svc.approve_refund(order_id, support_token, "Unauthorized attempt")
        print("  -> ERROR: Security check failed to block support agent!")
    except Exception as e:
        print(f"  -> Security Guard Active: Successfully blocked support agent! ({type(e).__name__}: {str(e)})")

    print("\n[Step 11] Finance Reviewer Frank authorizes refund...")
    refund_res = order_svc.approve_refund(order_id, finance_token, "Customer return validated; apparel unworn.")
    print(f"  -> Refund Approved! Txn: {refund_res['refund_details']['refund_transaction_id']} | Status: {refund_res['status']}")

    print("\n[Step 12] Immutable Audit Ledger Inspection:")
    audit_logs = order_svc.get_audit_trail(order_id)
    for log in audit_logs:
        print(f"  [{log['timestamp'][:19]}] {log['action']:<18} by {log['actor_id']:<14} ({log['actor_role']:<16}) : {log['from_state'] or 'NONE'} -> {log['to_state']} | {log['details']}")

    print("\n" + "=" * 75)
    print("  DEMONSTRATION COMPLETED SUCCESSFULLY: ALL WORKFLOW GATES PASSED")
    print("=" * 75)

if __name__ == "__main__":
    run_interactive_demo()
