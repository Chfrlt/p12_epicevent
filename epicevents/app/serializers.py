from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import User, Event, Client, Contract


class RegisterSerializer(ModelSerializer):

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
        if len(value) < 8:
            raise ValidationError('Le mot de passe doit contenir au moins 8 caractères')
        return make_password(value)


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'role']
        extra_kwargs = {'password': {'write_only': True}}



class ClientDetailSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class ClientListSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'company_name', 'email', 'sales_contact', 'client_status']


class ContractDetailSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"


class ContractListSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = ["id", "client", "contract_status"]


class EventDetailSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventListSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "contract", "support_contact", "event_status"]

