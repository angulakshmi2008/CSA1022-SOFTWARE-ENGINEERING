# RESTful API Contracts Specification

## 1. Overview
All endpoints accept and return `application/json`. Authenticated endpoints require a valid session cookie or Authorization header:
`Authorization: Bearer <token>` or `Authorization: Token <token>`.
System-level errors return standard RFC 7807 problem details with fields `error`, `detail`, `code`, and `timestamp`.

---

## 2. Core API Endpoint Contracts

### 2.1 Facilities Catalogue
- **Endpoint:** `GET /api/facilities/`
- **Access:** Any authenticated user.
- **Query Parameters:**
  - `campus`: (int, optional) Filter by campus ID.
  - `type`: (string, optional) Filter by facility type (`lecture_hall`, `computer_lab`, etc.).
  - `capacity_min`: (int, optional) Filter facilities by minimum capacity.
- **Success Response (`HTTP 200 OK`):**
  ```json
  [
    {
      "id": 1,
      "campus": 1,
      "campus_name": "Main University Campus",
      "name": "Robotics Automation Lab 101",
      "code": "ENG-ROBO-101",
      "facility_type": "research_lab",
      "capacity": 35,
      "is_restricted": true,
      "is_active": true
    }
  ]
  ```

---

### 2.2 Facility Booking Availability Calendar
- **Endpoint:** `GET /api/bookings/calendar/`
- **Access:** Any authenticated user.
- **Query Parameters:**
  - `facility_id`: (int, required) Facility ID to query.
  - `start`: (ISO 8601 string, required) e.g., `2026-11-20T00:00:00Z`
  - `end`: (ISO 8601 string, required) e.g., `2026-11-20T23:59:59Z`
- **Success Response (`HTTP 200 OK`):**
  ```json
  [
    {
      "id": 101,
      "facility_id": 1,
      "start_at": "2026-11-20T10:00:00Z",
      "end_at": "2026-11-20T12:00:00Z",
      "status": "confirmed",
      "purpose": "Academic Session",
      "requester_name": "Dr. Smith"
    }
  ]
  ```

---

### 2.3 Create Booking Reservation
- **Endpoint:** `POST /api/bookings/`
- **Access:** Authenticated users (`Student`, `Faculty`, `Manager`, `Admin`).
- **Request Body:**
  ```json
  {
    "facility_id": 1,
    "start_at": "2026-11-20T14:00:00Z",
    "end_at": "2026-11-20T16:00:00Z",
    "purpose": "Mechatronics Laboratory Practical",
    "request_key": "req-booking-token-9981"
  }
  ```
- **Responses:**
  - `HTTP 201 Created` (Success):
    ```json
    {
      "id": 105,
      "facility": 1,
      "facility_name": "Robotics Automation Lab 101",
      "requester": 4,
      "requester_name": "Dr. Smith",
      "start_at": "2026-11-20T14:00:00Z",
      "end_at": "2026-11-20T16:00:00Z",
      "status": "confirmed",
      "version": 1,
      "request_key": "req-booking-token-9981",
      "created_at": "2026-11-18T15:20:00Z"
    }
    ```
  - `HTTP 409 Conflict` (Overlap Rejection):
    ```json
    {
      "error": "Booking Conflict",
      "detail": "The requested facility is already reserved during this time interval.",
      "code": "OVERLAPPING_RESERVATION"
    }
    ```
  - `HTTP 403 Forbidden` (Restricted Facility Policy):
    ```json
    {
      "error": "Permission Denied",
      "detail": "Students are not permitted to reserve restricted research facilities directly.",
      "code": "RESTRICTED_FACILITY_ACCESS"
    }
    ```
  - `HTTP 422 Unprocessable Entity` (Malformed Duration):
    ```json
    {
      "error": "Invalid Time Range",
      "detail": "Booking end time must occur after start time.",
      "code": "INVALID_TIME_INTERVAL"
    }
    ```

---

### 2.4 Update Booking Lifecycle State
- **Endpoint:** `PATCH /api/bookings/{id}/status/`
- **Access:** Requester (cancellation only), Facility Manager, Admin.
- **Request Body:**
  ```json
  {
    "target_status": "cancelled",
    "expected_version": 1,
    "reason": "Lecture rescheduled"
  }
  ```
