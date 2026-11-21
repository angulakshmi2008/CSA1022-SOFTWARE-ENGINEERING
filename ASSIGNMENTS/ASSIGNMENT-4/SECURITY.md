# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.1.x   | :white_check_mark: |
| 2.0.x   | :x:                |
| < 2.0   | :x:                |

## Security Architecture & Release Principles

1. **Direct Backend Authorization Enforcement:**
   Frontend controls are never treated as the security boundary. Role-based authorization is checked on every protected endpoint in the API layer. Unauthorized requests are rejected with HTTP 403 Forbidden without mutating database state.

2. **Strict Cryptographic Standards:**
   - Password hashing utilizes salted bcrypt with 12 rounds.
   - JWT tokens are signed using HMAC-SHA256 with verifiable claims (`sub`, `role`, `exp`, `iat`).
   - Secret keys are loaded strictly from environment variables and never committed to source control.

3. **Transaction Isolation & Optimistic Locking:**
   - Booking overlap checks and record insertion occur within an isolated transaction.
   - Maintenance tickets enforce optimistic concurrency control via integer version counters to reject stale concurrent mutations (HTTP 409 Conflict).

4. **Automated Static & Dependency Scanning:**
   - Bandit runs on every pull request to detect AST security anti-patterns.
   - Pip-audit monitors pinned dependencies against the PyPI/OSV advisory databases.

## Reporting a Vulnerability

If you discover a security vulnerability, please submit a report to `security@campus.edu`.
All reports are acknowledged within 24 hours and treated with high confidentiality.
