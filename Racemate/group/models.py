from django.db import models

# Create your models here.
from main.models import MyUser


class RunningGroup(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(MyUser, related_name='members')
    admins = models.ManyToManyField(MyUser, related_name='admins')

    def __str__(self):
        return f'{self.name} {self.admins.name} {self.members}'
