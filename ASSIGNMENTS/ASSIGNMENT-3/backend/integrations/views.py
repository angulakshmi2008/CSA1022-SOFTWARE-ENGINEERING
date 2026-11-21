from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction

from .models import IntegrationIntent, IntentStatus
from .serializers import IntegrationIntentSerializer
from maintenance.models import Ticket
from audit.models import AuditEvent

class IntegrationIntentViewSet(viewsets.ModelViewSet):
    queryset = IntegrationIntent.objects.select_related('ticket').all()
    serializer_class = IntegrationIntentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Durable Integration Intent creation.
        Enforces idempotency: repeated submissions with identical correlation_key
        return the stored intent rather than duplicating the external action.
        """
        ticket_id = request.data.get('ticket_id') or request.data.get('ticket')
        operation = request.data.get('operation', 'create_developer_issue')
        correlation_key = request.data.get('correlation_key')

        if not ticket_id or not correlation_key:
            return Response({
                "error": "Both 'ticket_id' and 'correlation_key' are required fields."
            }, status=status.HTTP_400_BAD_REQUEST)

        # 1. Idempotency Check & Reconciliation
        existing = IntegrationIntent.objects.filter(correlation_key=correlation_key).first()
        if existing:
            return Response(
                IntegrationIntentSerializer(existing).data,
                status=status.HTTP_200_OK
            )

        ticket = Ticket.objects.filter(id=ticket_id).first()
        if not ticket:
            return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            intent = IntegrationIntent.objects.create(
                ticket=ticket,
                operation=operation,
                correlation_key=correlation_key,
                status=IntentStatus.PENDING,
                attempts=1,
                last_attempt_at=timezone.now()
            )

            # Synchronous / Near-line execution simulation for the demonstration workflow
            # Generates a tracked GitHub/Jira Issue representation
            intent.external_id = f"GH-ISSUE-{ticket.id}-DEV"
            intent.status = IntentStatus.CONFIRMED
            intent.save()

            AuditEvent.objects.create(
                actor=request.user,
                entity_type="IntegrationIntent",
                entity_id=intent.id,
                action="DISPATCH_INTEGRATION_INTENT",
                before_state=None,
                after_state={
                    "correlation_key": correlation_key,
                    "external_id": intent.external_id,
                    "status": intent.status
                },
                ip_address=request.META.get('REMOTE_ADDR')
            )

        return Response(IntegrationIntentSerializer(intent).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        """Safe retry endpoint reconciling durable state."""
        intent = self.get_object()
        intent.attempts += 1
        intent.last_attempt_at = timezone.now()
        intent.status = IntentStatus.CONFIRMED
        if not intent.external_id:
            intent.external_id = f"GH-ISSUE-{intent.ticket_id}-RETRY"
        intent.save()

        return Response(IntegrationIntentSerializer(intent).data, status=status.HTTP_200_OK)
