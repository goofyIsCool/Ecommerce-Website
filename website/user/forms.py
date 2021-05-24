from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm

class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input-box',
            'placeholder': 'nazwa użytkownika',
            }
    ))

    email = forms.EmailField(required=True, label='E-mail', widget=forms.TextInput(
        attrs={
            'class': 'input-box',
            'placeholder': 'e-mail',
            }
    ))
    first_name = forms.CharField(required=True, label='Imię', widget=forms.TextInput(
        attrs={
            'class': 'input-box',
            'placeholder': 'imię',
            }
    ))
    last_name = forms.CharField(required=True, label='Nazwisko', widget=forms.TextInput(
        attrs={
            'class': 'input-box',
            'placeholder': 'nazwisko',
            }
    ))

    password1 = forms.CharField(label="Hasło", widget=forms.PasswordInput(
        attrs={
            'class': 'input-box',
            'placeholder': 'passsword',
        }
    ))

    password2 = forms.CharField(label="Potwierdź hasło", widget=forms.PasswordInput(
        attrs={
            'class': 'input-box',
            'placeholder': 'passsword',
        }
    ))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    # TODO Change to e-mail
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input-box',
            'placeholder': 'username',
            }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input-box',
            'placeholder': 'passsword',
        }
    ))

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='Podaj swój adres e-mail', widget=forms.EmailInput(
        attrs={
            'class': 'input-box',
            'placeholder': 'e-mail',
            'type': 'email',
            'name': 'email'
            }
    ))
