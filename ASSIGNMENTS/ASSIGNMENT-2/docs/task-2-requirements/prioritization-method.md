# Task 2: Requirements Prioritization Methodology and Conflict Influence

## 1. Prioritization Framework: Risk-Adjusted MoSCoW
Standard MoSCoW (Must, Should, Could, Won't) prioritization frequently treats functional desire as the primary sorting criterion. In this project, requirements are prioritized using a **Risk-Adjusted MoSCoW Model**, which weights each candidate feature against two critical enterprise hazards:
1. **Financial Loss & Regulatory Penalty:** Risk of double disbursements, unrecorded revenues, overselling liabilities, or PCI-DSS non-compliance.
2. **Customer Harm & Broken Trust:** Risk of charging a customer without reserving inventory, exposing sensitive customer identity, or losing track of placed orders.

### Classification Rationale:
- **MUST HAVE (Critical Path to Prevent Loss and Establish Invariants):**
  - `FR01` (Authentication & Server RBAC): Essential to prevent unauthorized access or privilege escalation.
  - `FR02` (Order Placement Validation): Mandatory to guarantee data integrity at ingestion.
  - `FR03` (Atomic Stock Reservation): Critical to prevent physical overselling and warehouse deadlocks.
  - `FR04` (Authoritative Pricing & Tax): Non-negotiable to prevent client-side price tampering.
  - `FR05` (Idempotent Payment Callback): Essential to eliminate duplicate billing and double fulfilment.
  - `FR06` (Guarded Order Lifecycle): Mandatory to ensure orders cannot be dispatched without payment and picking.
  - `FR08` (Reservation Expiry & Late Reconciliation): Required to release dead stock while safely catching late payments.
  - `FR10` (Dual-Control Refund Governance): Critical to prevent internal fraud and unauthorized financial outflows.
  - `FR11` (Transactional Outbox Integration): Mandatory to ensure distributed network glitches do not drop delivery intents.
  - `FR13` & `FR14` (Regional Policies & Scanner Deduplication): Core expansion must-haves for multi-regional scaling.

- **SHOULD HAVE (High Operational Value, Delivered Immediately Following Core Invariants):**
  - `FR07` (Pick-List Filtering): Enhances warehouse worker productivity by sorting by warehouse region.
  - `FR09` (Dispatch Tracking & Milestones): Provides parcel tracking transparency to customers.
  - `FR12` (Audit Trail & Consolidated Reporting): Enables managerial visibility and compliance audits.

- **COULD HAVE (Deferred to Future Iterations):**
  - Dynamic AI-driven demand forecasting.
  - Mobile push notifications for warehouse pickers.
  - Automated carrier rate shopping across competing logistics providers.

---

## 2. Explanation of How Stakeholder Conflicts Shaped the Final Specification

The final requirements specification was directly formulated to resolve the fundamental stakeholder tensions documented in Task 1:

### Impact of Conflict 1 (Checkout Speed vs. Stock Accuracy)
- *Initial Proposal:* Merchandising proposed an optimistic asynchronous checkout where stock is decremented asynchronously in a message queue to achieve a 50 ms checkout response.
- *The Problem:* Under high concurrent demand for the final item, multiple customers receive confirmation emails before the queue processes, forcing embarrassing order cancellations and customer complaints.
- *Requirement Specification Response:* The final specification rejected optimistic queuing in favor of **FR03** and **FR08**. Stock reservation is executed **synchronously within the database transaction** of the checkout endpoint using an atomic conditional update and optimistic version checking. To prevent abandoned carts from indefinitely locking inventory, a hard 15-minute lease was specified with automated worker reclamation.

### Impact of Conflict 4 (Fast Customer Refunds vs. Financial Governance)
- *Initial Proposal:* Support management requested a "one-click instant refund" button on the support agent console to resolve customer complaints on the first call.
- *The Problem:* Giving frontline agents unilateral authority to disburse company funds without approval creates severe fraud vulnerability and audit failure under financial governance standards.
- *Requirement Specification Response:* The final specification established **FR10**, splitting the refund lifecycle into distinct, audited stages: `REQUESTED` vs. `APPROVED` vs. `EXECUTED`. Support agents can only transition a case to `REQUESTED`. The system enforces a server-side rule: refunds over \$50.00 strictly require an independent `FINANCE_REVIEWER` approval before the execution endpoint `/refunds/{id}/execute` will accept the command.
