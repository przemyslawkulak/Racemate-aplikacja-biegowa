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
        return f'{self.id} {self.username} {self.email} '


class RunningGroup(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(MyUser, related_name='members')
    admins = models.ManyToManyField(MyUser, related_name='admins')

    def __str__(self):
        return f'{self.name} {self.admins.name} {self.members}'


class TrainingElement(models.Model):
    name = models.CharField(max_length=255, default='easy')
    time = models.IntegerField()
    distance = models.IntegerField()
    type = models.IntegerField(choices=TRAINING_TYPE)


class Training(models.Model):
    name = models.CharField(max_length=255, null=True)
    trainingElements = models.ManyToManyField(TrainingElement)
    time_total = models.IntegerField(null=True)
    distance_total = models.IntegerField(null=True)
    date = models.DateTimeField(null=True)
    trainingday = models.IntegerField(null=True)
    walk = models.IntegerField(null=True)
    easy = models.IntegerField(null=True)
    marathon = models.IntegerField(null=True)
    threshold = models.IntegerField(null=True)
    interval = models.IntegerField(null=True)
    repetition = models.IntegerField(null=True)
    treningplan = models.CharField(max_length=255, null=True)

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
    to = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, related_name="Adresat", verbose_name="Adresat")
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, related_name="Nadawca", verbose_name="Nadawca")
    date_sent = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Data wysłania")
    groupjoin = models.OneToOneField(RunningGroup, on_delete=models.CASCADE, blank=True, null=True, related_name="Join")
    togroup = models.ForeignKey(RunningGroup, on_delete=models.CASCADE, blank=True, null=True,
                                related_name="Message", verbose_name="Wiadomość do grupy")
