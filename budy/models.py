from django.db import models
from django.contrib.auth.models import User


class area_Db(models.Model):
    area = models.CharField(max_length=30)

    def __str__(self):
        return "%s" % (self.area)


class exercises_Db(models.Model):
    exercise = models.CharField(max_length=30)
    duration = models.IntegerField()
    rest = models.IntegerField()
    difficulty = models.IntegerField()
    reps = models.IntegerField()
    dateposted = models.DateField()
    area = models.OneToOneField(area_Db,on_delete=models.CASCADE,)

    def __str__(self):
        return self.exercise

    class Meta:
        ordering = ['exercise']
