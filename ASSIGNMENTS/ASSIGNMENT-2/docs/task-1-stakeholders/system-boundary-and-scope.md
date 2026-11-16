# Task 1: System Boundary, Actors, and Scope Exclusions

## 1. System Boundary Definition
The boundary of the Omnichannel Order Fulfilment Platform encompasses all software components, data stores, background workers, and business logic owned and operated directly by the retail enterprise. 

```text
+-----------------------------------------------------------------------------------------+
|                                    SYSTEM BOUNDARY                                      |
|                                                                                         |
|  +--------------------+   +------------------------------------+   +-----------------+  |
|  | React Presentation |   |      Modular FastAPI Application   |   |   PostgreSQL    |  |
|  | - Storefront       |   | - Auth & Server RBAC               |   |   Transactional |  |
|  | - Picker Dash      |-->| - Catalog & Pricing Engine         |-->|   Database      |  |
|  | - Support Console  |   | - Atomic Reservation & Expiry      |   | - Orders        |  |
|  | - Finance Reviewer |   | - Order Lifecycle Management       |   | - Stock Items   |  |
|  | - Admin Panel      |   | - Callback Verification & Idemp.   |   | - Reservations  |  |
|  | - Manager Reports  |   | - Refund State Governance          |   | - Payments      |  |
|  +--------------------+   | - Offline Scanner Sync & Dedup     |   | - Refunds       |  |
|                           +------------------------------------+   | - Outbox Table  |  |
|                                             |                      | - Audit Trail   |  |
|                                             v                      +-----------------+  |
|                           +------------------------------------+            ^           |
|                           | Transactional Outbox Worker        |------------+           |
|                           | - Polls pending intents            |                        |
|                           | - Retries with exponential backoff |                        |
|                           | - Correlation key reconciliation   |                        |
|                           +------------------------------------+                        |
+-----------------------------------------------------------------------------------------+
             |                                              |
             | HTTPS Webhooks                               | REST API Integration
             v                                              v
+-----------------------------+               +-----------------------------+
|   Payment Gateway (Mock)    |               |      Courier API (Mock)     |
| - Sends signed callbacks    |               | - Accepts shipment intents  |
| - Processes refund requests |               | - Generates tracking IDs    |
+-----------------------------+               +-----------------------------+
```

### Components Within the System Boundary
1. **Frontend Client Layer:** Role-based web dashboards built in React and TypeScript for Customer, Picker, Support Agent, Finance Reviewer, Store Manager, and Administrator.
2. **Reverse Proxy & Routing Layer:** Nginx container managing TLS termination, CORS policy, and request proxying.
3. **Application Server Layer:** Python FastAPI stateless application service providing authenticated REST endpoints, server-side RBAC validation, atomic inventory management, order state machine execution, and scanner sync endpoints.
4. **Data Persistence Layer:** PostgreSQL relational database hosting operational tables, foreign keys, unique constraint indexes, row-level concurrency locks, and transactional outbox queues.
5. **Asynchronous Background Processing Layer:** Outbox worker daemon responsible for dispatching external integration requests (courier API, payment gateway refunds) and reservation expiry cleanup.

---

## 2. Principal Actors
1. **Human Actors:**
   - `Customer`: Authenticated retail buyer interacting with catalog, cart, checkout, order tracking, and returns.
   - `Warehouse Picker`: Warehouse floor operator executing physical item picking and packing.
   - `Support Agent`: Customer service representative resolving delivery questions and initiating return requests.
   - `Finance Reviewer`: Authorized accountant reviewing and deciding on high-value refund requests.
   - `Store Manager`: Retail supervisor monitoring aggregated regional sales, inventory levels, and refund analytics.
   - `Administrator`: Enterprise engineer managing user role grants, regional policy configuration, and audit inspections.

2. **System & Device Actors:**
   - `Payment Gateway`: External financial institution transmitting signed webhook callbacks and processing refund intents.
   - `Courier Service API`: External logistics partner ingesting shipment orders and returning parcel tracking tokens.
   - `Warehouse Scanner Node`: Handheld edge device buffering physical barcode scan events during connectivity loss and syncing batches on reconnect.

---

## 3. Explicit Scope Exclusions
To ensure realistic engineering execution and prevent unsubstantiated claims in the initial release, the following capabilities are explicitly **excluded from the system boundary**:
1. **Direct Storage of Raw Cardholder Data:** The platform NEVER stores Credit Card PANs, CVVs, or cardholder magnetic stripe data. All payment processing relies on tokenized references and signed webhooks, eliminating full PCI-DSS scope.
2. **Autonomous Machine Learning Demand Forecasting:** Inventory replenishment relies on deterministic, fixed low-stock thresholds rather than unverified statistical or machine-learning models.
3. **Autonomous High-Value Refund Approval:** The system does not permit unattended, algorithm-driven refund approvals for amounts exceeding the regional threshold. Human review is strictly enforced.
4. **Fully Decentralized Multi-Master Offline Database Clusters:** Offline warehouse scanners buffer events locally in a bounded client queue, but do not host an independent relational database engine. Offline global refund approval is strictly prohibited.
5. **Public Partner Marketplace APIs:** External programmatic API access is restricted to authenticated internal consumers and verified external webhooks; public open APIs are deferred to future releases.
