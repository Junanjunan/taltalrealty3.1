from django import forms
from . import models


class DateInput(forms.DateInput):
    input_type='date'
    

class ContractForm(forms.ModelForm):
    start_day = forms.DateField(widget=DateInput)
    middle_day = forms.DateField(widget=DateInput, required=False)
    last_day = forms.DateField(widget=DateInput)
    class Meta:
        model = models.ContractBase
        exclude = ['realtor']