from django import forms
from .models import Customer
from django.contrib.auth.models import User


class ShippingUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone', 'nip']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'surname', 'phone']
