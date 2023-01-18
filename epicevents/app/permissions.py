from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from .models import Client, Contract, Event, User


class IsManager():
    def has_permission(self, request, view):
        return request.user.role == User.MANAGER

    def has_object_permission(self, request, view, obj):
        return request.user.role == User.MANAGER


class ClientPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.role == User.SALES
        return request.user.role == User.SUPPORT or request.user.role == User.SALES

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if request.user.role == User.SALES:
                return True
            if request.user.role == User.SUPPORT:
                return (obj in [c for c in Client.objects
                                              .filter(contract__event__support_contact=request.user)])
        if request.method in ('PATCH', 'PUT'):
            if request.user.role == User.SALES:
                if not obj.sales_contact or obj.sales_contact == request.user:
                    return True
            if request.user.role == User.SUPPORT:
                return (obj in [c for c in Client.objects
                                              .filter(contract__event__support_contact=request.user)])


class ContractPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.role == User.SALES
        return request.user.role == User.SUPPORT or request.user.role == User.SALES

    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'PUT') or request.method in permissions.SAFE_METHODS:
            return (obj.client.sales_contact == request.user or
                    obj in [c for c in Contract.objects
                                               .filter(event__support_contact=request.user)])


class EventPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.role == User.SALES
        return request.user.role == User.SUPPORT or request.user.role == User.SALES

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (request.user == obj.support_contact
                    or request.user == User.SALES)
        if request.method in ('PATCH', 'PUT'):
            if obj.event_status is True:
                raise PermissionDenied("L'évènement est terminé!")
            else:
                return request.user == obj.contract.client.sales_contact or request.user == obj.support_contact
