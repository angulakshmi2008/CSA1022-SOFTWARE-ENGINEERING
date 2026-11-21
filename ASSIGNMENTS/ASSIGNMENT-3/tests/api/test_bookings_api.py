import pytest
import os
import sys
from datetime import timedelta
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent / 'backend'
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from campuses.models import Campus
from facilities.models import Facility, FacilityType
from bookings.models import Booking, BookingStatus

User = get_user_model()

@pytest.mark.django_db(transaction=True)
class TestBookingsAPI:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.client = APIClient()
        self.campus, _ = Campus.objects.get_or_create(code="TEST", defaults={"name": "Test Campus"})
        self.faculty, _ = User.objects.get_or_create(username="prof_x", defaults={"role": "faculty", "campus": self.campus})
        self.student, _ = User.objects.get_or_create(username="student_y", defaults={"role": "student", "campus": self.campus})
        
        self.regular_fac, _ = Facility.objects.get_or_create(
            code="LAB-A",
            defaults={
                "campus": self.campus, "name": "Lab A",
                "facility_type": FacilityType.COMPUTER_LAB, "capacity": 40, "is_restricted": False
            }
        )
        self.restricted_fac, _ = Facility.objects.get_or_create(
            code="BIO-SEC",
            defaults={
                "campus": self.campus, "name": "Bio Lab",
                "facility_type": FacilityType.RESEARCH_LAB, "capacity": 10, "is_restricted": True
            }
        )

    def test_01_valid_booking_creation(self):
        """US01: Faculty books a free laboratory slot, receiving 201 Created and version 1."""
        self.client.force_authenticate(user=self.faculty)
        start = timezone.now() + timedelta(days=1, hours=2)
        end = start + timedelta(hours=2)

        payload = {
            "facility_id": self.regular_fac.id,
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "purpose": "Machine Learning Lab Session",
            "request_key": "test-key-001"
        }
        response = self.client.post('/api/bookings/', payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['version'] == 1
        assert response.data['status'] == BookingStatus.CONFIRMED
        assert Booking.objects.filter(id=response.data['id']).exists()

    def test_02_overlapping_booking_rejection(self):
        """US02: Second overlapping reservation for same facility is rejected with HTTP 409."""
        self.client.force_authenticate(user=self.faculty)
        start1 = timezone.now() + timedelta(days=2, hours=4)
        end1 = start1 + timedelta(hours=2)

        # First booking succeeds
        r1 = self.client.post('/api/bookings/', {
            "facility_id": self.regular_fac.id,
            "start_at": start1.isoformat(),
            "end_at": end1.isoformat(),
            "purpose": "Initial Booking",
            "request_key": "slot-001"
        }, format='json')
        assert r1.status_code == status.HTTP_201_CREATED

        # Second booking overlaps
        start2 = start1 + timedelta(hours=1)
        end2 = start2 + timedelta(hours=2)
        r2 = self.client.post('/api/bookings/', {
            "facility_id": self.regular_fac.id,
            "start_at": start2.isoformat(),
            "end_at": end2.isoformat(),
            "purpose": "Conflicting Booking Attempt",
            "request_key": "slot-002"
        }, format='json')
        
        assert r2.status_code == status.HTTP_409_CONFLICT
        assert r2.data['code'] == 'OVERLAPPING_RESERVATION'

    def test_03_student_restricted_facility_access_denied(self):
        """Student attempting to book restricted facility receives HTTP 403 Forbidden."""
        self.client.force_authenticate(user=self.student)
        start = timezone.now() + timedelta(days=3)
        end = start + timedelta(hours=2)

        response = self.client.post('/api/bookings/', {
            "facility_id": self.restricted_fac.id,
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "purpose": "Unauthorized Student Project"
        }, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['code'] == 'RESTRICTED_FACILITY_ACCESS'

    def test_04_half_open_interval_boundary_no_conflict(self):
        """A booking ending at 12:00 and another starting at 12:00 do not overlap."""
        self.client.force_authenticate(user=self.faculty)
        start1 = timezone.now() + timedelta(days=4, hours=10)
        end1 = start1 + timedelta(hours=2) # 10:00 to 12:00
        start2 = end1                      # 12:00 to 14:00
        end2 = start2 + timedelta(hours=2)

        r1 = self.client.post('/api/bookings/', {
            "facility_id": self.regular_fac.id,
            "start_at": start1.isoformat(),
            "end_at": end1.isoformat(),
            "purpose": "Slot 1"
        }, format='json')
        assert r1.status_code == status.HTTP_201_CREATED

        r2 = self.client.post('/api/bookings/', {
            "facility_id": self.regular_fac.id,
            "start_at": start2.isoformat(),
            "end_at": end2.isoformat(),
            "purpose": "Slot 2 (Adjacent)"
        }, format='json')
        assert r2.status_code == status.HTTP_201_CREATED
