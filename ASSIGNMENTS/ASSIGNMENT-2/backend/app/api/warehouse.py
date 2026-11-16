from fastapi import APIRouter, Depends
from backend.app.core.security import require_role
from backend.app.models.enums import UserRole
from backend.app.services.warehouse_service import get_picker_orders, confirm_pick_and_pack, dispatch_order
from backend.app.database import get_db

router = APIRouter(prefix="/warehouse", tags=["Warehouse & Picking"])

@router.get("/pick-lists")
def view_pick_lists(current_user: dict = Depends(require_role([UserRole.PICKER, UserRole.ADMINISTRATOR]))):
    with get_db() as conn:
        region = current_user.get("region_id", "US-EAST")
        return get_picker_orders(conn, picker_region=region)

@router.post("/orders/{order_id}/pack")
def pack_order(order_id: str, current_user: dict = Depends(require_role([UserRole.PICKER, UserRole.ADMINISTRATOR]))):
    with get_db() as conn:
        return confirm_pick_and_pack(conn, order_id=order_id, picker_id=current_user["user_id"])

@router.post("/orders/{order_id}/dispatch")
def dispatch_order_endpoint(order_id: str, current_user: dict = Depends(require_role([UserRole.PICKER, UserRole.ADMINISTRATOR]))):
    with get_db() as conn:
        return dispatch_order(conn, order_id=order_id, picker_id=current_user["user_id"])
