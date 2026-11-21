from rest_framework import serializers
from .models import IntegrationIntent

class IntegrationIntentSerializer(serializers.ModelSerializer):
    ticket_title = serializers.CharField(source='ticket.title', read_only=True)
    ticket_priority = serializers.CharField(source='ticket.priority', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = IntegrationIntent
        fields = [
            'id', 'ticket', 'ticket_title', 'ticket_priority',
            'operation', 'correlation_key', 'status', 'status_display',
            'attempts', 'external_id', 'last_error', 'last_attempt_at', 'created_at'
        ]
        read_only_fields = ['id', 'attempts', 'external_id', 'last_error', 'last_attempt_at', 'created_at']
