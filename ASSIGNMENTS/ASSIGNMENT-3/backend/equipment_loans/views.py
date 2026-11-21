from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import EquipmentLoan, LoanStatus
from .serializers import EquipmentLoanSerializer
from audit.models import AuditEvent

class EquipmentLoanViewSet(viewsets.ModelViewSet):
    queryset = EquipmentLoan.objects.select_related('requester').all()
    serializer_class = EquipmentLoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == 'student':
            qs = qs.filter(requester=user)
        return qs

    def perform_create(self, serializer):
        loan = serializer.save(
            requester=self.request.user,
            status=LoanStatus.PENDING_APPROVAL
        )
        AuditEvent.objects.create(
            actor=self.request.user,
            entity_type="EquipmentLoan",
            entity_id=loan.id,
            action="REQUEST_LOAN",
            before_state=None,
            after_state={"asset": loan.asset_name, "status": loan.status},
            ip_address=self.request.META.get('REMOTE_ADDR')
        )
