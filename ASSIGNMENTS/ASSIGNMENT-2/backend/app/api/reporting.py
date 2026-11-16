from fastapi import APIRouter, Depends
from backend.app.core.security import require_role
from backend.app.models.enums import UserRole
from backend.app.database import get_db

router = APIRouter(prefix="/reporting", tags=["Reporting & Consolidated Analytics"])

@router.get("/summary")
def get_consolidated_summary(current_user: dict = Depends(require_role([UserRole.STORE_MANAGER, UserRole.ADMINISTRATOR]))):
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Total Gross Sales and Order Volume
        cursor.execute("""
            SELECT COUNT(*) as total_orders,
                   COALESCE(SUM(total_amount), 0.0) as gross_revenue,
                   COALESCE(SUM(tax_amount), 0.0) as total_tax_collected,
                   COALESCE(SUM(shipping_fee), 0.0) as total_shipping_revenue
            FROM orders
            WHERE state IN ('PAID', 'PACKED', 'DISPATCHED', 'DELIVERED', 'CLOSED')
        """)
        sales_data = dict(cursor.fetchone())
        
        # 2. Regional Sales Breakdown (12 regions)
        cursor.execute("""
            SELECT region_id,
                   COUNT(*) as order_count,
                   COALESCE(SUM(total_amount), 0.0) as regional_revenue
            FROM orders
            WHERE state IN ('PAID', 'PACKED', 'DISPATCHED', 'DELIVERED', 'CLOSED')
            GROUP BY region_id
            ORDER BY regional_revenue DESC
        """)
        regional_breakdown = [dict(r) for r in cursor.fetchall()]
        
        # 3. Total Inventory On Hand vs. Reserved across all warehouses
        cursor.execute("""
            SELECT COALESCE(SUM(on_hand), 0) as total_on_hand,
                   COALESCE(SUM(reserved), 0) as total_reserved,
                   COALESCE(SUM(on_hand - reserved), 0) as total_available
            FROM stock_items
        """)
        stock_data = dict(cursor.fetchone())
        
        # 4. Total Refunds Disbursed vs. Pending
        cursor.execute("""
            SELECT state, COUNT(*) as count, COALESCE(SUM(amount), 0.0) as total_amount
            FROM refund_requests
            GROUP BY state
        """)
        refunds_breakdown = [dict(r) for r in cursor.fetchall()]
        
        return {
            "sales_summary": sales_data,
            "regional_breakdown": regional_breakdown,
            "inventory_summary": stock_data,
            "refunds_summary": refunds_breakdown
        }
