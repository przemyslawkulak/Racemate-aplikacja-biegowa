from django.contrib.auth.models import AbstractUser
from django.db import models

TRAINING_TYPE = (
    (1, 'march'),
    (2, 'easy'),
    (3, 'marathon'),
    (4, 'threshold'),
    (5, 'interval'),
    (6, 'repetition'),
)


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
        return f'{self.username} {self.email} '


class RunningGroup(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(MyUser)

    def __str__(self):
        return f'{self.name} {self.members}'


class TrainingElement(models.Model):
    name = models.CharField(max_length=255, default='easy')
    speed = models.IntegerField()
    distance = models.IntegerField()
    type = models.IntegerField(choices=TRAINING_TYPE)


class Training(models.Model):
    name = models.CharField(max_length=255, null=True)
    trainingElements = models.ManyToManyField(TrainingElement)
    time_total = models.IntegerField()
    distance_total = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.name} {self.time_total} {self.distance_total}'


class PastTraining(models.Model):
    name = models.CharField(max_length=255, null=True)
    time_total = models.IntegerField()
    distance_total = models.IntegerField()
    date = models.DateTimeField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.time_total} {self.distance_total}'


class Message(models.Model):
    subject = models.CharField(max_length=256, verbose_name="Temat")
    content = models.TextField(verbose_name="Treść wiadomości", null=True)
    to = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, related_name="Adresat")
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, related_name="Nadawca")
    date_sent = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Data wysłania")
