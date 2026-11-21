from rest_framework import views, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Approval, RequestType, ApprovalDecision
from .serializers import ApprovalSerializer
from bookings.models import Booking, BookingStatus
from equipment_loans.models import EquipmentLoan, LoanStatus
from maintenance.models import Ticket, TicketStatus
from audit.models import AuditEvent

class ApprovalViewSet(viewsets.ModelViewSet):
    queryset = Approval.objects.select_related('approver').all()
    serializer_class = ApprovalSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Records an authoritative approval decision.
        Enforces server-side role check: only Department Approver or Admin can decide.
        """
        user = request.user
        if user.role not in ['department_approver', 'administrator'] and not user.is_superuser:
            return Response({
                "error": "Permission Denied",
                "detail": f"User with role '{user.role}' lacks delegated approval authority.",
                "code": "INSUFFICIENT_APPROVAL_PERMISSIONS"
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        req_type = serializer.validated_data['request_type']
        req_id = serializer.validated_data['request_id']
        decision = serializer.validated_data['decision']
        reason = serializer.validated_data['reason']

        with transaction.atomic():
            approval = Approval.objects.create(
                request_type=req_type,
                request_id=req_id,
                approver=user,
                decision=decision,
                reason=reason
            )

            # Apply state transition on target resource
            target_desc = ""
            if req_type == RequestType.BOOKING:
                booking = Booking.objects.filter(id=req_id).first()
                if not booking:
                    return Response({"error": "Target booking not found."}, status=status.HTTP_404_NOT_FOUND)
                old_status = booking.status
                booking.status = BookingStatus.CONFIRMED if decision == ApprovalDecision.APPROVED else BookingStatus.CANCELLED
                booking.version += 1
                if decision == ApprovalDecision.REJECTED:
                    booking.cancellation_reason = f"Rejected by approver: {reason}"
                booking.save()
                target_desc = f"Booking #{booking.id} ({booking.facility.code})"

            elif req_type == RequestType.EQUIPMENT_LOAN:
                loan = EquipmentLoan.objects.filter(id=req_id).first()
                if not loan:
                    return Response({"error": "Target equipment loan not found."}, status=status.HTTP_404_NOT_FOUND)
                loan.status = LoanStatus.APPROVED if decision == ApprovalDecision.APPROVED else LoanStatus.REJECTED
                if decision == ApprovalDecision.REJECTED:
                    loan.rejection_reason = reason
                loan.save()
                target_desc = f"Loan #{loan.id} ({loan.asset_name})"

            elif req_type == RequestType.TICKET_CHANGE:
                ticket = Ticket.objects.filter(id=req_id).first()
                if not ticket:
                    return Response({"error": "Target ticket not found."}, status=status.HTTP_404_NOT_FOUND)
                ticket.status = TicketStatus.IN_PROGRESS if decision == ApprovalDecision.APPROVED else TicketStatus.REJECTED
                ticket.version += 1
                ticket.save()
                target_desc = f"Ticket #{ticket.id} ({ticket.title})"

            AuditEvent.objects.create(
                actor=user,
                entity_type="Approval",
                entity_id=approval.id,
                action="DECIDE_APPROVAL",
                before_state=None,
                after_state={
                    "request_type": req_type,
                    "request_id": req_id,
                    "target": target_desc,
                    "decision": decision,
                    "reason": reason
                },
                ip_address=request.META.get('REMOTE_ADDR')
            )

        return Response(ApprovalSerializer(approval).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Aggregates all items requiring approval review."""
        pending_bookings = Booking.objects.filter(status=BookingStatus.REQUESTED).select_related('facility', 'requester')
        pending_loans = EquipmentLoan.objects.filter(status=LoanStatus.PENDING_APPROVAL).select_related('requester')
        pending_tickets = Ticket.objects.filter(status=TicketStatus.PENDING_APPROVAL).select_related('campus', 'facility', 'assignee')

        items = []
        for b in pending_bookings:
            items.append({
                "type": "booking",
                "id": b.id,
                "title": f"Restricted Booking: {b.facility.name}",
                "requester": b.requester.get_full_name() or b.requester.username,
                "start_at": b.start_at,
                "end_at": b.end_at,
                "purpose": b.purpose,
                "created_at": b.created_at
            })

        for l in pending_loans:
            items.append({
                "type": "equipment_loan",
                "id": l.id,
                "title": f"Loan: {l.asset_name} ({l.asset_code})",
                "requester": l.requester.get_full_name() or l.requester.username,
                "start_at": l.start_at,
                "end_at": l.end_at,
                "purpose": l.purpose,
                "created_at": l.created_at
            })

        for t in pending_tickets:
            items.append({
                "type": "ticket_change",
                "id": t.id,
                "title": f"Maintenance Hardware Change: #{t.id} - {t.title}",
                "requester": t.assignee.get_full_name() if t.assignee else "Technician",
                "priority": t.priority,
                "purpose": t.description,
                "created_at": t.updated_at
            })

        return Response(items, status=status.HTTP_200_OK)
