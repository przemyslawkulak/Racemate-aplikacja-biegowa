from django.db import models

# Create your models here.
from main.models import MyUser

TRAINING_TYPE = (
    (1, 'march'),
    (2, 'easy'),
    (3, 'marathon'),
    (4, 'threshold'),
    (5, 'interval'),
    (6, 'repetition'),
)


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
