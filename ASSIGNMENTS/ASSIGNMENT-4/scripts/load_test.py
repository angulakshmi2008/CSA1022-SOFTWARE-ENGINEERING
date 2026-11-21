"""
Bounded load test against the local application using synthetic concurrency.
Collects request counts, success/failure rates, throughput, and latency percentiles.
Outputs genuine CSV execution metrics to docs/evidence/load-test-results.csv.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from datetime import datetime, timezone
import os
import sys
import time
from fastapi.testclient import TestClient

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_DIR)

from app.main import app  # noqa: E402
from app.database import Base, engine  # noqa: E402
from app.security.authentication import create_access_token  # noqa: E402


def execute_request(client, headers, request_id: int):
    t_start = time.perf_counter()
    try:
        if request_id % 3 == 0:
            res = client.get("/health")
        elif request_id % 3 == 1:
            res = client.get("/api/v1/facilities")
        else:
            res = client.get(
                "/api/v1/sensors/threshold-check?value=28.00&threshold=28.0"
            )

        latency = (time.perf_counter() - t_start) * 1000.0  # ms
        success = res.status_code == 200
        return success, latency, res.status_code
    except Exception as e:
        latency = (time.perf_counter() - t_start) * 1000.0
        return False, latency, str(e)


def run_load_test(total_requests: int = 200, concurrency: int = 10):
    print("=" * 60)
    print("STARTING BOUNDED LOAD TEST EXPERIMENT (Q5)")
    print(f"Target: {total_requests} requests | Concurrency: {concurrency} threads")
    print("=" * 60)

    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    token = create_access_token({"sub": "load_test_user", "role": "FACILITY_MANAGER"})
    headers = {"Authorization": f"Bearer {token}"}

    latencies = []
    success_count = 0
    failure_count = 0

    t_experiment_start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [
            executor.submit(execute_request, client, headers, i)
            for i in range(total_requests)
        ]
        for f in as_completed(futures):
            success, lat, status_info = f.result()
            latencies.append(lat)
            if success:
                success_count += 1
            else:
                failure_count += 1

    total_duration = time.perf_counter() - t_experiment_start
    throughput = total_requests / total_duration if total_duration > 0 else 0

    latencies.sort()
    min_lat = min(latencies)
    max_lat = max(latencies)
    mean_lat = sum(latencies) / len(latencies)
    p50 = latencies[int(len(latencies) * 0.50)]
    p95 = latencies[int(len(latencies) * 0.95)]
    p99 = latencies[int(len(latencies) * 0.99)]

    print(f"[+] Total Requests: {total_requests}")
    print(f"[+] Successful: {success_count} ({(success_count/total_requests)*100:.1f}%)")
    print(f"[+] Failed: {failure_count}")
    print(f"[+] Total Duration: {total_duration:.3f} s")
    print(f"[+] Throughput: {throughput:.2f} req/sec")
    print(f"[+] Latency Min: {min_lat:.2f} ms | Mean: {mean_lat:.2f} ms | Max: {max_lat:.2f} ms")
    print(f"[+] Percentiles: p50={p50:.2f} ms | p95={p95:.2f} ms | p99={p99:.2f} ms")

    # Save to CSV
    evidence_dir = os.path.join(PROJECT_DIR, "docs", "evidence")
    os.makedirs(evidence_dir, exist_ok=True)
    csv_path = os.path.join(evidence_dir, "load-test-results.csv")

    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "Timestamp",
            "Total_Requests",
            "Concurrency",
            "Success_Count",
            "Failure_Count",
            "Duration_Seconds",
            "Throughput_RPS",
            "Min_Latency_ms",
            "Mean_Latency_ms",
            "P50_Latency_ms",
            "P95_Latency_ms",
            "P99_Latency_ms",
            "Max_Latency_ms"
        ])
        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            total_requests,
            concurrency,
            success_count,
            failure_count,
            round(total_duration, 4),
            round(throughput, 2),
            round(min_lat, 2),
            round(mean_lat, 2),
            round(p50, 2),
            round(p95, 2),
            round(p99, 2),
            round(max_lat, 2)
        ])

    print(f"[+] Genuine load test results written to {csv_path}")


if __name__ == "__main__":
    run_load_test()
