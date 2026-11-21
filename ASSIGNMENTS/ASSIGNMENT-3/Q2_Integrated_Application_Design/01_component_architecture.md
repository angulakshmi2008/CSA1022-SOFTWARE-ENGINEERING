# Integrated Application Component Architecture

## 1. Architectural Style and Topology
The Smart Campus Facility Booking and Maintenance Platform adopts a clean, modular, layered architecture designed for stateless multi-replica horizontal scaling. The system separates user interface concerns, authoritative business and security domain logic, transactional relational persistence, and asynchronous external system integrations.

```mermaid
graph TD
    subgraph ClientLayer ["Client & Interface Layer"]
        UI["Vue 3 Single Page Application<br/>(Student, Faculty, Manager, Tech, Approver Views)"]
        SensorClient["IoT Telemetry Simulation Client<br/>(Automated Sensor Emitter)"]
    end

    subgraph IngressLayer ["Ingress & Reverse Proxy Layer"]
        Proxy["Nginx Load Balancer / Reverse Proxy<br/>(Port 80/3000 -> /api Round-Robin)"]
    end

    subgraph ApplicationLayer ["Application & Domain Logic Layer (Stateless)"]
        subgraph BackendReplica1 ["Django REST API - Instance 1 (Port 8001)"]
            Auth1["Authentication & RBAC Engine"]
            BookingMod1["Booking & Calendar Module"]
            MaintMod1["Maintenance & Explainable Triage"]
            SensorMod1["Sensor Telemetry Intake"]
            ApprovalMod1["Approvals & Governance"]
            AuditMod1["Transactional Audit Logger"]
        end
        subgraph BackendReplica2 ["Django REST API - Instance 2 (Port 8002)"]
            Auth2["Authentication & RBAC Engine"]
            BookingMod2["Booking & Calendar Module"]
            MaintMod2["Maintenance & Explainable Triage"]
            SensorMod2["Sensor Telemetry Intake"]
            ApprovalMod2["Approvals & Governance"]
            AuditMod2["Transactional Audit Logger"]
        end
    end

    subgraph PersistenceLayer ["Shared Transactional Persistence Layer"]
        DB[("PostgreSQL 16 Database Engine<br/>- B-Tree & GiST Range Exclusion Constraints<br/>- Unique Telemetry & Idempotency Keys<br/>- ACID Transactions & Version Locks<br/>- Named Persistent Storage Volume")]
    end

    subgraph BackgroundLayer ["Asynchronous Integration Layer"]
        Worker["Durable Integration Worker<br/>(Outbox Intent Dispatcher)"]
        ExternalTracker["External Developer Issue Tracker /<br/>DevOps Platform API"]
    end

    UI -->|HTTP / REST| Proxy
    SensorClient -->|POST /api/sensor-events/| Proxy
    Proxy -->|Load Balanced| BackendReplica1
    Proxy -->|Load Balanced| BackendReplica2

    BackendReplica1 -->|Shared Relational State| DB
    BackendReplica2 -->|Shared Relational State| DB

    DB -->|Polls Durable Integration Intents| Worker
    Worker -->|HTTPS REST with Reconcile| ExternalTracker
    Worker -->|Updates Intent Status| DB
```

---

## 2. Component Descriptions

### 2.1 Vue 3 User Interface
- **Role & Responsibilities:** Provides responsive, accessible views for all six user personas. Renders the operations dashboard, availability calendar, maintenance queue, explainable triage details, and inspection modals.
- **Security Boundary:** Untrusted presentation layer. Performs client-side format guidance and form validations to enhance user experience, but relies entirely on backend APIs for security, access enforcement, and state authorization.

### 2.2 Nginx Ingress & Load Balancer
- **Role & Responsibilities:** Acts as the reverse proxy gateway, terminating external HTTP requests and distributing traffic across the two backend instances (`backend-1:8000` and `backend-2:8000`) using round-robin scheduling.
- **Failover Handling:** Configured with active health checks to detect unhealthy backend instances and route traffic exclusively to surviving replicas during maintenance or crashes.

### 2.3 Django REST Framework Backend Service (Stateless Replicas)
- **Role & Responsibilities:** The authoritative security and business logic boundary:
  - Validates authentication tokens/sessions.
  - Enforces RBAC permissions per endpoint and role.
  - Executes the deterministic explainable triage engine.
  - Implements optimistic concurrency checks (`expected_version`).
  - Employs atomic database transactions to ensure state transitions and audit logs commit together.
- **Statelessness:** Stores no session state, in-memory locks, or uncommitted work items in local process RAM, ensuring that any request can be fulfilled by any backend replica.

### 2.4 PostgreSQL Persistence Engine
- **Role & Responsibilities:** The definitive source of truth across all campus data:
  - Enforces relational referential integrity via foreign key cascades.
  - Prevents booking overlaps using generalized search tree (`GiST`) exclusion constraints (`booking_no_active_overlap`).
  - Enforces telemetry uniqueness on `(source_id, event_id)`.
  - Maintains persistent transactional isolation (Read Committed / Serializable where required).

### 2.5 Durable Integration Worker (Outbox Pattern)
- **Role & Responsibilities:** Asynchronously inspects pending `IntegrationIntent` records created during ticket triage or approval workflows, communicating with external developer issue trackers (e.g., GitHub Issues / Jira) via durable correlation keys to prevent duplicate ticket generation across network timeouts.
