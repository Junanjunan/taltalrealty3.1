from django.contrib import admin
from . import models


@admin.register(models.ContractBase)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'realtor',
        'types',
        'address',
        'price',
        "deposit",
        "month_fee",
        'start_money',
        'middle_money',
        'last_money',
        'start_day',
        'middle_day',
        'last_day',
        'due_days',
        'report',
        'finished',
        'owner_phone',
        'tenant_phone',
        'description',
    )
