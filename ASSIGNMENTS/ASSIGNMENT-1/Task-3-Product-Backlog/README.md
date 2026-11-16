# Task 3: Prioritized Product Backlog in Selected Tool

## Directory Contents

- [Epics.md](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/Task-3-Product-Backlog/Epics.md): Architectural definition of four first-release functional Epics (Order & Stock Core, Payments & Refund Governance, Warehouse Fulfilment & Tracking, Reproducible Delivery & Support) and one explicit Deferred Epic.
- [User-Stories.md](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/Task-3-Product-Backlog/User-Stories.md): Fifteen refined user stories (S01 to S13, including S03a/b and S09a/b) structured with MoSCoW priorities, relative Story Point estimates, dependencies, and assigned roles.
- [Acceptance-Criteria.md](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/Task-3-Product-Backlog/Acceptance-Criteria.md): Granular acceptance criteria for each story, detailing positive happy-paths, negative boundary cases, concurrency locks, and accessibility constraints.
- [Definition-of-Ready.md](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/Task-3-Product-Backlog/Definition-of-Ready.md): Six-point gating checklist governing backlog readiness before sprint commitment.
- [Definition-of-Done.md](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/Task-3-Product-Backlog/Definition-of-Done.md): Eight-point quality and governance contract, including detailed justifications for two competing stakeholder trade-off decisions.
- [Backlog-Import.csv](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/Task-3-Product-Backlog/Backlog-Import.csv): Standardized, import-ready CSV file formatted for direct ingestion into Atlassian Jira Software, GitHub Projects, or spreadsheet tooling.

---

## Key Artifact Highlights
1. **Total Epics:** 4 In-Scope + 1 Deferred.
2. **Total User Stories:** 15 Refined Stories (32 Must-Have, 11 Should-Have, 3 Could-Have Points = 46 Total Points).
3. **Decoupled Architecture:** Technical dependencies such as the Payment Gateway (S03) and Build Pipeline (S09) are sliced into local stubs (S03a, S09a) and external integrations (S03b, S09b) to decouple early sprint velocity from external delays.
4. **Resolved Conflicts:** Stock reservation prioritized over executive analytics; finance-controlled refunds prioritized over automated customer promotional features.
