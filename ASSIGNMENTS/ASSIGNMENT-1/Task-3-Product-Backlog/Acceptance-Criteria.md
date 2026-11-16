# Task 3: Comprehensive Acceptance Criteria (Positive & Negative Test Cases)

## 1. Overview
In accordance with the Definition of Ready, every user story must feature unambiguous, verifiable acceptance criteria containing both positive (happy path) and negative/boundary scenarios.

---

## 2. Acceptance Criteria by User Story

### Story S01: Role-Based Authentication and Scoped Sessions
- **Positive AC (Happy Path):**
  - *Given* valid credentials for an existing user with role `WAREHOUSE_PICKER`, *when* submitted to `/auth/login`, *then* the system issues a signed session token containing claims for role `WAREHOUSE_PICKER` and grants access to picking routes.
- **Negative & Boundary AC:**
  - *Given* invalid passwords or non-existent usernames, *when* login is attempted, *then* the system returns HTTP 401 Unauthorized with generic message `"Invalid credentials"`.
  - *Given* an authenticated user with role `SUPPORT_AGENT`, *when* attempting to access `/finance/refund/approve`, *then* the system rejects the request with HTTP 403 Forbidden and logs a security audit event.

### Story S02: Atomic Stock Reservation with TTL Expiry
- **Positive AC (Happy Path):**
  - *Given* an item with available stock of 5 units, *when* a customer initiates checkout for 2 units, *then* available stock immediately decrements to 3, reserved stock increments to 2, and a 15-minute reservation timer is created.
- **Negative & Boundary AC:**
  - *Given* an item with available stock of 0 units, *when* checkout is attempted, *then* the reservation is rejected with `OUT_OF_STOCK` error code and inventory remains untouched.
  - *Given* an item with 1 unit in stock, *when* two concurrent checkout requests arrive simultaneously, *then* exactly one succeeds and the other receives `CONCURRENCY_CONFLICT / OUT_OF_STOCK`; available stock never becomes negative.
  - *Given* an active reservation, *when* the 15-minute TTL timer expires without payment confirmation, *then* the system automatically releases the reserved units back to available stock.

### Story S03a: Payment Request with Idempotency Key (Local Stub)
- **Positive AC (Happy Path):**
  - *Given* an order in `RESERVED` state, *when* payment is submitted with idempotency key `IDEMP-12345`, *then* the system creates a payment transaction, records the key, returns `SUCCESS`, and transitions the order to `PAID`.
- **Negative & Boundary AC:**
  - *Given* an identical request repeated 10 times with idempotency key `IDEMP-12345`, *then* the system executes the charge exactly once, returns the cached confirmation payload, and creates zero duplicate payment intents.
  - *Given* a simulated payment gateway network timeout, *when* the request fails, *then* the order transitions to `PAYMENT_PENDING` and inventory reservation remains held until the retry window closes.

### Story S03b: External Gateway Sandbox Integration
- **Positive AC (Happy Path):**
  - *Given* valid sandbox credentials in Week 4, *when* a charge request is routed to the sandbox endpoint, *then* the system processes real sandbox responses (`APPROVED`, `DECLINED`) and updates order status.
- **Negative & Boundary AC:**
  - *Given* sandbox gateway error 504 Gateway Timeout, *when* handled by the retry handler, *then* exponential backoff is triggered (1s, 2s, 4s) up to 3 retries before marking as failed.
  - *Security Boundary:* Payment secret keys and API tokens must reside strictly in server-side environment variables and must never be exposed in client bundles or log outputs.

### Story S04: Warehouse Digital Pick List Generation
- **Positive AC (Happy Path):**
  - *Given* three orders in the database (`O1: PAID`, `O2: RESERVED`, `O3: CANCELLED`), *when* the warehouse picker loads the picking dashboard, *then* only items for `O1 (PAID)` are displayed.
- **Negative & Boundary AC:**
  - *Given* an unpaid order (`RESERVED`), *when* the picker queries the pick list, *then* the order is excluded to prevent premature physical item picking.
  - *Given* pickers assigned to Warehouse North, *then* items located in Warehouse South are filtered out.

### Story S05: Order Fulfillment State Machine Transitions
- **Positive AC (Happy Path):**
  - *Given* an order in state `PAID`, *when* a warehouse worker claims it, status transitions to `PICKING`; when pick is complete, status transitions to `PICKED`; when handed to courier, transitions to `DISPATCHED`.
- **Negative & Boundary AC:**
  - *Given* an order in state `RESERVED` (unpaid), *when* an attempt is made to transition directly to `DISPATCHED`, *then* the state machine rejects the transition with `InvalidStateTransitionError` and logs an audit failure.
  - *Given* an order in `DELIVERED` state, *when* an attempt is made to transition back to `PICKING`, *then* the transition is rejected.

