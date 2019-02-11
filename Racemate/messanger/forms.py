from django.forms import ModelForm

from messanger.models import Message


class SendMessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ['sender', 'groupjoin', 'togroup']


class SendMessageGroupForm(ModelForm):
    class Meta:
        model = Message
        exclude = ['sender', 'groupjoin', 'to']
