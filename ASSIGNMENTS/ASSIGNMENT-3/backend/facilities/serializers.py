from rest_framework import serializers
from .models import Facility

class FacilitySerializer(serializers.ModelSerializer):
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    campus_code = serializers.CharField(source='campus.code', read_only=True)
    facility_type_display = serializers.CharField(source='get_facility_type_display', read_only=True)

    class Meta:
        model = Facility
        fields = [
            'id', 'campus', 'campus_name', 'campus_code',
            'name', 'code', 'facility_type', 'facility_type_display',
            'capacity', 'is_restricted', 'is_active', 'location_details', 'created_at'
        ]
