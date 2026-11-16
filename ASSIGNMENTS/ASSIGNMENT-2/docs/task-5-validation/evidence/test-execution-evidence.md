# Task 5 & Task 6: Automated Test Execution Evidence Log

- **Execution Timestamp (UTC):** 2026-11-14 15:58:09
- **Total Scenarios Executed:** 11
- **Total Passing:** 11
- **Execution Duration:** 0.78 s
- **Execution Environment:** Python 3.13 / FastAPI Test Harness (SQLite ACID In-Memory/Disk)

| Scenario ID | Description | Expected Specification Result | Observed Empirical Evidence | Duration | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1_STOCK_CONTENTION** | Two buyers competing for the last unit | One 201 Created, one 409 Conflict, available stock == 0 | HTTP 201 and 409, available stock == 0 | 72.44 ms | **PASSED** |
| **T2_DUPLICATE_CALLBACK** | Repeated concurrent payment callback (10 deliveries) | 1 confirmation, 9 duplicate acknowledgements, 1 payment record, 1 outbox intent | 1 confirmed, 9 duplicates, 1 DB row, 1 outbox intent | 91.2 ms | **PASSED** |
| **T3_REFUND_FAILURE_RETRY** | Approved refund failing at gateway followed by controlled retry | Transitions REQUESTED -> APPROVED -> FAILED (approval retained) -> EXECUTED | Final state: EXECUTED, approved_by retained: user-t3-finance | 85.04 ms | **PASSED** |
| **T4_DISPATCH_GUARDS** | Dispatch attempt without payment or pick confirmation | HTTP 400 on PLACED, HTTP 400 on PAID, HTTP 200 on PACKED | Rejected PLACED (400), rejected PAID (400), allowed PACKED (200) | 90.79 ms | **PASSED** |
| **T5_COURIER_RETRY** | Courier synchronization request timeout and idempotent retry | Run 1 fails (attempts=1, status=PENDING), Run 2 succeeds (attempts=2, status=COMPLETED) | Run 1 failed as expected; Run 2 completed with tracking number TRK-95EB90A7 | 53.67 ms | **PASSED** |
| **T6_SECURITY_RBAC** | Unauthorized refund approval and cross-customer order access rejection | HTTP 403 on cross-customer read, HTTP 403 on customer approval, HTTP 403 on support approval, HTTP 200 on finance approval | Rejected cross-read (403), rejected customer approve (403), rejected support approve (403), allowed finance approve (200) | 109.26 ms | **PASSED** |
| **T7_LATE_PAYMENT_EXPIRY** | Late payment callback after reservation expiry and inventory resale | Order marked NEEDS_REFUND; automatic refund request created; zero stock oversold | Order state: NEEDS_REFUND, refund request created with state REQUESTED | 77.91 ms | **PASSED** |
| **T8_SCANNER_DEDUPLICATION** | Replayed scan burst after reconnect deduplicated by (node_id, event_id) | 10 received, 5 processed, 5 duplicates ignored, stock updated by 50 | Processed 5, Duplicates 5, final stock 100 | 32.04 ms | **PASSED** |
| **T9_REGIONAL_POLICY** | Regional policy changes during operation and historical snapshot preservation | Order 1 retains v1 total ($182.31); Order 2 calculates v2 total ($196.25) | Order 1 total: $182.31 (v1), Order 2 total: $196.25 (v2) | 72.27 ms | **PASSED** |
| **T10_RESILIENCE** | System health, API resilience, and 12-region database connectivity | HTTP 200, status HEALTHY, database CONNECTED, regions_supported == 12 | Status: HEALTHY, Database: CONNECTED, Regions: 12 | 0.01 ms | **PASSED** |
| **T11_OFFLINE_REFUND_APPROVAL** | Offline queued refund approval remains Pending until authenticated server validation | Unauthenticated or unprivileged attempt rejected with HTTP 403; remains REQUESTED until Finance approval | Rejected unauthorized decision (403), validated server approval (200) | 96.37 ms | **PASSED** |


## Verification Prompts & Invariant Assertions
1. **Invariant 1 (Unique Payment Identity):** Verified in `T2`—10 duplicate deliveries resulted in exactly 1 payment record and 1 outbox intent.
2. **Invariant 2 (Dual-Control Refund Approval):** Verified in `T3`, `T6`, and `T11`—unauthorized approval rejected with HTTP 403; failed execution retained approval for safe retry.
3. **Invariant 3 (Non-Negative Available Stock):** Verified in `T1` and `T7`—available stock strictly checked; never fell below zero under concurrent race conditions.
4. **Invariant 4 (Customer Isolation & Least Privilege):** Verified in `T6`—Customer B accessing Customer A's order blocked with HTTP 403.
5. **Invariant 5 (Outbox Resilient Retry):** Verified in `T5`—courier timeout retained pending intent, reconciled by correlation key, and completed on retry.
