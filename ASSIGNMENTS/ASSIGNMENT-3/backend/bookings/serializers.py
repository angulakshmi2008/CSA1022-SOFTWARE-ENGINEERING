from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import Booking, BookingStatus, ACTIVE_STATUSES
from facilities.models import Facility
from config.policies import MAX_BOOKING_DURATION_HOURS

class BookingSerializer(serializers.ModelSerializer):
    facility_id = serializers.PrimaryKeyRelatedField(
        source='facility',
        queryset=Facility.objects.all(),
        required=False
    )
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    facility_code = serializers.CharField(source='facility.code', read_only=True)
    campus_name = serializers.CharField(source='facility.campus.name', read_only=True)
    requester_name = serializers.CharField(source='requester.get_full_name', read_only=True)
    requester_username = serializers.CharField(source='requester.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'facility', 'facility_id', 'facility_name', 'facility_code', 'campus_name',
            'requester', 'requester_name', 'requester_username',
            'start_at', 'end_at', 'status', 'status_display',
            'purpose', 'version', 'request_key', 'cancellation_reason',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'requester', 'version', 'created_at', 'updated_at']
        extra_kwargs = {
            'facility': {'required': False}
        }

    def validate(self, attrs):
        # Support either facility or facility_id
        facility = attrs.get('facility')
        if not facility and self.initial_data.get('facility_id'):
            try:
                facility = Facility.objects.get(id=self.initial_data['facility_id'])
                attrs['facility'] = facility
            except Facility.DoesNotExist:
                raise serializers.ValidationError({"facility": "Facility does not exist."})
        elif not facility and self.initial_data.get('facility'):
            try:
                facility = Facility.objects.get(id=self.initial_data['facility'])
                attrs['facility'] = facility
            except Facility.DoesNotExist:
                raise serializers.ValidationError({"facility": "Facility does not exist."})

        if not attrs.get('facility') and not self.instance:
            raise serializers.ValidationError({"facility": "This field is required."})

        start_at = attrs.get('start_at')
        end_at = attrs.get('end_at')

        if start_at and end_at:
            if end_at <= start_at:
                raise serializers.ValidationError({
                    "end_at": "Booking end time must occur strictly after start time."
                })

            duration = end_at - start_at
            max_duration = timedelta(hours=MAX_BOOKING_DURATION_HOURS)
            if duration > max_duration:
                raise serializers.ValidationError({
                    "duration": f"Booking duration ({duration}) exceeds maximum policy limit of {MAX_BOOKING_DURATION_HOURS} hours."
                })

        return attrs

class BookingStatusUpdateSerializer(serializers.Serializer):
    target_status = serializers.ChoiceField(choices=BookingStatus.choices)
    expected_version = serializers.IntegerField(required=True)
    reason = serializers.CharField(required=False, allow_blank=True)
