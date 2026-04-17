from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class AdminCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            role='admin',
            is_staff=True,
            **validated_data,
        )


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if user.role != 'admin':
            raise serializers.ValidationError("Access restricted to admins.")
        data['user'] = user
        return data
