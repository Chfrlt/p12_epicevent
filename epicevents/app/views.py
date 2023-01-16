from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException

from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated

from .models import Client, Contract, Event
from .serializers import (RegisterSerializer, ClientDetailSerializer,
                          ClientListSerializer, ContractDetailSerializer,
                          ContractListSerializer, EventDetailSerializer,
                          EventListSerializer)
from .permissions import (IsManager, ClientPermissions,
                          ContractPermissions, EventPermissions)


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAdminUser()]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DualSerializerViewSet(ModelViewSet):
    
    detail_serializer_class = None

    def get_serializer_class(self):
        detail_serializer_actions = ["retrieve", "update", "partial_update", "create"]
        if self.action in detail_serializer_actions and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ClientViewset(DualSerializerViewSet, ModelViewSet):
    serializer_class = ClientListSerializer
    permission_classes = [IsAuthenticated, IsManager | ClientPermissions]
    detail_serializer_class = ClientDetailSerializer
    filterset_fields = ["client_status"]
    search_fields = ["company_name", "=client__sales_contact"]

    def get_queryset(self):
        if self.request.user.role == 2:
            query = Client.objects.filter(sales_contact=self.request.user).order_by(
                "id"
            )
            return query
        elif self.request.user.role == 3:
            raise APIException("Vous n'avez pas l'autorisation d'acceder à cette requête")
        else:
            queryset = Client.objects.all()
        return queryset

    def create(self, request):
        data = request.data.copy()

        serialized_data = self.detail_serializer_class(data=data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        client = get_object_or_404(Client, pk=serialized_data.data.get('id'))
        if client.sales_contact is not None:
            client.client_status = True
            client.save()

        return Response(serialized_data.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, **kwargs):
        client = get_object_or_404(Client, pk=pk)
        self.check_object_permissions(request, client) 

        serialized_data = self.detail_serializer_class(client, data=request.data, partial=True)
        serialized_data.is_valid(raise_exception=True)
        if 'client_status' in serialized_data.validated_data:
            raise ValidationError('Impossible: cette donnée se met à jour automatiquement.')
        if 'sales_contact' in serialized_data.validated_data:
            if serialized_data.validated_data['sales_contact']:
                serialized_data.validated_data['client_status'] = True
            else:
                serialized_data.validated_data['client_status'] = False
            serialized_data.save()
        else:
            serialized_data.save()

        return Response(serialized_data.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        client_inst = get_object_or_404(Client, pk=pk)
        self.check_object_permissions(request, client_inst)
        if Contract.objects.filter(client=client_inst):
            raise ValidationError('Ce client est lié à un ou plusieurs contract(s). Action impossible')
        try:
            self.perform_destroy(client_inst)
        except Http404:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)


class ContractViewset(DualSerializerViewSet, ModelViewSet):
    serializer_class = ContractListSerializer
    serializer_class = ContractListSerializer    
    permission_classes = [IsAuthenticated, IsManager | ContractPermissions]
    detail_serializer_class = ContractDetailSerializer
    filterset_fields = ['contract_status']

    def get_queryset(self):
        user = self.request.user

        if self.action == "list" and not user.is_superuser:
            client = Client.objects.filter(sales_contact=user)
            if client:
                queryset = Contract.objects.filter(client__in=client)
            else:
                raise APIException("Aucun contrat trouvé")
        else:
            queryset = Contract.objects.all()

        return queryset


    def create(self, request):
        data = request.data.copy()
        data['client_status'] = True

        serialized_data = self.detail_serializer_class(data=data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        client = get_object_or_404(Client, pk=serialized_data.data.get('client'))
        if client.sales_contact is None and self.request.user.role == 2:
            client.sales_contact = request.user
            client.save()

        return Response(serialized_data.data)

    def update(self, request, pk=None):
        
        contract = get_object_or_404(Contract, pk=pk)

        if contract.client.sales_contact == self.request.user:
            serialized_data = self.detail_serializer_class(contract, data=request.data, partial=True)
            serialized_data.is_valid(raise_exception=True)
            serialized_data.save()

        return Response(serialized_data.data)


class EventViewset(DualSerializerViewSet, ModelViewSet):

    serializer_class = EventListSerializer
    permission_classes = [IsAuthenticated, IsManager | EventPermissions]
    detail_serializer_class = EventDetailSerializer
    #TODO: add filter & search fileds

    def get_queryset(self):
        user = self.request.user

        if self.action == "list" and not user.is_superuser:
            queryset = Event.objects.filter(support_contact=user)
        else:
            queryset = Event.objects.all()        

        return queryset
