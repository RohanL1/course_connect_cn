from django.urls import include
from . import views

"""Rush_Comp_Node URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('broker/', views.assign_task, name="broker-msg"),
    path('set/server/',views.set_server_IP, name='set_server'),
    path('set/neighbour/',views.set_next_and_successor, name='set_neighbour'),
    path('set/leader', views.set_leader, name='set_leader'),
    path('set/broker/', views.set_message_broker, name= 'set_message_broker'),
    path('set/heartbeat/', views.set_heartbeat, name='set_heartbeat'),
    path('heartbeat/alive', views.heartbeat_recv, name='heartbeat_received'),
    path('election/', views.leader_election, name='leader_election'),
    path('elected/', views.leader_elected, name="leader_elected"),
    path('failure/', views.handle_failed_node, name='handle_failed_node')
]
