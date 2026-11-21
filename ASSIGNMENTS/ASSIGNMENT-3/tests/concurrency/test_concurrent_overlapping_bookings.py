"""
Concurrency Test: Two users attempt to reserve the same laboratory for overlapping time slots.
Validates:
1. One request succeeds (HTTP 201 Created).
2. The losing concurrent request is rejected with HTTP 409 Conflict.
3. Total persistent active booking rows for that slot equals exactly 1.
"""

import pytest
import os
import sys
import threading
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
from rest_framework import status
from django.contrib.auth import get_user_model
from campuses.models import Campus
from facilities.models import Facility, FacilityType
from bookings.models import Booking, BookingStatus

User = get_user_model()

@pytest.mark.django_db(transaction=True)
def test_concurrent_overlapping_bookings_exact_two():
    campus, _ = Campus.objects.get_or_create(code="CONC-CAMP", defaults={"name": "Concurrency Lab Campus"})
    user1, _ = User.objects.get_or_create(username="user_alpha", defaults={"role": "faculty", "campus": campus})
    user2, _ = User.objects.get_or_create(username="user_beta", defaults={"role": "faculty", "campus": campus})

    facility, _ = Facility.objects.get_or_create(
        code="ENG-HPC-01",
        defaults={
            "campus": campus,
            "name": "High Performance Computing Center",
            "facility_type": FacilityType.COMPUTER_LAB,
            "capacity": 50,
            "is_restricted": False
        }
    )

    start_time = timezone.now() + timedelta(days=5, hours=10)
    end_time = start_time + timedelta(hours=2)

    results = []
    barrier = threading.Barrier(2)

    def attempt_booking(user, req_key):
        connection.close()
        client = APIClient()
        client.force_authenticate(user=user)

        payload = {
            "facility_id": facility.id,
            "start_at": start_time.isoformat(),
            "end_at": end_time.isoformat(),
            "purpose": f"Concurrent Practical Booking by {user.username}",
            "request_key": req_key
        }

        # Synchronize release at the exact same instant
        barrier.wait()
        res = client.post('/api/bookings/', payload, format='json')
        results.append({
            "user": user.username,
            "status_code": res.status_code,
        })
        connection.close()

    t1 = threading.Thread(target=attempt_booking, args=(user1, "conc-slot-req-001"))
    t2 = threading.Thread(target=attempt_booking, args=(user2, "conc-slot-req-002"))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    status_codes = [r['status_code'] for r in results]
    print(f"\n[Observed Concurrent Booking Results]: {status_codes}")

    # Exactly one request must succeed (201) and exactly one must be rejected with Conflict (409)
    assert status.HTTP_201_CREATED in status_codes, "At least one booking must succeed"
    assert status.HTTP_409_CONFLICT in status_codes, "The overlapping booking must be rejected with 409 Conflict"
    assert len(status_codes) == 2

    # Database verification
    active_count = Booking.objects.filter(
        facility=facility,
        status__in=[BookingStatus.CONFIRMED, BookingStatus.APPROVED, BookingStatus.REQUESTED],
        start_at__lt=end_time,
        end_at__gt=start_time
    ).count()
    assert active_count == 1, f"Database must contain exactly 1 active reservation, but found {active_count}"
