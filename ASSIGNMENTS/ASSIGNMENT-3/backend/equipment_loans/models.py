from django.db import models
from django.conf import settings

class LoanStatus(models.TextChoices):
    PENDING_APPROVAL = 'pending_approval', 'Pending Approval'
    APPROVED = 'approved', 'Approved'
    ACTIVE = 'active', 'Active (Checked Out)'
    RETURNED = 'returned', 'Returned'
    REJECTED = 'rejected', 'Rejected'

class EquipmentLoan(models.Model):
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='equipment_loans'
    )
    asset_name = models.CharField(max_length=120)
    asset_code = models.CharField(max_length=50)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(
        max_length=30,
        choices=LoanStatus.choices,
        default=LoanStatus.PENDING_APPROVAL
    )
    purpose = models.TextField()
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'equipment_loans'
        ordering = ['-created_at']

    def __str__(self):
        return f"Loan #{self.id}: {self.asset_name} ({self.requester.username}) - {self.status}"
