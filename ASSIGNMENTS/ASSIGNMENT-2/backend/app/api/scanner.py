from fastapi import APIRouter, Depends
from backend.app.schemas.scanner import ScannerBatchSyncRequest, ScannerSyncResponse
from backend.app.core.security import get_current_user
from backend.app.services.scanner_service import sync_scanner_batch
from backend.app.database import get_db

router = APIRouter(prefix="/scanner", tags=["Warehouse Scanner Edge Sync"])

@router.post("/sync-batch", response_model=ScannerSyncResponse)
def sync_batch_scans(batch_in: ScannerBatchSyncRequest, current_user: dict = Depends(get_current_user)):
    with get_db() as conn:
        res = sync_scanner_batch(conn, events=batch_in.events, caller_id=current_user["user_id"])
        return ScannerSyncResponse(**res)
