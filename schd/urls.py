from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('start/', views.start_scheduling, name="schedule-taks")
]
