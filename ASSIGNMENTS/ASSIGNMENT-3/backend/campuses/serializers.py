from rest_framework import serializers
from .models import Campus

class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ['id', 'code', 'name', 'city', 'timezone', 'is_active', 'created_at']
