# End-to-End Operational Journey Demonstration

## 1. Journey Overview
This document logs the step-by-step execution of a complete operational journey through the Smart Campus Platform, integrating facility booking, sensor threshold intake, explainable triage, technician assignment, inspection, restricted change approval, and evidence-verified closure.

---

## 2. Step-by-Step Execution Record

### Step 1: Faculty Submits Facility Reservation
- **Actor:** `faculty.dr.anand` (Faculty Member)
- **API Request:** `POST /api/bookings/`
- **Payload:**
  ```json
  {
    "facility_id": 2,
    "start_at": "2026-11-22T09:00:00Z",
    "end_at": "2026-11-22T11:00:00Z",
    "purpose": "Autonomous Robotics Lab Session",
    "request_key": "journey-req-001"
  }
  ```
- **API Response:** `HTTP 201 Created`
  ```json
  {
    "id": 16,
    "facility": 2,
    "facility_name": "Alan Turing Computer Laboratory",
    "facility_code": "MAIN-CS-LAB-01",
    "status": "confirmed",
    "version": 1,
    "request_key": "journey-req-001"
  }
  ```

---

### Step 2: Overlapping Reservation Attempt (Negative Validation)
- **Actor:** `student.arun` (Student)
- **API Request:** `POST /api/bookings/`
- **Payload:** Overlapping slot (`2026-11-22T10:00:00Z` to `12:00:00Z` for Facility 2).
- **API Response:** `HTTP 409 Conflict`
  ```json
  {
    "error": "Booking Conflict",
    "detail": "The requested facility is already reserved during this time interval.",
    "code": "OVERLAPPING_RESERVATION",
    "conflicting_booking_id": 16
  }
  ```
- **Result:** Overlap successfully prevented at the storage boundary.

---

### Step 3: Automated Sensor Threshold Event Intake
- **Actor:** Automated IoT Sensor Client (`HVAC-TEMP-UNIT-04`)
- **API Request:** `POST /api/sensor-events/`
- **Payload:**
  ```json
  {
    "source_id": "HVAC-TEMP-UNIT-04",
    "event_id": "evt-journey-chiller-fault-01",
    "metric": "temperature_celsius",
    "value": 31.4,
    "observed_at": "2026-11-21T16:15:00Z",
    "facility_id": 2
  }
  ```
- **API Response:** `HTTP 201 Created`
  ```json
  {
    "status": "processed",
    "event_id": "evt-journey-chiller-fault-01",
    "threshold_breached": true,
    "ticket_created": true,
    "ticket_id": 5,
    "priority": "M1",
    "triage_summary": "[Explainable Triage Engine]\n1. Categorization: Matched keyword(s) ['temperature', 'hvac'] mapping to category 'hvac'.\n2. Priority Assessment: Impact='HIGH' and Urgency='HIGH' evaluate via matrix to Priority M1.\n3. SLA Target: Assigned resolution deadline of 120 minutes (2.0 hours)."
  }
  ```

---

### Step 4: Duplicate Telemetry Retry (Suppression Verification)
- **Action:** Repeating the identical payload from Step 3.
- **API Response:** `HTTP 200 OK`
  ```json
  {
    "status": "duplicate_suppressed",
    "event_id": "evt-journey-chiller-fault-01",
    "message": "Duplicate telemetry event suppressed; event previously recorded.",
    "existing_ticket_id": 5
  }
  ```
- **Result:** No duplicate ticket created. Ticket count remains 1.

---

### Step 5: Facility Manager Assigns Maintenance Technician
- **Actor:** `manager.priya` (Facility Manager)
- **API Request:** `PATCH /api/tickets/5/assign/`
- **Payload:** `{"assignee_id": 4}` (`tech.rajesh`)
- **API Response:** `HTTP 200 OK`
  ```json
  {
    "id": 5,
    "status": "assigned",
    "assignee": 4,
    "assignee_name": "Rajesh Kannan",
    "version": 2
  }
  ```

---

### Step 6: Technician Records Inspection Findings
- **Actor:** `tech.rajesh` (Technician)
- **API Request:** `POST /api/tickets/5/inspections/`
- **Payload:** `{"notes": "Diagnosed condenser coil: coolant pressure dropped to 18 PSI due to cracked solenoid valve."}`
- **API Response:** `HTTP 201 Created` (Comment logged).

---

### Step 7: Restricted Change Request & Department Approval
- **Technician Request:** `PATCH /api/tickets/5/state/` with `{"target_state": "pending_approval", "expected_version": 2, "is_restricted_change": true}`
- **Approver Decision:** `POST /api/approvals/`
  - **Actor:** `approver.dr.kumar` (Department Approver)
  - **Payload:**
    ```json
    {
      "request_type": "ticket_change",
      "request_id": 5,
      "decision": "approved",
      "reason": "Emergency chiller component replacement authorized under urgent operations fund."
    }
    ```
  - **API Response:** `HTTP 201 Created`. Target Ticket #5 transitions back to `in_progress`.

---

### Step 8: Premature Closure Rejection (Negative Validation)
- **Technician Request:** `PATCH /api/tickets/5/state/` with `{"target_state": "resolved", "expected_version": 3, "resolution_notes": ""}`
- **API Response:** `HTTP 422 Unprocessable Entity`
  ```json
  {
    "error": "Validation Error",
    "details": {
      "resolution_notes": ["Resolution notes and verification evidence are mandatory prior to resolving or closing a ticket."]
    },
    "code": "RESOLUTION_EVIDENCE_REQUIRED"
  }
  ```

---

### Step 9: Authorized Resolution and Manager Verification Closure
- **Technician Request:** `PATCH /api/tickets/5/state/`
  - **Payload:**
    ```json
    {
      "target_state": "resolved",
      "expected_version": 3,
      "resolution_notes": "Installed new Danfoss solenoid valve; evacuated and recharged R410A refrigerant to 42 PSI; ambient temperature normalized to 21.2°C."
    }
    ```
  - **API Response:** `HTTP 200 OK` (Status: `resolved`, Version: 4).
- **Manager Closure:** `PATCH /api/tickets/5/state/`
  - **Actor:** `manager.priya`
  - **Payload:** `{"target_state": "closed", "expected_version": 4, "resolution_notes": "Verified telemetry readings stable for 45 minutes; closed work order."}`
  - **API Response:** `HTTP 200 OK` (Status: `closed`, Version: 5).

---

### Step 10: Linked DevOps / External Issue Enqueue
- **API Request:** `POST /api/integration-intents/`
  - **Payload:** `{"ticket_id": 5, "operation": "create_developer_issue", "correlation_key": "CAMP-318-TKT-5"}`
  - **API Response:** `HTTP 201 Created`
  ```json
  {
    "id": 2,
    "ticket": 5,
    "correlation_key": "CAMP-318-TKT-5",
    "external_id": "GH-ISSUE-5-DEV",
    "status": "confirmed"
  }
  ```
- **Conclusion:** Full lifecycle executed with 100% data persistence and auditable traceability.
