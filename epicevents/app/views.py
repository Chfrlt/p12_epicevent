from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.exceptions import APIException

from .models import Client, Contract
from .serializers import ClientDetailSerializer, ClientListSerializer


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
    search_fields = ["company_name", "=sales_contact"]

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
