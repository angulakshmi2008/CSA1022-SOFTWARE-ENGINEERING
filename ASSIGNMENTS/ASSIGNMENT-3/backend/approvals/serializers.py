from rest_framework import serializers
from .models import Approval, RequestType, ApprovalDecision

class ApprovalSerializer(serializers.ModelSerializer):
    approver_name = serializers.CharField(source='approver.get_full_name', read_only=True)
    approver_username = serializers.CharField(source='approver.username', read_only=True)

    class Meta:
        model = Approval
        fields = [
            'id', 'request_type', 'request_id', 'approver',
            'approver_name', 'approver_username',
            'decision', 'reason', 'decided_at'
        ]
        read_only_fields = ['id', 'approver', 'decided_at']

    def validate_reason(self, value):
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError("An auditable justification reason (minimum 5 characters) is required.")
        return value.strip()
