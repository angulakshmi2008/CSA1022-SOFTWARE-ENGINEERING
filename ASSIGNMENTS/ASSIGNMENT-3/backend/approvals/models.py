from django.db import models
from django.conf import settings

class RequestType(models.TextChoices):
    BOOKING = 'booking', 'Restricted Facility Booking'
    EQUIPMENT_LOAN = 'equipment_loan', 'Equipment Loan Request'
    TICKET_CHANGE = 'ticket_change', 'Maintenance Hardware / High-Impact Change'

class ApprovalDecision(models.TextChoices):
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'

class Approval(models.Model):
    request_type = models.CharField(max_length=30, choices=RequestType.choices)
    request_id = models.PositiveIntegerField(db_index=True)
    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='approvals'
    )
    decision = models.CharField(max_length=20, choices=ApprovalDecision.choices)
    reason = models.TextField(help_text="Mandatory justification for decision.")
    decided_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'approvals'
        ordering = ['-decided_at']

    def __str__(self):
        return f"Approval #{self.id}: {self.request_type} #{self.request_id} -> {self.decision} by {self.approver.username}"
