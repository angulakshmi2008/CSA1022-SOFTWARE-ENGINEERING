# Smart Campus Facility Booking and Maintenance Platform
### Software Engineering Capstone Assignment 3 (CO3, 50 Marks)

**Course**: CSA1022 - Software Engineering  
**Author**: ANGULAKSHMI S  
**Register Number**: 192524402  
**Programme & Section**: CSA10 / Software Engineering  
**Target Repository**: `https://github.com/angulakshmi2008/CSA1022-SOFTWARE-ENGINEERING`  
**Subfolder**: `ASSIGNMENTS/ASSIGNMENT-3/`  
**Release Version**: `v1.0.0`

---

## 1. Project Overview

The **Smart Campus Facility Booking and Maintenance Platform** is a containerized, full-stack, distributed web platform engineered to manage academic space reservations, equipment loans, IoT sensor fault detection, explainable maintenance triage, and DevOps issue tracking across six university campuses.

### Key Capabilities
- **Multi-Campus Facility Catalogue**: Real-time filtering across 6 campuses (North, South, East, West, Innovation, Medical) and room types.
- **Overlap-Free Booking Engine**: Half-open interval reservation validation $[t_{\text{start}}, t_{\text{end}})$ backed by PostgreSQL GiST exclusion constraints and atomic row locking (`SELECT FOR UPDATE`).
- **Explainable Maintenance Triage**: Transparent 3x3 Impact $\times$ Urgency matrix mapping incidents to $M_1$–$M_4$ priorities with SLA response and resolution deadlines.
- **Evidence-Gated Ticket Closure**: Server-enforced requirement that prevents ticket closure without mandatory technician resolution notes (HTTP 422 Unprocessable Entity).
- **IoT Sensor Event Ingestion**: Deterministic deduplication engine suppressing redundant sensor alerts within time windows.
- **Durable Integration Outbox**: Asynchronous webhook and DevOps issue tracker synchronization with stable idempotency keys.
- **Optimistic Concurrency Control (OCC)**: Version-based ticket locking (`expected_version` returning HTTP 409 Conflict on stale updates).
- **Responsive Single-Page Application**: Vue 3 + Vite frontend with interactive demo persona switcher, live calendar, triage rationales, and audit logs.

---

## 2. System Architecture

```
                                [ Web Browser / Client ]
                                            │
                                            ▼ HTTP :80
                          ┌───────────────────────────────────┐
                          │          frontend                 │
                          │   (Vue 3 SPA + Nginx Alpine)      │
                          └─────────────────┬─────────────────┘
                                            │ /api/ reverse proxy
                                            ▼ HTTP :8000
                          ┌───────────────────────────────────┐
                          │          backend                  │
                          │   (Django 5.1 / DRF + Gunicorn)   │
                          └─────────────────┬─────────────────┘
                                            │ TCP :5432
                                            ▼
                          ┌───────────────────────────────────┐
                          │          database                 │
                          │        (PostgreSQL 16)            │
                          │   Persistent Volume: postgres_data│
                          └───────────────────────────────────┘
                                            ▲
                                            │ TCP :5432
                          ┌─────────────────┴─────────────────┐
                          │          worker                   │
                          │  (Async Outbox / Sensor Dispatch) │
                          └───────────────────────────────────┘
```

---

## 3. Directory Structure

```text
ASSIGNMENT-3/
├── backend/                  # Django REST Framework application
│   ├── accounts/             # Custom User model and role-based permissions
│   ├── campuses/             # Multi-campus data models (6 campus locations)
│   ├── facilities/           # Facility catalogue and inventory
│   ├── bookings/             # Booking engine, availability, and overlap check
│   ├── equipment_loans/      # Equipment checkout and loan requests
│   ├── maintenance/          # Maintenance tickets, 3x3 triage matrix, and SLA
│   ├── sensor_events/        # IoT sensor intake and deduplication engine
│   ├── approvals/            # Approval workflow for restricted facilities
│   ├── integrations/         # Durable outbox pattern with idempotency keys
│   ├── audit/                # Comprehensive transactional audit logging
│   └── config/               # Django project settings, URLs, and operating policies
├── frontend/                 # Vue 3 + Vite responsive Single Page Application
│   ├── src/                  # Vue components, persona switcher, API client
│   └── dist/                 # Production-built static assets
├── database/                 # Migrations and automated seed scripts
│   └── seed/                 # Preloads 6 campuses, 8 users, facilities, and SLAs
├── tests/                    # Comprehensive automated testing suite
│   ├── unit/                 # Unit tests for serializers and triage rules
│   ├── api/                  # API integration tests for all REST endpoints
│   ├── concurrency/          # Overlap race condition and version conflict tests
│   └── deployment/           # Persistence and container restart tests
├── deployment/               # Deployment manifests and Docker configurations
│   ├── docker/               # Nginx reverse proxy and load-balancer configs
│   ├── compose/              # Scaling Compose manifests (dual backends)
│   └── scripts/              # Persistence verification scripts
├── docs/                     # Architecture, database diagrams, API contracts, evidence
│   ├── architecture/         # System component and state machine diagrams
│   ├── api/                  # REST API contract documentation
│   └── evidence/             # Load test results, logs, and benchmark data
├── Q1_Scope_and_Technology/  # Specifications, roles, user stories, and evaluation
├── Q2_Integrated_Application_Design/ # Component, data, and state models
├── Q3_Full_Stack_Implementation/     # Architecture, triage workflow, journey log
├── Q4_Git_Workflow/          # Branching, conventional commits, deliberate conflict
├── Q5_Container_Deployment/  # Container architecture, runbook, restart persistence
├── Q6_Concurrency_and_Scaling/# 6-campus impact, concurrency controls, load test
├── Q7_Technical_Reflection/  # Technical reflection, defects fixed, and limitations
├── reference/                # Original PDF and complete academic report docx
├── docker-compose.yml        # Production multi-tier container orchestration
├── pytest.ini                # Pytest configuration
├── .env.example              # Environment variable template
├── README.md                 # Primary system documentation
└── CHANGELOG.md              # Semantic version change history
```

