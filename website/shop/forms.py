from django import forms
from .models import Customer


class ShippingUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['address', 'city', 'state', 'country', 'zip_code', 'phone', 'nip']
