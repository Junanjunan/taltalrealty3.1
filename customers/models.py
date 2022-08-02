from django.db import models


"""below customer"""

class ApartmentDealingCustomer(models.Model):
    realtor = models.ForeignKey(
        "users.User", null=True, on_delete=models.CASCADE)
    guest_phone = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    parking = models.BooleanField()
    elevator = models.BooleanField()
    loan = models.BooleanField()
    not_finished = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    area_m2 = models.FloatField()
    price = models.IntegerField()
    room = models.IntegerField()


class HouseDealingCustomer(models.Model):
    realtor = models.ForeignKey(
        "users.User", null=True, on_delete=models.CASCADE)
    guest_phone = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    room = models.IntegerField()
    price = models.IntegerField()
    area_m2 = models.FloatField()
    parking = models.BooleanField()
    elevator = models.BooleanField()
    loan = models.BooleanField()
    not_finished = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)


class OfficetelDealingCustomer(models.Model):
    realtor = models.ForeignKey(
        "users.User", null=True, on_delete=models.CASCADE)
    guest_phone = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    room = models.IntegerField()
    price = models.IntegerField()
    area_m2 = models.FloatField()
    parking = models.BooleanField()
    elevator = models.BooleanField()
    loan = models.BooleanField()
    not_finished = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)


class ShopDealingCustomer(models.Model):
    realtor = models.ForeignKey(
        "users.User", null=True, on_delete=models.CASCADE)
    guest_phone = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    price = models.IntegerField()
    area_m2 = models.FloatField()
    parking = models.BooleanField()
    elevator = models.BooleanField()
    loan = models.BooleanField()
    not_finished = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)


class BuildingDealingCustomer(models.Model):
    realtor = models.ForeignKey(
        "users.User", null=True, on_delete=models.CASCADE)
    guest_phone = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    price = models.IntegerField()
    land_m2 = models.FloatField(blank=True, null=True)
    elevator = models.BooleanField()
    loan = models.BooleanField()
    not_finished = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    


"""lease"""

class ApartmentLeaseCustomer(models.Model):
    realtor = models.ForeignKey(
        "users.User", null=True, on_delete=models.CASCADE)
    guest_phone = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    room = models.IntegerField()
    deposit = models.IntegerField()
    month_fee = models.IntegerField()
    area_m2 = models.FloatField()
    parking = models.BooleanField()
    elevator = models.BooleanField()
    loan = models.BooleanField()
    not_finished = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)  


class HouseLeaseCustomer(models.Model):
    realtor = models.ForeignKey(
        "users.User", null=True, on_delete=models.CASCADE)
    guest_phone = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    room = models.IntegerField()
    deposit = models.IntegerField()
    month_fee = models.IntegerField()
    area_m2 = models.FloatField()
    parking = models.BooleanField()
    elevator = models.BooleanField()
    loan = models.BooleanField()
    not_finished = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)


class OfficetelLeaseCustomer(models.Model):
    realtor = models.ForeignKey(
        "users.User", null=True, on_delete=models.CASCADE)
    guest_phone = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    room = models.IntegerField()
    deposit = models.IntegerField()
    month_fee = models.IntegerField()
    area_m2 = models.FloatField()
    parking = models.BooleanField()
    elevator = models.BooleanField()
    loan = models.BooleanField()
    not_finished = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    

class ShopLeaseCustomer(models.Model):
    realtor = models.ForeignKey(
        "users.User", null=True, on_delete=models.CASCADE)
    guest_phone = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    deposit = models.IntegerField()
    month_fee = models.IntegerField()
    area_m2 = models.FloatField()
    parking = models.BooleanField()
    loan = models.BooleanField()
    elevator = models.BooleanField()
    not_finished = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    
    
    




