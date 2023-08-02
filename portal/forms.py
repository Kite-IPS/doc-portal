from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms

# Overriding the default authentication form
class AuthForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-input',
                                                           'id': 'username',
                                                           'placeholder': 'username',
                                                           'autofocus': ''}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'class': 'form-input',
                                          'id': 'password',
                                          'placeholder': 'password',
                                          'autofocus': ''}))

