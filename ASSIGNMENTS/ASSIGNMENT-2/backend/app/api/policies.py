from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.schemas.policy import PolicyUpdate, RegionalPolicyResponse
from backend.app.core.security import require_role
from backend.app.models.enums import UserRole
from backend.app.database import get_db

router = APIRouter(prefix="/policies", tags=["Regional Policies"])

@router.get("/")
def list_regional_policies():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.region_id, p.region_name, p.policy_version, p.tax_rate, p.shipping_fee, p.refund_approval_threshold, p.is_active
            FROM regional_policies p
            INNER JOIN (
                SELECT region_id, MAX(policy_version) as max_v
                FROM regional_policies
                GROUP BY region_id
            ) latest ON p.region_id = latest.region_id AND p.policy_version = latest.max_v
            ORDER BY p.region_id ASC
        """)
        return [dict(r) for r in cursor.fetchall()]

@router.put("/{region_id}", response_model=RegionalPolicyResponse)
def update_regional_policy(
    region_id: str,
    update_in: PolicyUpdate,
    current_user: dict = Depends(require_role([UserRole.ADMINISTRATOR]))
):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT region_id, region_name, policy_version
            FROM regional_policies
            WHERE region_id = ?
            ORDER BY policy_version DESC LIMIT 1
        """, (region_id,))
        latest = cursor.fetchone()
        if not latest:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Region '{region_id}' not found")
            
        new_version = latest["policy_version"] + 1
        cursor.execute("""
            INSERT INTO regional_policies (
                region_id, region_name, policy_version, tax_rate, shipping_fee, refund_approval_threshold, is_active, effective_from
            ) VALUES (?, ?, ?, ?, ?, ?, 1, datetime('now', 'utc'))
        """, (region_id, latest["region_name"], new_version, update_in.tax_rate, update_in.shipping_fee, update_in.refund_approval_threshold))
        
        cursor.execute("""
            SELECT region_id, region_name, policy_version, tax_rate, shipping_fee, refund_approval_threshold, is_active
            FROM regional_policies WHERE region_id = ? AND policy_version = ?
        """, (region_id, new_version))
        return dict(cursor.fetchone())
