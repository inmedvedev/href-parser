from django.contrib import admin
from .models import DomainInfo, Address


@admin.register(DomainInfo)
class DomainInfoAdmin(admin.ModelAdmin):
    search_fields = [
        'url',
        'domain',
        'create_date',
        'update_date',
        'country',
        'is_dead'
    ]
    list_display = [
        'url',
        'domain',
        'create_date',
        'update_date',
        'country',
        'is_dead'
    ]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'url',
        'ip'
    ]
