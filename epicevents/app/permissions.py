from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsManager():
    def has_permission(self, request, view):
        return (request.user.role == 1)

    def has_object_permission(self, request, view, obj):
        return (request.user.role == 1)
