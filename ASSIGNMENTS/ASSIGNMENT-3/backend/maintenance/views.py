from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone

from .models import Ticket, InspectionComment, SLAPolicy, TicketStatus
from .serializers import (
    TicketSerializer,
    TicketCreateSerializer,
    TicketStateTransitionSerializer,
    InspectionCommentSerializer,
    SLAPolicySerializer
)
from audit.models import AuditEvent
from accounts.models import User

# Permitted state transition map
PERMITTED_TRANSITIONS = {
    TicketStatus.INTAKE: [TicketStatus.TRIAGED, TicketStatus.REJECTED],
    TicketStatus.TRIAGED: [TicketStatus.ASSIGNED, TicketStatus.IN_PROGRESS, TicketStatus.REJECTED],
    TicketStatus.ASSIGNED: [TicketStatus.IN_PROGRESS, TicketStatus.TRIAGED, TicketStatus.RESOLVED],
    TicketStatus.IN_PROGRESS: [TicketStatus.INSPECTION, TicketStatus.PENDING_APPROVAL, TicketStatus.RESOLVED],
    TicketStatus.INSPECTION: [TicketStatus.IN_PROGRESS, TicketStatus.PENDING_APPROVAL, TicketStatus.RESOLVED],
    TicketStatus.PENDING_APPROVAL: [TicketStatus.IN_PROGRESS, TicketStatus.REJECTED],
    TicketStatus.RESOLVED: [TicketStatus.CLOSED, TicketStatus.IN_PROGRESS],
    TicketStatus.REJECTED: [TicketStatus.CLOSED],
    TicketStatus.CLOSED: []  # Terminal state
}

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related('campus', 'facility', 'assignee').prefetch_related('comments').all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return TicketCreateSerializer
        return TicketSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        campus = self.request.query_params.get('campus')
        priority = self.request.query_params.get('priority')
        status_filter = self.request.query_params.get('status')
        category = self.request.query_params.get('category')
        assigned_to_me = self.request.query_params.get('assigned_to_me')

        if campus:
            qs = qs.filter(campus_id=campus)
        if priority:
            qs = qs.filter(priority=priority)
        if status_filter:
            qs = qs.filter(status=status_filter)
        if category:
            qs = qs.filter(category=category)
        if assigned_to_me and assigned_to_me.lower() in ('true', '1'):
            qs = qs.filter(assignee=user)

        if user.role == 'technician' and not campus:
            if user.campus:
                qs = qs.filter(campus=user.campus)

        return qs

    def create(self, request, *args, **kwargs):
        serializer = TicketCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()

        AuditEvent.objects.create(
            actor=request.user,
            entity_type="Ticket",
            entity_id=ticket.id,
            action="CREATE_TICKET",
            before_state=None,
            after_state={
                "id": ticket.id,
                "title": ticket.title,
                "priority": ticket.priority,
                "category": ticket.category,
                "status": ticket.status,
                "version": ticket.version
            },
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='state')
    def update_state(self, request, pk=None):
        ticket = self.get_object()
        serializer = TicketStateTransitionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "error": "Validation Error",
                "details": serializer.errors,
                "code": "RESOLUTION_EVIDENCE_REQUIRED"
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        target_state = serializer.validated_data['target_state']
        expected_version = serializer.validated_data['expected_version']
        inspection_notes = serializer.validated_data.get('inspection_notes', '')
        resolution_notes = serializer.validated_data.get('resolution_notes', '')
        is_restricted_change = serializer.validated_data.get('is_restricted_change')

        # 1. Optimistic Concurrency Control Check
        if ticket.version != expected_version:
            return Response({
                "error": "Concurrent Modification Conflict",
                "detail": f"Ticket #{ticket.id} was modified concurrently. "
                          f"Expected version {expected_version}, but persistent version is {ticket.version}.",
                "current_version": ticket.version,
                "code": "STALE_VERSION_CONFLICT"
            }, status=status.HTTP_409_CONFLICT)

        # 2. Lifecycle Transition Invariant
        valid_targets = PERMITTED_TRANSITIONS.get(ticket.status, [])
        if target_state != ticket.status and target_state not in valid_targets:
            return Response({
                "error": "Illegal State Transition",
                "detail": f"Cannot transition ticket directly from '{ticket.status}' to '{target_state}'. "
                          f"Permitted next states: {valid_targets}",
                "code": "ILLEGAL_STATE_TRANSITION"
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 3. Role Authorization
        user = request.user
        if target_state == TicketStatus.CLOSED:
            if user.role not in ['facility_manager', 'administrator']:
                return Response({
                    "error": "Unauthorized",
                    "detail": "Only Facility Managers and Administrators possess authority to verify and close tickets.",
                    "code": "AUTHORIZATION_REQUIRED"
                }, status=status.HTTP_403_FORBIDDEN)

        old_status = ticket.status
        old_version = ticket.version

        with transaction.atomic():
            ticket.status = target_state
            ticket.version += 1
            if resolution_notes:
                ticket.resolution_notes = resolution_notes
            if is_restricted_change is not None:
                ticket.is_restricted_change = is_restricted_change
            ticket.save()

            if inspection_notes:
                InspectionComment.objects.create(
                    ticket=ticket,
                    author=user,
                    comment_type=InspectionComment.CommentType.INSPECTION,
                    notes=inspection_notes
                )
            if resolution_notes and target_state in [TicketStatus.RESOLVED, TicketStatus.CLOSED]:
                InspectionComment.objects.create(
                    ticket=ticket,
                    author=user,
                    comment_type=InspectionComment.CommentType.RESOLUTION_EVIDENCE,
                    notes=resolution_notes
                )

            AuditEvent.objects.create(
                actor=user,
                entity_type="Ticket",
                entity_id=ticket.id,
                action="STATE_TRANSITION",
                before_state={"status": old_status, "version": old_version},
                after_state={
                    "status": ticket.status,
                    "version": ticket.version,
                    "resolution_notes": ticket.resolution_notes[:100] if ticket.resolution_notes else None
                },
                ip_address=request.META.get('REMOTE_ADDR')
            )

        return Response(TicketSerializer(ticket).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='assign')
    def assign_technician(self, request, pk=None):
        ticket = self.get_object()
        user = request.user

        if user.role not in ['facility_manager', 'administrator']:
            return Response({"error": "Only managers can assign technicians."}, status=status.HTTP_403_FORBIDDEN)

        assignee_id = request.data.get('assignee_id')
        try:
            assignee = User.objects.get(id=assignee_id, role='technician')
        except User.DoesNotExist:
            return Response({"error": "Technician not found or user is not a technician."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            ticket.assignee = assignee
            if ticket.status in [TicketStatus.INTAKE, TicketStatus.TRIAGED]:
                ticket.status = TicketStatus.ASSIGNED
            ticket.version += 1
            ticket.save()

            AuditEvent.objects.create(
                actor=user,
                entity_type="Ticket",
                entity_id=ticket.id,
                action="ASSIGN_TECHNICIAN",
                before_state=None,
                after_state={"assignee": assignee.username, "version": ticket.version},
                ip_address=request.META.get('REMOTE_ADDR')
            )

        return Response(TicketSerializer(ticket).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='inspections')
    def add_inspection(self, request, pk=None):
        ticket = self.get_object()
        notes = request.data.get('notes', '').strip()
        if not notes:
            return Response({"error": "Inspection notes cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        comment = InspectionComment.objects.create(
            ticket=ticket,
            author=request.user,
            comment_type=InspectionComment.CommentType.INSPECTION,
            notes=notes,
            evidence_ref=request.data.get('evidence_ref', '')
        )
        return Response(InspectionCommentSerializer(comment).data, status=status.HTTP_201_CREATED)

class SLAPolicyViewSet(viewsets.ModelViewSet):
    queryset = SLAPolicy.objects.filter(is_active=True).select_related('campus')
    serializer_class = SLAPolicySerializer
    permission_classes = [IsAuthenticated]
