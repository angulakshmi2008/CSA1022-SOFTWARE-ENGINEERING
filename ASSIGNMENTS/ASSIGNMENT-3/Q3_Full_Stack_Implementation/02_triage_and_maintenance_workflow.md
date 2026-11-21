# Explainable Maintenance Triage & Evidence-Gated Lifecycle

## 1. Deterministic and Explainable Triage
The platform avoids opaque or hallucinatory black-box AI by implementing a transparent, deterministic rule-based triage engine (`backend/maintenance/triage_engine.py`).

### 1.1 Category Classification via Domain Keywords
The system scans reported incident titles and descriptions against an approved campus taxonomy:
- **HVAC:** `ac`, `air-conditioning`, `chiller`, `temperature`, `overheat`, `fan`, `cooling`, `ventilation`, `thermostat`
- **Plumbing:** `leak`, `pipe`, `water`, `flood`, `drain`, `faucet`, `toilet`, `overflow`, `sewage`
- **Electrical:** `spark`, `power`, `electrical`, `breaker`, `blackout`, `wiring`, `fuse`, `outlet`, `short-circuit`, `voltage`
- **Network:** `wifi`, `network`, `ethernet`, `router`, `switch`, `internet`, `connectivity`, `latency`, `gateway`
- **Structural:** `door`, `window`, `lock`, `ceiling`, `wall`, `crack`, `glass`, `hinge`, `roof`

### 1.2 Priority Assessment Matrix
Priority is computed using the university-approved $3 \times 3$ Impact $\times$ Urgency matrix:

| Teaching / Operational Impact | High Urgency (Immediate Disruption) | Medium Urgency | Low Urgency |
|---|---|---|---|
| **High Impact** | **M1 – Critical** (2h SLA) | **M2 – High** (4h SLA) | **M3 – Medium** (8h SLA) |
| **Medium Impact** | **M2 – High** (4h SLA) | **M3 – Medium** (8h SLA) | **M4 – Low** (24h SLA) |
| **Low Impact** | **M3 – Medium** (8h SLA) | **M4 – Low** (24h SLA) | **M4 – Low** (24h SLA) |

### 1.3 Generated Explainability Record
Each triaged ticket stores a detailed explainability rationale visible to facility managers:
```text
[Explainable Triage Engine]
1. Categorization: Matched keyword(s) ['chiller', 'temperature'] mapping to category 'hvac'.
2. Priority Assessment: Impact='HIGH' and Urgency='HIGH' evaluate via matrix to Priority M1.
3. SLA Target: Assigned resolution deadline of 120 minutes (2.0 hours).
```

---

## 2. Evidence-Gated Maintenance Lifecycle Workflow

```mermaid
sequenceDiagram
    autonumber
    actor Sensor as IoT Sensor Client
    actor Manager as Facility Manager
    actor Tech as Maintenance Technician
    actor Approver as Dept Approver
    participant API as Django REST API
    participant DB as PostgreSQL Database
    participant Worker as Durable Outbox Worker

    Sensor->>API: POST /api/sensor-events/ (temp=31.2°C)
    API->>DB: Check (source_id, event_id) -> New
    API->>API: Execute Triage -> HVAC, M1 Critical (2h)
    API->>DB: INSERT Ticket #1 & SensorEvent in transaction
    API-->>Sensor: 201 Created (Ticket #1 spawned)

    Manager->>API: PATCH /api/tickets/1/assign/ (assignee=Rajesh)
    API->>DB: Update status='assigned', version=2, log audit
    API-->>Manager: 200 OK

    Tech->>API: PATCH /api/tickets/1/state/ (target='in_progress', expected_version=2)
    API->>DB: Update status='in_progress', version=3
    API-->>Tech: 200 OK

    Tech->>API: POST /api/tickets/1/inspections/ (diagnostics notes)
    API->>DB: INSERT InspectionComment

    opt Restricted Hardware Change
        Tech->>API: PATCH /api/tickets/1/state/ (target='pending_approval')
        Approver->>API: POST /api/approvals/ (decision='approved', reason='validated')
        API->>DB: Transition status='in_progress', log audit
    end

    Note over Tech,API: Step 6: Negative Case Validation (Closure without notes)
    Tech->>API: PATCH /api/tickets/1/state/ (target='resolved', notes='')
    API-->>Tech: 422 Unprocessable Entity (resolution_notes required)

    Tech->>API: PATCH /api/tickets/1/state/ (target='resolved', notes='Replaced thermal valve')
    API->>DB: Update status='resolved', version=4
    API-->>Tech: 200 OK

    Manager->>API: PATCH /api/tickets/1/state/ (target='closed', expected_version=4)
    API->>DB: Update status='closed', version=5, log closure audit
    API-->>Manager: 200 OK (Verified & Closed)

    API->>DB: INSERT IntegrationIntent (sync external issue)
    Worker->>DB: Polls pending intent
    Worker->>API: Reconciles correlation key -> confirmed
```
