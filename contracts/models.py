from django.db import models


class ContractBase(models.Model):
    
    TYPE_DEAL = "Deal"
    TYPE_LEASE = "Lease"
    TYPE_CHOICES = (
        (TYPE_DEAL, "매매"),
        (TYPE_LEASE, "임대")
    )

    realtor = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)
    types = models.CharField(max_length=10, choices=TYPE_CHOICES)
    address = models.CharField(max_length=100)
    price = models.IntegerField(blank=True, null=True)
    deposit = models.IntegerField(blank=True, null=True)
    month_fee = models.FloatField(blank=True, null=True)
    start_money = models.IntegerField()
    middle_money = models.IntegerField(blank=True, null=True)
    last_money = models.IntegerField()
    start_day = models.DateField()
    middle_day = models.DateField(blank=True, null=True)
    last_day = models.DateField()
    due_days = models.DurationField(blank=True, null=True)
    report = models.BooleanField()
    not_finished = models.BooleanField(default=True)
    owner_phone = models.CharField(blank=True, null=True, max_length=100)
    tenant_phone = models.CharField(blank=True, null=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    
