from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings

class BookingStatus(models.TextChoices):
    REQUESTED = 'requested', 'Requested (Pending Review)'
    APPROVED = 'approved', 'Approved'
    CONFIRMED = 'confirmed', 'Confirmed'
    IN_USE = 'in_use', 'In Use'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'

ACTIVE_STATUSES = [
    BookingStatus.REQUESTED,
    BookingStatus.APPROVED,
    BookingStatus.CONFIRMED,
    BookingStatus.IN_USE
]

class Booking(models.Model):
    facility = models.ForeignKey(
        'facilities.Facility',
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    start_at = models.DateTimeField(db_index=True)
    end_at = models.DateTimeField(db_index=True)
    status = models.CharField(
        max_length=30,
        choices=BookingStatus.choices,
        default=BookingStatus.CONFIRMED
    )
    purpose = models.TextField()
    version = models.PositiveIntegerField(
        default=1,
        help_text="Optimistic locking version token."
    )
    request_key = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        help_text="Idempotency key for safe client retries."
    )
    cancellation_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bookings'
        ordering = ['-start_at']
        indexes = [
            models.Index(fields=['facility', 'start_at', 'end_at', 'status']),
            models.Index(fields=['requester', 'status']),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_at__gt=models.F('start_at')),
                name='booking_end_after_start'
            ),
        ]

    def __str__(self):
        return f"Booking #{self.id}: {self.facility.code} ({self.start_at.strftime('%Y-%m-%d %H:%M')} to {self.end_at.strftime('%H:%M')}) - {self.status}"

    def clean(self):
        super().clean()
        if self.start_at and self.end_at:
            if self.end_at <= self.start_at:
                raise ValidationError({"end_at": "Booking end time must occur strictly after start time."})

            # Check for overlapping active reservations for the same facility
            if self.status in ACTIVE_STATUSES:
                conflicts = Booking.objects.filter(
                    facility=self.facility,
                    status__in=ACTIVE_STATUSES,
                    start_at__lt=self.end_at,
                    end_at__gt=self.start_at
                )
                if self.pk:
                    conflicts = conflicts.exclude(pk=self.pk)
                if conflicts.exists():
                    raise ValidationError(
                        "The requested facility is already reserved during this time interval."
                    )
