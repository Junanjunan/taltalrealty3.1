from django.db import models
from datetime import datetime


""" dealing """

class ApartmentDealing(models.Model):
    # apartmentdealing_id = models.BigAutoField(primary_key=True)
    realtor = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    price = models.IntegerField()
    deposit = models.IntegerField()
    month_fee = models.IntegerField()
    management_fee = models.IntegerField(blank=True, null=True)
    room = models.IntegerField()
    bath = models.IntegerField(blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    area_m2 = models.FloatField()
    total_area_m2 = models.FloatField(blank=True, null=True)
    land_m2 = models.FloatField(blank=True, null=True)
    parking = models.BooleanField(null=True)
    elevator = models.BooleanField(null=True)
    loan = models.BooleanField(null=True)
    empty = models.BooleanField(null=True)  
    not_finished = models.BooleanField(default=True)   
    naver = models.BooleanField(null=True)
    dabang = models.BooleanField(null=True)
    zicbang = models.BooleanField(null=True)
    peterpan = models.BooleanField(null=True)
    owner_phone = models.CharField(blank=True, null=True, max_length=100)
    tenant_phone = models.CharField(blank=True, null=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    
    
class RoomDealing(models.Model):
    realtor = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True, default=datetime.now().strftime('%Y-%m-%d'))
    price = models.IntegerField()
    deposit = models.IntegerField(blank=True, null=True)
    month_fee = models.IntegerField(blank=True, null=True)
    management_fee = models.IntegerField(blank=True, null=True)
    room = models.IntegerField()
    bath = models.IntegerField(blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    area_m2 = models.FloatField(blank=True, null=True)
    total_area_m2 = models.FloatField(blank=True, null=True)
    land_m2 = models.FloatField(blank=True, null=True)
    parking = models.BooleanField()    
    elevator = models.BooleanField()
    loan = models.BooleanField()
    empty = models.BooleanField()  
    not_finished = models.BooleanField(default=True)   
    naver = models.BooleanField()
    dabang = models.BooleanField()
    zicbang = models.BooleanField()
    peterpan = models.BooleanField()
    owner_phone = models.CharField(blank=True, null=True, max_length=100)
    tenant_phone = models.CharField(blank=True, null=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    
    
    
    

class OfficetelDealing(models.Model):
    realtor = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True, default=datetime.now().strftime('%Y-%m-%d'))
    price = models.IntegerField()
    deposit = models.IntegerField(blank=True, null=True)
    month_fee = models.IntegerField(blank=True, null=True)
    management_fee = models.IntegerField(blank=True, null=True)
    room = models.IntegerField()
    bath = models.IntegerField(blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    area_m2 = models.FloatField()
    total_area_m2 = models.FloatField(blank=True, null=True)
    land_m2 = models.FloatField(blank=True, null=True)
    parking = models.BooleanField() 
    elevator = models.BooleanField()
    loan = models.BooleanField()
    empty = models.BooleanField() 
    naver = models.BooleanField()
    dabang = models.BooleanField()
    zicbang = models.BooleanField()
    peterpan = models.BooleanField()
    not_finished = models.BooleanField(default=True)   
    owner_phone = models.CharField(blank=True, null=True, max_length=100)
    tenant_phone = models.CharField(blank=True, null=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    

class StoreDealing(models.Model):
    realtor = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    price = models.IntegerField()
    deposit = models.IntegerField(blank=True, null=True)
    month_fee = models.IntegerField(blank=True, null=True)
    management_fee = models.IntegerField(blank=True, null=True)
    bath = models.IntegerField(blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    area_m2 = models.FloatField()
    total_area_m2 = models.FloatField(blank=True, null=True)
    land_m2 = models.FloatField(blank=True, null=True)
    parking = models.BooleanField()
    elevator = models.BooleanField()
    loan = models.BooleanField()
    empty = models.BooleanField()
    not_finished = models.BooleanField(default=True)   
    naver = models.BooleanField()
    dabang = models.BooleanField()
    zicbang = models.BooleanField()
    peterpan = models.BooleanField()
    owner_phone = models.CharField(blank=True, null=True, max_length=100)
    tenant_phone = models.CharField(blank=True, null=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    

class BuildingDealing(models.Model):
    realtor = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    price = models.IntegerField()
    deposit = models.IntegerField()
    month_fee = models.IntegerField()
    management_fee = models.IntegerField(blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    floor_top = models.IntegerField(blank=True, null=True)
    floor_bottom = models.IntegerField(blank=True, null=True)
    land_type = models.CharField(blank=True, null=True, max_length=20)
    land_m2 = models.FloatField(blank=True, null=True)
    building_area_m2 = models.FloatField(blank=True, null=True)
    total_floor_area_m2 = models.FloatField(blank=True, null=True)
    total_floor_area_m2_for_ratio = models.FloatField(blank=True, null=True)
    building_coverage = models.FloatField(blank=True, null=True)
    floor_area_ratio = models.FloatField(blank=True, null=True)
    parking_number = models.IntegerField(blank=True, null=True)
    elevator = models.BooleanField()
    loan = models.BooleanField()
    not_finished = models.BooleanField(default=True)   
    naver = models.BooleanField()
    dabang = models.BooleanField()
    zicbang = models.BooleanField()
    peterpan = models.BooleanField()
    owner_phone = models.CharField(blank=True, null=True, max_length=100)
    tenant_phone = models.CharField(blank=True, null=True, max_length=100)
    description = models.TextField(blank=True, null=True)


""" lease """

class ApartmentLease(models.Model):
    realtor = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    deposit = models.IntegerField()
    month_fee = models.IntegerField()
    management_fee = models.IntegerField(blank=True, null=True)
    room = models.IntegerField()
    bath = models.IntegerField(blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    area_m2 = models.FloatField()
    total_area_m2 = models.FloatField(blank=True, null=True)
    parking = models.BooleanField()    
    elevator = models.BooleanField()
    loan = models.BooleanField()
    empty = models.BooleanField() 
    not_finished = models.BooleanField(default=True)   
    naver = models.BooleanField()
    dabang = models.BooleanField()
    zicbang = models.BooleanField()
    peterpan = models.BooleanField()
    owner_phone = models.CharField(blank=True, null=True, max_length=100)
    tenant_phone = models.CharField(blank=True, null=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    

class RoomLease(models.Model):
    realtor = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    deposit = models.IntegerField()
    month_fee = models.IntegerField()
    management_fee = models.IntegerField(blank=True, null=True)
    room = models.IntegerField()
    bath = models.IntegerField(blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    area_m2 = models.FloatField()
    total_area_m2 = models.FloatField(blank=True, null=True)
    parking = models.BooleanField()
    elevator = models.BooleanField()
    loan = models.BooleanField()
    empty = models.BooleanField()  
    naver = models.BooleanField()
    dabang = models.BooleanField()
    zicbang = models.BooleanField()
    peterpan = models.BooleanField()
    not_finished = models.BooleanField(default=True)   
    owner_phone = models.CharField(blank=True, null=True, max_length=100)
    tenant_phone = models.CharField(blank=True, null=True, max_length=100)
    description = models.TextField(blank=True, null=True)


class OfficetelLease(models.Model):
    realtor = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    deposit = models.IntegerField()
    month_fee = models.IntegerField()
    management_fee = models.IntegerField(blank=True, null=True)
    room = models.IntegerField()
    bath = models.IntegerField(blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    area_m2 = models.FloatField()
    total_area_m2 = models.FloatField(blank=True, null=True)
    parking = models.BooleanField()  
    elevator = models.BooleanField()
    loan = models.BooleanField()
    empty = models.BooleanField()  
    not_finished = models.BooleanField(default=True)   
    naver = models.BooleanField()
    dabang = models.BooleanField()
    zicbang = models.BooleanField()
    peterpan = models.BooleanField()
    owner_phone = models.CharField(blank=True, null=True, max_length=100)
    tenant_phone = models.CharField(blank=True, null=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    

class StoreLease(models.Model):
    realtor = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    updated = models.DateField(blank=True, null=True)
    right_deposit = models.IntegerField(blank=True, null=True)
    deposit = models.IntegerField()
    month_fee = models.IntegerField()
    management_fee = models.IntegerField(blank=True, null=True)
    bath = models.IntegerField(blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    area_m2 = models.FloatField()
    total_area_m2 = models.FloatField(blank=True, null=True)
    parking = models.BooleanField() 
    elevator = models.BooleanField()
    loan = models.BooleanField()
    empty = models.BooleanField()
    not_finished = models.BooleanField(default=True)   
    naver = models.BooleanField()
    dabang = models.BooleanField()
    zicbang = models.BooleanField()
    peterpan = models.BooleanField()
    owner_phone = models.CharField(blank=True, null=True, max_length=100)
    tenant_phone = models.CharField(blank=True, null=True, max_length=100)
    description = models.TextField(blank=True, null=True)