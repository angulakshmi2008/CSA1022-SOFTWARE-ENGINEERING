# ADR-003: Server-Side Role-Based Authorization and Client Idempotency Keys

## Status
Accepted

## Context and Problem Statement
The Omnichannel Order Fulfilment Platform coordinates six distinct user roles: Customer, Warehouse Picker, Support Agent, Finance Reviewer, Store Manager, and Administrator. Certain critical operations carry extreme financial and security implications:
1. Approving and executing financial refunds.
2. Altering warehouse order statuses and dispatch confirmations.
3. Accessing sensitive customer order records across accounts.
4. Managing regional tax and shipping policy rates.

In naive web architectures, role selection is often handled in the UI (e.g., role selector dropdowns or client-side route guards). Furthermore, erratic client mobile networks cause users to double-click buttons or retry HTTP requests, triggering duplicate mutating actions (duplicate orders, repeated refund requests).

How should the platform guarantee perimeter security, least privilege, and idempotent request safety?

## Decision Drivers
- Zero trust of client-side role declarations or browser-generated states.
- Prevention of privilege escalation (e.g., support agents approving financial refunds).
- Protection against cross-tenant / cross-customer data exfiltration.
- Elimination of duplicate side effects from retried network requests.

## Considered Alternatives
1. **Client-Side Authorization with Coarse API Checks:** UI hides buttons based on role; API verifies only token presence. High vulnerability to API tampering.
2. **Decentralized OAuth2/OIDC with External Policy Engine (OPA):** Highly scalable, but introduces extra network latency and operational complexity for a small application.
3. **Stateless Server-Side JWT Claims with Dependency-Injected FastAPI RBAC and Database-Backed Roles:** Cryptographically signed JWT tokens issued upon authentication; server-side security dependencies inspect roles and resource ownership for every endpoint.

## Decision Outcome
Chosen option: **Stateless Server-Side JWT Authorization with Scoped Resource Guards and Unique Idempotency Keys**.

### Positive Consequences
- **Server-Enforced Perimeter Security:** Every protected endpoint declares an explicit role dependency (e.g., `Depends(require_role([UserRole.FINANCE_REVIEWER]))`). A user attempting to access a privileged endpoint without the required role is rejected with HTTP 403 Forbidden.
- **Strict Customer Resource Ownership Isolation:** Customer order endpoints verify that `order.owner_id == authenticated_user_id`. Attempting to read another customer's order ID returns HTTP 403 Forbidden.
- **Idempotent Client Ingestion:** Financial mutation endpoints (`POST /api/refunds`, `POST /api/payments/callback`) require an `Idempotency-Key` header or payload identifier. Repeated deliveries return the cached outcome with identical HTTP status codes, preventing double refund disbursements.
- **Optimistic Versioning:** Mutable entities (`orders`, `stock_items`, `refund_requests`) maintain an integer `version` column. Concurrent updates verify `WHERE version = :expected_version`, preventing lost updates.

### Negative Consequences and Mitigations
- **Token Invalidation Complexity:** Stateless JWTs cannot be revoked instantly without maintaining a token blacklist.
  - *Mitigation:* Tokens enforce short lifetimes (60 minutes). Sensitive operations (e.g., refund approvals) require fresh authentication verification.
