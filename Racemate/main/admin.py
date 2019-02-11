from django.contrib import admin

# Register your models here.
from main.models import MyUser, TrainingElement, Training, Message, PastTraining

admin.site.register(MyUser)
admin.site.register(TrainingElement)
admin.site.register(Training)
admin.site.register(Message)
admin.site.register(PastTraining)