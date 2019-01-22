from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
