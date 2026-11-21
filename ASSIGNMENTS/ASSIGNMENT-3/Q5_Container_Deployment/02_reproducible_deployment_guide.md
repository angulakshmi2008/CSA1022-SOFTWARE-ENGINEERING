# Question 5: Reproducible Deployment Guide & Operational Runbook

## 1. Prerequisites
- Docker Engine v24.0.0+
- Docker Compose v2.20.0+
- Minimum Host Memory: 4 GB RAM
- Minimum Disk Space: 10 GB free space

---

## 2. Initial Setup & Secrets Configuration

1. **Clone the release tag**:
   ```bash
   git clone -b v1.0.0 https://github.com/angulakshmi2008/CSA1022-SOFTWARE-ENGINEERING.git
   cd CSA1022-SOFTWARE-ENGINEERING/ASSIGNMENTS/ASSIGNMENT-3
   ```

2. **Initialize Environment Variables**:
   Copy the template and supply secure credentials:
   ```bash
   cp .env.example .env
   ```
   Verify that `.env` contains:
   ```ini
   DEBUG=False
   SECRET_KEY=production-secure-random-token-change-in-prod-xyz
   ALLOWED_HOSTS=localhost,127.0.0.1,backend
   DB_ENGINE=django.db.backends.postgresql
   POSTGRES_DB=smart_campus_db
   POSTGRES_USER=smart_campus
   POSTGRES_PASSWORD=supersecurepassword123
   POSTGRES_HOST=database
   POSTGRES_PORT=5432
   ```

---

## 3. Container Startup & Lifecycle Commands

### 3.1 Build and Launch All Services
```bash
docker compose up -d --build
```
This command builds the frontend and backend images, initializes the `postgres_data` persistent volume, sets up `smart_campus_net`, and starts all four containers in detached mode.

### 3.2 Inspect Service Health & Readiness
```bash
docker compose ps
```
*Expected status*: All containers (`smart_campus_database`, `smart_campus_backend`, `smart_campus_frontend`, `smart_campus_worker`) report `Up` with `(healthy)` flags.

### 3.3 Execute Database Migrations
```bash
docker compose exec backend python manage.py migrate
```

### 3.4 Seed Baseline University Data
```bash
docker compose exec backend python database/seed/seed_data.py
```
This loads the 6 campuses, default facilities (lecture halls, labs, seminar rooms), user roles, and SLA matrices.

---

## 4. Verification and Health Probing

Probing endpoints directly from host or container:
```bash
# Probing backend health check endpoint
curl -i http://localhost:8000/api/health/

# Expected output:
# HTTP/1.1 200 OK
# Content-Type: application/json
# {"status": "healthy", "database": "connected", "version": "1.0.0"}
```

---

## 5. Shutdown and Maintenance Commands

### 5.1 Graceful Shutdown (Preserves Persistent Data)
```bash
docker compose down
```
*Note*: Stops and removes running containers and networks, but **retains** the `postgres_data` volume intact. When restarted via `docker compose up -d`, all bookings, tickets, and user accounts remain immediately available.

### 5.2 Clean Teardown (Removes Volumes - Destructive)
```bash
docker compose down -v
```
*Warning*: The `-v` flag deletes named persistent volumes. Use only when performing a total factory reset.

---

## 6. Backup and Restore Operational Limitations

### 6.1 Volume Limitations vs Logical Backups
- A Docker named volume (`postgres_data`) provides **persistence across container recreation**, but is **NOT a backup strategy**. If the host storage fails, corrupts, or the volume is deleted with `down -v`, data cannot be recovered from the volume alone.
- Production environments mandate scheduled logical database dumps:

### 6.2 Manual Logical Backup
```bash
docker compose exec -T database pg_dump -U smart_campus smart_campus_db | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

### 6.3 Manual Logical Restore
```bash
gunzip -c backup_20261121_120000.sql.gz | docker compose exec -T database psql -U smart_campus -d smart_campus_db
```