- **Responses:**
  - `HTTP 200 OK`: Updated booking record with version incremented (`version: 2`).
  - `HTTP 409 Conflict`: Expected version does not match database version (stale update).

---

### 2.5 Ingest Sensor Telemetry Event
- **Endpoint:** `POST /api/sensor-events/`
- **Access:** Authenticated Sensor Client / Internal Services.
- **Request Body:**
  ```json
  {
    "source_id": "HVAC-TEMP-UNIT-04",
    "event_id": "evt-7721-abc",
    "metric": "temperature_celsius",
    "value": 29.8,
    "observed_at": "2026-11-18T14:30:00Z"
  }
  ```
- **Responses:**
  - `HTTP 201 Created` (New Event Triggering Breach):
    ```json
    {
      "status": "processed",
      "event_id": "evt-7721-abc",
      "threshold_breached": true,
      "ticket_created": true,
      "ticket_id": 1042,
      "triage_summary": "High temperature alert - Priority M1 Critical"
    }
    ```
  - `HTTP 200 OK` (Duplicate Suppressed):
    ```json
    {
      "status": "duplicate_suppressed",
      "event_id": "evt-7721-abc",
      "message": "Event previously ingested; duplicate processing skipped.",
      "linked_ticket_id": 1042
    }
    ```

---

### 2.6 Maintenance Ticket State & Lifecycle Command
- **Endpoint:** `PATCH /api/tickets/{id}/state/`
- **Access:** Assigned Technician, Facility Manager, Admin.
- **Request Body:**
  ```json
  {
    "target_state": "resolved",
    "expected_version": 2,
    "resolution_notes": "Cleaned evaporator coils, purged refrigerant line, ambient temperature normalized to 20.8°C."
  }
  ```
- **Responses:**
  - `HTTP 200 OK` (Valid State Transition):
    ```json
    {
      "id": 1042,
      "status": "resolved",
      "version": 3,
      "assignee": 8,
      "resolution_notes": "Cleaned evaporator coils, purged refrigerant line, ambient temperature normalized to 20.8°C.",
      "updated_at": "2026-11-18T15:30:00Z"
    }
    ```
  - `HTTP 422 Unprocessable Entity` (Missing Mandatory Resolution Evidence):
    ```json
    {
      "error": "Missing Resolution Evidence",
      "detail": "Resolution notes and verification evidence are mandatory before resolving or closing a ticket.",
      "code": "RESOLUTION_NOTES_REQUIRED"
    }
    ```
  - `HTTP 409 Conflict` (Optimistic Concurrency Collision):
    ```json
    {
      "error": "Concurrent Modification Conflict",
      "detail": "Ticket was modified by another user. Refresh the current record before submitting changes.",
      "current_version": 3,
      "code": "STALE_VERSION_CONFLICT"
    }
    ```

---

### 2.7 Approval Decision
- **Endpoint:** `POST /api/approvals/`
- **Access:** Department Approver, Admin.
- **Request Body:**
  ```json
  {
    "request_type": "booking",
    "request_id": 105,
    "decision": "approved",
    "reason": "Departmental safety protocol and risk assessment validated."
  }
  ```
- **Responses:**
  - `HTTP 200 OK` / `201 Created`: Approval recorded, target resource updated, audit event appended.
  - `HTTP 403 Forbidden`: Non-approver attempting decision.
  - `HTTP 409 Conflict`: Target item is no longer pending approval.

---

### 2.8 DevOps / Integration Intent Hub
- **Endpoint:** `POST /api/integration-intents/`
- **Access:** Facility Manager, Admin, Service Worker.
- **Request Body:**
  ```json
  {
    "ticket_id": 1042,
    "operation": "create_developer_issue",
    "correlation_key": "CAMP-318-TKT-1042"
  }
  ```
- **Responses:**
  - `HTTP 202 Accepted` (New Intent Enqueued):
    ```json
    {
      "id": 44,
      "ticket_id": 1042,
      "correlation_key": "CAMP-318-TKT-1042",
      "status": "pending",
      "attempts": 0
    }
    ```
  - `HTTP 200 OK` (Reconciliation on Existing Key):
    ```json
    {
      "id": 44,
      "correlation_key": "CAMP-318-TKT-1042",
      "status": "confirmed",
      "external_id": "GH-ISSUE-889"
    }
    ```
