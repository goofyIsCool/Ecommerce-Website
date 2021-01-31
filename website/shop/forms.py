from django import forms
from .models import Customer


class ShippingUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone', 'nip']
