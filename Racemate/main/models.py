from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class MyUser(AbstractUser):
    r3 = models.IntegerField(null=True)
    r5 = models.IntegerField(null=True)
    r10 = models.IntegerField(null=True)
    r15 = models.IntegerField(null=True)
    r21 = models.IntegerField(null=True)
    r42 = models.IntegerField(null=True)
    efficiency = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.id} {self.username} {self.email} '