### Story S06: Screen-Reader Accessible Milestone Tracking
- **Positive AC (Happy Path):**
  - *Given* an authenticated customer viewing their order, *when* accessing `/orders/{id}/tracking`, *then* the page renders permitted visual milestones: `Order Placed` → `Payment Confirmed` → `Picked` → `Dispatched` → `Delivered`.
- **Negative & Boundary AC:**
  - *Accessibility Boundary:* All milestone icons must possess explicit `aria-label` tags (e.g., `aria-label="Current status: Dispatched"`), and the page must be 100% navigable using Tab and Shift+Tab keyboard shortcuts.
  - *Privacy Boundary:* Warehouse worker names, internal bin numbers, and private dispute comments must be stripped from the public API payload.

### Story S07: Customer Return Request Initiation
- **Positive AC (Happy Path):**
  - *Given* an order in `DELIVERED` state 5 days ago, *when* the customer submits a return request with reason `"Damaged item"`, *then* the status transitions to `RETURN_REQUESTED`.
- **Negative & Boundary AC:**
  - *Given* an order delivered 20 days ago (exceeding the 14-day policy limit), *when* a return is submitted, *then* the system rejects the request with `"Return window expired"`.
  - *Given* User A, *when* attempting to submit a return for User B's order ID, *then* the system returns HTTP 403 Forbidden.

### Story S08: Role-Controlled Refund Authorization
- **Positive AC (Happy Path):**
  - *Given* an order in `RETURN_REQUESTED` state with refund value \$45.00, *when* an authenticated `FINANCE_REVIEWER` approves the refund, *then* the status transitions to `REFUNDED`, the payment adapter executes refund reversal, and an immutable audit log is created.
- **Negative & Boundary AC:**
  - *Given* a `SUPPORT_AGENT` attempting to approve a refund, *when* submitted, *then* the API throws `AuthorizationError: Role SUPPORT_AGENT lacks REFUND_APPROVAL permission`.
  - *Given* a refund request of \$600.00, *when* a standard finance reviewer has a single-transaction limit of \$500.00, *then* the system flags the transaction as requiring `DUAL_FINANCE_AUTHORIZATION`.

### Story S09a: Local Build and Smoke Test Automation
- **Positive AC (Happy Path):**
  - *Given* a clean repository checkout, *when* executing `python -m unittest discover`, *then* 100% of unit and integration tests execute successfully with zero failures and exit code 0.
- **Negative & Boundary AC:**
  - *Given* a missing mandatory configuration file or corrupt SQLite schema, *when* tests run, *then* the build fails loudly with descriptive error messages.

### Story S09b: CI/CD Pipeline Enforcement
- **Positive AC (Happy Path):**
  - *Given* a pull request opened against `main`, *when* automated checks pass, *then* the pull request is marked eligible for merge.
- **Negative & Boundary AC:**
  - *Given* a failing unit test or security lint vulnerability, *when* CI runs, *then* merge capability is blocked.

### Story S10: Support Order Lookup Console
- **Positive AC (Happy Path):**
  - *Given* an authenticated `SUPPORT_AGENT`, *when* searching by email `customer@example.com`, *then* the console displays all matching orders, current state, courier tracking URL, and return notes.
- **Negative & Boundary AC:**
  - *Given* a support agent searching for an order, *then* customer credit card tokens and hashed passwords remain masked.

### Story S11: Deterministic Low-Stock Alerts
- **Positive AC (Happy Path):**
  - *Given* safety stock threshold set to 3 units, *when* stock decrements from 4 to 2, *then* a low-stock alert is generated for the store manager.
- **Negative & Boundary AC:**
  - *Given* stock already at 2 units, *when* another item is reserved, *then* duplicate alert spam is suppressed.

### Story S12: Barcode Scanner Verification (Emulated / Hardware)
- **Positive AC (Happy Path):**
  - *Given* a pick item with barcode `"8901234567890"`, *when* scanned via the test device, *then* the UI visually flags the line item as `VERIFIED`.
- **Negative & Boundary AC:**
  - *Given* a scanned barcode `"9999999999999"`, *when* submitted, *then* the system rejects it with an audible/visual `MISMATCH_ITEM_REJECTED` warning.

### Story S13: Sales Analytics Reconciliation (Deferred)
- **Positive AC (Happy Path):**
  - *Given* 50 completed orders totaling \$2,500.00, *when* the executive summary is generated, *then* displayed revenue reconciles exactly with transaction ledgers.
- **Boundary AC:**
  - Unpaid or cancelled orders must not be included in gross sales totals.
