from django.utils import timezone
from django import forms
from . import models

class DateInput(forms.DateInput):
    input_type='date'

class CommonInput(forms.ModelForm):
    updated = forms.DateField(widget=DateInput, required=False, initial=timezone.now())
    birth = forms.DateField(widget=DateInput, required=False)


class HouseLeaseCustomerForm(CommonInput):
    class Meta:
        model = models.HouseLeaseCustomer
        exclude = ['realtor']

class ApartmentLeaseCustomerForm(CommonInput):
    class Meta:
        model = models.ApartmentLeaseCustomer
        exclude = ['realtor']
    

class OfficetelLeaseCustomerForm(CommonInput):
    class Meta:
        model = models.OfficetelLeaseCustomer
        exclude = ['realtor']

class ShopLeaseCustomerForm(CommonInput):
    class Meta:
        model = models.ShopLeaseCustomer
        exclude = ['realtor']
    

class HouseDealingCustomerForm(CommonInput):
    class Meta:
        model = models.HouseDealingCustomer
        exclude = ['realtor']
   

class ApartmentDealingCustomerForm(CommonInput):
    class Meta:
        model = models.ApartmentDealingCustomer
        exclude = ['realtor']
    

class OfficetelDealingCustomerForm(CommonInput):
    class Meta:
        model = models.OfficetelDealingCustomer
        exclude = ['realtor']
    

class ShopDealingCustomerForm(CommonInput):
    class Meta:
        model = models.ShopDealingCustomer
        exclude = ['realtor']
    

class BuildingDealingCustomerForm(CommonInput):
    class Meta:
        model = models.BuildingDealingCustomer
        exclude = ['realtor']
