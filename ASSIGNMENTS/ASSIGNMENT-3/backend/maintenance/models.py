from django.db import models
from django.conf import settings
from django.utils import timezone

class TicketSource(models.TextChoices):
    SENSOR_EVENT = 'sensor_event', 'Automated Sensor Threshold Event'
    MANUAL_REPORT = 'manual_report', 'Manual User Report'
    ROUTINE_INSPECTION = 'routine_inspection', 'Routine Facility Inspection'

class TicketCategory(models.TextChoices):
    HVAC = 'hvac', 'Heating, Ventilation & Air Conditioning (HVAC)'
    PLUMBING = 'plumbing', 'Plumbing & Water Systems'
    ELECTRICAL = 'electrical', 'Electrical & Power Infrastructure'
    NETWORK = 'network', 'Campus IT & Wi-Fi Network'
    STRUCTURAL = 'structural', 'Doors, Windows & Structural'
    GENERAL = 'general', 'General Maintenance'

class ImpactLevel(models.TextChoices):
    HIGH = 'high', 'High Teaching / Facility Impact'
    MEDIUM = 'medium', 'Medium Operational Impact'
    LOW = 'low', 'Low Localized Impact'

class UrgencyLevel(models.TextChoices):
    HIGH = 'high', 'High Urgency (Immediate Hazard / Disruption)'
    MEDIUM = 'medium', 'Medium Urgency'
    LOW = 'low', 'Low Urgency'

class PriorityLevel(models.TextChoices):
    M1 = 'M1', 'M1 - Critical (2h Resolution SLA)'
    M2 = 'M2', 'M2 - High (4h Resolution SLA)'
    M3 = 'M3', 'M3 - Medium (8h Resolution SLA)'
    M4 = 'M4', 'M4 - Low (24h Resolution SLA)'

class TicketStatus(models.TextChoices):
    INTAKE = 'intake', 'Intake'
    TRIAGED = 'triaged', 'Triaged'
    ASSIGNED = 'assigned', 'Assigned'
    IN_PROGRESS = 'in_progress', 'In Progress'
    INSPECTION = 'inspection', 'Inspection / Diagnostics'
    PENDING_APPROVAL = 'pending_approval', 'Pending Change Approval'
    RESOLVED = 'resolved', 'Resolved'
    REJECTED = 'rejected', 'Rejected / Non-Viable'
    CLOSED = 'closed', 'Closed (Verified)'

class Ticket(models.Model):
    campus = models.ForeignKey(
        'campuses.Campus',
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    facility = models.ForeignKey(
        'facilities.Facility',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets'
    )
    source = models.CharField(
        max_length=30,
        choices=TicketSource.choices,
        default=TicketSource.MANUAL_REPORT
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=TicketCategory.choices,
        default=TicketCategory.GENERAL
    )
    impact = models.CharField(
        max_length=20,
        choices=ImpactLevel.choices,
        default=ImpactLevel.MEDIUM
    )
    urgency = models.CharField(
        max_length=20,
        choices=UrgencyLevel.choices,
        default=UrgencyLevel.MEDIUM
    )
    priority = models.CharField(
        max_length=10,
        choices=PriorityLevel.choices,
        default=PriorityLevel.M3
    )
    triage_explanation = models.TextField(
        blank=True,
        help_text="Deterministic rule explanation for assigned category and priority."
    )
    status = models.CharField(
        max_length=30,
        choices=TicketStatus.choices,
        default=TicketStatus.INTAKE
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )
    resolution_notes = models.TextField(
        blank=True,
        help_text="Mandatory documentation of repair actions prior to closure."
    )
    is_restricted_change = models.BooleanField(
        default=False,
        help_text="Flags repairs that alter structural/power systems and require approver signoff."
    )
    version = models.PositiveIntegerField(
        default=1,
        help_text="Optimistic concurrency control version token."
    )
    sla_due_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tickets'
        ordering = ['priority', '-created_at']
        indexes = [
            models.Index(fields=['campus', 'status', 'priority']),
            models.Index(fields=['assignee', 'status']),
        ]

    def __str__(self):
        return f"Ticket #{self.id} [{self.priority}]: {self.title} ({self.status}) - v{self.version}"

class InspectionComment(models.Model):
    class CommentType(models.TextChoices):
        INSPECTION = 'inspection', 'Inspection Finding'
        NOTE = 'note', 'Technician Work Log'
        RESOLUTION_EVIDENCE = 'resolution_evidence', 'Resolution Evidence'

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ticket_comments'
    )
    comment_type = models.CharField(
        max_length=30,
        choices=CommentType.choices,
        default=CommentType.INSPECTION
    )
    notes = models.TextField()
    evidence_ref = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ticket_comments'
        ordering = ['created_at']

    def __str__(self):
        return f"Comment #{self.id} on Ticket #{self.ticket_id} by {self.author.username}"

class SLAPolicy(models.Model):
    campus = models.ForeignKey(
        'campuses.Campus',
        on_delete=models.CASCADE,
        related_name='sla_policies'
    )
    category = models.CharField(max_length=50, default='all')
    priority = models.CharField(max_length=10, choices=PriorityLevel.choices)
    response_minutes = models.PositiveIntegerField(default=60)
    resolution_minutes = models.PositiveIntegerField(default=480)
    version = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'sla_policies'
        unique_together = [('campus', 'category', 'priority', 'version')]

    def __str__(self):
        return f"SLA: {self.campus.code} - {self.priority} ({self.resolution_minutes}m)"
