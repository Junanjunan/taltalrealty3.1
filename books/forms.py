from django import forms
from . import models


class DateInput(forms.DateInput):
    input_type='date'

class CommonInput(forms.ModelForm):
    updated = forms.DateField(widget=DateInput, required=False)
    birth = forms.DateField(widget=DateInput, required=False)

    def clean(self):
        owner_phone = self.cleaned_data.get("owner_phone")
        tenant_phone = self.cleaned_data.get("tenant_phone")
        if owner_phone is None and tenant_phone is None:
            self.add_error("owner_phone", forms.ValidationError("소유자, 세입자 연락처 중 최소한 하나는 입력 해주세요."))

class RoomLeaseForm(CommonInput):
    class Meta:
        model = models.RoomLease
        """fields = (
            'realtor',
            'address',
            "deposit",
            "month_fee",
            "management_fee",
            "area_m2",
            "room",
            "bath",
            "parking",
            "elevator",
            "loan",
            "empty",
            "not_finished",
            "owner_phone",
            "tenant_phone",
            "description")"""
        """"fields = '__all__'"""
        exclude = ['realtor']
        # widgets = {
        #     'description': forms.Textarea(attrs={'rows':2, 'cols':10}),
        # }

    # address = forms.CharField(widget=forms.TextInput(attrs={'class':'creating-address-input'}))
    # updated = forms.DateField(widget=DateInput)
    # birth = forms.DateField(widget=DateInput)

    

class ApartmentLeaseForm(CommonInput):
    class Meta:
        model = models.ApartmentLease
        exclude = ['realtor']


class OfficetelLeaseForm(CommonInput):
    class Meta:
        model = models.OfficetelLease
        exclude = ['realtor']



class StoreLeaseForm(CommonInput):
    class Meta:
        model = models.StoreLease
        exclude = ['realtor']


class RoomDealingForm(CommonInput):
    class Meta:
        model = models.RoomDealing
        exclude = ['realtor']


class ApartmentDealingForm(CommonInput):
    class Meta:
        model = models.ApartmentDealing
        exclude = ['realtor']


class OfficetelDealingForm(CommonInput):
    class Meta:
        model = models.OfficetelDealing
        exclude = ['realtor']


class StoreDealingForm(CommonInput):
    class Meta:
        model = models.StoreDealing
        exclude = ['realtor']


class BuildingDealingForm(CommonInput):
    class Meta:
        model = models.BuildingDealing
        exclude = ['realtor']