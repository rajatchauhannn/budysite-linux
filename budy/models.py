from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AreaDB(models.Model):
    area = models.CharField(max_length = 30)

    def __str__(self):
        return self.area

class ExercisesDB(models.Model):
    exercise = models.CharField(max_length=30)
    duration = models.IntegerField()
    rest = models.IntegerField()
    difficulty = models.IntegerField()
    reps = models.IntegerField()
    dateposted = models.DateField(default = timezone.now())
    area = models.OneToOneField(AreaDB, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" %self.exercise

    class Meta:
        ordering = ['exercise']