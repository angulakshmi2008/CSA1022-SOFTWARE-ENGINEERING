# Task 6: Edge Scanner Synchronization and Deduplication Rules

Industrial warehouse facilities frequently feature radio-frequency dead zones (e.g., cold storage vaults, metallic racking aisles, underground receiving docks) where handheld WiFi scanners lose connectivity. To prevent physical operations from halting, the edge architecture specifies a robust offline buffering and server-side deduplication protocol.

---

## 1. Edge Scanner Node Architecture and Buffer Protocol
1. **Device Identity:** Every handheld scanner possesses an immutable hardware identifier: `node_id` (e.g., `SCANNER-WH-A1`, `SCANNER-WH-LON-03`).
2. **Event Identity:** Every physical barcode scan generates an in-memory event with a globally unique UUID: `event_id`.
3. **Local Queue Bounding:** Handheld scanners maintain a local FIFO event queue backed by non-volatile flash memory (e.g., SQLite on Android/Linux) with an explicit capacity limit of **5,000 events**.
   - *Buffer Exhaustion Policy:* If the device reaches 5,000 un-synchronized events, an audible alarm sounds, visual amber warnings display, and further scanning is locked until connectivity is restored and the buffer flushes. No events are silently discarded.
4. **Event Payload Schema (Version 1.0):**
   ```json
   {
     "node_id": "SCANNER-WH-A1",
     "event_id": "8f8b3c84-18c9-4b2a-89a1-7d1a29f8c14b",
     "sku": "SKU-LAPTOP-001",
     "region_id": "US-EAST",
     "event_type": "RECEIVE",
     "quantity": 10,
     "observation_time": "2026-11-14T10:15:30Z",
     "schema_version": "1.0"
   }
   ```

---

## 2. Server-Side Ingestion and Deduplication Algorithm
When the handheld terminal moves into WiFi coverage, it establishes an authenticated TLS session and transmits its buffered batch via `POST /api/scanner/sync-batch`.

The server executes the following transactional algorithm:

```text
FOR each event IN batch:
    1. Parse observation_time and schema_version.
    2. Check staleness:
       IF (CurrentServerTime - event.observation_time) > 24 Hours:
           Mark is_stale = TRUE
           Log warning for manual inventory audit
       ELSE:
           is_stale = FALSE

    3. Attempt atomic insert into scanner_event_logs:
       INSERT INTO scanner_event_logs (node_id, event_id, ...) VALUES (...)
       
       IF Unique Constraint Violation ON (node_id, event_id):
           // DUPLICATE REPLAY DETECTED!
           Increment duplicate_count
           CONTINUE (Skip inventory update)
           
       ELSE:
           // VALID NEW EVENT
           Increment processed_count
           IF event.event_type == 'RECEIVE' AND is_stale == FALSE:
               UPDATE stock_items 
               SET on_hand = on_hand + event.quantity, version = version + 1 
               WHERE sku = event.sku AND region_id = event.region_id;

COMMIT Transaction
RETURN Summary { received, processed, duplicates, stale }
```

### Critical Invariants Preserved by this Algorithm:
1. **Zero Double-Counting on Edge Replay:** Network retransmissions, scanner reboots, or operator double-syncs transmit duplicate event IDs. The database-enforced unique constraint `UNIQUE(node_id, event_id)` immediately catches duplicate pairs, completely preventing duplicate inventory increments.
2. **Staleness Protection:** Barcode scans delayed by days are not blindly merged into live inventory. They are persisted with `is_stale = 1` and routed to the warehouse supervisor for physical stock reconciliation.

---

## 3. Offline Refund Approval Governance
A common vulnerability in distributed enterprise retail is allowing offline terminals to grant financial authorizations without central validation.
- **Strict Rule:** A scanner or disconnected regional client terminal **CANNOT approve refunds offline**.
- If a warehouse lead or support representative queues a refund decision while offline, the local client records the intent with state `REQUESTED (Offline Pending)`.
- Upon network reconnection, the server inspects the authenticated session token, user role, region assignment, monetary threshold, and four-eyes rule.
- If the reviewer lacks the `FINANCE_REVIEWER` role or the amount exceeds the regional limit, the server strictly returns HTTP 403 Forbidden, and the refund remains unapproved.
- This rule was codified and verified in test `T11_OFFLINE_REFUND_APPROVAL`.
