# Question 4: Git Workflow Specification & Contribution Attribution

## 1. Branching Strategy & Architecture

The repository adheres to a disciplined, trunk-based Git workflow augmented with short-lived feature branches, structured around conventional commits and pull-request verification cycles.

### 1.1 Branch Hierarchy
- **`main`**: The single production-ready baseline branch. Protected against direct unverified commits. Contains only release-tagged, tested, and reviewed code.
- **`feature/booking-workflow`**: Implements the facility catalogue, reservation lifecycle, interval overlap validation, and university standard operating policies for reservation duration.
- **`feature/concurrency-hardening`**: Implements database-level range exclusion constraints, optimistic concurrency version control on maintenance tickets (`version` / `expected_version`), deterministic sensor deduplication keys, and transactional outbox patterns for external DevOps issue trackers.

```
       [commit: initial core setup]
                 │
                 ├─── feature/booking-workflow ──────────┐
                 │    (duration=4h, booking serializer)  │ (Deliberate Merge Conflict)
                 │                                       ▼
                 │                                [merge: resolved to 4h] ──> v1.0.0
                 │                                       ▲
                 └─── feature/concurrency-hardening ─────┘
                      (duration=8h proposal, range checks)
```

---

## 2. Conventional Commit Standards

Every commit adheres to the Conventional Commits v1.0.0 specification with explicit scope definitions:

| Prefix | Scope | Description |
| :--- | :--- | :--- |
| `feat` | `(facilities)` | Facility catalogue, campus association, and filtering |
| `feat` | `(bookings)` | Half-open reservation intervals, calendar availability, and overlap check |
| `feat` | `(maintenance)` | Ticket lifecycle, 3x3 Impact-Urgency triage, and resolution notes gating |
| `feat` | `(sensor)` | IoT event intake, threshold analysis, and duplicate suppression |
| `feat` | `(integrations)` | Durable outbox pattern, external issue creation, idempotency keys |
| `fix` | `(concurrency)` | Optimistic locking checks (HTTP 409) and row locking |
| `test` | `(api)` | Automated pytest suite for REST endpoints and edge cases |
| `test` | `(concurrency)` | Concurrent overlapping reservation and conflicting ticket test harness |
| `chore` | `(deploy)` | Dockerfile, Docker Compose, Nginx load balancer configuration |
| `docs` | `(architecture)` | Architecture specifications, API schemas, and technical reflection |

---

## 3. Contribution Attribution & Academic Integrity

As an individual software engineering capstone assignment completed by:
- **Author**: ANGULAKSHMI S
- **Register Number**: 192524402
- **Course**: CSA1022 - Software Engineering

All design, architectural decisions, code implementation, test suites, container definitions, and documentation are the sole, verified work of the author.

To rigorously demonstrate real-world team engineering practices, multi-role development dynamics were simulated using distinct, isolated feature branches (`feature/booking-workflow` representing the Facility Services engineering team and `feature/concurrency-hardening` representing the Platform Infrastructure team). Pull request reviews, code analysis, and merge conflicts were systematically executed and recorded without falsely claiming external human review.

---

## 4. Key Conventional Commits Log

The following key commits form the spine of the implementation:

1. `feat(core): initialize Django project structure with custom User and RBAC roles`
2. `feat(campuses): add multi-campus data model for 6 university campus locations`
3. `feat(facilities): implement facility catalogue and equipment loan request models`
4. `feat(bookings): implement booking availability engine with half-open intervals`
5. `feat(maintenance): add explainable triage matrix and evidence-gated ticket closure`
6. `feat(sensor): add deterministic event deduplication and threshold alerts`
7. `feat(integrations): implement transactional outbox pattern for DevOps tracking`
8. `fix(concurrency): add optimistic version locking (HTTP 409) and GiST exclusion logic`
9. `feat(frontend): build responsive Vue 3 SPA with persona switcher and triage explainability`
10. `test(suite): create comprehensive pytest suite for RBAC, workflows, and concurrency`
11. `chore(deploy): build multi-stage Dockerfiles and Docker Compose configuration`
12. `chore(release): resolve deliberate merge conflict and tag v1.0.0 release`
