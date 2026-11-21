# Core User Stories and Measurable Acceptance Criteria

## 1. Overview
Six primary user stories define the acceptance contract for the Smart Campus Facility Booking and Maintenance Platform first release. Each user story specifies the persona, intent, measurable acceptance criterion, test preconditions, expected API response code, and persistent state verification.

---

### User Story US01: Facility Reservation Request
- **Story Statement:** As a Faculty Member, I want to book an available laboratory space for a scheduled research session so that my department has confirmed access without conflict.
- **Preconditions:**
  - Authenticated as Faculty user (`dr.smith@campus.edu`).
  - Target facility (`Robotics Lab 101`, ID: 1) is active and has no overlapping reservations for `2026-11-20T10:00:00Z` to `2026-11-20T12:00:00Z`.
- **Action:**
  - Send `POST /api/bookings/` with payload `{"facility_id": 1, "start_at": "2026-11-20T10:00:00Z", "end_at": "2026-11-20T12:00:00Z", "purpose": "Robotics Sensor Calibration", "request_key": "req-faculty-001"}`.
- **Measurable Acceptance Criteria:**
  - API returns `HTTP 201 Created` with a unique booking ID, state `confirmed` (or `approved` if restricted), version `1`, and timestamp.
  - Querying `GET /api/bookings/calendar/?facility_id=1` or refreshing the UI renders the slot with the booked interval.
  - The booking row is persisted in PostgreSQL and survives container restart.

---

### User Story US02: Database-Enforced Overlap Prevention
- **Story Statement:** As a Student or Facility User, I want the system to reject any booking request that conflicts with an existing confirmed reservation so that double-booking never occurs.
- **Preconditions:**
  - Facility 1 has a confirmed reservation from `10:00:00Z` to `12:00:00Z`.
- **Action:**
  - A concurrent or subsequent user submits `POST /api/bookings/` for Facility 1 from `11:00:00Z` to `13:00:00Z` (overlapping interval).
- **Measurable Acceptance Criteria:**
  - The second request is rejected with `HTTP 409 Conflict`.
  - The error payload states: `"Facility is already reserved during the requested time window."`
  - Total active booking count for that slot remains exactly 1 in the database; no duplicate or partial record is inserted.

---

### User Story US03: Restricted Action Approval Enforcement
- **Story Statement:** As a Department Approver, I want to review, justify, and decide restricted facility bookings and sensitive maintenance changes so that compliance and safety standards are maintained.
- **Preconditions:**
  - A booking request exists for a restricted facility (`Bio-Safety Containment Lab 304`) in `requested` status.
- **Action:**
  - Authorized Approver submits `POST /api/approvals/` with `{"request_type": "booking", "request_id": 12, "decision": "approved", "reason": "Authorized biosafety protocol certified."}`.
  - Conversely, an unauthorized Student user attempts the same `POST /api/approvals/` call.
- **Measurable Acceptance Criteria:**
  - Authorized Approver receives `HTTP 200 OK` (or `201 Created`); the booking status transitions to `approved`/`confirmed`; an immutable `AuditEvent` is persisted in the database.
  - Unauthorized Student receives `HTTP 403 Forbidden`; no status update or approval record is committed.

---

### User Story US04: Telemetry Ingestion and Duplicate Suppression
- **Story Statement:** As a Facility Manager, I want sensor telemetry to create actionable maintenance tickets upon threshold breach without generating duplicate tickets when network retries occur.
- **Preconditions:**
  - Sensor `HVAC-TEMP-UNIT-04` monitors Room 202; temperature threshold is set to 26.0°C.
- **Action:**
  - The sensor client posts telemetry: `POST /api/sensor-events/` with `{"source_id": "HVAC-TEMP-UNIT-04", "event_id": "evt-7721-abc", "metric": "temperature_celsius", "value": 29.5, "observed_at": "2026-11-18T14:30:00Z"}`.
  - The same payload is repeated 5 times sequentially or concurrently (simulating network timeouts and retries).
- **Measurable Acceptance Criteria:**
  - First request returns `HTTP 201 Created` and automatically spawns exactly 1 maintenance ticket linked to the breach.
  - Subsequent 4 requests return `HTTP 200 OK` with `{"status": "duplicate_suppressed", "existing_ticket_id": <id>}`.
  - PostgreSQL retains exactly 1 `SensorEvent` record and exactly 1 `Ticket` record.

---

### User Story US05: Evidence-Gated Maintenance Resolution and Closure
- **Story Statement:** As a Maintenance Technician, I want to record timestamped inspection observations, complete repairs, and submit resolution evidence so that tickets cannot be prematurely closed without audit verification.
- **Preconditions:**
  - Ticket `TKT-1042` is in `assigned` status assigned to technician `tech.raj@campus.edu`.
- **Action:**
  - Technician transitions ticket to `in_progress`, posts inspection findings, and attempts closure.
  - Case A: Attempt closure with empty resolution notes.
  - Case B: Submit closure with complete resolution notes: `"Replaced faulty thermal expansion valve; verified ambient cooling to 21.5°C."`.
- **Measurable Acceptance Criteria:**
  - Case A: API returns `HTTP 422 Unprocessable Entity` with validation message `"Resolution notes and verification evidence are required prior to ticket closure."` Ticket remains `in_progress`.
  - Case B: API returns `HTTP 200 OK`. Ticket transitions to `resolved` (and subsequently `closed` by manager verification), recording technician ID, timestamp, and audit event.

---

### User Story US06: Reproducible Containerized Deployment and Persistence
- **Story Statement:** As a System Administrator or DevOps Engineer, I want the full platform to launch reproducibly via containerization and retain all bookings and tickets across container restarts without manual database patching.
- **Preconditions:**
  - Clean host environment with Docker and Docker Compose installed.
- **Action:**
  - Execute `docker compose up -d --build`.
  - Run database migrations and seed data.
  - Insert synthetic booking and ticket.
  - Execute `docker compose restart backend`.
- **Measurable Acceptance Criteria:**
  - Both frontend, backend, and database containers become healthy automatically.
  - Health endpoint `GET /api/health/` returns `HTTP 200 OK` with database status `healthy`.
  - Previously created booking and ticket records remain 100% intact, readable, and queryable with identical IDs and version numbers.
