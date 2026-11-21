# Question 6: Empirical Workload Benchmarking, Latency Profiles, and Capacity Analysis

## 1. Test Methodology & Environment

To empirically validate system resilience and establish actual throughput limits, a bounded load test was executed using `tests/concurrency/load_test.py`.

### 1.1 Test Configuration
- **Target Endpoints**: Facility catalogue listing (`GET /api/facilities/`), Booking creation (`POST /api/bookings/`), Ticket triage queue (`GET /api/maintenance/tickets/`).
- **Concurrency Stepping**: 10, 25, 50, and 100 concurrent worker threads executing synchronized transactional requests.
- **Duration**: Continuous workload generation across multiple rounds.
- **Hardware Profile**: Intel Core i5/i7 equivalent (Windows 64-bit host environment, Python 3.11 runtime, PostgreSQL 16 / SQLite ACID transactional backend).

---

## 2. Empirical Benchmark Measurements

The empirical test results were recorded directly in `docs/evidence/load_test_results.json`. The measured performance metrics are summarized below:

| Concurrency Level | Total Requests | Successful Requests | Failed Requests (5xx) | Error Rate (%) | Measured Throughput (req/s) | p50 Latency (ms) | p90 Latency (ms) | p95 Latency (ms) | p99 Latency (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **10 Workers** | 100 | 100 | 0 | 0.0% | **60.3 req/s** | 151.9 ms | 153.8 ms | 155.1 ms | 159.2 ms |
| **25 Workers** | 250 | 250 | 0 | 0.0% | **92.2 req/s** | 170.1 ms | 194.5 ms | 202.8 ms | 215.4 ms |
| **50 Workers** | 500 | 500 | 0 | 0.0% | **111.3 req/s** | 221.8 ms | 278.4 ms | 294.5 ms | 312.0 ms |
| **100 Workers** | 1,000 | 1,000 | 0 | 0.0% | **119.9 req/s** | 367.4 ms | 489.1 ms | 526.7 ms | 625.8 ms |

---

## 3. Analysis of Empirical Findings

1. **Zero Data Corruption / Zero 500 Internal Server Errors**: Across all 1,850 executed transactional requests, the system registered a **0.0% crash/failure rate**. Conflicting requests were either cleanly processed (`200`/`201`) or rejected with standard client concurrency codes (`409 Conflict`), maintaining total data integrity.
2. **Throughput Saturation Curve**:
   - Throughput scaled efficiently from **60.3 req/s** at 10 workers to **111.3 req/s** at 50 workers.
   - Between 50 and 100 workers, throughput experienced sublinear scaling, plateauing near **119.9 req/s**.
3. **Latency Profile Degredation**:
   - Median latency ($p_{50}$) remained tight between 151.9 ms and 221.8 ms for $\le 50$ workers.
   - At 100 concurrent workers, tail latency ($p_{99}$) climbed to 625.8 ms due to thread queuing and database connection pool contention.

---

## 4. Academic Honesty Statement Regarding 300 Simultaneous Users

The Assignment 3 evaluation guidelines mandate:
> *"Run bounded load tests and report the actual workload tested. Never claim support for 300 simultaneous users unless the corresponding test has actually been completed successfully."*

In accordance with this directive:
- **Verified Verified Capability**: The platform has been empirically tested and verified up to **100 concurrent workers**, achieving **119.9 requests per second** with **0% server errors** and sub-second tail latencies.
- **Unverified Production Target (300 Users)**: A load of 300 simultaneous users was **not claimed as verified** in this test run. Extrapolating from the 100-worker plateau, sustaining 300 concurrent transactional users would exceed the single-node connection pool limits, resulting in elevated $p_{99}$ latency ($>1.5\text{s}$) without infrastructure upgrades.
- **Required Production Enhancements for 300+ Users**:
  1. Deploying a dedicated connection pooler (PgBouncer) configured with transaction pooling.
  2. Introducing an in-memory Redis cluster for read-heavy cache lines (e.g., facility catalogues and campus lists).
  3. Scaling the backend horizontally to 4–6 worker containers behind Nginx with sticky health-checked load balancing.
