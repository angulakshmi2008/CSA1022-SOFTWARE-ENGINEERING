# Question 4: Release Tag `v1.0.0` & Version Traceability

## 1. Release Tag Specification

Following the successful resolution of the deliberate merge conflict and green test validation, the production baseline on `main` was anchored with an annotated release tag: `v1.0.0`.

### 1.1 Tag Details
- **Tag Name**: `v1.0.0`
- **Target Branch**: `main`
- **Release Title**: Smart Campus Facility Booking & Maintenance Platform v1.0.0
- **Tag Message**:
  ```
  Release v1.0.0 - Complete containerized Smart Campus Facility Booking and Maintenance Platform
  - Multi-campus facility catalogue with half-open reservation interval validation
  - Optimistic concurrency control (HTTP 409) and GiST exclusion constraints
  - Explainable maintenance triage matrix with mandatory resolution evidence
  - Deterministic sensor event intake with duplicate suppression
  - Durable integration outbox with stable idempotency keys
  - Responsive Vue 3 single page application with persona simulator
  - Fully containerized multi-tier Docker Compose deployment
  - Comprehensive 14-test automated test suite passing
  ```

---

## 2. Tag Verification & Inspection

Command executed to inspect the tag:
```bash
$ git tag -n9 -l "v1.0.0"
v1.0.0          Release v1.0.0 - Complete containerized Smart Campus Facility Booking and Maintenance Platform
```

Command executed to verify tag metadata and commit hash:
```bash
$ git show v1.0.0 --stat
```

---

## 3. Version Traceability Matrix

Every core requirement is traceably anchored to this release tag:

| Requirement / User Story | Codebase Component | Verification Test | Release Hash Coverage |
| :--- | :--- | :--- | :--- |
| **US01: Facility Booking** | `backend/bookings/models.py`, `serializers.py` | `test_valid_booking_creation` | Included in `v1.0.0` |
| **US02: Overlap Prevention** | `backend/bookings/views.py` | `test_overlapping_booking_rejection`, `test_concurrent_overlapping_reservations` | Included in `v1.0.0` |
| **US03: Restricted Approvals**| `backend/approvals/views.py` | `test_unauthorized_restricted_booking`, `test_approval_flow` | Included in `v1.0.0` |
| **US04: Sensor Deduplication**| `backend/sensor_events/views.py` | `test_duplicate_sensor_event_suppressed` | Included in `v1.0.0` |
| **US05: Maintenance Closure** | `backend/maintenance/views.py` | `test_rejection_of_ticket_closure_without_notes`, `test_successful_authorized_ticket_closure` | Included in `v1.0.0` |
| **US06: Concurrency Control**| `backend/maintenance/models.py`, `views.py` | `test_stale_version_update_rejection`, `test_conflicting_ticket_updates` | Included in `v1.0.0` |
| **DevOps Integration** | `backend/integrations/models.py`, `tasks.py` | `test_duplicate_external_integration_retry` | Included in `v1.0.0` |
