# Task 3: Requirements-to-Model-to-Component-to-Validation Traceability Matrix

The traceability matrix below establishes an unbroken chain of evidence linking every functional requirement (`FR01`–`FR14`) and non-functional requirement (`NFR01`–`NFR08`) to its corresponding UML representation, underlying backend implementation file/module, and automated verification test ID.

| Requirement ID | Requirement Summary | UML Diagram & Model Element | Backend Code Module / File | Automated Validation Test ID |
| :--- | :--- | :--- | :--- | :--- |
| **FR01** | Authentication & Server RBAC | Use Case: Actor Permissions<br>Class: `User`, `RoleAssignment` | `backend/app/core/security.py`<br>`backend/app/api/auth.py` | `T6_SECURITY_RBAC` |
| **FR02** | Order Placement & Validation | Use Case: `UC2 (Place Order)`<br>Class: `Order`, `OrderLine` | `backend/app/api/orders.py`<br>`backend/app/services/order_service.py` | `T4_DISPATCH_GUARDS` |
| **FR03** | Atomic Stock Reservation | Use Case: `UC2`, Class: `StockItem`, `Reservation` | `backend/app/services/inventory_service.py`<br>`backend/app/models/inventory.py` | `T1_STOCK_CONTENTION` |
| **FR04** | Authoritative Pricing & Tax | Class: `RegionalPolicy`, `Order`<br>Sequence: Step 1 (Pricing) | `backend/app/services/pricing_service.py`<br>`backend/app/models/policy.py` | `T9_REGIONAL_POLICY` |
| **FR05** | Idempotent Payment Callback | Sequence: `Signed callback`<br>Class: `PaymentEvent (Unique Key)` | `backend/app/api/payments.py`<br>`backend/app/integrations/payment/mock_gateway.py` | `T2_DUPLICATE_CALLBACK` |
| **FR06** | Guarded Order Lifecycle | State Machine: Order State View<br>Class: `Order.transition_to()` | `backend/app/services/order_service.py`<br>`backend/app/models/order.py` | `T4_DISPATCH_GUARDS` |
| **FR07** | Pick-List Isolation | Use Case: `UC5 (View Pick Lists)`<br>Class: `Order (Assigned Region)` | `backend/app/api/warehouse.py`<br>`backend/app/services/warehouse_service.py` | `T4_DISPATCH_GUARDS` |
| **FR08** | Reservation Expiry & Late Reconcile | State Machine: `NEEDS_REFUND`<br>Class: `Reservation.release()` | `backend/app/workers/expiry_worker.py`<br>`backend/app/services/inventory_service.py` | `T7_LATE_PAYMENT_EXPIRY` |
| **FR09** | Dispatch Tracking Milestones | Use Case: `UC7`, Sequence: Step 3<br>Class: `IntegrationIntent` | `backend/app/api/orders.py`<br>`backend/app/integrations/courier/mock_courier.py` | `T5_COURIER_RETRY` |
| **FR10** | Dual-Control Refund Governance | State Machine: Refund State View<br>Class: `RefundRequest` | `backend/app/api/refunds.py`<br>`backend/app/services/refund_service.py` | `T3_REFUND_FAILURE_RETRY`<br>`T6_SECURITY_RBAC` |
| **FR11** | Transactional Outbox Integration | Sequence: Steps 8-16<br>Class: `IntegrationIntent` | `backend/app/workers/outbox_worker.py`<br>`backend/app/models/outbox.py` | `T5_COURIER_RETRY` |
| **FR12** | Immutable Audit Trail & Reports | Use Case: `UC14 (Reports)`<br>Class: `AuditEvent` | `backend/app/services/audit_service.py`<br>`backend/app/api/reporting.py` | `T2_DUPLICATE_CALLBACK`<br>`T6_SECURITY_RBAC` |
| **FR13** | Regional Versioned Policies | Class: `RegionalPolicy`<br>Order State: Region Snapshot | `backend/app/api/policies.py`<br>`backend/app/models/policy.py` | `T9_REGIONAL_POLICY` |
| **FR14** | Offline Scanner Sync & Dedup | Use Case: `UC8 (Sync Scans)`<br>Class: `ScannerEventLog` | `backend/app/api/scanner.py`<br>`backend/app/services/scanner_service.py` | `T8_SCANNER_DEDUPLICATION` |
| **NFR01** | p95 Latency < 800 ms | Deployment: Fast connection pooling | `backend/app/main.py` | Performance Benchmark Suite |
| **NFR02** | Zero Negative Stock Invariant | Class: `StockItem` constraint | `backend/app/models/inventory.py` | `T1_STOCK_CONTENTION` |
| **NFR03** | RTO <= 15m, RPO = 0 | Outbox Intent Durable Persistence | `backend/app/workers/outbox_worker.py` | `T5_COURIER_RETRY` |
| **NFR04** | Role-Based Least Privilege | Class: `User.has_permission()` | `backend/app/core/security.py` | `T6_SECURITY_RBAC` |
| **NFR05** | Keyboard Accessibility | React UI Component Specs | `frontend/src/components/` | Front-end Accessibility Walkthrough |
| **NFR06** | Single-Command Portability | Docker Compose Architecture | `docker-compose.yml`<br>`infra/docker/` | Docker Container Build Test |
| **NFR07** | Expansion to 12 Regions | Regional Policy Engine | `backend/app/models/policy.py` | `T9_REGIONAL_POLICY` |
| **NFR08** | Audit Trail Completeness | Class: `AuditEvent` | `backend/app/services/audit_service.py` | Test Suite Invariant Assertions |
