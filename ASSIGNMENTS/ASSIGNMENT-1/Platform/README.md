# Omnichannel Order Fulfilment Platform Prototype

## CSA10 – Software Engineering Assignment 1 Core Prototype

This directory contains the working software prototype demonstrating the omnichannel order fulfilment backbone required by the assignment scenario. The prototype models the complete journey from checkout and atomic stock reservation to payment verification, warehouse picking, dispatch, tracking, returns, and role-governed refund approvals.

---

## 1. Architectural Highlights

- **Domain Model:** Implements a 10-state finite state machine (`CREATED` → `RESERVED` → `PAID` → `PICKING` → `PICKED` → `DISPATCHED` → `DELIVERED` → `RETURN_REQUESTED` → `REFUND_PENDING` → `REFUNDED`).
- **Transactional Stock Reservation:** Uses SQLite row locks and atomic transactions to prevent inventory overselling and negative stock counts under high concurrency.
- **Payment Idempotency:** Implements unique idempotency keys preventing duplicate financial charges during network timeouts and retries.
- **Role-Based Access Control (RBAC):** Cryptographically signed session tokens enforcing strict role permissions (e.g., support agents cannot approve refunds; only authenticated finance reviewers can).
- **Regional Policy Engine:** Decoupled strategy pattern calculating regional taxes (12% North, 8% South, 10% West), courier shipping tables, and tiered refund thresholds across three regional warehouses.
- **Immutable Audit Trail:** Append-only audit records tracking actor, action, previous state, new state, and timestamp for all transactions.

---

## 2. Directory Layout

```
Platform/
├── src/
│   ├── models.py            # Enums, dataclasses, state machine transition tables
│   ├── database.py          # SQLite schema, transactional connection manager, seeder
│   ├── auth_service.py      # Session token generation and RBAC authorization middleware
│   ├── inventory_service.py # Atomic stock reservation, TTL expiry, and low-stock triggers
│   ├── payment_service.py   # Idempotent payment processing, local mock stub, and refunds
│   ├── policy_service.py    # Multi-regional tax, shipping, and refund threshold engine
│   ├── warehouse_service.py # Digital pick lists and barcode scanner emulation
│   ├── order_service.py     # Main business orchestration and state machine manager
│   └── cli.py               # Interactive CLI demonstration
│
├── tests/
│   ├── test_order_lifecycle.py     # MSC-01: Full 10-state transition validation
│   ├── test_concurrency_stock.py   # MSC-02: 100-thread concurrent reservation stress test
│   ├── test_payment_idempotency.py # MSC-03: 10-retry payment idempotency verification
│   ├── test_security_roles.py      # MSC-04: Role-based refund authorization checks
│   └── test_regional_policies.py   # Task 6: Multi-region tax, shipping, and return policies
│
├── test-data/
│   ├── synthetic_catalog.json # Synthetic apparel, footwear, and electronics catalogue
│   └── regional_rules.json    # Regional warehouse rules for North, South, and West
│
├── scripts/
│   ├── run_demo.py          # End-to-end interactive order-to-refund walkthrough
│   └── run_all_tests.py     # Discovers and executes the automated test suite
│
└── README.md                # Technical platform documentation
```

---

## 3. Quickstart and Execution Guide

### Prerequisites
- Python 3.10+ (tested on Python 3.13)
- Standard library only; zero external third-party dependencies required.

### 3.1 Execute the Automated Test Suite
To execute all automated unit and integration tests asserting MSC-01 through MSC-05:
```bash
python Platform/scripts/run_all_tests.py
```
*Or using Python's standard unittest runner:*
```bash
python -m unittest discover -s Platform/tests -p "test_*.py"
```

### 3.2 Run the Interactive End-to-End Demonstration
To execute the live CLI walkthrough demonstrating the complete order-to-refund flow:
```bash
python Platform/scripts/run_demo.py
```

---

## 4. Verification of Measurable Delivery Criteria

| Criterion ID | Target Requirement | Automated Test File | Result |
|---|---|---|---|
| **MSC-01** | Full 10-state order journey with audit logs | `tests/test_order_lifecycle.py` | **PASS (100%)** |
| **MSC-02** | 100 concurrent checkouts on 10 units; 0 negative stock | `tests/test_concurrency_stock.py` | **PASS (100%)** |
| **MSC-03** | 10 retries with same key -> 1 intent & 0 duplicate debits | `tests/test_payment_idempotency.py` | **PASS (100%)** |
| **MSC-04** | Role-governed refund approval; support agent blocked | `tests/test_security_roles.py` | **PASS (100%)** |
| **MSC-05** | Clean checkout build and test reproducibility | `scripts/run_all_tests.py` | **PASS (100%)** |
