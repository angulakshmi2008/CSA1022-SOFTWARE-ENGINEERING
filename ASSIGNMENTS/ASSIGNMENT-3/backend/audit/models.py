from django.db import models
from django.conf import settings

class AuditEvent(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_events'
    )
    entity_type = models.CharField(
        max_length=50,
        db_index=True,
        help_text="Target entity model name (Booking, Ticket, Approval, etc.)"
    )
    entity_id = models.PositiveIntegerField(db_index=True)
    action = models.CharField(
        max_length=50,
        help_text="Operation performed (CREATE, STATUS_TRANSITION, DECIDE_APPROVAL, etc.)"
    )
    before_state = models.JSONField(null=True, blank=True)
    after_state = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'audit_events'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['entity_type', 'entity_id']),
            models.Index(fields=['actor', 'created_at']),
        ]

    def __str__(self):
        actor_name = self.actor.username if self.actor else "System/Anonymous"
        return f"[{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {actor_name} -> {self.action} on {self.entity_type}#{self.entity_id}"
