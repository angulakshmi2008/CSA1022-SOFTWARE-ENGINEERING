# Technology Comparison and Stack Selection

## 1. Architectural Criteria for Selection
The technical stack for the Smart Campus Facility Booking and Maintenance Platform must satisfy the following core software engineering requirements:
1. **Relational Integrity & Declarative Overlap Protection:** Capability to enforce time-range non-overlap at the storage boundary under concurrent writes.
2. **Robust REST API Framework:** Standardized serialization, authentication, role-based authorization, and transparent validation error handling.
3. **Rapid, Responsive UI Development:** Clean reactivity, component reusability, and interactive calendar/dashboard rendering.
4. **Reproducible Multi-Container Delivery:** Light-weight container footprint, fast image builds, and predictable orchestration via Docker Compose.
5. **Timeline and Maintainability:** Feasible for an individual engineer to construct, test, validate, and document within a one-week sprint.

---

## 2. Comparative Evaluation of Feasible Technology Stacks

| Evaluation Dimension | Option A: Vue 3 + Django REST Framework + PostgreSQL (Selected) | Option B: Angular + Spring Boot + MySQL | Option C: React + FastAPI + PostgreSQL |
|---|---|---|---|
| **Frontend Framework** | **Vue 3 (Composition API / Vite)**<br>Lightweight, intuitive reactivity, rapid single-page component development, fast HMR build times. | **Angular (TypeScript)**<br>Full-featured enterprise framework, strict dependency injection, steep learning curve and verbose boilerplate. | **React 18**<br>Popular component ecosystem, but requires assembly of separate routing, state, and form validation libraries. |
| **Backend API Engine** | **Django 6.x + DRF (Python 3.13)**<br>Mature ORM, built-in migration system, declarative serializers, out-of-the-box admin panel, and direct support for PostgreSQL GiST exclusion constraints. | **Spring Boot 3 (Java 21)**<br>Enterprise-grade static typing and threading, but high startup latency, heavy memory footprint (~400MB+ per container), and verbose JPA annotations. | **FastAPI + SQLAlchemy 2.0 (Python)**<br>High async throughput and auto-generated OpenAPI docs, but requires assembling custom auth, migration, and admin tooling manually. |
| **Database & Concurrency** | **PostgreSQL 16**<br>Native `tstzrange` range types and `btree_gist` exclusion constraints allowing declarative, 100% database-enforced booking non-overlap (`EXCLUDE USING gist`). | **MySQL 8.0**<br>Lacks native range exclusion constraints; preventing booking overlap requires pessimistic table locking (`SELECT ... FOR UPDATE`) or application-level mutexes vulnerable to multi-instance races. | **PostgreSQL 16**<br>Full support for range types and exclusion constraints, matching Option A at the database layer. |
| **Container & Resource Footprint** | **Low to Moderate (~300MB RAM total)**<br>Alpine-based images, rapid container boot time (<5 seconds), ideal for multi-replica Docker Compose scaling on workstation hardware. | **Heavy (~1.2GB+ RAM total)**<br>JVM heap allocation, longer build times, and high container overhead. | **Low (~280MB RAM total)**<br>Lightweight async Python runtime and Node/Nginx static distribution. |
| **Development Velocity & Testing** | **Extremely High**<br>Unified pytest test suite, standard fixture factories, rapid migration commands, and clear REST serialization. | **Moderate**<br>Lengthy Maven/Gradle compilation phases slow down iterative test-driven development. | **Moderate**<br>FastAPI requires manual wiring of migration tooling (Alembic) and custom permission decorators. |

---

## 3. Justification of Final Technology Selection

### Primary Stack: Vue 3 + Django REST Framework + PostgreSQL + Docker Compose
1. **PostgreSQL as the Decisive Concurrency Arbiter:**
   Under Task 6, two backend replicas process concurrent reservation requests simultaneously. Application-level check-then-insert code inevitably suffers from time-of-check to time-of-use (TOCTOU) race conditions. PostgreSQL natively solves this via generalized search tree (`GiST`) exclusion constraints:
   ```sql
   ALTER TABLE bookings ADD CONSTRAINT booking_no_active_overlap
   EXCLUDE USING gist (
     facility_id WITH =,
     tstzrange(start_at, end_at, '[)') WITH &&
   ) WHERE (status IN ('approved', 'confirmed', 'in_use'));
   ```
   Neither MySQL nor standard SQLite can enforce this declaratively without distributed locking or severe serial isolation penalties.

2. **Django REST Framework for Server-Enforced RBAC:**
   DRF provides an battle-tested authorization layer where permission classes (`BasePermission`) inspect authenticated user credentials on every request, guaranteeing that role boundaries cannot be bypassed by modified HTTP client headers.

3. **Vue 3 for Modular User Interfaces:**
   Vue 3’s reactive system and component structure allow building an interactive operations dashboard, facility availability calendar, and telemetry console without the excessive ceremony of Angular or the fragmented package sprawl of React.

4. **Docker Compose for Transparent Multi-Service Deployment:**
   Compose provides declarative service networking, persistent named volumes, healthcheck-driven dependency ordering, and zero-downtime scaling (`--scale backend=2`), satisfying the deployment criteria without the cluster complexity of Kubernetes.
