from django.urls import path
from . import views

urlpatterns = [
    # path('',views.home, name="scheduler-home"),
    path('start/',views.start_schd, name="start-scheduler"),
    path('test/', views.test, name="start-scheduler")
]