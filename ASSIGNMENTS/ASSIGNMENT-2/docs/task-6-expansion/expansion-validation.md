# Task 6: Part C – Validation of the Redesigned Architecture

To evaluate the redesigned architecture under expanded multi-regional scale, edge scanner buffering, and partial failure conditions, four dedicated validation scenarios were constructed and executed:
- **Scenario T8:** Replayed Scanner Burst Deduplication (Edge Node Synchronization)
- **Scenario T9:** Regional Policy Versioning and Immutability During Live Operations
- **Scenario T10:** System Health, Reporting Read Model Decoupling, and Multi-Regional Resilience
- **Scenario T11:** Offline Queued Refund Approval Governance and Privilege Enforcement

---

## 1. Scenario Specifications and Empirical Verification

### Scenario T8: Replayed Scanner Burst Deduplication
- **Objective:** Verify that an edge scanner replaying a batch of buffered events (due to network re-transmission) applies each unique inventory movement exactly once.
- **Test Setup:** Handheld terminal `SCANNER-WH-A1` transmits a batch of 10 events: 5 unique events (`scan-evt-000` to `scan-evt-004`), each duplicated once within the same transmission payload. Target SKU is `SKU-PHONE-002` in `US-EAST` (initial `on_hand = 50`).
- **Expected Specification Result:** The server ingests all 10 events, successfully processes 5, identifies 5 as duplicates (`duplicate_count = 5`), and increments `on_hand` by exactly 50 units (final stock = 100).
- **Empirical Execution Result:**
  ```text
  Test Script: tests/test_t8_scanner_deduplication.py
  Execution Duration: 32.7 ms
  Observed Output: Received: 10, Processed: 5, Duplicates: 5, Final on_hand: 100
  Verdict: PASSED
  ```

---

### Scenario T9: Regional Policy Versioning and Historical Immutability
- **Objective:** Verify that when an administrator modifies a regional tax rate or shipping fee, existing orders retain their historical snapshot total while new orders immediately calculate totals using the new policy version.
- **Test Setup:**
  1. Customer places Order 1 in `EU-CENTRAL` under Policy Version 1 (`tax_rate = 0.19, shipping_fee = 5.00`).
  2. Administrator updates `EU-CENTRAL` policy via `PUT /api/policies/EU-CENTRAL` (`tax_rate = 0.25, shipping_fee = 10.00`), creating Policy Version 2.
  3. Customer places Order 2 in `EU-CENTRAL`.
  4. Server inspects Order 1 and Order 2 totals.
- **Expected Specification Result:** Order 1 maintains `policy_version = 1` and total $182.31. Order 2 calculates `policy_version = 2` and total $196.25. Historical calculations are not retroactively altered.
- **Empirical Execution Result:**
  ```text
  Test Script: tests/test_t9_regional_policy.py
  Execution Duration: 74.5 ms
  Observed Output: Order 1 Total: $182.31 (v1), Order 2 Total: $196.25 (v2)
  Verdict: PASSED
  ```

---

### Scenario T10: System Health, Reporting Decoupling, and Multi-Regional Resilience
- **Objective:** Verify that the platform maintains active configuration across all 12 operational regions, reporting endpoints compute cross-regional aggregates without deadlocking, and health checks return 200 OK.
- **Test Setup:** Automated query across `/health`, `/`, and `/api/reporting/summary`.
- **Expected Specification Result:** HTTP 200 OK, `status = 'HEALTHY'`, `database = 'CONNECTED'`, and `regions_supported = 12`.
- **Empirical Execution Result:**
  ```text
  Test Script: tests/test_t10_resilience.py
  Execution Duration: 0.02 ms
  Observed Output: Status: HEALTHY, Database: CONNECTED, Regions: 12
  Verdict: PASSED
  ```

---

### Scenario T11: Offline Queued Refund Approval Governance
- **Objective:** Verify that a refund decision queued offline on a warehouse scanner or client device cannot bypass server-side role validation upon reconnection.
- **Test Setup:** Customer requests a refund of $149.00 (`SKU-HEADSET-003`). An unauthorized floor picker attempts to approve the refund. A legitimate Finance Reviewer then approves the refund.
- **Expected Specification Result:** Unauthorized picker decision is rejected with HTTP 403 Forbidden; refund state strictly remains `REQUESTED (Pending)`. Legitimate Finance Reviewer decision succeeds with HTTP 200 OK and transitions state to `APPROVED`.
- **Empirical Execution Result:**
  ```text
  Test Script: tests/test_t11_offline_refund_approval.py
  Execution Duration: 94.8 ms
  Observed Output: Picker Approval: HTTP 403 Forbidden; Finance Approval: HTTP 200 OK -> State APPROVED
  Verdict: PASSED
  ```

---

## 2. Summary of Additional Validation Results

| Test ID | Operational Scenario | Expected Behavior | Observed Result | Duration | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T8** | Edge Scanner Replay Deduplication | 10 received, 5 processed, 5 duplicates ignored | 5 processed, 5 duplicates, inventory incremented exactly 50 | 32.7 ms | **PASSED** |
| **T9** | Regional Policy Versioning | Historical orders retain v1 total ($182.31); new orders use v2 ($196.25) | Order 1: $182.31 (v1); Order 2: $196.25 (v2) | 74.5 ms | **PASSED** |
| **T10**| Multi-Region Resilience | Healthy status across all 12 supported regions | Status HEALTHY, Database CONNECTED, 12 Regions | < 1 ms | **PASSED** |
| **T11**| Offline Refund Governance | Unauthorized offline decision rejected (403); validated by Finance (200) | Rejected picker (403); accepted finance reviewer (200) | 94.8 ms | **PASSED** |
