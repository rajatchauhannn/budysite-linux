from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'exercise'

urlpatterns = [
    path('', views.index, name='index'),
]