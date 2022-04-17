from dataclasses import fields
from django import forms
from . import models


class DateInput(forms.DateInput):
    input_type='date'
    

class ManagementForm(forms.ModelForm):
    contract_day = forms.DateField(widget=DateInput)
    contract_start_day = forms.DateField(widget=DateInput)
    contract_last_day = forms.DateField(widget=DateInput)
    class Meta:
        model = models.Management
        exclude = ['manager']