# Task 3: Identified Modeling Inconsistencies and Documented Corrections

During the iterative process of connecting use-case interactions, domain classes, sequence messages, and state machines, four significant architectural inconsistencies were uncovered. Below is the technical diagnosis, associated enterprise risk, and the implemented engineering correction for each.

---

### Inconsistency 1: Treating Client Browser Payment-Success Redirect as Payment Confirmation
- **Original Flawed Modeling:** The initial draft sequence diagram depicted the client browser returning from the payment gateway hosted checkout page (`/checkout/success?status=paid`) and directly invoking `POST /api/orders/{id}/confirm-payment`, causing the server to mark the order `PAID` and release items to warehouse picking.
- **Identified Failure Mode & Risk:** The browser client is an untrusted entity operating outside the enterprise trust boundary. A malicious user or automated script can forge a GET/POST request to the return URL with simulated success parameters without ever authorizing a credit card transaction. Furthermore, network drops could cause the user's browser to close before the redirect completes, leaving a legitimately paid order stranded in `PLACED` state.
- **Architectural Correction:** 
  The sequence model and state machine were revised to establish a strict separation between client presentation redirects and backend transactional confirmation. The order is transitioned to `PAID` **exclusively** upon receipt of an asynchronous, cryptographically signed server-to-server webhook callback from the payment gateway to `/api/payments/callback`. The webhook handler verifies the HMAC-SHA256 signature using a pre-shared secret and confirms that the captured amount matches the exact order total. The browser redirect is treated strictly as an informational UI transition that polls the order status until the authoritative webhook commits.

---

### Inconsistency 2: Treating Client UI Role Selector Dropdowns as Authorization
- **Original Flawed Modeling:** Early frontend wireframes and draft use-case specifications permitted users to toggle their operational persona via a top-bar dropdown (e.g., switching from "Customer" to "Support Agent" or "Finance Reviewer") to access restricted administrative and refund screens.
- **Identified Failure Mode & Risk:** Treating a UI element as an authorization boundary violates fundamental secure design principles. Any user using browser developer tools, Postman, or `curl` can forge HTTP requests with arbitrary headers or payloads, granting themselves unearned privileges to view private customer data or approve financial refunds.
- **Architectural Correction:**
  Authorization was shifted entirely to **stateless server-side verification**. The domain model was updated to bind roles to the authenticated principal's cryptographically signed JSON Web Token (JWT), backed by database-persisted `user_roles`. Every protected FastAPI endpoint incorporates dependency-injected security guards (`Depends(require_role([UserRole.FINANCE_REVIEWER]))`). Client-side UI toggles serve only as cosmetic view filters for users who legitimately possess multiple server-validated roles; attempting to invoke an unauthorized endpoint returns HTTP 403 Forbidden regardless of client UI configuration.

---

### Inconsistency 3: Naive Order Confirmation Following Reservation Expiry (Late Payment Race)
- **Original Flawed Modeling:** The initial order state machine permitted a direct transition from `PLACED` to `PAID` whenever a valid callback arrived, without checking whether the 15-minute stock reservation lease had already expired.
- **Identified Failure Mode & Risk:** If a customer placed an order, delayed payment for 25 minutes, and then completed authorization, the background worker would have already marked the original reservation as `EXPIRED` and released the inventory back to the available pool. If a second buyer subsequently purchased and reserved that same physical unit, a naive payment callback for the first order would mark it `PAID`, resulting in two confirmed orders for a single physical item (overselling).
- **Architectural Correction:**
  The callback sequence and order state machine were revised to incorporate a **re-reservation and reconciliation branch**. When a payment callback arrives for an order whose reservation has expired:
  1. The system checks whether unreserved stock remains available. If available, it re-reserves the unit atomically and marks the order `PAID`.
  2. If the inventory has already been claimed by another buyer, the system **refuses to transition the order to `PAID`**. Instead, it transitions the order to an explicit intermediate state: `NEEDS_REFUND` (Payment Captured, Stock Unavailable).
  3. Within the same transaction, an automated refund request is queued in the approval workflow, and the customer is notified of the out-of-stock condition, completely preserving the invariant that physical stock cannot be oversold.

---

### Inconsistency 4: Premature Destruction of Approval Evidence on Gateway Refund Failure
- **Original Flawed Modeling:** In the preliminary refund lifecycle model, if the external payment gateway rejected or timed out during a refund execution attempt (`EXECUTING` -> `FAILED`), the refund entity was reset to `REQUESTED` or deleted, requiring the customer support team to seek a fresh finance approval.
- **Identified Failure Mode & Risk:** Wiping out the approval record causes operational friction, delays customer reimbursement, and destroys the audit trail of the original finance officer's authorization. More dangerously, if the gateway actually accepted the transaction but the HTTP acknowledgement timed out, re-submitting a newly approved request could trigger a duplicate financial refund payout.
- **Architectural Correction:**
  The refund state machine was restructured to introduce a dedicated `FAILED` state that **explicitly retains the original `approved_by` reference, approval timestamp, and pre-allocated idempotency key**. A failure during execution simply flags the entity as `FAILED` (Retryable). A subsequent retry by the outbox worker or finance reviewer reuses the exact same idempotency key and original approval token. The gateway recognizes the idempotency key and prevents duplicate disbursements, while the audit log retains an unbroken chain of custody.
