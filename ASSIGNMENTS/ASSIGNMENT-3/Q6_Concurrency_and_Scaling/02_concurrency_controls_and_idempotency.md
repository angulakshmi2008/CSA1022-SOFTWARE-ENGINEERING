# Question 6: Concurrency Controls, Race Prevention, and Idempotency Architecture

## 1. Concurrency Challenges in Smart Campus Operations

In a distributed multi-instance environment serving six campuses, three critical concurrency hazards must be prevented:
1. **Concurrent Reservation Overlaps (Double-Booking Race Condition)**: Two users simultaneously submit overlapping reservation requests for the same facility via different backend instances.
2. **Conflicting Maintenance Updates (Lost Update Anomaly)**: Two technicians simultaneously update a ticket's status and notes, where the slower update inadvertently overwrites the faster update.
3. **Sensor-Event Replay and External Integration Duplication**: Network timeouts prompt automated IoT gateways or external DevOps ticket sync jobs to resubmit identical payloads.

---

## 2. Technical Control 1: Reservation Overlap Prevention

### 2.1 Multi-Layer Defense Architecture
To eliminate race conditions, the platform enforces concurrency control across three distinct tiers:
1. **Application Pre-validation**: Queries existing active bookings for overlapping intervals before execution.
2. **Atomic Row-Level Locking (`SELECT FOR UPDATE`)**: Within an ACID transaction, the target `Facility` row is locked. Any concurrent request for that facility must block until the active transaction commits or rolls back.
3. **Database-Level GiST Exclusion Constraint (PostgreSQL)**: At the database schema level, a generalized search tree (GiST) exclusion constraint guarantees that no two rows can have overlapping half-open timestamp ranges `[start_time, end_time)` for the same `facility_id`:

```sql
ALTER TABLE bookings
ADD CONSTRAINT no_overlapping_bookings
EXCLUDE USING gist (
    facility_id WITH =,
    tstzrange(start_time, end_time, '[)') WITH &&
)
WHERE (status NOT IN ('CANCELLED', 'REJECTED'));
```

### 2.2 Empirical Concurrency Validation
In `tests/concurrency/test_concurrent_overlapping_bookings.py`, multiple parallel threads simultaneously submitted overlapping booking requests for the same facility. The database serializability barrier allowed exactly **one** booking to commit (`HTTP 201 Created`) while the rival overlapping request was cleanly rejected (`HTTP 409 Conflict`), verifying zero double-bookings.

---

## 3. Technical Control 2: Optimistic Version-Based Concurrency Control (OCC)

For maintenance tickets, pessimistic locking (locking rows for minutes while a technician reads notes) would induce severe database contention. Instead, the platform implements **Optimistic Concurrency Control (OCC)**:

### 3.1 Mechanism
1. Every `Ticket` maintains an integer `version` field, initialized to `1`.
2. When a technician retrieves a ticket, the API returns the current `version`.
3. When submitting an update (triage, assignment, inspection, resolution), the client sends `expected_version`.
4. The backend validates:
   ```python
   if ticket.version != expected_version:
       return Response(
           {"error": "Stale ticket version. The ticket has been modified by another technician.", "current_version": ticket.version},
           status=status.HTTP_409_CONFLICT
       )
   ```
5. On successful update, `version` is atomically incremented by 1.

### 3.2 Verification
In `tests/concurrency/test_conflicting_ticket_updates.py`, two threads attempted to update a ticket with the same base version. Thread A succeeded (`HTTP 200 OK`, version incremented to 2), while Thread B was rejected with `HTTP 409 Conflict`.

---

## 4. Technical Control 3: Deterministic Idempotency Keys & Deduplication

### 4.1 Sensor Event Deduplication (US04)
IoT telemetry sensors may retransmit events due to network packet retries. The platform calculates a deterministic deduplication fingerprint:
$$\text{dedup\_key} = \text{SHA256}(\text{source\_id} \parallel \text{event\_type} \parallel \lfloor\text{timestamp} / 60\rfloor)$$
If an event arrives with an identical deduplication key within the 60-second window, the ingestion pipeline recognizes the existing record, increments a suppression counter, and returns `HTTP 200 OK` (`is_duplicate: true`) without creating duplicate maintenance tickets.

### 4.2 Durable Outbox Pattern for DevOps Issues
When an `M1` critical maintenance ticket requires synchronizing with an external issue tracker (e.g., Jira, GitHub Issues), network timeouts could trigger retry loops that create duplicate external tickets.
- An `IntegrationIntent` record is created atomically within the same database transaction as the ticket.
- Every external API dispatch includes a unique, immutable `idempotency_key` (UUID v4 or deterministic ticket hash).
- If a dispatch times out, subsequent retries resend the identical `idempotency_key`, allowing the remote system to acknowledge the request without duplicating tickets.
