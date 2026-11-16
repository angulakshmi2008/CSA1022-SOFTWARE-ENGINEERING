from fastapi import APIRouter, Query
from typing import List, Optional
from backend.app.database import get_db

router = APIRouter(prefix="/products", tags=["Product Catalogue"])

@router.get("/")
def list_products(region_id: str = "US-EAST", category: Optional[str] = None):
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT p.sku, p.name, p.description, p.base_price, p.category,
                   COALESCE(s.on_hand, 0) as on_hand,
                   COALESCE(s.reserved, 0) as reserved,
                   COALESCE(s.on_hand - s.reserved, 0) as available_stock
            FROM products p
            LEFT JOIN stock_items s ON p.sku = s.sku AND s.region_id = ?
            WHERE p.is_active = 1
        """
        params = [region_id]
        if category:
            query += " AND p.category = ?"
            params.append(category)
        query += " ORDER BY p.name ASC"
        
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]

@router.get("/{sku}")
def get_product(sku: str, region_id: str = "US-EAST"):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.sku, p.name, p.description, p.base_price, p.category,
                   COALESCE(s.on_hand, 0) as on_hand,
                   COALESCE(s.reserved, 0) as reserved,
                   COALESCE(s.on_hand - s.reserved, 0) as available_stock
            FROM products p
            LEFT JOIN stock_items s ON p.sku = s.sku AND s.region_id = ?
            WHERE p.sku = ? AND p.is_active = 1
        """, (region_id, sku))
        prod = cursor.fetchone()
        if not prod:
            return {"error": "Product not found"}
        return dict(prod)
