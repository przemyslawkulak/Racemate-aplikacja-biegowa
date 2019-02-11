from django.forms import ModelForm, forms

from training.models import PastTraining, TrainingElement


class PastTrainingForm(forms.ModelForm):
    class Meta:
        model = PastTraining
        exclude = ['user']


class AddTreningForm(ModelForm):
    class Meta:
        model = TrainingElement
        fields = ['name', 'time', 'type']
# class PastTrainingForm(forms.Form):
#     name = forms.CharField(max_length=255)
#     time_ = forms.IntegerField()
#     distance_in_km = forms.IntegerField()
#     date = forms.DateTimeField(widget=SelectDateWidget)
#     time = forms.TimeField()
