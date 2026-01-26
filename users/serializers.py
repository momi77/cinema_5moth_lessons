from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import CustomUser

class UserAuthSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField()

class UserCreateSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField()

    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise ValidationError('Email already exists!')       