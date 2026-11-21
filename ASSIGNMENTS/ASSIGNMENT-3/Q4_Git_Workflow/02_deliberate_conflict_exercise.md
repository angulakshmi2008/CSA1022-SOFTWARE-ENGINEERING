# Question 4: Deliberate Merge Conflict Exercise & Resolution

## 1. Conflict Rationale & Setup

In collaborative software engineering, merge conflicts arise when two independent feature branches modify the same lines of code or alter shared configuration files with diverging business logic.

To demonstrate mastery of Git conflict detection, diff analysis, manual reconciliation, and regression testing, a deliberate merge conflict was staged in `backend/config/policies.py`.

### 1.1 Conflicting Branches and Business Justifications
1. **Branch A: `feature/booking-workflow`** (Facility Operations Team)
   - *Requirement*: Enforce standard academic scheduling limits by capping reservations at **4 hours** (`MAX_BOOKING_DURATION_HOURS = 4`) to prevent room monopolization by single research groups.
2. **Branch B: `feature/concurrency-hardening`** (Infrastructure & Event Services Team)
   - *Requirement*: Support extended campus symposiums and full-day hackathons by expanding reservation duration to **8 hours** (`MAX_BOOKING_DURATION_HOURS = 8`) while adding concurrency guards.

Both branches modified line 8 of `backend/config/policies.py` simultaneously from the base commit.

---

## 2. Merge Conflict Occurrence

When attempting to merge `feature/concurrency-hardening` into `main` after `feature/booking-workflow` had already merged, Git automatically suspended the merge and generated conflict markers:

```bash
$ git checkout main
$ git merge feature/booking-workflow
Updating 3d2f9a1..a4c10e8
Fast-forward
 backend/config/policies.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)

$ git merge feature/concurrency-hardening
Auto-merging backend/config/policies.py
CONFLICT (content): Merge conflict in backend/config/policies.py
Automatic merge failed; fix conflicts and then commit the result.
```

### 2.1 Raw Conflict Markers in `backend/config/policies.py`

```python
<<<<<<< HEAD
# Maximum permitted reservation duration in hours for standard bookings
# Policy Ref: POL-FAC-2026-01 (Approved baseline: 4 hours)
MAX_BOOKING_DURATION_HOURS = 4
=======
# Maximum permitted reservation duration in hours for extended events
# Proposal: EXP-FAC-2026-08 (Extended baseline: 8 hours)
MAX_BOOKING_DURATION_HOURS = 8
>>>>>>> feature/concurrency-hardening
```

---

## 3. Conflict Resolution Strategy

### 3.1 Architectural Analysis & Consensus
- Releasing an unconditional 8-hour reservation limit would allow regular students to monopolize prime study spaces for entire days, directly violating academic equitable-access policies (US01 / US03).
- Conversely, strictly hardcoding a 4-hour limit without escalation prevents legitimate multi-hour faculty symposiums.
- **Architectural Resolution**:
  1. Maintain `MAX_BOOKING_DURATION_HOURS = 4` as the strict default ceiling for standard, unassisted bookings.
  2. Implement an explicit policy extension mechanism whereby bookings exceeding 4 hours (up to 8 hours) automatically require **Department Approver** sign-off via the `approvals` workflow.

### 3.2 Resolved File Content (`backend/config/policies.py`)

```python
# Maximum permitted reservation duration in hours for standard bookings
# Policy Ref: POL-FAC-2026-01 (Approved baseline: 4 hours)
# Extensions up to 8 hours require Department Approver sign-off via US03 workflow.
MAX_BOOKING_DURATION_HOURS = 4
MAX_EXTENDED_BOOKING_DURATION_HOURS = 8
```

---

## 4. Verification and Final Commit

After editing the file to remove conflict markers and incorporate the resolved policy:

```bash
$ git add backend/config/policies.py
$ git commit -m "chore(release): resolve booking duration conflict between operations and event scaling

- Keep default max reservation duration at 4 hours for standard bookings
- Introduce MAX_EXTENDED_BOOKING_DURATION_HOURS = 8 requiring Department Approver sign-off
- Verified passing test suite across all 14 unit and concurrency tests"
```

### 4.1 Post-Merge Test Verification
Following the resolution, the automated pytest suite was executed to verify zero regression:
```bash
$ python -m pytest tests/ -v
============================= 14 passed in 1.84s =============================
```
All booking validation, overlap checks, and approval tests passed with 100% compliance.
