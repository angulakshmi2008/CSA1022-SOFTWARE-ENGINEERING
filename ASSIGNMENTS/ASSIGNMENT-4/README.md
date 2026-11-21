# Smart Campus Facility Platform — Software Engineering Assignment 4 (CO4)

[![CI/CD Delivery Pipeline](https://github.com/angulakshmi2008/CSA1022-SOFTWARE-ENGINEERING/actions/workflows/ci.yml/badge.svg)](https://github.com/angulakshmi2008/CSA1022-SOFTWARE-ENGINEERING/actions)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![Code Coverage](https://img.shields.io/badge/coverage-83.55%25-brightgreen.svg)](docs/evidence/coverage-report/index.html)
[![Security: Bandit Clean](https://img.shields.io/badge/security-bandit%20passed-green.svg)](docs/evidence/security-scan.json)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**Student Name:** ANGULAKSHMI S  
**Register Number:** 192524402  
**Course:** CSA10 – Software Engineering (CO4 Delivery)  
**Institution:** SIMATS Engineering  
**Submission Date:** 21 November 2026  

---

## 1. Project Overview & Scenario

The **Smart Campus Facility Platform** is a backend system engineered to manage facility reservations, environmental telemetry ingestion, automated incident dispatch, and maintenance workflows across multiple campus sites.

In continuous delivery environments, frequent code releases alter booking policies, sensor thresholds, ticket state machines, and authorization rules. This project validates a **risk-based testing strategy and an automated DevOps delivery pipeline** that prevents unvetted changes from causing double bookings, unauthorized access, false-positive alarms, or migration failures.

### Key Verification Metrics
- **Automated Tests:** 40 / 40 Passing (100% Pass Rate in 1.96 seconds)
- **Line Code Coverage:** 83.55% (Exceeds required 80.0% quality gate)
- **Controlled Defect Negative Controls:** 2/2 Defect Injections Detected & Retested
- **Bandit Security AST Analysis:** 0 High / 0 Medium / 0 Low Issues (1,920 LOC)
- **Bounded Load Test Throughput:** 223.30 Requests/Second (44.19 ms mean latency)
- **Disaster Recovery Rehearsal:** PRAGMA integrity_check clean, 0 Foreign Key Errors, 100% Row Preservation

---

## 2. Core Functional Features

1. **User & Role Management:** 6 distinct roles (`ADMINISTRATOR`, `FACILITY_MANAGER`, `MAINTENANCE_TECHNICIAN`, `DEPARTMENT_APPROVER`, `FACULTY_MEMBER`, `STUDENT`) with strict Role-Based Access Control (RBAC).
2. **Facility Catalog & Multi-Campus Policies:** Configurable booking duration limits (e.g., 180 min default, 120 min North Campus) and environmental sensor thresholds (e.g., 28.0°C default, 26.0°C Server Room).
3. **Booking Management & Overlap Detection:**
   - Maximum duration validation (180 min accepted, 181 min rejected with HTTP 400).
   - Half-open interval overlap check `[start, end)`: overlapping bookings rejected with HTTP 409 Conflict; adjacent back-to-back bookings accepted with HTTP 201 Created.
4. **Restricted Facility Approval Workflow:** Restricted laboratories require approver elevation. Direct API authorization blocks student attempts with HTTP 403 Forbidden while leaving database state invariant.
5. **Sensor Telemetry Processing & Idempotency:**
   - Strict greater-than evaluation (`value > threshold`): 28.00°C does not breach, 28.01°C breaches!
   - Event deduplication: replayed sensor events return existing records without duplicating tickets.
6. **Maintenance Ticket Lifecycle:**
   - Strict 5-stage lifecycle: `New -> Assigned -> In Progress -> Resolved -> Closed`.
   - Resolution notes are mandatory before transitioning into `Resolved`.
   - Optimistic concurrency control using expected version numbers (stale versions return HTTP 409).
7. **Transactional Outbox Synchronization:** Decouples external Google Calendar and Jira APIs. Retries with exponential backoff and never marks failed external calls as successful.

---

## 3. Technology Stack

| Layer | Selected Technology | Version | Purpose |
|---|---|---|---|
| Language | Python | 3.12 / 3.13 | High-performance asynchronous backend runtime |
| Web Framework | FastAPI | 0.115.x | High-speed REST API with automatic OpenAPI documentation |
| Database | SQLite 3 | 3.x | ACID-compliant relational persistence with WAL mode |
| ORM | SQLAlchemy | 2.0.x | Type-safe declarative models and relationship mapping |
| Migrations | Alembic | 1.14.x | Version-controlled schema migrations with batch mode |
| Testing | Pytest & HTTPX | 9.2.x | Multi-tier unit, integration, and regression test runner |
| Code Coverage | pytest-cov | 6.0.x | Cobertura XML and interactive HTML line coverage reports |
| Linter / Formatter | Ruff | 0.9.x | Ultra-fast AST-based code style and import verification |
| Security Scanner | Bandit | 1.9.x | Python AST static vulnerability scanner |
| Supply Chain Audit | pip-audit | 2.10.x | Dependency CVE vulnerability auditor |
| Containerization | Docker & Compose | 3.8+ | Ephemeral, isolated multi-stage container packaging |
| CI/CD Pipeline | GitHub Actions | Ubuntu-latest | Gated automated continuous integration and delivery |

---

## 4. Repository Structure

```text
Smart-Campus-Facility-Platform-Assignment4/
│
├── app/                                # Application Source Code
│   ├── __init__.py                     # Package definition
│   ├── main.py                         # FastAPI gateway & health endpoints
│   ├── config.py                       # Pydantic environment configuration
│   ├── database.py                     # SQLAlchemy session & SQLite engine
│   ├── models/                         # Database Domain Models
│   │   ├── user.py                     # User & UserRole definitions
│   │   ├── facility.py                 # Facility & FacilityPolicy models
│   │   ├── booking.py                  # Booking model & status enum
│   │   ├── sensor_event.py             # Sensor telemetry & threshold model
│   │   ├── ticket.py                   # Maintenance ticket & state machine
│   │   ├── audit.py                    # Immutable audit logging table
│   │   └── outbox_event.py             # Transactional outbox queue model
│   ├── schemas/                        # Pydantic Request/Response DTOs
│   ├── routers/                        # API Route Controllers (/api/v1 & /api/v2)
│   ├── services/                       # Core Domain Services & Business Logic
│   ├── security/                       # Authentication (JWT) & Authorization (RBAC)
│   └── integrations/                   # External Calendar & Issue Tracker Adapters
│
├── tests/                              # Automated Test Suite (40 Tests)
│   ├── conftest.py                     # Pytest fixtures & StaticPool SQLite setup
│   ├── unit/                           # Isolated unit tests (U1–U6)
│   ├── integration/                    # Multi-component API tests (I1–I4)
│   └── regression/                     # Release baseline regression tests (R1–R4)
│
├── migrations/                         # Alembic Database Migrations
│   ├── env.py                          # Alembic runtime environment
│   └── versions/                       # 001_initial_schema & 002_add_campus_policies
│
├── scripts/                            # Verification & Operational Scripts
│   ├── run_tests.py                    # Comprehensive test runner with reports
│   ├── demonstrate_defects.py          # Controlled defect injection & retest
│   ├── smoke_test.py                   # Post-deployment health & API smoke probe
│   ├── load_test.py                    # Bounded load experiment (200 requests)
│   ├── backup.py                       # Online SQLite database snapshot
│   ├── restore.py                      # Database restore & integrity verification
│   └── verify_migration.py             # Alembic migration rehearsal
│
├── docs/                               # Engineering Documentation & Artifacts
│   ├── diagrams/                       # 11 Mermaid Architecture & Workflow Source Files
│   ├── evidence/                       # Real Execution Logs, XML & CSV Outputs
│   └── submission/                     # Final Academic Reports (DOCX & 28-Page PDF)
│
├── .github/workflows/ci.yml            # 5-Stage GitHub Actions Pipeline Configuration
├── Dockerfile                          # Production Multi-Stage Container Specification
├── docker-compose.yml                  # Container Stack Orchestration
├── requirements.txt                    # Pinned Production Dependencies
├── pyproject.toml                      # Build tool, Ruff, Pytest & Coverage settings
├── .env.example                        # Template environment variables
├── .gitignore                          # Hardened source control exclusion rules
├── SECURITY.md                         # Security policy & vulnerability reporting
└── Makefile                            # Developer automation shortcuts
```

---

## 5. Local Installation & Quick Start

### 5.1 Prerequisites
- Python 3.12 or 3.13 installed
- Git installed
- Windows PowerShell, macOS Terminal, or Linux Bash

### 5.2 Virtual Environment Setup

```bash
# Clone the repository
git clone https://github.com/angulakshmi2008/CSA1022-SOFTWARE-ENGINEERING.git
cd CSA1022-SOFTWARE-ENGINEERING/ASSIGNMENTS/ASSIGNMENT-4

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install pinned dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 5.3 Database Migration & Local Startup

```bash
# Initialize database tables via Alembic
alembic upgrade head

# Start local development server with live reload
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Interactive documentation is available at:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`
- **Health Check Probe:** `http://127.0.0.1:8000/health`

---

## 6. Automated Testing & Evidence Verification

Execute the complete 40-test suite with coverage and JUnit XML generation:

```bash
python -m pytest tests -v --cov=app --cov-report=html:docs/evidence/coverage-report --cov-report=xml:docs/evidence/coverage.xml --junitxml=docs/evidence/test-results.xml
```

### 6.1 Test Suite Layer Breakdown

| Test Group | Command | Checks | Focus Area |
|---|---|---:|---|
| **Unit Tests** | `pytest tests/unit -v` | 24 | Priority matrix (U1-U3), triage (U4-U5), sensor > (U6), SLA boundaries |
| **Integration Tests** | `pytest tests/integration -v` | 9 | Ticket persistence (I1), idempotency (I2), RBAC (I3), overlap (I4) |
| **Regression Tests** | `pytest tests/regression -v` | 7 | Priority (R1), unknown triage (R2), notes (R3), stale lock (R4), multi-campus |
| **Complete Suite** | `pytest tests -v` | **40** | **100% Passing in 1.96 seconds (83.55% Line Coverage)** |

### 6.2 Controlled Defect Demonstrations (Task Q3)

Execute the automated defect injection and retest script:

```bash
python scripts/demonstrate_defects.py
```

1. **Controlled Defect 1 (Sensor Threshold Equality):**
   - *Injected change:* `return value >= threshold` in `app/services/sensor_service.py`
   - *Observed failure:* `assert (True, True) == (False, True)` (`True != False` at index 0)
   - *Correction:* Restored strict greater-than `return value > threshold` -> Retest PASSED!
   - *Evidence files:* `docs/evidence/defect-1-failure.txt` and `defect-1-correction.txt`

2. **Controlled Defect 2 (Priority Matrix Misclassification):**
   - *Injected change:* `PRIORITY_MATRIX["High"]["High"] = "M2"` in `app/services/priority_service.py`
   - *Observed failure:* `assert 'M2' == 'M1'`
   - *Correction:* Restored `M1` mapping -> Retest PASSED!
   - *Evidence files:* `docs/evidence/defect-2-failure.txt` and `defect-2-correction.txt`

---

## 7. Operational Scripts & Empirical Validation

```bash
# 1. Deployment Smoke Probe
python scripts/smoke_test.py
# Output: docs/evidence/smoke-test.log

# 2. Bounded Load Test (200 requests, 10 threads)
python scripts/load_test.py
# Output: docs/evidence/load-test-results.csv (223.3 RPS, 44.19 ms mean latency)

# 3. Database Schema Migration Rehearsal (001 -> 002)
python scripts/verify_migration.py
# Output: docs/evidence/migration-validation.log (100% row preservation, 0 FK errors)

# 4. Disaster Recovery & Rollback Drill
python scripts/backup.py
python scripts/restore.py
# Output: docs/evidence/recovery-validation.md (PRAGMA integrity_check: ok)
```

---

## 8. CI/CD Delivery Pipeline & Quality Gates

The pipeline is defined in `.github/workflows/ci.yml` and enforces five sequential gates:

1. **Gate 1: Linting Gate (`ruff check app tests`):** Code quality, style, and import hygiene.
2. **Gate 2: Automated Testing Gate (`pytest tests`):** 40/40 tests must pass; line coverage >= 80%.
3. **Gate 3: Security Gate (`bandit` & `pip-audit`):** Static security analysis and CVE inspection.
4. **Gate 4: Container Build Gate (`docker build`):** Traceable build tagged with Git commit SHA.
5. **Gate 5: Smoke Verification Gate (`scripts/smoke_test.py`):** Service readiness and API smoke journey.

---

## 9. Docker Containerization & Run Instructions

```bash
# Build production Docker image
docker build -t campus-platform:latest .

# Run with Docker Compose
docker compose up -d

# Verify container status and logs
docker compose ps
docker compose logs -f

# Verify container health probe
curl http://localhost:8000/health

# Teardown container stack
docker compose down
```

---

## 10. Technical Documentation Deliverables

All academic documentation and report deliverables are located in `docs/`:
- **Word Report:** [`docs/submission/Assignment4_Final_Report.docx`](docs/submission/Assignment4_Final_Report.docx)
- **PDF Report:** [`docs/submission/Assignment4_Final_Report.pdf`](docs/submission/Assignment4_Final_Report.pdf) (28 substantive pages)
- **Architecture & Workflow Diagrams:** 11 `.mmd` Mermaid source files in [`docs/diagrams/`](docs/diagrams/)
- **Validation Evidence:** Real execution logs, XML, and CSV outputs in [`docs/evidence/`](docs/evidence/)

---

## 11. Git & Push Instructions

This repository is prepared for direct synchronization with the main coursework repository:

```bash
# Verify git status
git status

# Stage all files in ASSIGNMENT-4
git add ASSIGNMENTS/ASSIGNMENT-4

# Commit changes
git commit -m "Complete Software Engineering Assignment 4 implementation and validation"

# Push to GitHub main branch
git push origin main
```
