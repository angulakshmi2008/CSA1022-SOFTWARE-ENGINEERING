# Consistency, Concurrency, and Duplicate Prevention

## 1. The Challenge of Concurrent Multi-Instance Operations
In distributed environments running two or more stateless backend replicas sharing a database, conventional application-level availability checks fail due to **Time-Of-Check to Time-Of-Use (TOCTOU)** race conditions:

```text
Time  Replica 1 (User A)                  Replica 2 (User B)
 │
 t1   Check: Is Slot Free? -> YES
 t2                                       Check: Is Slot Free? -> YES
 t3   Insert Booking for User A -> OK
 t4                                       Insert Booking for User B -> OK (CORRUPTION: OVERLAP!)
 ▼
```

Both instances observe that no booking exists at $t_1$ and $t_2$, leading both to insert records, resulting in double-booking. To solve this definitively across multiple backend replicas, the database engine itself must serve as the authoritative arbiter of truth.

---

## 2. Technical Control 1: PostgreSQL Exclusion Constraint for Booking Non-Overlap
PostgreSQL provides generalized search tree (`GiST`) index extensions allowing declarative exclusion constraints over scalar values combined with time range types (`tstzrange`):

```sql
-- Step 1: Enable binary-tree GiST extension for scalar equality comparisons
CREATE EXTENSION IF NOT EXISTS btree_gist;

-- Step 2: Enforce that no two active bookings for the same facility have overlapping time ranges
ALTER TABLE bookings
ADD CONSTRAINT booking_no_active_overlap
EXCLUDE USING gist (
    facility_id WITH =,
    tstzrange(start_at, end_at, '[)') WITH &&
)
WHERE (status IN ('approved', 'confirmed', 'in_use'));
```

### Operational Mechanics:
1. The half-open interval `[start_at, end_at)` mathematically ensures that a booking ending at `11:00:00Z` does not conflict with a subsequent booking starting precisely at `11:00:00Z`.
2. The `WHERE (status IN ...)` clause ensures that `cancelled` or `completed` reservations release their slots immediately without requiring physical row deletion.
3. If two concurrent HTTP requests arrive at `backend-1` and `backend-2` at the exact same millisecond:
   - PostgreSQL’s GiST lock serializes the physical page modification.
   - The winning transaction commits (`HTTP 201 Created`).
   - The losing transaction triggers an `ExclusionViolation` exception.
   - Django catches this specific database integrity error and returns an explicit `HTTP 409 Conflict` to the client.

---

## 3. Technical Control 2: Optimistic Concurrency Control for Ticket Updates
When multiple technicians or managers view and edit the same maintenance ticket, last-write-wins overwriting is prevented via version-based optimistic locking:

```sql
-- Atomic update guarded by expected_version
UPDATE tickets
SET status = :target_state,
    assignee_id = :assignee_id,
    resolution_notes = :resolution_notes,
    version = version + 1,
    updated_at = CURRENT_TIMESTAMP
WHERE id = :ticket_id AND version = :expected_version;
```

### Collision Resolution Flow:
1. Technician 1 and Technician 2 both fetch Ticket #1042 at `version = 2`.
2. Technician 1 updates the ticket with inspection findings, supplying `expected_version = 2`.
   - Update affects 1 row. Database advances `version` to 3. Returns `HTTP 200 OK`.
3. Technician 2 attempts to resolve the ticket, also supplying `expected_version = 2`.
   - Update affects 0 rows because `version` in storage is now 3.
   - Backend detects `rows_affected == 0`, rolls back the transaction, and returns `HTTP 409 Conflict`:
     `{"error": "Concurrent Modification Conflict", "current_version": 3}`.
4. Technician 2's UI receives the 409, refreshes the ticket state with Technician 1’s new findings, and allows Technician 2 to merge their resolution without losing data.

---

## 4. Technical Control 3: Unique Sensor Telemetry Deduplication
Network timeouts between campus IoT gateways and the API frequently cause automated retry loops:

```sql
ALTER TABLE sensor_events
ADD CONSTRAINT sensor_event_unique_identity
UNIQUE (source_id, event_id);
```

### Ingestion Logic:
When `POST /api/sensor-events/` is received:
1. The system checks if `(source_id, event_id)` already exists.
2. If already present:
   - Deduplication suppresses ticket creation.
   - Returns `HTTP 200 OK` with `status: "duplicate_suppressed"` and the previously linked `ticket_id`.
3. If new:
   - Evaluates sensor threshold (e.g., $Temp > 26.0^\circ C$).
   - If breached, creates `Ticket` in `intake` status and links it to `SensorEvent` inside a single ACID database transaction.

---

## 5. Technical Control 4: Client Request Idempotency Keys
For network resilience during booking submissions:
1. The client generates a unique UUID `request_key` (e.g., `req-7782-bdf9-001`).
2. The backend records the `request_key` on the booking record.
3. If the user experiences a network interruption and resubmits the same form, the backend recognizes the duplicate key and returns the original booking confirmation rather than creating an additional reservation.

---

## 6. Technical Control 5: Transactional Append-Only Audit Trail
Every state transition, approval, rejection, or privileged update executes within `transaction.atomic()`:
```python
with transaction.atomic():
    booking.status = target_status
    booking.version += 1
    booking.save()
    
    AuditEvent.objects.create(
        actor=user,
        entity_type="Booking",
        entity_id=booking.id,
        action="STATUS_CHANGE",
        before_state={"status": old_status, "version": old_version},
        after_state={"status": booking.status, "version": booking.version},
        ip_address=client_ip
    )
```
If logging fails or an integrity violation occurs, the entire transaction rolls back cleanly, guaranteeing that no state change occurs without an auditable record.
