# Task 1: Stakeholder Investigation and Conflict Resolution

## 1. Task Overview and Assessment Mapping
- **Assessed Area:** Stakeholder Needs Investigation, Conflict Resolution, System Boundary Definition
- **Course Outcome:** CO2 – Analyze software requirements to design scalable and efficient system architectures using collaborative tools and structured modeling.
- **Marks Allocated:** 5 Marks
  - Questions, stakeholder findings and evidence (2 marks)
  - Three conflicts and justified resolutions (2 marks)
  - Boundary, actors, and scope exclusions (1 mark)

## 2. Directory Structure and Deliverables
```text
docs/task-1-stakeholders/
├── README.md                          # This document
├── investigation-questions.md         # 5 targeted investigation questions covering unresolved domain dilemmas
├── simulated-findings.md              # Explicitly labelled simulated responses for all 6 user roles
├── stakeholder-analysis.md            # Comprehensive stakeholder matrix (needs, concerns, priorities)
├── conflict-resolutions.md            # 4 major conflicts with justified trade-offs and acceptance criteria
└── system-boundary-and-scope.md       # Explicit system boundary, actors, external integrations & exclusions
```

## 3. Executive Summary of Task 1 Deliverables
The omnichannel order fulfilment platform coordinates interactions across multiple stakeholder groups whose operational objectives directly conflict:
1. **Customers** desire instantaneous checkout, real-time tracking, transparent order history, and frictionless refund processing.
2. **Warehouse Pickers** demand reliable, immutable pick lists and atomic reservations to prevent physical contention or picking expired inventory.
3. **Support Agents** require comprehensive order tracking to resolve customer inquiries without viewing restricted financial data (e.g., PAN, CVV, payment tokens).
4. **Finance Reviewers** mandate strict segregation of duties, audit logging, and human approval gates for refunds exceeding defined monetary limits.
5. **Store Managers** need accurate, consolidated inventory, sales, and refund reporting across all operating regions without analytical queries degrading operational checkout latency.
6. **Administrators** govern user role assignments, system-wide regional policies, and security configurations under least-privilege principles.

Because live access to enterprise stakeholders was unavailable in this academic setting, findings are explicitly labelled as **simulated responses** based on an industry-standard process review. All conflicts are resolved through deterministic software engineering patterns rather than human assumptions.
