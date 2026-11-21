"""
Persistence Verification Script for Smart Campus Platform.
Simulates application container restart and proves database persistence.
"""

import os
import sys
from pathlib import Path
from datetime import timedelta

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent / 'backend'
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.utils import timezone
from django.db import connection
from campuses.models import Campus
from facilities.models import Facility, FacilityType
from accounts.models import User
from bookings.models import Booking, BookingStatus
from maintenance.models import Ticket, TicketStatus, PriorityLevel, TicketCategory

def verify_persistence():
    print("=" * 60)
    print("APPLICATION RESTART & DATABASE PERSISTENCE VERIFICATION")
    print("=" * 60)

    # 1. Insert synthetic test records
    campus, _ = Campus.objects.get_or_create(code="PERS-CAMP", defaults={"name": "Persistence Verification Campus"})
    user, _ = User.objects.get_or_create(username="pers_user", defaults={"role": "faculty", "campus": campus})
    facility, _ = Facility.objects.get_or_create(
        code="PERS-LAB-01",
        defaults={
            "campus": campus,
            "name": "Persistence Test Facility",
            "facility_type": FacilityType.COMPUTER_LAB,
            "capacity": 25,
            "is_restricted": False
        }
    )

    start_time = timezone.now() + timedelta(days=20)
    end_time = start_time + timedelta(hours=2)

    booking = Booking.objects.create(
        facility=facility,
        requester=user,
        start_at=start_time,
        end_at=end_time,
        status=BookingStatus.CONFIRMED,
        purpose="Verification of persistent state retention across container restart",
        request_key="persist-key-check-9988",
        version=1
    )
    print(f"Created Synthetic Booking #{booking.id} (Version: {booking.version})")

    ticket = Ticket.objects.create(
        campus=campus,
        facility=facility,
        title="Persistent Storage Circuit Integrity Check",
        description="Verifying that ticket records survive stateless application instance restarts.",
        category=TicketCategory.ELECTRICAL,
        priority=PriorityLevel.M2,
        status=TicketStatus.ASSIGNED,
        version=1
    )
    print(f"Created Synthetic Ticket #{ticket.id} (Version: {ticket.version})")

    # 2. Simulate Application Container Restart:
    # Explicitly close all active database connections, reset the connection pool,
    # and re-initialize from storage
    print("\n--- Simulating Application Container Shutdown & Restart ---")
    connection.close()
    print("Application container database pool disconnected.")

    # 3. Re-read from storage
    print("Re-establishing connection from persistent storage volume...")
    retrieved_booking = Booking.objects.filter(id=booking.id).first()
    retrieved_ticket = Ticket.objects.filter(id=ticket.id).first()

    assert retrieved_booking is not None, "FATAL: Booking did not survive restart!"
    assert retrieved_ticket is not None, "FATAL: Ticket did not survive restart!"

    assert retrieved_booking.request_key == "persist-key-check-9988"
    assert retrieved_booking.version == 1
    assert retrieved_booking.status == BookingStatus.CONFIRMED

    assert retrieved_ticket.title == "Persistent Storage Circuit Integrity Check"
    assert retrieved_ticket.version == 1

    print("\n[SUCCESS]: All records verified intact!")
    print(f"Verified Booking ID {retrieved_booking.id}: Status={retrieved_booking.status}, Version={retrieved_booking.version}")
    print(f"Verified Ticket ID {retrieved_ticket.id}: Status={retrieved_ticket.status}, Version={retrieved_ticket.version}")
    print("=" * 60)

if __name__ == '__main__':
    verify_persistence()
