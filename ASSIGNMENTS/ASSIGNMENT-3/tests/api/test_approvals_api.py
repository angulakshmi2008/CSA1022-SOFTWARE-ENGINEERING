import pytest
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
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from campuses.models import Campus
from facilities.models import Facility, FacilityType
from bookings.models import Booking, BookingStatus
from approvals.models import Approval, RequestType, ApprovalDecision
from audit.models import AuditEvent

User = get_user_model()

@pytest.mark.django_db(transaction=True)
class TestApprovalsAPI:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.client = APIClient()
        self.campus, _ = Campus.objects.get_or_create(code="BIO-CAMP", defaults={"name": "Medical Campus"})
        self.approver, _ = User.objects.get_or_create(username="approver_dean", defaults={"role": "department_approver", "campus": self.campus})
        self.student, _ = User.objects.get_or_create(username="student_eve", defaults={"role": "student", "campus": self.campus})
        self.faculty, _ = User.objects.get_or_create(username="dr_anand", defaults={"role": "faculty", "campus": self.campus})

        self.restricted_lab, _ = Facility.objects.get_or_create(
            code="BIO-304",
            defaults={
                "campus": self.campus,
                "name": "Biosafety Containment Lab",
                "facility_type": FacilityType.RESEARCH_LAB,
                "capacity": 12,
                "is_restricted": True
            }
        )

        start = timezone.now() + timedelta(days=2)
        end = start + timedelta(hours=3)
        self.pending_booking = Booking.objects.create(
            facility=self.restricted_lab,
            requester=self.faculty,
            start_at=start,
            end_at=end,
            status=BookingStatus.REQUESTED,
            purpose="Pathogen culture analysis protocol"
        )

    def test_01_student_attempt_approval_forbidden(self):
        """US03 Negative Case: Student attempting to approve receives HTTP 403 Forbidden."""
        self.client.force_authenticate(user=self.student)
        payload = {
            "request_type": RequestType.BOOKING,
            "request_id": self.pending_booking.id,
            "decision": ApprovalDecision.APPROVED,
            "reason": "Student self-approval attempt."
        }
        response = self.client.post('/api/approvals/', payload, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['code'] == 'INSUFFICIENT_APPROVAL_PERMISSIONS'

        # Target booking must still be in 'requested' state
        self.pending_booking.refresh_from_db()
        assert self.pending_booking.status == BookingStatus.REQUESTED

    def test_02_authorized_approver_decision_success(self):
        """US03 Positive Case: Department Approver records decision with justification."""
        self.client.force_authenticate(user=self.approver)
        payload = {
            "request_type": RequestType.BOOKING,
            "request_id": self.pending_booking.id,
            "decision": ApprovalDecision.APPROVED,
            "reason": "Departmental Biosafety Protocol BSL-3 verified and approved."
        }
        response = self.client.post('/api/approvals/', payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['decision'] == ApprovalDecision.APPROVED

        # Target booking transitions to confirmed
        self.pending_booking.refresh_from_db()
        assert self.pending_booking.status == BookingStatus.CONFIRMED

        # AuditEvent is recorded
        assert AuditEvent.objects.filter(entity_type="Approval", action="DECIDE_APPROVAL").exists()
