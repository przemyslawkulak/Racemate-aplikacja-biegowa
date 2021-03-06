from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from racemate.models import PastTraining, Message, TrainingElement, RunningGroup


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class PastTrainingForm(forms.ModelForm):
    class Meta:
        model = PastTraining
        exclude = ['user']


class SendMessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ['sender', 'groupjoin', 'togroup', 'read']


class SendMessageGroupForm(ModelForm):
    class Meta:
        model = Message
        exclude = ['sender', 'groupjoin', 'to', 'read']


class CreateGroupForm(ModelForm):
    class Meta:
        model = RunningGroup
        fields = ['name']


class AddTreningForm(ModelForm):
    class Meta:
        model = TrainingElement
        fields = ['name', 'time', 'type']


class ContactForm(forms.Form):
    subject = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField(label='Your email')
