from django.urls import path
from . import views

urlpatterns = [
    path('setserver/',views.set_up_server, name="ping-set_Server"),
    path('set_up_heartbeat/',views.set_up_heartbeat, name="ping-set_up_heartbeat"),
    path('recv_alive/',views.recv_ping, name="ping-recv_ping"),
    path('send_alive/',views.send_alive_ping, name="ping-send_alive_ping"),
]