---

## 4. Quickstart Guide (Local Development)

### 4.1 Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run migrations and seed data
python manage.py migrate
python ../database/seed/seed_data.py

# Launch development server
python manage.py runserver 0.0.0.0:8000
```

### 4.2 Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run frontend development server
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 5. Dockerized Deployment (Production)

Deploy the entire containerized stack with a single command:

```bash
# Copy environment configuration
cp .env.example .env

# Build and start all containers in detached mode
docker compose up -d --build

# Run migrations and seed data inside container
docker compose exec backend python manage.py migrate
docker compose exec backend python database/seed/seed_data.py

# Verify service health
docker compose ps
```
The application will be accessible at `http://localhost:80` (or `http://localhost:8000` for backend API).

To verify persistence across backend container teardowns:
```bash
python deployment/scripts/verify_persistence.py
```

---

## 6. Automated Testing & Verification

The platform includes a comprehensive automated test suite verifying all assignment requirements:

```bash
# Run complete test suite
python -m pytest tests/ -v
```

### Test Coverage Summary:
- `test_valid_booking_creation`: Verifies standard facility reservation.
- `test_overlapping_booking_rejection`: Verifies rejection of overlapping intervals.
- `test_unauthorized_restricted_booking`: Verifies RBAC restrictions on specialized labs.
- `test_approval_flow`: Verifies department approver authorization lifecycle.
- `test_duplicate_sensor_event_suppressed`: Verifies deterministic IoT deduplication.
- `test_rejection_of_ticket_closure_without_notes`: Verifies HTTP 422 on empty resolution notes.
- `test_successful_authorized_ticket_closure`: Verifies resolution with valid technician evidence.
- `test_stale_version_update_rejection`: Verifies HTTP 409 on stale ticket version.
- `test_concurrent_overlapping_reservations`: Verifies multithreaded overlap race prevention.
- `test_conflicting_ticket_updates`: Verifies multithreaded optimistic locking.
- `test_duplicate_external_integration_retry`: Verifies durable outbox idempotency.

**Status**: 14/14 tests passing cleanly (100% pass rate).

---

## 7. Empirical Load Test & Capacity Findings

Empirical benchmarking was executed across 10, 25, 50, and 100 concurrent workers (`tests/concurrency/load_test.py`):
- **10 Workers**: 60.3 req/s | $p_{50}$ = 151.9 ms | $p_{99}$ = 159.2 ms | 0% errors
- **25 Workers**: 92.2 req/s | $p_{50}$ = 170.1 ms | $p_{99}$ = 215.4 ms | 0% errors
- **50 Workers**: 111.3 req/s | $p_{50}$ = 221.8 ms | $p_{99}$ = 312.0 ms | 0% errors
- **100 Workers**: 119.9 req/s | $p_{50}$ = 367.4 ms | $p_{99}$ = 625.8 ms | 0% errors

*Academic Honesty Disclosure*: Verified capacity supports up to **100 concurrent workers (119.9 req/s)** with 0% data corruption. Scaling to 300 simultaneous users requires production PgBouncer connection pooling and Redis caching.

---

## 8. Academic Integrity & License
This project is submitted as an individual capstone assessment for Course **CSA1022 - Software Engineering**. All code, architectural designs, test suites, and empirical benchmarks are authored by **ANGULAKSHMI S** (Reg No: 192524402).
