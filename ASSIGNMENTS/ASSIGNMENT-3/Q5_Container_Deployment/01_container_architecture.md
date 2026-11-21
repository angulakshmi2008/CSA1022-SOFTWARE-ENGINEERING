# Question 5: Container Architecture & Service Orchestration

## 1. Multi-Tier Container Architecture

The Smart Campus Platform uses Docker and Docker Compose to provide an immutable, isolated, and reproducible deployment environment across development, testing, and production.

```
                           [ User Browser / Client ]
                                       │
                                       ▼ HTTP :80
                     ┌───────────────────────────────────┐
                     │          frontend                 │
                     │  (Nginx Alpine + Vue 3 SPA dist)  │
                     └─────────────────┬─────────────────┘
                                       │ /api/ reverse proxy
                                       ▼ HTTP :8000
                     ┌───────────────────────────────────┐
                     │          backend                  │
                     │  (Python 3.11 + Django REST Guni) │
                     └─────────────────┬─────────────────┘
                                       │ TCP :5432
                                       ▼
                     ┌───────────────────────────────────┐
                     │          database                 │
                     │       (PostgreSQL 16)             │
                     │  Persistent Volume: postgres_data │
                     └───────────────────────────────────┘
                                       ▲
                                       │ TCP :5432
                     ┌─────────────────┴─────────────────┐
                     │          worker                   │
                     │  (Async Outbox / Sensor Dispatch) │
                     └───────────────────────────────────┘
```

---

## 2. Compose Service Definitions

### 2.1 `database` (PostgreSQL 16 Alpine)
- **Image**: `postgres:16-alpine`
- **Role**: Primary relational persistence store with native support for `btree_gist` range exclusion constraints, JSONB audit logs, and row-level locking (`FOR UPDATE`).
- **Storage**: Attached to named persistent Docker volume `postgres_data` mounted at `/var/lib/postgresql/data`.
- **Healthcheck**: Periodically polls `pg_isready -U smart_campus -d smart_campus_db` with a 5s interval, 5s timeout, and 5 retries.

### 2.2 `backend` (Django REST Framework Web Tier)
- **Base Image**: `python:3.11-slim`
- **Role**: Stateless REST API layer serving endpoints for facilities, bookings, maintenance, triage, approvals, and sensor ingestion.
- **Port**: Container port 8000 exposed internally and mapped to host port 8000.
- **Dependency**: Explicitly depends on `database` service condition `service_healthy`.
- **Healthcheck**: Probes `/api/health/` using `curl -f` with a 10s interval, ensuring readiness before traffic routing.

### 2.3 `frontend` (Vue 3 Single Page Application)
- **Base Image**: Multi-stage build (`node:20-alpine` build stage -> `nginx:1.25-alpine` runtime stage).
- **Role**: Serves optimized static assets and routes API traffic seamlessly via reverse proxy configuration in `/etc/nginx/conf.d/default.conf`.
- **Port**: Host port 80 (or 5173 for dev).

### 2.4 `worker` (Durable Integration & Outbox Dispatcher)
- **Base Image**: Identical to `backend` (`python:3.11-slim`).
- **Role**: Asynchronous background processor handling external DevOps issue synchronization, idempotent webhook dispatches, and SLA breach monitors without blocking user-facing HTTP request-response cycles.

---

## 3. Network & Isolation Policies

- **Bridge Network**: All services communicate across an isolated internal Docker bridge network: `smart_campus_net`.
- **DNS Service Discovery**: Services resolve each other by container service name (e.g., `http://backend:8000`, `postgres://database:5432`).
- **Host Port Exposure**: In production, only the frontend web server (port 80/443) is exposed to the public internet. The database port 5432 is strictly confined to `smart_campus_net` to prevent external database intrusion.

---

## 4. Secrets Management & Environment Configuration

In strict adherence to Twelve-Factor App principles and security standards:
- **Zero Secrets in Git**: No production passwords, secret keys, or API tokens are hardcoded or committed into Git. The repository tracks only `.env.example`.
- **Runtime Injection**: Environment variables are passed via Docker Compose environment blocks or an uncommitted `.env` file mounted at container initialization:
  - `DJANGO_SECRET_KEY`: High-entropy cryptographic signing key.
  - `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`: Database credentials.
  - `DEBUG`: Strictly set to `False` in production containers.
  - `ALLOWED_HOSTS`: Domain allowlist for host header validation.
  - `EXTERNAL_ISSUE_TRACKER_TOKEN`: Authentication token for DevOps issue tracker integration.
