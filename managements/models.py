from django.db import models


class Management(models.Model):
    manager = models.ForeignKey("users.User", related_name="managements", null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    deposit = models.IntegerField(blank=True, null=True)
    month_fee = models.FloatField(blank=True, null=True)
    management_fee = models.FloatField(blank=True, null=True)
    parking_fee = models.FloatField(blank=True, null=True)
    contract_day = models.DateField()
    deal_report = models.BooleanField()
    contract_start_day = models.DateField()
    contract_last_day = models.DateField()
    
    deal_renewal_notice = models.BooleanField()
    deal_renewal_right_usage = models.BooleanField()
    owner_phone = models.CharField(blank=True, null=True, max_length=100)
    tenant_phone = models.CharField(blank=True, null=True, max_length=100)
    description = models.TextField(blank=True, null=True)