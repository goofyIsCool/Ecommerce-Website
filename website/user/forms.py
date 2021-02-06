from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required')
    first_name = forms.CharField(required=True, label='First name')
    last_name = forms.CharField(required=True, label='Last surname')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
