from django.contrib import admin

from .models import User, Client, Contract, Event


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "role", "is_staff", "is_admin", "is_superuser")
    list_filter = ("is_admin", "role", "groups")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("company_name", "client_status", "email")
    list_filter = ("company_name", "client_status", "email")


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("client", "contract_status", "amount", "payment_due")
    list_filter = ("client", "contract_status", "amount", "payment_due")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("contract", "event_status", "event_date")
    list_filter = ("contract", "event_status", "event_date")
