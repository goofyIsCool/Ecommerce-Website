from django import forms
from .models import Customer
from django.contrib.auth.models import User


class ShippingUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone', 'nip']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input-box',
            'placeholder': 'nazwa użytkownika',
            }
    ))

    email = forms.CharField(label="E-mail",widget=forms.TextInput(
        attrs={
            'class': 'input-box',
            'placeholder': 'email',
            }
    ))

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):

    name = forms.CharField(label="Imię",widget=forms.TextInput(
        attrs={
            'class': 'input-box',
            'placeholder': 'imię',
            }
    ))

    surname = forms.CharField(label="Nazwisko", widget=forms.TextInput(
        attrs={
            'class': 'input-box',
            'placeholder': 'nazwisko',
            }
    ))

    phone = forms.CharField(label="Numer telefonu", widget=forms.TextInput(
        attrs={
            'class': 'input-box',
            'placeholder': 'nr telefonu',
            }
    ))

    class Meta:
        model = Customer
        fields = ['name', 'surname', 'phone']
