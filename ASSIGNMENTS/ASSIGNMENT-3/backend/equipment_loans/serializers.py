from rest_framework import serializers
from .models import EquipmentLoan

class EquipmentLoanSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(source='requester.get_full_name', read_only=True)
    requester_username = serializers.CharField(source='requester.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = EquipmentLoan
        fields = [
            'id', 'requester', 'requester_name', 'requester_username',
            'asset_name', 'asset_code', 'start_at', 'end_at',
            'status', 'status_display', 'purpose', 'rejection_reason',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'requester', 'created_at', 'updated_at']
