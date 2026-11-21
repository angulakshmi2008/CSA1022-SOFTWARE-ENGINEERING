import pytest
import os
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent / 'backend'
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from campuses.models import Campus
from sensor_events.models import SensorEvent
from maintenance.models import Ticket

@pytest.mark.django_db(transaction=True)
class TestSensorEventsAPI:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.client = APIClient()
        self.campus, _ = Campus.objects.get_or_create(code="SENS-CAMP", defaults={"name": "Sensor Test Campus"})

    def test_01_sensor_duplicate_suppression_5_times(self):
        """US04: Same source/event ID sent 5 times produces exactly 1 ticket and duplicate acknowledgements."""
        event_uuid = f"evt-idempotent-{timezone.now().timestamp()}"
        payload = {
            "source_id": "HVAC-TEMP-UNIT-04",
            "event_id": event_uuid,
            "metric": "temperature_celsius",
            "value": 31.8, # Critical breach > 26.0
            "observed_at": timezone.now().isoformat(),
            "campus_id": self.campus.id
        }

        # 1st Submission: Must create event and 1 ticket
        r1 = self.client.post('/api/sensor-events/', payload, format='json')
        assert r1.status_code == status.HTTP_201_CREATED
        assert r1.data['status'] == 'processed'
        assert r1.data['ticket_created'] is True
        created_ticket_id = r1.data['ticket_id']
        assert created_ticket_id is not None

        # 2nd through 5th Submissions: Must be suppressed as duplicates
        for i in range(2, 6):
            r_dup = self.client.post('/api/sensor-events/', payload, format='json')
            assert r_dup.status_code == status.HTTP_200_OK
            assert r_dup.data['status'] == 'duplicate_suppressed'
            assert r_dup.data['existing_ticket_id'] == created_ticket_id

        # Verify persistent state in database
        event_count = SensorEvent.objects.filter(source_id="HVAC-TEMP-UNIT-04", event_id=event_uuid).count()
        assert event_count == 1, "Exactly one SensorEvent row must exist"

        ticket_count = Ticket.objects.filter(sensor_events__event_id=event_uuid).count()
        assert ticket_count == 1, "Exactly one Ticket must be linked to the sensor event"

    def test_02_normal_telemetry_no_ticket(self):
        """Nominal sensor telemetry (e.g. 21.5°C) is recorded without spawning tickets."""
        event_uuid = f"evt-nominal-{timezone.now().timestamp()}"
        payload = {
            "source_id": "HVAC-TEMP-ROOM-102",
            "event_id": event_uuid,
            "metric": "temperature_celsius",
            "value": 21.5,
            "observed_at": timezone.now().isoformat(),
            "campus_id": self.campus.id
        }
        response = self.client.post('/api/sensor-events/', payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['ticket_created'] is False
        assert SensorEvent.objects.filter(event_id=event_uuid).exists()
