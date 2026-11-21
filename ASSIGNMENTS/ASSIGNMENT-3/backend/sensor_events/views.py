from rest_framework import views, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction, IntegrityError
import hashlib

from .models import SensorEvent
from .serializers import SensorEventSerializer, SensorEventIngestSerializer
from maintenance.models import Ticket, TicketSource, TicketStatus
from maintenance.triage_engine import triage_ticket
from facilities.models import Facility
from campuses.models import Campus
from audit.models import AuditEvent
from config.policies import SENSOR_THRESHOLDS

class SensorEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SensorEvent.objects.select_related('ticket').order_by('-processed_at')
    serializer_class = SensorEventSerializer
    permission_classes = [IsAuthenticated]

class SensorEventIngestView(views.APIView):
    """
    Controlled sensor event intake endpoint.
    Guarantees:
    1. Idempotent deduplication on (source_id, event_id).
    2. Threshold evaluation and automatic ticket creation inside ACID transaction.
    3. Audit logging of telemetry alert events.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SensorEventIngestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        source_id = serializer.validated_data['source_id']
        event_id = serializer.validated_data['event_id']
        metric = serializer.validated_data['metric']
        value = serializer.validated_data['value']
        observed_at = serializer.validated_data['observed_at']
        facility_id = serializer.validated_data.get('facility_id')
        campus_id = serializer.validated_data.get('campus_id')

        # 1. Deduplication check: Has this physical event already been ingested?
        existing_event = SensorEvent.objects.filter(source_id=source_id, event_id=event_id).first()
        if existing_event:
            return Response({
                "status": "duplicate_suppressed",
                "source_id": source_id,
                "event_id": event_id,
                "message": "Duplicate telemetry event suppressed; event previously recorded.",
                "existing_ticket_id": existing_event.ticket_id
            }, status=status.HTTP_200_OK)

        # 2. Threshold evaluation
        is_breach = False
        threshold_info = ""

        if metric == 'temperature_celsius':
            limits = SENSOR_THRESHOLDS['temperature_celsius']
            if value >= limits['high_warning']:
                is_breach = True
                threshold_info = f"High temperature alert: {value}°C exceeds warning threshold {limits['high_warning']}°C"
        elif metric == 'vibration_hz':
            limits = SENSOR_THRESHOLDS['vibration_hz']
            if value >= limits['high_warning']:
                is_breach = True
                threshold_info = f"Abnormal mechanical vibration: {value} Hz exceeds threshold {limits['high_warning']} Hz"

        # Resolve campus and facility
        facility = None
        campus = None
        if facility_id:
            facility = Facility.objects.filter(id=facility_id).first()
            if facility:
                campus = facility.campus
        if not campus and campus_id:
            campus = Campus.objects.filter(id=campus_id).first()
        if not campus:
            campus = Campus.objects.filter(is_active=True).first()

        ticket = None
        try:
            with transaction.atomic():
                if is_breach and campus:
                    title = f"Telemetry Alert: {metric.replace('_', ' ').title()} breach on {source_id}"
                    description = (
                        f"Automated alert detected from sensor device {source_id}.\n"
                        f"Observed value: {value} {metric}.\n"
                        f"Details: {threshold_info}\n"
                        f"Timestamp: {observed_at}"
                    )

                    cat, priority, sla_due_at, explanation = triage_ticket(
                        title=title,
                        description=description,
                        impact='high',
                        urgency='high'
                    )

                    ticket = Ticket.objects.create(
                        campus=campus,
                        facility=facility,
                        source=TicketSource.SENSOR_EVENT,
                        title=title,
                        description=description,
                        category=cat,
                        impact='high',
                        urgency='high',
                        priority=priority,
                        triage_explanation=explanation,
                        status=TicketStatus.TRIAGED,
                        sla_due_at=sla_due_at,
                        version=1
                    )

                event = SensorEvent.objects.create(
                    source_id=source_id,
                    event_id=event_id,
                    metric=metric,
                    value=value,
                    observed_at=observed_at,
                    ticket=ticket
                )

                if ticket:
                    actor = request.user if request.user.is_authenticated else None
                    AuditEvent.objects.create(
                        actor=actor,
                        entity_type="SensorEvent",
                        entity_id=event.id,
                        action="BREACH_TRIGGERED_TICKET",
                        before_state=None,
                        after_state={
                            "source_id": source_id,
                            "metric": metric,
                            "value": value,
                            "ticket_id": ticket.id,
                            "priority": ticket.priority
                        },
                        ip_address=request.META.get('REMOTE_ADDR')
                    )

        except IntegrityError:
            # Handle concurrent race condition on duplicate event_id
            existing = SensorEvent.objects.filter(source_id=source_id, event_id=event_id).first()
            return Response({
                "status": "duplicate_suppressed",
                "source_id": source_id,
                "event_id": event_id,
                "message": "Duplicate telemetry event suppressed via unique constraint.",
                "existing_ticket_id": existing.ticket_id if existing else None
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "processed",
            "source_id": source_id,
            "event_id": event_id,
            "threshold_breached": is_breach,
            "ticket_created": ticket is not None,
            "ticket_id": ticket.id if ticket else None,
            "priority": ticket.priority if ticket else None,
            "triage_summary": ticket.triage_explanation if ticket else "Telemetry recorded within nominal operating limits."
        }, status=status.HTTP_201_CREATED)
