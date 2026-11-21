"""
Concurrency Test: Two technicians submit conflicting updates to the same ticket.
Validates:
1. First update succeeds (HTTP 200 OK), incrementing ticket version from 1 to 2.
2. Second update using stale expected_version=1 is rejected with HTTP 409 Conflict.
3. Database retains first accepted update without silent overwrite.
"""

import pytest
import os
import sys
import threading
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent / 'backend'
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.db import connection
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from campuses.models import Campus
from maintenance.models import Ticket, TicketStatus, PriorityLevel, TicketCategory

User = get_user_model()

@pytest.mark.django_db(transaction=True)
def test_conflicting_ticket_updates():
    campus, _ = Campus.objects.get_or_create(code="TKT-CONC", defaults={"name": "Ticket Concurrency Campus"})
    tech1, _ = User.objects.get_or_create(username="tech_alpha", defaults={"role": "technician", "campus": campus})
    tech2, _ = User.objects.get_or_create(username="tech_bravo", defaults={"role": "technician", "campus": campus})

    ticket = Ticket.objects.create(
        campus=campus,
        title="Centrifugal Water Pump Bearing Noise",
        description="Vibration detected in basement pump 2.",
        category=TicketCategory.PLUMBING,
        priority=PriorityLevel.M2,
        status=TicketStatus.IN_PROGRESS,
        version=1
    )

    results = []

    def technician_update(tech, notes, expected_ver):
        connection.close()
        client = APIClient()
        client.force_authenticate(user=tech)

        payload = {
            "target_state": TicketStatus.RESOLVED,
            "expected_version": expected_ver,
            "resolution_notes": notes
        }

        res = client.patch(f'/api/tickets/{ticket.id}/state/', payload, format='json')
        results.append({
            "tech": tech.username,
            "status_code": res.status_code,
        })
        connection.close()

    # Step 1: Technician 1 reads version 1 and submits valid resolution
    technician_update(tech1, "Replaced worn front roller bearing and lubricated seal assembly.", 1)
    
    # Step 2: Technician 2 (who also read version 1) submits conflicting resolution with stale version 1
    technician_update(tech2, "Tightened motor mount bolts; motor alignment completed.", 1)

    status_codes = [r['status_code'] for r in results]
    print(f"\n[Observed Conflicting Ticket Update Results]: {status_codes}")

    assert status_codes[0] == status.HTTP_200_OK, "Winning update must receive HTTP 200 OK"
    assert status_codes[1] == status.HTTP_409_CONFLICT, "Stale concurrent update must receive HTTP 409 Conflict"

    ticket.refresh_from_db()
    assert ticket.version == 2, f"Final ticket version must be exactly 2, but found {ticket.version}"
    assert ticket.status == TicketStatus.RESOLVED
