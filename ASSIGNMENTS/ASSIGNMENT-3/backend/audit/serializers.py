from rest_framework import serializers
from .models import AuditEvent

class AuditEventSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source='actor.get_full_name', read_only=True)
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    actor_role = serializers.CharField(source='actor.role', read_only=True)

    class Meta:
        model = AuditEvent
        fields = [
            'id', 'actor', 'actor_name', 'actor_username', 'actor_role',
            'entity_type', 'entity_id', 'action',
            'before_state', 'after_state', 'ip_address', 'created_at'
        ]
        read_only_fields = '__all__'
