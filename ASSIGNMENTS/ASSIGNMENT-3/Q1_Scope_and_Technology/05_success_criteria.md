# Measurable Success and Reproducibility Criteria

## 1. Overview
This specification establishes quantifiable, test-verifiable criteria to assess the operational success of the Smart Campus Platform across functionality, security, concurrency, container reproducibility, and data persistence.

---

## 2. Functional & API Correctness Criteria

| Metric ID | Target Dimension | Measurable Target / Threshold | Verification Method |
|---|---|---|---|
| **SC-F01** | Booking Creation | Returns `HTTP 201 Created` with unique ID, status, and version for valid intervals. | Automated API test and UI booking submission verification. |
| **SC-F02** | Overlap Prevention | 100% of conflicting overlapping reservations for the same facility return `HTTP 409 Conflict`. Zero double-booked active intervals in storage. | Concurrent dual-request HTTP test suite (`tests/concurrency/test_concurrent_overlapping_bookings.py`). |
| **SC-F03** | Telemetry Deduplication | Identical `(source_id, event_id)` payloads submitted 5 times yield exactly 1 maintenance ticket and 4 duplicate acknowledgements. | Automated deduplication test suite (`tests/concurrency/test_sensor_deduplication.py`). |
| **SC-F04** | Resolution Enforcement | Attempting ticket closure without mandatory resolution notes returns `HTTP 422 Unprocessable Entity`. | Negative API validation test case (`tests/api/test_tickets_api.py`). |
| **SC-F05** | Triage Explainability | Triage recommendations return the category, calculated priority ($M1$ to $M4$), and the human-readable explanation rule. | Unit test verifying the triage engine against keyword and impact-urgency matrices. |

---

## 3. Authorization & Security Criteria

| Metric ID | Target Dimension | Measurable Target / Threshold | Verification Method |
|---|---|---|---|
| **SC-S01** | Unauthorized Access Denial | Non-approver (Student/Technician) attempting restricted facility or ticket approval receives `HTTP 403 Forbidden`. | Security permission tests (`tests/api/test_permissions_api.py`). |
| **SC-S02** | Session Identity Derivation | Actor identity is extracted authoritatively from verified server session/token; client tampering of `requester_id` is rejected. | Tamper injection test verifying actor ID matches JWT/token identity. |
| **SC-S03** | Audit Trail Completeness | 100% of state transitions (bookings, ticket updates, approvals) generate an immutable `AuditEvent` with actor, action, timestamp, and state delta. | Transactional database inspection after test workflow execution. |
| **SC-S04** | Secrets Sanitization | Zero unencrypted credentials, passwords, or production secrets committed in git history or tracked repository files. | Automated `.gitignore` and git history inspection. |

---

## 4. Concurrency & High-Availability Scaling Criteria

| Metric ID | Target Dimension | Measurable Target / Threshold | Verification Method |
|---|---|---|---|
| **SC-C01** | Dual Backend Consistency | Two independent backend instances (`backend-1`, `backend-2`) process interleaved requests against a shared PostgreSQL database without state divergence. | Nginx reverse proxy load balancer routing requests across both instances. |
| **SC-C02** | Optimistic Lock Collision | Concurrent competing updates to the same ticket version yield exactly 1 success (`HTTP 200 OK`) and 1 conflict (`HTTP 409 Conflict`). | Concurrent threading test (`tests/concurrency/test_conflicting_ticket_updates.py`). |
| **SC-C03** | Instance Failover Resilience | Terminating one backend instance during active traffic causes zero request drops or state corruption on the surviving instance. | Failover test script executing requests during container restart. |
| **SC-C04** | Stepped Workload Verification | Successful execution of stepped concurrency tests (10, 25, 50, 100 concurrent requests) reporting p50, p95, and p99 response latencies without deadlocks. | Automated load test benchmark (`tests/concurrency/load_test.py`). |

---

## 5. Deployment Reproducibility & Persistence Criteria

| Metric ID | Target Dimension | Measurable Target / Threshold | Verification Method |
|---|---|---|---|
| **SC-D01** | Clean Environment Launch | `docker compose up --build -d` provisions all services, applies migrations, and establishes readiness without manual database intervention. | Execution of clean build on empty Docker volume. |
| **SC-D02** | Service Healthchecks | PostgreSQL and Django backend report `healthy` via automated Docker healthchecks prior to accepting ingress web traffic. | `docker compose ps` status inspection. |
| **SC-D03** | Application Restart Persistence | Data created prior to `docker compose restart backend` survives with 100% fidelity, matching IDs, timestamps, and audit events. | Automated persistence test (`deployment/scripts/verify_persistence.py`). |
| **SC-D04** | Git Release Traceability | Source code corresponding to deployment is uniquely tagged as `v1.0.0` with conventional commit history and documented conflict resolution. | `git tag -v v1.0.0` and `git log --graph` inspection. |
