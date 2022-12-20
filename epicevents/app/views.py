from rest_framework import permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException

from .models import Client, Contract
from .serializers import (RegisterSerializer, ClientDetailSerializer,
                          ClientListSerializer, ContractDetailSerializer,
                          ContractListSerializer, EventDetailSerializer,
                          EventListSerializer)


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAdminUser()]

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


class ContractViewset(DualSerializerViewSet, ModelViewSet):
    serializer_class = ContractListSerializer
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
    detail_serializer_class = EventDetailSerializer
    #TODO: add filter & search fileds

    def get_queryset(self):
        user = self.request.user

        if self.action == "list" and not user.is_superuser:
            queryset = Event.objects.filter(support_contact=user)
        else:
            queryset = Event.objects.all()        

        return queryset
