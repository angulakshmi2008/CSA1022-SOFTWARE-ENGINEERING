import pytest
import os
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent / 'backend'
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from campuses.models import Campus
from maintenance.models import Ticket, TicketStatus, PriorityLevel, TicketCategory

User = get_user_model()

@pytest.mark.django_db(transaction=True)
class TestTicketsAPI:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.client = APIClient()
        self.campus, _ = Campus.objects.get_or_create(code="ENG-TEST", defaults={"name": "Engineering Campus"})
        self.manager, _ = User.objects.get_or_create(username="mgr_priya", defaults={"role": "facility_manager", "campus": self.campus})
        self.technician, _ = User.objects.get_or_create(username="tech_raj", defaults={"role": "technician", "campus": self.campus})
        self.student, _ = User.objects.get_or_create(username="student_sam", defaults={"role": "student", "campus": self.campus})

        self.ticket = Ticket.objects.create(
            campus=self.campus,
            title="Severe Water Pipe Leak in Chemistry Lab",
            description="High pressure pipe burst under sink 4, water flooding floor.",
            category=TicketCategory.PLUMBING,
            impact="high",
            urgency="high",
            priority=PriorityLevel.M1,
            triage_explanation="Matched 'leak', 'pipe', 'water' -> Plumbing. Priority M1 Critical.",
            status=TicketStatus.ASSIGNED,
            assignee=self.technician,
            version=1
        )

    def test_01_explainable_triage_creation(self):
        """Ticket created via API is triaged with explainable rationale."""
        self.client.force_authenticate(user=self.manager)
        payload = {
            "campus": self.campus.id,
            "title": "Air conditioning unit blowing warm air",
            "description": "Temperature in server room rising, chiller unit fan stopped.",
            "impact": "high",
            "urgency": "medium"
        }
        response = self.client.post('/api/tickets/', payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['category'] == 'hvac'
        assert response.data['priority'] == 'M2'
        assert "Explainable Triage Engine" in response.data['triage_explanation']

    def test_02_rejection_of_closure_without_resolution_notes(self):
        """US05: Attempting ticket resolution/closure without required notes returns HTTP 422."""
        self.client.force_authenticate(user=self.technician)
        
        # Technician attempts transition to 'resolved' with empty notes
        payload = {
            "target_state": TicketStatus.RESOLVED,
            "expected_version": 1,
            "resolution_notes": ""
        }
        response = self.client.patch(f'/api/tickets/{self.ticket.id}/state/', payload, format='json')
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert 'resolution_notes' in response.data.get('details', {})

        # Ticket must remain in its previous state
        self.ticket.refresh_from_db()
        assert self.ticket.status == TicketStatus.ASSIGNED

    def test_03_successful_authorized_closure_with_notes(self):
        """Technician resolves with evidence, then Manager verifies and closes."""
        self.client.force_authenticate(user=self.technician)
        
        # Step 1: Technician transitions to resolved
        res_payload = {
            "target_state": TicketStatus.RESOLVED,
            "expected_version": 1,
            "resolution_notes": "Isolated water isolation valve #12, replaced cracked coupling with copper compression joint. Pressure tested to 45 PSI."
        }
        r1 = self.client.patch(f'/api/tickets/{self.ticket.id}/state/', res_payload, format='json')
        assert r1.status_code == status.HTTP_200_OK
        assert r1.data['status'] == TicketStatus.RESOLVED
        assert r1.data['version'] == 2

        # Step 2: Manager closes ticket
        self.client.force_authenticate(user=self.manager)
        close_payload = {
            "target_state": TicketStatus.CLOSED,
            "expected_version": 2,
            "resolution_notes": "Site inspection confirmed dry flooring. Closed work order."
        }
        r2 = self.client.patch(f'/api/tickets/{self.ticket.id}/state/', close_payload, format='json')
        assert r2.status_code == status.HTTP_200_OK
        assert r2.data['status'] == TicketStatus.CLOSED
        assert r2.data['version'] == 3

    def test_04_stale_version_update_rejected(self):
        """Optimistic locking rejects update with stale expected_version with HTTP 409."""
        self.client.force_authenticate(user=self.technician)
        
        # Someone else already bumped version to 2
        self.ticket.version = 2
        self.ticket.status = TicketStatus.IN_PROGRESS
        self.ticket.save()

        # Stale request still expects version 1
        payload = {
            "target_state": TicketStatus.RESOLVED,
            "expected_version": 1,
            "resolution_notes": "Work completed."
        }
        response = self.client.patch(f'/api/tickets/{self.ticket.id}/state/', payload, format='json')
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data['code'] == 'STALE_VERSION_CONFLICT'
        assert response.data['current_version'] == 2
