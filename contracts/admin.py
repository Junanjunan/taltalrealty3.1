from django.contrib import admin
from import_export.admin import ImportExportMixin
from . import models


@admin.register(models.ContractBase)
class ContractAdmin(ImportExportMixin, admin.ModelAdmin):
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
        'report',
        'not_finished',
        'owner_phone',
        'tenant_phone',
        'description',
    )
