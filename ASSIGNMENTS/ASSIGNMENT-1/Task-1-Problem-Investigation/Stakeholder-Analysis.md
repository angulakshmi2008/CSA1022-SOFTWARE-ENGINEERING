# Task 1: Stakeholder Analysis and Simulated Findings

## 1. Stakeholder Classification Matrix
The omnichannel order fulfilment ecosystem involves multiple user roles with divergent operational priorities, access requirements, and constraints.

| Stakeholder Role | Primary Priority | Key Pain Point in Current System | Access Permissions Required |
|---|---|---|---|
| **Customer** | Timely delivery, transparent tracking, easy returns. | Orders show "Processing" for days; no visibility into actual package location; delayed refunds. | Read-only access to own orders, payment history, and public milestone tracking. |
| **Warehouse Picker** | High pick accuracy, zero phantom inventory, efficient routing. | Items on pick lists have already been sold online; pick lists contain out-of-stock items. | Read/Update access to allocated warehouse pick batches; barcode scan confirmation. |
| **Support Agent** | Rapid customer resolution, comprehensive order lookup. | Cannot view detailed order history or return status; inundated with status inquiries. | Read access to customer order history; permission to initiate return requests. |
| **Finance Reviewer** | Strict auditability, regulatory compliance, zero revenue leakage. | Refunds approved via informal messaging; no reconciliation between payments and orders. | Sole authorization to approve refunds > \$50; read access to financial audit journals. |
| **Store Manager** | Omnichannel inventory parity, accurate local stock counts. | Store walk-in sales cause online orders for the same item to fail due to sync delays. | Read/Write access to local store inventory adjustments and store-pickup releases. |
| **Development Team** | Stable contracts, decoupled architecture, low defect rate. | External payment sandbox and physical scanners are delayed; tight 8-week deadline. | Full repository, CI/CD, database schema, and test-harness configuration access. |

---

## 2. Simulated Stakeholder Discussion Findings

> **Note:** All findings below represent structured planning responses generated from simulated stakeholder interview sessions.

### 2.1 Customer Persona Findings (Simulated)
- *"I ordered a jacket that showed 'In Stock'. Three days later, my order was abruptly cancelled because the warehouse didn't have it. When I asked for a refund, it took 12 days to show up in my account with no status updates."*
- **Delivery Implication:** The platform must execute an atomic stock reservation at the moment the checkout begins, backed by a 15-minute countdown timer. Furthermore, the customer portal must display clear milestones (`Paid`, `Picked`, `Dispatched`, `Delivered`, `Refunded`) rather than generic statuses.

### 2.2 Warehouse Picker Findings (Simulated)
- *"We waste 20% of our shift walking to bin locations only to find empty shelves because the website allowed three different customers to buy the last pair of sneakers. We need pick lists that only show items physically reserved for paid orders."*
- **Delivery Implication:** Decouple available stock from physical on-hand stock. An order must not appear on a picker's dashboard until payment is confirmed and inventory reservation is verified.

### 2.3 Customer Support Agent Findings (Simulated)
- *"Over 60% of our incoming tickets are customers asking 'Where is my order?' or 'Why hasn't my return been processed?'. We currently have to email the warehouse manager and finance team manually to check."*
- **Delivery Implication:** Implement a centralized Support Order Lookup console that exposes timeline events, carrier tracking links, and return validation states without granting support staff direct write access to financial ledgers.

### 2.4 Finance Reviewer Findings (Simulated)
- *"We discovered store managers and junior agents issuing refunds directly to appease angry customers. Our quarterly audit flagged 14 untraceable refunds totaling over \$3,800. Every single refund must have an immutable audit trail showing who approved it, when, and the originating transaction ID."*
- **Delivery Implication:** Enforce strict Separation of Concerns (SoC). Support agents can submit return requests, but refunds must transition to `REFUND_PENDING` and require authenticated approval from a designated `Finance Reviewer` with monetary thresholds.

### 2.5 Store Manager Findings (Simulated)
- *"With 12 physical stores acting as mini-fulfilment hubs, physical inventory drifts rapidly during peak shopping hours. We need deterministic stock thresholds so that when stock falls below 3 units, online sales for that store are suspended immediately."*
- **Delivery Implication:** Implement a deterministic low-stock rule engine that triggers automatic availability locks when inventory dips below safety stock thresholds.

### 2.6 Development Team Findings (Simulated)
- *"The payment gateway vendor cannot provide sandbox API credentials until Week 4, and the industrial barcode scanner demo units won't arrive until Week 5. We cannot wait until then to start building."*
- **Delivery Implication:** Adopt a contract-first architectural pattern. Construct a local mock payment adapter with idempotency validation and a software-based barcode emulation layer to enable unblocked development during Sprints 1 and 2.
