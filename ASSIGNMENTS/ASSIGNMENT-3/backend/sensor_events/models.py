from django.db import models

class SensorEvent(models.Model):
    source_id = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Telemetry sensor hardware ID, e.g. HVAC-TEMP-UNIT-04"
    )
    event_id = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Unique event UUID generated at the sensor device."
    )
    metric = models.CharField(
        max_length=50,
        help_text="Telemetry metric name, e.g. temperature_celsius, vibration_hz"
    )
    value = models.FloatField()
    observed_at = models.DateTimeField()
    payload_hash = models.CharField(max_length=64, blank=True)
    ticket = models.ForeignKey(
        'maintenance.Ticket',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sensor_events'
    )
    processed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sensor_events'
        unique_together = [('source_id', 'event_id')]
        indexes = [
            models.Index(fields=['source_id', 'observed_at']),
        ]

    def __str__(self):
        return f"SensorEvent {self.source_id}:{self.event_id} ({self.metric}={self.value})"
