from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter

from .views import (RegisterAPIView, ClientViewset,
                    ContractViewset, EventViewset)


clients_router  = DefaultRouter()
clients_router.register("clients", ClientViewset, basename="clients")
contracts_router  = DefaultRouter()
contracts_router.register("contracts", ContractViewset, basename="contracts")
events_router = DefaultRouter()
events_router.register("events", EventViewset, basename='events')

urlpatterns = [
    path('signup/', RegisterAPIView.as_view()),
    path('login/', jwt_views.TokenObtainPairView.as_view(),
         name='login'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('', include(clients_router.urls)),
    path('', include(contracts_router.urls)),
    path('', include(events_router.urls))
    ]
