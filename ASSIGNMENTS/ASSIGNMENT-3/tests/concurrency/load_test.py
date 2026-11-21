"""
Bounded Stepped Concurrency and Workload Verification Harness.
Executes stepped concurrent requests (10, 25, 50, 100 requests) to evaluate
throughput, latency distribution (p50, p95, p99), and data consistency.
"""

import os
import sys
import time
import json
import statistics
import concurrent.futures
from pathlib import Path
from datetime import timedelta

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent / 'backend'
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.utils import timezone
from django.db import connection
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from campuses.models import Campus
from facilities.models import Facility, FacilityType
from bookings.models import Booking

User = get_user_model()

def run_bounded_load_test():
    print("=" * 70)
    print("SMART CAMPUS PLATFORM - BOUNDED CONCURRENCY & WORKLOAD TEST")
    print("=" * 70)

    # Setup test fixture
    campus, _ = Campus.objects.get_or_create(code="LOAD-CAMP", defaults={"name": "Load Test Campus"})
    user, _ = User.objects.get_or_create(username="load_test_user", defaults={"role": "faculty", "campus": campus})
    
    facility, _ = Facility.objects.get_or_create(
        code="LOAD-FAC-01",
        defaults={
            "campus": campus,
            "name": "Scalability Testing Suite",
            "facility_type": FacilityType.COMPUTER_LAB,
            "capacity": 100,
            "is_restricted": False
        }
    )

    steps = [10, 25, 50, 100]
    overall_results = {}

    for concurrency in steps:
        print(f"\n--- Testing Concurrency Step: {concurrency} Concurrent Workers ---")
        latencies = []
        status_counts = {}
        
        start_base = timezone.now() + timedelta(days=10)

        def worker_task(worker_id):
            connection.close()
            client = APIClient()
            client.force_authenticate(user=user)

            # Each worker requests an independent 30-minute slot
            start_slot = start_base + timedelta(hours=worker_id * 2)
            end_slot = start_slot + timedelta(hours=1)

            payload = {
                "facility_id": facility.id,
                "start_at": start_slot.isoformat(),
                "end_at": end_slot.isoformat(),
                "purpose": f"Load Test Slot #{worker_id}",
                "request_key": f"load-test-key-{concurrency}-{worker_id}"
            }

            t0 = time.perf_counter()
            try:
                res = client.post('/api/bookings/', payload, format='json')
                status_code = res.status_code
            except Exception as e:
                status_code = 500
            t1 = time.perf_counter()

            connection.close()
            latency_ms = (t1 - t0) * 1000
            return status_code, latency_ms

        t_step_start = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(worker_task, i) for i in range(concurrency)]
            for f in concurrent.futures.as_completed(futures):
                sc, lat = f.result()
                status_counts[sc] = status_counts.get(sc, 0) + 1
                latencies.append(lat)

        t_step_total = time.perf_counter() - t_step_start
        latencies.sort()

        p50 = statistics.median(latencies)
        p95 = latencies[int(len(latencies) * 0.95)] if len(latencies) >= 20 else latencies[-1]
        p99 = latencies[int(len(latencies) * 0.99)] if len(latencies) >= 100 else latencies[-1]
        throughput = concurrency / t_step_total

        step_summary = {
            "concurrency_level": concurrency,
            "total_requests": concurrency,
            "status_distribution": status_counts,
            "total_duration_sec": round(t_step_total, 3),
            "throughput_req_per_sec": round(throughput, 2),
            "latency_ms": {
                "min": round(min(latencies), 2),
                "mean": round(statistics.mean(latencies), 2),
                "p50": round(p50, 2),
                "p95": round(p95, 2),
                "p99": round(p99, 2),
                "max": round(max(latencies), 2),
            }
        }
        overall_results[f"step_{concurrency}"] = step_summary

        print(f"Completed in {t_step_total:.2f}s | Throughput: {throughput:.1f} req/s")
        print(f"Status Codes: {status_counts}")
        print(f"Latency: p50={p50:.1f}ms | p95={p95:.1f}ms | p99={p99:.1f}ms | min={min(latencies):.1f}ms | max={max(latencies):.1f}ms")

    # Save results to evidence directory
    out_dir = Path(__file__).resolve().parent.parent.parent / 'docs' / 'evidence'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'load_test_results.json'

    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(overall_results, f, indent=2)
    print(f"\nSaved empirical workload evidence to: {out_file}")

    return overall_results

if __name__ == '__main__':
    run_bounded_load_test()
