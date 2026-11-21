from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'campus', 'campus_name',
            'department', 'phone', 'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({"error": "Invalid username or password credentials."})
        if not user.is_active:
            raise serializers.ValidationError({"error": "User account is suspended or inactive."})
        attrs['user'] = user
        return attrs
