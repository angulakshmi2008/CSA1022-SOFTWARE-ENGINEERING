from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db import transaction, IntegrityError, OperationalError, connection
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ValidationError

from .models import Booking, BookingStatus, ACTIVE_STATUSES
from .serializers import BookingSerializer, BookingStatusUpdateSerializer
from facilities.models import Facility
from audit.models import AuditEvent

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('facility', 'facility__campus', 'requester').all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        facility = self.request.query_params.get('facility')
        campus = self.request.query_params.get('campus')
        status_filter = self.request.query_params.get('status')

        if facility:
            qs = qs.filter(facility_id=facility)
        if campus:
            qs = qs.filter(facility__campus_id=campus)
        if status_filter:
            qs = qs.filter(status=status_filter)

        # Standard students can only see their own bookings unless viewing calendar view
        if user.role == 'student' and self.action not in ['calendar', 'retrieve']:
            qs = qs.filter(requester=user)

        return qs

    def create(self, request, *args, **kwargs):
        data = request.data
        request_key = data.get('request_key')

        # Idempotency check: if key supplied and booking exists, return existing record
        if request_key:
            existing = Booking.objects.filter(request_key=request_key).first()
            if existing:
                serializer = self.get_serializer(existing)
                return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        facility_id = data.get('facility') or data.get('facility_id')
        try:
            facility = Facility.objects.get(id=facility_id)
        except Facility.DoesNotExist:
            return Response({"error": "Facility not found."}, status=status.HTTP_404_NOT_FOUND)

        start_at = serializer.validated_data['start_at']
        end_at = serializer.validated_data['end_at']
        purpose = serializer.validated_data.get('purpose', '')

        # Role authority check: Students cannot reserve restricted research facilities directly
        initial_status = BookingStatus.CONFIRMED
        if facility.is_restricted:
            if request.user.role == 'student':
                return Response({
                    "error": "Permission Denied",
                    "detail": "Students are not permitted to reserve restricted research facilities directly.",
                    "code": "RESTRICTED_FACILITY_ACCESS"
                }, status=status.HTTP_403_FORBIDDEN)
            elif request.user.role == 'faculty':
                # Faculty booking a restricted facility requires Department Approver review
                initial_status = BookingStatus.REQUESTED

        # Enforce non-overlap within atomic transaction
        try:
            with transaction.atomic():
                # On PostgreSQL, lock the facility record to serialize concurrent booking attempts
                if connection.vendor == 'postgresql':
                    _ = Facility.objects.select_for_update().get(id=facility.id)

                # Database overlap check
                overlapping = Booking.objects.filter(
                    facility=facility,
                    status__in=ACTIVE_STATUSES,
                    start_at__lt=end_at,
                    end_at__gt=start_at
                )

                if overlapping.exists():
                    return Response({
                        "error": "Booking Conflict",
                        "detail": "The requested facility is already reserved during this time interval.",
                        "code": "OVERLAPPING_RESERVATION",
                        "conflicting_booking_id": overlapping.first().id
                    }, status=status.HTTP_409_CONFLICT)

                booking = Booking.objects.create(
                    facility=facility,
                    requester=request.user,
                    start_at=start_at,
                    end_at=end_at,
                    status=initial_status,
                    purpose=purpose,
                    request_key=request_key,
                    version=1
                )

                # Append audit event in the same transaction
                AuditEvent.objects.create(
                    actor=request.user,
                    entity_type="Booking",
                    entity_id=booking.id,
                    action="CREATE_BOOKING",
                    before_state=None,
                    after_state={
                        "id": booking.id,
                        "facility": facility.code,
                        "status": booking.status,
                        "start_at": str(booking.start_at),
                        "end_at": str(booking.end_at),
                        "version": booking.version
                    },
                    ip_address=request.META.get('REMOTE_ADDR')
                )

        except (IntegrityError, OperationalError) as exc:
            return Response({
                "error": "Booking Conflict",
                "detail": "Database constraint or concurrent access rejected overlapping reservation.",
                "code": "OVERLAPPING_RESERVATION",
                "db_error": str(exc)
            }, status=status.HTTP_409_CONFLICT)

        output_serializer = self.get_serializer(booking)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def calendar(self, request):
        """Calendar view returning booked intervals for scheduling."""
        facility_id = request.query_params.get('facility_id')
        start = request.query_params.get('start')
        end = request.query_params.get('end')

        qs = Booking.objects.filter(status__in=ACTIVE_STATUSES).select_related('facility', 'requester')
        if facility_id:
            qs = qs.filter(facility_id=facility_id)
        if start:
            start_dt = parse_datetime(start)
            if start_dt:
                qs = qs.filter(end_at__gte=start_dt)
        if end:
            end_dt = parse_datetime(end)
            if end_dt:
                qs = qs.filter(start_at__lte=end_dt)

        data = []
        for b in qs:
            data.append({
                "id": b.id,
                "facility_id": b.facility_id,
                "facility_name": b.facility.name,
                "facility_code": b.facility.code,
                "start_at": b.start_at,
                "end_at": b.end_at,
                "status": b.status,
                "purpose": b.purpose,
                "requester_name": b.requester.get_full_name() or b.requester.username
            })
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='my-bookings')
    def my_bookings(self, request):
        bookings = Booking.objects.filter(requester=request.user).select_related('facility').order_by('-created_at')
        return Response(self.get_serializer(bookings, many=True).data)

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        """Update booking lifecycle status with optimistic locking version check."""
        booking = self.get_object()
        serializer = BookingStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        target_status = serializer.validated_data['target_status']
        expected_version = serializer.validated_data['expected_version']
        reason = serializer.validated_data.get('reason', '')

        # Optimistic concurrency check
        if booking.version != expected_version:
            return Response({
                "error": "Concurrent Modification Conflict",
                "detail": f"Booking has been modified. Expected version {expected_version}, but current version is {booking.version}.",
                "current_version": booking.version,
                "code": "STALE_VERSION_CONFLICT"
            }, status=status.HTTP_409_CONFLICT)

        # Authorization: Requesters can cancel; managers/approvers/admins can manage
        user = request.user
        if target_status == BookingStatus.CANCELLED:
            if booking.requester != user and not (user.role in ['facility_manager', 'administrator']):
                return Response({"error": "Unauthorized to cancel this reservation."}, status=status.HTTP_403_FORBIDDEN)
        elif target_status in [BookingStatus.APPROVED, BookingStatus.CONFIRMED]:
            if user.role not in ['department_approver', 'facility_manager', 'administrator']:
                return Response({"error": "Insufficient privileges to approve bookings."}, status=status.HTTP_403_FORBIDDEN)

        old_status = booking.status
        old_version = booking.version

        with transaction.atomic():
            booking.status = target_status
            booking.version += 1
            if reason:
                booking.cancellation_reason = reason
            booking.save()

            AuditEvent.objects.create(
                actor=user,
                entity_type="Booking",
                entity_id=booking.id,
                action="STATUS_TRANSITION",
                before_state={"status": old_status, "version": old_version},
                after_state={"status": booking.status, "version": booking.version, "reason": reason},
                ip_address=request.META.get('REMOTE_ADDR')
            )

        return Response(self.get_serializer(booking).data, status=status.HTTP_200_OK)
