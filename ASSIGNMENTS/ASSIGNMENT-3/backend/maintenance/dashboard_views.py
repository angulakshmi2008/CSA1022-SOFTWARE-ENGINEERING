from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta

from .models import Ticket, TicketStatus, PriorityLevel
from bookings.models import Booking, ACTIVE_STATUSES, BookingStatus
from facilities.models import Facility
from equipment_loans.models import EquipmentLoan, LoanStatus
from audit.models import AuditEvent
from audit.serializers import AuditEventSerializer

class DashboardSummaryView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        one_hour_ahead = now + timedelta(hours=1)
        campus_id = request.query_params.get('campus')

        # Base querysets
        bookings_qs = Booking.objects.all()
        tickets_qs = Ticket.objects.all()
        facilities_qs = Facility.objects.filter(is_active=True)
        loans_qs = EquipmentLoan.objects.all()

        if campus_id:
            bookings_qs = bookings_qs.filter(facility__campus_id=campus_id)
            tickets_qs = tickets_qs.filter(campus_id=campus_id)
            facilities_qs = facilities_qs.filter(campus_id=campus_id)

        active_bookings_count = bookings_qs.filter(status__in=ACTIVE_STATUSES).count()

        terminal_states = [TicketStatus.RESOLVED, TicketStatus.CLOSED, TicketStatus.REJECTED]
        open_tickets_qs = tickets_qs.exclude(status__in=terminal_states)
        open_tickets_count = open_tickets_qs.count()

        pending_booking_approvals = bookings_qs.filter(status=BookingStatus.REQUESTED).count()
        pending_loan_approvals = loans_qs.filter(status=LoanStatus.PENDING_APPROVAL).count()
        pending_ticket_approvals = tickets_qs.filter(status=TicketStatus.PENDING_APPROVAL).count()
        total_pending_approvals = pending_booking_approvals + pending_loan_approvals + pending_ticket_approvals

        sla_at_risk_count = open_tickets_qs.filter(
            sla_due_at__isnull=False,
            sla_due_at__lte=one_hour_ahead
        ).count()

        # Priority distribution
        priority_breakdown = {
            'M1': open_tickets_qs.filter(priority=PriorityLevel.M1).count(),
            'M2': open_tickets_qs.filter(priority=PriorityLevel.M2).count(),
            'M3': open_tickets_qs.filter(priority=PriorityLevel.M3).count(),
            'M4': open_tickets_qs.filter(priority=PriorityLevel.M4).count(),
        }

        # Recent audit activity
        recent_audits = AuditEvent.objects.select_related('actor').order_by('-created_at')[:10]

        return Response({
            "metrics": {
                "active_bookings": active_bookings_count,
                "open_tickets": open_tickets_count,
                "pending_approvals": total_pending_approvals,
                "pending_booking_approvals": pending_booking_approvals,
                "pending_loan_approvals": pending_loan_approvals,
                "pending_ticket_approvals": pending_ticket_approvals,
                "sla_at_risk": sla_at_risk_count,
                "total_facilities": facilities_qs.count(),
            },
            "priority_breakdown": priority_breakdown,
            "recent_activity": AuditEventSerializer(recent_audits, many=True).data,
            "timestamp": now.isoformat()
        }, status=status.HTTP_200_OK)
