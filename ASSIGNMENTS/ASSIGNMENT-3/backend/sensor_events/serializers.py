from rest_framework import serializers
from .models import SensorEvent

class SensorEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorEvent
        fields = [
            'id', 'source_id', 'event_id', 'metric', 'value',
            'observed_at', 'payload_hash', 'ticket', 'processed_at'
        ]
        read_only_fields = ['id', 'processed_at']

class SensorEventIngestSerializer(serializers.Serializer):
    source_id = serializers.CharField(max_length=100)
    event_id = serializers.CharField(max_length=100)
    metric = serializers.CharField(max_length=50)
    value = serializers.FloatField()
    observed_at = serializers.DateTimeField()
    facility_id = serializers.IntegerField(required=False, allow_null=True)
    campus_id = serializers.IntegerField(required=False, allow_null=True)
