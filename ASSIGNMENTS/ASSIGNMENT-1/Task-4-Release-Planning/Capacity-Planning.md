# Task 4: Capacity Planning and Velocity Model

## 1. Capacity Model Foundations

In greenfield software development where no historical velocity exists, Agile teams must not confuse nominal working hours with delivery commitments. The team uses an explicit capacity envelope based on available engineering time while maintaining story points as strictly relative estimates of complexity and uncertainty.

### 1.1 Mathematical Formulation of Capacity
- **Team Size ($N$):** 7 cross-functional engineers.
- **Sprint Duration ($D$):** 10 working days (2 calendar weeks).
- **Daily Focused Availability ($H$):** 6 focused engineering hours per developer (excluding administrative overhead, enterprise emails, and personal breaks).

$$\text{Nominal Sprint Capacity} = N \times D \times H = 7 \times 10 \times 6 = 420 \text{ nominal hours}$$

### 1.2 The Operational Reserve (The 20% Rule)
Empirical software engineering demonstrates that dedicating 100% of nominal hours to feature coding leads to severe burnout, testing shortcuts, and unmanaged defects. An explicit **20% operational reserve** (84 hours) is set aside:
- **Sprint Ceremonies:** Planning (2h), Review (1h), Retrospective (1h), Daily Standups (2.5h) = ~6.5 hours/person.
- **Stakeholder Window:** 90 minutes per week (3 hours/person per sprint) for refinement and demos.
- **Peer Code Reviews:** ~1.5 hours per developer per week.
- **Unplanned Defect Triaging & Environment Maintenance:** Remaining buffer.

$$\text{Net Focused Engineering Capacity} = 420 \times (1 - 0.20) = \mathbf{336 \text{ focused hours}}$$

---

## 2. Decoupling Story Points from Hours

> **Critical Agile Principle:** Story points **MUST NOT** be equated to fixed hours (e.g., "1 point = 21 hours").

### Why Point-to-Hour Equivalence is Rejected:
1. **Non-Linear Cognitive Complexity:** Writing 50 lines of complex concurrency locking code (Story S02, 5 points) may take the same number of clock hours as writing 500 lines of standard CRUD forms, but carries ten times the defect risk and cognitive load.
2. **Multi-Role Distribution:** A 5-point story involves backend coding, database migration, and QA automated testing. Converting points to hours creates false assumptions about individual developer productivity.
3. **Estimation Independence:** Story points measure relative size and uncertainty using a modified Fibonacci sequence (1, 2, 3, 5, 8). Hours measure duration.

---

## 3. Initial Velocity Ceiling and Empirical Adaptation

Because the team has no historical velocity prior to Sprint 1:
- An **initial provisional ceiling of 16 Story Points** is established for Sprint 1.
- This ceiling acts as an upper-bound governor to prevent the team from taking on excessive work in progress during the initial architectural setup.
- The actual completed story points from Sprint 1 will serve as empirical calibration data to adjust the commitments for Sprint 2, Sprint 3, and Sprint 4.
