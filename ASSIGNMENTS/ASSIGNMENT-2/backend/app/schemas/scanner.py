from pydantic import BaseModel, Field
from typing import List

class ScannerEventItem(BaseModel):
    node_id: str
    event_id: str
    sku: str
    region_id: str
    event_type: str = Field(description="'STOCK_COUNT', 'RECEIVE', or 'PICK_VERIFY'")
    quantity: int
    observation_time: str
    schema_version: str = "1.0"

class ScannerBatchSyncRequest(BaseModel):
    events: List[ScannerEventItem]

class ScannerSyncResponse(BaseModel):
    received_count: int
    processed_count: int
    duplicate_count: int
    stale_count: int
    message: str
