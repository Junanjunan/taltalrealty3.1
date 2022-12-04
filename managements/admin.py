from django.contrib import admin
from . import models

@admin.register(models.Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = (
        'address',
        'realtor',
        'deposit',
        'month_fee',
        'management_fee',
        'parking_fee',
        'contract_day',
        'deal_report',
        'contract_start_day',
        'contract_last_day',
        'deal_renewal_notice',
        'deal_renewal_right_usage',
        'owner_phone',
        'tenant_phone',
        'description',
    )