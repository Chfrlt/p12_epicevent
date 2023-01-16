from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from .models import Client, Contract, Event, User


class IsManager():
    def has_permission(self, request, view):
        return request.user.role == 1

    def has_object_permission(self, request, view, obj):
        return request.user.role == 1


class ClientPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.role == User.SALES
        return request.user.role == 3 or request.user.role == 2

    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'PUT') or request.method in permissions.SAFE_METHODS:
            if request.user.role == 2:
                    return True
            if request.user.role == 3:
                return (obj in [c.id for c in Client.objects
                                              .filter(contract__event__support_contact=request.user)])

    def has_object_permission(self, request, view, obj):
        return (request.user.role == 1)
