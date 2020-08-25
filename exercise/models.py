from django.db import models
from django.contrib.auth.models import User
from budy.models import ExercisesDB
from django.utils import timezone

class Exercise(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    exercise = models.ForeignKey(ExercisesDB, on_delete=models.CASCADE, related_name='exercises')
    duration = models.IntegerField()
    rest = models.IntegerField()
    difficulty = models.IntegerField()
    reps = models.IntegerField()
    dateposted = models.DateField(default=timezone.now())

    def __str__(self):
        return "%s (%s)" % (self.exercise, self.user.username)

    def save(self, **kwargs):
        super().save()

    class Meta:
        ordering = ['user']


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    exercise = models.ManyToManyField(Exercise, blank=True)


    def __str__(self):
        return "%s" % (self.user.username)

    def save(self, **kwargs):
        super().save()
        for ex in Exercise.objects.filter(user = self.user):
            self.exercise.add(ex)
            ex.save()

    class Meta:
        ordering = ['user']

