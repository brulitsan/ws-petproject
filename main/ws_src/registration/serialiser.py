from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name", "role"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
