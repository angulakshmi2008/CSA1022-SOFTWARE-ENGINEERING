"""
Smoke test suite for deployed application verification and release gates.
Validates service readiness, health probe, sensor threshold evaluation, and API smoke journey.
"""

from datetime import datetime, timezone
import os
import sys
import time
from fastapi.testclient import TestClient

# Ensure app is importable
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_DIR)

from app.main import app  # noqa: E402
from app.database import SessionLocal, Base, engine  # noqa: E402
from app.models.user import User, UserRole  # noqa: E402
from app.models.facility import Facility  # noqa: E402
from app.security.authentication import hash_password, create_access_token  # noqa: E402


def run_smoke_tests():
    evidence_dir = os.path.join(PROJECT_DIR, "docs", "evidence")
    os.makedirs(evidence_dir, exist_ok=True)
    log_file = os.path.join(evidence_dir, "smoke-test.log")

    log_lines = []

    def log(msg):
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        formatted = f"[{timestamp}] {msg}"
        print(formatted)
        log_lines.append(formatted)

    log("=== SMART CAMPUS PLATFORM SMOKE TEST EXECUTION ===")
    start_time = time.time()

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Seed smoke test user if needed
    smoke_user = db.query(User).filter(User.username == "smoke_admin").first()
    if not smoke_user:
        smoke_user = User(
            username="smoke_admin",
            email="smoke_admin@campus.edu",
            full_name="Smoke Test Admin",
            role=UserRole.ADMINISTRATOR,
            department="DevOps Validation",
            hashed_password=hash_password("SmokeAdminSecret123!"),
            is_active=True,
        )
        db.add(smoke_user)
        db.commit()
        db.refresh(smoke_user)
        log("Seeded smoke_admin test user")

    # Seed smoke facility
    smoke_fac = db.query(Facility).filter(Facility.code == "SMOKE-LAB-01").first()
    if not smoke_fac:
        smoke_fac = Facility(
            code="SMOKE-LAB-01",
            name="Smoke Test Validation Lab",
            campus="Main Campus",
            building="DevOps Block",
            room_number="D01",
            facility_type="Lab",
            capacity=25,
            is_restricted=False,
        )
        db.add(smoke_fac)
        db.commit()
        db.refresh(smoke_fac)
        log("Seeded SMOKE-LAB-01 test facility")

    db.close()

    token = create_access_token({"sub": "smoke_admin", "role": "ADMINISTRATOR"})
    auth_headers = {"Authorization": f"Bearer {token}"}

    client = TestClient(app)

    # 1. Health Probe
    log("Step 1: Checking /health readiness and liveness probe...")
    res = client.get("/health")
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    health_data = res.json()
    assert health_data["status"] == "UP"
    assert health_data["database"] == "healthy"
    log(f"-> Health check PASSED: status={health_data['status']}, db={health_data['database']}")

    # 2. Facilities list
    log("Step 2: Testing facility retrieval /api/v1/facilities...")
    res = client.get("/api/v1/facilities")
    assert res.status_code == 200
    facilities = res.json()
    assert len(facilities) >= 1
    log(f"-> Facilities catalog PASSED: retrieved {len(facilities)} facilities")

    # 3. Sensor threshold check (28.00 and 28.01)
    log("Step 3: Testing strict greater-than threshold /api/v1/sensors/threshold-check...")
    res_28_00 = client.get("/api/v1/sensors/threshold-check?value=28.00&threshold=28.0")
    assert res_28_00.status_code == 200
    assert res_28_00.json()["breached"] is False, "28.00 must not breach threshold"

    res_28_01 = client.get("/api/v1/sensors/threshold-check?value=28.01&threshold=28.0")
    assert res_28_01.status_code == 200
    assert res_28_01.json()["breached"] is True, "28.01 must breach threshold"
    log("-> Threshold validation PASSED: 28.00 -> False, 28.01 -> True")

    # 4. Authenticated profile check
    log("Step 4: Testing authenticated endpoint /api/v1/auth/me...")
    res = client.get("/api/v1/auth/me", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["username"] == "smoke_admin"
    log("-> Authenticated access PASSED: user identity verified")

    duration = time.time() - start_time
    log(f"=== ALL SMOKE TESTS COMPLETED SUCCESSFULLY IN {duration:.3f} SECONDS ===")

    with open(log_file, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")
    print(f"[+] Smoke test log saved to {log_file}")


if __name__ == "__main__":
    run_smoke_tests()
