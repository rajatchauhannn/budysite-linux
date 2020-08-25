from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Client, Exercise
from budy.models import ExercisesDB
from django.utils import timezone


@receiver(post_save, sender = User)
def create_client_exercise(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance)
        for currentExercise in ExercisesDB.objects.values_list('exercise', flat = True):
            obj = ExercisesDB.objects.filter(exercise=currentExercise)[0]
            Exercise.objects.create(user=instance,
            exercise = obj,
            duration = obj.duration,
            rest = obj.rest,
            difficulty = obj.difficulty,
            reps = obj.reps,
            dateposted=timezone.now())

        

@receiver(post_save, sender=User)
def save_client(sender, instance, **kwargs):
    instance.client.save()

