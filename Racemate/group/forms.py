from django.forms import ModelForm

from group.models import RunningGroup


class CreateGroupForm(ModelForm):
    class Meta:
        model = RunningGroup
        fields = ['name']
