from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        if validate_password(validated_data['password']) is None:
            validated_data['password'] = (
                make_password(validated_data['password'])
                )
        user = User.objects.create(**validated_data)
        return user

class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        """Hashes password."""
        if len(value) < 8:
            raise ValidationError('Le mot de passe doit contenir au moins 8 caractères')
        return make_password(value)


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'role']
        extra_kwargs = {'password': {'write_only': True}}
