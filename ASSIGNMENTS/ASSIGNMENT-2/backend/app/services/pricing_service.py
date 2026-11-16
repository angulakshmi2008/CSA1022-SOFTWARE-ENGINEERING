import sqlite3
from typing import Dict, Any, List
from fastapi import HTTPException, status

def get_active_policy(conn: sqlite3.Connection, region_id: str) -> sqlite3.Row:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT region_id, region_name, policy_version, tax_rate, shipping_fee, refund_approval_threshold
        FROM regional_policies
        WHERE region_id = ? AND is_active = 1
        ORDER BY policy_version DESC
        LIMIT 1
    """, (region_id,))
    policy = cursor.fetchone()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No active policy found for region '{region_id}'"
        )
    return policy

def calculate_order_pricing(conn: sqlite3.Connection, items: List[Dict[str, Any]], region_id: str) -> Dict[str, Any]:
    policy = get_active_policy(conn, region_id)
    tax_rate = policy["tax_rate"]
    shipping_fee = policy["shipping_fee"]
    policy_version = policy["policy_version"]
    
    subtotal = 0.0
    evaluated_lines = []
    
    cursor = conn.cursor()
    for item in items:
        sku = item["sku"]
        qty = item["quantity"]
        cursor.execute("SELECT sku, name, base_price, is_active FROM products WHERE sku = ?", (sku,))
        prod = cursor.fetchone()
        if not prod:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product SKU '{sku}' not found")
        if not prod["is_active"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product SKU '{sku}' is inactive")
        
        unit_price = round(float(prod["base_price"]), 2)
        line_subtotal = round(unit_price * qty, 2)
        line_tax = round(line_subtotal * tax_rate, 2)
        line_total = round(line_subtotal + line_tax, 2)
        
        subtotal += line_subtotal
        evaluated_lines.append({
            "sku": sku,
            "quantity": qty,
            "unit_price": unit_price,
            "tax_rate": tax_rate,
            "tax_amount": line_tax,
            "line_total": line_total
        })
    
    total_tax = round(subtotal * tax_rate, 2)
    grand_total = round(subtotal + shipping_fee + total_tax, 2)
    
    return {
        "subtotal": round(subtotal, 2),
        "tax_amount": round(total_tax, 2),
        "shipping_fee": round(shipping_fee, 2),
        "total_amount": round(grand_total, 2),
        "policy_version": policy_version,
        "lines": evaluated_lines
    }
