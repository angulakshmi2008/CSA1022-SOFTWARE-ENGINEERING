# Task 4: Comparative Evaluation of Architectural Alternatives

To establish a defensible architectural foundation for the Omnichannel Order Fulfilment Platform, two meaningfully distinct architectural patterns were designed and evaluated:
- **Alternative A:** Modular Monolith with Asynchronous Integration Worker
- **Alternative B:** Distributed Microservices with Event Broker (Kafka/RabbitMQ)

---

## 1. Architectural Pattern Descriptions

### Alternative A: Modular Monolith with Asynchronous Outbox Worker
Alternative A organizes the backend application as a single deployable service partitioned into strictly encapsulated domain modules (`Auth`, `Orders`, `Inventory`, `Payments`, `Refunds`, `Warehouse`, `Courier`, `Reporting`). All modules share a centralized PostgreSQL relational database, but communicate through well-defined internal Python interfaces (service layer APIs). mutating cross-module operations (such as placing an order and reserving stock) execute within local ACID database transactions. Asynchronous third-party integrations (courier parcel registration, gateway refund requests) are stored in an `outbox_intents` table within the same transaction and processed by a dedicated background worker daemon.

### Alternative B: Distributed Microservices with Event Broker
Alternative B decomposes the platform into independent, separately deployed microservices: `Order Service`, `Inventory Service`, `Payment Service`, `Refund Service`, `Fulfilment Service`, and `Reporting Service`. Each service possesses private database persistence (Database-per-Service pattern). Cross-service communication relies on an asynchronous event broker (e.g., Apache Kafka or RabbitMQ) utilizing choreograph-based Sagas, compensating transactions, and idempotent event consumers.

---

## 2. In-Depth Comparative Evaluation Across 10 Dimensions

| Evaluation Dimension | Alternative A: Modular Monolith with Worker | Alternative B: Distributed Microservices with Event Broker |
| :--- | :--- | :--- |
| **1. Components & Responsibilities** | Single application container containing modular domain subpackages. Clear code-level boundaries; easy refactoring and shared domain types. | 6+ distinct deployable microservice containers, API gateway, and message broker cluster. High component sprawl. |
| **2. Data Ownership & Schema** | Centralized PostgreSQL schema with strict logical ownership per module. Cross-module foreign keys enforce referential integrity. | Database-per-service pattern. Zero database-level referential integrity; cross-service data queries require data duplication or CQRS read models. |
| **3. Communication Overhead** | In-process function/method calls with zero network serialization latency. High execution efficiency (~microseconds). | Inter-service HTTP/gRPC or asynchronous AMQP message queues. Network serialization, latency overhead (~milliseconds), and network partition risks. |
| **4. Duplicate Payment Prevention** | Atomic database `UNIQUE(gateway_id, event_id)` constraint within the callback transaction. 100% deterministic duplicate rejection. | Requires distributed deduplication cache (e.g., Redis) or dual-stage deduplication in Payment Service and event consumer sagas. |
| **5. Last-Unit Stock Reservation** | Row-level locking (`SELECT ... FOR UPDATE` or conditional SQL update) within local transaction. Guaranteed zero overselling. | Distributed Saga orchestration. Requires complex reservation leases, distributed locking, and compensating events if payment fails. |
| **6. Security & Authorization** | Centralized security middleware validating JWT tokens and user roles in memory on each incoming request. Uniform audit logging. | Each microservice must authenticate requests (propagating security tokens) or trust the upstream API gateway, increasing attack surface. |
| **7. Scalability & Elasticity** | Horizontal scaling achieved by replicating stateless API containers behind Nginx. Database connection pooling manages load. | Fine-grained independent horizontal scaling (e.g., scaling Inventory Service during flash sales without scaling Refund Service). |
| **8. Availability & Fault Isolation** | Central database failure impacts entire system. However, absence of distributed network dependencies reduces transient failures. | High theoretical service isolation (e.g., Reporting Service crash does not impact Checkout). However, broker or network partition cascades. |
| **9. Operational Complexity** | Very Low: Single CI/CD pipeline, standard Docker Compose local setup, single database backup regimen, simple log aggregation. | Very High: Multi-repo/poly-repo CI/CD pipelines, distributed tracing (OpenTelemetry/Jaeger), message broker management, schema registries. |
| **10. Failure Points & Maintenance** | Few failure modes: API container, worker daemon, PostgreSQL. Simple failure reproduction and debugging. | Numerous failure modes: message serialization bugs, broker lag, dead-letter queues, out-of-order events, split-brain network failures. |

---

## 3. Justified Selection: Alternative A (Modular Monolith)

Alternative A is selected as the authoritative architectural foundation for the initial release based on the following engineering rationale:
1. **Team Size and Operational Reality:** The problem statement explicitly establishes that the platform is initially developed and maintained by a *modest technical team*. Microservices impose severe "microservice tax"—infrastructure engineering, distributed debugging, distributed tracing, and distributed transactions—that would divert limited resources away from core fulfilment logic.
2. **Absolute Consistency for Financial and Inventory State:** Business rules mandate that available stock can never drop below zero and duplicate payment callbacks must never double-bill. In a microservices architecture, preventing overselling across separate Order and Inventory databases requires distributed sagas with eventual consistency, creating edge cases where items are promised to customers but lost in distributed rollback races. Alternative A guarantees ACID serializability at the database level.
3. **Decoupled Asynchrony Without Broker Overhead:** By employing the **Transactional Outbox Pattern** with a relational table (`outbox_intents`), Alternative A achieves the core resilience benefits of an event broker (retry with backoff, fault isolation against third-party courier outages) without the operational burden of managing a Kafka or RabbitMQ cluster.
4. **Clean Evolutionary Path:** Because domain boundaries are cleanly enforced through modular code design, should measured real-world traffic patterns in future years demand service extraction, individual modules (e.g., Reporting or Inventory) can be decoupled cleanly into microservices without rewriting business logic.
