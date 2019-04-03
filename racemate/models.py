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
    r3 = models.IntegerField(null=True, default=0)
    r5 = models.IntegerField(null=True, default=0)
    r10 = models.IntegerField(null=True, default=0)
    r15 = models.IntegerField(null=True, default=0)
    r21 = models.IntegerField(null=True, default=0)
    r42 = models.IntegerField(null=True, default=0)
    efficiency = models.IntegerField(null=True, default=30)

    def __str__(self):
        return f' {self.username}'


class RunningGroup(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(MyUser, related_name='members')
    admins = models.ManyToManyField(MyUser, related_name='admins')

    @property
    def owner(self):
        return self.admins.first()

    def __str__(self):
        return f'{self.name}'


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

    @property
    def owner(self):
        return self.user

    @property
    def get_time_total_in_hms(self):
        hours = self.time_total // 3600
        minutes = (self.time_total - hours * 3600) // 60
        seconds = self.time_total - hours * 3600 - minutes * 60
        if hours > 0:
            hours = str(hours) + "h "
        else:
            hours = ''
        if minutes > 0:
            minutes = str(minutes) + "min "
        else:
            minutes = ''
        if seconds > 0:
            seconds = str(seconds) + "sec "
        else:
            seconds = ''

        return hours + minutes + seconds

    def __str__(self):
        return f'{self.name} {self.time_total} {self.distance_total}'


class Message(models.Model):
    subject = models.CharField(max_length=256, verbose_name="Temat")
    content = models.TextField(verbose_name="Treść wiadomości", null=True)
    to = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True,
                           null=True, related_name="Adresat", verbose_name="Adresat")
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True,
                               related_name="Nadawca", verbose_name="Nadawca")
    date_sent = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Data wysłania")
    groupjoin = models.ForeignKey(RunningGroup, on_delete=models.CASCADE, null=True, related_name="Join")
    togroup = models.ForeignKey(RunningGroup, on_delete=models.CASCADE, blank=True, null=True,
                                related_name="Message", verbose_name="Wiadomość do grupy")
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.subject} {self.content} {self.groupjoin} {self.read}'
