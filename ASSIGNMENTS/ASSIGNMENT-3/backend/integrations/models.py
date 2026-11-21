from django.db import models

class IntentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending Dispatch'
    IN_FLIGHT = 'in_flight', 'In Flight'
    CONFIRMED = 'confirmed', 'Confirmed Linked'
    FAILED = 'failed', 'Failed (Awaiting Reconcile)'

class IntegrationIntent(models.Model):
    ticket = models.ForeignKey(
        'maintenance.Ticket',
        on_delete=models.CASCADE,
        related_name='integration_intents'
    )
    operation = models.CharField(max_length=50, default='create_developer_issue')
    correlation_key = models.CharField(
        max_length=100,
        unique=True,
        help_text="Idempotent correlation identity to reconcile retries across network timeouts."
    )
    status = models.CharField(
        max_length=30,
        choices=IntentStatus.choices,
        default=IntentStatus.PENDING
    )
    attempts = models.PositiveIntegerField(default=0)
    external_id = models.CharField(max_length=100, blank=True)
    last_error = models.TextField(blank=True)
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'integration_intents'
        ordering = ['-created_at']

    def __str__(self):
        return f"Intent #{self.id}: {self.operation} ({self.correlation_key}) - {self.status}"
