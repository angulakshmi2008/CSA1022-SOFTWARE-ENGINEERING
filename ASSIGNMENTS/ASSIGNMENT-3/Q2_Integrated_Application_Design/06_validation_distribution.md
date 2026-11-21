# Validation Responsibility Distribution Across Architectural Layers

## 1. Overview
A core software engineering principle applied throughout this system is **Defense in Depth**: validation logic is distributed thoughtfully across Frontend, Backend, and Database tiers based on which layer authoritatively owns each type of invariant.

---

## 2. Layered Validation Responsibilities

```text
┌────────────────────────────────────────────────────────┐
│                      FRONTEND                          │
│  - Input formatting & real-time UX guidance            │
│  - Start time < End time pre-check                     │
│  - Required field highlighting                         │
│  - Role-scoped UI element visibility                   │
│  - Human-friendly translation of backend HTTP errors   │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTP Request
                           ▼
┌────────────────────────────────────────────────────────┐
│                      BACKEND                           │
│  - Authentication verification (Session / Token)       │
│  - Authoritative RBAC permission checks                │
│  - Business policy enforcement (max duration, hours)   │
│  - State machine transition validity (FSM guards)      │
│  - Mandatory resolution notes validation (HTTP 422)    │
│  - Optimistic locking version validation (HTTP 409)    │
│  - Idempotency key lookup and caching                  │
│  - Transaction orchestration and audit dispatch        │
└──────────────────────────┬─────────────────────────────┘
                           │ SQL / Transaction
                           ▼
┌────────────────────────────────────────────────────────┐
│                      DATABASE                          │
│  - Foreign key referential integrity                   │
│  - Unique constraint on (source_id, event_id)          │
│  - Unique constraint on request_key                    │
│  - Check constraint (end_at > start_at)                │
│  - GiST Non-Overlap Exclusion Constraint for bookings  │
│  - Not-Null column constraints                         │
│  - Transactional ACID isolation                        │
└────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Matrix of Responsibilities

| Validation Concern | Frontend Responsibility | Backend Responsibility | Database Responsibility |
|---|---|---|---|
| **User Role & Authority** | Hides unpermitted buttons/tabs for clean UI; never trusted as security. | **Authoritative:** Checks JWT/session user role against endpoint permission classes. Returns 403 on breach. | Stores user roles; enforces foreign key link from user to campus. |
| **Booking Time Interval** | Datepicker prevents selecting past dates; checks `end > start`. | Validates ISO timestamps, operating hour bounds, max booking duration (e.g., 4h). | **Authoritative:** Table check constraint enforces `end_at > start_at`. |
| **Booking Overlap** | Queries availability API to color calendar slots green/red. | Queries overlapping intervals and serializes write path. | **Authoritative Final Arbiter:** GiST exclusion constraint physically prevents concurrent overlapping slot inserts. |
| **Maintenance Evidence** | Form marks resolution notes as required when clicking Resolve. | **Authoritative:** Evaluates target state; if `resolved`/`closed`, strictly verifies `len(resolution_notes) >= 10`. Returns 422 if invalid. | Column stores resolution text. |
| **Concurrent Updates** | Tracks entity `version` in local state; submits `expected_version`. | Compares `expected_version` against current database version in SQL UPDATE. Returns 409 on mismatch. | Enforces atomic row update and version increment. |
| **Sensor Replays** | Simulates retries in testing view. | Inspects unique event index; wraps intake and ticket generation in `transaction.atomic()`. | **Authoritative:** `UNIQUE (source_id, event_id)` constraint rejects duplicate physical inserts. |
| **Audit Integrity** | Displays audit log in dashboard. | **Authoritative:** Automatically generates audit row within same transaction. | Transactional rollback if audit insert fails; append-only schema. |
