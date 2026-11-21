# Changelog
All notable changes to the Smart Campus Facility Booking and Maintenance Platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-11-21

### Added
- **Campuses**: Multi-campus topology supporting 6 distinct university campus entities (North, South, East, West, Innovation, Medical) with timezone and geographic attributes.
- **Facilities**: Facility catalogue with category filtering (Lecture Hall, Lab, Seminar Room), capacity management, and restricted-access flags.
- **Bookings**: Reservation engine with half-open interval availability checks $[t_{\text{start}}, t_{\text{end}})$, PostgreSQL GiST range exclusion constraints, and atomic row-level locking (`SELECT FOR UPDATE`).
- **Maintenance**: Explainable triage engine combining automated keyword taxonomy with a 3x3 Impact $\times$ Urgency matrix to assign $M_1$–$M_4$ priorities with SLA response/resolution deadlines.
- **Evidence-Gated Closure**: Strict server-side enforcement returning HTTP 422 Unprocessable Entity if ticket closure is attempted without mandatory resolution notes.
- **Sensor Events**: Deterministic IoT sensor ingestion pipeline with hash-based duplicate suppression (`source_id:event_type:time_window`) and automatic alert threshold triggering.
- **Approvals**: Multi-tier authorization workflow for restricted research laboratories and extended duration bookings.
- **Equipment Loans**: Equipment checkout and loan request tracking linked to campus facilities.
- **Integrations**: Durable transactional outbox pattern for external DevOps issue trackers using stable idempotency keys and retry reconciliation.
- **Concurrency Controls**: Version-based Optimistic Concurrency Control (OCC) for maintenance tickets returning HTTP 409 Conflict on stale updates.
- **Frontend SPA**: Responsive Vue 3 + Vite application featuring interactive Persona Switcher (Student, Faculty, Manager, Technician, Approver, Admin), live booking calendar, triage rationales, sensor simulator, and audit log.
- **Automated Tests**: Comprehensive 14-test automated test suite across unit, API, and concurrency dimensions.
- **Deployment**: Multi-tier Docker Compose deployment with PostgreSQL 16 (persistent named volume `postgres_data`), stateless Django backend, and Nginx frontend reverse proxy.
- **Deliberate Merge Conflict**: Successfully demonstrated and resolved merge conflict in `backend/config/policies.py` reconciling standard (4h) vs extended (8h) reservation policies.

### Changed
- Switched default reservation duration policy to 4 hours with department approval required for extensions up to 8 hours.
- Transitioned booking overlap validation from inclusive timestamp queries to standardized half-open interval boundaries.

### Fixed
- Fixed SQLite multi-threaded table locking anomaly during concurrent reservation stress tests by implementing engine-specific row locking and exception isolation.
- Fixed boundary condition collision where back-to-back bookings sharing start/end boundaries were incorrectly rejected.
- Fixed missing priority field in serialized ticket triage response payload.
