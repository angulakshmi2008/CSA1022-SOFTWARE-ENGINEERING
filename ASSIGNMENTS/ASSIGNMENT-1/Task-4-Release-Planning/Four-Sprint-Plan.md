# Task 4: Four-Sprint Release Plan and Capacity Negotiation

## 1. Initial Backlog Selection vs Capacity Negotiation

During initial release scoping, the Product Owner initially proposed committing to all foundational stories in Sprint 1:
- `S01 (3 pts)` + `S02 (5 pts)` + `S03 (5 pts)` + `S04 (3 pts)` + `S09 (5 pts)` = **21 Story Points**.

### The Overcommitment Dilemma:
Committing 21 points against an uncalibrated 16-point ceiling would guarantee delivery failure, unreviewed code, and QA starvation. Furthermore, Story S03 depended on the payment gateway sandbox (arriving in Week 4), which would cause developers to stall mid-sprint.

### The Architectural Slicing Solution:
1. **Slicing Story S03 (Payment Integration):**
   - **S03a (2 pts):** Idempotent payment request contract and local in-memory mock adapter. *Scheduled in Sprint 1.*
   - **S03b (3 pts):** Live external vendor sandbox integration and retry handler. *Resequenced to Sprint 3 (post Week 4).*
2. **Slicing Story S09 (Build and Automation):**
   - **S09a (3 pts):** Local build script and automated smoke test execution. *Scheduled in Sprint 1.*
   - **S09b (2 pts):** Full CI/CD automated pipeline enforcement. *Resequenced to Sprint 2.*

Following this negotiation, the Sprint 1 commitment reduced from 21 points to **exactly 16 points** ($3 + 5 + 2 + 3 + 3$), satisfying the capacity ceiling.

---

## 2. Four-Sprint Release Plan Breakdown

```
[Sprint 1: Weeks 1–2]  ──► Secure Ordering Foundation (16 Points)
[Sprint 2: Weeks 3–4]  ──► Dispatch, Tracking & Stock Alerts (13 Points)
[Sprint 3: Weeks 5–6]  ──► Payment Sandbox, Scanning & Refunds (14 Points)
[Sprint 4: Weeks 7–8]  ──► Support Console, Hardening & Release Rehearsal (3 Points + Buffer)
```

| Sprint | Calendar Timeline | Sprint Goal Statement | Selected Stories & Points | Total Points | External Constraints & Dependencies Handled |
|---|---|---|---|---|---|
| **Sprint 1** | Weeks 1–2 | **Establish Secure Ordering Foundation:** Enable authenticated users to log in, place an order with atomic stock reservation, process idempotent payments via a local stub, view eligible warehouse pick lists, and verify local build reproducibility. | • S01 (3) Login & RBAC<br>• S02 (5) Stock Reservation<br>• S03a (2) Idempotent Stub<br>• S04 (3) Warehouse Pick List<br>• S09a (3) Local Build & Smoke | **16 Pts** | Gateway sandbox and scanners are unavailable; mock payment adapter and synthetic stock data used. |
| **Sprint 2** | Weeks 3–4 | **Deliver Fulfillment Lifecycle, Milestone Tracking & Inventory Safety:** Enable warehouse dispatch state transitions, provide screen-reader accessible milestone tracking, enforce CI/CD checks, and trigger deterministic low-stock alerts. | • S05 (5) Dispatch Transitions<br>• S06 (3) Customer Tracking<br>• S09b (2) CI/CD Pipeline<br>• S11 (3) Low-Stock Alerts | **13 Pts** | Gateway sandbox access begins at end of Week 4; prepares order state machine for live integration. |
| **Sprint 3** | Weeks 5–6 | **Integrate External Payment Gateway, Barcode Scanning & Controlled Refunds:** Integrate live sandbox payments, verify physical barcode picking, and enable customer returns with finance-controlled refund approvals. | • S03b (3) Sandbox Payment<br>• S07 (3) Return Requests<br>• S08 (5) Refund Approval<br>• S12 (3) Barcode Scanning | **14 Pts** | Payment sandbox active (Week 4); Barcode test scanner arrives (Week 5). |
| **Sprint 4** | Weeks 7–8 | **Support Visibility, End-to-End Hardening & Release Rehearsal:** Empower customer support order lookups, absorb carryover defects, execute full cross-browser regression, and complete release staging rehearsal. | • S10 (3) Support Order Lookup<br>• Unplanned defect buffer<br>• End-to-end regression rehearsal | **3 New Pts** (+ Buffer) | Dedicated 80% capacity reserve for production dry-runs ahead of festival-sale launch. |
| **Deferred** | Post-Launch | **Advanced Enterprise Capabilities:** Machine-learning demand forecasting, automated loyalty programs, multi-currency conversion, and executive sales analytics. | • S13 (3) Sales Analytics<br>• Advanced Roadmap Modules | **Deferred** | Excluded to protect core transactional integrity. |

---

## 3. Product Goal Coherence

The four-sprint roadmap systematically delivers the complete order-to-refund journey:
1. **Weeks 1–2 (Sprint 1):** Orders are created without risk of inventory overselling (`S01`, `S02`) and paid via an idempotent interface (`S03a`), generating initial warehouse pick queues (`S04`).
2. **Weeks 3–4 (Sprint 2):** Orders are packed and dispatched through audited state transitions (`S05`), and customers track public milestones (`S06`) while inventory levels are protected by automated thresholds (`S11`).
3. **Weeks 5–6 (Sprint 3):** Real gateway sandbox integration is validated (`S03b`), physical items are verified via barcode scanning (`S12`), and customers can request returns (`S07`) that finance reviewers approve through audited controls (`S08`).
4. **Weeks 7–8 (Sprint 4):** Customer support gains rapid lookup capabilities (`S10`), and the entire omnichannel pipeline is hardened through full regression rehearsal.

By Sprint 4, every operational problem identified in Task 1 (overselling, untraceable orders, duplicate charges, unauthorized refunds) is resolved by demonstrable, tested software.
