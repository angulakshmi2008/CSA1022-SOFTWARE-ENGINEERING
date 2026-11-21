from rest_framework import serializers
from django.utils import timezone
from .models import Ticket, InspectionComment, SLAPolicy, TicketStatus
from .triage_engine import triage_ticket

class InspectionCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = InspectionComment
        fields = [
            'id', 'ticket', 'author', 'author_name', 'author_username',
            'comment_type', 'notes', 'evidence_ref', 'created_at'
        ]
        read_only_fields = ['id', 'author', 'created_at']

class TicketSerializer(serializers.ModelSerializer):
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    campus_code = serializers.CharField(source='campus.code', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    facility_code = serializers.CharField(source='facility.code', read_only=True)
    assignee_name = serializers.CharField(source='assignee.get_full_name', read_only=True)
    assignee_username = serializers.CharField(source='assignee.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    comments = InspectionCommentSerializer(many=True, read_only=True)
    is_sla_breached = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'campus', 'campus_name', 'campus_code',
            'facility', 'facility_name', 'facility_code',
            'source', 'title', 'description', 'category', 'category_display',
            'impact', 'urgency', 'priority', 'priority_display',
            'triage_explanation', 'status', 'status_display',
            'assignee', 'assignee_name', 'assignee_username',
            'resolution_notes', 'is_restricted_change', 'version',
            'sla_due_at', 'is_sla_breached', 'comments',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'version', 'triage_explanation', 'sla_due_at', 'created_at', 'updated_at']

    def get_is_sla_breached(self, obj):
        if obj.sla_due_at and obj.status not in [TicketStatus.RESOLVED, TicketStatus.CLOSED]:
            return timezone.now() > obj.sla_due_at
        return False

class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'campus', 'facility', 'source', 'title', 'description',
            'category', 'impact', 'urgency', 'is_restricted_change'
        ]

    def create(self, validated_data):
        title = validated_data.get('title', '')
        description = validated_data.get('description', '')
        impact = validated_data.get('impact', 'medium')
        urgency = validated_data.get('urgency', 'medium')
        override_category = validated_data.get('category')

        cat, priority, sla_due_at, explanation = triage_ticket(
            title=title,
            description=description,
            impact=impact,
            urgency=urgency,
            override_category=override_category
        )

        validated_data['category'] = cat
        validated_data['priority'] = priority
        validated_data['sla_due_at'] = sla_due_at
        validated_data['triage_explanation'] = explanation
        validated_data['status'] = TicketStatus.TRIAGED
        validated_data['version'] = 1

        return super().create(validated_data)

class TicketStateTransitionSerializer(serializers.Serializer):
    target_state = serializers.ChoiceField(choices=TicketStatus.choices)
    expected_version = serializers.IntegerField(required=True)
    inspection_notes = serializers.CharField(required=False, allow_blank=True)
    resolution_notes = serializers.CharField(required=False, allow_blank=True)
    is_restricted_change = serializers.BooleanField(required=False)

    def validate(self, attrs):
        target_state = attrs.get('target_state')
        res_notes = attrs.get('resolution_notes', '').strip()

        # Strict validation: moving to RESOLVED or CLOSED requires resolution notes
        if target_state in [TicketStatus.RESOLVED, TicketStatus.CLOSED]:
            if not res_notes or len(res_notes) < 8:
                raise serializers.ValidationError({
                    "resolution_notes": "Resolution notes and verification evidence are mandatory prior to resolving or closing a ticket."
                })

        return attrs

class SLAPolicySerializer(serializers.ModelSerializer):
    campus_name = serializers.CharField(source='campus.name', read_only=True)

    class Meta:
        model = SLAPolicy
        fields = '__all__'
